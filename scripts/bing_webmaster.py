"""Bing Webmaster Tools API helper (companydebt.com + sister sites).

Auth: BING_WEBMASTER_API_KEY in project .env. No MCP server exists for Bing,
so this is the reusable path for pulling Bing search data.

The JSON API lives at https://ssl.bing.com/webmaster/api.svc/json/<Method>.
GetQueryStats / GetPageStats return a PER-DATE time series, so this helper
aggregates rows by query/page (sum clicks+impressions, impression-weighted
average position) before returning them.

CLI:
    sites
    queries   <siteUrl> [--limit N] [--json]
    pages     <siteUrl> [--limit N] [--json]
    traffic   <siteUrl> [--json]                 # GetRankAndTrafficStats
    quickwins <siteUrl> [--min-impr 20] [--max-ctr 2] [--pos-min 4] [--pos-max 10] [--json]

`quickwins` = you already rank on page 1 (pos 4-10) with enough impressions but
a low CTR — the cheapest clicks to win via title/snippet or a small rank nudge.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict

from dotenv import load_dotenv

ROOT = pathlib.Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
BASE = "https://ssl.bing.com/webmaster/api.svc/json/"


def _key() -> str:
    k = os.environ.get("BING_WEBMASTER_API_KEY")
    if not k:
        sys.exit("BING_WEBMASTER_API_KEY missing from .env")
    return k


def call(method: str, **params):
    params["apikey"] = _key()
    url = BASE + method + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "cd-bing-webmaster"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            payload = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        sys.exit(f"{method} HTTP {e.code}: {e.read().decode()[:300]}")
    # Bing wraps the result in {"d": ...}
    return payload.get("d", payload) if isinstance(payload, dict) else payload


def _aggregate(rows, key_field):
    """Collapse the per-date time series into one row per query/page."""
    agg = defaultdict(lambda: {"clicks": 0, "impr": 0, "pos_w": 0.0})
    for r in rows:
        k = r.get(key_field)
        if k is None:
            continue
        clicks = r.get("Clicks") or 0
        impr = r.get("Impressions") or 0
        pos = r.get("AvgImpressionPosition") or 0
        a = agg[k]
        a["clicks"] += clicks
        a["impr"] += impr
        a["pos_w"] += pos * (impr or 1)
        a["_wsum"] = a.get("_wsum", 0) + (impr or 1)
    out = []
    for k, a in agg.items():
        impr = a["impr"]
        pos = a["pos_w"] / a["_wsum"] if a["_wsum"] else 0
        ctr = (a["clicks"] / impr * 100) if impr else 0.0
        out.append({key_field: k, "clicks": a["clicks"], "impressions": impr,
                    "ctr_pct": round(ctr, 2), "avg_position": round(pos, 1)})
    return out


def _print_table(rows, key_field, label):
    if not rows:
        print("  (no rows)")
        return
    width = max(len(label), *(len(str(r[key_field])[:48]) for r in rows))
    print(f"  {label:<{width}}  {'clicks':>6} {'impr':>7} {'ctr%':>6} {'pos':>5}")
    for r in rows:
        print(f"  {str(r[key_field])[:48]:<{width}}  {r['clicks']:>6} "
              f"{r['impressions']:>7} {r['ctr_pct']:>6} {r['avg_position']:>5}")


def cmd_sites(a):
    sites = call("GetUserSites")
    if a.json:
        print(json.dumps(sites, indent=2)); return
    for s in sites:
        print(f"  {'OK ' if s.get('IsVerified') else 'NV '} {s.get('Url')}")


def _query_rows(site):
    return _aggregate(call("GetQueryStats", siteUrl=site), "Query")


def _page_rows(site):
    return _aggregate(call("GetPageStats", siteUrl=site), "Query")  # Query field holds the URL


def cmd_queries(a):
    rows = sorted(_query_rows(a.siteUrl), key=lambda r: -r["clicks"])[: a.limit]
    print(json.dumps(rows, indent=2)) if a.json else _print_table(rows, "Query", "query")


def cmd_pages(a):
    rows = sorted(_page_rows(a.siteUrl), key=lambda r: -r["clicks"])[: a.limit]
    print(json.dumps(rows, indent=2)) if a.json else _print_table(rows, "Query", "page")


def cmd_traffic(a):
    print(json.dumps(call("GetRankAndTrafficStats", siteUrl=a.siteUrl), indent=2))


def cmd_quickwins(a):
    rows = [r for r in _query_rows(a.siteUrl)
            if a.pos_min <= r["avg_position"] <= a.pos_max
            and r["impressions"] >= a.min_impr
            and r["ctr_pct"] <= a.max_ctr]
    rows.sort(key=lambda r: -r["impressions"])
    rows = rows[: a.limit]
    if a.json:
        print(json.dumps(rows, indent=2)); return
    print(f"Bing quick wins for {a.siteUrl} "
          f"(pos {a.pos_min}-{a.pos_max}, impr>={a.min_impr}, ctr<={a.max_ctr}%):")
    _print_table(rows, "Query", "query")


def main() -> int:
    ap = argparse.ArgumentParser(description="Bing Webmaster Tools helper")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("sites"); p.set_defaults(fn=cmd_sites); p.add_argument("--json", action="store_true")
    for name, fn in (("queries", cmd_queries), ("pages", cmd_pages)):
        p = sub.add_parser(name); p.set_defaults(fn=fn)
        p.add_argument("siteUrl"); p.add_argument("--limit", type=int, default=25)
        p.add_argument("--json", action="store_true")
    p = sub.add_parser("traffic"); p.set_defaults(fn=cmd_traffic); p.add_argument("siteUrl")
    p = sub.add_parser("quickwins"); p.set_defaults(fn=cmd_quickwins)
    p.add_argument("siteUrl")
    p.add_argument("--min-impr", dest="min_impr", type=int, default=20)
    p.add_argument("--max-ctr", dest="max_ctr", type=float, default=2.0)
    p.add_argument("--pos-min", dest="pos_min", type=float, default=4.0)
    p.add_argument("--pos-max", dest="pos_max", type=float, default=10.0)
    p.add_argument("--limit", type=int, default=25)
    p.add_argument("--json", action="store_true")

    a = ap.parse_args()
    a.fn(a)
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
