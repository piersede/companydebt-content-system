"""Export downloadable CSV distributions for the data-hub Dataset schema.

Each data page's Dataset JSON-LD (mu-plugins/cd-insolvency-data-hub.php) points
its `distribution` at one of these CSVs. The CSVs are generated from the SAME real
source data the pages render (data/insolvency-statistics, data/the-gazette,
data/companies-house, data/payment-practices) so the download matches the page.

Writes to data/distributions/*.csv (version-controlled provenance). Deploy to the
public theme-assets path with scripts/datahub/upload_distributions.py.

Run:  PYTHONIOENCODING=utf-8 python scripts/datahub/export_distributions.py
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
OUT = DATA / "distributions"


def _load(rel: str) -> dict:
    return json.loads((DATA / rel).read_text(encoding="utf-8"))


def _write(name: str, header: list[str], rows: list[list]) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    # newline="" + \n lineterminator => stable LF CSV, no platform CRLF surprises
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    print(f"wrote {path.relative_to(ROOT)}  ({len(rows)} rows)")
    return path


def export_insolvency() -> None:
    ms = _load("insolvency-statistics/monthly_series.json")
    rs = _load("insolvency-statistics/rate_series.json")
    rate_by_month = dict(zip(rs["months"], rs["rate_per_10k"]))
    s = ms["series"]
    months = ms["months"]
    rows = []
    for i, m in enumerate(months):
        rows.append([
            m,
            s["total"][i],
            s["cvls"][i],
            s["compulsory"][i],
            s["administrations"][i],
            s["cvas"][i],
            s["receiverships"][i],
            rate_by_month.get(m, ""),
        ])
    _write(
        "uk-company-insolvency-statistics.csv",
        ["month", "total_insolvencies", "cvl", "compulsory_liquidation",
         "administration", "cva", "receivership", "rate_per_10k_12m_rolling"],
        rows,
    )


def export_petitions() -> None:
    gz = _load("the-gazette/monthly_notice_series.json")
    months = sorted(gz["months"].keys())  # ISO YYYY-MM sorts chronologically
    rows = []
    for m in months:
        rec = gz["months"][m]
        met = rec.get("metrics", {})
        rows.append([
            m,
            rec.get("total_corporate_insolvency_notices", ""),
            met.get("winding_up_petitions", ""),
            met.get("winding_up_petition_dismissals", ""),
            met.get("winding_up_orders", ""),
            met.get("administrator_appointments", ""),
            met.get("administration_orders", ""),
            met.get("liquidator_appointments", ""),
            met.get("winding_up_resolutions_cvl", ""),
        ])
    _write(
        "uk-winding-up-petition-notices.csv",
        ["month", "total_corporate_insolvency_notices", "winding_up_petitions",
         "winding_up_petition_dismissals", "winding_up_orders",
         "administrator_appointments", "administration_orders",
         "liquidator_appointments", "winding_up_resolutions_cvl"],
        rows,
    )


def export_dissolutions() -> None:
    ch = _load("companies-house/monthly_flows_series.json")
    ms = _load("insolvency-statistics/monthly_series.json")
    ins_by_month = dict(zip(ms["months"], ms["series"]["total"]))
    months = sorted(ch["months"].keys())
    rows = []
    for m in months:
        rec = ch["months"][m]
        rows.append([
            m,
            rec.get("incorporations", ""),
            rec.get("dissolutions", ""),
            ins_by_month.get(m, ""),  # insolvencies for context; blank if not yet released
        ])
    _write(
        "uk-company-dissolutions-vs-insolvencies.csv",
        ["month", "incorporations", "dissolutions", "company_insolvencies"],
        rows,
    )


def export_payment() -> None:
    pay = _load("payment-practices/payment_practices_summary.json")
    rows = []
    for sec in pay["sector_breakdown"]:
        rows.append([
            sec.get("code", ""),
            sec.get("label", ""),
            sec.get("companies", ""),
            sec.get("average_days_to_pay_mean", ""),
            sec.get("pct_invoices_paid_late_mean", ""),
            sec.get("pct_paid_within_30_days_mean", ""),
        ])
    _write(
        "uk-payment-practices-by-sector.csv",
        ["sic_section_code", "sector", "reporting_companies",
         "avg_days_to_pay", "pct_invoices_paid_late", "pct_paid_within_30_days"],
        rows,
    )


def main() -> int:
    export_insolvency()
    export_petitions()
    export_dissolutions()
    export_payment()
    print(f"\nAll distributions written to {OUT.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
