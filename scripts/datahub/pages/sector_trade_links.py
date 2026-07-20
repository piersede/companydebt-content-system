"""Shared registry of trade-detail-page links: the single source both the
flagship's "Get the insolvency data for your trade" table
(build_insolvency_dashboard.py) and the hub landing page's "By sector" cards
(company_insolvency_hub.py) read from.

Previously each caller hand-rolled its own version of this list. That is how
the hub's card list went stale in the first place - a design snapshot with
only Construction, missing the 9 trade pages built since. Both callers now
read the same rows() output, so a new trade page appears on both pages the
moment it is added to sic_group_stats.py's SECTORS registry, with no second
list to remember to update.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data" / "insolvency-statistics"

# Construction is the one whole-section detail page (build_construction() in
# sector_pages.py) rather than a SECTORS entry, so it is added by hand.
CONSTRUCTION_TRADE_LINK = {
    "slug": "construction-insolvency-statistics",
    "trade": "Construction",
    "parent_section_code": "F",
    "blurb": "The largest sector by insolvency volume: builders, contractors and specialist trades.",
}

# One-line scope notes (distinct from each page's own longer
# scope_description): tight, <=120 chars, describes coverage not figures, so
# it never needs a monthly data refresh.
TRADE_LINK_BLURBS = {
    "furniture-insolvency-statistics": "Household, office, kitchen and shop furniture and mattress manufacturers.",
    "restaurant-insolvency-statistics": "Restaurants, cafes and mobile or takeaway food service businesses.",
    "road-haulage-insolvency-statistics": "Freight transport by road and removal services.",
    "recruitment-agency-insolvency-statistics": "Permanent-placement and executive-search recruitment agencies.",
    "temporary-staffing-agency-insolvency-statistics": "Agencies supplying temporary office, industrial, medical and teaching staff.",
    "motor-vehicle-repair-insolvency-statistics": "Garages and workshops carrying out motor vehicle maintenance and repair.",
    "cleaning-company-insolvency-statistics": "Commercial and industrial cleaning contractors, including window cleaning.",
    "hotel-insolvency-statistics": "Hotels, motels and similar short-stay accommodation with daily housekeeping.",
    "estate-agency-insolvency-statistics": "Estate agencies and fee-based property management businesses.",
}


def rows() -> list[dict]:
    """Every published trade-detail row: slug, trade name, blurb, and the
    parent SIC section's rolling-12-month rank (1 = largest), used only for
    sort order. Ranks are computed live from sector_series.json rather than
    hand-maintained, so the list reorders itself if the sector mix shifts.
    Sorted by rank ascending, then trade name alphabetically within a rank."""
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).resolve().parent))
    from sic_group_stats import SECTORS  # noqa: E402  (late: avoids a cycle)

    series = json.loads((DATA_DIR / "sector_series.json").read_text(encoding="utf-8"))
    section_total = {s["code"]: sum((s["monthly"] or [])[-12:]) for s in series["sections"]}
    rank_of = {
        code: i + 1
        for i, code in enumerate(sorted(section_total, key=lambda c: section_total[c], reverse=True))
    }

    out = [{
        "slug": CONSTRUCTION_TRADE_LINK["slug"],
        "trade": CONSTRUCTION_TRADE_LINK["trade"],
        "blurb": CONSTRUCTION_TRADE_LINK["blurb"],
        "sic_rank": rank_of.get(CONSTRUCTION_TRADE_LINK["parent_section_code"], 99),
    }]
    for slug, cfg in SECTORS.items():
        out.append({
            "slug": slug,
            "trade": cfg["eyebrow"],
            "blurb": TRADE_LINK_BLURBS[slug],
            "sic_rank": rank_of.get(cfg["parent_section_code"], 99),
        })
    out.sort(key=lambda r: (r["sic_rank"], r["trade"]))
    return out
