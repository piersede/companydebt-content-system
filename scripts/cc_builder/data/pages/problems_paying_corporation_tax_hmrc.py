"""Page config for: Can't Pay Corporation Tax: What are the Options?

HMRC tax-debt triage page at /hmrc/problems-paying-corporation-tax-hmrc/.
Covers what happens when a company cannot pay its Corporation Tax bill, the
HMRC enforcement arc, Time to Pay, and the director-level decisions that
follow. Sibling page to cant-pay-vat and cant-pay-paye in the same HMRC
tax-debt family. Page-class override ("problems-paying-corporation-tax-hmrc"
-> "trigger") sits in scripts/page_runtime_metadata.py SLUG_PAGE_CLASS_OVERRIDES.

This is a slim insolvency-page config -- only the fields the Bernstein pipeline
and runtime-pack router actually read. Content is read directly from
drafts/8408_problems-paying-corporation-tax-hmrc.html.
"""

PAGE_CONFIG = {
    'slug': 'problems-paying-corporation-tax-hmrc',
    'page_type': 'definition',
    'wp_page_id': 8408,
    'title': "Can't Pay Corporation Tax: What are the Options?",
    'verification_date': '23 July 2026',
}
