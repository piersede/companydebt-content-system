"""Report which pages genuinely differ between staging and live.

WHY THIS EXISTS
---------------
"Put the whole staging site live" is not available: the WP Engine environment
copy replaces the entire live database and destroys form entries, and the
files-only copy moves no page content at all. Content goes page by page.

That is only sane if you know which pages actually changed. This builds that
list. Read-only against both sites; it writes nothing anywhere.

Both sides are read over the REST API by page id, which is gentler than the
front end (the live front end rate-limits bursts within seconds).

USAGE
    python scripts/diff_staging_live.py --sample 10     # quick sanity check
    python scripts/diff_staging_live.py                 # all pages
    python scripts/diff_staging_live.py --out diff.json
"""

from __future__ import annotations

import argparse
import difflib
import io
import json
import os
import sys
import time
from pathlib import Path

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
STAGING = (os.getenv("WP_STAGING_URL") or "").rstrip("/")

LIVE_AUTH = (os.getenv("WP_LIVE_USERNAME"), os.getenv("WP_LIVE_APP_PASSWORD"))
STAGING_AUTH = (os.getenv("WP_STAGING_USERNAME"), os.getenv("WP_STAGING_APP_PASSWORD"))
BASIC = (os.getenv("WP_BASIC_AUTH_USER"), os.getenv("WP_BASIC_AUTH_PASS"))

HDRS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def rest_get(base, ptype, pid, auth, basic=None, tries=4):
    url = f"{base}/wp-json/wp/v2/{ptype}/{pid}?context=edit"
    for _ in range(tries):
        try:
            r = requests.get(url, auth=auth, headers=HDRS, timeout=60)
        except Exception:
            time.sleep(5)
            continue
        if r.status_code == 429:
            time.sleep(12)
            continue
        return r
    return None


def content_of(resp):
    if resp is None or resp.status_code != 200:
        return None, None
    try:
        d = resp.json()
    except Exception:
        return None, None
    return (d.get("content") or {}).get("raw", ""), d.get("slug")


def main() -> int:
    ap = argparse.ArgumentParser(description="List pages whose content differs between staging and live.")
    ap.add_argument("--sample", type=int, help="only check the first N pages")
    ap.add_argument("--pause", type=float, default=1.5, help="seconds between pages")
    ap.add_argument("--out", default="staging_live_diff.json")
    args = ap.parse_args()

    cache = json.loads(CACHE.read_text(encoding="utf-8"))
    items = list(cache.items())
    if args.sample:
        items = items[:args.sample]

    print(f"Comparing {len(items)} page(s): staging vs live (read-only)\n")

    differs, same, problems = [], 0, []

    for path, meta in items:
        pid = meta.get("id")
        ptype = meta.get("endpoint") or ("posts" if meta.get("type") == "post" else "pages")

        s_resp = rest_get(STAGING, ptype, pid, STAGING_AUTH)
        s_html, s_slug = content_of(s_resp)
        l_resp = rest_get(LIVE, ptype, pid, LIVE_AUTH)
        l_html, l_slug = content_of(l_resp)

        if s_html is None or l_html is None:
            why = []
            if s_html is None:
                why.append(f"staging {s_resp.status_code if s_resp else 'no response'}")
            if l_html is None:
                why.append(f"live {l_resp.status_code if l_resp else 'no response'}")
            problems.append((path, "; ".join(why)))
            print(f"  ??    {path}  ({'; '.join(why)})")
        elif s_slug and l_slug and s_slug != l_slug:
            # id means a different page on each site - do not trust the comparison
            problems.append((path, f"id {pid} is '{s_slug}' on staging but '{l_slug}' on live"))
            print(f"  MISMATCH {path}  id points at different pages")
        elif s_html.strip() == l_html.strip():
            same += 1
        else:
            ratio = difflib.SequenceMatcher(None, s_html, l_html).quick_ratio()
            differs.append({
                "path": path, "id": pid, "type": ptype, "slug": s_slug,
                "staging_bytes": len(s_html), "live_bytes": len(l_html),
                "similarity": round(ratio, 3),
            })
            print(f"  DIFF  {path}  staging {len(s_html):,}b vs live {len(l_html):,}b  "
                  f"({ratio:.0%} similar)")

        time.sleep(args.pause)

    out = ROOT / args.out
    out.write_text(json.dumps(
        {"differs": differs, "identical": same, "problems": problems}, indent=2), encoding="utf-8")

    print(f"\ndiffer: {len(differs)}   identical: {same}   could not compare: {len(problems)}")
    print(f"written to {out.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
