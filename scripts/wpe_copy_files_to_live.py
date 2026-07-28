"""Copy staging FILES ONLY to production via the WP Engine API.

This is the scripted equivalent of the portal's "Copy environment" with
"file system only" selected. It never touches the database.

Why this script exists rather than a raw curl: the API's ``include_db``
defaults to **true**. A POST to /install_copy that simply omits ``custom_options``
copies the full database and wipes every Gravity Forms entry, user account and
comment created on live since the previous copy. That destroyed roughly 160
enquiries between 23 March and 28 July 2026. This script hard-codes
``include_db: false``, refuses to send ``db_tables`` at all, and asserts both
before the request leaves.

Credentials (.env): WPENGINE_API_USER + WPENGINE_API_PASSWORD, generated
together in the WP Engine portal under Profile > API Access. Both halves are
required; the username alone returns "Bad Credentials".

Usage:
    python scripts/wpe_copy_files_to_live.py                 # dry run, shows the plan
    python scripts/wpe_copy_files_to_live.py --confirm       # actually copies
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys

import requests
from dotenv import load_dotenv

ROOT = pathlib.Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
API = "https://api.wpengineapi.com/v1"


def auth() -> tuple[str, str]:
    user = os.environ.get("WPENGINE_API_USER") or os.environ.get("WPENGINE_API_KEY")
    password = os.environ.get("WPENGINE_API_PASSWORD")
    if not user or not password:
        sys.exit(
            "Missing WP Engine API credentials.\n"
            "  WPENGINE_API_USER     : " + ("set" if user else "MISSING") + "\n"
            "  WPENGINE_API_PASSWORD : " + ("set" if password else "MISSING") + "\n"
            "Generate both in the WP Engine portal: Profile > API Access > Generate\n"
            "credentials, then add them to .env. The username on its own gives a 401."
        )
    return user, password


def get(path: str) -> dict:
    r = requests.get(API + path, auth=auth(), timeout=45)
    if r.status_code == 401:
        sys.exit("401 Bad Credentials from WP Engine. Check WPENGINE_API_USER/PASSWORD in .env.")
    r.raise_for_status()
    return r.json()


def find_installs(source_name: str, dest_name: str) -> tuple[dict, dict]:
    """Return the (source, destination) installs, matched by name.

    This API user can see 14 installs across several sites, so the names are
    explicit rather than inferred from the environment field.
    """
    installs = get("/installs?limit=100").get("results", [])

    def pick(name: str) -> dict:
        for i in installs:
            if i["name"] == name:
                return i
        listing = [f"{i['name']} ({i.get('environment')})" for i in installs]
        sys.exit(f"No install named '{name}'. Visible installs:\n  " + "\n  ".join(listing))

    return pick(source_name), pick(dest_name)


def primary_domain(install_id: str) -> str:
    domains = get(f"/installs/{install_id}/domains?limit=50").get("results", [])
    for d in domains:
        if d.get("primary"):
            return d["name"]
    return "?"


def check_destination(install: dict) -> str:
    """Refuse to write to anything that isn't the site named in CD_LIVE_URL."""
    expected = os.environ.get("CD_LIVE_URL", "").split("//")[-1].strip("/")
    actual = primary_domain(install["id"])
    if not expected:
        sys.exit("CD_LIVE_URL is not set in .env; cannot verify the destination site.")
    if actual != expected:
        sys.exit(
            f"Destination check FAILED.\n"
            f"  install '{install['name']}' serves : {actual}\n"
            f"  CD_LIVE_URL expects              : {expected}\n"
            "Refusing to copy files onto a site that isn't the one in .env."
        )
    return actual


def main() -> None:
    ap = argparse.ArgumentParser(description="Copy staging files (never the database) to production.")
    ap.add_argument("--confirm", action="store_true", help="actually perform the copy")
    ap.add_argument("--notify", default="", help="comma-separated emails to notify on completion")
    ap.add_argument("--source", default="comdebstage", help="source install name (default: comdebstage)")
    ap.add_argument("--destination", default="companydebtltd", help="destination install name (default: companydebtltd)")
    args = ap.parse_args()

    staging, production = find_installs(args.source, args.destination)
    domain = check_destination(production)
    print(f"source      : {staging['name']:<16} {staging.get('environment'):<12} {staging['id']}")
    print(f"destination : {production['name']:<16} {production.get('environment'):<12} {production['id']}")
    print(f"              serves {domain}  (matches CD_LIVE_URL)")

    payload = {
        "source_environment_id": staging["id"],
        "destination_environment_id": production["id"],
        "custom_options": {"include_files": True, "include_db": False},
    }
    if args.notify:
        payload["notification_emails"] = [e.strip() for e in args.notify.split(",") if e.strip()]

    # Belt and braces: the whole point of this script is that these hold.
    opts = payload["custom_options"]
    assert opts["include_db"] is False, "include_db must be False"
    assert "db_tables" not in opts, "db_tables must never be sent"
    assert opts["include_files"] is True, "include_files must be True"

    print("\npayload:")
    print(json.dumps(payload, indent=2))
    print("\nfiles: YES   database: NO   (no table is copied, read or replaced)")

    if not args.confirm:
        print("\nDRY RUN. Nothing sent. Re-run with --confirm to perform the copy.")
        return

    r = requests.post(API + "/install_copy", auth=auth(), json=payload, timeout=60)
    print(f"\nHTTP {r.status_code}")
    print(r.text[:1000])
    r.raise_for_status()
    print("\nCopy queued. It runs asynchronously; WP Engine emails on completion.")
    print("Then: purge Cloudflare, and run scripts/check_live_form_entries.py to confirm")
    print("the newest entry date has NOT moved.")


if __name__ == "__main__":
    main()
