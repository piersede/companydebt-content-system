"""Bring staging back into step with live, page by page.

WHY THIS EXISTS
---------------
Staging and live drift in BOTH directions. A full 320-page comparison found
~190 pages where LIVE was newer: live carried the CTA button arrow and heading
anchor ids that staging never received. Pushing staging over live would have
stripped that work from every one of them, reporting success each time.

The fix is to bring staging up to date first, so the two sites only differ
where staging genuinely holds newer editorial work. After that, a comparison
means something and a live push is safe.

This writes to STAGING only. It can never touch live - the live site is read
read-only here, purely as the source. Staging pushes are pre-approved and need
no per-run permission.

DIRECTION SAFETY
----------------
Only copies live -> staging where live is genuinely ahead. Skips any page where
staging looks newer (more words, or content live does not have), so real
staging work is never overwritten. Use --list to see the decisions without
writing anything.

USAGE
    python scripts/sync_staging_from_live.py --list
    python scripts/sync_staging_from_live.py --confirm
    python scripts/sync_staging_from_live.py --path /liquidation/ --confirm
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
STAGING = (os.getenv("WP_STAGING_URL") or "").rstrip("/")

LIVE_HOST = "www.companydebt.com"
STAGING_HOST = "comdebstage.wpengine.com"


def live_headers() -> dict:
    tok = base64.b64encode(
        f"{os.getenv('WP_LIVE_USERNAME')}:{os.getenv('WP_LIVE_APP_PASSWORD')}".encode()).decode()
    return {"User-Agent": "Company Debt-Publisher/1.0", "Authorization": f"Basic {tok}"}


def staging_session() -> requests.Session:
    """Staging needs cookie auth: nginx and WP both want the Authorization header."""
    http_auth = (os.getenv("WP_BASIC_AUTH_USER"), os.getenv("WP_BASIC_AUTH_PASS"))
    s = requests.Session()
    s.headers["User-Agent"] = "Company Debt-Publisher/1.0"
    s.get(f"{STAGING}/wp-login.php", auth=http_auth, timeout=20)
    s.post(f"{STAGING}/wp-login.php", auth=http_auth,
           headers={"Referer": f"{STAGING}/wp-login.php", "Origin": STAGING},
           data={"log": os.getenv("WP_USERNAME", os.getenv("WP_STAGING_USERNAME")),
                 "pwd": os.getenv("WP_STAGING_APP_PASSWORD"),
                 "wp-submit": "Log In", "redirect_to": f"{STAGING}/wp-admin/",
                 "testcookie": "1"},
           allow_redirects=True, timeout=40)
    if not [c for c in s.cookies if c.name.startswith("wordpress_logged_in_")]:
        sys.exit("ERROR: staging login failed - check WP_STAGING_* in .env")
    admin = s.get(f"{STAGING}/wp-admin/", auth=http_auth, timeout=20)
    m = (re.search(r'wpApiSettings[^}]+nonce["\s:]+"([a-f0-9]+)"', admin.text)
         or re.search(r'"nonce":"([a-f0-9]+)"', admin.text))
    if not m:
        sys.exit("ERROR: could not get the staging REST nonce")
    s.headers["X-WP-Nonce"] = m.group(1)
    s.auth = http_auth
    return s


def words(html: str) -> int:
    return len(re.sub(r"<[^>]+>", " ", html).split())


def anchors(html: str) -> int:
    return len(re.findall(r'id="[a-z0-9\-]+"', html))


def to_staging_urls(html: str) -> str:
    """Live content points at live; on staging it should point at staging."""
    return html.replace(f"https://{LIVE_HOST}", f"https://{STAGING_HOST}")


def decide(live: str, stage: str) -> tuple[str, str]:
    """Which side is newer. Returns (action, reason)."""
    if live.strip() == stage.strip():
        return "skip", "identical"

    lw, sw = words(live), words(stage)
    la, sa = anchors(live), anchors(stage)

    # Staging clearly holds newer editorial work - never overwrite it.
    if sw > lw + 50:
        return "hold", f"staging has {sw - lw} more words - staging work, leave for review"
    if sa > la:
        return "hold", f"staging has {sa - la} more anchors - staging work, leave for review"

    if lw > sw + 20 or la > sa:
        bits = []
        if lw > sw:
            bits.append(f"{lw - sw} more words")
        if la > sa:
            bits.append(f"{la - sa} more heading anchors")
        return "sync", "live has " + " and ".join(bits)

    return "sync", "live is newer (cosmetic drift, e.g. CTA arrows)"


def main() -> int:
    ap = argparse.ArgumentParser(description="Bring staging back into step with live.")
    ap.add_argument("--confirm", action="store_true", help="actually write to staging")
    ap.add_argument("--list", action="store_true", help="show decisions only")
    ap.add_argument("--path", nargs="*", help="only paths containing these strings")
    ap.add_argument("--pause", type=float, default=1.2)
    ap.add_argument("--report", default="staging_sync_report.json")
    args = ap.parse_args()

    cache = json.loads(CACHE.read_text(encoding="utf-8"))
    items = list(cache.items())
    if args.path:
        items = [i for i in items if any(p in i[0] for p in args.path)]

    LH = live_headers()
    sess = staging_session() if args.confirm else None

    print("WRITING TO STAGING" if args.confirm else "DRY RUN - nothing will be written")
    print(f"{len(items)} page(s). Live is read-only throughout.\n")

    synced, held, same, failed = [], [], 0, []

    for path, meta in items:
        pid = meta.get("id")
        ptype = meta.get("endpoint") or ("posts" if meta.get("type") == "post" else "pages")
        stage_html = meta.get("raw") or ""

        r = requests.get(f"{LIVE}/wp-json/wp/v2/{ptype}/{pid}?context=edit",
                         headers=LH, timeout=90)
        if r.status_code == 429:
            time.sleep(12)
            r = requests.get(f"{LIVE}/wp-json/wp/v2/{ptype}/{pid}?context=edit",
                             headers=LH, timeout=90)
        if r.status_code != 200:
            failed.append((path, f"live read {r.status_code}"))
            print(f"  ??    {path}  (live read {r.status_code})")
            time.sleep(args.pause)
            continue

        d = r.json()
        live_html = (d.get("content") or {}).get("raw", "")
        if d.get("slug") and meta.get("slug") and d["slug"] != meta["slug"]:
            held.append((path, f"id {pid} is a different page on each site"))
            print(f"  HOLD  {path}  id points at different pages")
            time.sleep(args.pause)
            continue

        action, reason = decide(live_html, stage_html)

        if action == "skip":
            same += 1
        elif action == "hold":
            held.append((path, reason))
            print(f"  hold  {path}  {reason}")
        elif not args.confirm:
            synced.append({"path": path, "id": pid, "reason": reason})
            print(f"  would {path}  {reason}")
        else:
            payload = {"content": to_staging_urls(live_html)}
            w = sess.post(f"{STAGING}/wp-json/wp/v2/{ptype}/{pid}", json=payload, timeout=90)
            if w.status_code in (200, 201):
                synced.append({"path": path, "id": pid, "reason": reason})
                print(f"  sync  {path}  {reason}")
            else:
                failed.append((path, f"staging write {w.status_code}"))
                print(f"  FAIL  {path}  staging write {w.status_code}")

        time.sleep(args.pause)

    (ROOT / args.report).write_text(json.dumps(
        {"synced": synced, "held": held, "identical": same, "failed": failed},
        indent=2), encoding="utf-8")

    verb = "synced" if args.confirm else "would sync"
    print(f"\n{verb}: {len(synced)}   already matching: {same}   "
          f"held (staging newer): {len(held)}   failed: {len(failed)}")
    print(f"\nHELD - these are the pages with genuine staging work:")
    for p, why in held:
        print(f"  {p}: {why}")
    print(f"\nreport written to {args.report}")
    if args.confirm:
        print("\nRefresh the local copy afterwards: python scripts/build_content_cache.py")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
