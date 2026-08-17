# Draft request to the Insolvency Service statistics team

**Status:** draft for Piers to review and send. Not sent.
**To:** statistics@insolvency.gov.uk
**Written:** 15 August 2026

Context for whoever sends it: the published record-level file stops at April 2024.
We are working to June 2026, so 26 months are missing. Everything asked for below
is grounded in the checks recorded in `docs/data-hub/insolvency-intelligence-spec.md`
and the commit "Add the official record-level insolvency dataset, and validate it".

The two data-quirk notes at the end are optional. They are genuine feedback from
using the file properly, they cost the reader nothing, and they make it obvious we
are not asking speculatively. Cut them if you would rather keep the email short.

---

**Subject:** Request for updated record-level company insolvency data (following the January 2012 to April 2024 release)

Dear Insolvency Service statistics team,

I am writing from Company Debt, a licensed insolvency practice. We publish a set of
free, sourced statistics pages built on your monthly company insolvency releases,
covering the national picture, the individual procedures and around twenty
industries at three-digit SIC level.

We have been using your record-level release, "Underlying data for company
insolvency statistics, England, Wales and Scotland, January 2012 to April 2024",
published on 23 May 2024. Following the filtering guidance in the README, we
reproduced your published annual totals for England and Wales to within 0.04 per
cent, so we are confident we are reading it as intended.

**Our request**

Is an updated record-level extract available covering the period since April 2024,
ideally through the most recent published month?

If it is, we would be grateful to know:

1. Which month the data would run to, and whether updates are issued on any regular basis.
2. Whether the updated extract retains the bulk insolvency flag, and the SIC breakdown at three digits and finer.
3. Whether there is any charge, and what terms apply. We assume the Open Government Licence as before, but would rather confirm than presume.
4. Whether an update would be issued as a public ad-hoc release, which we would prefer, since other users would benefit and we could cite a public source rather than a private supply.

**Why we are asking**

Two things in the record-level data are not available from the aggregate tables,
and both directly improve the accuracy of what we publish.

The first is the bulk insolvency flag. Bulk and connected-company events distort
monthly figures severely, and the effect is not evenly spread across industries. In
your published file, December 2016 carried 1,704 bulk cases against 1,171 other
insolvencies, and almost all of them fell in a single SIC group. At present we
handle this by reading your monthly commentary and writing the caveat onto each
affected page by hand, which is slow and easy to get wrong. With the flag we can
calculate the underlying trend directly and show readers both figures.

The second is the industry breakdown by procedure. We understand that the detailed
sector procedure tables are published quarterly. Because the record-level file
carries both the procedure and the SIC code on each row, it allows a monthly view
for a given industry, which is the question our readers most often ask.

**How we would use it**

We publish aggregate, sector-level statistics only. We would not publish
company-level data, and we note the statement in your README that the dataset is
provided for statistical purposes only and should not be used to determine whether
a particular company is insolvent. Every figure we publish is attributed to the
Insolvency Service, with our own calculations labelled separately as ours.

**Two small notes on the published file**

Offered only in case they are useful for a future release. Neither caused us any
lasting difficulty.

- The metadata file names the bulk column `isBulk`, while the header in
  `record-level-data.csv` is `is_bulk`.
- The README suggests filtering on the bulk variable being "Y" or "N". In the file,
  bulk cases are marked "Y" and all other rows carry an empty value rather than "N",
  so a filter written literally on "N" returns nothing.

Thank you for making the 2012 to 2024 file available. It is a genuinely useful
release, and an updated version would let us publish more accurate industry figures
than the aggregate tables allow on their own.

Kind regards,

[Name]
[Role], Company Debt
[Email] · [Phone]
https://www.companydebt.com/data/
