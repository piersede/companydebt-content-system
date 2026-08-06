#!/usr/bin/env python
"""Check that the CTA blocks actually on staging match the reviewed decisions.

A 200 proves nothing here: the placement filter can be skipped by a page template, the
stylesheet can fail to load, and the response still looks fine. So this fetches each
reviewed page, pulls out every ``data-cd-cta`` attribute and compares the set against
what the placement rules in ``mu-plugins/cd-cta-insolvency-test.php`` should produce for
that page's row in ``docs/cta-review-list-completed.csv``.

The expectation mirrors the placement filter, not just the review's Alternative-CTA
column. On a non-urgent page that column records a fallback; the test block is what
renders.

    python scripts/verify_cta_placement.py            # pages carrying an alternative CTA
    python scripts/verify_cta_placement.py --all      # the whole reviewed corpus

Exits non-zero if any page disagrees with its review.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import csv
import os
import pathlib
import re
import sys

import requests
from dotenv import load_dotenv

ROOT = pathlib.Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
CSV = ROOT / "docs" / "cta-review-list-completed.csv"

# Review label -> the data-cd-cta value the block emits. Must stay in step with the
# switch in cd_cta_alternative_block().
BLOCK = {
    "direct advice": "direct-advice",
    "solvent closure": "solvent-closure",
    "company assets": "assets",
    "process guidance": "process-guidance",
    "failed cva": "cva-failed",
    "personal-liability guidance": "personal-liability",
    "partnership advice": "partnership",
    "charity advice": "charity",
    "group company advice": "group-company",
    "creditor guidance": "creditor",
    "hmrc affordability": "hmrc-affordability",
    "closure options": "closure-options",
}

# A block suppresses itself rather than link to the page it sits on. The MVL page swaps
# in its own wording instead of dropping the block.
SUPPRESSED = {
    "/insolvency/insolvent-company-owes-me-money/": "creditor",
    "/closing-a-limited-company/": "closure-options",
    "/insolvency-calculator/": "insolvency-test",
}
SWAPPED = {"/liquidation/members-voluntary-liquidation/": ("solvent-closure", "mvl-advice")}


def expected(row: dict) -> set[str]:
    """The blocks the placement filter should put on this page."""
    variant = (row["Variant"] or "").strip().lower()
    urgency = (row["Urgency modifier"] or "").strip().lower()
    size = (row["Block size"] or "").strip().lower()
    alt = (row["Alternative primary CTA"] or "").strip().lower()

    want: set[str] = set()
    if variant == "none":
        if alt in BLOCK:
            want.add(BLOCK[alt])
    elif urgency == "urgent_action":
        want.add(BLOCK.get(alt, "direct-advice"))
        want.add("insolvency-test")
    elif size == "compact":
        want.add("insolvency-test")
        # Only a reviewed alternative that is NOT the corpus-wide 'direct advice'
        # fallback leads on a non-urgent page. See the placement filter.
        if alt in BLOCK and alt != "direct advice":
            want.add(BLOCK[alt])
    else:
        want.add("insolvency-test")

    page = row["Page"]
    want.discard(SUPPRESSED.get(page, ""))
    if page in SWAPPED:
        was, now = SWAPPED[page]
        if was in want:
            want.discard(was)
            want.add(now)
    return want


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="check every reviewed page")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    base = os.environ["WP_STAGING_URL"].rstrip("/")
    s = requests.Session()
    s.auth = (os.environ["WP_BASIC_AUTH_USER"], os.environ["WP_BASIC_AUTH_PASS"])
    s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) cd-cta-verify"

    rows = list(csv.DictReader(CSV.open(encoding="utf-8-sig")))
    if not args.all:
        rows = [r for r in rows if (r["Alternative primary CTA"] or "").strip().lower() in BLOCK]

    def fetch(r):
        try:
            return r, s.get(base + r["Page"], timeout=60), None
        except Exception as exc:  # noqa: BLE001
            return r, None, f"fetch failed: {exc}"

    bad, ok = [], 0
    with cf.ThreadPoolExecutor(max_workers=args.workers) as pool:
        for r, resp, err in pool.map(fetch, rows):
            page = r["Page"]
            if err:
                bad.append((page, err))
            elif resp.status_code != 200:
                bad.append((page, f"http {resp.status_code}"))
            elif "There has been a critical error" in resp.text or "Fatal error" in resp.text:
                bad.append((page, "PHP fatal error on page"))
            else:
                found = set(re.findall(r'data-cd-cta="([^"]+)"', resp.text))
                want = expected(r)
                if found == want:
                    ok += 1
                else:
                    bad.append(
                        (page, f"want {sorted(want) or 'nothing'}, got {sorted(found) or 'nothing'}")
                    )

    print(f"{len(rows)} pages checked")
    print(f"  {ok} match the review")
    if bad:
        print(f"  {len(bad)} do NOT match:")
        for page, why in bad:
            print(f"      {page}\n          {why}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
