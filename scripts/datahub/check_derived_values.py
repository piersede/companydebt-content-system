"""Catch stale derived values in the SIC trade page configs.

WHY THIS EXISTS
---------------
The trade pages compute their headline figures from sector_series.json, but a
lot of supporting copy quotes derived values by hand: "at 42% of the section",
"the largest single trade in its section", the share tiles in extra_findings.
When the data moves, the computed half updates and the hand-written half does
not, so one page states two different shares for the same thing.

That happened on three pages at once in the June 2026 vintage: sports said 42%
in the hero and 44.0% in key findings, creative arts said 28% against 31.2%,
and real estate letting still claimed to be "the largest single trade in the
section" at 37% when bulk administrations had pushed property trading to 60.5%
and letting down to 22.7%. An outside reviewer found them; nothing in the build
did.

This recomputes every parent-share percentage and every largest/second-largest
ranking claim straight from the series, and compares them with what the config
says. Run it after any data refresh, before publishing.

USAGE
    python scripts/datahub/check_derived_values.py            # all sectors
    python scripts/datahub/check_derived_values.py --slug retail-insolvency-statistics
    python scripts/datahub/check_derived_values.py --tolerance 0.6

Exit code 1 if any mismatch is found, so it can gate a publish.
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                                      errors="replace", line_buffering=True)
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent.parent
SERIES = ROOT / "data" / "insolvency-statistics" / "sector_series.json"
CONFIG = ROOT / "scripts" / "datahub" / "pages" / "sic_group_stats.py"

# "at 44.0% of the section", "44.0% of the section's total", "at 31.2% of\narts, ..."
SHARE_PATTERNS = [
    r"at ([\d.]+)% of\s+(?:the\s+)?(?:section|arts|real estate|its section)",
    r"([\d.]+)% of the section(?:'s)?(?: total)?",
    r"at ([\d.]+)% of\s+(?:the\s+)?section",
]
# The negative lookbehind must sit on every alternative, or "second-largest
# trade in its section" matches the largest-claim pattern and reports a bogus
# failure. It did exactly that on the creative arts page first time out.
RANK_LARGEST = (r"(?<!second-)(?:largest single trade"
                r"|largest trade in (?:its|the)"
                r"|the largest of)")
RANK_SECOND = r"second-largest"


def load_series() -> dict:
    return json.loads(SERIES.read_text(encoding="utf-8"))


def num(v):
    return v if isinstance(v, (int, float)) else 0


def ytd_window(ser: dict, year: int = 2026, upto: int = 6):
    months = ser["monthly_months"]
    want = ["%d-%02d" % (year, m) for m in range(1, upto + 1)]
    return [months.index(w) for w in want if w in months]


def sum_at(entity: dict, idx) -> int:
    mon = entity.get("monthly") or []
    return sum(num(mon[i]) for i in idx if i < len(mon))


def find_entity(ser: dict, code: str):
    for kind in ("groups", "divisions", "sections"):
        for e in ser.get(kind, []):
            if e.get("code") == code:
                return kind, e
    return None, None


def latest_month(ser: dict) -> str:
    return ser["monthly_months"][-1]


def parse_configs(text: str) -> dict:
    """Slice the SECTORS dict into one text segment per slug (no import needed)."""
    slugs = re.findall(r'^    "([a-z0-9\-]+)":\s*\{', text, re.M)
    marks = []
    for s in slugs:
        m = re.search(r'"' + re.escape(s) + r'":\s*\{', text)
        if m:
            marks.append((s, m.start()))
    marks.sort(key=lambda x: x[1])
    out = {}
    for i, (slug, start) in enumerate(marks):
        end = marks[i + 1][1] if i + 1 < len(marks) else len(text)
        out[slug] = text[start:end]
    return out


def joined_strings(segment: str) -> str:
    """Python source joins adjacent string literals; do the same so a phrase
    split across two source lines is still matched."""
    parts = re.findall(r'"((?:[^"\\]|\\.)*)"', segment)
    return " ".join(parts)


def field(segment: str, key: str):
    m = re.search(r'"' + key + r'":\s*"([^"]*)"', segment)
    return m.group(1) if m else None


def check_slug(slug: str, segment: str, ser: dict, idx, tol: float):
    problems = []
    sic = field(segment, "sic_code")
    if not sic:
        return problems

    kind, entity = find_entity(ser, sic)
    if entity is None:
        problems.append("SIC %s not found in the series" % sic)
        return problems

    # The parent the page compares against: an explicit division, else the section.
    parent_code = field(segment, "parent_kind_code") or field(segment, "division_code")
    use_division = '"parent_kind"' in segment
    section_code = field(segment, "parent_section_code")
    parent = None
    if use_division and parent_code:
        _, parent = find_entity(ser, parent_code)
    if parent is None and section_code:
        _, parent = find_entity(ser, section_code)
    if parent is None:
        return problems

    own = sum_at(entity, idx)
    tot = sum_at(parent, idx)
    if not tot:
        return problems
    true_share = 100.0 * own / tot

    # siblings inside the same parent, for ranking claims
    pcode = parent.get("code")
    sibs = [(sum_at(g, idx), g["code"]) for g in ser["groups"]
            if g.get("section") == pcode or g.get("division") == pcode]
    sibs.sort(reverse=True)
    rank = next((i + 1 for i, (_, c) in enumerate(sibs) if c == sic), None)

    text = joined_strings(segment)

    seen = set()
    for pat in SHARE_PATTERNS:
        for m in re.finditer(pat, text):
            val = float(m.group(1))
            if val in seen:
                continue
            seen.add(val)
            if abs(val - true_share) > tol:
                problems.append(
                    "share claim %.1f%% but the series gives %.1f%% (%s of %s, Jan-Jun)"
                    % (val, true_share, own, tot))

    for m in re.finditer(r'\{"value":\s*"([\d.]+)%"[^}]*"label":\s*"of ([^"]*insolvencies)"', segment):
        val = float(m.group(1))
        if abs(val - true_share) > tol:
            problems.append("key-finding tile says %.1f%% but the series gives %.1f%%"
                            % (val, true_share))

    if rank:
        if re.search(RANK_LARGEST, text) and rank != 1:
            problems.append("claims to be the largest trade in its parent, but it ranks %d "
                            "(largest is SIC %s)" % (rank, sibs[0][1]))
        if re.search(RANK_SECOND, text) and rank != 2:
            problems.append("claims to be second-largest, but it ranks %d" % rank)

    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slug", help="check one sector only")
    ap.add_argument("--tolerance", type=float, default=0.55,
                    help="allowed percentage-point drift (default 0.55, covers rounding)")
    args = ap.parse_args()

    ser = load_series()
    idx = ytd_window(ser)
    segments = parse_configs(CONFIG.read_text(encoding="utf-8"))
    if args.slug:
        segments = {k: v for k, v in segments.items() if k == args.slug}
        if not segments:
            print("no such sector:", args.slug)
            return 1

    print("series release: %s, latest month %s, window Jan-Jun 2026"
          % (ser.get("release_label", "?"), latest_month(ser)))
    print()

    bad = 0
    for slug, segment in segments.items():
        problems = check_slug(slug, segment, ser, idx, args.tolerance)
        if problems:
            bad += 1
            print("FAIL  %s" % slug)
            for p in problems:
                print("        %s" % p)
        else:
            print("ok    %s" % slug)

    print()
    if bad:
        print("%d sector(s) carry stale derived values. Fix before publishing." % bad)
        return 1
    print("All derived shares and ranking claims match the series.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
