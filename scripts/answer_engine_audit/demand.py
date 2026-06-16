"""Demand layer: turn real Ahrefs search keywords into capture probes.

The rest of the audit probes what the page already knows to ask about (the
target keyword + generic insolvency use-cases). That misses demand the page never
anticipated. This stage pulls the keywords people actually search around the
topic (Ahrefs Keywords Explorer -> matching terms, volume-ranked), drops the
navigational / brand-ops noise, and converts each surviving keyword into the
natural-language question a person would put to an AI assistant. Those questions
are appended to the capture prompt set, so the engine is probed on real demand,
not only on the page's own framing.

Verification, the already-covered guard, and recommend are unchanged downstream:
this stage only changes WHAT gets asked.

Live fetch needs ``AHREFS_API_TOKEN`` (or ``AHREFS_API_KEY``) in the env/.env.
Without it, pass a saved JSON/CSV export via ``fixture`` (same shape as the API
response, or the Keywords Explorer CSV export) so the stage still runs offline.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import prompts
from .core import load_env, slugify

AHREFS_ENDPOINT = "https://api.ahrefs.com/v3/keywords-explorer/matching-terms"
AHREFS_SELECT = "keyword,volume,difficulty,cpc,intents"

# Intents that earn a keyword a place in the probe set. A keyword survives if it
# carries at least one of these; a purely navigational/branded/local term does
# not (login, contact number, head office).
USEFUL_INTENTS = ("informational", "commercial", "transactional")

# Brand-ops / navigational noise the intent flags don't always catch. Whole-word/
# phrase match on the lowercased keyword. Overridable per page via
# cfg['demand_stop_terms'].
DEFAULT_STOP_TERMS = (
    "login", "log in", "sign in", "signin", "logon",
    "contact", "phone", "telephone", "email address",
    "jobs", "job", "careers", "career", "vacancy", "vacancies",
    "salary", "glassdoor", "linkedin", "logo", "head office",
    "address", "opening times", "wiki", "ceo", "owner",
)


# --------------------------------------------------------------------------
# Data
# --------------------------------------------------------------------------

@dataclass
class KeywordRow:
    keyword: str
    volume: int
    intents: list[str] = field(default_factory=list)
    difficulty: int | None = None
    cpc: int | None = None
    # filled in by the pipeline:
    probe: str | None = None
    label: str | None = None
    dropped_reason: str | None = None

    @property
    def primary_intent(self) -> str:
        for it in USEFUL_INTENTS:
            if it in self.intents:
                return it
        return self.intents[0] if self.intents else "unknown"


# --------------------------------------------------------------------------
# Fetch (Ahrefs API, or a saved-export fixture)
# --------------------------------------------------------------------------

def _ahrefs_token() -> str:
    import os

    load_env()
    token = os.getenv("AHREFS_API_TOKEN") or os.getenv("AHREFS_API_KEY")
    if not token:
        raise RuntimeError(
            "AHREFS_API_TOKEN not found. The token is only needed for unattended "
            "(scheduled) runs where the tool fetches Ahrefs itself. For an "
            "agent/human-driven run, export the Keywords Explorer matching terms "
            "from Ahrefs and pass the file via --demand-fixture (CSV or JSON); add "
            "the token to the repo-root .env only if you want autonomous runs."
        )
    return token


def _parse_intents(raw: Any) -> list[str]:
    """Ahrefs returns intents as an object of booleans; normalise to a list of
    the true ones. Tolerates a list or comma-string too."""
    if isinstance(raw, dict):
        return [k.lower() for k, v in raw.items() if v]
    if isinstance(raw, list):
        return [str(x).lower().strip() for x in raw]
    if isinstance(raw, str):
        return [p.strip().lower() for p in raw.split(",") if p.strip()]
    return []


def _rows_from_payload(payload: Any) -> list[KeywordRow]:
    """Defensive parse: the rows may sit under one of several keys, or be a bare
    list. Each row's volume/intents field names are stable in v3."""
    items: Any = None
    if isinstance(payload, list):
        items = payload
    elif isinstance(payload, dict):
        for key in ("keywords", "matching_terms", "terms", "data", "results"):
            if isinstance(payload.get(key), list):
                items = payload[key]
                break
        if items is None:  # first list value, whatever it's called
            items = next((v for v in payload.values() if isinstance(v, list)), [])
    rows: list[KeywordRow] = []
    for it in items or []:
        if not isinstance(it, dict):
            continue
        kw = str(it.get("keyword", "")).strip()
        if not kw:
            continue
        vol = it.get("volume")
        rows.append(KeywordRow(
            keyword=kw,
            volume=int(vol) if isinstance(vol, (int, float)) else 0,
            intents=_parse_intents(it.get("intents")),
            difficulty=it.get("difficulty"),
            cpc=it.get("cpc"),
        ))
    return rows


