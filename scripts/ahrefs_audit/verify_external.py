"""Re-check every external URL Ahrefs flagged as 4XX, using a real browser UA.

Ahrefs' verdict cannot be trusted for hosts that block bots. This asks the
question that actually matters: what does a *reader* get?

  200 to browser + 404 to bot  -> FALSE POSITIVE, leave the citation alone
  404 to both                  -> GENUINELY DEAD, needs a new target URL
  redirect                     -> ALIVE but moved, update citation to final URL
"""
from __future__ import annotations

import concurrent.futures as cf
import json
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).parent))
from parse_export import read_export

BROWSER_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
BOT_UA = "Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/)"

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def fetch(url: str, ua: str) -> tuple[int | str, str]:
    """Return (status, final_url). GET not HEAD: many hosts 405/404 a HEAD."""
    req = urllib.request.Request(url, headers={
        "User-Agent": ua,
        "Accept": "text/html,application/xhtml+xml,application/pdf,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.9",
    })
    try:
        with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
            r.read(2048)
            return r.status, r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, url
    except Exception as e:
        return type(e).__name__, url


def verdict(browser_status, bot_status, final, url):
    ok = browser_status == 200
    moved = ok and final.rstrip("/") != url.rstrip("/")
    if ok and bot_status != 200:
        return "FALSE_POSITIVE_BOT_BLOCK", "Reader gets 200; bot gets %s. Leave as-is." % bot_status
    if moved:
        return "MOVED", "Alive but redirects to %s - update citation." % final
    if ok:
        return "OK_NOW", "200 to everyone; Ahrefs data may be stale."
    return "GENUINELY_DEAD", "Browser also gets %s - needs a replacement URL." % browser_status


def check(url: str) -> dict:
    b_status, b_final = fetch(url, BROWSER_UA)
    r_status, _ = fetch(url, BOT_UA)
    v, note = verdict(b_status, r_status, b_final, url)
    return {"url": url, "host": urlsplit(url).netloc, "browser": b_status,
            "bot": r_status, "final": b_final, "verdict": v, "note": note}


def main(export_dir: Path, out_path: Path):
    rows = read_export(export_dir / "Notice-External_4XX.csv")
    urls = sorted({r["URL"] for r in rows if r["URL"].startswith("http")})
    print(f"Checking {len(urls)} external URLs with browser + bot UA...\n")

    results = []
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        for res in ex.map(check, urls):
            results.append(res)

    order = ["GENUINELY_DEAD", "MOVED", "OK_NOW", "FALSE_POSITIVE_BOT_BLOCK"]
    results.sort(key=lambda r: (order.index(r["verdict"]), r["url"]))

    for v in order:
        group = [r for r in results if r["verdict"] == v]
        if not group:
            continue
        print(f"\n{'=' * 78}\n{v}  ({len(group)})\n{'=' * 78}")
        for r in group:
            print(f"  browser={r['browser']!s:<12} bot={r['bot']!s:<6} {r['url'][:95]}")
            if r["verdict"] == "MOVED":
                print(f"      -> {r['final'][:95]}")

    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\n\nWrote {out_path}")
    print("\nSUMMARY:")
    for v in order:
        n = sum(1 for r in results if r["verdict"] == v)
        if n:
            print(f"  {n:>4}  {v}")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
