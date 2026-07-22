"""Parse Table A1b (company insolvencies by 3-level SIC) from the Insolvency
Service source workbook into a clean by-sector time series for the data hub.

Output: data/insolvency-statistics/sector_series.json
  {
    "release_label": "April 2026",
    "annual_years": [2016, ..., 2025],
    "monthly_months": ["2023-01", ..., "2026-04"],
    "total": {"annual": [...], "monthly": [...]},
    "sections": [ {code, label, annual:[...], monthly:[...]} , ... ],   # 21 SIC sections
    "construction": {                                                    # Section F detail
        "section": {...},
        "subsectors": [ {code, level, label, annual:[...], monthly:[...]}, ... ]
    },
    "groups": [ {code, section, division, label, annual:[...], monthly:[...]}, ... ],   # all ~272 3-digit SIC groups
    "divisions": [ {code, section, label, annual:[...], monthly:[...]}, ... ]           # all ~90 2-digit SIC divisions
  }

"groups"/"divisions" are a generic, code-keyed capture of every row in Table A1b
(not just Construction), for single-SIC-sector pages (e.g. furniture = group
310) that don't need a bespoke sub-sector breakdown like Construction has.

Annual covers 2016 onward; monthly only from Jan 2023 (the source does not
publish monthly-by-industry before then). Suppressed cells ([x]/[z]/[c]) -> null.
Idempotent. Run after each quarterly (Jan/Apr/Jul/Oct) release refreshes the xlsx.

Usage:
    python scripts/datahub/parse_sector_series.py
"""

from __future__ import annotations

import glob
import json
import re
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "insolvency-statistics"
OUT = DATA / "sector_series.json"

MONTHS = {m: i + 1 for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])}


def to_num(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return int(v)
    s = str(v).strip()
    if s.isdigit():
        return int(s)
    return None  # [x] [z] [c] or blank -> suppressed/not available


def title(label: str) -> str:
    """'CONSTRUCTION' -> 'Construction'; keep short, drop trailing detail."""
    s = (label or "").strip()
    return s[:1].upper() + s[1:].lower() if s.isupper() else s


def main() -> int:
    xlsx = sorted(glob.glob(str(DATA / "source_data_tables_*.xlsx")))[-1]
    release = re.search(r"(\d{4})-(\d{2})", xlsx)
    wb = openpyxl.load_workbook(xlsx, read_only=True, data_only=True)
    rows = list(wb["Table_1c"].iter_rows(values_only=True))

    # Header row begins with 'Section'.
    hi = next(i for i, r in enumerate(rows) if r and r[0] == "Section")
    header = rows[hi]
    annual_cols, monthly_cols = {}, {}
    for ci, label in enumerate(header):
        if label is None:
            continue
        lab = str(label).strip()
        if re.fullmatch(r"20\d{2}", lab):
            annual_cols[int(lab)] = ci
        elif re.fullmatch(r"[A-Z][a-z]{2} 20\d{2}", lab):
            mon, yr = lab.split()
            monthly_cols[f"{yr}-{MONTHS[mon]:02d}"] = ci

    annual_years = sorted(annual_cols)
    monthly_months = sorted(monthly_cols)

    def series(r):
        return (
            [to_num(r[annual_cols[y]]) for y in annual_years],
            [to_num(r[monthly_cols[m]]) for m in monthly_months],
        )

    sections, total, construction_sub = [], None, []
    groups, divisions = [], []
    for r in rows[hi + 1:]:
        if not r or r[0] in (None, "", "Back to top"):
            continue
        code, div, grp, desc = r[0], r[1], r[2], r[3]
        div = None if div in (None, "", "-") else div   # Total row uses '-'
        grp = None if grp in (None, "", "-") else grp
        a, mth = series(r)
        is_section = (div in (None, "")) and (grp in (None, ""))
        if code == "Total" and is_section:
            total = {"annual": a, "monthly": mth}
        elif is_section and isinstance(code, str) and len(code) == 1 and code.isalpha():
            sections.append({"code": code, "label": title(desc), "annual": a, "monthly": mth})
        if code == "F" and not is_section:  # construction sub-sectors
            construction_sub.append({
                "code": (str(grp) if grp not in (None, "") else str(div)),
                "level": "group" if grp not in (None, "") else "division",
                "label": title(desc), "annual": a, "monthly": mth,
            })
        if not is_section and grp not in (None, ""):  # generic 3-digit SIC group
            groups.append({
                "code": str(grp), "section": code, "division": str(div) if div else None,
                "label": title(desc), "annual": a, "monthly": mth,
            })
        elif not is_section and div not in (None, ""):  # generic 2-digit SIC division
            divisions.append({
                "code": str(div), "section": code, "label": title(desc), "annual": a, "monthly": mth,
            })

    construction_section = next((s for s in sections if s["code"] == "F"), None)
    out = {
        "release_label": f"{release.group(0)}" if release else "",
        "annual_years": annual_years,
        "monthly_months": monthly_months,
        "total": total,
        "sections": sections,
        "construction": {"section": construction_section, "subsectors": construction_sub},
        "groups": groups,
        "divisions": divisions,
    }
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"Wrote {OUT.name}: {len(sections)} sections, {len(groups)} groups, {len(divisions)} divisions, "
          f"annual {annual_years[0]}-{annual_years[-1]}, "
          f"monthly {monthly_months[0]}..{monthly_months[-1]} ({len(monthly_months)} months), "
          f"{len(construction_sub)} construction sub-sectors")
    # quick proof
    f = construction_section
    print(f"  Construction (F) annual: {f['annual']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
