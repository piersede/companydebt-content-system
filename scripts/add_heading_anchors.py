"""Add WordPress heading anchors to stored page content that is missing them.

WHY THIS EXISTS
---------------
Live pages carry heading anchor ids (`<h2 id="...">` plus the matching
`{"anchor":"..."}` in the block comment). The on-page contents links point at
them. Several staging rewrites were drafted without them, so pushing those
rewrites live would gain the new copy but break the contents links.

This adds the anchors mechanically: the id is a slug of the heading's own text,
which is how WordPress generates them in the editor. No prose is touched - only
the id attribute and the block comment.

Read-only unless --write is passed. Compares against live so you can see which
anchors live already has and keep those ids identical (a changed id breaks any
existing deep link into the page).

USAGE
    python scripts/add_heading_anchors.py --path closing-a-limited-company
    python scripts/add_heading_anchors.py --path closing-a-limited-company --write
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import os
import re
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

if sys.platform == "win32":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)
    except Exception:
        pass

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "content_cache.json"
LIVE = "https://www.companydebt.com"


def slugify(text: str) -> str:
    t = re.sub(r"<[^>]+>", "", text)
    t = t.replace("&amp;", "and").replace("&rarr;", "")
    t = re.sub(r"[^\w\s-]", "", t).strip().lower()
    return re.sub(r"[\s_]+", "-", t)


HEADING_RE = re.compile(
    r"(<!--\s*wp:heading(?P<attrs>\s*\{[^}]*\})?\s*-->\s*)"
    r"(?P<tag><h(?P<level>[2-4])(?P<htmlattrs>[^>]*)>)(?P<text>.*?)(</h(?P=level)>)",
    re.S,
)


def existing_ids(html: str) -> list[str]:
    return re.findall(r'<h[2-4][^>]*id="([^"]+)"', html)


def add_anchors(html: str) -> tuple[str, int]:
    """Give every heading an id derived from its text. Returns (html, added)."""
    added = 0
    seen: set[str] = set(existing_ids(html))

    def repl(m: re.Match) -> str:
        nonlocal added
        htmlattrs = m.group("htmlattrs") or ""
        if 'id="' in htmlattrs:
            return m.group(0)

        slug = slugify(m.group("text"))
        if not slug:
            return m.group(0)
        base, n = slug, 2
        while slug in seen:
            slug = f"{base}-{n}"
            n += 1
        seen.add(slug)
        added += 1

        attrs = m.group("attrs") or ""
        if attrs.strip():
            inner = attrs.strip()[1:-1].strip()
            new_attrs = ' {"anchor":"%s"%s}' % (slug, ("," + inner) if inner else "")
        else:
            new_attrs = ' {"anchor":"%s"}' % slug

        comment = f"<!-- wp:heading{new_attrs} -->\n"
        level = m.group("level")
        cls = re.search(r'class="([^"]*)"', htmlattrs)
        cls_attr = f' class="{cls.group(1)}"' if cls else ' class="wp-block-heading"'
        return (f'{comment}<h{level}{cls_attr} id="{slug}">'
                f'{m.group("text")}</h{level}>')

    return HEADING_RE.sub(repl, html), added


def main() -> int:
    ap = argparse.ArgumentParser(description="Add heading anchors to stored content.")
    ap.add_argument("--path", required=True, help="path substring, e.g. closing-a-limited-company")
    ap.add_argument("--write", action="store_true", help="save back into content_cache.json")
    args = ap.parse_args()

    cache = json.loads(CACHE.read_text(encoding="utf-8"))
    matches = [(p, m) for p, m in cache.items() if args.path in p]
    if not matches:
        print(f"No page matching '{args.path}'.")
        return 1

    tok = base64.b64encode(
        f"{os.getenv('WP_LIVE_USERNAME')}:{os.getenv('WP_LIVE_APP_PASSWORD')}".encode()).decode()
    LH = {"User-Agent": "Company Debt-Publisher/1.0", "Authorization": f"Basic {tok}"}

    for path, meta in matches:
        ptype = meta.get("endpoint") or ("posts" if meta.get("type") == "post" else "pages")
        stage = meta.get("raw") or ""
        r = requests.get(f"{LIVE}/wp-json/wp/v2/{ptype}/{meta['id']}?context=edit",
                         headers=LH, timeout=90)
        live = (r.json().get("content") or {}).get("raw", "") if r.status_code == 200 else ""

        fixed, added = add_anchors(stage)
        live_ids = set(existing_ids(live))
        new_ids = set(existing_ids(fixed))

        print(f"=== {path}")
        print(f"  staging anchors before: {len(existing_ids(stage))}, after: {len(new_ids)} (+{added})")
        print(f"  live anchors: {len(live_ids)}")

        lost = live_ids - new_ids
        if lost:
            print(f"  WARNING - live ids not reproduced ({len(lost)}); deep links to these would break:")
            for x in sorted(lost)[:10]:
                print(f"      #{x}")
        else:
            print("  every live anchor id is reproduced - no deep links break")

        if args.write:
            cache[path]["raw"] = fixed

    if args.write:
        CACHE.write_text(json.dumps(cache, indent=2), encoding="utf-8")
        print("\ncontent_cache.json updated. Push with push_site_content_live.py.")
    else:
        print("\nDry run. Re-run with --write to apply.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
