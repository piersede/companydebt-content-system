"""Extract stage — the coverage DELTA.

Reads the consolidated answer-engine witnesses and our existing page, and emits
one :class:`ledger.Nugget` per fact that is genuinely ABSENT from our page. This
is discovery, not proof: every commercial figure is flagged for primary
verification downstream and nothing here is fit to publish.

Two design points carried from the manual run (operational learning 2026-06-05):

1. **Cheap model.** The delta is a constrained reading task, so it runs on
   ``gemini-2.5-flash``, not Opus. Opus is reserved for the human judgement and
   drafting that happen AFTER verification.

2. **The already-covered guard.** A candidate is only "missing" if it is absent
   from our page BODY *and* its JSON-LD. The JSON-LD matters because
   ``corpus.html_to_text`` strips ``<script>`` tags, so a fact can be invisible
   in prose yet present in the ItemList / FAQPage / Article schema. The manual
   run false-flagged "we never state Amex's 29.1% rate" for exactly this reason;
   the body already covered it. We build the page and feed the schema blocks into
   the comparison context so the model cannot re-flag a fact we already ship.
"""

from __future__ import annotations

import importlib
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

from . import display_formats, sitemap
from .core import REPO_ROOT, gemini_client, read_run_meta, require_key
from .corpus import consolidate_our_page, consolidate_witnesses, latest_run
from .ledger import ARTICLE_STATUSES, Nugget, save_jsonl

# The category vocabulary the extractor must choose from. Keeping it closed (the
# display-format taxonomy's keys) is what lets `display_formats.default_format`
# seed a render-aware format for every nugget.
ALLOWED_CATEGORIES = list(display_formats.DEFAULT_FORMAT_BY_CATEGORY.keys())

# Categories whose facts are statutory, financial or consequential and must be
# primary-verified before they can touch copy. Anything outside this set still
# gets verification forced if the detail itself carries a hard signal (see
# `_needs_verification`).
_MUST_VERIFY_CATEGORIES = {
    "Cost / Fees", "Timeline / Duration", "Eligibility / Criteria",
    "Director Liability / Personal Risk", "Consequences / Aftermath",
    "Creditor / HMRC Treatment", "Legal / Regulatory", "Statistics / Data",
}

# Hard-claim signals in the detail text itself. Any hit forces primary
# verification even for a softly-categorised nugget (e.g. a "Process" step that
# names a statutory deadline, a voting threshold or a director-liability test).
# Note the word-form thresholds (half/majority/two-thirds...) and voting terms:
# the CVA voting-rule false-pass slipped through because the threshold was
# written in words, not digits or "%".
_FIGURE_SIGNALS = re.compile(
    r"(%|£|\bs\.?\s?\d|section\s\d|\bact\b|\brule\b|\bregulation\b|"
    r"\bday(?:s)?\b|\bweek(?:s)?\b|\bmonth(?:s)?\b|\byear(?:s)?\b|"
    r"liabl|disqualif|wrongful|fraudulent|misfeasance|preferential|"
    r"penalt|threshold|hmrc|guarantee|\bmust\b|require|\d|"
    r"\bhalf\b|\bmajority\b|\bquorum\b|\bunanim|two[- ]thirds|three[- ]quarters|"
    r"\bvote(?:s|d)?\b|\bresolution\b|\bapprov|\bqualif|\beligib)",
    re.I,
)


