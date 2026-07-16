"""Find (and optionally fix) WP nav-menu items pointing at redirecting URLs.

Ahrefs reported ~820 'links to redirect' warnings from just two URLs, each with
410 inlinks and a single consistent anchor - the signature of a nav menu, not
in-article links. Fixing the menu item fixes every page at once.

Usage:
  python fix_menu_links.py                 # report
  python fix_menu_links.py --apply         # rewrite matching menu items
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from staging_edit import session, STAGING_URL  # noqa: E402

# old redirecting URL -> verified final destination (single hop, 200)
REDIRECT_MAP = {
    "/uk-insolvency-statistics/": "/data/uk-insolvency-statistics/",
    "/what-is-a-pre-pack-administration/": "/company-rescue-solutions/pre-packs/",
    "/business-debt-advice/": "/advice/get-free-business-debt-advice/",
    "/liquidation-hub/": "/liquidation/",
    "/liquidation/voluntary-liquidation/": "/liquidation/creditors-voluntary-liquidation/",
    "/what-is-wrongful-trading/": "/insolvency/what-is-wrongful-trading/",
    "/faqs/what-is-wrongful-trading/": "/insolvency/what-is-wrongful-trading/",
    "/liquidation/liquidate-registered-charity/": "/liquidation/",
}

apply = "--apply" in sys.argv
s = session()


def all_menu_items():
    items, page = [], 1
    while True:
        r = s.get(f"{STAGING_URL}/wp-json/wp/v2/menu-items",
                  params={"per_page": 100, "page": page, "context": "edit"}, timeout=60)
        if r.status_code != 200:
            break
        batch = r.json()
        if not batch:
            break
        items += batch
        if len(batch) < 100:
            break
        page += 1
    return items


items = all_menu_items()
print(f"Scanned {len(items)} menu items\n")

hits = []
for it in items:
    url = (it.get("url") or "")
    for old, new in REDIRECT_MAP.items():
        # match on path so staging/live host differences do not matter
        if url.rstrip("/") .endswith(old.rstrip("/")) and old.strip("/"):
            # avoid matching /liquidation/ inside /liquidation/voluntary-liquidation/
            from urllib.parse import urlsplit
            if urlsplit(url).path.rstrip("/") != old.rstrip("/"):
                continue
            hits.append((it, old, new))
            break

if not hits:
    print("No menu items point at redirecting URLs.")
for it, old, new in hits:
    print(f"  menu-item {it['id']:<6} menu={it.get('menus')}  title={it.get('title',{}).get('rendered','')!r}")
    print(f"     {it['url']}\n  -> {new}")
    if apply:
        r = s.post(f"{STAGING_URL}/wp-json/wp/v2/menu-items/{it['id']}",
                   json={"url": new}, headers={"Content-Type": "application/json"}, timeout=40)
        print(f"     PATCH {r.status_code}")
    else:
        print("     (dry run)")
    print()
print(f"{len(hits)} menu item(s) affected")
