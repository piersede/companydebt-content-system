"""Page config for: What Is the Corporate Insolvency Test? A UK Director's Guide Under the Insolvency Act 1986

Live at /insolvency-calculator/ (WP pages 13600).

The draft slug (insolvency-test) differs from the live URL slug (insolvency-calculator); the config keeps the draft slug because
build_page.py resolves content from drafts/{wp_page_id}_{slug}.html.

Adopted into Bernstein by registration only -- no content was regenerated.
Page class ("insolvency-test" -> "trigger") sits in
scripts/page_runtime_metadata.py SLUG_PAGE_CLASS_OVERRIDES.

verification_date is the date the draft was last changed in git, not a claim
that the page has been fact-checked since. It exists so the runtime router can
infer an honest freshness tier.

Slim config -- only the fields the Bernstein pipeline and runtime-pack router
read. Content is read directly from drafts/13600_insolvency-test.html.
"""

PAGE_CONFIG = {
    'slug': "insolvency-test",
    'page_type': "definition",
    'wp_page_id': 13600,
    'title': "What Is the Corporate Insolvency Test? A UK Director's Guide Under the Insolvency Act 1986",
    'verification_date': "08 July 2026",
}
