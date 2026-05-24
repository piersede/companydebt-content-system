"""
Two-part audit:
1. Draft-status destinations — links in _all/ pointing to non-published pages
2. Inbound link coverage — which pages have zero or very few inbound links
"""

import json
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
ALL_DIR = ROOT / "internal-links" / "_all"
INVENTORY = ROOT / "staging_page_inventory_fresh.json"

inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))

# Normalise: strip trailing slash for comparison
def norm(path):
    return "/" + path.strip("/") + "/"

inventory_norm = {norm(k): v for k, v in inventory.items()}

# Build link map: source_slug -> [dest_path, ...]
link_map = defaultdict(list)  # dest -> [source_slugs]
source_links = defaultdict(list)  # source_slug -> [dest_paths]

HREF_RE = re.compile(r'href="(/[^"#?]*)"')

for f in sorted(ALL_DIR.glob("*.txt")):
    slug = f.stem
    text = f.read_text(encoding="utf-8")
    for m in HREF_RE.finditer(text):
        dest = norm(m.group(1))
        link_map[dest].append(slug)
        source_links[slug].append(dest)

# ── Part 1: Draft-status destinations ─────────────────────────────────────────
print("=" * 70)
print("PART 1: Links pointing to non-published pages")
print("=" * 70)

draft_issues = []
for dest, sources in sorted(link_map.items()):
    entry = inventory_norm.get(dest)
    if entry and entry["status"] != "publish":
        draft_issues.append((dest, entry["status"], sources))

if draft_issues:
    for dest, status, sources in draft_issues:
        print(f"\n  {dest}  [{status}]")
        for s in sources:
            print(f"    <- {s}")
else:
    print("\n  None — all linked destinations are published.\n")

# ── Part 2: Inbound link coverage ─────────────────────────────────────────────
print()
print("=" * 70)
print("PART 2: Published pages with zero or very few inbound links")
print("=" * 70)

# Only care about published pages that have a corresponding _all/ file
# (i.e. pages we're actively managing content for)
managed_slugs = {f.stem for f in ALL_DIR.glob("*.txt")}

# All published page paths
published = {norm(k): v for k, v in inventory.items() if v["status"] == "publish"}

print(f"\n  Total published pages in inventory: {len(published)}")
print(f"  Pages with _all/ content files: {len(managed_slugs)}")

# For each published path, count inbound links from managed files
inbound_counts = []
for path, entry in sorted(published.items()):
    slug = entry["slug"]
    count = len(link_map.get(path, []))
    inbound_counts.append((count, path, slug, entry.get("type", "?")))

inbound_counts.sort()

print("\n  Pages with 0 inbound links (from managed _all/ files):")
zero = [(p, s, t) for c, p, s, t in inbound_counts if c == 0]
# Filter to only pages that have _all/ files (skip utility/boilerplate pages)
zero_managed = [(p, s, t) for p, s, t in zero if s in managed_slugs]
for p, s, t in zero_managed:
    print(f"    {p}  ({t})")

print(f"\n  Pages with exactly 1 inbound link:")
one_managed = [(p, s, t) for c, p, s, t in inbound_counts
               if c == 1 and s in managed_slugs]
for p, s, t in one_managed:
    sources = link_map.get(p, [])
    print(f"    {p}  <- {sources[0]}")

print(f"\n  Pages with exactly 2 inbound links:")
two_managed = [(p, s, t) for c, p, s, t in inbound_counts
               if c == 2 and s in managed_slugs]
for p, s, t in two_managed:
    sources = link_map.get(p, [])
    print(f"    {p}  <- {', '.join(sources)}")

print(f"\n  Summary: 0 inbound={len(zero_managed)}  1 inbound={len(one_managed)}  2 inbound={len(two_managed)}")

# Also show top 10 most-linked pages for reference
print("\n  Top 10 most-linked pages (for context):")
for c, p, s, t in reversed(inbound_counts[-10:]):
    print(f"    {c:3d}  {p}")
