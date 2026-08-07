"""Copy every page's CONTENT from staging to live, one page at a time.

WHAT THIS IS
------------
The safe equivalent of "put the whole staging site live".

WP Engine's environment copy offers two options and neither does the job:
  - copy the database  -> page content moves, but the LIVE database is
                          replaced, destroying every Gravity Forms entry,
                          user and comment created on live since the last
                          push (~160 enquiries, 23 Mar - 28 Jul 2026)
  - files only         -> the database is untouched, so form entries are
                          safe, but NO page content moves at all, and
                          Gravity Forms gets deactivated (versioned folder)

Page content and form entries live in the same database, so there is no
setting that moves one and spares the other.

This script writes only the post_content of each page. Form entries, users,
comments, options and every other table are never touched. Same end state as
a database copy as far as content goes, without the data loss.

Each page is independent: a failure stops that page, not the run, and every
page's previous version stays in its WordPress revision history.

AUTHORISATION
-------------
Dry run by default. Refuses to write without --confirm, and Piers must have
asked for this specific push.

USAGE
    python scripts/push_site_content_live.py                   # dry run, report only
    python scripts/push_site_content_live.py --changed-only    # dry run, changed pages
    python scripts/push_site_content_live.py --changed-only --confirm
    python scripts/push_site_content_live.py --path /liquidation/ --confirm

AFTERWARDS
    Purge Cloudflare and WP Rocket / WP Engine, then:
        python scripts/check_live_form_entries.py
"""

from __future__ import annotations

import argparse
import base64
import difflib
import io
import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import quote

import requests
from dotenv import load_dotenv

if sys.platform == "win32":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)
    except Exception:
        pass

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "content_cache.json"
LIVE = "https://www.companydebt.com"

HDRS = {"User-Agent": "Company Debt-Publisher/1.0"}

# Refuse to shrink a live page below this fraction of its current size. The
# classic failure is a truncated push landing with a 200 OK.
SHRINK_FLOOR = 0.60


def staging_base() -> str:
    """Staging sits behind nginx basic auth AND WP auth, and both use the
    Authorization header - so the nginx pair goes in the URL, as wp_publish does."""
    url = (os.getenv("WP_STAGING_URL") or "").rstrip("/")
    u = os.getenv("WP_BASIC_AUTH_USER") or ""
    p = os.getenv("WP_BASIC_AUTH_PASS") or ""
    if u and "://" in url:
        scheme, rest = url.split("://", 1)
        return f"{scheme}://{quote(u, safe='')}:{quote(p, safe='')}@{rest}"
    return url


