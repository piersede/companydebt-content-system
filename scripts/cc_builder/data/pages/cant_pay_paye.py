"""Page config for: A Guide to PAYE Arrears

HMRC-family page at /hmrc/cant-pay-paye/, sibling to cant_pay_vat and
problems_paying_corporation_tax_hmrc. Covers why PAYE arrears escalate
faster than other tax debts: personal liability notices, secondary
preferential status, and RTI leaving no ambiguity about the amount.

This is a slim insolvency-page config -- only the fields the Bernstein pipeline
and runtime-pack router actually read. Content is read directly from
drafts/8324_cant-pay-paye.html.
"""

PAGE_CONFIG = {
    'slug': 'cant-pay-paye',
    'page_type': 'process_guide',
    'wp_page_id': 8324,
    'title': 'A Guide to PAYE Arrears',
    'verification_date': '30 July 2026',
}
