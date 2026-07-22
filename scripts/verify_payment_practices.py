#!/usr/bin/env python3
"""Recompute UK payment-practices headline figures straight from the primary
government source, so any published figure is independently reproducible.

WHY THIS EXISTS: figures on published assets must be verifiable from primary
source, not transcribed from a derived repo file. Run this, and every number
matches the government export or it does not ship.

SOURCE (public, no API key):
    https://check-payment-practices.service.gov.uk/export/csv/
    One CSV of every statutory Payment Practices report since 2017. Large UK
    companies (2 of: >£54m turnover, >£27m balance sheet, >250 staff) must
    report twice a year under the Reporting on Payment Practices and
    Performance Regulations 2017. Self-reported and UNAUDITED.

METHOD: latest report per company within a trailing window on report
period-end date (mirrors scripts/datahub/sources/payment_practices.py), with
sanity filters for the data-entry errors the raw file contains (e.g. a
period-end date in year 3025).

NOTE: this file has NO sector/SIC column. Any by-sector figure requires a
Companies House SIC join (needs COMPANIES_HOUSE_API_KEY) and is a Company Debt
derivation, never a government-published number. This script does not produce
sector figures and will not pretend to.

Usage:
    curl -sL -o ppr_export.csv https://check-payment-practices.service.gov.uk/export/csv/
    python scripts/verify_payment_practices.py ppr_export.csv --asof 2026-07-22
"""
import argparse
import csv
import statistics as st
from datetime import date, timedelta

WINDOW_DAYS = 540
EARLIEST = date(2017, 1, 1)


def parse_date(s):
    s = (s or "").strip()
    try:
        return date.fromisoformat(s)
    except ValueError:
        return None


def parse_pct(s):
    s = (s or "").strip()
    try:
        v = float(s)
    except ValueError:
        return None
    return v if 0 <= v <= 100 else None


def parse_days(s):
    s = (s or "").strip()
    try:
        v = float(s)
    except ValueError:
        return None
    return v if 0 <= v <= 366 else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    ap.add_argument("--asof", default=str(date.today()),
                    help="ceiling date; period-ends after this are filer typos")
    ap.add_argument("--window", type=int, default=WINDOW_DAYS)
    args = ap.parse_args()
    asof = date.fromisoformat(args.asof)

    fields = {
        "avg": "Average time to pay",
        "late": "% Invoices not paid within agreed terms",
        "w30": "% Invoices paid within 30 days",
        "d3160": "% Invoices paid between 31 and 60 days",
        "o60": "% Invoices paid later than 60 days",
    }

    rows, max_end = [], None
    with open(args.csv_path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            end = parse_date(r["End date"])
            if end is None or not (EARLIEST <= end <= asof):
                continue
            rows.append((
                r["Company number"].strip(), end, parse_date(r["Filing date"]),
                parse_days(r[fields["avg"]]),
                parse_pct(r[fields["late"]]),
                parse_pct(r[fields["w30"]]),
                parse_pct(r[fields["d3160"]]),
                parse_pct(r[fields["o60"]]),
            ))
            if max_end is None or end > max_end:
                max_end = end

    start = max_end - timedelta(days=args.window)
    latest = {}
    for rec in rows:
        num, end, filing = rec[0], rec[1], rec[2]
        if not num or not (start <= end <= max_end):
            continue
        prev = latest.get(num)
        if prev is None or end > prev[1] or (end == prev[1] and (filing or date.min) > (prev[2] or date.min)):
            latest[num] = rec
    comp = list(latest.values())

    print(f"source rows in range:   {len(rows):,}")
    print(f"latest period-end:      {max_end}")
    print(f"trailing window:        {start} to {max_end} ({args.window} days)")
    print(f"companies (latest each): {len(comp):,}\n")

    labels = [(3, "Average time to pay (days)"),
              (4, "% invoices paid late (past agreed terms)"),
              (5, "% paid within 30 days"),
              (6, "% paid 31 to 60 days"),
              (7, "% paid later than 60 days")]
    for idx, label in labels:
        vals = [c[idx] for c in comp if c[idx] is not None]
        print(f"{label}")
        print(f"    mean {st.mean(vals):.1f}   median {st.median(vals):.1f}   n {len(vals):,}")


if __name__ == "__main__":
    main()
