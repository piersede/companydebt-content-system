"""Page config for: A Guide to PAYE Arrears

Live at /hmrc/cant-pay-paye/ (WP pages 8324).

Adopted into Bernstein by registration only -- no content was regenerated.
Page class ("cant-pay-paye" -> "trigger") sits in
scripts/page_runtime_metadata.py SLUG_PAGE_CLASS_OVERRIDES.

verification_date is the date the draft was last changed in git, not a claim
that the page has been fact-checked since. It exists so the runtime router can
infer an honest freshness tier.

Slim config -- only the fields the Bernstein pipeline and runtime-pack router
read. Content is read directly from drafts/8324_cant-pay-paye.html.
"""

PAGE_CONFIG = {
    'slug': "cant-pay-paye",
    'page_type': "definition",
    'wp_page_id': 8324,
    'title': "A Guide to PAYE Arrears",
    'verification_date': "16 July 2026",
}
