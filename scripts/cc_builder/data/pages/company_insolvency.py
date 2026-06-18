"""Page config for: UK Company Insolvency Data and Statistics

Insolvency-page slim config — only the fields the Bernstein pipeline
and runtime-pack router actually read. Page-class routing for this
slug (data_reference) sits in scripts/page_runtime_metadata.py.
"""

PAGE_CONFIG = {
    # The insolvency data hub now lives at /data/ itself (WP page 79845, slug
    # 'data'); the old /data/company-insolvency/ page (79846) has been retired
    # and 301s here. Draft content is drafts/79845_data.html.
    'slug': 'data',
    'page_type': 'data_reference',
    'wp_page_id': 79845,
    'title': 'UK Company Insolvency Data and Statistics',
    'verification_date': '18 June 2026',
}
