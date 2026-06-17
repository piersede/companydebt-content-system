"""Payment practices acquisition: late-payment ENRICHMENT context only.

ENRICHMENT, NOT INSOLVENCY. UK statutory "Payment Practices and Performance"
reporting requires large companies and LLPs to report, twice a year, how
promptly they pay suppliers. This is useful CONTEXT on payment stress in the
economy - it is NOT an insolvency statistic and must NEVER be blended into, or
presented as, insolvency figures (see caveat 'payment_practices_enrichment').

Source: the public bulk export at
https://check-payment-practices.service.gov.uk/export, whose "Get CSV File"
button points at /export/csv/. That endpoint streams a SINGLE CSV containing
every report ever filed (~100 MB, 110k+ rows since 2017), not per-period files.
Open data, no API key, no registration.

Two awkward shapes of this source, handled below:
  - Reporting periods are biannual PER COMPANY and staggered, so there is no
    single aligned national "reporting period". We summarise a trailing window
    on the report's period-end date (see _recent_window / RECENT_WINDOW_DAYS).
  - The data is self-reported and unaudited, so it carries entry errors (period
    end dates in the year 3025, payment percentages outside 0-100). We sanity-
    filter every value before averaging (see caveats 'payment_self_reported').

The export carries NO sector/SIC column, so a clean sector breakdown is not
supported by this file alone (it would need a Companies House join, out of
scope here). We say so rather than fabricate one.

Usage:
    python scripts/datahub/sources/payment_practices.py            # download + summarise
    python scripts/datahub/sources/payment_practices.py --from-file <saved.csv>
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import time
from datetime import date, timedelta
from pathlib import Path
from statistics import mean, median

import requests

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data" / "payment-practices"
EXPORT_PAGE = "https://check-payment-practices.service.gov.uk/export"
EXPORT_CSV = "https://check-payment-practices.service.gov.uk/export/csv/"
HEADERS = {"User-Agent": "CompanyDebt-DataHub/0.1 (insolvency statistics; +https://companydebt.com)"}
SOURCE_ID = "payment_practices"

# Earliest the reporting regime existed; anything before is an entry error.
EARLIEST_PERIOD = date(2017, 1, 1)
# Trailing window (on report period-end date) used for the headline summary.
# 540 days ~= the most recent ~3 half-year periods, so most reporting companies
# appear at least once even with the usual filing lag.
RECENT_WINDOW_DAYS = 540
# Companies House allows 600 requests / 5 min. Pace SIC lookups just under that
# (1 per 0.55s) so a large sector join never trips the rolling rate limit.
SIC_PACE_SECONDS = 0.55

# CSV column -> (summary key, lower bound, upper bound) for the numeric headline
# metrics. Bounds reject the self-reported entry errors before averaging.
METRIC_COLUMNS = {
    "Average time to pay": ("average_days_to_pay", 0, 365),
    "% Invoices paid within 30 days": ("pct_paid_within_30_days", 0, 100),
    "% Invoices paid between 31 and 60 days": ("pct_paid_31_to_60_days", 0, 100),
    "% Invoices paid later than 60 days": ("pct_paid_later_than_60_days", 0, 100),
    "% Invoices not paid within agreed terms": ("pct_invoices_paid_late", 0, 100),
}
METRIC_LABELS = {
    "average_days_to_pay": "Average days to pay an invoice",
    "pct_invoices_paid_late": "% of invoices not paid within agreed terms",
    "pct_paid_within_30_days": "% of invoices paid within 30 days",
    "pct_paid_31_to_60_days": "% of invoices paid in 31-60 days",
    "pct_paid_later_than_60_days": "% of invoices paid later than 60 days",
}

# SIC 2007 division (2-digit) -> section letter + label. Mirrors the rollup in
# ons_business.py so the payment-practices sector split lines up with the ONS
# business-population sections used elsewhere in the hub.
SECTION_RANGES = [
    ("A", 1, 3, "Agriculture, forestry and fishing"),
    ("B", 5, 9, "Mining and quarrying"),
    ("C", 10, 33, "Manufacturing"),
    ("D", 35, 35, "Electricity and gas"),
    ("E", 36, 39, "Water and waste"),
    ("F", 41, 43, "Construction"),
    ("G", 45, 47, "Wholesale and retail"),
    ("H", 49, 53, "Transport and storage"),
    ("I", 55, 56, "Accommodation and food"),
    ("J", 58, 63, "Information and communication"),
    ("K", 64, 66, "Finance and insurance"),
    ("L", 68, 68, "Real estate"),
    ("M", 69, 75, "Professional services"),
    ("N", 77, 82, "Admin and support"),
    ("O", 84, 84, "Public administration"),
    ("P", 85, 85, "Education"),
    ("Q", 86, 88, "Health and social work"),
    ("R", 90, 93, "Arts and recreation"),
    ("S", 94, 96, "Other services"),
    ("T", 97, 98, "Households as employers"),
    ("U", 99, 99, "Extraterritorial"),
]
SECTION_LABELS = {s: lab for s, _, _, lab in SECTION_RANGES}

_DATE_PAT = re.compile(r"^(\d{4})-(\d{2})-(\d{2})")


def _section_for_division(div: int) -> str | None:
    for sec, lo, hi, _ in SECTION_RANGES:
        if lo <= div <= hi:
            return sec
    return None


def _primary_section(sic_codes: list | None) -> str | None:
    """Map a company's primary (first) SIC code to a SIC section letter."""
    if not sic_codes:
        return None
    code = str(sic_codes[0]).strip()
    if len(code) >= 2 and code[:2].isdigit():
        return _section_for_division(int(code[:2]))
    return None


