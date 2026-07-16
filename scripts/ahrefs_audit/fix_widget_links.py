"""Repoint redirecting links inside WP block widgets (footer link columns).

Two footer widgets account for ~820 of the audit's 'links to redirect'
warnings: they sit on every page, so one bad href becomes 410 warnings.

Matches on the EXACT href value, not a substring: '/liquidation/voluntary-liquidation/'
must not match '/liquidation/creditors-voluntary-liquidation/'.

Usage:
  python fix_widget_links.py            # dry run
  python fix_widget_links.py --apply
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from staging_edit import session, STAGING_URL  # noqa: E402

# Verified single-hop destinations (see Warning-3XX_redirect.csv).
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
HOSTS = ["https://www.companydebt.com", "https://comdebstage.wpengine.com", ""]

apply = "--apply" in sys.argv
s = session()

r = s.get(f"{STAGING_URL}/wp-json/wp/v2/widgets", params={"per_page": 100, "context": "edit"}, timeout=60)
r.raise_for_status()
widgets = r.json()
print(f"Scanned {len(widgets)} widgets  [{'APPLY' if apply else 'DRY RUN'}]\n")

total = 0
for w in widgets:
    inst = w.get("instance", {}).get("raw", {}) or {}
    content = inst.get("content", "") or ""
    if not content:
        continue
    modified, changes = content, []
    for old, new in REDIRECT_MAP.items():
        for host in HOSTS:
            for q in ('"', "'"):
                token = f"href={q}{host}{old}{q}"
                n = modified.count(token)
                if n:
                    modified = modified.replace(token, f"href={q}{new}{q}")
                    changes.append(f"{n}x {host}{old} -> {new}")
    if not changes:
        continue
    total += len(changes)
    print(f"  widget {w['id']}  (sidebar={w.get('sidebar')})")
    for c in changes:
        print(f"     {c}")
    if apply:
        payload = {"id": w["id"], "sidebar": w.get("sidebar"),
                   "instance": {"raw": {**inst, "content": modified}}}
        pr = s.post(f"{STAGING_URL}/wp-json/wp/v2/widgets/{w['id']}", json=payload,
                    headers={"Content-Type": "application/json"}, timeout=40)
        print(f"     PATCH {pr.status_code}" + ("" if pr.ok else f"  {pr.text[:200]}"))
    else:
        print("     (dry run)")
    print()

print(f"{total} link change(s) across widgets")
