"""Detect what the Insolvency Service changed between two releases.

WHY THIS EXISTS
---------------
The monthly figures are provisional. History gets restated, quietly. Without a
comparison we cannot tell a genuine trend change from a revision to last month's
number, and we would publish the difference as news.

This compares two built release objects and reports three things: figures the
source restated, sectors whose direction flipped, and sectors that crossed a
volume-confidence band. It reads releases only. It never edits one.

USAGE
    python scripts/intelligence/revisions.py --from 2026-06 --to 2026-07
    python scripts/intelligence/revisions.py --from 2026-06 --to 2026-07 --threshold 1.0
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
RELEASES = ROOT / "data" / "releases"

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Figures that describe a period both releases cover, so a change means the
# source restated history rather than simply adding a new month.
RESTATABLE = ["ytd_prior", "prior_12m"]


def load(period: str) -> dict:
    p = RELEASES / period / "release.json"
    if not p.exists():
        raise SystemExit("no release built for %s" % period)
    return json.loads(p.read_text(encoding="utf-8"))


def direction(pct) -> str:
    if pct is None:
        return "unknown"
    if pct <= -5:
        return "improving"
    if pct >= 5:
        return "deteriorating"
    return "broadly stable"


def compare(a: dict, b: dict, threshold: float) -> dict:
    restated, flipped, banded, annual_changed = [], [], [], []

    for slug, sb in b["sectors"].items():
        sa = a["sectors"].get(slug)
        if not sa:
            continue

        for f in RESTATABLE:
            va, vb = sa.get(f), sb.get(f)
            if isinstance(va, int) and isinstance(vb, int) and va != vb:
                pct = 100.0 * (vb - va) / va if va else 0
                if abs(pct) >= threshold:
                    restated.append((slug, f, va, vb, round(pct, 2)))

        da, db = direction(sa.get("rolling_change_pct")), direction(sb.get("rolling_change_pct"))
        if da != db:
            flipped.append((slug, da, db,
                            sa.get("rolling_change_pct"), sb.get("rolling_change_pct")))

        if sa.get("volume_confidence") != sb.get("volume_confidence"):
            banded.append((slug, sa.get("volume_confidence"), sb.get("volume_confidence")))

        aa, ab = sa.get("annual") or {}, sb.get("annual") or {}
        for yr in sorted(set(aa) & set(ab)):
            if aa[yr] != ab[yr] and isinstance(aa[yr], int) and isinstance(ab[yr], int):
                annual_changed.append((slug, yr, aa[yr], ab[yr]))

    return {"restated": restated, "flipped": flipped,
            "banded": banded, "annual_changed": annual_changed}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--from", dest="frm", required=True)
    ap.add_argument("--to", dest="to", required=True)
    ap.add_argument("--threshold", type=float, default=0.5,
                    help="ignore restatements smaller than this percent (default 0.5)")
    args = ap.parse_args()

    a, b = load(args.frm), load(args.to)
    print("comparing %s (vintage %s) with %s (vintage %s)"
          % (args.frm, a["meta"]["vintage_hash"], args.to, b["meta"]["vintage_hash"]))
    print()

    r = compare(a, b, args.threshold)

    print("=== figures the source restated (>= %.1f%%) ===" % args.threshold)
    for slug, f, va, vb, pct in r["restated"] or []:
        print("  %-48s %-12s %s -> %s (%+.2f%%)" % (slug[:48], f, va, vb, pct))
    if not r["restated"]:
        print("  none")

    print()
    print("=== annual history changed ===")
    for slug, yr, va, vb in r["annual_changed"] or []:
        print("  %-48s %s: %s -> %s" % (slug[:48], yr, va, vb))
    if not r["annual_changed"]:
        print("  none")

    print()
    print("=== direction changed ===")
    for slug, da, db, pa, pb in r["flipped"] or []:
        print("  %-48s %s (%s%%) -> %s (%s%%)" % (slug[:48], da, pa, db, pb))
    if not r["flipped"]:
        print("  none")

    print()
    print("=== volume confidence band changed ===")
    for slug, ba, bb in r["banded"] or []:
        print("  %-48s %s -> %s" % (slug[:48], ba, bb))
    if not r["banded"]:
        print("  none")

    print()
    total = sum(len(v) for v in r.values())
    print("%d item(s) for editorial review." % total)
    print("A restatement is not news. Check it before writing about any change.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
