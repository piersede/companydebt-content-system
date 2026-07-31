# Inline CTA rollout — status & handoff (2026-07-31)

Snapshot of the article inline-CTA system on **staging** (`comdebstage.wpengine.com`).
Nothing has been pushed to live.

## Where CTAs come from — two mechanisms, identical look

Both render the site-wide `.cd-cta` component (eyebrow / title / intro / plain
button / tick trust-pills; variants `--test` blue, `--service` amber, `--phone`
green — styling lives in the theme `style.css`).

1. **Hand-placed (194 pages)** — an earlier rollout wrote 3 `cd-cta` blocks into
   each page's saved content, with **bespoke CTA2 copy** per page. To edit these,
   edit the page content.
2. **Injected (~50 pages)** — the theme filter in `functions.php` injects 3 CTAs
   at H2 boundaries at render time, with **generic per-cluster CTA2**. To edit
   these, edit `functions.php` (one place). See `cd_acta_map()`,
   `cd_acta_service()`, `cd_acta_block()`, and the `the_content` filter.
   - The injector **skips any page that already contains a `cd-cta` block**, so
     the 194 hand-placed pages are never touched or duplicated.
   - Gate: page id must be in `cd_acta_map()` **and** have ≥4 H2s.

## Reconciled counts (307 published pages)

- **244 pages have 3 CTAs**: 194 hand-placed + 49 gap pages injected this session
  + 1 earlier pilot injection (`75111`).
- **63 pages have 0 CTAs**: 58 excluded by design (30 `/data/` stats, 21
  utility/legal, 6 landing, 1 homepage) + **5 hub/index nav pages** intentionally
  left out (too little body for 3 inline CTAs):
  `guides-resources-hub` (77339), `sector-insolvency-hub` (77248),
  `sample-letters` index (53253), `bounce-back-loan-support-hub` index (43758),
  `liquidation/liquidation-hub` (22075). These need hand-placement if wanted.

## Done this session

- Rebuilt the injector to match the site `cd-cta` component (was an off-brand
  `cd-acta` card); removed em dashes and arrow glyphs from injected copy.
- Rolled injection out from the 10-page pilot to the 49 gap article pages.
- **Removed the trailing arrow (`→`) from the button of all 194 hand-placed
  pages** — surgical arrow-only content edits via REST, each backed up, verified
  0 arrows remain site-wide and all 194 kept their 3-block structure.

## Open / next

- **5 hub pages** still have no CTAs (see list above) — decide per-page.
- **Generic vs bespoke CTA2** on the injected ~50: currently generic per-cluster.
  Could be upgraded to bespoke copy later (needs a writing pass, Opus only).
- **Live push** not done. Follow `docs/staging-to-live-push.md`; run
  `python scripts/audit_mu_plugins.py` first; content goes one page at a time via
  `publish_to_live.py`; never DB-push staging→live.

## Local-only artifacts (NOT in git — on Théo's machine)

- `scratch_arrow_backup.json` — original raw content of all 194 pages before the
  arrow edit (rollback safety).
- `scratch_cta_audit.json` — per-page CTA count audit.
- `scratch_54_clusters.json` — the 54 gap pages → cluster mapping.