EXTRACT_DELTA = """\
You are running a COVERAGE DELTA for an existing UK guide about company
insolvency, company debt, or director responsibilities, for answer-engine
optimisation (AEO/GEO). The goal is NOT fact-checking. The goal is to make our
page the most COMPREHENSIVE, citable answer for this query so the engines cite
US. So you are hunting the material the engines surface that our page lacks or
under-covers — correction of a wrong figure is a secondary safety net, not the
main job.

Target keyword: {keyword}
Market: United Kingdom (company / corporate insolvency). Language: en-GB.

You are given four blocks:
1. CITED-SOURCE LANDSCAPE — which domains ChatGPT and Gemini grounded their
   answers on for this query, and whether WE are already cited. Where a
   competitor domain (a rival adviser, a .gov.uk page, an IP firm) wins a query,
   that is a coverage gap to read for.
2. WITNESSES — what ChatGPT and Gemini actually say for this query, each with the
   sources it cited. Discovery material; some may be wrong or out of date. Do NOT
   treat it as true.
3. OUR PAGE (prose) — the visible text of our existing page.
4. OUR PAGE (structured data / JSON-LD) — schema blocks that ALSO render facts on
   our page (comparison list items, FAQs, article metadata). A fact present here
   counts as ALREADY COVERED even if it is not obvious in the prose.

What counts as a coverage delta (ADDITIVE-FIRST — this is the priority order):
- A SUB-QUESTION or ANGLE the engines answer that our page does not (e.g. "what
  happens to the director's loan account?", "can I start a new company with the
  same name?", "does HMRC get paid before the bank?", "what if I gave a personal
  guarantee?", "how long does it actually take from first call to closure?").
- A PROCESS step, ELIGIBILITY test, or DOCUMENT the engines describe that we omit
  or only mention in passing (the order of steps, who files what, who pays).
- A FRAMING / POSITIONING the engines use that we miss (when one route beats
  another, who each route is really for, the common misconception to correct).
- A statutory / financial SPECIFIC (threshold, deadline, fee, liability test,
  creditor-ranking rule, time-bar) we lack.
- A fact present on our page but materially WRONG / OUTDATED vs the witnesses
  (correction — secondary, not the main job).

CRITICAL — the already-covered guard (prevents on-page duplication):
- Before listing anything, scan BOTH our-page blocks (prose AND JSON-LD). If the
  fact, figure, sub-question or its equivalent already appears in either, DROP it.
- If we touch the topic but only shallowly (one passing sentence) while the
  engines/cited sources cover it in depth, KEEP it but set article_status to
  "present_but_weak" and frame it as DEEPEN-EXISTING, not add-new.
- If our page states something the witnesses contradict, keep it and set
  article_status to "outdated" or "contradicted"; say what we currently show.

CRITICAL — self-deduplication (prevents a fact-dump):
- One object per ATOMIC, DISTINCT point. Do NOT emit near-duplicates.
- When the engines give CONFLICTING VALUES for the same fact (e.g. a CVL quoted
  at £4,000, £5,000 and £6,000), emit ONE object capturing the RANGE
  ("£4,000-£6,000") with article_status reflecting that it needs verification —
  never one object per value.
- Group by the underlying point, not the sentence. A strong run is a SHORT list
  of real gaps, not hundreds of fragments.

For each delta return an object with these fields:
- detail: ONE self-contained line — entity/route + claim/angle + qualifier (e.g.
  "A Creditors' Voluntary Liquidation must be confirmed by a shareholders'
  resolution requiring a 75% majority by value"). Preserve qualifiers ("usually",
  "from", "in most cases", "subject to").
- category: choose EXACTLY ONE from this list: {categories}
- provider: the entity or insolvency route the fact concerns (e.g. "Creditors'
  Voluntary Liquidation", "Administration", "HMRC", "The Insolvency Service"), or
  "General" if it is not route-specific. Use the term a reader would recognise.
- card_name: the specific procedure, document or legal provision the fact is
  specific to (e.g. "winding-up petition", "s.216 Insolvency Act 1986"), else "".
- value: the headline figure, threshold, range or timeline if any (e.g.
  "£10,000", "75%", "21 days", "up to 6 years"), else "".
- mentioned_by: list of witness labels that surfaced it (copy the bracketed
  "[engine · label]" headers verbatim). More labels = stronger demand signal.
- source_urls: any cited URLs the witness attached to this fact (else []).
- article_status: present_but_weak | missing | outdated | unsupported | buried |
  contradicted. Use "missing" only for a genuinely net-new gap.
- why_it_matters: one short clause on the decision impact for a director (kept
  out of the ledger; helps you self-check relevance — drop trivia).

Rules:
- Do NOT invent figures, deadlines or statutory references. Only list what a
  witness actually stated; the verification stage will check it against authority.
- Do NOT restate definitions or advice our page already gives.
- Prefer DEEPEN-EXISTING (present_but_weak) over add-new wherever the topic is
  already on the page in any form.
- This is YMYL content: when a witness states a legal/liability claim, capture it
  but expect it to be primary-verified before it can be used.

Return a single JSON array of objects. No prose before or after it.

=== CITED-SOURCE LANDSCAPE ===
{landscape}

=== WITNESSES ===
{witnesses}

=== OUR PAGE (prose) ===
{our_prose}

=== OUR PAGE (structured data / JSON-LD) ===
{our_jsonld}
"""


