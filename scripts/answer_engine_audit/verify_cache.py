"""Verification cache — the efficiency unlock for regular audits.

Verification (fetching a provider page and confirming a commercial claim) is the
slowest, most token-heavy, least reliable stage. Most facts do not change between
runs, so we cache each verdict keyed by (provider, normalised_claim) and skip
re-verification while it is fresh. The cache is CENTRAL (shared across pages), so
a fact confirmed for one page is reused everywhere that provider appears.

This is deliberately a thin store of verdicts, not a parallel source of truth:
the authoritative value still lives in the card JSON `verify_date` mechanism.
The cache only answers "did we already confirm this exact claim recently?".
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

from .core import RESEARCH_DIR

CACHE_PATH = RESEARCH_DIR / "_answer_audit" / "verification_cache.json"
DEFAULT_TTL_DAYS = 90  # commercial finance facts: re-confirm quarterly


def normalise_claim(claim: str) -> str:
    """Collapse a claim to a stable cache key fragment: lowercase, strip
    punctuation, collapse whitespace. Keeps digits/%/£ so '2.95%' stays distinct
    from '2.99%'."""
    s = claim.lower()
    s = re.sub(r"[^a-z0-9%£.\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


@dataclass
class CacheEntry:
    provider: str
    claim: str
    verification_status: str
    verified_source_url: str
    verified_quote: str
    evidence_tier: str
    verify_date: str  # ISO date


class VerificationCache:
    def __init__(self, path: Path = CACHE_PATH) -> None:
        self.path = path
        self._data: dict[str, dict] = {}
        if path.exists():
            try:
                self._data = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                self._data = {}

    @staticmethod
    def _key(provider: str, claim: str) -> str:
        return f"{provider.strip().lower()}::{normalise_claim(claim)}"

    def get(self, provider: str, claim: str) -> CacheEntry | None:
        row = self._data.get(self._key(provider, claim))
        return CacheEntry(**row) if row else None

    def is_fresh(self, provider: str, claim: str,
                 ttl_days: int = DEFAULT_TTL_DAYS, *, today: date | None = None) -> bool:
        entry = self.get(provider, claim)
        if entry is None or not entry.verify_date:
            return False
        try:
            checked = datetime.fromisoformat(entry.verify_date).date()
        except ValueError:
            return False
        return (today or date.today()) - checked <= timedelta(days=ttl_days)

    def put(self, provider: str, claim: str, *, verification_status: str,
            verified_source_url: str = "", verified_quote: str = "",
            evidence_tier: str = "", verify_date: str | None = None) -> CacheEntry:
        entry = CacheEntry(
            provider=provider, claim=claim,
            verification_status=verification_status,
            verified_source_url=verified_source_url,
            verified_quote=verified_quote,
            evidence_tier=evidence_tier,
            verify_date=verify_date or date.today().isoformat(),
        )
        self._data[self._key(provider, claim)] = asdict(entry)
        return entry

    def save(self) -> Path:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self._data, indent=2, ensure_ascii=False),
                             encoding="utf-8")
        return self.path

    def stats(self) -> dict[str, int]:
        from collections import Counter
        c = Counter(v["verification_status"] for v in self._data.values())
        return {"total": len(self._data), **c}
