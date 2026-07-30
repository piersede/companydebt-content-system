"""Body-prose citation corrections from the 2026-07-30 citation accuracy audit.

Companion to fix_citations_batch.py, which handled the reference-block-only
findings. These edits touch running prose, so each page also gets a persona /
density read on Opus, and the changed sentences are re-read in context rather
than swapped blind.

77157_construction-insolvency is not here: its claim was legally wrong rather
than mis-cited, so it was rewritten by hand in its own commit.

74891 is included even though the audit listed it under prose. On closer
inspection its Schedule 26 reference sits in the page's <aside class="cd-sources">
block; the zone classifier missed it because it looked for a closing </div>.
It is a pure reference swap.

Every replacement is an exact string match, and a miss is a hard error.

Usage:
    python scripts/fix_citations_prose.py            # dry run
    python scripts/fix_citations_prose.py --apply    # write
"""
import argparse
import os
import sys

DRAFTS = "drafts"
DRD = "section 51 and Schedule 8 of the Finance (No. 2) Act 2015"

FIXES = [
    # --- Finding 1 (reference block, reclassified): FA 2020 Sch 26 does not exist ---
    ("74891_secured-vs-unsecured-creditors", "F1",
     '<li><a href="https://www.legislation.gov.uk/ukpga/2020/14/contents">Finance Act 2020, Schedule 26 (HMRC secondary preferential status from 1 December 2020)</a>',
     '<li><a href="https://www.legislation.gov.uk/ukpga/2020/14/section/98">Finance Act 2020, section 98 (HMRC secondary preferential status from 1 December 2020)</a>'),

    # --- Finding 3: the small-company moratorium is Part A1, not Part 1A ---
    ("9702_receivership-mean-business", "F3",
     "eligible smaller companies can apply for one under Part 1A of the Insolvency Act 1986",
     "eligible smaller companies can apply for a standalone moratorium under Part A1 of the Insolvency Act 1986"),

    # --- Finding 4: s.216 (and s.217) are in the Insolvency Act, not the CDDA ---
    ("68120_can-you-sell-your-insolvent-company", "F4",
     "Section 216 of the Company Directors Disqualification Act 1986 prohibits you",
     "Section 216 of the Insolvency Act 1986 prohibits you"),

    # --- Finding 5: DRD is s.51 + Sch 8; Part 2 is inheritance tax rate bands ---
    ("13029_understanding-hmrc-debt-collection", "F5",
     "Under Part 2 of the Finance (No. 2) Act 2015, HMRC can take tax debts",
     f"Under {DRD}, HMRC can take tax debts"),
    ("77162_hmrc-enforcement-action", "F5",
     "directly from company bank accounts under Part 2 of the Finance (No. 2) Act 2015.",
     f"directly from company bank accounts under {DRD}."),
    ("79563_what-happens-if-hmrc-freezes-your-business-bank-account", "F5",
     "directly from company bank accounts, under Part 2 of the Finance (No. 2) Act 2015.",
     f"directly from company bank accounts, under {DRD}."),

    # --- Finding 12: s.94 is the final account; dissolution timing is s.201 ---
    ("7676_members-voluntary-liquidation", "F12",
     "<p>There is no final general meeting; that requirement was removed in 2015. Once the work is done, the liquidator prepares a final account showing how the winding up was conducted, sends it to the members, and files it with the required return at Companies House. Under section 94 of the Insolvency Act 1986, the company is then dissolved three months after that account is registered.</p>",
     "<p>There is no final general meeting; that requirement was removed in 2015. Once the work is done, the liquidator prepares a final account showing how the winding up was conducted, sends it to the members, and files it with the required return at Companies House.</p>\n"
     "<p>Section 94 of the Insolvency Act 1986 governs that final account. Dissolution follows three months after the registrar registers the return, under section 201.</p>"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write changes (default is a dry run)")
    args = ap.parse_args()

    by_file = {}
    for slug, finding, old, new in FIXES:
        by_file.setdefault(slug, []).append((finding, old, new))

    errors = []
    changed = 0
    for slug, items in by_file.items():
        path = os.path.join(DRAFTS, slug + ".html")
        if not os.path.exists(path):
            errors.append(f"{slug}: draft not found at {path}")
            continue
        with open(path, encoding="utf-8") as fh:
            original = fh.read()
        text = original
        for finding, old, new in items:
            n = text.count(old)
            if n != 1:
                errors.append(f"{slug} [{finding}]: expected exactly 1 match, found {n}")
                continue
            text = text.replace(old, new)
            print(f"  {slug}  [{finding}]  OK")
        if text != original:
            changed += 1
            if args.apply:
                with open(path, "w", encoding="utf-8", newline="") as fh:
                    fh.write(text)

    print()
    if errors:
        print("FAILED - nothing written for the pages listed below:")
        for e in errors:
            print("  !! " + e)
        sys.exit(1)

    verb = "updated" if args.apply else "would update"
    print(f"{len(FIXES)} replacements across {len(by_file)} pages; {verb} {changed} files.")
    if not args.apply:
        print("Dry run. Re-run with --apply to write.")


if __name__ == "__main__":
    main()
