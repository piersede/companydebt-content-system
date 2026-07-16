"""Map each genuinely-dead external URL back to the pages that cite it."""
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from parse_export import read_export

D = Path(sys.argv[1])
verdicts = json.load(open(sys.argv[2], encoding="utf-8"))
dead = {r["url"] for r in verdicts if r["verdict"] == "GENUINELY_DEAD"}

# The -links files carry Source URL -> Target URL edges.
edges = defaultdict(set)
for fname in ["Error-indexable-Page_has_links_to_broken_page-links.csv",
              "Notice-External_4XX-links.csv"]:
    p = D / fname
    if not p.exists():
        continue
    for r in read_export(p):
        tgt = r.get("Target URL", "")
        if tgt in dead:
            edges[tgt].add((r.get("Source URL", ""), r.get("Anchor", "").strip()))

print(f"Dead targets: {len(dead)}  |  located on pages: {sum(len(v) for v in edges.values())}\n")
for tgt in sorted(dead):
    srcs = edges.get(tgt, set())
    print("=" * 78)
    print(f"DEAD: {tgt}")
    if not srcs:
        print("   (no source page recorded in export)")
    for src, anchor in sorted(srcs):
        print(f"   cited on: {src}")
        print(f"     anchor: {anchor[:80]!r}")
    print()
