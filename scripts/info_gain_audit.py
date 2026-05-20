"""Info-gain audit tool for Bernstein review stage.

Implements the per-H2 walk required by editorial-os/16-pre-publish-gate.md
§Check 12a (Information Gain). Two modes:

    --emit-template <article.html> [--output FILE]
        Scan H2s in the article and emit a markdown template with one block
        per H2 that the operator must fill in.

    --check <template.md> --file <article.html>
        Verify a filled template covers every H2 in the article with at
        least one info-gain element OR an explicit no-info-gain opt-out.
        Exit 0 on pass, 1 on fail.

Bernstein's review stage uses --check to gate the review_notes_complete
checkpoint. The checkpoint cannot be marked complete until --check passes.

Pass criteria (per §Check 12a):
- Every H2 contains at least one of: a fact competitors usually omit,
  a better why-it-matters explanation, a clearer recommendation per user
  type, or a more exact trade-off than the SERP norm.
- 3+ net-new value elements across the article.
- No H2 with zero info-gain elements (use no-info-gain opt-out only for
  genuinely structural sections — e.g. Related Guides navigation).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


H2_RE = re.compile(r"<h2[^>]*>(.*?)</h2>", re.IGNORECASE | re.DOTALL)


def extract_h2s(html: str) -> list[str]:
    h2s: list[str] = []
    for m in H2_RE.finditer(html):
        text = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        text = re.sub(r"\s+", " ", text)
        if text:
            h2s.append(text)
    return h2s


def emit_template(article_path: Path, h2s: list[str]) -> str:
    n = len(h2s)
    lines: list[str] = [
        f"# Info Gain Audit: {article_path.name}",
        "",
        f"- Source file: `{article_path}`",
        f"- H2 count: {n}",
        "",
        "## How to fill this in",
        "",
        "For each H2 below, either:",
        "",
        "1. Replace the `- ` placeholder under **Info-gain elements** with one or",
        "   more concrete elements. Each element should be one of: a fact",
        "   competitors usually omit, a better why-it-matters explanation, a",
        "   clearer recommendation per user type, or a more exact trade-off than",
        "   the SERP norm. Quote the exact prose where possible.",
        "",
        "2. OR uncomment the `<!-- no-info-gain: ... -->` line and replace the",
        "   placeholder with a real reason. Use sparingly and only for genuinely",
        "   structural sections (e.g. Related Guides navigation, FAQ). The audit",
        "   will count opt-outs and warn if more than 2 are used.",
        "",
        "When done, run:",
        "",
        f"    python scripts/info_gain_audit.py --check <this-file> --file {article_path}",
        "",
        "Bernstein's `review` stage cannot advance until that check passes.",
        "",
        "---",
        "",
    ]
    for i, h2 in enumerate(h2s, 1):
        lines.extend([
            f"## H2 {i} of {n}: {h2}",
            "",
            "**Info-gain elements:**",
            "",
            "- ",
            "",
            "<!-- no-info-gain: REASON -->",
            "",
            "---",
            "",
        ])
    return "\n".join(lines)


def split_h2_sections(template_text: str) -> list[str]:
    parts = re.split(r"^## H2 \d+ of \d+: ", template_text, flags=re.MULTILINE)
    return parts[1:] if len(parts) > 1 else []


def check_section(section: str) -> tuple[bool, str]:
    """Return (pass, reason). Pass if section has 1+ filled bullet under
    Info-gain elements, OR an active no-info-gain opt-out comment with a
    reason that isn't the placeholder."""
    # Active opt-out: must NOT be the literal placeholder, must NOT be commented-out by leaving REASON
    opt_out_match = re.search(r"<!--\s*no-info-gain:\s*(.+?)\s*-->", section)
    if opt_out_match:
        reason = opt_out_match.group(1).strip()
        if reason and reason.upper() != "REASON":
            return True, "opt-out"

    elements_match = re.search(
        r"\*\*Info-gain elements:\*\*\s*\n(.*?)(?=\n\*\*|\n## H2 |\n---|\Z)",
        section,
        re.DOTALL,
    )
    if not elements_match:
        return False, "no Info-gain elements block found"
    block = elements_match.group(1)
    # Single-line bullets only — \s+ would swallow newlines and pull in the
    # next line (e.g. capturing a no-info-gain comment as bullet content).
    bullets = re.findall(r"^[ \t]*-[ \t]+(.+?)[ \t]*$", block, re.MULTILINE)
    non_empty = [b for b in bullets if b and b.strip() and b.strip().lower() not in {"none", "(none)", "n/a", "tbd"}]
    if not non_empty:
        return False, "empty Info-gain elements (no bullet text filled in)"
    return True, f"{len(non_empty)} element(s)"


