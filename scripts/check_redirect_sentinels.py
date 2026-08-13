"""Guard against silently-lost redirects.

The pre-pack 404 (2026-06-20) happened because a Quick Redirects (qppr) 301 for a
trashed/consolidated page vanished and turned into a 404 with nobody watching.
This checker hits a curated list of must-always-301 URLs (redirect-sentinels.json)
on staging and asserts each still resolves to its canonical target in a SINGLE hop.

Run it after any qppr change, and periodically. Exits non-zero on any drift so it
can gate a workflow or CI step.

Usage:
    python scripts/check_redirect_sentinels.py
"""
from __future__ import annotations

import json
import os
import pathlib
import sys

import requests
from dotenv import load_dotenv

ROOT = pathlib.Path(__file__).resolve().parents[1]
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
from _env import load_env as _load_env
_load_env()
BROWSER_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


def main() -> int:
    cfg = json.loads((ROOT / "redirect-sentinels.json").read_text(encoding="utf-8"))
    host = cfg["host"].rstrip("/")
    auth = (os.environ["WP_BASIC_AUTH_USER"], os.environ["WP_BASIC_AUTH_PASS"])
    headers = {"User-Agent": BROWSER_UA}

    failures = []
    for s in cfg["sentinels"]:
        req = s["request"]
        want = host + s["expect_final"]
        try:
            r = requests.get(host + req, auth=auth, headers=headers,
                             allow_redirects=True, timeout=60)
        except requests.RequestException as exc:
            failures.append(f"{req}  ERROR {exc}")
            print(f"XX {req}  ERROR {exc}")
            continue
        hops = [h.status_code for h in r.history]
        ok = (len(r.history) == 1 and r.history[0].status_code == 301
              and r.status_code == 200 and r.url == want)
        if not ok:
            failures.append(f"{req}  chain={hops} final={r.status_code} {r.url}")
        print(f"{'OK' if ok else 'XX'} {req}  chain={hops} final={r.status_code} {r.url}")

    print()
    if failures:
        print(f"DRIFT: {len(failures)}/{len(cfg['sentinels'])} sentinel(s) failed:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"All {len(cfg['sentinels'])} redirect sentinels healthy (single-hop 301 -> canonical).")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
