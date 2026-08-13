"""Publish a single page/post straight to LIVE over the WordPress REST API.

WHY THIS EXISTS
---------------
The old route to live was a WP Engine staging->live "copy environment", which
replaces the LIVE database wholesale. Staging never receives real form
submissions, so every full-DB push destroyed every Gravity Forms entry created
on live since the previous push - roughly 160 enquiries between 23 Mar and
28 Jul 2026, silently. See docs/staging-to-live-push.md.

Publishing one page at a time over the REST API touches only that page, so the
database push (and the data loss) is no longer needed for content changes.

Note `wp_push.py` CANNOT do this: it works over SFTP + a one-shot mu-plugin,
and there is no live SFTP by design.

AUTHORISATION
-------------
Piers's standing rule: "always wait for my explicit instructions before pushing
live." Credentials existing is NOT permission. This script therefore refuses to
write unless --confirm is passed, and Claude must be asked for each specific
push. Without --confirm it is a dry run that only reads.

USAGE
    python scripts/publish_to_live.py --id 7669 --file preview/liquidation.html
    python scripts/publish_to_live.py --id 7669 --file preview/liquidation.html --confirm
    python scripts/publish_to_live.py --id 24589 --file x.html --post-type posts --confirm

Environment (.env): CD_LIVE_URL, WP_LIVE_USERNAME, WP_LIVE_APP_PASSWORD
"""
from __future__ import annotations

import argparse
import difflib
import os
import pathlib
import re
import sys

import requests
from dotenv import load_dotenv

ROOT = pathlib.Path(__file__).resolve().parents[1]

# .env sits at the top of the main checkout. When this runs from a git worktree
# under .claude/worktrees/<name>/, ROOT is the worktree and holds no .env, so
# the credentials came back empty and the script aborted claiming they were
# missing from a file it had never looked at. Walk up until one is found.
def _load_env() -> None:
    for candidate in (ROOT, *ROOT.parents):
        env = candidate / ".env"
        if env.is_file():
            load_dotenv(env)
            return
    load_dotenv(ROOT / ".env")  # keep the original behaviour if none found


_load_env()

# The live WAF rejects the default requests user-agent; WP rejects some writes
# without a same-origin Referer/Origin.
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

# Refuse a push that shrinks a page below this fraction of its current size.
# A 200 OK has silently truncated a live page to a garbage fragment before.
SHRINK_FLOOR = 0.5


def _cfg():
    base = (os.environ.get("CD_LIVE_URL") or "").rstrip("/")
    user = os.environ.get("WP_LIVE_USERNAME")
    pw = os.environ.get("WP_LIVE_APP_PASSWORD")
    missing = [k for k, v in (("CD_LIVE_URL", base), ("WP_LIVE_USERNAME", user),
                              ("WP_LIVE_APP_PASSWORD", pw)) if not v]
    if missing:
        sys.exit(f"ERROR: missing from .env: {', '.join(missing)}")
    return base, (user, pw)


def _headers(base):
    return {"User-Agent": UA, "Referer": base + "/", "Origin": base,
            "Content-Type": "application/json"}


def fetch(base, auth, post_type, pid):
    r = requests.get(f"{base}/wp-json/wp/v2/{post_type}/{pid}",
                     params={"context": "edit"}, auth=auth,
                     headers={"User-Agent": UA}, timeout=60)
    if r.status_code == 404:
        sys.exit(f"ERROR: no {post_type[:-1]} with ID {pid} on live. Check the ID "
                 f"and --post-type (pages vs posts).")
    r.raise_for_status()
    return r.json()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--id", type=int, required=True, help="LIVE post/page ID")
    ap.add_argument("--file", required=True, help="HTML file to publish")
    ap.add_argument("--post-type", default="pages", choices=["pages", "posts"],
                    help="default: pages. A blog article is 'posts'.")
    ap.add_argument("--status", choices=["publish", "draft", "pending", "private"],
                    help="set post_status (omit to leave unchanged)")
    ap.add_argument("--title", help="override post title")
    ap.add_argument("--confirm", action="store_true",
                    help="actually write. Without this it is a read-only dry run.")
    ap.add_argument("--force", action="store_true",
                    help="override the shrink guard (think hard first)")
    args = ap.parse_args()

    path = pathlib.Path(args.file)
    if not path.exists():
        sys.exit(f"ERROR: file not found: {path}")
    new_html = path.read_text(encoding="utf-8")
    if not new_html.strip():
        sys.exit("ERROR: file is empty")

    base, auth = _cfg()
    current = fetch(base, auth, args.post_type, args.id)
    cur_html = (current.get("content") or {}).get("raw", "")
    cur_title = (current.get("title") or {}).get("raw", "")

    print(f"target   : {base}/wp-json/wp/v2/{args.post_type}/{args.id}")
    print(f"title    : {cur_title}")
    print(f"link     : {current.get('link')}")
    print(f"status   : {current.get('status')}")
    print(f"current  : {len(cur_html):,} bytes")
    print(f"new      : {len(new_html):,} bytes")

    if cur_html:
        ratio = len(new_html) / len(cur_html)
        print(f"change   : {ratio:.0%} of current size")
        if ratio < SHRINK_FLOOR and not args.force:
            print()
            print(f"REFUSING: new content is under {SHRINK_FLOOR:.0%} of the live page.")
            print("This is the exact shape of the truncation bug that has wiped a live")
            print("page before while returning 200 OK. Check the file is complete.")
            print("Pass --force only if the shrink is genuinely intended.")
            return 1

    sm = difflib.SequenceMatcher(None, cur_html, new_html)
    print(f"similarity: {sm.quick_ratio():.0%}")

    if not args.confirm:
        print()
        print("DRY RUN - nothing was written.")
        print("Re-run with --confirm to publish. Per Piers's standing rule, only do")
        print("that when he has explicitly asked for this specific push.")
        return 0

    payload = {"content": new_html}
    if args.status:
        payload["status"] = args.status
    if args.title:
        payload["title"] = args.title

    print("\npublishing...")
    r = requests.post(f"{base}/wp-json/wp/v2/{args.post_type}/{args.id}",
                      json=payload, auth=auth, headers=_headers(base), timeout=180)
    print(f"http     : {r.status_code}")
    if r.status_code >= 400:
        print(r.text[:600])
        return 1

    # A 200 is not proof. Re-read and measure.
    after = fetch(base, auth, args.post_type, args.id)
    got = (after.get("content") or {}).get("raw", "")
    print(f"verified : {len(got):,} bytes now live")
    if len(got) < len(new_html) * 0.95:
        print()
        print("WARNING: live content is materially shorter than what was sent.")
        print("Likely kses stripping (inline SVG/script) - inspect the page before")
        print("calling this done.")
        return 1
    print(f"live URL : {after.get('link')}")
    print("\nOK. Now purge caches and re-render the page to confirm what visitors see.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
