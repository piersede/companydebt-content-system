"""Recommend stage — turn the VERIFIED ledger into render-aware editorial actions.

Input: ``processed/verified-ledger.jsonl`` (Nuggets with verify fields filled).
Output: ``reports/06-recommended-edits.md`` for human review.

Three hard rules:

1. **Only publishable nuggets become recommendations.** A nugget informs copy
   only if it is verified (or it is a non-commercial angle that did not need
   primary verification). Everything else — contradicted, not_found,
   manual_review — is listed under a "Needs verification" heading and is never
   drafted into page copy. This is the discovery-not-proof discipline.

2. **Additive-first + judicious (the AEO/GEO convergence layer).** Verified
   nuggets are deduped (so conflicting values of one fact, and phrasing variants,
   collapse to one), ranked (coverage angles and multi-engine gaps first, raw
   figures last), clustered by the model (so differently-worded duplicates merge),
   and diversity-capped (no single theme dominates). The top ``max_gaps`` are the
   apply list; the rest drop to an appendix. This is what stops the run regressing
   into a flat, hundred-item fact-dump.

3. **Anti-cannibalisation.** Before recommending we ADD a fact, we check that
   another companydebt.com page does not already own it (which would split the
   citation authority we are trying to win). Flagged items are kept but marked
   "link, don't duplicate".
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any

from . import display_formats, prompts
from .core import gemini_client, read_run_meta
from .corpus import latest_run
from .ledger import ARTICLE_STATUSES, Nugget, load_jsonl

_PRIORITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}

# Default ceiling on the headline "coverage gaps to close" list. The full deduped
# ledger stays in an appendix; this caps what an editor is asked to APPLY, so a
# busy page yields a judicious shortlist, not a fact-dump.
DEFAULT_MAX_GAPS = 10

# Status weights for ranking. present_but_weak (deepen-existing) and missing
# (net-new) are the additive-coverage core; corrections rank below them, except
# contradicted (our page states something FALSE) which ranks with the gaps.
_STATUS_WEIGHT = {
    "missing": 3, "present_but_weak": 3, "contradicted": 3, "buried": 2,
    "outdated": 2, "unsupported": 1, "present": 0, "not_relevant": 0,
}

# Categories that ARE additive coverage angles (a sub-question, a process, a
# framing, a comparison) rather than a raw statutory/cost figure. Additive-first:
# these rank UP; pure figure categories (Cost / Fees, Timeline / Duration,
# Statistics / Data) rank down. Names mirror display_formats.DEFAULT_FORMAT_BY_CATEGORY
# (CD's existing insolvency categories + the three AEO-native angle categories).
_COVERAGE_CATEGORIES = {
    # AEO-native angle categories (added to display_formats in this reframe):
    "Coverage Gap", "Sub-Question", "Framing / Positioning",
    # Existing insolvency categories that are angles, not raw figures:
    "Process / Steps", "Route Comparison", "Alternatives / Options",
    "FAQs / User Questions", "Risks / Pitfalls", "Consequences / Aftermath",
    "Director Liability / Personal Risk",
}

_RATE = re.compile(r"(\d+(\.\d+)?\s*%)|(£\s*\d)|(\b\d+\s*p\b)|(\bAER\b)|(\bAPR\b)", re.I)

# en-GB stop-words stripped before building a dedup signature, so two phrasings
# of the same point collapse to one.
_STOP = {
    "the", "a", "an", "and", "or", "of", "to", "for", "on", "in", "at", "by",
    "with", "is", "are", "be", "per", "from", "up", "as", "it", "its", "this",
    "that", "you", "your", "they", "their", "has", "have", "but", "not", "no",
    "if", "when", "than", "then", "also", "any", "all", "each", "into", "via",
}


def _signature(provider: str, detail: str) -> str:
    """A normalised content-word signature for near-dup collapse. Digits and
    punctuation are dropped so conflicting VALUES of the same fact (a CVL quoted
    at £4k vs £6k) map to one signature; stop-words are dropped so phrasing
    variants collapse."""
    words = re.findall(r"[a-z]+", (detail or "").lower())
    sig = sorted({w for w in words if w not in _STOP and len(w) > 2})
    return (provider or "").strip().lower() + "|" + " ".join(sig)


def _is_rate_only(n: "Nugget") -> bool:
    """A pure figure (cost/percentage with no additive angle) — deprioritised."""
    if n.category in _COVERAGE_CATEGORIES:
        return False
    return bool(_RATE.search(n.value or "")) or bool(_RATE.search(n.detail or ""))


def _score(n: "Nugget") -> int:
    s = _STATUS_WEIGHT.get(n.article_status, 1) * 2
    s += min(len(n.mentioned_by), 4)              # cross-engine demand signal
    if n.category in _COVERAGE_CATEGORIES:
        s += 3                                     # additive-first
    if _is_rate_only(n):
        s -= 2                                     # raw figures rank down
    return s


def _dedupe(nuggets: list["Nugget"]) -> list["Nugget"]:
    """Collapse near-duplicates by content-word signature, keeping the
    highest-scoring representative and merging its siblings' engine mentions and
    source URLs (so the demand/citation signal is not lost). Prevents both the
    conflicting-value fan-out and phrasing-variant duplication."""
    best: dict[str, "Nugget"] = {}
    for n in nuggets:
        key = _signature(n.provider, n.detail)
        cur = best.get(key)
        if cur is None:
            best[key] = n
            continue
        keep, drop = (cur, n) if _score(cur) >= _score(n) else (n, cur)
        for m in drop.mentioned_by:
            if m not in keep.mentioned_by:
                keep.mentioned_by.append(m)
        for u in drop.source_urls:
            if u not in keep.source_urls:
                keep.source_urls.append(u)
        best[key] = keep
    return list(best.values())


def _cited_domains(urls: list[str]) -> list[str]:
    from .source_landscape import _norm_domain
    out: list[str] = []
    for u in urls or []:
        d = _norm_domain(str(u))
        if d and d not in out:
            out.append(d)
    return out


def _scrub(text: str) -> str:
    """Strip em-dashes from any rendered text. The site bans them sitewide; even
    raw discovery text echoed into the report must not carry one (wptexturize
    renders ``--`` as an em-dash, so collapse that form too)."""
    return (text or "").replace("—", ", ").replace("--", ", ")


def _gemini_recommend(prompt: str, model: str, *, attempts: int = 3) -> str:
    from google import genai  # noqa: F401  (kept for parity / explicit dependency)
    from google.genai import errors as genai_errors

    client = gemini_client()
    # Fail fast on 5xx: short backoff so a throttled Gemini does not hang the run.
    last: Exception | None = None
    for i in range(attempts):
        try:
            resp = client.models.generate_content(model=model, contents=prompt)
            return getattr(resp, "text", "") or ""
        except genai_errors.ServerError as exc:
            last = exc
            time.sleep(min(2 ** i * 3, 12))
    raise last if last else RuntimeError("gemini recommend call failed")


def _coerce_array(text: str) -> list[dict[str, Any]]:
    cleaned = re.sub(r"^```(?:json)?", "", text.strip()).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()
    start = cleaned.find("[")
    if start == -1:
        return []
    depth = 0
    for i in range(start, len(cleaned)):
        if cleaned[i] == "[":
            depth += 1
        elif cleaned[i] == "]":
            depth -= 1
            if depth == 0:
                try:
                    obj = json.loads(cleaned[start:i + 1])
                except Exception:
                    return []
                return obj if isinstance(obj, list) else []
    return []


def _enrich_payload(nuggets: list[Nugget]) -> str:
    """Compact JSON the model enriches — only the fields it needs to reason."""
    rows = []
    for n in nuggets:
        rows.append({
            "detail_id": n.detail_id,
            "detail": n.detail,
            "category": n.category,
            "provider": n.provider,
            "card_name": n.card_name,
            "value": n.value,
            "verified_quote": n.verified_quote,
            "verified_source_url": n.verified_source_url,
            "seed_display_format": n.recommended_display_format
            or display_formats.default_format(n.category),
        })
    return json.dumps(rows, ensure_ascii=False, indent=1)


def _enrich_recommendations(nuggets: list[Nugget], *, model: str) -> dict[str, str]:
    """Fill recommended_display_format / recommended_action / priority /
    article_status on each nugget, in place, via one model pass. Also returns a
    ``{detail_id: cluster}`` map: the model groups items that make the SAME
    underlying point under one kebab cluster label, so semantically-equivalent
    but differently-worded duplicates (which the lexical dedup cannot catch)
    collapse to one headline recommendation."""
    if not nuggets:
        return {}
    prompt = (
        prompts.RECOMMEND_EDITS
        + "\n\nReturn a SINGLE JSON array. One object per input nugget, keyed by "
        "detail_id, with exactly these fields: detail_id, cluster (a SHORT kebab "
        "label naming the underlying point, e.g. 'director-loan-account' or "
        "'hmrc-crown-preference'; give items that make the SAME point the IDENTICAL "
        "cluster so duplicates merge, even if worded differently), "
        "recommended_display_format "
        "(one OR MORE formats from the list above; when a fact belongs in two places, "
        "e.g. a route-comparison column AND a warning callout, join them with ' + '), "
        "recommended_action (the smallest useful edit, en-GB plain-English voice, "
        "no em-dashes), article_status "
        "(present_but_weak|missing|outdated|unsupported|buried|contradicted), "
        "priority (low|medium|high|critical), editorial_note (optional one-line steer "
        "for the human applying it). No prose outside the array.\n\n"
        "=== VERIFIED NUGGETS ===\n" + _enrich_payload(nuggets)
    )
    reply = _gemini_recommend(prompt, model)
    by_id = {str(r.get("detail_id")): r for r in _coerce_array(reply) if isinstance(r, dict)}
    clusters: dict[str, str] = {}
    for n in nuggets:
        r = by_id.get(n.detail_id)
        if not r:
            continue
        cl = str(r.get("cluster", "")).strip().lower()
        if cl:
            clusters[n.detail_id] = cl
        # Accept one or more formats; normalise doc aliases; keep the compound.
        formats = display_formats.split_formats(str(r.get("recommended_display_format", "")))
        if formats:
            n.recommended_display_format = " + ".join(formats)
        action = str(r.get("recommended_action", "")).strip()
        if action:
            n.recommended_action = _scrub(action)  # site bans em-dashes in copy
        status = str(r.get("article_status", "")).strip()
        if status in ARTICLE_STATUSES:
            n.article_status = status
        prio = str(r.get("priority", "")).strip().lower()
        if prio in _PRIORITY_RANK:
            n.priority = prio
        note = str(r.get("editorial_note", "")).strip()
        if note:
            n.editorial_note = _scrub(note)
    return clusters


def _render_gap(lines: list[str], n: Nugget) -> None:
    """Render one headline coverage gap as a compact, apply-ready block."""
    card = f" ({n.card_name})" if n.card_name else ""
    deepen = n.article_status in ("present_but_weak", "buried")
    mode = "DEEPEN EXISTING" if deepen else (
        "CORRECT" if n.article_status in ("outdated", "contradicted") else "ADD")
    src = f" _( {n.verified_source_url} )_" if n.verified_source_url else ""
    lines.append(
        f"- **[{mode}] [{n.priority}] {n.category}{card}** "
        f"`{n.recommended_display_format}`")
    lines.append(f"  - Gap: {_scrub(n.detail)}")
    if n.cannibalisation_risk:
        lines.append(
            f"  - **[CANNIBALISATION RISK]** another companydebt.com page already "
            f"covers this: {n.cannibal_owner_url} . Do NOT duplicate it here; link "
            f"to that page so it stays the single source we get quoted for.")
    if n.recommended_action:
        verb = "Link" if n.cannibalisation_risk else "Edit"
        lines.append(f"  - {verb}: {_scrub(n.recommended_action)}")
    if n.editorial_note:
        lines.append(f"  - Note: {_scrub(n.editorial_note)}")
    if deepen:
        lines.append("  - Page status: present_but_weak — extend the existing "
                     "line/section; do NOT add a new block.")
    # Who currently wins this citation (the GEO rationale), if the witnesses
    # attached sources.
    cited = _cited_domains(n.source_urls)
    if cited:
        lines.append(f"  - Currently covered by: {', '.join(cited[:5])}")
    if n.verified_quote:
        lines.append(f"  - Verified: \"{_scrub(n.verified_quote.strip())}\"{src}")
    elif src:
        lines.append(f"  - Source:{src}")
    if n.source_required or n.last_checked_required:
        bits = []
        if n.last_checked_required:
            bits.append(f"Details last checked: {n.verify_date or '[set on publish]'}")
        if n.source_required:
            bits.append("cite the primary source on the page"
                        if not n.verified_source_url
                        else f"primary source: {n.verified_source_url}")
        lines.append(f"  - Must show: {'; '.join(bits)}")
    lines.append("")


def _render_markdown(keyword: str, run_id: str, headline: list[Nugget],
                     appendix: list[Nugget], needs_verify: list[Nugget],
                     max_gaps: int) -> str:
    lines: list[str] = [
        f"# Recommended edits: {keyword}",
        "",
        f"**Run:** {run_id}  ",
        "**Approach:** additive-first AEO. Section 1 is the JUDICIOUS shortlist to "
        f"apply (capped at {max_gaps}), ranked by how many engines raised it and "
        "whether it is a real gap. Coverage angles rank above raw figures.  ",
        "**Discipline:** answer-engine output is discovery, not proof; every item "
        "in section 1 is primary-source verified. DEEPEN-EXISTING beats add-new; "
        "no item duplicates the page or another item. Unverified material is "
        "quarantined in section 3 and must NOT be drafted into copy.",
        "",
        "Review per item: flag anything to cut, merge or reword before any patch.",
        "",
        "---",
        "",
        f"## 1. Coverage gaps to close (apply list, max {max_gaps})",
        "",
    ]
    if not headline:
        lines.append("_No verified coverage gaps to recommend in this run._\n")
    else:
        # Theme the shortlist by category so related gaps sit together.
        groups: dict[str, list[Nugget]] = {}
        for n in headline:
            groups.setdefault(n.category or "General", []).append(n)
        for theme in sorted(groups):
            lines.append(f"### {theme}")
            lines.append("")
            for n in sorted(groups[theme], key=lambda n: _PRIORITY_RANK.get(n.priority, 2)):
                _render_gap(lines, n)
    lines += [
        "---",
        "",
        "## 2. Lower-priority / deduped ledger (NOT the apply list)",
        "",
        "Verified but below the cap, or pure figures that belong in a values "
        "verification run, not an AEO pass. Pull one up into section 1 only if you "
        "judge it a real gap. Already deduplicated against section 1.",
        "",
    ]
    if not appendix:
        lines.append("_Nothing below the cap._\n")
    else:
        lines.append("| Provider | Category | Detail | Status |")
        lines.append("|---|---|---|---|")
        for n in sorted(appendix, key=lambda n: (n.provider, n.category)):
            detail = _scrub(n.detail.replace("|", "/"))
            lines.append(f"| {n.provider} | {n.category} | {detail} | {n.article_status} |")
        lines.append("")
    lines += [
        "---",
        "",
        "## 3. Needs verification (NOT page copy)",
        "",
        "Could not be confirmed against a primary source, or contradicted. Stays "
        "out of copy until a human confirms it. Ready-to-paste browser prompts are "
        "in `reports/04-provider-verification-needed.csv`.",
        "",
    ]
    if not needs_verify:
        lines.append("_Nothing outstanding._\n")
    else:
        lines.append("| Provider | Category | Detail | Status | Notes |")
        lines.append("|---|---|---|---|---|")
        for n in sorted(needs_verify, key=lambda n: (n.provider, n.category)):
            note = _scrub((n.notes or "").replace("|", "/").strip())
            detail = _scrub(n.detail.replace("|", "/"))
            lines.append(
                f"| {n.provider} | {n.category} | {detail} | "
                f"{n.verification_status} | {note} |")
        lines.append("")
    lines += [
        "---",
        "",
        "_AI engines were discovery only; every item in section 1 is "
        "primary-verified. Apply-to-live stays human-reviewed via Bernstein "
        "`patch --humanise-note`, staging only._",
    ]
    return "\n".join(lines) + "\n"


def recommend_edits(slug: str, *, model: str = "gemini-2.5-flash",
                    run_dir: Path | None = None,
                    ledger_path: Path | None = None,
                    max_gaps: int = DEFAULT_MAX_GAPS,
                    cannibal_max_live: int | None = 20) -> tuple[Path, dict[str, int]]:
    """Generate ``reports/06-recommended-edits.md`` from the verified ledger.

    Additive-first + judicious: the verified nuggets are deduped, ranked
    (coverage angles and multi-engine gaps first, raw figures last), clustered and
    the top ``max_gaps`` become the apply list; the rest drop to an appendix. Only
    the shortlist is enriched and cannibalisation-checked. Returns (path, counts).
    """
    run = run_dir or latest_run(slug)
    meta = read_run_meta(run)
    keyword = meta.get("keyword") or slug.replace("__", " ").replace("-", " ")
    target_url = meta.get("url", "")
    path = ledger_path or (run / "processed" / "verified-ledger.jsonl")
    if not path.exists():
        raise RuntimeError(
            f"No verified ledger at {path}. Run the verify stage first.")

    nuggets = load_jsonl(path)
    publishable = _dedupe([n for n in nuggets if n.is_publishable])
    needs_verify = _dedupe([n for n in nuggets if not n.is_publishable])

    # Rank: additive coverage angles + multi-engine gaps first, figures last.
    publishable.sort(key=_score, reverse=True)

    # Enrich a candidate POOL (wider than the cap) in one model pass; the model
    # also clusters semantically-equivalent items so differently-worded duplicates
    # (which the lexical dedup misses) collapse to one. Keep the highest-scoring
    # representative per cluster.
    pool = publishable[:max(max_gaps * 3, max_gaps)]
    clusters = _enrich_recommendations(pool, model=model)

    seen_clusters: set[str] = set()
    reps: list[Nugget] = []
    pooled_dups: list[Nugget] = []
    for n in pool:  # pool is score-desc, so first per cluster is the best
        key = clusters.get(n.detail_id) or f"_id:{n.detail_id}"
        if key in seen_clusters:
            pooled_dups.append(n)        # same point, lower score -> appendix
            continue
        seen_clusters.add(key)
        reps.append(n)

    # Diversity cap (deterministic backstop): no single theme/category may
    # dominate the apply list, in case clustering under-merges a busy theme.
    per_theme = max(2, max_gaps // 3)
    headline: list[Nugget] = []
    overflow: list[Nugget] = []
    theme_count: dict[str, int] = {}
    for n in reps:
        theme = n.category or "General"
        if len(headline) < max_gaps and theme_count.get(theme, 0) < per_theme:
            headline.append(n)
            theme_count[theme] = theme_count.get(theme, 0) + 1
        else:
            overflow.append(n)

    # Anti-cannibalisation: only the apply list is checked (keeps the live-call
    # budget tight). Flags, in place, any apply-list fact another of our pages owns.
    if target_url and headline:
        from .cannibal import check_cannibalisation
        check_cannibalisation(headline, target_url, model=model,
                              max_live=cannibal_max_live)

    appendix = overflow + pooled_dups + publishable[len(pool):]

    md = _render_markdown(keyword, run.name, headline, appendix, needs_verify, max_gaps)
    out = run / "reports" / "06-recommended-edits.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    counts = {
        "total": len(nuggets),
        "publishable": len(publishable),
        "headline": len(headline),
        "appendix": len(appendix),
        "needs_verification": len(needs_verify),
        "cannibalisation_risk": sum(1 for n in headline if n.cannibalisation_risk),
    }
    return out, counts
