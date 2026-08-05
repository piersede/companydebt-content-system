"""One-shot: bootstrap the Insolvency Test on live via the mu-plugin's
/wp-json/cd-itest/v1/bootstrap endpoint.

Runs AFTER the WPE files-only copy has put cd-insolvency-test-zoho.php on
live. Uses the live WordPress application-password (WP_LIVE_USERNAME +
WP_LIVE_APP_PASSWORD in .env) for auth, so no shell/SFTP into live is
needed. Zoho credentials come from CD_ZOHO_* in .env and are sent in the
POST body.

The endpoint is idempotent and self-disables after first success (via
wp_options['cd_itest_bootstrap_done']), so re-running is safe but will
409 once it's already run.

Usage:
    python scripts/live_bootstrap_insolvency_test.py             # dry run
    python scripts/live_bootstrap_insolvency_test.py --confirm   # actually run
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import sys

import requests
from dotenv import load_dotenv

ROOT = pathlib.Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
LIVE = "https://www.companydebt.com"


def _env(key: str) -> str:
    v = os.getenv(key, "")
    return v.strip().strip('"').strip("'")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--confirm", action="store_true", help="actually POST to live")
    args = ap.parse_args()

    user   = _env("WP_LIVE_USERNAME")
    app_pw = _env("WP_LIVE_APP_PASSWORD")
    zoho = dict(
        client_id       = _env("CD_ZOHO_CLIENT_ID"),
        client_secret   = _env("CD_ZOHO_CLIENT_SECRET"),
        refresh_token   = _env("CD_ZOHO_REFRESH_TOKEN"),
        api_domain      = _env("CD_ZOHO_API_DOMAIN") or "https://www.zohoapis.com",
        accounts_domain = _env("CD_ZOHO_ACCOUNTS_DOMAIN") or "https://accounts.zoho.com",
    )
    missing = [k for k, v in dict(user=user, app_pw=app_pw, **zoho).items() if not v]
    if missing:
        print("ERROR: missing env values:", ", ".join(missing))
        return 2

    url = f"{LIVE}/wp-json/cd-itest/v1/bootstrap"
    payload = {"zoho": zoho}
    redacted = {k: (v[:6] + "…") for k, v in zoho.items() if k in ("client_id","client_secret","refresh_token")}
    print("plan:")
    print(f"  POST {url}")
    print(f"  auth: Basic {user}:<app-password>")
    print(f"  body: {{ zoho: {json.dumps({**zoho, **redacted}, indent=2)} }}")
    if not args.confirm:
        print("\ndry run — pass --confirm to actually POST")
        return 0

    r = requests.post(url, auth=(user, app_pw), json=payload,
                      headers={"User-Agent": "cd-itest-bootstrap/1.0"}, timeout=60)
    print(f"\nHTTP {r.status_code}")
    try:
        d = r.json()
        print(json.dumps(d, indent=2))
    except Exception:
        print(r.text[:2000])
    return 0 if r.status_code == 200 else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
