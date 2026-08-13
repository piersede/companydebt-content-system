#!/usr/bin/env python
"""Build the CTA placement review list for EVERY page on the site.

    python scripts/build_cta_review_list.py

Reads the site's own sitemap (staging) rather than an older roll-out list, so nothing is
silently left out. The first version of this script inherited a previous list that had
already dropped 77 pages and never contained the blog at all — 109 pages were never put
in front of a reviewer, and "no CTA here" was an invisible assumption instead of a
recorded decision.

Decisions already made are carried over verbatim from
docs/cta-review-list-completed.csv. Pages that page-type rules settle (blog, category,
about, legal, navigation, hub, the test's own page) are filled in as "no CTA". Anything
left is filled in with a proposal and listed at the end for a human to confirm.

Output: docs/cta-review-list.csv
"""
from __future__ import annotations

import csv
import os
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
COMPLETED = ROOT / "docs" / "cta-review-list-completed.csv"
OUT = ROOT / "docs" / "cta-review-list.csv"
BASE = "https://comdebstage.wpengine.com"

COLUMNS = [
    "Page", "Primary audience", "Assumed state", "Formal action", "Personal-risk context",
    "Test fit", "Variant", "Urgency modifier", "Block size", "Alternative primary CTA",
    "Confidence", "Reviewed", "Notes",
]

# Piers, 2026-08-06: about pages, navigation pages, hub pages, terms-and-conditions type
# pages and blog pages get no CTA. Everything else gets one.
NO_CTA_EXACT = {
    "/",                                 # homepage — navigation
    "/about-us/",
    "/meet-the-team/",
    "/contact-us/",
    "/cookie-policy/",
    "/privacy-policy/",
    "/terms-conditions/",
    "/site-map/",
    "/testimonials/",
    "/insolvency-news-commentary/",      # news/blog
    "/insolvency-calculator/",           # the test itself
    "/data/",                            # index of the statistics pages
    "/sample-letters/",                  # index of the letter templates
    "/sector-specific-insolvency/",      # index of the sector pages
}
NO_CTA_KINDS = {"post", "category", "testimonial"}

# Decisions Piers has made explicitly. These override anything already in the completed
# review, because the review was filled in before he saw these groups.
PIERS_NO_CTA = (
    ("/data/",           "insolvency figures and statistics (Piers, 2026-08-06)"),
    ("/sample-letters/", "letter templates (Piers, 2026-08-06)"),
)
PIERS_NO_CTA_EXACT = {
    "/debt-charities-uk/":                "debt charities support page (Piers, 2026-08-06)",
    "/mental-health-debt-stress-support/": "mental-health support page (Piers, 2026-08-06)",
}


def piers_no_cta(path: str) -> str | None:
    if path in PIERS_NO_CTA_EXACT:
        return PIERS_NO_CTA_EXACT[path]
    for prefix, reason in PIERS_NO_CTA:
        if path.startswith(prefix):
            return reason
    return None


def no_cta_row(path: str, reason: str, stamp: str) -> dict:
    return {
        "Page": path,
        "Primary audience": "Mixed", "Assumed state": "Uncertain", "Formal action": "None",
        "Personal-risk context": "No", "Test fit": "None", "Variant": "none",
        "Urgency modifier": "none", "Block size": "None",
        "Alternative primary CTA": "None", "Confidence": "High",
        "Reviewed": stamp, "Notes": f"no CTA: {reason}",
    }


def reason_no_cta(path: str, kind: str) -> str | None:
    if kind == "post":
        return "blog article"
    if kind == "category":
        return "category listing — navigation"
    if kind == "testimonial":
        return "testimonial page"
    if path in NO_CTA_EXACT:
        return "about / navigation / legal / index page"
    if path.rstrip("/").endswith("-hub"):
        return "hub page — navigation"
    # Piers, 2026-08-06: the insolvency figures and statistics pages get no CTA at all.
    if path.startswith("/data/"):
        return "insolvency figures and statistics"
    return None