def _parse_date(value: str) -> date | None:
    """Parse an ISO-ish date, or None. Used to sanity-check period bounds."""
    m = _DATE_PAT.match((value or "").strip())
    if not m:
        return None
    try:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def _num(value: str, lo: float, hi: float) -> float | None:
    """Parse a number inside [lo, hi]; reject blanks, 'None', and entry errors."""
    s = (value or "").strip()
    if not s or s.lower() == "none":
        return None
    try:
        n = float(s)
    except ValueError:
        return None
    return n if lo <= n <= hi else None


def download_export(retrieved_at: str) -> tuple[Path, bytes]:
    """Download the bulk CSV to data/payment-practices/, return (path, bytes).

    The server names the file with a date stamp via Content-Disposition; we keep
    that name so the raw artifact is traceable to the day it was pulled.
    """
    resp = requests.get(EXPORT_CSV, headers=HEADERS, timeout=300)
    resp.raise_for_status()
    disp = resp.headers.get("content-disposition", "")
    m = re.search(r'filename="?([^"]+)"?', disp)
    name = m.group(1) if m else f"{retrieved_at}-prompt-payments.csv"
    path = DATA_DIR / name
    path.write_bytes(resp.content)
    return path, resp.content


def _recent_window(period_ends: list[date]) -> tuple[date, date]:
    """Trailing window on report period-end date for the headline summary.

    There is no single national reporting period (companies report on staggered
    biannual cycles), so we anchor on the latest sane period-end seen and look
    back RECENT_WINDOW_DAYS. Returns (window_start, window_end).
    """
    latest = max(period_ends)
    return latest - timedelta(days=RECENT_WINDOW_DAYS), latest


def _parse_window(raw: bytes) -> tuple[int, dict[str, dict], date, date, list[dict]]:
    """Parse the export down to the deduped window records.

    To avoid double-counting (companies report twice a year), we keep only each
    company's MOST RECENT sane report, then restrict that deduped set to the
    trailing window so the headline reflects currently-active reporters - one
    company, one figure. Returns (all_time, latest_by_company, window_start,
    window_end, recent_records).
    """
    text = raw.decode("utf-8", "replace")
    reader = csv.DictReader(io.StringIO(text))

    all_time = 0
    today = date.today()
    latest_by_company: dict[str, dict] = {}  # company key -> latest sane report

    for row in reader:
        all_time += 1
        end = _parse_date(row.get("End date", ""))
        if end is None or not (EARLIEST_PERIOD <= end <= today):
            continue  # entry error or out-of-range period; skip
        number = (row.get("Company number") or "").strip().upper()
        key = number or (row.get("Company") or "").strip().upper()
        if not key:
            continue
        filed = _parse_date(row.get("Filing date", "")) or end
        prev = latest_by_company.get(key)
        # Keep the most recent report per company (tie-break on filing date).
        if prev is None or (end, filed) > (prev["end"], prev["filed"]):
            latest_by_company[key] = {
                "number": number,
                "end": end,
                "filed": filed,
                "values": {k: _num(row.get(col, ""), lo, hi)
                           for col, (k, lo, hi) in METRIC_COLUMNS.items()},
            }

    if not latest_by_company:
        raise SystemExit("No reports with a sane period-end date found in the export.")

    deduped = list(latest_by_company.values())
    window_start, window_end = _recent_window([r["end"] for r in deduped])
    recent = [r for r in deduped if window_start <= r["end"] <= window_end]
    return all_time, latest_by_company, window_start, window_end, recent


