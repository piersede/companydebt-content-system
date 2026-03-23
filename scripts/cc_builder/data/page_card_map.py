"""Master card-to-page mapping for all 19 credit card pages.

This is the reference for which cards appear on each page.
Each page config in data/pages/ should use these assignments.
"""

PAGE_CARD_MAP = {

    # ── ROUNDUP PAGES ─────────────────────────────────────────────────────

    'best-business-credit-cards': {
        'page_type': 'roundup',
        'card_ids': [
            'capital_on_tap', 'barclaycard', 'funding_circle_cashback',
            'moss', 'santander', 'lloyds', 'natwest', 'hsbc',
            'metro_bank', 'amex_business_gold', 'ba_amex_accelerating',
            'amex_business_platinum', 'lloyds_charge', 'barclaycard_charge',
            'funding_circle_flexipay',
        ],
        'separate_card_ids': [
            'natwest_business_plus', 'rbs', 'amazon_amex', 'cooperative_charge',
        ],
    },

    'best-business-credit-cards-for-sole-traders': {
        'page_type': 'roundup',
        'card_ids': [
            'barclaycard', 'lloyds', 'metro_bank', 'amex_business_gold',
            'amex_business_basic', 'ba_amex_accelerating',
            'funding_circle_cashback', 'natwest_business_plus',
        ],
        'separate_card_ids': [
            'capital_on_tap', 'santander', 'hsbc',
        ],
    },

    'best-cashback-and-reward': {
        'page_type': 'roundup',
        'card_ids': [
            'amex_business_gold', 'ba_amex_accelerating', 'amex_business_platinum',
            'amex_business_basic', 'amazon_amex', 'santander', 'barclaycard',
            'capital_on_tap', 'funding_circle_cashback', 'natwest_business_plus', 'rbs',
        ],
        'separate_card_ids': [
            'moss', 'barclays_premium_plus',
        ],
    },

    'best-credit-cards-for-start-ups': {
        'page_type': 'roundup',
        'card_ids': [
            'barclaycard', 'capital_on_tap', 'moss', 'funding_circle_cashback',
            'funding_circle_flexipay', 'amex_business_basic', 'amex_business_gold',
        ],
        'separate_card_ids': [
            'lloyds', 'natwest', 'metro_bank', 'barclays_premium_plus',
        ],
    },

    'poor-credit': {
        'page_type': 'roundup',
        'card_ids': [
            'capital_on_tap', 'funding_circle_cashback', 'funding_circle_flexipay',
            'moss', 'barclaycard',
        ],
        'separate_card_ids': [
            'lloyds', 'natwest',
        ],
    },

    'the-best-interest-free-credit-cards': {
        'page_type': 'roundup',
        'card_ids': [
            'barclaycard', 'amex_business_gold', 'amex_business_basic',
            'amex_business_platinum', 'capital_on_tap',
            'lloyds', 'metro_bank', 'hsbc',
        ],
        'separate_card_ids': [
            'natwest', 'santander', 'barclaycard_charge',
            'lloyds_charge', 'cooperative_charge',
        ],
    },

    'what-are-the-best-business-credit-cards-for-travel': {
        'page_type': 'roundup',
        'card_ids': [
            'ba_amex_accelerating', 'amex_business_platinum', 'amex_business_gold',
            'natwest', 'capital_on_tap', 'natwest_business_plus',
        ],
        'separate_card_ids': [
            'barclaycard', 'lloyds', 'funding_circle_cashback', 'moss',
        ],
    },

    'best-cards-with-air-miles-avios': {
        'page_type': 'roundup',
        'card_ids': [
            'ba_amex_accelerating', 'amex_business_gold', 'amex_business_platinum',
            'amex_business_basic', 'capital_on_tap',
        ],
        'separate_card_ids': [
            'amazon_amex', 'natwest_business_plus', 'barclays_premium_plus',
        ],
    },

    'instant-approval-business-credit-cards': {
        'page_type': 'roundup',
        'card_ids': [
            'capital_on_tap', 'moss', 'funding_circle_cashback',
            'funding_circle_flexipay', 'barclaycard',
        ],
        'separate_card_ids': [
            'amex_business_basic', 'amex_business_gold', 'lloyds', 'metro_bank',
        ],
    },

    'best-business-charge-cards': {
        'page_type': 'roundup',
        'card_ids': [
            'amex_business_gold', 'amex_business_platinum', 'lloyds_charge',
            'barclaycard_charge', 'cooperative_charge', 'natwest_onecard',
            'funding_circle_flexipay',
        ],
        'separate_card_ids': [
            'ba_amex_accelerating', 'amex_business_basic', 'moss',
        ],
    },

    # ── REVIEWS ───────────────────────────────────────────────────────────

    'capital-on-tap-review': {
        'page_type': 'review',
        'card_ids': ['capital_on_tap'],
        'separate_card_ids': ['barclaycard', 'moss', 'funding_circle_cashback'],
    },

    'funding-circle-business-credit-card-review': {
        'page_type': 'review',
        'card_ids': ['funding_circle_cashback'],
        'separate_card_ids': ['capital_on_tap', 'barclaycard', 'santander'],
    },

    'flexipay-review': {
        'page_type': 'review',
        'card_ids': ['funding_circle_flexipay'],
        'separate_card_ids': ['capital_on_tap', 'moss', 'amex_business_gold', 'barclaycard_charge'],
    },

    # ── BRAND COMPARISONS ─────────────────────────────────────────────────

    'compare-barclaycard-business-credit-cards': {
        'page_type': 'brand_comparison',
        'card_ids': ['barclaycard', 'barclaycard_charge', 'barclays_premium_plus'],
        'separate_card_ids': ['capital_on_tap', 'amex_business_gold'],
    },

    'compare-american-express-business-credit-cards': {
        'page_type': 'brand_comparison',
        'card_ids': [
            'amex_business_gold', 'amex_business_platinum', 'amex_business_basic',
            'ba_amex_accelerating', 'amazon_amex',
        ],
        'separate_card_ids': ['capital_on_tap', 'barclaycard'],
    },

    'capital-on-tap-vs-amex': {
        'page_type': 'brand_comparison',
        'card_ids': ['capital_on_tap', 'amex_business_gold'],
        'separate_card_ids': [
            'amex_business_basic', 'ba_amex_accelerating',
            'barclaycard', 'funding_circle_cashback',
        ],
    },

    # ── GUIDES ────────────────────────────────────────────────────────────

    'guide-to-business-credit-cards': {
        'page_type': 'guide',
        'card_ids': [],
        'separate_card_ids': [
            'barclaycard', 'capital_on_tap', 'lloyds',
            'amex_business_gold', 'ba_amex_accelerating',
        ],
    },

    'business-credit-cards-vs-charge-cards': {
        'page_type': 'guide',
        'card_ids': [],
        'separate_card_ids': [
            'amex_business_gold', 'amex_business_platinum', 'lloyds_charge',
            'barclaycard_charge', 'barclaycard', 'capital_on_tap',
            'funding_circle_flexipay',
        ],
    },

    'what-is-a-balance-transfer-credit-card': {
        'page_type': 'guide',
        'card_ids': [],
        'separate_card_ids': [
            'barclaycard', 'lloyds', 'metro_bank', 'capital_on_tap',
        ],
    },
}
