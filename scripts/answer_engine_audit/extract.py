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

from . import display_formats
from .core import REPO_ROOT, require_key, resolve_page
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
# names a statutory deadline or a director-liability threshold).
_FIGURE_SIGNALS = re.compile(
    r"(%|£|\bs\.?\s?\d|section\s\d|\bact\b|\brule\b|\bregulation\b|"
    r"\bday(?:s)?\b|\bweek(?:s)?\b|\bmonth(?:s)?\b|\byear(?:s)?\b|"
    r"liabl|disqualif|wrongful|fraudulent|misfeasance|preferential|"
    r"penalt|threshold|hmrc|guarantee|\bmust\b|require|\d)",
    re.I,
)


EXTRACT_DELTA = """\
You are running a COVERAGE DELTA for an existing UK guide about company
insolvency, company debt, or director responsibilities.

Target keyword: {keyword}
Market: United Kingdom (company / corporate insolvency). Language: en-GB.

You are given three blocks:
1. WITNESSES — what ChatGPT and Gemini surface for this query, with the sources
   they cited. This is discovery material; some of it may be wrong or out of date.
   Do NOT treat it as true. Your job is only to spot facts the witnesses raise
   that our page does not currently cover.
2. OUR PAGE (prose) — the visible text of our existing page.
3. OUR PAGE (structured data / JSON-LD) — schema blocks that ALSO render facts
   on our page (comparison list items, FAQs, article metadata). A fact present
   here counts as ALREADY COVERED even if it is not obvious in the prose.

Task:
Return ONLY the salient facts that are genuinely ABSENT from BOTH our prose AND
our JSON-LD, or that are present on our page but materially WRONG / OUTDATED
versus what the witnesses surface.

CRITICAL — the already-covered guard:
- Before listing a fact as missing, scan BOTH our-page blocks (prose and
  JSON-LD). If the fact, figure or its equivalent already appears in either,
  DROP it. Do not re-flag facts we already ship.
- If our page states something the witnesses contradict, keep it but set
  article_status to "outdated" or "contradicted" and say what we currently show.

For each fact return an object with these fields:
- detail: ONE self-contained line — entity/route + claim + qualifier (e.g.
  "A Creditors' Voluntary Liquidation must be confirmed by a shareholders'
  resolution requiring a 75% majority by value"). Preserve qualifiers ("usually",
  "from", "in most cases", "subject to").
- category: choose EXACTLY ONE from this list: {categories}
- provider: the entity or insolvency route the fact concerns (e.g. "Creditors'
  Voluntary Liquidation", "Administration", "HMRC", "The Insolvency Service"), or
  "General" if it is not route-specific. Use the term a reader would recognise.
- card_name: the specific procedure, document or legal provision the fact is
  specific to (e.g. "winding-up petition", "s.216 Insolvency Act 1986"), else "".
- value: the headline figure, threshold or timeline if any (e.g. "£10,000",
  "75%", "21 days", "up to 6 years"), else "".
- mentioned_by: list of witness labels that surfaced it (e.g.
  ["gemini · usecase-2"]). Copy the bracketed label headers verbatim.
- source_urls: any cited URLs the witness attached to this fact (else []).
- article_status: one of present_but_weak, missing, outdated, unsupported,
  buried, contradicted. Use "missing" for a genuine gap.
- why_it_matters: one short clause on the decision impact for a director (kept
  out of the ledger; helps you self-check relevance — drop trivia).

Rules:
- Prefer decision-useful specifics: process steps and their order, eligibility/
  criteria, cost and who pays, timelines, director personal liability, creditor/
  HMRC treatment, consequences, and the governing rule or official source.
- Do NOT invent figures, deadlines or statutory references. Only list what a
  witness actually stated; the verification stage will check it against authority.
- Do NOT list generic reassurance, restated definitions, or facts already on our page.
- One object per atomic fact. Aim for completeness over the genuine gaps, not volume.
- This is YMYL content: when a witness states a legal/liability claim, capture it
  but expect it to be primary-verified before it can be used.

Return a single JSON array of objects. No prose before or after it.

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


def _coerce_array(text: str) -> list[dict[str, Any]]:
    """Pull the outermost JSON array out of a model reply, tolerating code
    fences and stray prose."""
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()
    start = cleaned.find("[")
    if start == -1:
        return []
    depth = 0
    for i in range(start, len(cleaned)):
        ch = cleaned[i]
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                try:
                    obj = json.loads(cleaned[start:i + 1])
                except Exception:
                    return []
                return obj if isinstance(obj, list) else []
    return []


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


def _gemini_delta(prompt: str, model: str, *, attempts: int = 4) -> str:
    from google import genai
    from google.genai import errors as genai_errors

    client = genai.Client(api_key=require_key("GEMINI_API_KEY"))
    # No search tool: this is a constrained reading/reasoning pass over the text
    # we supply, not a live lookup. Grounding belongs to the verify stage.
    last: Exception | None = None
    for i in range(attempts):
        try:
            resp = client.models.generate_content(model=model, contents=prompt)
            return getattr(resp, "text", "") or ""
        except genai_errors.ServerError as exc:  # 5xx high-demand spikes are transient
            last = exc
            time.sleep(min(2 ** i * 5, 40))
    raise last if last else RuntimeError("gemini delta call failed")


def extract_nuggets(slug: str, *, model: str = "gemini-2.5-flash",
                    run_dir: Path | None = None) -> tuple[list[Nugget], Path]:
    """Run the delta pass for ``slug`` and write ``processed/nuggets.jsonl``.

    Returns (nuggets, path). Uses the latest capture run unless ``run_dir`` is
    given. Rebuilds witnesses.md / our-page.txt from the run if either is absent.
    """
    cfg = resolve_page(slug)
    keyword = cfg.get("title", slug).split(":")[0].strip()
    run = run_dir or latest_run(slug)

    witnesses_path = run / "processed" / "witnesses.md"
    if not witnesses_path.exists():
        consolidate_witnesses(run)
    witnesses = witnesses_path.read_text(encoding="utf-8")

    our_page_path = run / "processed" / "our-page.txt"
    if not our_page_path.exists():
        # Fall back to a built/cached article HTML if we have one to consolidate.
        article_html = REPO_ROOT / "research" / slug / f"{slug}.html"
        if article_html.exists():
            consolidate_our_page(run, article_html)
    our_prose = our_page_path.read_text(encoding="utf-8") if our_page_path.exists() else ""

    our_jsonld = _page_jsonld(slug)

    prompt = EXTRACT_DELTA.format(
        keyword=keyword,
        categories=", ".join(ALLOWED_CATEGORIES),
        witnesses=witnesses,
        our_prose=our_prose,
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

    out = save_jsonl(nuggets, run / "processed" / "nuggets.jsonl")
    # Keep the raw model reply for audit/debug (discovery transparency).
    (run / "processed" / "nuggets-raw.txt").write_text(reply, encoding="utf-8")
    return nuggets, out
