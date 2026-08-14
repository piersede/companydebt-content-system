"""Shorten the 8 over-long meta descriptions on /data/ pages.

Ahrefs flags anything over ~160; Google truncates around 155-160. Each
rewrite keeps the same promise as the original (what data, what period,
what source) inside the budget rather than just truncating.

This module is DATA ONLY and must stay side-effect free on import; push_meta_desc.py
imports FIXES/LIMIT from it and does the writing. Run it directly to check lengths.
"""
LIMIT = 155

FIXES = {
    "uk-insolvency-statistics":
        "UK company insolvency statistics, updated monthly from Insolvency Service "
        "data: headline count, procedure mix, sector breakdown and trends since 2000.",
    "company-insolvencies-by-sector":
        "UK company insolvencies by sector: which industries have the most, annual "
        "trends since 2016 and the latest 12-month breakdown across all SIC sections.",
    "cvl-statistics":
        "UK creditors' voluntary liquidation (CVL) statistics: monthly volumes since "
        "2000, share of all company insolvencies and the rate per 10,000 companies.",
    "administration-statistics":
        "UK company administration statistics: monthly volumes since 2000, share of "
        "all company insolvencies and the rate per 10,000 companies.",
    "winding-up-petition-tracker":
        "Monthly UK winding-up petition statistics from The Gazette: petitions "
        "advertised, orders made and the trend. A data source, not legal advice.",
    "dissolutions-vs-insolvencies":
        "UK company dissolutions set against formal insolvencies: how many companies "
        "are dissolved each month, incorporations, and why most closures are solvent.",
    "compulsory-liquidation-statistics":
        "UK compulsory liquidation statistics: monthly court-ordered winding-up "
        "volumes since 2000, share of all insolvencies and the rate per 10,000.",
    "construction-insolvency-statistics":
        "UK construction insolvency statistics: insolvencies in construction since "
        "2016, the trend, sub-sector breakdown and construction's share of the total.",
}

def report() -> int:
    """Print lengths. Returns the count over LIMIT."""
    print(f"{'len':>4}  {'ok':<4} slug")
    bad = 0
    for slug, desc in FIXES.items():
        ok = len(desc) <= LIMIT
        if not ok:
            bad += 1
        print(f"{len(desc):>4}  {'OK' if ok else 'LONG':<4} {slug}")
        if not ok:
            print(f"       {desc}")
    print(f"\n{len(FIXES) - bad}/{len(FIXES)} within {LIMIT} chars.")
    return bad


# NOTE: this module is imported by push_meta_desc.py purely for FIXES/LIMIT.
# Everything above must stay side-effect free - no printing, no sys.argv reads,
# no sys.exit at import time. An earlier version did all three, which meant
# importing it exited the caller, and `push_meta_desc.py --apply` would have
# been seen as `--apply` by THIS module and fired a content push.
if __name__ == "__main__":
    raise SystemExit(1 if report() else 0)
