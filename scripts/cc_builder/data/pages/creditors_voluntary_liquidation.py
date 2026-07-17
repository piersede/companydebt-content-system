"""Page config for: Creditors' Voluntary Liquidation (CVL)

Route-guide / explainer page for the insolvent-company director-led
liquidation route, at /liquidation/creditors-voluntary-liquidation/.
Page-class override ("creditors-voluntary-liquidation" -> "entity_owner")
sits in scripts/page_runtime_metadata.py SLUG_PAGE_CLASS_OVERRIDES.

This is a slim insolvency-page config — only the fields the Bernstein
pipeline and runtime-pack router actually read. Content is read directly
from drafts/7674_creditors-voluntary-liquidation.html.
"""

PAGE_CONFIG = {
    'slug': 'creditors-voluntary-liquidation',
    'page_type': 'definition',
    'wp_page_id': 7674,
    'title': "Creditors' Voluntary Liquidation (CVL): Practical Guide for UK Directors",
    'verification_date': '17 July 2026',
}
