#!/usr/bin/env python3
"""End-to-end check: did each live Gravity Forms entry reach the Zoho CRM?

Pulls every entry in a date range from the named live forms, extracts the
email address from each, then looks for a matching Zoho Lead or Contact. Names
the entries with no match so someone can chase them.

Read-only against both systems. Never writes.

    python scripts/reconcile_forms_to_zoho.py --from 2026-08-01 --to 2026-08-19
    python scripts/reconcile_forms_to_zoho.py --from 2026-08-01 --to 2026-08-19 \
        --out google-ads-auditor/runs/2026-08-20-weekly-audit
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import pathlib
import re
import sys

import requests
from requests_oauthlib import OAuth1

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _env import load_env as _load_env  # noqa: E402

_load_env()

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

FORMS = {
    "29": "Contact Us",
    "44": "Home Page Contact Block",
    "46": "Insolvency Test",
    "40": "Quick Quote",
    "30": "Guide Download",
}

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")


def gf_auth():
    key = os.environ["CD_GF_CONSUMER_KEY"]
    secret = os.environ["CD_GF_CONSUMER_SECRET"]
    return OAuth1(key, secret, signature_type="auth_header")


def gf_entries(base, form_id, date_from, date_to, page_size=600):
    """Every entry for one form in the range.

    Only `paging[page_size]` may be sent: adding `paging[offset]` or any
    `sorting[...]` parameter makes the site reject the request signature. So
    ask for one large newest-first page and apply the date range here.
    """
    r = requests.get(f"{base}/wp-json/gf/v2/forms/{form_id}/entries", auth=gf_auth(),
                     params={"paging[page_size]": str(page_size)},
                     headers={"User-Agent": UA}, timeout=180)
    r.raise_for_status()
    data = r.json()
    batch = data.get("entries", [])
    out = [e for e in batch if date_from <= (e.get("date_created") or "")[:10] <= date_to]
    if batch:
        oldest = (batch[-1].get("date_created") or "")[:10]
        if oldest > date_from and len(batch) >= page_size:
            print(f"    WARNING: form {form_id} page did not reach back to {date_from} "
                  f"(oldest seen {oldest}); raise --page-size")
    return out


def entry_email(entry):
    for k, v in entry.items():
        if not isinstance(v, str) or "@" not in v:
            continue
        m = EMAIL_RE.search(v)
        if m:
            return m.group(0).lower()
    return None


def entry_name(entry):
    """Best-effort person name: the first short, alphabetic answer field."""
    def order(k):
        try:
            return (0, float(k))
        except ValueError:
            return (1, 0.0)
    for k in sorted((k for k in entry if re.match(r"^\d+(\.\d+)?$", k)), key=order):
        v = entry[k]
        if not isinstance(v, str) or not v.strip() or "@" in v or len(v) >= 60:
            continue
        if re.match(r"^[A-Za-z][A-Za-z'. -]+$", v.strip()):
            return v.strip()
    return "(no name field)"


def zoho_token():
    domain = os.environ.get("CD_ZOHO_ACCOUNTS_DOMAIN", "https://accounts.zoho.com")
    r = requests.post(
        f"{domain.rstrip('/')}/oauth/v2/token",
        data={
            "refresh_token": os.environ["CD_ZOHO_REFRESH_TOKEN"],
            "client_id": os.environ["CD_ZOHO_CLIENT_ID"],
            "client_secret": os.environ["CD_ZOHO_CLIENT_SECRET"],
            "grant_type": "refresh_token",
        },
        timeout=60,
    )
    r.raise_for_status()
    payload = r.json()
    if "access_token" not in payload:
        raise SystemExit(f"Zoho refused the refresh token: {payload}")
    return payload["access_token"]


def zoho_records(token, module, date_from, date_to):
    """Every record in a module created in the range, paged (200 per page)."""
    api = os.environ.get("CD_ZOHO_API_DOMAIN", "https://www.zohoapis.com").rstrip("/")
    headers = {"Authorization": f"Zoho-oauthtoken {token}"}
    out, page = [], 1
    while True:
        params = {
            "per_page": 200,
            "page": page,
            "sort_by": "Created_Time",
            "sort_order": "desc",
            "fields": "id,Email,Last_Name,First_Name,Created_Time,Lead_Source,Company",
        }
        r = requests.get(f"{api}/crm/v6/{module}", headers=headers, params=params, timeout=90)
        if r.status_code == 204:
            break
        if r.status_code in (401, 403):
            return {"error": f"{r.status_code} {r.text[:300]}"}
        r.raise_for_status()
        data = r.json()
        recs = data.get("data", [])
        out.extend(recs)
        oldest = min((x.get("Created_Time") or "9999") for x in recs) if recs else ""
        if not data.get("info", {}).get("more_records") or oldest[:10] < date_from:
            break
        page += 1
        if page > 60:
            break
    return [x for x in out if date_from <= (x.get("Created_Time") or "")[:10] <= date_to]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="date_from", required=True)
    ap.add_argument("--to", dest="date_to", required=True)
    ap.add_argument("--out", default=None, help="directory to write the CSV and JSON into")
    ap.add_argument("--page-size", type=int, default=600,
                    help="entries fetched per form, newest first (default 600)")
    args = ap.parse_args()

    base = os.environ["CD_LIVE_URL"].rstrip("/")

    print(f"Gravity Forms entries {args.date_from} .. {args.date_to}")
    all_entries = []
    for fid, label in FORMS.items():
        rows = gf_entries(base, fid, args.date_from, args.date_to, args.page_size)
        print(f"  form {fid:>2} {label:<26} {len(rows):>4} entries")
        for e in rows:
            all_entries.append({
                "form_id": fid,
                "form": label,
                "entry_id": e.get("id"),
                "created": e.get("date_created"),
                "email": entry_email(e),
                "name": entry_name(e),
                "source_url": e.get("source_url", "") or "",
                "paid_click": bool(re.search(r"gclid=|gbraid=|wbraid=|msclkid=", e.get("source_url", "") or "")),
            })
    print(f"  {'':>2} {'TOTAL':<26} {len(all_entries):>4} entries")

    # widen the Zoho window: a lead can land a little either side of the entry
    z_from = (dt.date.fromisoformat(args.date_from) - dt.timedelta(days=2)).isoformat()
    z_to = (dt.date.fromisoformat(args.date_to) + dt.timedelta(days=2)).isoformat()

    print("\nZoho CRM")
    token = zoho_token()
    print("  access token obtained")
    zoho = {}
    for module in ("Leads", "Contacts", "Deals"):
        recs = zoho_records(token, module, z_from, z_to)
        if isinstance(recs, dict):
            print(f"  {module:<10} NOT READABLE: {recs['error']}")
            zoho[module] = []
            continue
        print(f"  {module:<10} {len(recs):>4} records created {z_from} .. {z_to}")
        zoho[module] = recs

    by_email = {}
    for module, recs in zoho.items():
        for r in recs:
            em = (r.get("Email") or "").strip().lower()
            if em:
                by_email.setdefault(em, []).append((module, r))

    matched, missing, no_email = [], [], []
    for e in all_entries:
        if not e["email"]:
            no_email.append(e)
            continue
        hits = by_email.get(e["email"])
        if hits:
            e["zoho"] = "; ".join(f"{m} {r.get('id')} @ {(r.get('Created_Time') or '')[:19]}" for m, r in hits)
            matched.append(e)
        else:
            e["zoho"] = ""
            missing.append(e)

    print("\n=== RESULT ===")
    print(f"entries in range          : {len(all_entries)}")
    print(f"  with a usable email     : {len(all_entries) - len(no_email)}")
    print(f"  no email field captured : {len(no_email)}")
    print(f"  found in Zoho           : {len(matched)}")
    print(f"  NOT found in Zoho       : {len(missing)}")

    from collections import Counter
    print("\nby form (entries / reached Zoho):")
    tot = Counter(e["form"] for e in all_entries)
    hit = Counter(e["form"] for e in matched)
    ne = Counter(e["form"] for e in no_email)
    for f in FORMS.values():
        print(f"  {f:<26} {tot[f]:>4} entries, {hit[f]:>4} in Zoho, {ne[f]:>3} had no email")

    if missing:
        print("\nEntries with an email that are NOT in Zoho:")
        for e in sorted(missing, key=lambda x: x["created"]):
            print(f"  form {e['form_id']:>2} entry {e['entry_id']:>6}  {e['created']}  {e['email']:<38} {e['name']}")

    if args.out:
        out_dir = pathlib.Path(args.out)
        out_dir.mkdir(parents=True, exist_ok=True)
        with (out_dir / "forms-to-zoho-reconciliation.csv").open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(["form_id", "form", "entry_id", "created", "email", "name",
                        "from_paid_click", "source_url", "in_zoho", "zoho_match"])
            for e in sorted(all_entries, key=lambda x: x["created"]):
                w.writerow([e["form_id"], e["form"], e["entry_id"], e["created"], e["email"] or "",
                            e["name"], "yes" if e["paid_click"] else "no", e["source_url"],
                            "yes" if e.get("zoho") else "no", e.get("zoho", "")])
        (out_dir / "zoho-records.json").write_text(
            json.dumps({k: v for k, v in zoho.items()}, indent=2), encoding="utf-8")
        print(f"\nwrote {out_dir / 'forms-to-zoho-reconciliation.csv'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
