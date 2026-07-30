"""Page config for: HMRC Penalties and Investigations.

HMRC penalties page at /hmrc/hmrc-penalties-investigations/ (WordPress PAGE id 76920,
template templates/take-the-test-template.php). Registered as editorial
'process_guide' so build_page reads the authored draft
drafts/76920_hmrc-penalties-investigations.html directly. Page-class routing
('enforcement') lives in scripts/page_runtime_metadata.py
SLUG_PAGE_CLASS_OVERRIDES.
"""

PAGE_CONFIG = {
    'slug': 'hmrc-penalties-investigations',
    'page_type': 'process_guide',
    'page_class': 'enforcement',
    'wp_page_id': 76920,
    'title': 'HMRC Penalties and Investigations',
    'verification_date': '30 July 2026',
}
