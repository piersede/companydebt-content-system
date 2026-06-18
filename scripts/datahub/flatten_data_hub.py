"""One-off: flatten the data hub so /data/ IS the hub.

Moves the hub up a level and re-parents its children directly under /data/:

  BEFORE                                          AFTER
  /data/ (79845, thin landing)                    /data/ (79845, THE hub)
    /data/company-insolvency/ (79846, hub)          /data/winding-up-petition-tracker/   (79847)
      .../winding-up-petition-tracker/   (79847)    /data/dissolutions-vs-insolvencies/  (79848)
      .../dissolutions-vs-insolvencies/  (79848)    /data/payment-practices-late-payment/(79850)
      .../payment-practices-late-payment/(79850)    /data/uk-insolvency-statistics/      (77399, unchanged)

STRUCTURE only, idempotent:
  - re-parent 79847 / 79848 / 79850 -> 79845
  - 79845: parent 0, data-hub-template, hub title + Yoast/RankMath SEO
  - 79846: retire (status=draft) so /data/company-insolvency/ frees up for a 301

Content is pushed separately by build_page passthrough. Redirects, mu-plugin
deploy and cache purge are separate steps. STAGING ONLY.

Usage:
    python scripts/datahub/flatten_data_hub.py            # read-only dry-run
    python scripts/datahub/flatten_data_hub.py --apply    # execute
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from dotenv import load_dotenv  # noqa: E402

for c in [ROOT / ".env.local", ROOT / ".env"]:
    if c.exists():
        load_dotenv(c)
        break

from wp_publish import get_credentials, create_authenticated_session  # noqa: E402

HUB_ID = 79845          # /data/  -> becomes the hub
RETIRE_ID = 79846       # /data/company-insolvency/ -> retire (draft)
CHILD_IDS = [79847, 79848, 79850]  # re-parent to HUB_ID

TEMPLATE = "templates/data-hub-template.php"
HUB_TITLE = "UK Company Insolvency Data and Statistics"
HUB_META = (
    "Official, citable UK company insolvency data for journalists, accountants, "
    "lenders and company directors. Latest headline figures and a directory of "
    "every data page."
)


def fetch(session, api_base, pid):
    r = session.get(f"{api_base}/pages/{pid}", params={"context": "edit"}, timeout=30)
    r.raise_for_status()
    return r.json()


def summary(p):
    title = (p.get("title") or {}).get("raw") or (p.get("title") or {}).get("rendered", "")
    return (f"id={p['id']} slug={p.get('slug')!r} status={p.get('status')} "
            f"parent={p.get('parent')} template={p.get('template') or 'default'!r} "
            f"link={p.get('link')} title={title!r}")


def post(session, api_base, pid, payload, apply):
    if not apply:
        print(f"  [DRY] would POST /pages/{pid}: {payload}")
        return None
    r = session.post(f"{api_base}/pages/{pid}", json=payload, timeout=30)
    if r.status_code not in (200, 201):
        print(r.text[:400])
        sys.exit(f"Failed POST /pages/{pid}: HTTP {r.status_code}")
    print(f"  [OK ] POST /pages/{pid}: {list(payload.keys())}")
    return r.json()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="execute (default: dry-run)")
    args = ap.parse_args()

    creds = get_credentials(prod=False)
    session, api_base = create_authenticated_session(creds)
    session.headers["Content-Type"] = "application/json"

    who = session.get(f"{api_base}/users/me", timeout=30)
    if who.status_code != 200:
        sys.exit(f"Auth failed ({who.status_code}). Check .env staging creds.")
    print(f"Connected: {who.json().get('name')} @ {api_base}")
    print(f"Mode: {'APPLY' if args.apply else 'DRY-RUN (read-only)'}\n")

    print("BEFORE:")
    for pid in [HUB_ID, RETIRE_ID, *CHILD_IDS]:
        print("  " + summary(fetch(session, api_base, pid)))
    print()

    # 1) Re-parent the children directly under /data/.
    print("Re-parent children -> /data/ (79845):")
    for pid in CHILD_IDS:
        post(session, api_base, pid, {"parent": HUB_ID}, args.apply)

    # 2) Promote /data/ to the hub: top-level, hub template, hub title + SEO.
    print("\nPromote /data/ (79845) to the hub:")
    post(session, api_base, HUB_ID, {
        "parent": 0,
        "slug": "data",
        "title": HUB_TITLE,
        "template": TEMPLATE,
        "meta": {
            "_yoast_wpseo_title": HUB_TITLE,
            "_yoast_wpseo_metadesc": HUB_META,
            "rank_math_title": HUB_TITLE,
            "rank_math_description": HUB_META,
        },
    }, args.apply)

    # 3) Retire the old hub page so /data/company-insolvency/ can 301.
    print("\nRetire /data/company-insolvency/ (79846 -> draft):")
    post(session, api_base, RETIRE_ID, {"status": "draft"}, args.apply)

    if args.apply:
        print("\nAFTER:")
        for pid in [HUB_ID, RETIRE_ID, *CHILD_IDS]:
            print("  " + summary(fetch(session, api_base, pid)))

    print("\nNext: build_page --publish (content), qppr 301s, mu-plugin deploy, cache purge.")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
