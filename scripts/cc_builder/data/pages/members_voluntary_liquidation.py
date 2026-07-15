"""Page config for: Members' Voluntary Liquidation (MVL) Explained

Route-guide / explainer page for the solvent-company liquidation route, at
/liquidation/members-voluntary-liquidation/. Page-class override
("members-voluntary-liquidation" -> "entity_owner") sits in
scripts/page_runtime_metadata.py SLUG_PAGE_CLASS_OVERRIDES.

This is a slim insolvency-page config — only the fields the Bernstein pipeline
and runtime-pack router actually read. Insolvency pages do not carry the hero
zone, info_gain map, or section configs that credit-card pages need. Content is
read directly from drafts/7676_members-voluntary-liquidation.html.

The registered H-tag structure for this page lives in
editorial-os/28-htag-semantic-framework.md under "Registered page templates"
(added 2026-07-15, implementing the Google/AI-retrieval brief). That
registration is the binding spec, per that file's own rule that named-slug
registrations take precedence over the general family templates. It
supersedes the 2026-06-11 adopted outline ("What Is... / Two Legal Tests /
MVL Liquidation Timeline / Director Duties / MVL Liquidation Costs / Risks
and Disadvantages / Next Steps / FAQs"), which the Bernstein state.json
review_notes_complete checkpoint still describes as "6/8 H2 info-gain
filled" against that old outline. Bernstein revise/gate runs on this page
should check the draft's headings against the framework registration, not
that stale note.
"""

PAGE_CONFIG = {
    'slug': 'members-voluntary-liquidation',
    'page_type': 'definition',
    'wp_page_id': 7676,
    'title': "Members' Voluntary Liquidation: Process, Costs and Tax",
    'verification_date': '15 July 2026',
}
