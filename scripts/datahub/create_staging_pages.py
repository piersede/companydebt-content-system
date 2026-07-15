"""Create the insolvency data-hub pages on STAGING (idempotent).

Creates the page hierarchy the nested URLs need and captures the WP page ids:

    /data/                                  (slug: data,  parent: -)   [Data Hub Template]  <- the hub
      /data/winding-up-petition-tracker/    (slug: winding-up-...,       parent: data)      [Data Hub Template]
      /data/dissolutions-vs-insolvencies/   (slug: dissolutions-vs-...,  parent: data)      [Data Hub Template]
      /data/payment-practices-late-payment/ (slug: payment-practices-..., parent: data)     [Data Hub Template]

    NOTE: this reconciles a FRESH or already-flat tree. It cannot re-parent
    children that still hang off the retired /data/company-insolvency/ page
    (find_by_slug matches on the new parent) — that one-off move was done by
    scripts/datahub/flatten_data_hub.py.

Sets the page template, parent and SEO title/meta-description at creation time
(the generic publisher does not touch those). Content is left minimal here; the
real dashboard markup is pushed afterwards by build_page.py passthrough.

Re-running is safe: existing pages (matched by slug) are reused, and their
parent/template are corrected if missing. STAGING ONLY.

Usage:
    python scripts/datahub/create_staging_pages.py          # create / reconcile
    python scripts/datahub/create_staging_pages.py --dry-run
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

TEMPLATE = "templates/data-hub-template.php"

# Page tree, parents first. Each: slug, title, parent_slug (None=top level),
# template (""=default), seo_title, meta_description, content.
PAGES = [
    {
        # The hub itself. /data/ carries the full data-hub dashboard; its
        # content is pushed by build_page.py passthrough (drafts/79845_data.html),
        # not set here.
        "slug": "data",
        "title": "UK Company Insolvency Data and Statistics",
        "parent": None,
        "template": TEMPLATE,
        "seo_title": "UK Company Insolvency Data and Statistics",
        "meta": "Official, citable UK company insolvency data for journalists, accountants, lenders and company directors. Latest headline figures and a directory of every data page.",
        "content": "",
    },
    {
        "slug": "winding-up-petition-tracker",
        "title": "Winding-Up Petition Tracker (UK)",
        "parent": "data",
        "template": TEMPLATE,
        "seo_title": "Winding-Up Petition Tracker (UK)",
        "meta": "A monthly count of winding-up petitions advertised against UK companies in The Gazette, with the trend and how many petitions convert into winding-up orders.",
        "content": "",
    },
    {
        "slug": "dissolutions-vs-insolvencies",
        "title": "Company Dissolutions vs Insolvencies (UK Data)",
        "parent": "data",
        "template": TEMPLATE,
        "seo_title": "Company Dissolutions vs Insolvencies (UK Data)",
        "meta": "Most UK company closures are ordinary, solvent strike-offs, not insolvencies. The latest dissolution, incorporation and formal insolvency figures, set on a shared scale.",
        "content": "",
    },
    {
        "slug": "payment-practices-late-payment",
        "title": "Payment Practices & Late Payment (UK Data)",
        "parent": "data",
        "template": TEMPLATE,
        "seo_title": "UK Payment Practices & Late Payment Data",
        "meta": "How slowly large UK companies pay their suppliers, the share of invoices paid late, and which sectors are slowest. Enrichment context from statutory Payment Practices Reporting, not insolvency data.",
        "content": "",
    },
    {
        "slug": "cvl-statistics",
        "title": "CVL Statistics (UK)",
        "parent": "data",
        "template": TEMPLATE,
        "seo_title": "CVL Statistics (UK): Creditors' Voluntary Liquidations",
        "meta": "UK creditors' voluntary liquidation (CVL) statistics: monthly volumes since 2000, the share of all company insolvencies and the rate per 10,000 companies. From the Insolvency Service.",
        "content": "",
    },
    {
        "slug": "compulsory-liquidation-statistics",
        "title": "Compulsory Liquidation Statistics (UK)",
        "parent": "data",
        "template": TEMPLATE,
        "seo_title": "Compulsory Liquidation Statistics (UK)",
        "meta": "UK compulsory liquidation statistics: monthly court-ordered winding-up volumes since 2000, the share of all company insolvencies and the rate per 10,000 companies. From the Insolvency Service.",
        "content": "",
    },
    {
        "slug": "administration-statistics",
        "title": "Administration Statistics (UK)",
        "parent": "data",
        "template": TEMPLATE,
        "seo_title": "Company Administration Statistics (UK)",
        "meta": "UK company administration statistics: monthly volumes since 2000, the share of all company insolvencies and the rate per 10,000 companies. From the Insolvency Service.",
        "content": "",
    },
    {
        "slug": "company-insolvencies-by-sector",
        "title": "Company Insolvencies by Sector (UK Data)",
        "parent": "data",
        "template": TEMPLATE,
        "seo_title": "UK Company Insolvencies by Sector",
        "meta": "UK company insolvencies by industry sector: which sectors have the most, annual trends since 2016 and the latest 12-month breakdown across all SIC sections. From the Insolvency Service.",
        "content": "",
    },
    {
        "slug": "construction-insolvency-statistics",
        "title": "Construction Insolvency Statistics (UK)",
        "parent": "data",
        "template": TEMPLATE,
        "seo_title": "Construction Insolvency Statistics (UK)",
        "meta": "UK construction insolvency statistics: company insolvencies in construction since 2016, the trend, sub-sector breakdown and construction's share of all company insolvencies.",
        "content": "",
    },
    {
        "slug": "furniture-insolvency-statistics",
        "title": "Furniture Manufacturing Insolvency Statistics (UK)",
        "parent": "data",
        "template": TEMPLATE,
        "seo_title": "Furniture Manufacturing Insolvency Statistics (UK)",
        "meta": "UK furniture manufacturing insolvency statistics: company insolvencies among furniture manufacturers since 2016, the monthly trend since 2023 and the sector's share of all company insolvencies.",
        "content": "",
    },
    {
        "slug": "restaurant-insolvency-statistics",
        "title": "Restaurant Insolvency Statistics (UK)",
        "parent": "data",
        "template": TEMPLATE,
        "seo_title": "Restaurant Insolvency Statistics (UK)",
        "meta": "UK restaurant insolvency statistics: company insolvencies among restaurants and mobile food service businesses, year-to-date, rolling 12-month and annual figures.",
        "content": "",
    },
    {
        "slug": "road-haulage-insolvency-statistics",
        "title": "Road Haulage Insolvency Statistics (UK)",
        "parent": "data",
        "template": TEMPLATE,
        "seo_title": "Road Haulage Insolvency Statistics (UK)",
        "meta": "UK road haulage insolvency statistics: company insolvencies among freight transport and removal firms, year-to-date, rolling 12-month and annual figures.",
        "content": "",
    },
    {
        "slug": "recruitment-agency-insolvency-statistics",
        "title": "Recruitment Agency Insolvency Statistics (UK)",
        "parent": "data",
        "template": TEMPLATE,
        "seo_title": "Recruitment Agency Insolvency Statistics (UK)",
        "meta": "UK recruitment agency insolvency statistics: company insolvencies among permanent-placement recruitment agencies, year-to-date, rolling 12-month and annual figures.",
        "content": "",
    },
    {
        "slug": "temporary-staffing-agency-insolvency-statistics",
        "title": "Temporary Staffing Agency Insolvency Statistics (UK)",
        "parent": "data",
        "template": TEMPLATE,
        "seo_title": "Temporary Staffing Agency Insolvency Statistics (UK)",
        "meta": "UK temporary staffing agency insolvency statistics: company insolvencies among temp and agency staffing businesses, year-to-date, rolling 12-month and annual figures.",
        "content": "",
    },
    {
        "slug": "motor-vehicle-repair-insolvency-statistics",
        "title": "Motor Vehicle Repair Insolvency Statistics (UK)",
        "parent": "data",
        "template": TEMPLATE,
        "seo_title": "Motor Vehicle Repair Insolvency Statistics (UK)",
        "meta": "UK motor vehicle repair insolvency statistics: company insolvencies among garages and repair workshops, year-to-date, rolling 12-month and annual figures.",
        "content": "",
    },
    {
        "slug": "cleaning-company-insolvency-statistics",
        "title": "Cleaning Company Insolvency Statistics (UK)",
        "parent": "data",
        "template": TEMPLATE,
        "seo_title": "Cleaning Company Insolvency Statistics (UK)",
        "meta": "UK cleaning company insolvency statistics: company insolvencies among commercial and industrial cleaning contractors, year-to-date, rolling 12-month and annual figures.",
        "content": "",
    },
    {
        "slug": "hotel-insolvency-statistics",
        "title": "Hotel Insolvency Statistics (UK)",
        "parent": "data",
        "template": TEMPLATE,
        "seo_title": "Hotel Insolvency Statistics (UK)",
        "meta": "UK hotel insolvency statistics: company insolvencies among hotels and similar accommodation, year-to-date, rolling 12-month and annual figures.",
        "content": "",
    },
]


def find_by_slug(session, api_base, slug, parent_id=None):
    r = session.get(f"{api_base}/pages", params={"slug": slug, "status": "any", "context": "edit"}, timeout=30)
    r.raise_for_status()
    for p in r.json():
        if parent_id is None or p.get("parent") == parent_id:
            return p
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    creds = get_credentials(prod=False)
    session, api_base = create_authenticated_session(creds)
    session.headers["Content-Type"] = "application/json"

    whoami = session.get(f"{api_base}/users/me")
    if whoami.status_code != 200:
        sys.exit(f"Auth failed ({whoami.status_code}). Check .env staging creds.")
    print(f"Connected: {whoami.json().get('name')} @ {api_base}")

    ids: dict[str, int] = {}
    for spec in PAGES:
        parent_id = ids.get(spec["parent"], 0) if spec["parent"] else 0
        existing = find_by_slug(session, api_base, spec["slug"], parent_id if spec["parent"] else None)

        payload = {
            "title": spec["title"],
            "slug": spec["slug"],
            "status": "publish",
            "parent": parent_id,
            "template": spec["template"],
            "meta": {
                "_yoast_wpseo_title": spec["seo_title"],
                "_yoast_wpseo_metadesc": spec["meta"],
                "rank_math_title": spec["seo_title"],
                "rank_math_description": spec["meta"],
            },
        }
        if spec["content"]:
            payload["content"] = spec["content"]

        if args.dry_run:
            print(f"  [{'EXISTS' if existing else 'CREATE'}] {spec['slug']} (parent={parent_id}, template={spec['template'] or 'default'})")
            if existing:
                ids[spec["slug"]] = existing["id"]
            else:
                ids[spec["slug"]] = -1
            continue

        if existing:
            # Reconcile parent + template + meta without clobbering content.
            resp = session.post(f"{api_base}/pages/{existing['id']}", json=payload)
            action = "reconciled"
        else:
            resp = session.post(f"{api_base}/pages", json=payload)
            action = "created"

        if resp.status_code not in (200, 201):
            print(resp.text[:400])
            sys.exit(f"Failed to {action} {spec['slug']}: HTTP {resp.status_code}")
        data = resp.json()
        ids[spec["slug"]] = data["id"]
        print(f"  {action:10} {spec['slug']:38} id={data['id']:>6}  {data.get('link','')}")

    print("\nPAGE IDS:")
    for slug, pid in ids.items():
        print(f"  {slug} = {pid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