def proposal(path: str) -> tuple[dict, str]:
    """A filled-in row plus the reason, for pages the page-type rules do not settle.

    These are proposals. Each one is printed at the end so a human can overturn it.
    """
    row = {c: "" for c in COLUMNS}

    if path == "/close-my-company/":
        row.update({
            "Primary audience": "Director", "Assumed state": "Uncertain", "Formal action": "None",
            "Personal-risk context": "No", "Test fit": "Primary", "Variant": "early_check",
            "Urgency modifier": "none", "Block size": "Large",
            "Alternative primary CTA": "None", "Confidence": "Medium",
        })
        return row, "covers both solvent and insolvent closure, so the softer wording is the safe one"

    if path == "/insolvency-practitioner/":
        row.update({
            "Primary audience": "Director", "Assumed state": "Serious distress", "Formal action": "None",
            "Personal-risk context": "No", "Test fit": "Primary", "Variant": "serious_position",
            "Urgency modifier": "none", "Block size": "Large",
            "Alternative primary CTA": "None", "Confidence": "Medium",
        })
        return row, "someone looking for an insolvency practitioner is usually past wondering whether there is a problem"

    row.update({
        "Primary audience": "Director", "Assumed state": "Uncertain", "Formal action": "None",
        "Personal-risk context": "No", "Test fit": "Primary", "Variant": "early_check",
        "Urgency modifier": "none", "Block size": "Large",
        "Alternative primary CTA": "None", "Confidence": "Low",
    })
    return row, "no rule covers this page — the safe default, needs a read"


def fetch_sitemap() -> dict[str, str]:
    import sys as _sys, pathlib as _pl
    _sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
    from _env import load_env as _load_env
    _load_env()
    auth = (os.environ["WP_BASIC_AUTH_USER"], os.environ["WP_BASIC_AUTH_PASS"])
    ua = {"User-Agent": "Mozilla/5.0 CD-check"}
    pages: dict[str, str] = {}
    index = requests.get(f"{BASE}/sitemap_index.xml", auth=auth, timeout=60, headers=ua).text
    for loc in re.findall(r"<loc>([^<]+)</loc>", index):
        if "sitemap" not in loc:
            continue
        kind = loc.rsplit("/", 1)[-1].replace("-sitemap.xml", "")
        body = requests.get(loc, auth=auth, timeout=60, headers=ua).text
        for url in re.findall(r"<loc>([^<]+)</loc>", body):
            pages[urlparse(url).path] = kind
    return pages


def main() -> None:
    live = fetch_sitemap()
    done = {}
    if COMPLETED.exists():
        done = {r["Page"]: r for r in csv.DictReader(COMPLETED.open(encoding="utf-8-sig"))}

    rows, proposals, carried, ruled, overridden = [], [], 0, 0, 0
    for path in sorted(live):
        forced = piers_no_cta(path) or reason_no_cta(path, live[path])
        if forced:
            rows.append(no_cta_row(path, forced, "decision 2026-08-06"))
            overridden += 1
            continue
        if path in done:
            rows.append({c: done[path].get(c, "") for c in COLUMNS})
            carried += 1
            continue

        row = {c: "" for c in COLUMNS}
        row["Page"] = path
        if False:
            pass
        else:
            proposed, why = proposal(path)
            proposed["Page"] = path
            proposed["Reviewed"] = "proposed"
            proposed["Notes"] = f"proposal: {why}"
            row = proposed
            proposals.append((path, row["Variant"], row["Block size"], why))
        rows.append(row)

    stale = sorted(set(done) - set(live))

    with OUT.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"{len(rows)} pages -> {OUT.relative_to(ROOT)}")
    print(f"  carried over from the completed review: {carried}")
    print(f"  no CTA by explicit decision:             {overridden}")
    print(f"  settled by the no-CTA rule:             {ruled}")
    print(f"  proposed, needs confirming:             {len(proposals)}")
    print("  variants:", dict(Counter(r["Variant"] for r in rows)))
    if stale:
        print(f"\nin the old review but no longer on the site ({len(stale)}), dropped:")
        for p in stale:
            print("   ", p)
    if proposals:
        print("\nproposals to confirm or overturn:")
        groups: dict[str, list[str]] = {}
        for path, variant, size, why in proposals:
            groups.setdefault(f"{variant} / {size or 'no block'} — {why}", []).append(path)
        for why, paths in sorted(groups.items(), key=lambda kv: -len(kv[1])):
            print(f"\n  [{len(paths)}] {why}")
            for p in paths[:4]:
                print("       ", p)
            if len(paths) > 4:
                print(f"        ... and {len(paths) - 4} more")


if __name__ == "__main__":
    main()
