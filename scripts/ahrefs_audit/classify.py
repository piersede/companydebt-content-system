"""Classify every issue in the export into: FALSE POSITIVE / BY DESIGN / REAL.

The point of this file is to stop the next person re-litigating the same
triage. Anything marked FALSE_POSITIVE has been verified as such (see
verify_external.py) and must NOT be 'fixed' by editing the site.
"""
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).parent))
from parse_export import read_export, issue_name, severity

# Hosts proven to serve 404 to bot user-agents but 200 to browsers.
# Verified 2026-07-16 via verify_external.py. Do not "fix" links to these.
BOT_BLOCKING_HOSTS = {"www.legislation.gov.uk", "legislation.gov.uk"}

FALSE_POSITIVE = "FALSE POSITIVE - do not touch site"
BY_DESIGN = "BY DESIGN - intentional, no action"
REAL = "REAL - actionable"
INFO = "INFORMATIONAL - not an issue"


def classify(export_dir: Path):
    D = export_dir
    out = []

    # --- Broken external links: split blocked-host noise from genuine 404s ---
    rows = read_export(D / "Error-indexable-Page_has_links_to_broken_page-links.csv")
    blocked = [r for r in rows if urlsplit(r["Target URL"]).netloc in BOT_BLOCKING_HOSTS]
    genuine = [r for r in rows if urlsplit(r["Target URL"]).netloc not in BOT_BLOCKING_HOSTS]
    out.append(("Links to broken page (legislation.gov.uk)", len(blocked), FALSE_POSITIVE,
                "Verified 200 to browser UA, 404 to bot UA. Exclude host in Ahrefs settings."))
    out.append(("Links to broken page (other hosts)", len(genuine), REAL,
                "Needs per-URL verification with a browser UA before any edit."))

    ext = read_export(D / "Notice-External_4XX.csv")
    eb = [r for r in ext if urlsplit(r["URL"]).netloc in BOT_BLOCKING_HOSTS]
    eg = [r for r in ext if urlsplit(r["URL"]).netloc not in BOT_BLOCKING_HOSTS]
    out.append(("External 4XX (legislation.gov.uk)", len(eb), FALSE_POSITIVE, "Same block."))
    out.append(("External 4XX (other hosts)", len(eg), REAL, "Verify each with browser UA."))

    return out, genuine, eg


if __name__ == "__main__":
    D = Path(sys.argv[1])
    out, genuine, eg = classify(D)
    print(f"{'ISSUE':<48}{'N':>6}  VERDICT")
    print("-" * 100)
    for name, n, verdict, note in out:
        print(f"{name:<48}{n:>6}  {verdict}\n{'':<54}{note}")

    print("\n\n=== Genuinely broken NON-blocked external targets (need checking) ===")
    for url, n in Counter(r["Target URL"] for r in genuine).most_common():
        print(f"{n:>4}  {url}")

    print("\n=== Non-blocked external 4XX pages (need checking) ===")
    for r in eg:
        print(f"  {r['URL'][:110]}  (inlinks: {r.get('No. of all inlinks')})")
