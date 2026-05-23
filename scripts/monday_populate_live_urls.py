"""Populate the 'Live URL' column on Monday board 18406273663 'Live' group.

Source of truth: each item's existing 'Staging URL' column (path is taken from there).
Production base: https://www.companydebt.com  (apex 301s to www).

Workflow:
  1. Fetch all Live group items + their Staging URL column.
  2. For each, HEAD/GET https://www.companydebt.com{path} with a browser User-Agent.
  3. Status 200            -> write Live URL = that exact URL
     Status 301/302/3xx    -> follow once and use final 200 URL (don't follow further)
     Status 4xx/5xx        -> SKIP and flag (don't write a broken URL)
  4. Touch ONLY the Live URL column. Nothing else.

Usage:
  python scripts/monday_populate_live_urls.py --dry-run
  MONDAY_LIVE_URL_CONFIRM=yes python scripts/monday_populate_live_urls.py --apply
"""

from __future__ import annotations

import argparse
import io
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

if sys.platform == "win32":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)
    except Exception:
        pass

BOARD_ID = 18406273663
LIVE_GROUP_TITLE = "Live"
LIVE_URL_COLUMN_ID = "link_mm29234m"  # Live URL column on this board
STAGING_URL_COLUMN_ID = "link_mm1ywn7s"
PROD_BASE = "https://www.companydebt.com"
MONDAY_URL = "https://api.monday.com/v2"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def load_token() -> str:
    here = Path(__file__).resolve()
    for c in [here.parents[1] / ".env", here.parents[3] / ".env", here.parents[4] / ".env"]:
        if c.exists():
            load_dotenv(c); break
    tok = os.environ.get("MONDAY_API_KEY")
    if not tok:
        sys.exit("MONDAY_API_KEY not set")
    return tok


def gql(token: str, query: str, variables: dict[str, Any] | None = None, api_version: str = "2025-10") -> dict[str, Any]:
    import time
    for _ in range(5):
        r = requests.post(MONDAY_URL,
                          headers={"Authorization": token, "Content-Type": "application/json", "API-Version": api_version},
                          json={"query": query, "variables": variables or {}}, timeout=30)
        if r.status_code == 429:
            time.sleep(int(r.headers.get("Retry-After", "10"))); continue
        r.raise_for_status()
        data = r.json()
        if "errors" in data:
            err = json.dumps(data["errors"])
            if "ComplexityException" in err or "rate" in err.lower():
                time.sleep(10); continue
            raise RuntimeError(err)
        return data["data"]
    raise RuntimeError("gql: exhausted retries")


def fetch_live_items(token: str) -> list[dict[str, Any]]:
    q1 = '{ boards(ids: [18406273663]) { groups { id title } } }'
    groups = gql(token, q1)["boards"][0]["groups"]
    live_id = next(g["id"] for g in groups if g["title"].strip().lower() == LIVE_GROUP_TITLE.lower())

    q2 = """query ($g: String!, $c: String) {
      boards(ids: [18406273663]) {
        groups(ids: [$g]) {
          items_page(limit: 100, cursor: $c) {
            cursor
            items {
              id name
              column_values(ids: ["link_mm1ywn7s", "link_mm29234m"]) {
                id text value column { title }
              }
            }
          }
        }
      }
    }"""
    items: list[dict[str, Any]] = []
    cursor = None
    while True:
        page = gql(token, q2, {"g": live_id, "c": cursor})["boards"][0]["groups"][0]["items_page"]
        items.extend(page["items"])
        cursor = page.get("cursor")
        if not cursor: break
    return items


def extract_path(item: dict[str, Any]) -> str:
    for cv in item.get("column_values", []):
        if cv.get("column", {}).get("title") == "Staging URL" and cv.get("text"):
            text = cv["text"].strip()
            first = text.split(" - ", 1)[0].strip()
            if first.startswith("/"):
                p = first.split("?", 1)[0].split("#", 1)[0]
                if not p.endswith("/"):
                    p += "/"
                return p
    return ""


def existing_live_url(item: dict[str, Any]) -> str:
    for cv in item.get("column_values", []):
        if cv.get("column", {}).get("title") == "Live URL":
            return (cv.get("text") or "").strip()
    return ""


def probe(path: str) -> dict[str, Any]:
    """HEAD-style probe with GET (some servers reject HEAD). Returns final URL + status."""
    url = PROD_BASE + path
    try:
        r = requests.get(url, allow_redirects=True, timeout=15, headers={"User-Agent": USER_AGENT})
        return {"path": path, "status": r.status_code, "final_url": r.url, "ok": r.status_code == 200}
    except Exception as e:
        return {"path": path, "status": 0, "final_url": "", "ok": False, "error": str(e)}


