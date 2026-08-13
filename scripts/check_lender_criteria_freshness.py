#!/usr/bin/env python3
"""Flag stale rows in the mortgage-lender CCJ criteria study.

Lender criteria change often. A stale comparison table on a page about
mortgages is worse than no table, so every row in
research/lender-company-ccj-criteria.json carries its own date_checked and
this script is the thing that notices when one has aged out.

Cadence agreed with Piers on 12 August 2026:

  - Halifax, BM Solutions and Barclays  -> re-check every 30 days
  - every other lender                  -> re-check every 183 days

Those three carry the weight of the page: they are the only lenders in the
sample that publish a company-judgment criterion at all. The other eleven are
recorded as silent, and silence moves more slowly than a threshold does.

Exit codes:
  0  every row is inside its cadence
  1  at least one row is overdue
  2  the dataset is missing or unreadable

Run read-only, any time:

    python scripts/check_lender_criteria_freshness.py

Machine-readable, for a scheduled job:

    python scripts/check_lender_criteria_freshness.py --json
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATASET = REPO_ROOT / "research" / "lender-company-ccj-criteria.json"

# Lenders whose rows drive the page's conclusions. Matched case-insensitively
# against the start of the row's "lender" field, so brand suffixes such as
# "(Lloyds Banking Group)" do not need repeating here.
HOT_LENDERS = ("halifax", "bm solutions", "barclays")

HOT_MAX_AGE_DAYS = 30
COLD_MAX_AGE_DAYS = 183

PAGE_SLUG = "company-ccj-mortgage-lender-criteria"


def _parse_check_date(raw: str) -> date | None:
    """Accept the ISO dates the dataset uses; return None if unparseable."""
    try:
        return datetime.strptime(raw.strip(), "%Y-%m-%d").date()
    except (AttributeError, ValueError):
        return None


def _cadence_for(lender: str) -> tuple[int, str]:
    name = (lender or "").strip().lower()
    if name.startswith(HOT_LENDERS):
        return HOT_MAX_AGE_DAYS, "monthly"
    return COLD_MAX_AGE_DAYS, "6-monthly"


def assess(dataset: dict, today: date) -> list[dict]:
    """Return one assessment record per row, newest breach first."""
    rows = []
    for entry in dataset.get("lenders", []):
        lender = entry.get("lender", "(unnamed)")
        book = entry.get("book", "")
        max_age, cadence = _cadence_for(lender)
        checked = _parse_check_date(entry.get("date_checked", ""))

        if checked is None:
            rows.append({
                "lender": lender,
                "book": book,
                "cadence": cadence,
                "date_checked": entry.get("date_checked"),
                "age_days": None,
                "max_age_days": max_age,
                "overdue": True,
                "reason": "date_checked missing or unreadable",
                "source_url": entry.get("source_url"),
            })
            continue

        age = (today - checked).days
        rows.append({
            "lender": lender,
            "book": book,
            "cadence": cadence,
            "date_checked": checked.isoformat(),
            "age_days": age,
            "max_age_days": max_age,
            "overdue": age > max_age,
            "reason": f"{age} days since last check, cadence allows {max_age}",
            "source_url": entry.get("source_url"),
        })

    rows.sort(key=lambda r: (not r["overdue"], -(r["age_days"] or 10**6)))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", action="store_true",
                        help="emit machine-readable output for a scheduled job")
    parser.add_argument("--today", default=None,
                        help="override today's date as YYYY-MM-DD (for testing)")
    args = parser.parse_args()

    if not DATASET.exists():
        print(f"ERROR: dataset not found at {DATASET}", file=sys.stderr)
        return 2

    try:
        dataset = json.loads(DATASET.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        print(f"ERROR: could not read {DATASET.name}: {exc}", file=sys.stderr)
        return 2

    today = _parse_check_date(args.today) if args.today else date.today()
    if today is None:
        print("ERROR: --today must be YYYY-MM-DD", file=sys.stderr)
        return 2

    rows = assess(dataset, today)
    overdue = [r for r in rows if r["overdue"]]

    if args.json:
        print(json.dumps({
            "page_slug": PAGE_SLUG,
            "checked_on": today.isoformat(),
            "total_rows": len(rows),
            "overdue_count": len(overdue),
            "overdue": overdue,
            "rows": rows,
        }, indent=2))
        return 1 if overdue else 0

    print(f"Lender criteria freshness -- {PAGE_SLUG}")
    print(f"  dataset : {DATASET.relative_to(REPO_ROOT)}")
    print(f"  as at   : {today.isoformat()}")
    print(f"  rows    : {len(rows)}  ({len(overdue)} overdue)")
    print()

    for row in rows:
        mark = "OVERDUE" if row["overdue"] else "ok     "
        book = f" [{row['book']}]" if row["book"] else ""
        print(f"  {mark}  {row['lender']}{book}")
        print(f"           {row['cadence']} cadence, {row['reason']}")

    if overdue:
        print()
        print("Re-check these against the lender's published criteria in a browser,")
        print("then update date_checked and the verbatim wording in the dataset and")
        print("the table in the draft. Pull any row you cannot re-verify rather than")
        print("showing a figure nobody has stood behind recently.")
        return 1

    print()
    print("Every row is inside its cadence.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
