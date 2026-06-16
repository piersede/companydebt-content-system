"""Anti-cannibalisation check.

Before we recommend ADDING a fact to a page, make sure another page on
companydebt.com does not already own that fact. If two of our own pages state
the same key fact, search engines and AI answer engines cannot tell which one to
quote, so our citation authority is split and BOTH pages get weaker. When a fact
is already owned elsewhere, the recommendation should be to LINK to the owning
page, not to duplicate the fact.

Implementation mirrors verify.py: a Google-grounded lookup, but constrained to
``site:companydebt.com`` and explicitly excluding the page being audited.
"""

from __future__ import annotations

import json
import re
from typing import Any

from .core import gemini_client, require_key
from .ledger import Nugget

SITE = "companydebt.com"

CANNIBAL_PROMPT = """\
You are checking whether facts are ALREADY published on the website {site}, to
avoid two pages on the same site competing to be quoted for the same fact.

Search the web, but consider ONLY pages on {site}. Ignore every other website.
Do NOT count the page we are auditing itself: {exclude_url}

Below is a NUMBERED list of facts we are about to add to {exclude_url}. For each
one, decide whether some OTHER page on {site} (not {exclude_url}) already states
or clearly covers that same fact.

FACTS:
{facts}

Return ONLY a JSON array, no prose. One object per fact, in the same order,
exactly:
[{{"index": 1, "already_covered": true|false,
   "owner_url": "the {site} URL that already covers it, or empty string"}}, ...]

Rules:
- already_covered = true ONLY if the SAME fact is on a DIFFERENT {site} page.
- If the only page covering it is {exclude_url} itself, return false for it.
- If you cannot find it on {site}, return false for it.
- Return exactly one object per numbered fact.
"""


def _parse(text: str) -> dict[str, Any] | None:
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        obj = json.loads(m.group(0))
    except Exception:
        return None
    return obj if "already_covered" in obj else None


def _parse_array(text: str) -> list[dict[str, Any]]:
    """Pull the outermost JSON array from a model reply, tolerating code fences."""
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


def _norm(url: str) -> str:
    """Normalise a URL to host+path for same-page comparison."""
    u = (url or "").strip().lower().rstrip("/")
    u = re.sub(r"^https?://", "", u)
    u = re.sub(r"^www\.", "", u)
    return u


def check_one(claim: str, exclude_url: str, *,
              model: str = "gemini-2.5-flash") -> dict[str, Any]:
    from google import genai
    from google.genai import types

    client = gemini_client()
    prompt = CANNIBAL_PROMPT.format(site=SITE, exclude_url=exclude_url, claim=claim)
    try:
        resp = client.models.generate_content(
            model=model, contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]),
        )
        verdict = _parse(getattr(resp, "text", "") or "")
    except Exception as exc:
        return {"already_covered": False, "owner_url": "", "quote": "",
                "error": f"{type(exc).__name__}: {exc}"}
    if verdict is None:
        return {"already_covered": False, "owner_url": "", "quote": "",
                "error": "unparseable"}
    return verdict


def check_cannibalisation(nuggets: list[Nugget], target_url: str, *,
                          model: str = "gemini-2.5-flash",
                          max_live: int | None = None, on_progress=None) -> dict[str, int]:
    """Flag, in place, any nugget already owned by another companydebt.com page.

    ONE batched grounded call for all nuggets (not one per nugget): on a
    throttled key, call count is the bottleneck, so we ask about every fact at
    once. ``max_live`` is ignored (kept for signature compatibility).
    """
    from google import genai
    from google.genai import types

    counts = {"checked": len(nuggets), "risk": 0, "clear": 0, "error": 0}
    if not nuggets:
        return counts
    target = _norm(target_url)

    facts = "\n".join(f"{i}. {n.detail}" for i, n in enumerate(nuggets, 1))
    prompt = CANNIBAL_PROMPT.format(site=SITE, exclude_url=target_url, facts=facts)
    client = gemini_client()
    try:
        resp = client.models.generate_content(
            model=model, contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]),
        )
        rows = _parse_array(getattr(resp, "text", "") or "")
    except Exception:
        counts["error"] = len(nuggets)
        return counts  # fail-soft: leave all clear rather than block the report

    by_index = {int(r.get("index", -1)): r for r in rows if isinstance(r, dict)}
    for i, n in enumerate(nuggets, 1):
        r = by_index.get(i, {})
        owner = _norm(r.get("owner_url", ""))
        if r.get("already_covered") and owner and owner != target:
            n.cannibalisation_risk = True
            n.cannibal_owner_url = r.get("owner_url", "").strip()
            counts["risk"] += 1
            if on_progress:
                on_progress(n, "risk")
        else:
            counts["clear"] += 1
            if on_progress:
                on_progress(n, "clear")
    return counts
