"""Page config for: Pub Closures in the UK: How Many, and Why.

Article at /articles/pub-closures-in-the-uk/ (WordPress POST id 24589), a
data-hub-style rebuild (KPI strip, charts, sourced stats). Not previously
registered in Bernstein -- adopted per reference_bernstein_adopt_existing
memory so the existing, already-live draft comes under pipeline tracking
instead of being edited directly.

Registered as 'data_reference' so build_page reads the authored draft HTML
directly (drafts/24589_pub-closures-in-the-uk.html). Push to the POST via
wp_push.py (this is a post, not a page) -- staging only.

Slim config -- only the fields the Bernstein pipeline and runtime-pack router
read.
"""

PAGE_CONFIG = {
    'slug': 'pub-closures-in-the-uk',
    'page_type': 'data_reference',
    'page_class': 'data_reference',
    'wp_page_id': 24589,
    'title': 'Pub Closures in the UK: How Many, and Why (2026 Data)',
    'verification_date': '8 July 2026',
}
