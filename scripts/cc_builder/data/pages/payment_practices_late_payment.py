"""Page config for: Payment Practices & Late Payment (UK Data)

Slim data_reference config. ENRICHMENT-only late-payment context, NOT an
insolvency statistic and never blended into insolvency figures. Page-class
routing for this slug (data_reference) sits in scripts/page_runtime_metadata.py.
"""

PAGE_CONFIG = {
    'slug': 'payment-practices-late-payment',
    'page_type': 'data_reference',
    'wp_page_id': 79850,
    'title': 'Payment Practices & Late Payment (UK Data)',
    'verification_date': '18 June 2026',
}
