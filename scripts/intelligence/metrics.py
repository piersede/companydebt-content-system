"""Deterministic metric calculations. One definition per metric, computed once.

WHY THIS EXISTS
---------------
Every metric on the data pages is currently computed inside whichever builder
happens to need it, and quoted by hand wherever prose mentions it. Two audits in
August 2026 found the predictable result: pages stating two different values for
the same thing, and superlatives that were true when typed and false later.

This module is the only place a metric is defined. It takes a series and returns
numbers. It knows nothing about pages, prose or HTML.

Definitions match docs/data-hub/insolvency-intelligence-spec.md Part 6.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SERIES = ROOT / "data" / "insolvency-statistics" / "sector_series.json"


def load_series() -> dict:
    return json.loads(SERIES.read_text(encoding="utf-8"))


def num(v) -> float:
    """Series files use '[x]'/'[z]'/None for suppressed or missing values."""
    return v if isinstance(v, (int, float)) else 0


def find(ser: dict, code: str, level: str | None = None):
    """Locate a group, division or section by code."""
    pools = {"group": ["groups"], "division": ["divisions"], "section": ["sections"]}
    for pool in pools.get(level, ["groups", "divisions", "sections"]):
        for e in ser.get(pool, []):
            if e.get("code") == code:
                return e
    return None


def month_index(ser: dict, month: str) -> int:
    return ser["monthly_months"].index(month)


def window(ser: dict, entity: dict, start: str, end: str) -> int:
    """Inclusive sum over a month range."""
    months = ser["monthly_months"]
    i, j = months.index(start), months.index(end)
    mon = entity.get("monthly") or []
    return int(sum(num(mon[k]) for k in range(i, j + 1) if k < len(mon)))


def ytd(ser: dict, entity: dict, latest: str) -> tuple[int, int]:
    """Year to date against the same months a year earlier."""
    year, mo = latest.split("-")
    this = window(ser, entity, "%s-01" % year, latest)
    prior_year = str(int(year) - 1)
    prior = window(ser, entity, "%s-01" % prior_year, "%s-%s" % (prior_year, mo))
    return this, prior


def rolling(ser: dict, entity: dict, latest: str) -> tuple[int, int]:
    """Latest 12 months against the preceding 12."""
    months = ser["monthly_months"]
    j = months.index(latest)
    mon = entity.get("monthly") or []
    cur = int(sum(num(mon[k]) for k in range(max(0, j - 11), j + 1) if k < len(mon)))
    prev = int(sum(num(mon[k]) for k in range(max(0, j - 23), max(0, j - 11)) if k < len(mon)))
    return cur, prev


def pct_change(current: float, prior: float) -> float | None:
    if not prior:
        return None
    return round(100.0 * (current - prior) / prior, 1)


def annual(ser: dict, entity: dict) -> dict:
    years = ser["annual_years"]
    arr = entity.get("annual") or []
    return {str(y): (arr[i] if i < len(arr) else None) for i, y in enumerate(years)}


def vs_baseline(ser: dict, entity: dict, baseline: int = 2019) -> dict:
    """Latest COMPLETE year against the baseline year."""
    years = ser["annual_years"]
    arr = entity.get("annual") or []
    complete = [y for y in years if y < int(ser["monthly_months"][-1][:4])]
    if not complete or baseline not in years:
        return {}
    latest_year = max(complete)
    a = num(arr[years.index(latest_year)])
    b = num(arr[years.index(baseline)])
    return {"year": latest_year, "value": int(a), "baseline_year": baseline,
            "baseline_value": int(b), "change_pct": pct_change(a, b)}


def parent_position(ser: dict, sector: dict, latest: str) -> dict:
    """Share of parent and rank among siblings, on the SAME window and geography."""
    compare = sector.get("compare_against", "section")
    pcode = sector["parent_division"] if compare == "division" else sector["parent_section"]
    plevel = "division" if compare == "division" else "section"
    parent = find(ser, pcode, plevel) if pcode else None
    entity = find(ser, sector["sic_code"], sector["sic_level"]) if sector["sic_code"] else None
    if parent is None or entity is None:
        return {}

    own, _ = ytd(ser, entity, latest)
    tot, _ = ytd(ser, parent, latest)
    if not tot:
        return {}

    siblings = []
    for g in ser["groups"]:
        if g.get("section") == pcode or g.get("division") == pcode:
            v, _ = ytd(ser, g, latest)
            siblings.append((v, g["code"]))
    siblings.sort(reverse=True)
    rank = next((i + 1 for i, (_, c) in enumerate(siblings) if c == sector["sic_code"]), None)

    return {
        "parent_code": pcode,
        "parent_level": plevel,
        "parent_ytd": tot,
        "share_pct": round(100.0 * own / tot, 1),
        "rank": rank,
        "of": len(siblings),
        "largest_sibling": siblings[0][1] if siblings else None,
        "is_largest": rank == 1,
        "is_second": rank == 2,
    }


def percentile(ser: dict, entity: dict, latest: str) -> float | None:
    """Where the current rolling 12m sits in this sector's own history."""
    months = ser["monthly_months"]
    j = months.index(latest)
    mon = [num(v) for v in (entity.get("monthly") or [])]
    if j < 23:
        return None
    rolls = []
    for end in range(11, j + 1):
        rolls.append(sum(mon[end - 11:end + 1]))
    current = rolls[-1]
    below = sum(1 for r in rolls if r < current)
    return round(100.0 * below / len(rolls), 1)


def sector_metrics(ser: dict, sector: dict, latest: str) -> dict:
    """Every metric for one sector, from one series, in one place."""
    if not sector.get("sic_code"):
        return {}
    entity = find(ser, sector["sic_code"], sector["sic_level"])
    if entity is None:
        return {}

    y, yp = ytd(ser, entity, latest)
    r, rp = rolling(ser, entity, latest)
    months = ser["monthly_months"]
    j = months.index(latest)
    latest_month_value = int(num((entity.get("monthly") or [])[j]))

    # The raw monthly values up to this period, keyed by month. Revision
    # detection needs like-for-like: a restatement is the SAME month carrying a
    # different value in a later release. Comparing derived windows instead
    # (ytd_prior, prior_12m) reports a false restatement for every sector every
    # month, because those windows legitimately move when the period advances.
    mon = entity.get("monthly") or []
    monthly = {months[k]: int(num(mon[k])) for k in range(min(j + 1, len(mon)))}

    ytd_chg, roll_chg = pct_change(y, yp), pct_change(r, rp)
    return {
        "sic_code": sector["sic_code"],
        "sic_level": sector["sic_level"],
        "latest_month": latest,
        "latest_month_value": latest_month_value,
        "ytd": y,
        "ytd_prior": yp,
        "ytd_change_pct": ytd_chg,
        "rolling_12m": r,
        "prior_12m": rp,
        "rolling_change_pct": roll_chg,
        "momentum_delta_pp": (round(roll_chg - ytd_chg, 1)
                              if roll_chg is not None and ytd_chg is not None else None),
        "monthly": monthly,
        "annual": annual(ser, entity),
        "vs_2019": vs_baseline(ser, entity),
        "parent": parent_position(ser, sector, latest),
        "percentile_of_own_history": percentile(ser, entity, latest),
        "volume_confidence": ("higher" if r >= 200 else "moderate" if r >= 50 else "low"),
    }
