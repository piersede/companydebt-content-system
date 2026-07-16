import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from parse_export import read_export

D = Path(sys.argv[1])

print("=" * 70, "\nSTRUCTURED DATA ERRORS\n", "=" * 70)
sd = read_export(D / "Notice-Structured_data_has_schema.org_validation_error.csv")
print("cols:", list(sd[0].keys()) if sd else "none")
errcol = next((c for c in sd[0] if "rror" in c and c != "PR"), None)
print("errcol:", errcol)
for e, n in Counter(r.get(errcol, "") for r in sd).most_common(15):
    print(f"{n:>5}  {e[:160]}")

print("\n", "=" * 70, "\nNOINDEX PAGES (sample)\n", "=" * 70)
ni = read_export(D / "Warning-Noindex_page.csv")
print("cols:", list(ni[0].keys()) if ni else "none")
for r in ni[:15]:
    print("  ", r["URL"][:100], "| traffic:", r.get("Organic traffic"))

print("\n", "=" * 70, "\nINDEXABLE PAGE NOT IN SITEMAP\n", "=" * 70)
for r in read_export(D / "Notice-Indexable_page_not_in_sitemap.csv"):
    print("  ", r["URL"][:110])

print("\n", "=" * 70, "\nCSS BROKEN\n", "=" * 70)
for r in read_export(D / "Warning-CSS_broken.csv"):
    print("  ", {k: v[:90] for k, v in list(r.items())[:6]})

print("\n", "=" * 70, "\nTITLE / META ISSUES\n", "=" * 70)
for f in ["Warning-indexable-Title_too_long.csv", "Warning-indexable-Title_too_short.csv",
          "Notice-Title_too_short.csv", "Warning-indexable-Meta_description_too_long.csv",
          "Notice-Meta_description_too_short.csv"]:
    rows = read_export(D / f)
    print(f"\n-- {f} ({len(rows)})")
    for r in rows:
        print("   ", r["URL"][:95])

print("\n", "=" * 70, "\n3XX PAGE RECEIVES ORGANIC TRAFFIC\n", "=" * 70)
for r in read_export(D / "Error-3XX_page_receives_organic_traffic.csv"):
    print("  ", {k: v[:80] for k, v in r.items() if k in ("URL", "Redirect URL", "Organic traffic", "HTTP status code")})
