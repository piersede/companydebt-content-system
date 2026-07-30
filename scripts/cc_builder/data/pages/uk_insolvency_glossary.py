"""Page config for: Glossary of UK Insolvency Terms

Live at /liquidation/uk-insolvency-glossary/ (WP pages 79404).

Adopted into Bernstein by registration only -- no content was regenerated.
Page class ("uk-insolvency-glossary" -> "entity_owner") sits in
scripts/page_runtime_metadata.py SLUG_PAGE_CLASS_OVERRIDES.

verification_date is the date the draft was last changed in git, not a claim
that the page has been fact-checked since. It exists so the runtime router can
infer an honest freshness tier.

Slim config -- only the fields the Bernstein pipeline and runtime-pack router
read. Content is read directly from drafts/79404_uk-insolvency-glossary.html.
"""

PAGE_CONFIG = {
    'slug': "uk-insolvency-glossary",
    'page_type': "definition",
    'wp_page_id': 79404,
    'title': "Glossary of UK Insolvency Terms",
    'verification_date': "20 May 2026",
}
