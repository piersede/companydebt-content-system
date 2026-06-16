"""Verify stage — confirm each commercial nugget against the provider's OWN site.

Flow per nugget that needs primary verification:
  1. Check the central cache. If a fresh verdict exists, reuse it (no API call).
  2. Otherwise run a strict grounded verification constrained to the provider's
     official domain, parse a structured verdict, and cache it.
  3. Anything not_found / contradicted / unparseable goes to the human-check
     queue (`04-provider-verification-needed.csv`) and never silently passes.

Evidence honesty: the automated tier is "grounded" (the engine read the official
site for us), not a byte-for-byte primary fetch. Contradictions and low-confidence
verdicts are pushed to a human, matching the manual process that caught both page
errors and false AI nuggets.
"""

from __future__ import annotations

import csv
import json
import re
from datetime import date
from pathlib import Path
from typing import Any

from .core import CARDS_DIR, REPO_ROOT, RunContext, gemini_client, require_key, resolve_page
from .ledger import Nugget
from .verify_cache import DEFAULT_TTL_DAYS, VerificationCache

VERIFY_PROMPT = """\
You are fact-checking a claim about UK company insolvency, company debt, or
director responsibilities against AUTHORITATIVE UK sources only.

Subject / route: {entity}
Claim to verify: "{claim}"
{preferred}
Treat as authoritative, in this order of preference:
1. GOV.UK and The Insolvency Service official guidance.
2. Legislation on legislation.gov.uk (e.g. Insolvency Act 1986, Companies Act 2006,
   Insolvency (England and Wales) Rules 2016) — prefer the in-force version.
3. Companies House guidance and The Gazette (thegazette.co.uk) official notices.
4. Courts and statutory regulators; recognised professional bodies (ICAEW, IPA, R3)
   only where they restate official rules.

Search the web, but base the verdict ONLY on these authoritative sources. Do NOT
rely on insolvency-firm marketing pages, blogs, forums or comparison sites for the
verdict (you may follow them only to locate the primary source).

Return ONLY a JSON object, no prose, in exactly this shape:
{{"verification_status": "verified|partially_verified|contradicted|not_found",
  "verified_quote": "exact wording from the authoritative source, or empty string",
  "verified_source_url": "the authoritative URL, or empty string",
  "evidence_tier": "grounded",
  "notes": "qualifiers, the governing section/rule, effective date, conflicts, or why it could not be confirmed"}}

Rules:
- Statutory facts change with legislation; prefer the current in-force position and
  note the date or section where it matters.
- If you cannot confirm it from an authoritative source, return "not_found" (do not guess).
- If an authoritative source disagrees with the claim, return "contradicted" with the quote.
- Keep the quote short and exact.
"""

_VALID = {"verified", "partially_verified", "contradicted", "not_found"}


def provider_domains(slug: str) -> dict[str, str]:
    """Map entity name (lowercased) -> a preferred official domain, from any cards
    the page declares (`verify_source`, falling back to the cta_url host).

    Insolvency / debt-advice pages have no provider cards, so this returns {} and
    verification falls back to authoritative UK sources (GOV.UK / The Insolvency
    Service / legislation) as defined in VERIFY_PROMPT. The map is only a hint:
    when a domain is present it is offered as a preferred source, not the sole
    authority."""
    try:
        cfg = resolve_page(slug)
    except Exception:
        # Sitemap-resolved pages have no local PAGE_CONFIG (and no provider
        # cards); verification relies wholly on the authoritative UK sources in
        # VERIFY_PROMPT, the correct default for insolvency.
        return {}
    ids = list(cfg.get("card_ids", [])) + list(cfg.get("separate_card_ids", []))
    out: dict[str, str] = {}
    for cid in ids:
        path = CARDS_DIR / f"{cid}.json"
        if not path.exists():
            continue
        try:
            card = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        domain = card.get("verify_source") or ""
        if not domain and card.get("cta_url"):
            m = re.search(r"https?://([^/]+)/", card["cta_url"])
            domain = m.group(1).replace("www.", "") if m else ""
        for name in (card.get("short_name"), card.get("bank"), card.get("name")):
            if name and domain:
                out[name.strip().lower()] = domain
    return out


def _sanitise_source_url(url: str) -> str:
    """Drop Google grounding-redirect links. Gemini sometimes returns a
    vertexaisearch.cloud.google.com/grounding-api-redirect/... tracking URL
    instead of the real source. Those are useless as published citations, so we
    blank them — the fact stays verified (the quote is real), but the report then
    asks for the provider's primary source rather than printing a junk link."""
    u = (url or "").strip()
    if "vertexaisearch.cloud.google.com" in u or "grounding-api-redirect" in u:
        return ""
    return u


def _parse_verdict(text: str) -> dict[str, Any] | None:
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        obj = json.loads(m.group(0))
    except Exception:
        return None
    if obj.get("verification_status") not in _VALID:
        return None
    obj["verified_source_url"] = _sanitise_source_url(obj.get("verified_source_url", ""))
    return obj


