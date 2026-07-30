"""Page config for: HMRC Security Bonds

Live at /hmrc/security-bond-notices/ (WP pages 10564).

Adopted into Bernstein by registration only -- no content was regenerated.
Page class ("security-bond-notices" -> "enforcement") sits in
scripts/page_runtime_metadata.py SLUG_PAGE_CLASS_OVERRIDES.

verification_date is the date the draft was last changed in git, not a claim
that the page has been fact-checked since. It exists so the runtime router can
infer an honest freshness tier.

Slim config -- only the fields the Bernstein pipeline and runtime-pack router
read. Content is read directly from drafts/10564_security-bond-notices.html.
"""

PAGE_CONFIG = {
    'slug': "security-bond-notices",
    'page_type': "process_guide",
    'wp_page_id': 10564,
    'title': "HMRC Security Bonds",
    'verification_date': "20 May 2026",
}