def wp_header(user: str, pw: str) -> dict:
    token = base64.b64encode(f"{user}:{pw}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


STAGING = staging_base()
S_HDRS = {**HDRS, **wp_header(os.getenv("WP_STAGING_USERNAME") or "",
                              os.getenv("WP_STAGING_APP_PASSWORD") or "")}
L_HDRS = {**HDRS, **wp_header(os.getenv("WP_LIVE_USERNAME") or "",
                              os.getenv("WP_LIVE_APP_PASSWORD") or "")}


def req(method, url, headers, tries=4, **kw):
    for _ in range(tries):
        try:
            r = requests.request(method, url, headers=headers, timeout=90, **kw)
        except Exception:
            time.sleep(5)
            continue
        if r.status_code == 429:
            time.sleep(12)
            continue
        return r
    return None


def get_content(base, ptype, pid, headers):
    r = req("GET", f"{base}/wp-json/wp/v2/{ptype}/{pid}?context=edit", headers)
    if r is None or r.status_code != 200:
        return None, None, (r.status_code if r is not None else "no response")
    try:
        d = r.json()
    except Exception:
        return None, None, "bad json"
    return (d.get("content") or {}).get("raw", ""), d.get("slug"), None


def main() -> int:
    ap = argparse.ArgumentParser(description="Push staging page content to live, page by page.")
    ap.add_argument("--confirm", action="store_true", help="actually write (default: dry run)")
    ap.add_argument("--changed-only", action="store_true",
                    help="skip pages whose content already matches live")
    ap.add_argument("--path", nargs="*", help="only paths containing these strings")
    ap.add_argument("--limit", type=int, help="stop after N pages (for testing)")
    ap.add_argument("--pause", type=float, default=1.5)
    ap.add_argument("--report", default="site_push_report.json")
    args = ap.parse_args()

    cache = json.loads(CACHE.read_text(encoding="utf-8"))
    items = list(cache.items())
    if args.path:
        items = [i for i in items if any(p in i[0] for p in args.path)]
    if args.limit:
        items = items[:args.limit]

    mode = "PUBLISHING TO LIVE" if args.confirm else "DRY RUN - nothing will be written"
    print(f"{mode}")
    print(f"{len(items)} page(s). Content only - form entries, users and comments are untouched.\n")

    pushed, identical, skipped, failed = [], 0, [], []

    for path, meta in items:
        pid = meta.get("id")
        ptype = meta.get("endpoint") or ("posts" if meta.get("type") == "post" else "pages")

        s_html, s_slug, s_err = get_content(STAGING, ptype, pid, S_HDRS)
        l_html, l_slug, l_err = get_content(LIVE, ptype, pid, L_HDRS)

        if s_err or l_err:
            failed.append((path, f"staging={s_err or 'ok'} live={l_err or 'ok'}"))
            print(f"  ??    {path}  (staging={s_err or 'ok'} live={l_err or 'ok'})")
            time.sleep(args.pause)
            continue

        if s_slug and l_slug and s_slug != l_slug:
            skipped.append((path, f"id {pid} is '{s_slug}' on staging, '{l_slug}' on live"))
            print(f"  SKIP  {path}  id points at a different page on each site")
            time.sleep(args.pause)
            continue

        if s_html.strip() == l_html.strip():
            identical += 1
            if not args.changed_only:
                print(f"  same  {path}")
            time.sleep(args.pause)
            continue

        if l_html and len(s_html) < len(l_html) * SHRINK_FLOOR:
            skipped.append((path, f"staging {len(s_html):,}b is under {SHRINK_FLOOR:.0%} of live "
                                  f"{len(l_html):,}b - looks truncated"))
            print(f"  SKIP  {path}  staging copy is much smaller than live - not pushing")
            time.sleep(args.pause)
            continue

        sim = difflib.SequenceMatcher(None, s_html, l_html).quick_ratio()

        if not args.confirm:
            print(f"  would {path}  live {len(l_html):,}b -> staging {len(s_html):,}b ({sim:.0%} similar)")
            pushed.append({"path": path, "id": pid, "similarity": round(sim, 3)})
            time.sleep(args.pause)
            continue

        r = req("POST", f"{LIVE}/wp-json/wp/v2/{ptype}/{pid}", L_HDRS,
                json={"content": s_html})
        if r is None or r.status_code not in (200, 201):
            failed.append((path, f"write returned {r.status_code if r else 'no response'}"))
            print(f"  FAIL  {path}  write returned {r.status_code if r else 'no response'}")
            time.sleep(args.pause)
            continue

        back, _, _ = get_content(LIVE, ptype, pid, L_HDRS)
        if back is None or len(back) < len(s_html) * 0.9:
            failed.append((path, "read-back shorter than what was sent"))
            print(f"  FAIL  {path}  read-back shorter than sent - check this page")
        else:
            pushed.append({"path": path, "id": pid, "bytes": len(back)})
            print(f"  sent  {path}  {len(back):,}b verified")

        time.sleep(args.pause)

    report = {"pushed": pushed, "identical": identical,
              "skipped": skipped, "failed": failed, "confirmed": args.confirm}
    (ROOT / args.report).write_text(json.dumps(report, indent=2), encoding="utf-8")

    verb = "pushed" if args.confirm else "would push"
    print(f"\n{verb}: {len(pushed)}   already identical: {identical}   "
          f"skipped: {len(skipped)}   failed: {len(failed)}")
    for p, why in skipped:
        print(f"  skipped {p}: {why}")
    for p, why in failed:
        print(f"  failed  {p}: {why}")
    print(f"\nreport written to {args.report}")

    if args.confirm and pushed:
        print("\nNow purge Cloudflare and WP Rocket / WP Engine, then run:")
        print("  python scripts/check_live_form_entries.py")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
