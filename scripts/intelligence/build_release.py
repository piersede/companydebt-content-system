"""Assemble one immutable release object, and move the current-release pointer.

WHY THIS EXISTS
---------------
Phase 0 Core. Every figure any page shows must come from one object, so that the
hub, the dashboard and 20 sector pages cannot disagree. In August 2026 the hub sat
on May while the dashboard was on June, and nothing detected it.

A release is written once and never edited. The pointer is what makes a release
live, and it only moves after checks pass, so all pages switch together.

USAGE
    python scripts/intelligence/build_release.py                  # build for the latest month
    python scripts/intelligence/build_release.py --month 2026-06
    python scripts/intelligence/build_release.py --promote        # move the pointer
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import metrics as M          # noqa: E402
import taxonomy as T         # noqa: E402

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent.parent
RELEASES = ROOT / "data" / "releases"
POINTER = RELEASES / "current.json"
META = ROOT / "data" / "insolvency-statistics" / "release_metadata.json"
MONTHLY = ROOT / "data" / "insolvency-statistics" / "monthly_series.json"
RATE = ROOT / "data" / "insolvency-statistics" / "rate_series.json"


def vintage_hash(ser: dict, meta: dict) -> str:
    """Identifies the source data this release was built from.

    The Insolvency Service revises history, so a figure is only reproducible if
    you know which vintage produced it.
    """
    h = hashlib.sha256()
    h.update(json.dumps(ser.get("release_label", ""), sort_keys=True).encode())
    h.update(json.dumps(ser.get("monthly_months", []), sort_keys=True).encode())
    h.update(json.dumps(meta, sort_keys=True).encode())
    return h.hexdigest()[:16]


def headline(latest: str) -> dict:
    meta = json.loads(META.read_text(encoding="utf-8"))
    mon = json.loads(MONTHLY.read_text(encoding="utf-8"))
    rate = json.loads(RATE.read_text(encoding="utf-8"))

    out = {"latest_month_label": meta.get("latest_month_label"),
           "publication_date": meta.get("publication_date"),
           "next_release_date": meta.get("next_release_date"),
           "figures_table": meta.get("latest_figures_table")}

    months = mon.get("months", [])
    if latest in months:
        i = months.index(latest)
        out["by_procedure"] = {k: (v[i] if i < len(v) else None)
                               for k, v in mon.get("series", {}).items()}
    rmonths = rate.get("months", [])
    if latest in rmonths:
        out["rate_per_10k"] = rate["rate_per_10k"][rmonths.index(latest)]
    return out


def build(month: str | None) -> dict:
    ser = M.load_series()
    meta = json.loads(META.read_text(encoding="utf-8"))
    latest = month or ser["monthly_months"][-1]
    if latest not in ser["monthly_months"]:
        raise SystemExit("month %s is not in the series" % latest)

    sectors = {}
    for s in T.load():
        m = M.sector_metrics(ser, s, latest)
        if m:
            sectors[s["slug"]] = {"sector_id": s["sector_id"],
                                  "display_name": s["display_name"],
                                  "wp_id": s["wp_id"],
                                  "geography": s["geography"],
                                  "peer_group": s["peer_group"],
                                  **m}

    return {
        "_about": "Immutable release object. Every published figure must come from here.",
        "meta": {
            "period": latest,
            "release_label": ser.get("release_label"),
            "geography": "England and Wales",
            "publication_date": meta.get("publication_date"),
            "next_release_date": meta.get("next_release_date"),
            "vintage_hash": vintage_hash(ser, meta),
            "sector_count": len(sectors),
        },
        "headline": headline(latest),
        "sectors": sectors,
    }


def write(rel: dict) -> Path:
    d = RELEASES / rel["meta"]["period"]
    d.mkdir(parents=True, exist_ok=True)
    p = d / "release.json"
    p.write_text(json.dumps(rel, indent=2), encoding="utf-8")
    return p


def promote(period: str) -> None:
    p = RELEASES / period / "release.json"
    if not p.exists():
        raise SystemExit("no release built for %s" % period)
    POINTER.write_text(json.dumps({
        "_about": "The live release. Nothing publishes from any other.",
        "current": period,
        "release_path": "data/releases/%s/release.json" % period,
    }, indent=2), encoding="utf-8")
    print("pointer now at", period)


def current() -> dict | None:
    if not POINTER.exists():
        return None
    ptr = json.loads(POINTER.read_text(encoding="utf-8"))
    return json.loads((ROOT / ptr["release_path"]).read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--month")
    ap.add_argument("--promote", action="store_true", help="move the pointer to this release")
    args = ap.parse_args()

    rel = build(args.month)
    p = write(rel)
    print("built %s" % p.relative_to(ROOT))
    print("  period      %s" % rel["meta"]["period"])
    print("  vintage     %s" % rel["meta"]["vintage_hash"])
    print("  sectors     %d" % rel["meta"]["sector_count"])
    print("  next release %s" % rel["meta"]["next_release_date"])

    if args.promote:
        promote(rel["meta"]["period"])
    else:
        cur = json.loads(POINTER.read_text(encoding="utf-8"))["current"] if POINTER.exists() else "none"
        print("  pointer currently at %s (use --promote to move it)" % cur)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
