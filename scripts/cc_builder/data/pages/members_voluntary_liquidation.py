"""Page config for: Members' Voluntary Liquidation (MVL) Explained

Route-guide / explainer page for the solvent-company liquidation route, at
/liquidation/members-voluntary-liquidation/. Page-class override
("members-voluntary-liquidation" -> "entity_owner") sits in
scripts/page_runtime_metadata.py SLUG_PAGE_CLASS_OVERRIDES.

This is a slim insolvency-page config — only the fields the Bernstein pipeline
and runtime-pack router actually read. Insolvency pages do not carry the hero
zone, info_gain map, or section configs that credit-card pages need. Content is
read directly from drafts/7676_members-voluntary-liquidation.html.
"""

PAGE_CONFIG = {
    'slug': 'members-voluntary-liquidation',
    'page_type': 'definition',
    'wp_page_id': 7676,
    'title': "Members' Voluntary Liquidation (MVL) Explained",
    'verification_date': '11 June 2026',
}
