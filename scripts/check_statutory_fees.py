"""Scan content for superseded statutory fees and banned claims.

The site had four different strike-off fees in circulation (£10, £33, "£10-£33",
"£33 (£10 online)"), none of them correct, plus a stale £343 winding-up petition
court fee on ~24 pages. Every figure was hard-typed into prose, so nothing caught
the drift when the fees changed.

data/statutory_fees.json is now the source of truth. This script is the guard:
it fails any page still carrying a superseded value or a banned claim.

Usage:
    python scripts/check_statutory_fees.py                 # scan drafts/
    python scripts/check_statutory_fees.py --path preview  # scan somewhere else
    python scripts/check_statutory_fees.py --slug how-much-does-liquidation-cost
    python scripts/check_statutory_fees.py --json          # machine-readable

Exit code 1 if any violation is found, so it can gate a build.
"""

from __future__ import annotations

import argparse
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
FEES_PATH = ROOT / "data" / "statutory_fees.json"

# Superseded values are bare currency strings, so a naive search throws false
# positives: "£10,000 of HMRC debt" contains "£10". Require that the match is
# not immediately followed by more digits, a comma, or a decimal point.
def _boundary(value: str) -> re.Pattern[str]:
    # Block "£10" matching inside "£10,000" (a comma or point followed by a digit
    # means we are mid-number), but still allow a value that simply ends a clause:
    # "£9,000 to £12,000, and payments..." must match. A blanket (?![\d,.]) rejects
    # that trailing comma and silently misses every banned claim.
    return re.compile(re.escape(value) + r"(?!\d)(?![,.]\d)")


# "£302 million of debt" is not a stale court fee. Exclude scale words.
SCALE = re.compile(r"^\s*(million|billion|m\b|bn\b|k\b)", re.I)

# A superseded figure quoted AS HISTORY is correct, not stale. "the cap is £751
# (previously £719 for 2025/26)" must not be flagged, or the guard cries wolf and
# gets ignored. Only flag a superseded value asserted as the CURRENT figure.
HISTORICAL = re.compile(
    r"previous|up from|was\s|prior|until|last year|earlier|former|"
    r"20\d\d/\d\d|in 20\d\d|replaced|superseded|before 6 April|"
    # Rate changes get narrated as a progression ("18%, having risen from 14%
    # and, before that, 10%"). Without these the guard flags the very sentence
    # that documents the change correctly.
    r"risen from|rose from|increased from|reduced from|down from|before that|"
    r"used to be|historically|no longer",
    re.I,
)


def _is_false_positive(text: str, m: re.Match[str]) -> bool:
    trailing = text[m.end(): m.end() + 12]
    if SCALE.match(trailing):
        return True
    # Look behind and ahead for historical framing in the same sentence-ish window.
    window = text[max(0, m.start() - 110): m.end() + 60]
    return bool(HISTORICAL.search(window))


def _rel(path: pathlib.Path) -> str:
    # --path can point outside the repo (a scratch directory of test fixtures,
    # a checkout elsewhere). relative_to raises there, which crashed the whole
    # scan rather than reporting a finding.
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_fees() -> dict:
    if not FEES_PATH.exists():
        sys.exit(f"ERROR: {FEES_PATH} not found. It is the source of truth for this check.")
    return json.loads(FEES_PATH.read_text(encoding="utf-8"))


