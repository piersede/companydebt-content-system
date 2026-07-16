import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from parse_export import read_export

D = Path(sys.argv[1])
rows = read_export(D / "Warning-3XX_redirect-links.csv")
print(f"3XX redirect inlink rows: {len(rows)}")
print("cols:", list(rows[0].keys()) if rows else "-")

print("\n--- redirect targets by how many pages link to them ---")
for tgt, n in Counter(r["Target URL"] for r in rows).most_common(15):
    print(f"{n:>5}  {tgt}")

print("\n--- ANCHOR TEXT used for the two big ones (tells us if it's nav/footer) ---")
for big in ["https://www.companydebt.com/uk-insolvency-statistics/",
            "https://www.companydebt.com/what-is-a-pre-pack-administration/"]:
    sub = [r for r in rows if r["Target URL"] == big]
    print(f"\n{big}  ({len(sub)} inlinks)")
    for anchor, n in Counter(r.get("Anchor", "").strip() for r in sub).most_common(6):
        print(f"   {n:>4}x  anchor={anchor[:70]!r}")
    print("   sample source pages:")
    for r in sub[:4]:
        print(f"      {r['Source URL'][:88]}")

print("\n--- nofollow / link type breakdown ---")
for k in ("Link type", "Is nofollow"):
    if rows and k in rows[0]:
        print(f"  {k}: {dict(Counter(r[k] for r in rows))}")
