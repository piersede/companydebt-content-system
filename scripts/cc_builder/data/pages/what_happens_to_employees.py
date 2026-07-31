"""Page config for: What Happens to Employees in Liquidation?

Liquidation-section page at /liquidation/what-happens-to-employees/. Covers
the National Insurance Fund safety net, Redundancy Payments Service claims,
preferential status under Schedule 6, and the director duties around telling
staff early.

Page-class override ("what-happens-to-employees" -> "process_guide") already
sits in scripts/page_runtime_metadata.py.

Content is read directly from drafts/15010_what-happens-to-employees.html.
"""

PAGE_CONFIG = {
    'slug': 'what-happens-to-employees',
    'page_type': 'process_guide',
    'wp_page_id': 15010,
    'title': 'What Happens to Employees in Liquidation? Redundancy Rights and Payments in the UK',
    'verification_date': '30 July 2026',
}