def fetch_from_api(seed: str, *, country: str = "gb", limit: int = 1000,
                   timeout: int = 60) -> list[KeywordRow]:
    """Pull matching terms for ``seed`` from Ahrefs Keywords Explorer v3."""
    import requests

    params = {
        "country": country.lower(),
        "select": AHREFS_SELECT,
        "keywords": seed,
        "match_mode": "terms",
        "order_by": "volume:desc",
        "limit": limit,
        "output": "json",
    }
    resp = requests.get(
        AHREFS_ENDPOINT, params=params,
        headers={"Authorization": f"Bearer {_ahrefs_token()}",
                 "Accept": "application/json"},
        timeout=timeout,
    )
    resp.raise_for_status()
    return _rows_from_payload(resp.json())


def _parse_volume(raw: Any) -> int:
    """Tolerate '55,000', '55K', '1.2M' as well as plain ints (Ahrefs CSV/UI)."""
    if isinstance(raw, (int, float)):
        return int(raw)
    s = str(raw).strip().replace(",", "").replace(" ", "")
    if not s:
        return 0
    mult = 1
    if s[-1:].lower() in ("k", "m"):
        mult = 1000 if s[-1].lower() == "k" else 1_000_000
        s = s[:-1]
    try:
        return int(float(s) * mult)
    except ValueError:
        return 0


def _pick_column(fieldnames: list[str], *candidates: str) -> str | None:
    """Match an Ahrefs CSV header case-insensitively. Earlier candidates win, so
    'Volume' is preferred over 'Global volume'."""
    lower = {f.lower().strip(): f for f in fieldnames}
    for cand in candidates:
        if cand in lower:
            return lower[cand]
    for cand in candidates:  # fall back to a 'contains' match
        for low, orig in lower.items():
            if cand in low:
                return orig
    return None


def fetch_from_csv(path: str | Path) -> list[KeywordRow]:
    """Read rows from an Ahrefs Keywords Explorer CSV export (the 'Export'
    button). Column names are matched flexibly; the Intents cell is a
    comma-separated string like 'Informational, Branded'."""
    import csv

    text = Path(path).read_text(encoding="utf-8-sig")
    reader = csv.DictReader(text.splitlines())
    fields = reader.fieldnames or []
    kw_col = _pick_column(fields, "keyword")
    vol_col = _pick_column(fields, "volume", "search volume")
    int_col = _pick_column(fields, "intents", "intent")
    diff_col = _pick_column(fields, "difficulty", "kd")
    cpc_col = _pick_column(fields, "cpc")
    if not kw_col:
        raise RuntimeError(
            f"No 'Keyword' column in {path}. Found: {', '.join(fields) or '(none)'}.")
    rows: list[KeywordRow] = []
    for r in reader:
        kw = (r.get(kw_col) or "").strip()
        if not kw:
            continue
        rows.append(KeywordRow(
            keyword=kw,
            volume=_parse_volume(r.get(vol_col)) if vol_col else 0,
            intents=_parse_intents(r.get(int_col)) if int_col else [],
            difficulty=None,
            cpc=None,
        ))
    return rows


def load_rows(path: str | Path) -> list[KeywordRow]:
    """Dispatch a saved Ahrefs export by extension: .csv (native export) or
    .json (API-shaped)."""
    return fetch_from_csv(path) if str(path).lower().endswith(".csv") \
        else fetch_from_fixture(path)


