import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from parse_export import read_export

D = Path(sys.argv[1])


def show(fname, cols, limit=30, title=None):
    p = D / fname
    if not p.exists():
        print(f"!! missing {fname}")
        return
    rows = read_export(p)
    print(f"\n{'=' * 70}\n{title or fname}  ({len(rows)} rows)\n{'=' * 70}")
    for r in rows[:limit]:
        print(" | ".join(str(r.get(c, ""))[:90] for c in cols))
    if len(rows) > limit:
        print(f"... +{len(rows) - limit} more")


# 1. The redirected images - what are the unique image URLs?
show("Warning-Image_redirects.csv",
     ["URL", "HTTP status code", "Redirect URL", "No. of IMG inlinks"],
     20, "IMAGE REDIRECTS (unique images)")

# 2. Internal URLs that are redirecting and still being linked to
show("Warning-3XX_redirect.csv",
     ["URL", "HTTP status code", "Redirect URL", "No. of all inlinks", "Organic traffic"],
     20, "3XX REDIRECT (internal URLs linked to)")

# 3. Redirect chains
show("Notice-Redirect_chain.csv",
     ["URL", "Redirect chain URLs", "No. of redirect chain URLs", "Redirect URL"],
     10, "REDIRECT CHAINS")

# 4. Broken pages being linked to - group by the broken target
p = D / "Error-indexable-Page_has_links_to_broken_page-links.csv"
rows = read_export(p)
print(f"\n{'=' * 70}\nBROKEN LINK TARGETS (from {len(rows)} link rows)\n{'=' * 70}")
if rows:
    print("cols:", list(rows[0].keys()))
    tgt = [c for c in rows[0] if "arget" in c or c == "Link URL"]
    key = tgt[0] if tgt else list(rows[0])[1]
    for url, n in Counter(r[key] for r in rows).most_common(40):
        print(f"{n:>5}  {url[:100]}")
