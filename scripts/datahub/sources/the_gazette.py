"""The Gazette acquisition: corporate insolvency legal-notice counts.

The Gazette publishes statutory insolvency notices. Reading them is public
(no API key). The 'insolvency' notice feed returns JSON; we page a whole month
of corporate-insolvency notices (categorycode 24) and tally them by type.

This is the hub's early-warning layer:
  - winding-up petitions (the pressure signal)
  - petition dismissals (petitions that fell away)
  - winding-up orders (completed compulsory liquidation)
  - administrator / liquidator appointments, CVL resolutions

Important: a Gazette notice records that an event was *advertised* on a date.
It is NOT a completed Insolvency Service statistic, and a petition may be
dismissed, withdrawn or settled (see caveat 'gazette_not_outcome'). The same
procedure appears under several notice codes across the London, Edinburgh and
Belfast gazettes, so we group by code into named metrics below.

Usage:
    python scripts/datahub/sources/the_gazette.py --month 2026-05
"""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data" / "the-gazette"
FEED = "https://www.thegazette.co.uk/insolvency/notice/data.json"
HEADERS = {"User-Agent": "CompanyDebt-DataHub/0.1 (insolvency statistics; +https://companydebt.com)"}
SOURCE_ID = "the_gazette_notices"

# Notice code -> named metric. Multiple codes map to one metric because the
# three UK gazettes use different codes for the same procedure.
CODE_TO_METRIC = {
    "2450": "winding_up_petitions",
    "2461": "winding_up_petition_dismissals",
    "2452": "winding_up_orders",
    "2410": "administrator_appointments",
    "2411": "administration_orders",
    "2432": "liquidator_appointments",
    "2443": "liquidator_appointments",
    "2454": "liquidator_appointments",
    "2431": "winding_up_resolutions_cvl",
    "2441": "winding_up_resolutions_cvl",
}
METRIC_LABELS = {
    "winding_up_petitions": "Winding-up petitions",
    "winding_up_petition_dismissals": "Winding-up petition dismissals",
    "winding_up_orders": "Winding-up orders (compulsory liquidation)",
    "administrator_appointments": "Administrator appointments",
    "administration_orders": "Administration orders",
    "liquidator_appointments": "Liquidator appointments",
    "winding_up_resolutions_cvl": "Resolutions for winding-up (CVL)",
}


def _month_bounds(month: str) -> tuple[str, str]:
    year, mon = (int(p) for p in month.split("-"))
    start = date(year, mon, 1)
    nxt = date(year + (mon == 12), (mon % 12) + 1, 1)
    return start.isoformat(), (nxt - timedelta(days=1)).isoformat()


def _prev_complete_month() -> str:
    first = date.today().replace(day=1)
    last = first - timedelta(days=1)
    return f"{last.year}-{last.month:02d}"


def _category_label(entry: dict) -> str:
    cat = entry.get("category")
    if isinstance(cat, dict):
        return cat.get("@term", "")
    if isinstance(cat, list) and cat:
        return cat[0].get("@term", "")
    return ""


def fetch_month(month: str, *, page_size: int = 100, pause: float = 0.3, max_pages: int = 300) -> dict:
    """Page every corporate-insolvency notice in `month` and tally by type."""
    start, end = _month_bounds(month)
    code_counts: Counter = Counter()
    code_labels: dict[str, str] = {}
    petitions: list[dict] = []
    total_reported = None

    for page in range(1, max_pages + 1):
        params = {
            "start-publish-date": start, "end-publish-date": end,
            "categorycode": "24", "results-page-size": page_size,
            "results-page": page, "sort-by": "latest-date",
        }
        resp = requests.get(FEED, params=params, headers=HEADERS, timeout=40)
        resp.raise_for_status()
        j = resp.json()
        if total_reported is None:
            total_reported = int(j.get("f:total", 0))
        entries = j.get("entry") or []
        if not entries:
            break
        for e in entries:
            code = e.get("f:notice-code", "")
            code_counts[code] += 1
            code_labels.setdefault(code, _category_label(e))
            if code == "2450":  # winding-up petition: keep the company-level record
                petitions.append({
                    "company_name": e.get("title", "").strip(),
                    "published": e.get("published", "")[:10],
                    "notice_url": e.get("id", ""),
                })
        if len(entries) < page_size:
            break
        time.sleep(pause)

    # Roll notice codes up into named metrics.
    metrics: Counter = Counter()
    for code, n in code_counts.items():
        metric = CODE_TO_METRIC.get(code)
        if metric:
            metrics[metric] += n
    total_notices = sum(code_counts.values())

    return {
        "month": month,
        "total_corporate_insolvency_notices": total_notices,
        "total_reported_by_feed": total_reported,
        "metrics": {k: metrics.get(k, 0) for k in METRIC_LABELS},
        "by_notice_code": [
            {"code": c, "label": code_labels[c], "count": code_counts[c]}
            for c in sorted(code_counts, key=lambda c: -code_counts[c])
        ],
        "petitions": petitions,
    }