def fetch_from_fixture(path: str | Path) -> list[KeywordRow]:
    """Read rows from a saved Ahrefs JSON export (same shape as the API)."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return _rows_from_payload(data)


# --------------------------------------------------------------------------
# Filter (intent + brand-ops denylist + volume + top-N)
# --------------------------------------------------------------------------

def _matches_stop_term(keyword: str, stop_terms: tuple[str, ...]) -> str | None:
    low = keyword.lower()
    for term in stop_terms:
        if re.search(rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])", low):
            return term
    return None


def filter_rows(rows: list[KeywordRow], *, min_volume: int = 0, top_n: int = 30,
                stop_terms: tuple[str, ...] = DEFAULT_STOP_TERMS,
                ) -> tuple[list[KeywordRow], list[KeywordRow]]:
    """Return (kept, dropped). Kept are volume-ranked, capped at ``top_n``;
    every dropped row carries a ``dropped_reason`` for the audit trail."""
    kept: list[KeywordRow] = []
    dropped: list[KeywordRow] = []
    seen: set[str] = set()
    for row in sorted(rows, key=lambda r: r.volume, reverse=True):
        key = row.keyword.lower().strip()
        if key in seen:
            row.dropped_reason = "duplicate"
            dropped.append(row)
            continue
        seen.add(key)
        if row.volume < min_volume:
            row.dropped_reason = f"below min_volume ({row.volume} < {min_volume})"
            dropped.append(row)
            continue
        stop = _matches_stop_term(row.keyword, stop_terms)
        if stop:
            row.dropped_reason = f"brand-ops/navigational term '{stop}'"
            dropped.append(row)
            continue
        # Intent gate: needs at least one useful intent. If Ahrefs returned no
        # intents at all, keep it (don't silently drop on missing metadata).
        if row.intents and not any(it in row.intents for it in USEFUL_INTENTS):
            row.dropped_reason = f"intent not useful ({','.join(row.intents) or 'none'})"
            dropped.append(row)
            continue
        if len(kept) < top_n:
            kept.append(row)
        else:
            row.dropped_reason = f"beyond top_n ({top_n})"
            dropped.append(row)
    return kept, dropped


# --------------------------------------------------------------------------
# Convert (keyword -> natural-language probe, batched Gemini call)
# --------------------------------------------------------------------------

def _fallback_probe(keyword: str) -> str:
    return f"What should I know about {keyword}?"


def _parse_numbered(text: str, n: int) -> dict[int, str]:
    out: dict[int, str] = {}
    for line in text.splitlines():
        m = re.match(r"\s*(\d+)[.)]\s*(.+\S)\s*$", line)
        if m:
            idx = int(m.group(1))
            if 1 <= idx <= n:
                out[idx] = m.group(2).strip().strip('"').strip()
    return out


def convert_keywords(keywords: list[str], *, model: str = "gemini-2.5-flash",
                     ) -> list[str]:
    """Rewrite each keyword as the question a person would ask an AI assistant.
    Faithful to ``prompts.KEYWORD_TO_PROMPT`` rules, batched into one call.
    Always returns one probe per input (deterministic fallback on any gap)."""
    if not keywords:
        return []
    from .core import gemini_client

    numbered = "\n".join(f"{i}. {k}" for i, k in enumerate(keywords, 1))
    prompt = prompts.KEYWORD_TO_PROMPT_BATCH.format(numbered_keywords=numbered)
    client = gemini_client()
    resp = client.models.generate_content(model=model, contents=prompt)
    parsed = _parse_numbered(getattr(resp, "text", "") or "", len(keywords))
    return [parsed.get(i, _fallback_probe(k)) for i, k in enumerate(keywords, 1)]


# --------------------------------------------------------------------------
# Orchestrate: seed -> fetch -> filter -> convert -> probes + audit record
# --------------------------------------------------------------------------

# Page-type suffixes to strip off the derived keyword to get a cleaner Ahrefs
# seed (the slug-derived keyword is already topic-shaped on this site, so this is
# light: drop only generic article-shape words).
_TOPIC_SUFFIXES = (
    "guide", "explained", "advice", "process", "meaning", "definition",
    "uk", "for directors", "for company directors",
)


def resolve_seed(cfg: dict[str, Any], keyword: str, override: str | None) -> str:
    """The Ahrefs seed should be the topic, not an article-shaped phrase.
    Order: CLI override -> cfg['demand_seed'] -> strip generic suffixes off the
    derived keyword."""
    if override:
        return override.strip()
    if isinstance(cfg.get("demand_seed"), str) and cfg["demand_seed"].strip():
        return cfg["demand_seed"].strip()
    seed = keyword.strip()
    low = seed.lower()
    for suf in _TOPIC_SUFFIXES:
        if low.endswith(suf):
            seed = seed[: len(seed) - len(suf)].strip(" -:")
            break
    return seed or keyword.strip()


def collect_demand(seed: str, *, country: str = "gb", min_volume: int = 0,
                   top_n: int = 30, model: str = "gemini-2.5-flash",
                   stop_terms: tuple[str, ...] = DEFAULT_STOP_TERMS,
                   fixture: str | Path | None = None) -> dict[str, Any]:
    """Run the full demand stage. Returns a record dict with kept rows (each
    carrying its probe + label), dropped rows with reasons, and counts."""
    rows = load_rows(fixture) if fixture else fetch_from_api(seed, country=country)
    kept, dropped = filter_rows(rows, min_volume=min_volume, top_n=top_n,
                                stop_terms=stop_terms)
    probes = convert_keywords([r.keyword for r in kept], model=model)
    for i, (row, probe) in enumerate(zip(kept, probes), 1):
        row.probe = probe
        row.label = f"demand-{i:02d}-{slugify(row.keyword)[:40]}".rstrip("-")
    return {
        "seed": seed,
        "country": country,
        "fetched": len(rows),
        "kept": len(kept),
        "dropped": len(dropped),
        "min_volume": min_volume,
        "top_n": top_n,
        "rows": [_row_dict(r) for r in kept],
        "dropped_rows": [_row_dict(r) for r in dropped],
    }


def _row_dict(r: KeywordRow) -> dict[str, Any]:
    return {
        "keyword": r.keyword, "volume": r.volume, "intent": r.primary_intent,
        "intents": r.intents, "probe": r.probe, "label": r.label,
        "dropped_reason": r.dropped_reason,
    }


def demand_prompt_set(record: dict[str, Any], seed: str) -> list[tuple[str, str]]:
    """Turn the kept rows into (label, prompt) pairs for the capture set. Each
    converted question is wrapped in the same USE_CASE envelope the config-driven
    use-cases use, so downstream extract gets comparison-ready answers."""
    pset: list[tuple[str, str]] = []
    for row in record.get("rows", []):
        question = row.get("probe") or _fallback_probe(row["keyword"])
        pset.append((row["label"],
                     prompts.USE_CASE.format(keyword=seed, question=question)))
    return pset
