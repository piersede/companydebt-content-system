"""Remove an entire <li>...</li> containing a given href from a staging page.

staging_edit.py's swap-link can only unwrap an <a> (leaving its text behind).
For a fabricated citation that is wrong, leaving the text is not acceptable:
the whole list item has to go. Matching on href avoids quoting the anchor
prose, which differs between draft and staging.

Usage: python remove_li_staging.py <url> <href-substring> [--apply]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from staging_edit import session, resolve_post, patch  # noqa: E402

url, href = sys.argv[1], sys.argv[2]
apply = "--apply" in sys.argv

s = session()
res = resolve_post(s, url)
if not res:
    sys.exit(f"NOT_FOUND: {url}")
endpoint, pid, slug, link, raw = res

# Non-greedy <li>...</li> that contains the href. [^\0] style DOTALL match.
pat = re.compile(r"<li>(?:(?!</li>).)*?" + re.escape(href) + r"(?:(?!</li>).)*?</li>\s*", re.DOTALL)
found = pat.findall(raw)
print(f"[{slug}] ({endpoint}/{pid}) matches={len(found)}")
for m in pat.finditer(raw):
    print(f"  REMOVING: {m.group(0).strip()[:220]}")

if not found:
    sys.exit(0)

modified = pat.sub("", raw)
if apply:
    print(f"  PATCH {patch(s, endpoint, pid, modified)}")
else:
    print("  (dry run - pass --apply to write)")
