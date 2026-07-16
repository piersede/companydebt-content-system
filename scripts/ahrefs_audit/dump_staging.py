"""Dump a staging page's FULL raw block content (staging_edit.py show truncates at 4k).

Usage: python scripts/ahrefs_audit/dump_staging.py <url> [grep-substring]
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from staging_edit import session, resolve_post  # noqa: E402

url = sys.argv[1]
needle = sys.argv[2] if len(sys.argv) > 2 else None

s = session()
res = resolve_post(s, url)
if not res:
    sys.exit(f"NOT_FOUND: {url}")
endpoint, pid, slug, link, raw = res
print(f"[{slug}] {endpoint}/{pid}  raw_len={len(raw)}  link={link}\n")

if needle:
    low, nlow = raw.lower(), needle.lower()
    i, n = 0, 0
    while (j := low.find(nlow, i)) != -1:
        print(f"--- match {n + 1} @ {j} ---")
        print(raw[max(0, j - 260):j + 260].replace("\n", " "))
        print()
        i, n = j + 1, n + 1
    if not n:
        print(f"(no match for {needle!r})")
else:
    print(raw)
