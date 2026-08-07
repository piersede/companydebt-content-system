"""Push the /data/ sector + trade pages to LIVE in one run, then verify each one.

WHY THIS EXISTS
---------------
These pages live in the WordPress database, not in files, so there is no
"copy the whole site" route that moves them. The WP Engine environment copy
replaces the entire live database and destroys every form entry created on
live since the previous push (~160 enquiries, 23 Mar - 28 Jul 2026). The
files-only variant moves no page content at all and deactivates Gravity Forms.

So content goes one page at a time. This wrapper just removes the tedium of
typing that out per page: same per-page safety, one command.

Each page keeps the protections of publish_to_live.py: a dry run by default,
a refusal if the new content is suspiciously shorter than what is live, and a
read-back check after writing. Any page that fails is reported and the run
continues; nothing is all-or-nothing.

AUTHORISATION
-------------
Refuses to write without --confirm, and Piers must have asked for this
specific push. Credentials existing is not permission.

USAGE
    python scripts/push_data_pages_live.py                      # dry run, all pages
    python scripts/push_data_pages_live.py --confirm            # write, all pages
    python scripts/push_data_pages_live.py --only retail --confirm
    python scripts/push_data_pages_live.py --skip construction --confirm

AFTERWARDS
    Purge Cloudflare (dashboard) and WP Rocket / WP Engine, then re-run this
    script with --verify-only to confirm what visitors actually see.
"""

from __future__ import annotations

import argparse
import io
import re
import subprocess
import sys
import time
from pathlib import Path

import requests

# UTF-8 stdout on Windows
if sys.platform == "win32":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
DRAFTS = ROOT / "drafts"
HDRS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# live id -> slug. Live ids match staging ids for this set.
PAGES = [
    (79856, "construction-insolvency-statistics"),
    (80098, "furniture-insolvency-statistics"),
    (80134, "restaurant-insolvency-statistics"),
    (80136, "road-haulage-insolvency-statistics"),
    (80137, "recruitment-agency-insolvency-statistics"),
    (80138, "temporary-staffing-agency-insolvency-statistics"),
    (80139, "motor-vehicle-repair-insolvency-statistics"),
    (80140, "cleaning-company-insolvency-statistics"),
    (80141, "hotel-insolvency-statistics"),
    (80260, "estate-agency-insolvency-statistics"),
    (80578, "it-consultancy-insolvency-statistics"),
    (80581, "management-consultancy-insolvency-statistics"),
    (80584, "architectural-engineering-insolvency-statistics"),
    (80587, "personal-care-services-insolvency-statistics"),
    (80590, "sports-facility-insolvency-statistics"),
    (80593, "medical-dental-practice-insolvency-statistics"),
    (80596, "creative-arts-entertainment-insolvency-statistics"),
    (80597, "amusement-recreation-insolvency-statistics"),
    (80601, "real-estate-letting-investment-insolvency-statistics"),
    (80604, "freight-forwarding-logistics-insolvency-statistics"),
    (80679, "retail-insolvency-statistics"),
]

MIN_BYTES = 50_000          # anything smaller than this is truncation, not a page
EXPECTED_CHART_POINTS = 126  # monthly series length; update when the series grows


def fetch(url: str, tries: int = 5):
    """GET with backoff - the live host rate-limits bursts with 429."""
    r = None
    for _ in range(tries):
        r = requests.get(url, headers=HDRS, timeout=90)
        if r.status_code != 429:
            return r
        time.sleep(10)
    return r


