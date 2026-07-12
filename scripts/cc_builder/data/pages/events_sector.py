"""Page config for: Insolvency and Business Rescue for the Events Sector.

Sector page at /sectors/events/ (WordPress POST id 49880, category 'sectors',
template templates/post-sectors.php). /sectors/ rewrite programme, clean
article rebuild on the lean template. Registered as editorial 'process_guide'
so build_page reads drafts/49880_events.html. Push via wp_push.py.
"""

PAGE_CONFIG = {
    'slug': 'events',
    'page_type': 'process_guide',
    'page_class': 'process_guide',
    'wp_page_id': 49880,
    'title': 'Insolvency and Business Rescue for the Events Sector',
    'verification_date': '12 July 2026',
}
