"""Page config for: Insolvency and Business Rescue for the Construction Sector.

Sector page at /sectors/construction/ (WordPress POST id 49778, category
'sectors', rendered by templates/post-sectors.php). Part of the /sectors/
rewrite programme: clean article rebuild with proper H1>H2>H3 structure and
genuine sector-specific research, replacing the old thin templated version.

Registered as an editorial 'process_guide' so build_page reads the authored
draft HTML directly (drafts/49778_construction.html). Push to the POST via
wp_push.py (these are posts, not pages).

Slim config -- only the fields the Bernstein pipeline and runtime-pack router
read.
"""

PAGE_CONFIG = {
    'slug': 'construction',
    'page_type': 'process_guide',
    'page_class': 'process_guide',
    'wp_page_id': 49778,
    'title': 'Insolvency and Business Rescue for the Construction Sector',
    'verification_date': '11 July 2026',
}
