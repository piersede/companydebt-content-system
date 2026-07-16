"""Read-only dump of the Quick Redirects (qppr) rule table from staging.

Rules live in the `quickppr_redirects` option, not in the repo, so they are
invisible to grep. This scrapes the plugin's admin screen with the existing
authenticated staging session. Read-only: it never posts the form.

Usage: python scripts/ahrefs_audit/dump_qppr.py [filter-substring]
"""
import html
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from staging_edit import session, STAGING_URL  # noqa: E402

needle = sys.argv[1].lower() if len(sys.argv) > 1 else None

s = session()
r = s.get(f"{STAGING_URL}/wp-admin/admin.php", params={"page": "redirect-updates"}, timeout=60)
print(f"HTTP {r.status_code}  {len(r.text)} bytes\n")

# qppr renders rows as paired inputs: qppr_redirect[old][] / [new][]
pairs = re.findall(
    r'name=["\']qppr_redirect\[old\]\[\]["\'][^>]*value=["\']([^"\']*)["\'][\s\S]{0,400}?'
    r'name=["\']qppr_redirect\[new\]\[\]["\'][^>]*value=["\']([^"\']*)["\']',
    r.text)
if not pairs:
    # fallback: generic two-column textarea/table render
    pairs = re.findall(r'value=["\']([^"\']*?)["\'][^>]*>\s*</td>\s*<td[^>]*>\s*<input[^>]*value=["\']([^"\']*?)["\']', r.text)

print(f"parsed {len(pairs)} rule(s)\n")
shown = 0
for old, new in pairs:
    old, new = html.unescape(old), html.unescape(new)
    if needle and needle not in old.lower() and needle not in new.lower():
        continue
    print(f"  {old}\n    -> {new}\n")
    shown += 1
print(f"shown: {shown}")
if not pairs:
    print("\n(no rules parsed - dumping a sample of the page for inspection)")
    txt = re.sub(r"<script[\s\S]*?</script>", "", r.text)
    m = re.search(r"(qppr_redirect[\s\S]{0,1500})", txt)
    print(m.group(1)[:1500] if m else txt[:1200])
