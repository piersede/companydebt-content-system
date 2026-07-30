"""Page config for: Winding-Up Petition: What Company Directors Must Do Now

Main petition guide at /winding-up-petitions/. Owns the primary "winding up
petition" query. Written for directors of limited companies in England and
Wales who have received, or expect to receive, a creditor or HMRC petition.

Page-class override ("winding-up-petitions" -> "enforcement") sits in
scripts/page_runtime_metadata.py SLUG_PAGE_CLASS_OVERRIDES, matching the
sibling petition pages.

This is a slim insolvency-page config -- only the fields the Bernstein pipeline
and runtime-pack router actually read. Content is read directly from
drafts/7687_winding-up-petitions.html.
"""

PAGE_CONFIG = {
    'slug': 'winding-up-petitions',
    'page_type': 'process_guide',
    'wp_page_id': 7687,
    'title': 'Winding-Up Petition: What Company Directors Must Do Now',
    'verification_date': '29 July 2026',
}
