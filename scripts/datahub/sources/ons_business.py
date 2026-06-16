"""ONS acquisition: UK business population by SIC section (denominators).

Source: Nomis "UK Business Counts - enterprises by industry and employment size
band" (dataset NM_142_1), the ONS business population. Public, no API key.

Nomis only exposes detailed (5-digit SIC) industries plus a grand Total, so we
pull every detailed industry for the UK and roll them up into SIC sections
ourselves. A self-check confirms the rolled-up sections sum to the official
Total (within ONS's round-to-5 noise).

Use: sector and regional CONTEXT / denominators. Important: these are
enterprises (VAT/PAYE-registered businesses incl. sole traders and
partnerships), a DIFFERENT universe from Companies House registered companies.
Do not divide company insolvencies by this to get a precise company rate; the
headline insolvency rate uses the Companies House register. See caveat
'ons_denominator'.

Usage:
    python scripts/datahub/sources/ons_business.py            # latest year
    python scripts/datahub/sources/ons_business.py --year 2024
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data" / "ons-business"
BASE = "https://www.nomisweb.co.uk/api/v01/dataset/NM_142_1.data.json"
HEADERS = {"User-Agent": "CompanyDebt-DataHub/0.1 (insolvency statistics; +https://companydebt.com)"}
SOURCE_ID = "ons_business"
GEOG_UK = "2092957697"

# SIC 2007 division (2-digit) -> section letter, with a short label per section.
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


def _section_for_division(div: int) -> str:
    for sec, lo, hi, _ in SECTION_RANGES:
        if lo <= div <= hi:
            return sec
    return "?"


def fetch_business_population(year: str = "latest") -> dict:
    """Fetch UK enterprises by detailed SIC, roll up to sections, self-check."""
    params = {
        "geography": GEOG_UK, "employment_sizeband": "0", "legal_status": "0",
        "measures": "20100", "time": year,
    }
    resp = requests.get(BASE, params=params, headers=HEADERS, timeout=90)
    resp.raise_for_status()
    obs = resp.json().get("obs", [])

    section_counts: dict[str, int] = defaultdict(int)
    official_total = None
    data_year = None
    leaf_pat = re.compile(r"^(\d{2})\d{3} : ")
    for o in obs:
        desc = o["industry"]["description"]
        val = o["obs_value"]["value"]
        data_year = data_year or o["time"]["value"]
        if desc.strip() == "Total":
            official_total = int(val) if val is not None else None
            continue
        m = leaf_pat.match(desc)
        if m and val is not None:
            section_counts[_section_for_division(int(m.group(1)))] += int(val)

    rolled_total = sum(section_counts.values())
    sections = [
        {"code": s, "label": SECTION_LABELS[s], "count": section_counts[s]}
        for s, _, _, _ in SECTION_RANGES if section_counts.get(s)
    ]
    sections.sort(key=lambda d: -d["count"])

    return {
        "source_id": SOURCE_ID,
        "dataset": "NM_142_1",
        "year": data_year,
        "uk_total_enterprises": official_total,
        "rolled_section_total": rolled_total,
        "rollup_matches_total": official_total is not None and abs(rolled_total - official_total) <= 50,
        "unit": "enterprises",
        "sections": sections,
        "rounding": "ONS rounds each cell to the nearest 5; section sums carry small rounding noise.",
        "note": "Enterprises = VAT/PAYE-registered businesses (incl. sole traders and partnerships). A different universe from Companies House registered companies. Sector context only, not a precise company-insolvency denominator.",
        "caveats": ["ons_denominator", "sector_volumes_not_rates"],
    }


def _write_release(result: dict, retrieved_at: str) -> None:
    path = DATA_DIR / "dataset_release.json"
    if path.exists():
        doc = json.loads(path.read_text(encoding="utf-8"))
    else:
        doc = {
            "_about": "Release ledger for ONS/Nomis UK Business Counts (enterprises by SIC section).",
            "_schema": [
                "release_id", "source_id", "dataset_name", "period_start", "period_end",
                "publication_date", "source_files", "is_provisional", "status", "notes",
            ],
            "releases": [],
        }
    year = result["year"]
    rel_id = f"ons_business_counts_{year}"
    doc["releases"] = [r for r in doc["releases"] if r.get("release_id") != rel_id]
    for r in doc["releases"]:
        if r.get("status") == "current":
            r["status"] = "superseded"
    doc["releases"].append({
        "release_id": rel_id,
        "source_id": SOURCE_ID,
        "dataset_name": f"ONS UK Business Counts - enterprises by SIC section, {year}",
        "period_start": f"{year}-01", "period_end": f"{year}-12",
        "publication_date": retrieved_at,
        "source_files": [{
            "endpoint": BASE,
            "query": f"geography={GEOG_UK}, all industries, time={year}",
            "retrieved_at": retrieved_at,
            "note": "Detailed SIC pulled and rolled up to sections; no file artifact.",
        }],
        "is_provisional": False,
        "status": "current",
        "notes": "Annual business population. Enterprises universe, not registered companies. Rolled-up sections validated against the official Total.",
    })
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Fetch ONS UK business population by SIC section")
    ap.add_argument("--year", default="latest", help="Year (e.g. 2025) or 'latest'")
    args = ap.parse_args()

    retrieved_at = date.today().isoformat()
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("Fetching ONS UK Business Counts (enterprises) ...")
    result = fetch_business_population(args.year)

    (DATA_DIR / "business_population.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    _write_release(result, retrieved_at)

    print(f"  Year: {result['year']}")
    print(f"  UK total enterprises: {result['uk_total_enterprises']:,}")
    print(f"  Rollup self-check matches official total: {result['rollup_matches_total']}")
    print("  Top sections by business count:")
    for s in result["sections"][:6]:
        print(f"    {s['code']} {s['label']:26} {s['count']:>10,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
