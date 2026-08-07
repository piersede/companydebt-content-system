"""Find live pages whose stored content points at the staging site.

WHY THIS EXISTS
---------------
Live content should never reference comdebstage.*. When it does, visitors get
broken images: the staging host sits behind HTTP basic auth and returns 401.
The live homepage hero image is served this way today.

This is the signature of a staging->live content copy made without rewriting
the domain - the exact trap that push_site_content_live.py now guards against.

Read-only by default. With --fix it rewrites the staging host back to the live
host in the stored content, one page at a time, and reads each write back.

USAGE
    python scripts/find_staging_urls_on_live.py
    python scripts/find_staging_urls_on_live.py --fix --confirm
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import os
import re
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
LIVE_HOST = "www.companydebt.com"

STAGING_RE = re.compile(r"https?://comdebstage\.[a-z0-9.\-]+")


def headers() -> dict:
    tok = base64.b64encode(
        f"{os.getenv('WP_LIVE_USERNAME')}:{os.getenv('WP_LIVE_APP_PASSWORD')}".encode()).decode()
    return {"User-Agent": "Company Debt-Publisher/1.0", "Authorization": f"Basic {tok}"}


def main() -> int:
    ap = argparse.ArgumentParser(description="Find (and optionally fix) staging URLs in live content.")
    ap.add_argument("--fix", action="store_true", help="rewrite them back to the live host")
    ap.add_argument("--confirm", action="store_true", help="required alongside --fix to write")
    ap.add_argument("--pause", type=float, default=1.0)
    args = ap.parse_args()

    cache = json.loads(CACHE.read_text(encoding="utf-8"))
    H = headers()
    hits, fixed, failed = [], [], []

    for path, meta in cache.items():
        pid = meta.get("id")
        ptype = meta.get("endpoint") or ("posts" if meta.get("type") == "post" else "pages")

        r = requests.get(f"{LIVE}/wp-json/wp/v2/{ptype}/{pid}?context=edit", headers=H, timeout=90)
        if r.status_code == 429:
            time.sleep(12)
            r = requests.get(f"{LIVE}/wp-json/wp/v2/{ptype}/{pid}?context=edit", headers=H, timeout=90)
        if r.status_code != 200:
            failed.append((path, f"read {r.status_code}"))
            time.sleep(args.pause)
            continue

        html = (r.json().get("content") or {}).get("raw", "")
        found = STAGING_RE.findall(html)
        if not found:
            time.sleep(args.pause)
            continue

        hits.append({"path": path, "id": pid, "count": len(found),
                     "hosts": sorted(set(found))})
        print(f"  {len(found):>3} refs  {path}")

        if args.fix and args.confirm:
            new = STAGING_RE.sub(f"https://{LIVE_HOST}", html)
            w = requests.post(f"{LIVE}/wp-json/wp/v2/{ptype}/{pid}", headers=H,
                              json={"content": new}, timeout=90)
            if w.status_code in (200, 201):
                back = (w.json().get("content") or {}).get("raw", "")
                if STAGING_RE.search(back):
                    failed.append((path, "staging refs still present after write"))
                    print("        FAILED - refs still present after write")
                else:
                    fixed.append(path)
                    print(f"        fixed ({len(found)} refs)")
            else:
                failed.append((path, f"write {w.status_code}"))
                print(f"        FAILED - write {w.status_code}")

        time.sleep(args.pause)

    (ROOT / "live_staging_urls.json").write_text(
        json.dumps({"hits": hits, "fixed": fixed, "failed": failed}, indent=2), encoding="utf-8")

    total = sum(h["count"] for h in hits)
    print(f"\npages affected: {len(hits)}   total references: {total}")
    if args.fix and args.confirm:
        print(f"fixed: {len(fixed)}   failed: {len(failed)}")
        print("\nNow purge the live caches.")
    elif hits:
        print("\nRead-only. Re-run with --fix --confirm to rewrite them.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
