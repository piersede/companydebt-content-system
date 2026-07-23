"""Compute a genuine 6-monthly historical trend of average days to pay from the
Payment Practices Reporting bulk export, for Chart A on the payment-practices
data page.

payment_practices_summary.json (built by payment_practices.py) gives one
current headline window; it has no history. The Claude Design reference for
this page shows a 6-period trend line, but its sample figures include a
period that has not happened yet (H2 2026) - clearly placeholder, not real.
This script computes the real thing instead of reusing that shape with real
numbers dropped in.

Unlike payment_practices.py's headline summary, which dedupes to each
company's single MOST RECENT report (one company, one figure, for a snapshot),
a trend needs each company's report IN EVERY PERIOD IT REPORTED, since
companies file roughly every six months across years. So this buckets by the
report's period-end date into six-monthly bins (H1: Jan-Jun, H2: Jul-Dec),
keeping the most-recently-filed report per company PER BIN (not globally) to
avoid double counting a company that (rarely) filed twice for the same bin.

Applies the same row-level sanity bounds as payment_practices.py's
METRIC_COLUMNS (self-reported data carries entry errors: dates in year 3025,
percentages outside 0-100) so a garbage row cannot skew a period average.

Usage:
    python scripts/datahub/sources/payment_practices_trend.py
    python scripts/datahub/sources/payment_practices_trend.py --periods 6
"""

from __future__ import annotations

import argparse
import csv
import io
import json
from datetime import date
from pathlib import Path

from payment_practices import DATA_DIR, EARLIEST_PERIOD, _num, _parse_date

MIN_SAMPLE_SIZE = 30  # below this, a period average is too thin to publish


def _period_of(d: date) -> str:
    half = "H1" if d.month <= 6 else "H2"
    return f"{half} {d.year}"


def _period_bounds(label: str) -> tuple[date, date]:
    half, year = label.split()
    year = int(year)
    return (date(year, 1, 1), date(year, 6, 30)) if half == "H1" else (date(year, 7, 1), date(year, 12, 31))


def compute_trend(raw: bytes, periods: int) -> dict:
    text = raw.decode("utf-8", "replace")
    reader = csv.DictReader(io.StringIO(text))
    today = date.today()

    # (period_label, company_key) -> latest-filed sane record for that period.
    by_period_company: dict[tuple[str, str], dict] = {}

    for row in reader:
        end = _parse_date(row.get("End date", ""))
        if end is None or not (EARLIEST_PERIOD <= end <= today):
            continue
        days = _num(row.get("Average time to pay", ""), 0, 365)
        if days is None:
            continue
        number = (row.get("Company number") or "").strip().upper()
        key = number or (row.get("Company") or "").strip().upper()
        if not key:
            continue
        filed = _parse_date(row.get("Filing date", "")) or end
        period = _period_of(end)
        cell = (period, key)
        prev = by_period_company.get(cell)
        if prev is None or filed > prev["filed"]:
            by_period_company[cell] = {"filed": filed, "days": days}

    by_period: dict[str, list[float]] = {}
    for (period, _key), rec in by_period_company.items():
        by_period.setdefault(period, []).append(rec["days"])

    # A period is only "complete enough" to publish once its window has
    # closed AND late filers have had time to submit: reports are due within
    # 30 days of period end, so require 45 days' clearance as a safety
    # margin. This is the ONLY completeness test - a period ending in an
    # earlier calendar month is not enough on its own, since a period that
    # closed three weeks ago is still mostly unfiled.
    complete_periods = [
        p for p, bounds in ((p, _period_bounds(p)) for p in by_period)
        if (today - bounds[1]).days > 45
    ]
    ordered = sorted(complete_periods, key=lambda p: _period_bounds(p)[0])
    ordered = [p for p in ordered if len(by_period[p]) >= MIN_SAMPLE_SIZE][-periods:]

    return {
        "source_id": "payment_practices_trend",
        "is_enrichment_only": True,
        "metric": "average_days_to_pay",
        "basis": (
            f"Most recently filed report per company per six-monthly period "
            f"(period-end date), sample size >= {MIN_SAMPLE_SIZE} companies."
        ),
        "min_sample_size": MIN_SAMPLE_SIZE,
        "periods": [
            {
                "label": p,
                "average_days_to_pay": round(sum(by_period[p]) / len(by_period[p]), 1),
                "companies": len(by_period[p]),
            }
            for p in ordered
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--periods", type=int, default=6)
    ap.add_argument("--from-file", type=Path, default=None)
    args = ap.parse_args()

    if args.from_file:
        raw = args.from_file.read_bytes()
    else:
        candidates = sorted(DATA_DIR.glob("*-prompt-payments.csv"))
        if not candidates:
            raise SystemExit("No cached export found; run payment_practices.py first "
                              "or pass --from-file.")
        raw = candidates[-1].read_bytes()

    trend = compute_trend(raw, args.periods)
    out_path = DATA_DIR / "payment_practices_trend.json"
    out_path.write_text(json.dumps(trend, indent=2), encoding="utf-8")

    print(f"Computed trend: {len(trend['periods'])} periods")
    for p in trend["periods"]:
        print(f"  {p['label']}: {p['average_days_to_pay']} days (n={p['companies']})")
    print(f"Wrote: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
