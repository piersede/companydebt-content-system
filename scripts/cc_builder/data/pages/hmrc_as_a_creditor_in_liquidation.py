"""Page config for: HMRC as a Creditor in Liquidation

Liquidation-section page at /liquidation/hmrc-as-a-creditor-in-liquidation/.
Covers HMRC's secondary preferential status since 1 December 2020, what that
did to bank and supplier recovery, HMRC's voting power in formal procedures,
and the personal-liability routes HMRC can use against a director.

Page-class override ("hmrc-as-a-creditor-in-liquidation" -> "enforcement")
already sits in scripts/page_runtime_metadata.py SLUG_PAGE_CLASS_OVERRIDES.

Content is read directly from
drafts/79342_hmrc-as-a-creditor-in-liquidation.html.
"""

PAGE_CONFIG = {
    'slug': 'hmrc-as-a-creditor-in-liquidation',
    'page_type': 'definition',
    'wp_page_id': 79342,
    'title': 'HMRC as a Creditor in Liquidation: What to Expect',
    'verification_date': '30 July 2026',
}
