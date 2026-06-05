"""Recommend stage — turn the VERIFIED ledger into render-aware editorial actions.

Input: ``processed/verified-ledger.jsonl`` (Nuggets with verify fields filled).
Output: ``reports/06-recommended-edits.md`` for human review.

Two hard rules carried from the manual run:

1. **Only publishable nuggets become recommendations.** A nugget informs copy
   only if it is verified (or it is a non-commercial angle that did not need
   primary verification). Everything else — contradicted, not_found,
   manual_review — is listed under a "Needs verification" heading and is never
   drafted into page copy. This is the discovery-not-proof discipline.

2. **Recommendations are render-aware.** Each recommendation carries a
   ``recommended_display_format`` from ``display_formats``; the prompt
   (``prompts.RECOMMEND_EDITS``) bakes in the page shapes a fact can take
   (definition, ordered process steps, risk callout, route-comparison table,
   key-takeaways, FAQ) and the rule that statutory/cost/liability facts carry a
   primary source. The model fills in the action and format per nugget; the
   markdown is rendered deterministically so the structure is stable and auditable.
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any

from . import display_formats, prompts
from .core import require_key, resolve_page
from .corpus import latest_run
from .ledger import ARTICLE_STATUSES, Nugget, load_jsonl

_PRIORITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def _scrub(text: str) -> str:
    """Strip em-dashes from any rendered text. The site bans them sitewide; even
    raw discovery text echoed into the report must not carry one (wptexturize
    renders ``--`` as an em-dash, so collapse that form too)."""
    return (text or "").replace("—", ", ").replace("--", ", ")


def _gemini_recommend(prompt: str, model: str, *, attempts: int = 4) -> str:
    from google import genai
    from google.genai import errors as genai_errors

    client = genai.Client(api_key=require_key("GEMINI_API_KEY"))
    last: Exception | None = None
    for i in range(attempts):
        try:
            resp = client.models.generate_content(model=model, contents=prompt)
            return getattr(resp, "text", "") or ""
        except genai_errors.ServerError as exc:
            last = exc
            time.sleep(min(2 ** i * 5, 40))
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


def _enrich_recommendations(nuggets: list[Nugget], *, model: str) -> None:
    """Fill recommended_display_format / recommended_action / priority /
    article_status on each publishable nugget, in place, via one model pass."""
    if not nuggets:
        return
    prompt = (
        prompts.RECOMMEND_EDITS
        + "\n\nReturn a SINGLE JSON array. One object per input nugget, keyed by "
        "detail_id, with exactly these fields: detail_id, recommended_display_format "
        "(one OR MORE formats from the list above; when a fact belongs in two places, "
        "e.g. a route-comparison column AND a warning callout, join them with ' + '), "
        "recommended_action (the smallest useful edit, en-GB plain-English voice, "
        "no em-dashes), article_status "
        "(present_but_weak|missing|outdated|unsupported|buried|contradicted), "
        "priority (low|medium|high|critical), editorial_note (optional one-line steer "
        "for the human applying it, e.g. label charge vs credit clearly). No prose "
        "outside the array.\n\n"
        "=== VERIFIED NUGGETS ===\n" + _enrich_payload(nuggets)
    )
    reply = _gemini_recommend(prompt, model)
    by_id = {str(r.get("detail_id")): r for r in _coerce_array(reply) if isinstance(r, dict)}
    for n in nuggets:
        r = by_id.get(n.detail_id)
        if not r:
            continue
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


def _render_markdown(keyword: str, run_id: str,
                     publishable: list[Nugget], needs_verify: list[Nugget]) -> str:
    lines: list[str] = [
        f"# Recommended edits: {keyword}",
        "",
        f"**Run:** {run_id}  ",
        "**Discipline:** answer-engine output is discovery, not proof. Every "
        "recommendation below is primary-source verified; unverified nuggets are "
        "quarantined under section 2 and must NOT be drafted into copy.  ",
        "**Render-aware:** each edit names the page shape it belongs in "
        "(definition, ordered process steps, risk callout, route-comparison table, "
        "key-takeaways, or FAQ), and every statutory/cost/liability fact carries a "
        "primary source.",
        "",
        "Review per item: flag anything to cut or reword before any patch to staging.",
        "",
        "---",
        "",
        "## 1. Verified recommendations (smallest useful edit)",
        "",
    ]
    if not publishable:
        lines.append("_No verified nuggets to recommend in this run._\n")
    else:
        # Group by entity/route so each route's edits sit together.
        groups: dict[str, list[Nugget]] = {}
        for n in publishable:
            key = n.provider or "General"
            groups.setdefault(key, []).append(n)
        for provider in sorted(groups):
            items = sorted(groups[provider],
                           key=lambda n: _PRIORITY_RANK.get(n.priority, 2))
            lines.append(f"### {provider}")
            lines.append("")
            for n in items:
                card = f" ({n.card_name})" if n.card_name else ""
                src = f" _( {n.verified_source_url} )_" if n.verified_source_url else ""
                lines.append(
                    f"- **[{n.priority}] {n.category}{card}** "
                    f"`{n.recommended_display_format}`")
                lines.append(f"  - Fact: {_scrub(n.detail)}")
                if n.recommended_action:
                    lines.append(f"  - Edit: {_scrub(n.recommended_action)}")
                if n.editorial_note:
                    lines.append(f"  - Note: {_scrub(n.editorial_note)}")
                if n.article_status and n.article_status != "missing":
                    lines.append(f"  - Page status: {n.article_status}")
                if n.verified_quote:
                    lines.append(f"  - Verified: \"{_scrub(n.verified_quote.strip())}\"{src}")
                elif src:
                    lines.append(f"  - Source:{src}")
                # Citation-ready fact pattern: commercial facts must ship with a
                # visible source + last-checked line (presentation doc sections 7-8).
                if n.source_required or n.last_checked_required:
                    bits = []
                    if n.last_checked_required:
                        bits.append(f"Details last checked: {n.verify_date or '[set on publish]'}")
                    if n.source_required:
                        bits.append("cite the provider's primary source on the page"
                                    if not n.verified_source_url
                                    else f"primary source: {n.verified_source_url}")
                    lines.append(f"  - Must show: {'; '.join(bits)}")
                lines.append("")
    lines += [
        "---",
        "",
        "## 2. Needs verification (NOT page copy)",
        "",
        "These nuggets could not be confirmed against the provider's own site, or "
        "were contradicted. They stay out of copy until a human confirms them. The "
        "ready-to-paste browser prompts are in `reports/04-provider-verification-needed.csv`.",
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
        "_AI engines were discovery only; every figure in section 1 is "
        "provider-verified. Apply-to-live stays human-reviewed via Bernstein "
        "`patch --humanise-note`, staging only._",
    ]
    return "\n".join(lines) + "\n"


def recommend_edits(slug: str, *, model: str = "gemini-2.5-flash",
                    run_dir: Path | None = None,
                    ledger_path: Path | None = None) -> tuple[Path, dict[str, int]]:
    """Generate ``reports/06-recommended-edits.md`` from the verified ledger.

    Returns (report_path, counts)."""
    cfg = resolve_page(slug)
    keyword = cfg.get("title", slug).split(":")[0].strip()
    run = run_dir or latest_run(slug)
    path = ledger_path or (run / "processed" / "verified-ledger.jsonl")
    if not path.exists():
        raise RuntimeError(
            f"No verified ledger at {path}. Run the verify stage first.")

    nuggets = load_jsonl(path)
    publishable = [n for n in nuggets if n.is_publishable]
    needs_verify = [n for n in nuggets if not n.is_publishable]

    _enrich_recommendations(publishable, model=model)

    md = _render_markdown(keyword, run.name, publishable, needs_verify)
    out = run / "reports" / "06-recommended-edits.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    counts = {
        "total": len(nuggets),
        "publishable": len(publishable),
        "needs_verification": len(needs_verify),
    }
    return out, counts