def check_rendered(slug: str) -> tuple[bool, str]:
    """Re-render the live page and check what a visitor actually gets."""
    r = fetch(f"https://www.companydebt.com/data/{slug}/")
    if r is None or r.status_code != 200:
        return False, f"http {r.status_code if r else 'no response'}"

    b = r.text
    problems = []

    if len(b) < MIN_BYTES:
        problems.append(f"only {len(b):,} bytes - truncated?")
    if "January 2023" in b or "since 2023" in b:
        problems.append("stale 2023 wording still present")
    if "&lt;!--" in b or "u003c" in b:
        problems.append("escaped markup - content mangled")

    m = re.search(r'id="([a-z0-9\-]*monthly)-title"', b)
    if not m:
        problems.append("monthly chart not found")
    else:
        j = b.find(m.group(1) + "-title")
        i = b.rfind("<svg", 0, j)
        seg = b[i:b.find("</svg>", i) + 6]
        pts = re.findall(r'points="([^"]+)"', seg)
        n = len(pts[0].split()) if pts else 0
        if n != EXPECTED_CHART_POINTS:
            problems.append(f"chart has {n} points, expected {EXPECTED_CHART_POINTS}")

    cf = r.headers.get("cf-cache-status")
    age = r.headers.get("age")
    if problems and cf == "HIT":
        problems.append(f"NOTE: served from Cloudflare cache (age {age}s) - purge, then re-check")

    return (not problems), (f"{len(b):,} bytes" if not problems else "; ".join(problems))


def push_one(page_id: int, slug: str, confirm: bool) -> bool:
    draft = DRAFTS / f"{page_id}_{slug}.html"
    if not draft.exists():
        print(f"  SKIP  {slug}: draft not found ({draft.name})")
        return False

    cmd = [sys.executable, str(ROOT / "scripts" / "publish_to_live.py"),
           "--id", str(page_id), "--file", str(draft)]
    if confirm:
        cmd.append("--confirm")

    res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    out = res.stdout + res.stderr

    if not confirm:
        sim = re.search(r"similarity:\s*(\d+%)", out)
        chg = re.search(r"change\s*:\s*(\d+%)", out)
        print(f"  dry   {slug}: {chg.group(1) if chg else '?'} of current size, "
              f"{sim.group(1) if sim else '?'} similar")
        return res.returncode == 0

    if "verified" in out and res.returncode == 0:
        got = re.search(r"verified\s*:\s*([\d,]+) bytes", out)
        print(f"  sent  {slug}: {got.group(1) if got else '?'} bytes written")
        return True

    reason = next((ln for ln in out.splitlines() if "REFUS" in ln or "ERROR" in ln), "")
    print(f"  FAIL  {slug}: {reason or 'push did not confirm'}")
    return False


def main() -> int:
    ap = argparse.ArgumentParser(description="Push the /data/ pages to live, one at a time.")
    ap.add_argument("--confirm", action="store_true", help="actually write (default is a dry run)")
    ap.add_argument("--only", nargs="*", help="only these slugs (substring match)")
    ap.add_argument("--skip", nargs="*", help="skip these slugs (substring match)")
    ap.add_argument("--verify-only", action="store_true",
                    help="skip pushing; just re-render every live page and report")
    ap.add_argument("--pause", type=float, default=3.0, help="seconds between pages")
    args = ap.parse_args()

    pages = PAGES
    if args.only:
        pages = [p for p in pages if any(o in p[1] for o in args.only)]
    if args.skip:
        pages = [p for p in pages if not any(s in p[1] for s in args.skip)]

    if not pages:
        print("No pages matched.")
        return 1

    if not args.verify_only:
        mode = "PUBLISHING TO LIVE" if args.confirm else "DRY RUN (nothing will be written)"
        print(f"{mode} - {len(pages)} page(s)\n")
        for pid, slug in pages:
            push_one(pid, slug, args.confirm)
            time.sleep(args.pause)

        if not args.confirm:
            print("\nDry run complete. Re-run with --confirm to publish.")
            return 0

        print("\nNow purge Cloudflare and WP Rocket / WP Engine, then re-run with "
              "--verify-only.\nUntil the caches are cleared, visitors still see the old pages.")

    print(f"\nVerifying {len(pages)} live page(s) as a visitor sees them\n")
    ok, bad = 0, []
    for _pid, slug in pages:
        passed, detail = check_rendered(slug)
        if passed:
            ok += 1
            print(f"  ok    {slug}: {detail}")
        else:
            bad.append(slug)
            print(f"  FAIL  {slug}: {detail}")
        time.sleep(args.pause)

    print(f"\nclean: {ok}/{len(pages)}")
    if bad:
        print("needs attention: " + ", ".join(bad))
        return 1

    print("\nAll pages verified. Finally, run: python scripts/check_live_form_entries.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
