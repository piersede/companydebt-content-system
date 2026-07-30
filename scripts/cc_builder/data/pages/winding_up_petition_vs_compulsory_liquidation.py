"""Page config for: Winding-Up Petition vs Compulsory Liquidation

Comparison page at /liquidation/winding-up-petition-vs-compulsory-liquidation/.
Separates the application (the petition) from the outcome (the order), and the
window between them where a director still has options.

Page-class override ("winding-up-petition-vs-compulsory-liquidation" ->
"enforcement") already sits in scripts/page_runtime_metadata.py
SLUG_PAGE_CLASS_OVERRIDES.

This is a slim insolvency-page config -- only the fields the Bernstein pipeline
and runtime-pack router actually read. Content is read directly from
drafts/79322_winding-up-petition-vs-compulsory-liquidation.html.
"""

PAGE_CONFIG = {
    'slug': 'winding-up-petition-vs-compulsory-liquidation',
    'page_type': 'definition',
    'wp_page_id': 79322,
    'title': 'Winding-Up Petition vs Compulsory Liquidation: Key Differences',
    'verification_date': '30 July 2026',
}