def _aggregate(records: list[dict]) -> dict:
    """Mean/median/n per headline metric over a set of records."""
    out = {}
    for key in METRIC_LABELS:
        vals = [r["values"][key] for r in records if r["values"][key] is not None]
        out[key] = {
            "label": METRIC_LABELS[key],
            "mean": round(mean(vals), 1) if vals else None,
            "median": round(median(vals), 1) if vals else None,
            "n": len(vals),
        }
    return out


def summarise(raw: bytes) -> dict:
    """Build the COMPACT headline summary (no raw dump). No sector join."""
    all_time, latest_by_company, window_start, window_end, recent = _parse_window(raw)
    return {
        "source_id": SOURCE_ID,
        "is_enrichment_only": True,
        "all_time_report_count": all_time,
        "distinct_companies_all_time": len(latest_by_company),
        "basis": "latest report per company, restricted to the trailing window (no double-counting)",
        "latest_period": {"start": window_start.isoformat(), "end": window_end.isoformat()},
        "reporting_companies_in_window": len(recent),
        "window_days": RECENT_WINDOW_DAYS,
        "headline": _aggregate(recent),
        "sector_breakdown": None,
        "sector_note": "Run with --with-sectors to add a SIC-section breakdown via a Companies House join.",
        "note": "ENRICHMENT/CONTEXT ONLY. Self-reported large-company payment behaviour. Not an insolvency statistic and must never be blended into insolvency figures.",
        "caveats": ["payment_practices_enrichment", "payment_self_reported", "payment_large_companies_only"],
    }


def enrich_sectors(recent: list[dict], cache_path: Path) -> tuple[list[dict], dict]:
    """Join window companies to Companies House SIC, roll up to SIC sections.

    Each window company's primary SIC code is fetched from Companies House (the
    export has no sector field) and mapped to a SIC section. Lookups are cached
    to `cache_path` so re-runs are instant and a long run is resumable. Returns
    (sector_breakdown, coverage). Still ENRICHMENT ONLY - this is payment
    behaviour by sector, never a sector insolvency figure.
    """
    from companies_house import CompaniesHouseClient  # local import; needs API key

    cache: dict[str, str | None] = {}
    if cache_path.exists():
        cache = json.loads(cache_path.read_text(encoding="utf-8"))

    client = CompaniesHouseClient()
    numbered = [r for r in recent if r["number"]]
    looked_up = 0
    for i, rec in enumerate(numbered, 1):
        num = rec["number"]
        if num in cache:
            continue  # already resolved on a previous run; no API call
        while True:
            try:
                profile = client.get_company(num)
                cache[num] = _primary_section(profile.get("sic_codes"))
                break
            except requests.HTTPError as exc:
                code = exc.response.status_code if exc.response is not None else None
                if code == 404:  # removed / changed number -> unknown
                    cache[num] = None
                    break
                if code == 429:  # quota exhausted: save progress, outwait the window
                    cache_path.write_text(json.dumps(cache, indent=2), encoding="utf-8")
                    print(f"    rate limited at {i}/{len(numbered)}; pausing 60s then resuming")
                    time.sleep(60)
                    continue
                raise
        looked_up += 1
        time.sleep(SIC_PACE_SECONDS)  # stay under 600 requests / 5 min
        if looked_up % 100 == 0:
            cache_path.write_text(json.dumps(cache, indent=2), encoding="utf-8")
            print(f"    SIC lookups: {i}/{len(numbered)} ({looked_up} fetched this run, rest cached)")
    cache_path.write_text(json.dumps(cache, indent=2), encoding="utf-8")

    # Roll the window records up by section using the resolved SIC.
    by_section: dict[str, list[dict]] = {}
    resolved = unknown = 0
    for rec in numbered:
        sec = cache.get(rec["number"])
        if sec is None:
            unknown += 1
            continue
        resolved += 1
        by_section.setdefault(sec, []).append(rec)

    sectors = []
    for sec, recs in by_section.items():
        agg = _aggregate(recs)
        sectors.append({
            "code": sec,
            "label": SECTION_LABELS.get(sec, sec),
            "companies": len(recs),
            "average_days_to_pay_mean": agg["average_days_to_pay"]["mean"],
            "pct_invoices_paid_late_mean": agg["pct_invoices_paid_late"]["mean"],
            "pct_paid_within_30_days_mean": agg["pct_paid_within_30_days"]["mean"],
        })
    sectors.sort(key=lambda d: -d["companies"])

    coverage = {
        "companies_in_window": len(recent),
        "with_company_number": len(numbered),
        "sic_resolved": resolved,
        "sic_unknown": unknown,
        "note": "Primary (first) SIC code only; companies with no resolvable SIC are excluded from the sector split. Sector figures are payment behaviour, never insolvency rates.",
    }
    return sectors, coverage


