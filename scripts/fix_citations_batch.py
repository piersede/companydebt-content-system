"""Reference-block-only citation corrections from the 2026-07-30 citation accuracy audit.

Scope: the 17 page-findings where the incorrect citation appears ONLY inside a
Sources & References or Methodology block. No body prose is touched, so no
humanise pass is required for these pages.

Body-prose findings (74891, 9702, 68120, 13029, 77162, 79563, 77157, 7676) are
deliberately NOT handled here. They go through Bernstein per page.

Every replacement is an exact string match. A miss is a hard error, not a warning,
so a silently-stale expectation cannot pass as a successful fix.

Usage:
    python scripts/fix_citations_batch.py            # dry run, shows the diff
    python scripts/fix_citations_batch.py --apply    # write
"""
import argparse
import os
import sys

DRAFTS = "drafts"

FA2020_S98 = "https://www.legislation.gov.uk/ukpga/2020/14/section/98"
DRD_S51 = "https://www.legislation.gov.uk/ukpga/2015/33/section/51"

# (slug, finding, old_exact, new_exact)
FIXES = [
    # --- Finding 1: FA 2020 Schedule 26 does not exist (FA 2020 has 16 Schedules) ---
    ("7665_company-rescue-solutions", "F1",
     '<li><a href="https://www.legislation.gov.uk/ukpga/2020/14/schedule/26">Finance Act 2020, Schedule 26 (Crown preference reinstatement)</a>',
     f'<li><a href="{FA2020_S98}">Finance Act 2020, section 98 (Crown preference reinstatement)</a>'),
    ("77146_debt-creditor-pressure-hub", "F1",
     '<li><a href="https://www.legislation.gov.uk/ukpga/2020/14/schedule/26">Finance Act 2020, Schedule 26 (Crown preference reinstatement)</a>',
     f'<li><a href="{FA2020_S98}">Finance Act 2020, section 98 (Crown preference reinstatement)</a>'),
    ("77372_company-rescue-recovery-hub", "F1",
     '<li><a href="https://www.legislation.gov.uk/ukpga/2020/14/schedule/26">Finance Act 2020, Schedule 26 (Crown preference reinstatement)</a>',
     f'<li><a href="{FA2020_S98}">Finance Act 2020, section 98 (Crown preference reinstatement)</a>'),

    # --- Findings 1 + 7: Sch 26 wrong, and FA 2020 did not introduce PLNs (SSAA 1992 s.121C did) ---
    # Split across paragraphs: naming the three separate instruments in one sentence
    # pushes the paragraph past the 400-char check-20 ceiling.
    ("79342_hmrc-as-a-creditor-in-liquidation", "F1+F7",
     "<p>We have drawn on the Insolvency Act 1986 (sections 122 on winding-up by the court, 127 on void dispositions, 175 on preferential debts, and 176ZA on expenses), the Finance Act 2020 (Schedule 26 reinstating HMRC secondary preferential status and introducing Personal Liability Notices and Joint and Several Liability Notices), and current HMRC and Insolvency Service guidance.</p>",
     "<p>We have drawn on the Insolvency Act 1986 (sections 122 on winding-up by the court, 127 on void dispositions, 175 on preferential debts, and 176ZA on expenses).</p>\n"
     "<p>For HMRC's own powers we have used the Finance Act 2020: section 98 reinstating secondary preferential status, and section 100 with Schedule 13 on Joint and Several Liability Notices.</p>\n"
     "<p>Personal Liability Notices come from the Social Security Administration Act 1992, section 121C. We have also used current HMRC and Insolvency Service guidance.</p>"),

    # --- Finding 2: FA 2020 Schedule 28 does not exist ---
    ("77739_which-creditors-get-paid-first", "F2",
     "the Finance Act 2020 (Schedule 28 on HMRC secondary preferential creditor status from 1 December 2020)",
     "the Finance Act 2020 (section 98 on HMRC secondary preferential creditor status from 1 December 2020)"),

    # --- Finding 8: FA 2020 Sch 2 is "The loan charge: consequential amendments" ---
    ("20428_vs-liquidation", "F8",
     '<li><a href="https://www.legislation.gov.uk/ukpga/2020/14/schedule/2">Finance Act 2020, Schedule 2 (Crown preference reinstatement, in force 1 December 2020)</a>',
     f'<li><a href="{FA2020_S98}">Finance Act 2020, section 98 (Crown preference reinstatement, in force 1 December 2020)</a>'),

    # --- Finding 9: FA 2020 Sch 9 is "DST payment notices" ---
    ("79498_pay-hmrc-or-suppliers-first", "F9",
     '<li><a href="https://www.legislation.gov.uk/ukpga/2020/14/schedule/9">Finance Act 2020, Schedule 9 (HMRC secondary preferential status)</a>',
     f'<li><a href="{FA2020_S98}">Finance Act 2020, section 98 (HMRC secondary preferential status)</a>'),

    # --- Finding 5: F(No.2)A 2015 Part 2 is inheritance tax rate bands; DRD is s.51 + Sch 8 ---
    ("77205_hmrc-debt-enforcement-hub", "F5",
     '<li><a href="https://www.legislation.gov.uk/ukpga/2015/33/contents">Finance (No. 2) Act 2015, Part 2 (Direct Recovery of Debts)</a>',
     f'<li><a href="{DRD_S51}">Finance (No. 2) Act 2015, section 51 and Schedule 8 (Direct Recovery of Debts)</a>'),
    ("79580_can-hmrc-shut-down-my-business", "F5",
     '<li><a href="https://www.legislation.gov.uk/ukpga/2015/33/contents">Finance (No. 2) Act 2015, Part 2 (Direct Recovery of Debts)</a>',
     f'<li><a href="{DRD_S51}">Finance (No. 2) Act 2015, section 51 and Schedule 8 (Direct Recovery of Debts)</a>'),
    ("79588_what-happens-if-you-ignore-hmrc-letters", "F5",
     '<li><a href="https://www.legislation.gov.uk/ukpga/2015/33/contents">Finance (No. 2) Act 2015, Part 2 (Direct Recovery of Debts)</a>',
     f'<li><a href="{DRD_S51}">Finance (No. 2) Act 2015, section 51 and Schedule 8 (Direct Recovery of Debts)</a>'),
    ("79596_what-happens-if-hmrc-rejects-your-time-to-pay-arrangement", "F5",
     '<li><a href="https://www.legislation.gov.uk/ukpga/2015/33/contents">Finance (No. 2) Act 2015, Part 2 (Direct Recovery of Debts)</a>',
     f'<li><a href="{DRD_S51}">Finance (No. 2) Act 2015, section 51 and Schedule 8 (Direct Recovery of Debts)</a>'),
    ("8350_hmrc-threatening-letters", "F5",
     '<li><a href="https://www.legislation.gov.uk/ukpga/2015/33/contents">Finance (No. 2) Act 2015, Part 2 (Direct Recovery of Debts)</a>',
     f'<li><a href="{DRD_S51}">Finance (No. 2) Act 2015, section 51 and Schedule 8 (Direct Recovery of Debts)</a>'),
    ("11788_frozen-bank-account", "F5",
     '<li><a href="https://www.legislation.gov.uk/ukpga/2015/33/contents"><strong>Finance (No. 2) Act 2015, Part 2</strong>',
     f'<li><a href="{DRD_S51}"><strong>Finance (No. 2) Act 2015, section 51 and Schedule 8</strong>'),
    ("67809_hmrc", "F5",
     '<li><a href="https://www.legislation.gov.uk/ukpga/2015/33/contents"><strong>Finance (No. 2) Act 2015, Part 2</strong>',
     f'<li><a href="{DRD_S51}"><strong>Finance (No. 2) Act 2015, section 51 and Schedule 8</strong>'),

    # --- Finding 10: IR 2016 Part 4 is Receivership; CVL is Part 6 ---
    ("79445_list-of-liquidation-documents", "F10",
     '<li><a href="https://www.legislation.gov.uk/uksi/2016/1024/contents/made">Insolvency (England and Wales) Rules 2016, Part 4 (statement of affairs in CVL)</a>',
     '<li><a href="https://www.legislation.gov.uk/uksi/2016/1024/part/6">Insolvency (England and Wales) Rules 2016, Part 6 (statement of affairs in CVL)</a>'),

    # --- Finding 11: s.126 is the compulsory track (post-petition), not voluntary liquidation ---
    ("79360_ccj-when-going-insolvent", "F11-sources",
     '<li><a href="https://www.legislation.gov.uk/ukpga/1986/45/section/126">Insolvency Act 1986, section 126 (stay of proceedings, voluntary)</a>',
     '<li><a href="https://www.legislation.gov.uk/ukpga/1986/45/section/126">Insolvency Act 1986, section 126 (power to stay proceedings once a winding-up petition has been presented)</a>'),
    # Split across paragraphs for the same check-20 reason as 79342 above.
    ("79360_ccj-when-going-insolvent", "F11-methodology",
     "<p>We have drawn on the Insolvency Act 1986 (section 123(1)(b) on insolvency evidenced by an unsatisfied judgement, section 126 on stay of proceedings in voluntary liquidation, section 130 on stay in compulsory liquidation, and section 239 on preferences), the Civil Procedure Rules (Part 12 on default judgement and Part 13 on setting aside), and current Insolvency Service and HMCTS guidance.</p>",
     "<p>We have drawn on the Insolvency Act 1986: section 123(1)(b) on insolvency evidenced by an unsatisfied judgement, and section 239 on preferences.</p>\n"
     "<p>On stays, section 126 covers staying proceedings once a winding-up petition has been presented, and section 130 the automatic stay that follows a winding-up order.</p>\n"
     "<p>We have also used the Civil Procedure Rules (Part 12 on default judgement and Part 13 on setting aside) and current Insolvency Service and HMCTS guidance.</p>"),

    # --- Finding 13: s.121C is in the Social Security ADMINISTRATION Act (1992 c.5), not c.4 ---
    ("41082_can-personal-assets-of-directors-be-seized-from-a-ltd-company", "F13",
     '<li><a href="https://www.legislation.gov.uk/ukpga/1992/4/section/121C">HMRC personal liability notices for directors (Social Security Contributions and Benefits Act 1992 s.121C)</a>',
     '<li><a href="https://www.legislation.gov.uk/ukpga/1992/5/section/121C">HMRC personal liability notices for directors (Social Security Administration Act 1992 s.121C)</a>'),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write changes (default is a dry run)")
    args = ap.parse_args()

    # group by file so multi-fix pages are written once
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
        print("FAILED - no partial state was written for the pages listed below:")
        for e in errors:
            print("  !! " + e)
        sys.exit(1)

    verb = "updated" if args.apply else "would update"
    print(f"{len(FIXES)} replacements across {len(by_file)} pages; {verb} {changed} files.")
    if not args.apply:
        print("Dry run. Re-run with --apply to write.")


if __name__ == "__main__":
    main()
