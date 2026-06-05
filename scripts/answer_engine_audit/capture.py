"""Answer-engine capture: OpenAI (web_search) and Gemini (grounded search).

Each engine is a separate WITNESS. We preserve the full raw response plus the
provenance the API exposes (search queries it ran, the sources it consulted,
and the citation mapping back into the answer). Nothing here decides truth —
that is the verification layer's job.
"""

from __future__ import annotations

import json
from typing import Any

from .core import RunContext, require_key, write_raw

# Defaults are conservative/broadly-available; override via CLI flags.
DEFAULT_OPENAI_MODEL = "gpt-4o"
DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"


# --------------------------------------------------------------------------
# OpenAI
# --------------------------------------------------------------------------

def _extract_openai_provenance(resp_dump: dict[str, Any]) -> dict[str, Any]:
    """Pull citations, consulted sources and web_search actions out of a
    Responses API dump, defensively (shapes shift across SDK versions)."""
    citations: list[dict[str, Any]] = []
    source_urls: list[str] = []
    actions: list[dict[str, Any]] = []
    for item in resp_dump.get("output", []) or []:
        itype = item.get("type")
        if itype == "web_search_call":
            action = item.get("action") or {}
            actions.append({"type": action.get("type"), "query": action.get("query"),
                            "url": action.get("url")})
            for s in action.get("sources", []) or []:
                url = s.get("url") if isinstance(s, dict) else None
                if url:
                    source_urls.append(url)
        if itype == "message":
            for block in item.get("content", []) or []:
                for ann in block.get("annotations", []) or []:
                    if ann.get("type") in ("url_citation", "url"):
                        url = ann.get("url")
                        citations.append({"url": url, "title": ann.get("title")})
                        if url:
                            source_urls.append(url)
    # de-dupe URLs, preserve order
    seen: set[str] = set()
    deduped = [u for u in source_urls if not (u in seen or seen.add(u))]
    return {"citations": citations, "source_urls": deduped, "web_search_actions": actions}


def capture_openai(ctx: RunContext, prompt: str, label: str, *,
                   model: str = DEFAULT_OPENAI_MODEL, country: str = "GB") -> dict[str, Any]:
    from openai import OpenAI

    client = OpenAI(api_key=require_key("OPENAI_API_KEY"))

    def _call(tool_type: str, tool_choice: Any):
        kwargs: dict[str, Any] = dict(
            model=model,
            tools=[{"type": tool_type,
                    "user_location": {"type": "approximate", "country": country}}],
            input=prompt,
        )
        if tool_choice is not None:
            kwargs["tool_choice"] = tool_choice
        return client.responses.create(**kwargs)

    # Force the web search: left to "auto", chat models often answer from
    # parametric memory and return zero sources, which defeats provenance
    # capture. Try forcing the specific tool, then "required", then auto.
    last_exc: Exception | None = None
    resp = None
    for tool_type in ("web_search", "web_search_preview"):
        for choice in ({"type": tool_type}, "required", None):
            try:
                resp = _call(tool_type, choice)
                last_exc = None
                break
            except Exception as exc:
                last_exc = exc
        if resp is not None:
            break
    if resp is None:
        raise last_exc if last_exc else RuntimeError("OpenAI web_search capture failed")

    resp_dump = resp.model_dump()
    text = getattr(resp, "output_text", "") or ""
    prov = _extract_openai_provenance(resp_dump)

    write_raw(ctx, f"openai/{label}.response.json", resp_dump,
              source_type="answer_engine", engine="openai", query=prompt,
              source_urls=prov["source_urls"])
    write_raw(ctx, f"openai/{label}.sources.json", prov,
              source_type="answer_engine", engine="openai", query=prompt,
              source_urls=prov["source_urls"])
    write_raw(ctx, f"openai/{label}.answer.md", text,
              source_type="answer_engine", engine="openai", query=prompt,
              source_urls=prov["source_urls"])
    return {"engine": "openai", "label": label, "model": model,
            "text_chars": len(text), "sources": len(prov["source_urls"])}


# --------------------------------------------------------------------------
# Gemini (grounded with Google Search)
# --------------------------------------------------------------------------

def _extract_gemini_provenance(resp: Any) -> dict[str, Any]:
    queries: list[str] = []
    chunks: list[dict[str, Any]] = []
    cited_uris: list[str] = []
    try:
        cand = resp.candidates[0]
        gm = getattr(cand, "grounding_metadata", None)
        if gm is not None:
            queries = list(getattr(gm, "web_search_queries", None) or [])
            for ch in getattr(gm, "grounding_chunks", None) or []:
                web = getattr(ch, "web", None)
                if web is not None:
                    uri = getattr(web, "uri", None)
                    chunks.append({"uri": uri, "title": getattr(web, "title", None)})
                    if uri:
                        cited_uris.append(uri)
    except Exception:
        pass
    seen: set[str] = set()
    deduped = [u for u in cited_uris if not (u in seen or seen.add(u))]
    return {"web_search_queries": queries, "grounding_chunks": chunks,
            "cited_uris": deduped}


def capture_gemini(ctx: RunContext, prompt: str, label: str, *,
                   model: str = DEFAULT_GEMINI_MODEL) -> dict[str, Any]:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=require_key("GEMINI_API_KEY"))
    resp = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
        ),
    )

    text = getattr(resp, "text", "") or ""
    prov = _extract_gemini_provenance(resp)
    try:
        resp_dump = resp.model_dump(mode="json")
    except Exception:
        resp_dump = {"text": text, "note": "model_dump unavailable"}

    write_raw(ctx, f"gemini/{label}.response.json", resp_dump,
              source_type="answer_engine", engine="gemini", query=prompt,
              source_urls=prov["cited_uris"])
    write_raw(ctx, f"gemini/{label}.grounding-metadata.json", prov,
              source_type="answer_engine", engine="gemini", query=prompt,
              source_urls=prov["cited_uris"])
    write_raw(ctx, f"gemini/{label}.answer.md", text,
              source_type="answer_engine", engine="gemini", query=prompt,
              source_urls=prov["cited_uris"])
    return {"engine": "gemini", "label": label, "model": model,
            "text_chars": len(text), "queries": len(prov["web_search_queries"]),
            "sources": len(prov["cited_uris"])}