def check_template(template_text: str, h2s: list[str]) -> tuple[bool, list[str], dict]:
    sections = split_h2_sections(template_text)
    failures: list[str] = []
    stats = {"opt_outs": 0, "filled": 0, "total_elements": 0}
    if len(sections) != len(h2s):
        failures.append(
            f"H2 count mismatch: template has {len(sections)} sections, "
            f"source article has {len(h2s)} H2s. Re-emit the template."
        )
        return False, failures, stats
    for i, (h2_text, section) in enumerate(zip(h2s, sections), start=1):
        ok, reason = check_section(section)
        if not ok:
            failures.append(f"H2 {i} ({h2_text[:60]}): {reason}")
            continue
        if reason == "opt-out":
            stats["opt_outs"] += 1
        else:
            stats["filled"] += 1
            try:
                stats["total_elements"] += int(reason.split(" ", 1)[0])
            except (ValueError, IndexError):
                pass
    if stats["opt_outs"] > 2:
        failures.append(
            f"too many no-info-gain opt-outs ({stats['opt_outs']}); "
            "max 2 allowed (only structural sections like Related Guides should opt out)"
        )
    if stats["total_elements"] < 3 and stats["filled"] > 0:
        failures.append(
            f"only {stats['total_elements']} info-gain element(s) recorded "
            "across the article; §Check 12a requires 3+ net-new value elements"
        )
    return len(failures) == 0, failures, stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True, help="Article HTML file")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--emit-template", action="store_true", help="Emit a fresh template based on the article's H2s")
    g.add_argument("--check", help="Path to a filled template to verify")
    ap.add_argument("--output", help="Output path for --emit-template (default stdout)")
    args = ap.parse_args()

    article_path = Path(args.file)
    if not article_path.exists():
        print(f"ERROR: article not found: {article_path}", file=sys.stderr)
        return 2
    html = article_path.read_text(encoding="utf-8")
    h2s = extract_h2s(html)
    if not h2s:
        print(f"ERROR: no <h2> elements found in {article_path}", file=sys.stderr)
        return 2

    if args.emit_template:
        template = emit_template(article_path, h2s)
        if args.output:
            out_path = Path(args.output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(template, encoding="utf-8")
            print(f"Template written to {out_path}")
            print(f"  {len(h2s)} H2 sections to fill in")
            print(f"  Run: python scripts/info_gain_audit.py --check {out_path} --file {article_path}")
        else:
            print(template)
        return 0

    if args.check:
        check_path = Path(args.check)
        if not check_path.exists():
            print(f"ERROR: template not found: {check_path}", file=sys.stderr)
            return 2
        template_text = check_path.read_text(encoding="utf-8")
        ok, failures, stats = check_template(template_text, h2s)
        if ok:
            print(
                f"INFO-GAIN AUDIT: PASS — {stats['filled']} H2(s) with elements "
                f"({stats['total_elements']} elements total), {stats['opt_outs']} opt-out(s)"
            )
            return 0
        print(
            f"INFO-GAIN AUDIT: FAIL — {stats['filled']}/{len(h2s)} H2(s) filled, "
            f"{stats['opt_outs']} opt-out(s), {stats['total_elements']} elements"
        )
        for f in failures:
            print(f"  - {f}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
