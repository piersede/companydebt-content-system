#!/usr/bin/env python
"""Turn the completed CTA review list into the page map the CTA plugin reads.

Input:  a completed copy of docs/cta-review-list.csv (all 13 columns filled in).
Output: mu-plugins/cd-cta-blocks/page-map.php — generated, do not hand-edit.

    python scripts/build_cta_page_map.py <completed.csv>

The generated file holds one entry per reviewed page:
    slug => array( variant, urgency, block size, alternative primary CTA )

Refuses to write if the input contradicts itself, because a contradiction here ships
the wrong message to a director rather than throwing a visible error.
"""
from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "mu-plugins" / "cd-cta-blocks" / "page-map.php"

VARIANTS = {"early_check", "serious_position", "personal_risk_secondary", "none"}
SIZES = {"large", "compact", "none"}

# Alternative primary CTAs that exist as a block today. Anything else is recorded in the
# map but has nothing to render yet, and is reported at the end.
BUILT = {"direct advice", "solvent closure", "none", ""}


def norm(value: str) -> str:
    return (value or "").strip().lower()


def check(rows: list[dict]) -> list[str]:
    problems = []
    for r in rows:
        page = r["Page"]
        variant, fit = norm(r["Variant"]), norm(r["Test fit"])
        size, urgency = norm(r["Block size"]), norm(r["Urgency modifier"])

        if variant not in VARIANTS:
            problems.append(f"{page}: unknown variant {variant!r}")
        if size not in SIZES:
            problems.append(f"{page}: unknown block size {size!r}")
        if variant == "none" and (fit != "none" or size != "none"):
            problems.append(f"{page}: variant none but test fit {fit!r} / size {size!r}")
        if variant == "personal_risk_secondary" and size != "compact":
            problems.append(f"{page}: personal-risk pages are compact only, got {size!r}")
        if urgency == "urgent_action" and size == "large":
            problems.append(f"{page}: urgent page cannot carry a large test block")
        if fit == "primary" and size != "large":
            problems.append(f"{page}: test fit primary but size {size!r}")
        if fit == "secondary" and size != "compact":
            problems.append(f"{page}: test fit secondary but size {size!r}")
    return problems


def php_string(value: str) -> str:
    return "'" + value.replace("\\", "\\\\").replace("'", "\\'") + "'"


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("usage: build_cta_page_map.py <completed-review-list.csv>")
    src = Path(sys.argv[1])
    rows = list(csv.DictReader(src.open(encoding="utf-8-sig")))
    if not rows:
        sys.exit("no rows read")

    problems = check(rows)
    if problems:
        print(f"{len(problems)} problem(s) — nothing written:")
        for p in problems[:40]:
            print("  ", p)
        sys.exit(1)

    entries = []
    for r in sorted(rows, key=lambda x: x["Page"]):
        slug = r["Page"].strip("/").split("/")[-1]
        variant = norm(r["Variant"])
        urgency = "urgent_action" if norm(r["Urgency modifier"]) == "urgent_action" else ""
        size = norm(r["Block size"])
        alt = (r["Alternative primary CTA"] or "").strip()
        if norm(alt) == "none":
            alt = ""
        entries.append((slug, variant, urgency, size, alt, r["Page"]))

    width = max(len(php_string(e[0])) for e in entries)
    lines = [
        "<?php",
        "/**",
        " * CTA page map — GENERATED, do not hand-edit.",
        " *",
        " * Source: a completed copy of docs/cta-review-list.csv, one reviewed decision per",
        " * page, per docs/cta-insolvency-test-wording-plan.md.",
        " * Rebuild: python scripts/build_cta_page_map.py <completed.csv>",
        " *",
        " * Each entry is: slug => array( variant, urgency, block size, alternative primary CTA ).",
        f" * {len(entries)} pages reviewed.",
        " */",
        "if ( ! defined( 'ABSPATH' ) ) { exit; }",
        "",
        "return array(",
    ]
    for slug, variant, urgency, size, alt, page in entries:
        key = php_string(slug).ljust(width)
        lines.append(
            f"\t{key} => array( {php_string(variant)}, {php_string(urgency)}, "
            f"{php_string(size)}, {php_string(alt)} ), // {page}"
        )
    lines += [");", ""]
    OUT.write_text("\n".join(lines), encoding="utf-8")

    counts = Counter(e[1] for e in entries)
    print(f"{len(entries)} pages -> {OUT.relative_to(ROOT)}")
    print("variants:", dict(counts))
    print("urgent:", sum(1 for e in entries if e[2]))

    missing = Counter(e[4] for e in entries if norm(e[4]) not in BUILT)
    if missing:
        print("\nalternative primary CTAs with no block built yet:")
        for name, n in missing.most_common():
            print(f"  {n:4}  {name}")


if __name__ == "__main__":
    main()