def _write_summary(summary: dict) -> Path:
    path = DATA_DIR / "payment_practices_summary.json"
    path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return path


def _write_release(summary: dict, raw_path: Path, raw: bytes, retrieved_at: str) -> None:
    """Append a release; mark any prior 'current' superseded (like siblings)."""
    path = DATA_DIR / "dataset_release.json"
    if path.exists():
        doc = json.loads(path.read_text(encoding="utf-8"))
    else:
        doc = {
            "_about": "Release ledger for UK Payment Practices and Performance reporting. ENRICHMENT/CONTEXT ONLY - late-payment behaviour of large companies, never an insolvency statistic.",
            "_schema": [
                "release_id", "source_id", "dataset_name", "period_start", "period_end",
                "publication_date", "source_files", "is_provisional", "status", "notes",
            ],
            "releases": [],
        }
    rel_id = f"payment_practices_{retrieved_at}"
    doc["releases"] = [r for r in doc["releases"] if r.get("release_id") != rel_id]
    for r in doc["releases"]:
        if r.get("status") == "current":
            r["status"] = "superseded"
    doc["releases"].append({
        "release_id": rel_id,
        "source_id": SOURCE_ID,
        "dataset_name": f"UK payment practices export, pulled {retrieved_at}",
        "period_start": summary["latest_period"]["start"],
        "period_end": summary["latest_period"]["end"],
        "publication_date": retrieved_at,
        "source_files": [{
            "endpoint": EXPORT_CSV,
            "filename": raw_path.name,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
            "retrieved_at": retrieved_at,
            "note": "Full bulk export (all reports since 2017); headline summary is a trailing window on period-end date.",
        }],
        "is_provisional": True,
        "status": "current",
        "notes": "ENRICHMENT ONLY: self-reported large-company payment performance, not an insolvency statistic. Rolling export with no fixed publication period; period bounds are the trailing summary window, not a national reporting period.",
    })
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Fetch UK payment practices export (ENRICHMENT context only)")
    ap.add_argument("--from-file", help="Summarise a previously downloaded CSV instead of downloading")
    ap.add_argument("--with-sectors", action="store_true",
                    help="Add a SIC-section breakdown via a Companies House join (needs COMPANIES_HOUSE_API_KEY; slow on first run, then cached)")
    args = ap.parse_args()

    retrieved_at = date.today().isoformat()
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if args.from_file:
        raw_path = Path(args.from_file)
        raw = raw_path.read_bytes()
        print(f"Summarising local file {raw_path.name} ({len(raw) / 1e6:.0f} MB) ...")
    else:
        print("Downloading payment practices bulk export (~100 MB) ...")
        raw_path, raw = download_export(retrieved_at)
        print(f"  Saved raw CSV: {raw_path.name} ({len(raw) / 1e6:.0f} MB)")

    summary = summarise(raw)

    if args.with_sectors:
        print("Joining window companies to Companies House SIC sections ...")
        _, _, _, _, recent = _parse_window(raw)
        sectors, coverage = enrich_sectors(recent, DATA_DIR / "sic_cache.json")
        summary["sector_breakdown"] = sectors
        summary["sector_coverage"] = coverage
        summary["sector_note"] = "Payment behaviour by SIC section, joined from Companies House (primary SIC). Sector context only, never a sector insolvency rate."

    _write_summary(summary)
    _write_release(summary, raw_path, raw, retrieved_at)

    print("\nENRICHMENT ONLY - late-payment context, NOT an insolvency statistic.")
    print(f"  All-time reports in export:   {summary['all_time_report_count']:,}")
    print(f"  Distinct companies all-time:  {summary['distinct_companies_all_time']:,}")
    lp = summary["latest_period"]
    print(f"  Headline window (period end): {lp['start']} .. {lp['end']}")
    print(f"  Reporting companies in window:{summary['reporting_companies_in_window']:,}")
    for key, h in summary["headline"].items():
        unit = "days" if key == "average_days_to_pay" else "%"
        print(f"  {h['label']:42} mean {h['mean']!s:>6} {unit:<4} median {h['median']!s:>6} (n={h['n']:,})")
    if summary.get("sector_breakdown"):
        cov = summary["sector_coverage"]
        print(f"\n  Sector split (SIC resolved for {cov['sic_resolved']}/{cov['with_company_number']} companies):")
        for s in summary["sector_breakdown"][:8]:
            print(f"    {s['code']} {s['label']:26} n={s['companies']:>5}  "
                  f"avg pay {s['average_days_to_pay_mean']!s:>5}d  late {s['pct_invoices_paid_late_mean']!s:>5}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
