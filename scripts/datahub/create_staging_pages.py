"""Create the insolvency data-hub pages on STAGING (idempotent).

Creates the page hierarchy the nested URLs need and captures the WP page ids:

    /data/                                  (slug: data,                parent: -)
      /data/company-insolvency/             (slug: company-insolvency,  parent: data)        [Data Hub Template]
        .../winding-up-petition-tracker/    (slug: winding-up-...,      parent: company-...) [Data Hub Template]
        .../company-dissolutions-vs-insolvencies/                                            [Data Hub Template]

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
        "slug": "data",
        "title": "Data",
        "parent": None,
        "template": "",
        "seo_title": "CompanyDebt Data",
        "meta": "CompanyDebt's UK company data products: official, citable statistics on insolvency, dissolutions and corporate distress.",
        "content": (
            "<!-- wp:paragraph --><p>CompanyDebt publishes citable UK company data drawn from official "
            "sources. Start with the "
            "<a href=\"/data/company-insolvency/\">UK Company Insolvency Data hub</a>.</p><!-- /wp:paragraph -->"
        ),
    },
    {
        "slug": "company-insolvency",
        "title": "UK Company Insolvency Data and Statistics",
        "parent": "data",
        "template": TEMPLATE,
        "seo_title": "UK Company Insolvency Data and Statistics",
        "meta": "Official, citable UK company insolvency data for journalists, accountants, lenders and company directors. Latest headline figures and a directory of every data page.",
        "content": "",
    },
    {
        "slug": "winding-up-petition-tracker",
        "title": "Winding-Up Petition Tracker (UK)",
        "parent": "company-insolvency",
        "template": TEMPLATE,
        "seo_title": "Winding-Up Petition Tracker (UK)",
        "meta": "A monthly count of winding-up petitions advertised against UK companies in The Gazette, with the trend and how many petitions convert into winding-up orders.",
        "content": "",
    },
    {
        "slug": "dissolutions-vs-insolvencies",
        "title": "Company Dissolutions vs Insolvencies (UK Data)",
        "parent": "company-insolvency",
        "template": TEMPLATE,
        "seo_title": "Company Dissolutions vs Insolvencies (UK Data)",
        "meta": "Most UK company closures are ordinary, solvent strike-offs, not insolvencies. The latest dissolution, incorporation and formal insolvency figures, set on a shared scale.",
        "content": "",
    },
    {
        "slug": "payment-practices-late-payment",
        "title": "Payment Practices & Late Payment (UK Data)",
        "parent": "company-insolvency",
        "template": TEMPLATE,
        "seo_title": "UK Payment Practices & Late Payment Data",
        "meta": "How slowly large UK companies pay their suppliers, the share of invoices paid late, and which sectors are slowest. Enrichment context from statutory Payment Practices Reporting, not insolvency data.",
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
