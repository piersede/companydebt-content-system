"""Phase 0 Core success criterion: can the release object reproduce the live pages?

If a figure on a published page cannot be derived from the release object, the
release model is not yet the source of truth and Phase 0 is not done.

This reads the built drafts (what we publish) and checks the headline numbers
against the release object, sector by sector.

USAGE
    python scripts/intelligence/verify_against_pages.py
    python scripts/intelligence/verify_against_pages.py --month 2026-06 --verbose
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DRAFTS = ROOT / "drafts"

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def draft_for(wp_id: int, slug: str) -> Path | None:
    p = DRAFTS / ("%d_%s.html" % (wp_id, slug))
    return p if p.exists() else None


def visible_text(path: Path) -> str:
    t = path.read_text(encoding="utf-8")
    t = re.sub(r"<style.*?</style>|<script.*?</script>|<svg.*?</svg>", " ", t, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t))


def fmt(n) -> list[str]:
    """A figure can legitimately appear with or without a thousands separator."""
    if n is None:
        return []
    i = int(n)
    return list({"{:,}".format(i), str(i)})


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--month")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    period = args.month or json.loads(
        (ROOT / "data/insolvency-statistics/sector_series.json").read_text(encoding="utf-8")
    )["monthly_months"][-1]
    rel_path = ROOT / "data" / "releases" / period / "release.json"
    if not rel_path.exists():
        raise SystemExit("no release built for %s" % period)
    rel = json.loads(rel_path.read_text(encoding="utf-8"))

    print("release %s (vintage %s), %d sectors"
          % (period, rel["meta"]["vintage_hash"], rel["meta"]["sector_count"]))
    print()

    checked = reproduced = 0
    failures = []
    for slug, s in sorted(rel["sectors"].items()):
        if not s.get("wp_id"):
            continue
        p = draft_for(s["wp_id"], slug)
        if p is None:
            print("  %-52s NO DRAFT" % slug[:52])
            continue
        text = visible_text(p)

        # Pages come in two shapes. The 20 trade pages lead on year-to-date and
        # rolling 12 months. The whole-section pages (construction, the overview)
        # publish an annual series instead and never show a YTD figure, so
        # testing them for one reports a false failure.
        rolling_shape = [("ytd", s.get("ytd")), ("ytd_prior", s.get("ytd_prior")),
                         ("rolling_12m", s.get("rolling_12m"))]
        annual = s.get("annual") or {}
        annual_shape = [("annual %s" % y, v) for y, v in annual.items() if v]

        def score(tests):
            hit, miss = 0, []
            for name, val in tests:
                if val is None:
                    continue
                if any(f in text for f in fmt(val)):
                    hit += 1
                else:
                    miss.append("%s=%s" % (name, val))
            return hit, miss

        hit, miss = score(rolling_shape)
        mode = "rolling"
        if hit == 0 and annual_shape:          # not a rolling-shape page
            hit, miss = score(annual_shape)
            mode = "annual"

        total = len([t for t in (rolling_shape if mode == "rolling" else annual_shape)
                     if t[1] is not None])
        checked += total
        reproduced += hit
        status = "ok (%s, %d/%d)" % (mode, hit, total) if not miss else \
                 "MISSING [%s] %s" % (mode, ", ".join(miss))
        if miss:
            failures.append((slug, miss))
        if args.verbose or miss:
            print("  %-52s %s" % (slug[:52], status))

    print()
    print("figures checked: %d, found on the page: %d (%.1f%%)"
          % (checked, reproduced, 100.0 * reproduced / checked if checked else 0))
    if failures:
        print()
        print("Sectors whose published figures the release object does not reproduce:")
        for slug, miss in failures:
            print("  %-52s %s" % (slug[:52], ", ".join(miss)))
        return 1
    print("Every published headline figure is derivable from the release object.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