def _merge_series(month: str, result: dict) -> Path:
    path = DATA_DIR / "monthly_notice_series.json"
    if path.exists():
        doc = json.loads(path.read_text(encoding="utf-8"))
    else:
        doc = {
            "_about": "Monthly corporate-insolvency notice counts from The Gazette, by type. Legal notices, not completed insolvency outcomes.",
            "source_id": SOURCE_ID,
            "metric_labels": METRIC_LABELS,
            "months": {},
        }
    doc["metric_labels"] = METRIC_LABELS
    doc["months"][month] = {
        "total_corporate_insolvency_notices": result["total_corporate_insolvency_notices"],
        "metrics": result["metrics"],
    }
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return path


def _write_release(month: str, result: dict, retrieved_at: str) -> None:
    path = DATA_DIR / "dataset_release.json"
    if path.exists():
        doc = json.loads(path.read_text(encoding="utf-8"))
    else:
        doc = {
            "_about": "Release ledger for The Gazette corporate-insolvency notice tallies.",
            "_schema": [
                "release_id", "source_id", "dataset_name", "period_start", "period_end",
                "publication_date", "source_files", "is_provisional", "status", "notes",
            ],
            "releases": [],
        }
    rel_id = f"gazette_corp_{month}"
    doc["releases"] = [r for r in doc["releases"] if r.get("release_id") != rel_id]
    for r in doc["releases"]:
        if r.get("status") == "current":
            r["status"] = "superseded"
    start, end = _month_bounds(month)
    doc["releases"].append({
        "release_id": rel_id,
        "source_id": SOURCE_ID,
        "dataset_name": f"The Gazette corporate insolvency notices, {month}",
        "period_start": start, "period_end": end,
        "publication_date": retrieved_at,
        "source_files": [{
            "endpoint": FEED,
            "query": f"categorycode=24, {start}..{end}",
            "retrieved_at": retrieved_at,
            "note": "Counts tallied from the public insolvency notice feed; no file artifact.",
        }],
        "is_provisional": True,
        "status": "current",
        "notes": "Legal notices advertised in the month, not completed insolvency outcomes. Late notices can lift a month after the fact.",
    })
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Tally The Gazette corporate insolvency notices for a month")
    ap.add_argument("--month", default=_prev_complete_month(), help="Month YYYY-MM (default: previous complete month)")
    args = ap.parse_args()

    retrieved_at = date.today().isoformat()
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Fetching The Gazette corporate insolvency notices for {args.month} ...")
    result = fetch_month(args.month)

    (DATA_DIR / "petitions_latest.json").write_text(
        json.dumps({"month": args.month, "retrieved_at": retrieved_at,
                    "count": len(result["petitions"]), "petitions": result["petitions"]}, indent=2),
        encoding="utf-8",
    )
    _merge_series(args.month, result)
    _write_release(args.month, result, retrieved_at)

    print(f"  Total corporate insolvency notices: {result['total_corporate_insolvency_notices']:,}")
    for key, label in METRIC_LABELS.items():
        print(f"  {label:42} {result['metrics'][key]:>7,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
