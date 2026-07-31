"""Page config for: Sample Letters Hub

Live at /sample-letters/ (WP pages 53253).

The draft slug (sample-letters-hub) differs from the live URL slug (sample-letters); the config keeps the draft slug because
build_page.py resolves content from drafts/{wp_page_id}_{slug}.html.

Adopted into Bernstein by registration only -- no content was regenerated.
Page class ("sample-letters-hub" -> "entity_owner") sits in
scripts/page_runtime_metadata.py SLUG_PAGE_CLASS_OVERRIDES.

verification_date is the date the draft was last changed in git, not a claim
that the page has been fact-checked since. It exists so the runtime router can
infer an honest freshness tier.

Slim config -- only the fields the Bernstein pipeline and runtime-pack router
read. Content is read directly from drafts/53253_sample-letters-hub.html.
"""

PAGE_CONFIG = {
    'slug': "sample-letters-hub",
    'page_type': "hub",
    'wp_page_id': 53253,
    'title': "Sample Letters Hub",
    'verification_date': "26 May 2026",
}
