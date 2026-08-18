"""Page config for: Liquidation Deadlines and Time Limits for Company Directors

Live at /liquidation/liquidation-deadlines-and-time-limits/ (WP pages 78690).

Adopted into Bernstein by registration only -- no content was regenerated.
Page class ("liquidation-deadlines-and-time-limits" -> "legal_compliance") sits in
scripts/page_runtime_metadata.py SLUG_PAGE_CLASS_OVERRIDES.

verification_date is the date the draft was last changed in git, not a claim
that the page has been fact-checked since. It exists so the runtime router can
infer an honest freshness tier.

Slim config -- only the fields the Bernstein pipeline and runtime-pack router
read. Content is read directly from drafts/78690_liquidation-deadlines-and-time-limits.html.
"""

PAGE_CONFIG = {
    'slug': "liquidation-deadlines-and-time-limits",
    'page_type': "process_guide",
    'wp_page_id': 78690,
    'title': "Liquidation Deadlines and Time Limits for Company Directors",
    'verification_date': "12 May 2026",
    # Yoast falls back to the excerpt when this is empty, and build_page sets the
    # excerpt to "Last reviewed <date>", which made the live search snippet read
    # "Last reviewed 12 May 2026". Set explicitly so that cannot recur.
    'meta_description': (
        "Liquidation deadlines for company directors in England and Wales: the "
        "14-day CVL window, winding-up petition dates, and what to do if you "
        "have missed one."
    ),
}
