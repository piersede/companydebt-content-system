"""Page config for: Can't Pay VAT? What Happens and What Directors Should Do

HMRC tax-debt triage page at /hmrc/cant-pay-vat/. Covers what happens when a
company cannot pay its VAT bill, the HMRC enforcement arc, Time to Pay, and the
director-level decisions that follow. Page-class override
("cant-pay-vat" -> "trigger") sits in scripts/page_runtime_metadata.py
SLUG_PAGE_CLASS_OVERRIDES.

This is a slim insolvency-page config -- only the fields the Bernstein pipeline
and runtime-pack router actually read. Content is read directly from
drafts/9443_cant-pay-vat.html.
"""

PAGE_CONFIG = {
    'slug': 'cant-pay-vat',
    'page_type': 'definition',
    'wp_page_id': 9443,
    'title': "Can't Pay VAT? What Happens and What Directors Should Do",
    'verification_date': '14 June 2026',
}