def verify_one(provider: str, claim: str, domain: str, *,
               model: str = "gemini-2.5-flash") -> dict[str, Any]:
    """Single grounded verification. Returns a verdict dict; manual_review on
    any failure to parse or call."""
    from google import genai
    from google.genai import types

    client = gemini_client()
    preferred = (f"Prefer this official source if it is relevant: {domain}\n"
                 if domain else "")
    prompt = VERIFY_PROMPT.format(entity=provider or "this topic", claim=claim,
                                  preferred=preferred)
    try:
        resp = client.models.generate_content(
            model=model, contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]),
        )
        verdict = _parse_verdict(getattr(resp, "text", "") or "")
    except Exception as exc:
        return {"verification_status": "manual_review", "verified_quote": "",
                "verified_source_url": "", "evidence_tier": "",
                "notes": f"verify call failed: {type(exc).__name__}: {exc}"}
    if verdict is None:
        return {"verification_status": "manual_review", "verified_quote": "",
                "verified_source_url": "", "evidence_tier": "",
                "notes": "could not parse a structured verdict"}
    return verdict


def verify_nuggets(nuggets: list[Nugget], cache: VerificationCache,
                   domains: dict[str, str], *, ttl_days: int = DEFAULT_TTL_DAYS,
                   model: str = "gemini-2.5-flash", today: date | None = None,
                   max_live: int | None = None, on_progress=None) -> dict[str, int]:
    """Verify in place. Returns counts. Uses the cache to skip fresh facts.

    ``max_live`` caps the number of LIVE (non-cached) grounded calls in this run
    — the budget guard at the bottleneck. Once reached, any remaining
    needs-verification nugget is parked as ``manual_review`` (queued for a human)
    instead of spending another call, so a single audit can never run away.
    """
    stamp = (today or date.today()).isoformat()
    counts: dict[str, int] = {"cached": 0, "verified": 0, "queued": 0,
                              "skipped": 0, "budget_parked": 0}
    live_used = 0
    for n in nuggets:
        if not n.needs_primary_verification:
            counts["skipped"] += 1
            continue
        claim = n.detail
        domain = domains.get(n.provider.strip().lower(), "")
        if cache.is_fresh(n.provider, claim, ttl_days, today=today):
            entry = cache.get(n.provider, claim)
            source = "cached"
            counts["cached"] += 1
            verdict = {
                "verification_status": entry.verification_status,
                "verified_quote": entry.verified_quote,
                "verified_source_url": entry.verified_source_url,
                "evidence_tier": entry.evidence_tier, "notes": "from cache",
            }
        elif max_live is not None and live_used >= max_live:
            # Budget reached: park for a human rather than spend another call.
            n.verification_status = "manual_review"
            n.notes = (n.notes + " | " if n.notes else "") + \
                "skipped: per-run verification budget reached"
            counts["budget_parked"] += 1
            counts["queued"] += 1
            if on_progress:
                on_progress(n, "budget")
            continue
        else:
            verdict = verify_one(n.provider, claim, domain, model=model)
            source = "live"
            live_used += 1
            cache.put(n.provider, claim,
                      verification_status=verdict["verification_status"],
                      verified_source_url=verdict.get("verified_source_url", ""),
                      verified_quote=verdict.get("verified_quote", ""),
                      evidence_tier=verdict.get("evidence_tier", "grounded"),
                      verify_date=stamp)
        n.verification_status = verdict["verification_status"]
        n.verified_source_url = verdict.get("verified_source_url", "")
        n.verified_quote = verdict.get("verified_quote", "")
        n.evidence_tier = verdict.get("evidence_tier", "")
        n.verify_date = stamp if source == "live" else (cache.get(n.provider, claim).verify_date)
        n.notes = (n.notes + " | " if n.notes else "") + verdict.get("notes", "")
        if n.verification_status in ("verified", "partially_verified"):
            counts["verified"] += 1
        else:
            counts["queued"] += 1
        if on_progress:
            on_progress(n, source)
    return counts


def write_human_queue(nuggets: list[Nugget], path: Path) -> Path:
    """Write 04-provider-verification-needed.csv: everything a human must check."""
    rows = [n for n in nuggets
            if n.needs_primary_verification
            and n.verification_status in ("not_found", "contradicted", "manual_review")]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["subject", "detail", "verification_status", "official_check_url",
                    "browser_prompt", "notes"])
        for n in rows:
            prompt = (f"Confirm against an authoritative UK source (GOV.UK / The "
                      f"Insolvency Service / legislation.gov.uk / Companies House): "
                      f"{n.detail}. Return the exact quote and the official URL.")
            w.writerow([n.provider, n.detail, n.verification_status,
                        n.verified_source_url, prompt, n.notes])
    return path
