"""Shared nugget/ledger schema for the audit pipeline.

One row per atomic detail, carried from extract -> verify -> recommend. Keeping
a single typed schema (rather than ad-hoc dicts per stage) is what lets the
stages be wired into one CLI without each re-parsing the last one's output.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

ARTICLE_STATUSES = (
    "present", "present_but_weak", "missing", "outdated",
    "unsupported", "buried", "contradicted", "not_relevant",
)
VERIFICATION_STATUSES = (
    "unverified", "verified", "partially_verified",
    "contradicted", "not_found", "manual_review",
)
EVIDENCE_TIERS = ("primary", "headless", "grounded", "secondary", "human", "")


@dataclass
class Nugget:
    """A single salient detail the audit surfaced, with extract + verify state."""

    detail_id: str
    detail: str                                   # self-contained: entity + claim + qualifier
    category: str = ""
    provider: str = ""
    card_name: str = ""
    value: str = ""                               # the figure/qualifier, if any
    source_urls: list[str] = field(default_factory=list)
    mentioned_by: list[str] = field(default_factory=list)  # which engines surfaced it
    # extract verdict
    article_status: str = "missing"
    recommended_display_format: str = ""          # canonical format, or compound "a + b"
    recommended_action: str = ""
    priority: str = "medium"                      # low|medium|high|critical
    needs_primary_verification: bool = True
    # presentation-layer fields (from llm_friendly_content_presentation.md)
    source_required: bool = False                 # must cite a primary source line
    last_checked_required: bool = False           # must show a visible last-checked date
    editorial_note: str = ""                      # free-text steer for the human applying it
    # verify verdict (filled by the verify stage)
    verification_status: str = "unverified"
    verified_source_url: str = ""
    verified_quote: str = ""
    verify_date: str = ""                         # ISO date the claim was confirmed
    evidence_tier: str = ""                       # how it was confirmed
    notes: str = ""
    # anti-cannibalisation: is this fact already owned by ANOTHER of our pages?
    # If so, adding it here would split our own citation authority — link instead.
    cannibalisation_risk: bool = False
    cannibal_owner_url: str = ""                   # the existing page that owns the fact

    def __post_init__(self) -> None:
        if self.article_status not in ARTICLE_STATUSES:
            raise ValueError(f"bad article_status: {self.article_status!r}")
        if self.verification_status not in VERIFICATION_STATUSES:
            raise ValueError(f"bad verification_status: {self.verification_status!r}")

    @property
    def is_publishable(self) -> bool:
        """A nugget may inform copy only if verified (or it is a non-commercial
        angle that did not need primary verification)."""
        if not self.needs_primary_verification:
            return self.verification_status != "contradicted"
        return self.verification_status in ("verified", "partially_verified")


def save_jsonl(nuggets: list[Nugget], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for n in nuggets:
            fh.write(json.dumps(asdict(n), ensure_ascii=False) + "\n")
    return path


def load_jsonl(path: Path) -> list[Nugget]:
    out: list[Nugget] = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(Nugget(**json.loads(line)))
    return out


def save_csv(nuggets: list[Nugget], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(asdict(nuggets[0]).keys()) if nuggets else [f for f in Nugget.__dataclass_fields__]
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for n in nuggets:
            row: dict[str, Any] = asdict(n)
            for k in ("source_urls", "mentioned_by"):
                row[k] = "|".join(row[k])
            w.writerow(row)
    return path
