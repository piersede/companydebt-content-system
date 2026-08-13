"""Alarm for the silent failure that cost four months of form entries.

A WP Engine staging->live "copy environment" replaces the LIVE database wholesale.
Staging never receives real form submissions, so every full-database push restores
staging's stale snapshot over live and destroys every entry collected since the last
push. That ran undetected from 23 Mar 2026 to 28 Jul 2026 (~160 enquiries) because
nothing ever complained.

Run this AFTER any staging->live push, or on a schedule. It reads live's newest
Gravity Forms entry and fails loudly if entries have stopped arriving.

    python scripts/check_live_form_entries.py
    python scripts/check_live_form_entries.py --max-age-days 7
    python scripts/check_live_form_entries.py --json

Exit codes: 0 healthy, 1 stale (probable wipe), 2 cannot check.

Read-only. Never writes to live.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import sys

import requests
from dotenv import load_dotenv
from requests_oauthlib import OAuth1

ROOT = pathlib.Path(__file__).resolve().parents[1]
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
from _env import load_env as _load_env
_load_env()
# The live WAF rejects the default requests user-agent.
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


def _auth():
    key = os.environ.get("CD_GF_CONSUMER_KEY")
    secret = os.environ.get("CD_GF_CONSUMER_SECRET")
    if not key or not secret:
        raise SystemExit("2: CD_GF_CONSUMER_KEY / CD_GF_CONSUMER_SECRET missing from .env")
    # signature_type must be auth_header: the "query" form 401s on bracketed params
    return OAuth1(key, secret, signature_type="auth_header")


def fetch(base: str, path: str, params: dict | None = None):
    r = requests.get(f"{base}/wp-json/gf/v2{path}", auth=_auth(), params=params,
                     headers={"User-Agent": UA}, timeout=60)
    if r.status_code == 401:
        raise SystemExit(
            "2: Gravity Forms API key rejected (401).\n"
            "   A full database push INVALIDATES the key - regenerate it in\n"
            "   Forms > Settings > REST API, then update .env.\n"
            "   Check the consumer key is 43 chars starting with a SINGLE 'ck_'\n"
            "   (a doubled 'ck_ck_' prefix gives this exact error)."
        )
    r.raise_for_status()
    return r.json()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--max-age-days", type=float, default=3.0,
                    help="fail if the newest entry is older than this (default 3)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    base = (os.environ.get("CD_LIVE_URL") or "").rstrip("/")
    if not base:
        print("2: CD_LIVE_URL missing from .env", file=sys.stderr)
        return 2

    newest_dt, newest = None, None
    per_form = []
    forms = fetch(base, "/forms")
    for fid in sorted(forms, key=lambda x: int(x)):
        data = fetch(base, f"/forms/{fid}/entries", {"paging[page_size]": "1"})
        entries = data.get("entries") or []
        created = entries[0].get("date_created") if entries else None
        per_form.append({"form_id": int(fid), "title": forms[fid].get("title", ""),
                         "total": data.get("total_count"), "newest": created})
        if created:
            try:
                parsed = dt.datetime.strptime(created, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue
            if newest_dt is None or parsed > newest_dt:
                newest_dt, newest = parsed, {"form_id": int(fid), "date": created}

    if newest_dt is None:
        age_days = None
        healthy = False
    else:
        # Gravity Forms stores date_created in UTC; compare naive-to-naive.
        now_utc = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
        age_days = (now_utc - newest_dt).total_seconds() / 86400
        healthy = age_days <= args.max_age_days

    if args.json:
        print(json.dumps({"healthy": healthy, "newest": newest,
                          "age_days": None if age_days is None else round(age_days, 2),
                          "max_age_days": args.max_age_days, "forms": per_form}, indent=1))
        return 0 if healthy else 1

    print(f"live site : {base}")
    print(f"{'form':>5}  {'entries':>7}  newest entry")
    for f in per_form:
        print(f"{f['form_id']:>5}  {str(f['total']):>7}  {f['newest'] or '(none)'}   {f['title'][:38]}")
    print()
    if newest_dt is None:
        print("FAIL: no entries found at all.")
        return 1
    print(f"newest entry anywhere: {newest['date']} (form {newest['form_id']}), "
          f"{age_days:.1f} days old")
    if healthy:
        print(f"OK: entries are arriving (threshold {args.max_age_days} days).")
        return 0
    print()
    print(f"FAIL: newest entry is {age_days:.1f} days old, over the "
          f"{args.max_age_days}-day threshold.")
    print("Most likely cause: a staging->live push copied the FULL database and")
    print("wiped every entry created on live since the previous push.")
    print("Fix: when copying environments, select specific tables and exclude")
    print("wp_gf_entry, wp_gf_entry_meta, wp_gf_entry_notes, wp_gf_draft_submissions,")
    print("wp_gf_form_view, wp_users, wp_usermeta, wp_comments, wp_commentmeta,")
    print("wp_stream, wp_stream_meta, wp_actionscheduler_actions, wp_rg_lead*.")
    print("Better: publish content straight to live and never push the database.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