def scan_file(path: pathlib.Path, fees: dict) -> list[dict]:
    # Drafts write money as HTML entities (&#163;343), so a raw read never matched a
    # single "£" pattern in this file and the check passed on pages carrying every
    # stale fee we have. Unescape first. Offsets shift, but nothing here reports
    # character positions - only line numbers, recomputed below from the same text.
    text = html.unescape(path.read_text(encoding="utf-8", errors="replace"))
    hits: list[dict] = []
    # File-scoped: £33 is superseded for BOTH the online and paper DS01 keys, so a
    # per-entry set would still report every strike-off hit twice.
    seen: set[tuple[int, str]] = set()

    for key, entry in fees.items():
        if key.startswith("_"):
            continue
        current = entry["value"]
        for old in entry.get("superseded", []):
            for m in _boundary(old).finditer(text):
                if _is_false_positive(text, m):
                    continue
                line = text.count("\n", 0, m.start()) + 1
                ctx = text[max(0, m.start() - 90): m.start() + 90].replace("\n", " ")
                # Strike-off and court fees are only wrong in a topical context.
                # £33 in an unrelated sum is not a stale DS01 fee.
                if "strike" in key and not re.search(r"strike|dissol|DS01", ctx, re.I):
                    continue
                if "petition" in key and not re.search(
                    r"petition|winding|wind|court fee|deposit", ctx, re.I
                ):
                    continue
                if (line, old) in seen:
                    continue
                seen.add((line, old))
                expected = current
                if "strike_off" in key:
                    expected = "£13 online / £18 paper"
                hits.append({
                    "file": _rel(path),
                    "line": line,
                    "type": "superseded_fee",
                    "key": key,
                    "found": old,
                    "expected": expected,
                    "context": ctx.strip(),
                })

    # Commercial (non-statutory) fees drift too. The CVL fee was published as
    # £4,000-£6,000 on four pages and £4,000-£7,000 on a fifth. These are regex
    # because the drift is a range, not a single token.
    #
    # Two tiers, because the drift is not always a distinctive range. The CVL fee
    # also appeared as a bare "from around £5,000", "£5,000 or more" and "£5,000
    # upfront", and a bare £5,000 is a perfectly legitimate figure for a CVA or an
    # administration. Tier 2 patterns therefore only fire when the surrounding text
    # is talking about the procedure the fee belongs to, and not about a different
    # one. Without that gate the check either misses the drift or cries wolf, and
    # a guard that cries wolf gets switched off.
    for key, entry in fees.items():
        if key.startswith("_"):
            continue
        ctx_required = entry.get("context_required")
        ctx_forbidden = entry.get("context_forbidden")
        tiers = [(p, False) for p in entry.get("drift_patterns", [])]
        tiers += [(p, True) for p in entry.get("drift_patterns_in_context", [])]

        for pat, needs_ctx in tiers:
            for m in re.finditer(pat, text, re.I):
                line = text.count("\n", 0, m.start()) + 1
                if (line, key) in seen:
                    continue
                ctx = text[max(0, m.start() - 120): m.end() + 100].replace("\n", " ")
                if needs_ctx:
                    if ctx_required and not re.search(ctx_required, ctx, re.I):
                        continue
                    if ctx_forbidden and re.search(ctx_forbidden, ctx, re.I):
                        continue
                # A superseded figure quoted as history is documentation, not drift.
                if _is_false_positive(text, m):
                    continue
                seen.add((line, key))
                hits.append({
                    "file": _rel(path),
                    "line": line,
                    "type": "fee_drift",
                    "key": key,
                    "found": re.sub(r"<[^>]+>", "", m.group(0))[:40],
                    "expected": entry["value"],
                    "context": ctx.strip(),
                })

    banned = fees.get("_banned_claims", {})
    for bkey, bentry in banned.items():
        if bkey.startswith("_"):
            continue
        # Patterns, not literals, and NO topical context gate. The phrasings vary
        # ("the average successful claim is", "can be worth", "often turns out to be
        # closer to") and a sentence stating the figure frequently never says the word
        # "redundancy" at all. The pattern itself is the signal; gating it on nearby
        # keywords produced false negatives, which is the failure mode that matters.
        banned_lines: set[int] = set()
        ctx_re = bentry.get("context_required")
        # Tier 1 fires anywhere; tier 2 is loose and needs a topical word nearby,
        # or it flags the legitimate "£5,000 to £9,000" CVL cost range.
        tiers = [(p, False) for p in bentry.get("banned_patterns", [])]
        tiers += [(p, True) for p in bentry.get("banned_patterns_in_context", [])]

        for pat, needs_ctx in tiers:
            for m in re.finditer(pat, text, re.I):
                line = text.count("\n", 0, m.start()) + 1
                if line in banned_lines:
                    continue
                ctx = text[max(0, m.start() - 120): m.end() + 80].replace("\n", " ")
                if needs_ctx and ctx_re and not re.search(ctx_re, ctx, re.I):
                    continue
                banned_lines.add(line)
                hits.append({
                    "file": _rel(path),
                    "line": line,
                    "type": "banned_claim",
                    "key": bkey,
                    "found": re.sub(r"<[^>]+>", "", m.group(0))[:60],
                    "expected": bentry.get("use_instead", "(remove)"),
                    "context": ctx.strip(),
                })

    return hits


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--path", default="drafts", help="Directory to scan (default: drafts)")
    ap.add_argument("--slug", help="Scan only files whose name contains this slug")
    ap.add_argument("--json", action="store_true", help="Emit JSON")
    ap.add_argument("--include-snapshots", action="store_true",
                    help="Also scan drafts/audit/ (point-in-time snapshots, not a publish source)")
    args = ap.parse_args()

    fees = load_fees()
    target = ROOT / args.path
    files = sorted(target.rglob("*.html"))
    # drafts/audit/ holds point-in-time snapshots taken during past audits. No
    # script reads it and nothing publishes from it, so stale fees in there are
    # a historical record, not a live defect. Scanning it only adds noise.
    if not args.include_snapshots:
        files = [f for f in files if "audit" not in f.parts]
    if args.slug:
        files = [f for f in files if args.slug in f.name]

    all_hits: list[dict] = []
    for f in files:
        all_hits.extend(scan_file(f, fees))

    if args.json:
        print(json.dumps(all_hits, indent=2, ensure_ascii=False))
        return 1 if all_hits else 0

    if not all_hits:
        print(f"OK: no superseded fees or banned claims in {len(files)} file(s) under {args.path}/")
        return 0

    by_file: dict[str, list[dict]] = {}
    for h in all_hits:
        by_file.setdefault(h["file"], []).append(h)

    print(f"FAIL: {len(all_hits)} violation(s) across {len(by_file)} file(s)\n")
    for fname, hits in sorted(by_file.items()):
        print(f"  {fname}")
        for h in hits:
            arrow = "REMOVE:" if h["type"] == "banned_claim" else "->"
            print(f"    L{h['line']:<5} [{h['type']}] {h['found']} {arrow} {h['expected']}")
    print(f"\nSource of truth: data/statutory_fees.json")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
