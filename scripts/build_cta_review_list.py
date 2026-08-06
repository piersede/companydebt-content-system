#!/usr/bin/env python
"""Build the CTA placement review list.

Produces docs/cta-review-list.csv in the column format set out in section 12 of
docs/cta-insolvency-test-wording-plan.md, ordered by the review order in section 13.

The plan is explicit that page intent is decided by a human and that clusters and URL
names are not decisions. So this script deliberately does NOT fill in the decision
columns except where a page name is genuinely conclusive (enforcement wording, the
solvent-closure cluster). Everything else is left blank with the confidence marked, so
the reviewer is filling gaps rather than second-guessing a machine's guess.

Re-run after the manifest changes:
    python scripts/build_cta_review_list.py
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "docs" / "cta-rollout-manifest.md"
DRAFTS = ROOT / "drafts"
THEME_FUNCTIONS = ROOT / "theme" / "functions.php"
OUT = ROOT / "docs" / "cta-review-list.csv"

COLUMNS = [
    "Page",
    "Primary audience",
    "Assumed state",
    "Formal action",
    "Personal-risk context",
    "Test fit",
    "Variant",
    "Urgency modifier",
    "Block size",
    "Alternative primary CTA",
    "Confidence",
    "Reviewed",
    "Notes",
]

# Section 13 review order. First match wins, so the more specific groups come first.
PHASES: list[tuple[str, tuple[str, ...]]] = [
    ("1.1 Winding-up petitions", ("winding-up-petition", "winding-up-order", "wind-up")),
    ("1.2 Statutory demands and enforcement",
     ("statutory-demand", "bailiff", "enforcement", "distraint", "high-court-writ",
      "notice-of-enforcement", "ccj", "county-court-judgment")),
    ("1.3 CVL and insolvent liquidation",
     ("creditors-voluntary-liquidation", "/cvl", "compulsory-liquidation",
      "voluntary-vs-compulsory", "liquidate", "liquidation-process", "liquidation-costs")),
    ("1.4 Cannot-pay HMRC", ("cant-pay", "hmrc", "time-to-pay", "vat", "paye", "corporation-tax")),
    ("1.5 Rescue and restructuring",
     ("rescue", "administration", "cva", "restructur", "turnaround", "viability")),
    ("1.6 Personal liability",
     ("personal-guarantee", "directors-loan", "disqualif", "wrongful-trading", "misfeasance",
      "personal-liability", "director-conduct", "overdrawn")),
    ("2.1 Warning signs and insolvency tests",
     ("warning-sign", "insolvency-test", "is-my-company-insolvent", "signs-of")),
    ("2.2 Cash flow", ("cash-flow", "cashflow")),
    ("2.3 Stopping trade", ("stop-trading", "ceasing-trade", "cease-trading", "stopped-trading")),
    ("2.4 Director duties", ("director-duties", "duties-of", "directors-responsibilities")),
    ("2.5 Creditor pressure", ("creditor", "supplier", "debt-collect", "county-court")),
    ("2.6 Liquidation consequences", ("-in-liquidation", "what-happens-to", "after-liquidation")),
]

# The only two page groups where the page name really is conclusive.
ENFORCEMENT = (
    "winding-up-petition", "statutory-demand", "bailiff", "enforcement", "distraint",
    "high-court-writ", "notice-of-enforcement", "ccj", "county-court-judgment",
)


def read_manifest() -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*(/[^|]*?)\s*\|\s*([A-Za-z-]+)\s*\|", line)
        if m:
            rows.append((m.group(1).strip(), m.group(2).strip()))
    return [r for r in rows if r[1] not in ("EXCLUDE", "REVIEW")]


def previously_injected_slugs() -> set[str]:
    """Slugs of the 54 pages the removed injector used to place CTAs on.

    The injector's map was keyed by post id; drafts are named <id>_<slug>.html.
    """
    text = THEME_FUNCTIONS.read_text(encoding="utf-8")
    m = re.search(r"function cd_acta_map\(\)\s*\{.*?return array\((.*?)\);", text, re.S)
    if not m:
        return set()
    ids = {int(x) for x in re.findall(r"(\d+)\s*=>", m.group(1))}
    slugs = set()
    for path in DRAFTS.glob("*.html"):
        head, _, rest = path.stem.partition("_")
        if head.isdigit() and int(head) in ids:
            slugs.add(rest)
    return slugs


def phase_for(url: str) -> str:
    for name, keys in PHASES:
        if any(k in url for k in keys):
            return name
    return "3 Long tail"


def build_row(url: str, cluster: str, injected: bool) -> dict[str, str]:
    row = {c: "" for c in COLUMNS}
    row["Page"] = url
    notes = [f"cluster: {cluster}"]
    if injected:
        notes.append("carried the old injected CTA set")

    if cluster == "solvent-closure":
        # Conclusive: the test's first question has no solvent answer (plan 6A, 7.1, 16).
        row["Assumed state"] = "solvent"
        row["Test fit"] = "none"
        row["Variant"] = "none"
        row["Block size"] = "compact"
        row["Alternative primary CTA"] = "solvent closure"
        row["Confidence"] = "high"
        notes.append("test cannot serve a solvent company until its first question offers a solvent answer")
    elif any(k in url for k in ENFORCEMENT):
        # Conclusive on urgency only. The diagnostic state still needs a human.
        row["Formal action"] = "active"
        row["Urgency modifier"] = "urgent_action"
        row["Test fit"] = "secondary"
        row["Block size"] = "compact"
        row["Alternative primary CTA"] = "direct advice"
        row["Confidence"] = "medium"
        notes.append("page name names a formal creditor action; confirm the reader has one rather than is researching one")
    else:
        row["Confidence"] = "low"
        notes.append("needs a read of the page: audience, assumed state and test fit all undecided")

    row["Notes"] = "; ".join(notes)
    return row


def main() -> None:
    injected = previously_injected_slugs()
    rows = []
    for url, cluster in read_manifest():
        slug = url.strip("/").split("/")[-1]
        row = build_row(url, cluster, slug in injected)
        row["_phase"] = phase_for(url)
        rows.append(row)

    rows.sort(key=lambda r: (r["_phase"], r["Page"]))
    phases = [r["_phase"] for r in rows]

    with OUT.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["Review phase"] + COLUMNS)
        writer.writeheader()
        for r in rows:
            out = {"Review phase": r.pop("_phase")}
            out.update(r)
            writer.writerow(out)

    print(f"{len(rows)} pages -> {OUT.relative_to(ROOT)}")
    from collections import Counter
    for phase, n in sorted(Counter(phases).items()):
        print(f"  {n:4}  {phase}")
    conf = Counter(r["Confidence"] for r in rows)
    print("confidence:", dict(conf))
    print(f"previously carried a CTA: {sum(1 for r in rows if 'old injected' in r['Notes'])}")


if __name__ == "__main__":
    main()
