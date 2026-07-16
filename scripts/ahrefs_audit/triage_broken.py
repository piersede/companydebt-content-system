import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).parent))
from parse_export import read_export

D = Path(sys.argv[1])

rows = read_export(D / "Error-indexable-Page_has_links_to_broken_page-links.csv")
print(f"Total broken-link rows: {len(rows)}\n")

print("--- internal vs external ---")
for k, n in Counter(r["Is link internal"] for r in rows).most_common():
    print(f"  internal={k}: {n}")

print("\n--- broken target by HOST ---")
for host, n in Counter(urlsplit(r["Target URL"]).netloc for r in rows).most_common(25):
    print(f"{n:>5}  {host}")

print("\n--- target status codes ---")
for c, n in Counter(r["Target HTTP status code"] for r in rows).most_common():
    print(f"{n:>5}  status={c!r}")

print("\n--- INTERNAL broken targets only (the genuinely actionable set) ---")
internal = [r for r in rows if r["Is link internal"].lower() == "true"]
print(f"internal rows: {len(internal)}")
for url, n in Counter(r["Target URL"] for r in internal).most_common(50):
    print(f"{n:>5}  {url}")

print("\n--- EXTERNAL 4XX by host (Notice-External_4XX) ---")
ext = read_export(D / "Notice-External_4XX.csv")
print("cols:", list(ext[0].keys()) if ext else "none")
for host, n in Counter(urlsplit(r["URL"]).netloc for r in ext).most_common(25):
    print(f"{n:>5}  {host}")
