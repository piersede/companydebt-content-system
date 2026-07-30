"""Page config for: HMRC Winding Up Petitions: A UK Director's Guide

Child page of /winding-up-petitions/, covering the HMRC-specific petition:
the seven-day advertisement window, the section 127 backdating trap,
validation orders, and the pay / negotiate / administer decision.

Page-class override ("dealing-with-an-hmrc-winding-up-petition" ->
"enforcement") already sits in scripts/page_runtime_metadata.py
SLUG_PAGE_CLASS_OVERRIDES, matching the sibling petition pages.

This is a slim insolvency-page config -- only the fields the Bernstein pipeline
and runtime-pack router actually read. Content is read directly from
drafts/67438_dealing-with-an-hmrc-winding-up-petition.html.
"""

PAGE_CONFIG = {
    'slug': 'dealing-with-an-hmrc-winding-up-petition',
    'page_type': 'process_guide',
    'wp_page_id': 67438,
    'title': "HMRC Winding Up Petitions: A UK Director's Guide",
    'verification_date': '30 July 2026',
}