def _page_jsonld(slug: str) -> str:
    """Build the page in-process and return its JSON-LD schema blocks as one
    readable string. Returns "" if the build is unavailable for any reason —
    the guard then degrades to a prose-only check rather than crashing."""
    scripts_dir = REPO_ROOT / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    try:
        build_page = importlib.import_module("build_page")
        html, _cfg = build_page.build_page(slug)
    except Exception as exc:  # build problems must not block discovery
        return f"(JSON-LD unavailable: {type(exc).__name__}: {exc})"
    blocks = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    pretty: list[str] = []
    for b in blocks:
        try:
            pretty.append(json.dumps(json.loads(b), ensure_ascii=False, indent=1))
        except Exception:
            pretty.append(b.strip())
    return "\n\n".join(pretty)


def _salvage_objects(body: str) -> list[dict[str, Any]]:
    """Recover every complete top-level ``{...}`` object from the inside of a
    JSON array, even when the array itself is truncated (model hit its output
    token cap) or otherwise un-parseable as a whole. String-aware so braces and
    brackets inside URL/quote values do not corrupt depth tracking."""
    objs: list[dict[str, Any]] = []
    depth = 0
    in_str = False
    esc = False
    obj_start = -1
    for i, ch in enumerate(body):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            if depth == 0:
                obj_start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and obj_start != -1:
                chunk = body[obj_start:i + 1]
                try:
                    parsed = json.loads(chunk)
                    if isinstance(parsed, dict):
                        objs.append(parsed)
                except Exception:
                    pass  # skip the one malformed object, keep going
                obj_start = -1
    return objs


