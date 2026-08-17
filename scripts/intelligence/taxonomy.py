"""Canonical sector taxonomy: the single definition of every sector we publish.

WHY THIS EXISTS
---------------
Today a sector's identity is spread across five places: the SECTORS dict in
sic_group_stats.py, a cc_builder page config, build_page.py's PAGE_REGISTRY,
page_runtime_metadata.py, and sector_trade_links.py. Nothing checks they agree.
That is how a page ended up claiming to be "the largest single trade in the
section" at 37% when it was second at 22.7%: the claim lived in prose, and no
code owned the fact.

This module makes one record per sector the source of truth for identity, SIC
mapping, parent, tier and peer group. Metrics and pages read from here.

It does NOT hold prose. Editorial copy stays where it is. This owns facts.

USAGE
    python scripts/intelligence/taxonomy.py --extract   # rebuild from the live configs
    python scripts/intelligence/taxonomy.py --validate  # check it against the series
    python scripts/intelligence/taxonomy.py --show 561
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
from pathlib import Path

if sys.platform == "win32":
    # reconfigure(), not a fresh TextIOWrapper: two modules each wrapping
    # sys.stdout.buffer means the first wrapper closes the buffer when it is
    # collected, and the second one then fails with "I/O operation on closed file".
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent.parent
TAXONOMY = ROOT / "data" / "taxonomy" / "sectors.json"
SECTOR_CONFIG = ROOT / "scripts" / "datahub" / "pages" / "sic_group_stats.py"
SERIES = ROOT / "data" / "insolvency-statistics" / "sector_series.json"

# Pages that are not SECTORS entries but are part of the family.
EXTRA_PAGES = [
    {"sector_id": "construction", "slug": "construction-insolvency-statistics",
     "wp_id": 79856, "sic_code": "F", "sic_level": "section",
     "display_name": "Construction", "tier": "A", "peer_group": "construction",
     "builder": "sector_pages.build_construction"},
    {"sector_id": "all_sectors", "slug": "company-insolvencies-by-sector",
     "wp_id": 79855, "sic_code": None, "sic_level": "overview",
     "display_name": "All sectors overview", "tier": "A", "peer_group": None,
     "builder": "sector_pages.build_sector"},
]

PEER_GROUPS = {
    "employment": ["781", "782"],
    "hospitality": ["561", "551"],
    "logistics": ["494", "522"],
    "professional": ["620", "702", "711"],
    "leisure": ["931", "900", "932"],
    "property": ["682", "683"],
    "retail": ["47"],
    "construction": ["F"],
}


def _peer_group_for(sic: str | None) -> str | None:
    for name, codes in PEER_GROUPS.items():
        if sic in codes:
            return name
    return None


def _field(segment: str, key: str) -> str | None:
    m = re.search(r'"' + key + r'":\s*"([^"]*)"', segment)
    return m.group(1) if m else None


def _int_field(segment: str, key: str) -> int | None:
    m = re.search(r'"' + key + r'":\s*(\d+)', segment)
    return int(m.group(1)) if m else None


def extract() -> list[dict]:
    """Read the live SECTORS dict and turn it into canonical records."""
    text = SECTOR_CONFIG.read_text(encoding="utf-8")
    slugs = re.findall(r'^    "([a-z0-9\-]+)":\s*\{', text, re.M)
    marks = []
    for s in slugs:
        m = re.search(r'"' + re.escape(s) + r'":\s*\{', text)
        if m:
            marks.append((s, m.start()))
    marks.sort(key=lambda x: x[1])

    out = []
    for i, (slug, start) in enumerate(marks):
        end = marks[i + 1][1] if i + 1 < len(marks) else len(text)
        seg = text[start:end]
        sic = _field(seg, "sic_code")
        kind = _field(seg, "sic_code_kind") or "group"
        out.append({
            "sector_id": slug.replace("-insolvency-statistics", "").replace("-", "_"),
            "slug": slug,
            "wp_id": _int_field(seg, "wp_id"),
            "sic_code": sic,
            "sic_level": "division" if kind == "division" else "group",
            "display_name": (_field(seg, "h1a") or slug).replace("UK ", ""),
            "keyword": _field(seg, "keyword"),
            "official_name": _field(seg, "sic_label"),
            "parent_section": _field(seg, "parent_section_code"),
            "parent_division": _field(seg, "division_code"),
            "compare_against": "division" if '"parent_kind"' in seg else "section",
            "geography": "England and Wales",
            "peer_group": _peer_group_for(sic),
            "tier": "A",
            "builder": "sic_group_stats",
            "status": "active",
        })

    out.extend(EXTRA_PAGES)
    for e in out:
        e.setdefault("keyword", None)
        e.setdefault("official_name", None)
        e.setdefault("parent_section", None)
        e.setdefault("parent_division", None)
        e.setdefault("compare_against", "section")
        e.setdefault("geography", "England and Wales")
        e.setdefault("status", "active")
    return out


def load() -> list[dict]:
    if not TAXONOMY.exists():
        raise SystemExit("taxonomy not built yet: run --extract")
    return json.loads(TAXONOMY.read_text(encoding="utf-8"))["sectors"]


def by_slug(slug: str) -> dict | None:
    return next((s for s in load() if s["slug"] == slug), None)


def validate(sectors: list[dict]) -> list[str]:
    """Every SIC code must exist in the series, and nothing may be double-counted."""
    problems = []
    ser = json.loads(SERIES.read_text(encoding="utf-8"))
    known = {k: {e["code"] for e in ser.get(k, [])} for k in ("groups", "divisions", "sections")}

    seen_ids, seen_slugs, seen_wp = set(), set(), set()
    for s in sectors:
        sid, sic, lvl = s["sector_id"], s["sic_code"], s["sic_level"]
        if sid in seen_ids:
            problems.append("duplicate sector_id: %s" % sid)
        if s["slug"] in seen_slugs:
            problems.append("duplicate slug: %s" % s["slug"])
        if s["wp_id"] and s["wp_id"] in seen_wp:
            problems.append("duplicate wp_id: %s" % s["wp_id"])
        seen_ids.add(sid)
        seen_slugs.add(s["slug"])
        if s["wp_id"]:
            seen_wp.add(s["wp_id"])

        if sic is None:
            continue
        pool = {"group": "groups", "division": "divisions", "section": "sections"}.get(lvl)
        if pool and sic not in known.get(pool, set()):
            problems.append("%s: SIC %s not found among %s in the series" % (s["slug"], sic, pool))

    # Two sectors must not claim the same SIC code at the same level.
    pairs = {}
    for s in sectors:
        if s["sic_code"] is None:
            continue
        k = (s["sic_level"], s["sic_code"])
        if k in pairs:
            problems.append("SIC %s (%s) claimed by both %s and %s"
                            % (s["sic_code"], s["sic_level"], pairs[k], s["slug"]))
        pairs[k] = s["slug"]
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--extract", action="store_true", help="rebuild from the live configs")
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--show", metavar="SIC")
    args = ap.parse_args()

    if args.extract:
        sectors = extract()
        problems = validate(sectors)
        TAXONOMY.parent.mkdir(parents=True, exist_ok=True)
        TAXONOMY.write_text(json.dumps(
            {"_about": "Canonical sector definitions. Facts only, no editorial copy.",
             "generated_from": "scripts/datahub/pages/sic_group_stats.py",
             "sectors": sectors}, indent=2), encoding="utf-8")
        print("wrote %s with %d sectors" % (TAXONOMY.relative_to(ROOT), len(sectors)))
        for p in problems:
            print("  PROBLEM:", p)
        return 1 if problems else 0

    if args.validate:
        problems = validate(load())
        for p in problems:
            print("  PROBLEM:", p)
        print("validation:", "PASS" if not problems else "%d problem(s)" % len(problems))
        return 1 if problems else 0

    if args.show:
        for s in load():
            if s["sic_code"] == args.show or s["slug"] == args.show:
                print(json.dumps(s, indent=2))
        return 0

    for s in load():
        print("%-52s %-6s %-9s parent=%-4s tier=%s"
              % (s["slug"][:52], s["sic_code"], s["sic_level"],
                 s["parent_section"] or s["parent_division"], s["tier"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
