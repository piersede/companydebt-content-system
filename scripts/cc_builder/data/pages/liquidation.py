"""Page config for: What Is Company Liquidation?

Definition / explainer page covering the three statutory liquidation routes
(CVL, Compulsory, MVL) at the top of /liquidation/. Page-class override
("liquidation" -> "entity_owner") sits in scripts/page_runtime_metadata.py.

This is a slim insolvency-page config — only the fields the Bernstein pipeline
and runtime-pack router actually read. Insolvency pages do not carry the hero
zone, info_gain map, or section configs that credit-card pages need.
"""

PAGE_CONFIG = {
    'slug': 'liquidation',
    'page_type': 'definition',
    'wp_page_id': 7669,
    'title': 'Company Liquidation: Process, Costs and Director Advice',
    'verification_date': '15 April 2026',
}