def _coerce_array(text: str) -> list[dict[str, Any]]:
    """Pull the outermost JSON array out of a model reply, tolerating code
    fences and stray prose. Falls back to object-by-object salvage when the
    array is truncated or invalid, so a single over-long reply that blows the
    model's output-token cap never silently yields zero nuggets — which matters
    more now the additive-first prompt produces a larger candidate set."""
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()
    start = cleaned.find("[")
    if start == -1:
        return []
    # Fast path: a well-formed, fully-closed array.
    depth = 0
    in_str = False
    esc = False
    for i in range(start, len(cleaned)):
        ch = cleaned[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                try:
                    obj = json.loads(cleaned[start:i + 1])
                    if isinstance(obj, list):
                        return obj
                except Exception:
                    break  # malformed despite balanced brackets -> salvage
                break
    # Salvage path: array was truncated (no closing ]) or failed to parse.
    salvaged = _salvage_objects(cleaned[start:])
    if salvaged:
        print(
            f"[extract] WARNING: outer JSON array was truncated/invalid; "
            f"salvaged {len(salvaged)} complete object(s) from the reply. "
            f"The model likely hit its output-token cap - some tail nuggets "
            f"may be lost.",
            file=sys.stderr,
        )
    return salvaged


def _landscape_summary(run: Path) -> str:
    """Compact, deterministic cited-source landscape for the extract prompt.

    Built from the run's raw witnesses (no model, no live call). Tells the delta
    model whether we are already cited and which domains win the query, so it
    reads the witnesses query-first instead of figure-first.
    """
    try:
        from .source_landscape import OUR_DOMAIN, build_landscape
        land = build_landscape(run)
    except Exception:
        return "(source landscape unavailable)"
    lines: list[str] = []
    if land.get("we_cited"):
        on = ", ".join(land.get("we_cited_on", []))
        lines.append(f"We ({OUR_DOMAIN}) ARE already cited, on: {on or 'some queries'}. "
                     "Defend and widen the lead by closing gaps competitors answer.")
    else:
        lines.append(f"We ({OUR_DOMAIN}) are NOT cited for this query. The domains "
                     "below take the citation; closing their coverage gaps gets us in.")
    comp = land.get("competitors", [])[:10]
    if comp:
        lines.append("Most-cited domains (domain: #queries): "
                     + ", ".join(f"{d}: {c}" for d, c in comp))
    return "\n".join(lines)


def _needs_verification(category: str, detail: str) -> bool:
    """A nugget needs primary verification if its category is statutory/financial/
    consequential OR its text carries a hard claim signal (figure, deadline,
    legal provision, liability term). Soft editorial framing with no such signal
    does not."""
    if category in _MUST_VERIFY_CATEGORIES:
        return True
    return bool(_FIGURE_SIGNALS.search(detail or ""))


def _to_nugget(idx: int, raw: dict[str, Any]) -> Nugget | None:
    detail = str(raw.get("detail", "")).strip()
    if not detail:
        return None
    category = str(raw.get("category", "")).strip()
    if category not in ALLOWED_CATEGORIES:
        category = ""  # keep the nugget; default_format falls back gracefully
    status = str(raw.get("article_status", "missing")).strip()
    if status not in ARTICLE_STATUSES:
        status = "missing"
    mentioned = raw.get("mentioned_by") or []
    if isinstance(mentioned, str):
        mentioned = [mentioned]
    urls = raw.get("source_urls") or []
    if isinstance(urls, str):
        urls = [urls]
    needs_verify = _needs_verification(category, detail)
    return Nugget(
        detail_id=f"n{idx}",
        detail=detail,
        category=category,
        provider=str(raw.get("provider", "")).strip(),
        card_name=str(raw.get("card_name", "")).strip(),
        value=str(raw.get("value", "")).strip(),
        source_urls=[str(u) for u in urls],
        mentioned_by=[str(m) for m in mentioned],
        article_status=status,
        recommended_display_format=display_formats.default_format(category),
        needs_primary_verification=needs_verify,
        # Commercial facts must carry a visible primary source and last-checked
        # date when they reach the page (presentation doc, sections 7-8 + the
        # citation-ready fact pattern).
        source_required=needs_verify,
        last_checked_required=needs_verify,
    )


def _gemini_delta(prompt: str, model: str, *, attempts: int = 5) -> str:
    from google import genai
    from google.genai import errors as genai_errors

    client = gemini_client()
    # No search tool: this is a constrained reading/reasoning pass over the text
    # we supply, not a live lookup. Grounding belongs to the verify stage.
    # The additive-first delta can emit a large candidate set; lift the output cap
    # well above the default so the JSON array is not truncated mid-object (the
    # salvage parser in _coerce_array is the backstop if it still overflows).
    try:
        from google.genai import types as genai_types

        config = genai_types.GenerateContentConfig(max_output_tokens=65535)
    except Exception:
        config = None
    # Fail fast on 5xx: short backoff so a throttled Gemini does not hang the run.
    last: Exception | None = None
    for i in range(attempts):
        try:
            if config is not None:
                resp = client.models.generate_content(
                    model=model, contents=prompt, config=config)
            else:
                resp = client.models.generate_content(model=model, contents=prompt)
            return getattr(resp, "text", "") or ""
        except genai_errors.ServerError as exc:  # 5xx high-demand spikes are transient
            last = exc
            time.sleep(min(2 ** i * 3, 12))
    raise last if last else RuntimeError("gemini delta call failed")


def extract_nuggets(slug: str, *, model: str = "gemini-2.5-flash",
                    run_dir: Path | None = None,
                    concept_guard: bool = True,
                    semantic_guard: bool = False) -> tuple[list[Nugget], Path]:
    """Run the delta pass for ``slug`` and write ``processed/nuggets.jsonl``.

    Returns (nuggets, path). Uses the latest capture run unless ``run_dir`` is
    given. Rebuilds witnesses.md / our-page.txt from the run if either is absent.

    The cited-source landscape is injected into the prompt so the delta is read
    query-first (close the gaps competitor domains win), not figure-first. After
    the model, a deterministic concept-aware guard (``concept_guard``) drops any
    residual nugget the page already expresses under different words, while
    hard-protecting figures and corrections. ``semantic_guard`` adds an opt-in
    Gemini-embedding pass (extra API calls).
    """
    run = run_dir or latest_run(slug)
    meta = read_run_meta(run)
    keyword = meta.get("keyword") or slug.replace("__", " ").replace("-", " ")

    witnesses_path = run / "processed" / "witnesses.md"
    if not witnesses_path.exists():
        consolidate_witnesses(run)
    witnesses = witnesses_path.read_text(encoding="utf-8")

    # "Our page" is the live snapshot taken at capture time (raw/our-page.html).
    live_html_path = run / "raw" / "our-page.html"
    our_page_path = run / "processed" / "our-page.txt"
    if not our_page_path.exists() and live_html_path.exists():
        consolidate_our_page(run, live_html_path)
    our_prose = our_page_path.read_text(encoding="utf-8") if our_page_path.exists() else ""

    # JSON-LD from the REAL rendered page (the already-covered guard). Falls back
    # to a local build only for legacy slug-based runs with no live snapshot.
    if live_html_path.exists():
        our_jsonld = sitemap.extract_jsonld(live_html_path.read_text(encoding="utf-8"))
    else:
        our_jsonld = _page_jsonld(slug)

    # The full page text the deterministic guard scans = visible prose + schema.
    page_text = "\n\n".join(
        t for t in (our_prose, our_jsonld)
        if t and not t.startswith("(JSON-LD unavailable"))

    prompt = EXTRACT_DELTA.format(
        keyword=keyword,
        categories=", ".join(ALLOWED_CATEGORIES),
        landscape=_landscape_summary(run),
        witnesses=witnesses,
        our_prose=our_prose or "(our page prose unavailable — rely on the structured data block)",
        our_jsonld=our_jsonld,
    )
    reply = _gemini_delta(prompt, model)
    raw_items = _coerce_array(reply)

    nuggets: list[Nugget] = []
    for i, raw in enumerate(raw_items, 1):
        if isinstance(raw, dict):
            n = _to_nugget(i, raw)
            if n is not None:
                nuggets.append(n)

    # Deterministic concept-aware already-covered guard: drop nuggets the page
    # already covers under different vocabulary (protecting figures + corrections).
    parsed = len(nuggets)
    suppressed = 0
    if concept_guard and page_text:
        from . import concept_guard as cg

        result = cg.guard_nuggets(nuggets, page_text, semantic=semantic_guard, model=model)
        nuggets = result.kept
        suppressed = len(result.suppressed)
        _write_guard_sidecar(run, result)
        print(f"[concept-guard] {result.counts}", file=sys.stderr)

    out = save_jsonl(nuggets, run / "processed" / "nuggets.jsonl")
    # Keep the raw model reply for audit/debug (discovery transparency).
    (run / "processed" / "nuggets-raw.txt").write_text(reply, encoding="utf-8")
    # Truncation reconciliation: with the guard active, suppressed nuggets move to
    # already-covered.jsonl, so raw "detail" count ~= nuggets.jsonl + already-covered.
    raw_details = reply.count('"detail":')
    print(f"[extract] raw details={raw_details} parsed={parsed} "
          f"(kept={len(nuggets)}, guard-suppressed={suppressed})",
          file=sys.stderr)
    return nuggets, out


def _write_guard_sidecar(run: Path, result: "Any") -> None:
    """Record what the concept guard suppressed (and why) for audit transparency:
    a JSONL of the dropped nuggets and a short human-readable summary."""
    from . import concept_guard as cg

    proc = run / "processed"
    proc.mkdir(parents=True, exist_ok=True)
    rows = cg.suppressed_records(result)
    with (proc / "already-covered.jsonl").open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    lines = [f"# Already-covered guard — {result.counts}", ""]
    for n, reason in result.suppressed:
        prov = f"{n.provider} " if n.provider else ""
        lines.append(f"- [{reason}] ({n.article_status}) {prov}{n.detail}")
    (proc / "already-covered.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