def probe_all(paths: list[str], workers: int = 10) -> dict[str, dict[str, Any]]:
    results: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(probe, p): p for p in paths}
        done = 0
        for fut in as_completed(futures):
            r = fut.result()
            results[r["path"]] = r
            done += 1
            if done % 50 == 0:
                print(f"  probed {done}/{len(paths)}")
    return results


def write_live_url(token: str, item_id: str, url: str, display_text: str) -> None:
    """Write to the Live URL link column. Touches ONLY this column."""
    # Monday link column expects a JSON value with url + text.
    value = json.dumps({"url": url, "text": display_text})
    mutation = """
    mutation ($board: ID!, $item: ID!, $col: String!, $val: JSON!) {
      change_column_value(board_id: $board, item_id: $item, column_id: $col, value: $val) { id }
    }
    """
    gql(token, mutation, {
        "board": str(BOARD_ID),
        "item": str(item_id),
        "col": LIVE_URL_COLUMN_ID,
        "val": value,
    })


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--workers", type=int, default=10)
    ap.add_argument("--report", default="data/monday-live-url-plan.json")
    ap.add_argument("--overwrite-existing", action="store_true",
                    help="Also overwrite items that already have a Live URL set (default: skip them)")
    args = ap.parse_args()
    if args.apply == args.dry_run:
        sys.exit("Pick exactly one of --dry-run or --apply.")

    token = load_token()
    print(f"Fetching Live group items...")
    items = fetch_live_items(token)
    print(f"  fetched {len(items)} items")

    plans: list[dict[str, Any]] = []
    no_path: list[dict[str, Any]] = []
    for it in items:
        path = extract_path(it)
        existing = existing_live_url(it)
        if not path:
            no_path.append({"id": it["id"], "name": it["name"]})
            continue
        plans.append({"id": it["id"], "name": it["name"], "path": path, "existing_live_url": existing})

    paths = sorted({p["path"] for p in plans})
    print(f"Probing {len(paths)} unique paths against {PROD_BASE}...")
    results = probe_all(paths, workers=args.workers)

    will_write: list[dict[str, Any]] = []
    skip_404: list[dict[str, Any]] = []
    skip_existing: list[dict[str, Any]] = []
    skip_redirect_offsite: list[dict[str, Any]] = []
    for p in plans:
        probe_res = results.get(p["path"], {})
        if not probe_res.get("ok"):
            skip_404.append({**p, "status": probe_res.get("status"), "final_url": probe_res.get("final_url")})
            continue
        final_url = probe_res["final_url"]
        # Sanity: final URL should still be on companydebt.com
        if "companydebt.com" not in final_url:
            skip_redirect_offsite.append({**p, "final_url": final_url})
            continue
        if p["existing_live_url"] and not args.overwrite_existing:
            skip_existing.append({**p, "final_url": final_url})
            continue
        # Display text mirrors the Staging URL convention: show the path
        display_text = p["path"]
        will_write.append({**p, "live_url": final_url, "display_text": display_text})

    Path(args.report).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report).write_text(json.dumps({
        "will_write": will_write,
        "skip_404_or_error": skip_404,
        "skip_existing": skip_existing,
        "skip_redirect_offsite": skip_redirect_offsite,
        "no_path": no_path,
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n=== Plan summary ===")
    print(f"  will write Live URL:        {len(will_write)}")
    print(f"  skip (already set):         {len(skip_existing)} (use --overwrite-existing to force)")
    print(f"  skip (404/error):           {len(skip_404)}")
    print(f"  skip (redirects off-site):  {len(skip_redirect_offsite)}")
    print(f"  skip (no Staging URL):      {len(no_path)}")

    if will_write:
        print(f"\n  First 5 to write:")
        for w in will_write[:5]:
            print(f"    {w['name'][:60]:<60}  {w['live_url']}")

    if skip_404:
        print(f"\n  Items with 404/error (will NOT be written):")
        for s in skip_404[:20]:
            print(f"    [{s.get('status')}] {s['name'][:55]:<55}  {s['path']}")
        if len(skip_404) > 20:
            print(f"    ... and {len(skip_404) - 20} more")

    if skip_redirect_offsite:
        print(f"\n  Items that redirect OFF companydebt.com (will NOT be written):")
        for s in skip_redirect_offsite:
            print(f"    {s['name']}  {s['path']}  ->  {s['final_url']}")

    if args.apply:
        if os.environ.get("MONDAY_LIVE_URL_CONFIRM") != "yes":
            sys.exit("\nRefusing to apply: set MONDAY_LIVE_URL_CONFIRM=yes to proceed.")
        print(f"\n=== APPLYING — writing Live URL to {len(will_write)} items ===")
        for i, w in enumerate(will_write, 1):
            write_live_url(token, w["id"], w["live_url"], w["display_text"])
            if i % 25 == 0 or i == len(will_write):
                print(f"  wrote {i}/{len(will_write)}")
        print(f"\nDone.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
