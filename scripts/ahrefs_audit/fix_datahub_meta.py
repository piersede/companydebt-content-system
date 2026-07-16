"""Shorten the over-long data-hub meta descriptions at their real source.

The /data/ pages do NOT take their meta description from post meta. The
cd-insolvency-data-hub mu-plugin registers a `wpseo_metadesc` filter and
serves a hardcoded per-slug value, so it is the single source of truth
(the plugin's own comment says as much). Writing post meta or dropping the
Yoast indexable row changes nothing - verified 2026-07-16.

Rewrites only the `desc` for the 8 slugs Ahrefs flagged as over-long.
Dry run by default.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from meta_desc_fixes import FIXES, LIMIT  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
PLUGIN = ROOT / "mu-plugins" / "cd-insolvency-data-hub.php"

apply = "--apply" in sys.argv
src = PLUGIN.read_text(encoding="utf-8")
orig = src
changed = 0

for slug, new_desc in FIXES.items():
    if len(new_desc) > LIMIT:
        sys.exit(f"REFUSING: {slug} is {len(new_desc)} chars (> {LIMIT})")
    # PHP single-quoted string: escape backslash then single quote.
    php_desc = new_desc.replace("\\", "\\\\").replace("'", "\\'")
    # Find the slug's array block, then its desc line within it.
    pat = re.compile(
        r"('" + re.escape(slug) + r"'\s*=>\s*array\(\s*\n\s*'title'\s*=>\s*'(?:[^'\\]|\\.)*',\s*\n\s*'desc'\s*=>\s*')((?:[^'\\]|\\.)*)(')"
    )
    m = pat.search(src)
    if not m:
        print(f"  !! no match for {slug}")
        continue
    old_desc = m.group(2)
    # Unescape only for the length report.
    old_len = len(old_desc.replace("\\'", "'").replace("\\\\", "\\"))
    src = src[:m.start(2)] + php_desc + src[m.end(2):]
    changed += 1
    print(f"  {slug}\n     {old_len:>4} -> {len(new_desc):<4} chars")

print(f"\n{changed}/{len(FIXES)} descriptions rewritten")
if src == orig:
    print("no change")
elif apply:
    PLUGIN.write_text(src, encoding="utf-8")
    print(f"WROTE {PLUGIN}")
else:
    print("\nDry run. Pass --apply to write, then SFTP the plugin to staging.")
