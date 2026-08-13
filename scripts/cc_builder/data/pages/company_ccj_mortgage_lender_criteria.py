"""Page config for: Company CCJs and Mortgages: What 14 UK Lenders Actually Ask

Maintained lender study supporting /county-court-judgements/ (WP page 68076).

Records what 14 UK mortgage lenders publish about County Court Judgments
registered against a limited company, where the director's own credit file is
clean. Collected by hand in a browser on 12 August 2026, because lender
criteria sites block automated retrieval.

Dataset of record: research/lender-company-ccj-criteria.json. The draft table
and the dataset must agree; scripts/check_lender_criteria_freshness.py checks
the dataset's check dates against the agreed re-check cadence.

Maintenance cadence agreed with Piers on 12 August 2026:
  - Halifax, BM Solutions and Barclays  -> re-check monthly
  - the remaining 11 lenders            -> re-check every 6 months

Page ids differ by environment: staging 81464, LIVE 81458. `wp_page_id` below
is the staging id, because `build_page.py --publish` targets staging. For a
live push use `publish_to_live.py --id 81458`.

Went live 13 August 2026 after practitioner sign-off, together with the
corrected mortgage section on /county-court-judgements/ (live id 68076).

Slim config -- only the fields the Bernstein pipeline and runtime-pack router
read. Content is read directly from
drafts/81464_company-ccj-mortgage-lender-criteria.html.
"""

PAGE_CONFIG = {
    'slug': "company-ccj-mortgage-lender-criteria",
    'page_type': "process_guide",
    'wp_page_id': 81464,
    'title': "Company CCJs and Mortgages: What 14 UK Lenders Actually Ask",
    'verification_date': "12 August 2026",
}
