"""Page config for: Construction Insolvency in the UK

Sector-specific insolvency explainer at /construction-insolvency/, distinct from
the /sectors/construction/ guide page (registered as 'construction' ->
construction_sector). This page is post 77157 and is <article>-wrapped, so it is
a normal editorial page rather than a data_reference passthrough.

Adopted into Bernstein on 2026-07-30 to fix a citation error found by the
citation accuracy audit (docs/audits/citation-accuracy-audit-2026-07-30.md,
finding 6): the page claimed HMRC could issue a Personal Liability Notice for
unpaid CIS deductions under Finance Act 2020 s.69. That section is "Recovery of
DST liability", and PLNs (Social Security Administration Act 1992 s.121C) reach
unpaid NIC only, never CIS. Adopted per the adopt-existing recipe, not
regenerated.

This is a slim config — only the fields the Bernstein pipeline and runtime-pack
router read. Content is read directly from
drafts/77157_construction-insolvency.html.
"""

# page_class is set explicitly rather than left to infer_page_class, which returns
# None for page_type 'definition' and would otherwise leave this page unclassified.
# The page's shape (assess whether recovery is possible -> options -> director
# risks -> what to do now) matches recovery_strategy, alongside peers such as
# should-i-close-my-company-or-try-to-save-it and alternatives-to-company-liquidation.
PAGE_CONFIG = {
    'slug': 'construction-insolvency',
    'page_type': 'definition',
    'page_class': 'recovery_strategy',
    'wp_page_id': 77157,
    'title': 'Construction Insolvency in the UK: Causes, Warning Signs & Rescue Options',
    'verification_date': '30 July 2026',
}
