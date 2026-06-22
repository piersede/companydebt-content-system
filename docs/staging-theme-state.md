# Staging theme: source of truth & v2-flag retirement (2026-06-20)

## TL;DR
The **live theme on WP Engine staging is the source of truth**, not the repo.
The repo `theme/` folder is a stale, partial, heavily-divergent snapshot and
must NOT be treated as a mirror or wholesale-uploaded.

Active theme on staging: `wp-content/themes/company-debt-webpigment/`
(NOT the inactive `company-debt/` decoy theme.)

## Why the repo `theme/` is not the truth
Measured 2026-06-20 (repo vs canonical staging file):

| file          | repo size | staging size | changed lines |
|---------------|-----------|--------------|---------------|
| header.php    | 4,989     | 10,261       | 79            |
| functions.php | 32,776    | 39,602       | 189           |
| footer.php    | 4,741     | 57,417       | 934           |
| style.css     | 524,829   | 499,650      | 5,739         |

`footer.php` in the repo is ~1/12th the live size; `inc/` is absent entirely.
The repo theme is years behind. Reconciling it is a dedicated task (see
"Follow-up" below) and was deliberately NOT attempted as part of this change,
to avoid burying a small functional change under thousands of lines of
unrelated drift.

## Edit / verify / revert workflow
See memory `reference_staging_theme_edit_workflow`. In short, from PowerShell:
- pull:  `python scripts/sftp_edit.py get <remote-path>`
- push:  `python scripts/sftp_edit.py put <local> <remote> --tag <tag>`
  (auto server-side `.bak-a11y-<tag>` backup before first overwrite)
- purge: `python scripts/wpe_purge.py`  (then warm each page ~2x before re-auditing)
- Browser cache is sticky: hard-refresh (Ctrl+Shift+R). A stale browser CSS copy
  briefly showed the insolvency CTA as transparent during verification; a clean
  reload showed the correct orange.

---

## Change set: v2 feature-flag retirement
The "v2 redesign" was gated on `<html>` `data-*` flags set by delayed inline JS;
WP Rocket's Delay-JS + Remove-Unused-CSS held those until first interaction,
causing a base->v2 flicker. The header flag (`data-topnav-v2`) was de-flagged in
an earlier session. This change retires three more flags.

### Retired this session (2026-06-20)
- **`data-sticky-nav`** -> CSS de-flagged in `style.css` (rules made unconditional;
  `header.site-header{top:0!important}` + heading `scroll-margin-top:110px`).
- **`data-licensed-v2`** -> CSS de-flagged in `style.css` (the `#block-35`
  Licensed & Accredited widget rules; 3 logos on one line via `flex-wrap:nowrap`).
- **`data-insolvency-v2`** -> the Free Insolvency Test widget (`#block-20`) is now
  **server-rendered** as the `.cd-itest` layout (no JS rewrite, no visibility gate).

### Files changed on staging (each has a `.bak-a11y-retire-v2-flags` backup)
1. `wp-content/mu-plugins/cd-rocket-flicker-fix.php` — rewritten. Now:
   (a) server-renders `#block-20` via the `widget_block_content` filter, matching
       the unique `content-cd-list-with-button` class and outputting the
       `.cd-itest` markup (CTA href preserved, falls back to `/insolvency-calculator/`);
   (b) keeps the still-active early flag-setter + topnav logo/phone scripts
       un-delayed in WP Rocket;
   (c) keeps the header/nav CSS in the RUCSS safelist.
2. `theme/header.php` — early `cd-v2-flags-early` script: removed the now-dead
   `data-sticky-nav` / `data-licensed-v2` / `data-insolvency-v2` setAttribute lines.
   (Critical inline `<style id="cd-canonical-type-scale">` for header colours is unchanged.)
3. `theme/functions.php` — `language_attributes` filter: dropped `data-sticky-nav`
   and `data-licensed-v2` (kept `data-toc-sidebar`).
4. `theme/footer.php` — removed three dead script blocks: `cd-sticky-nav-flag`,
   `cd-licensed-v2-flag`, `cd-insolvency-widget-v2` (the JS rewrite).
5. `theme/style.css` — dropped the `html[data-...="on"]` prefixes on the sticky-nav
   (3), licensed-v2 (8) and insolvency-v2 (25) rule blocks; DELETED the
   `visibility:hidden` reveal-gate (it depended on a `cd-sidebar-ready` class that
   only the now-removed JS added — de-flagging it would have hidden the sidebar
   permanently). Comments updated.

### Still-active flags (intentionally NOT touched)
`data-topnav-v2` (logo/phone JS still uses it; header colours are unconditional
critical CSS), `data-toc-sidebar`, `data-reviewsio-hidden`, `data-narrow-sidebar`,
`data-footer-v2`. These remain set by the early head script + footer scripts, kept
un-delayed by the mu-plugin.

### Verification (live browser, CVA + /liquidation/)
- `<html>` now carries only the 5 still-active flags above — none of the 3 retired.
- Stripping ALL `data-*` flags off `<html>` leaves header (white/sticky/top:0),
  insolvency CTA (orange `#ff6600`), licensed logos (`nowrap`), and all 5 nav
  dropdowns (white bg, absolute) UNCHANGED -> truly unconditional.
- `#block-20` HTML contains `.cd-itest` server-side; the legacy
  `.content-cd-list-with-button` v1 markup is gone. No page-level console errors.

### Revert
Restore any file from its `.bak-a11y-retire-v2-flags` sibling on staging, or
delete `cd-rocket-flicker-fix.php` to drop both the server-render and the
WP Rocket exclusions. The original v1 widget content and the old footer JS path
are untouched in source history (footer backup).

## Follow-up (recommended, separate task)
Import the **real** active theme (`company-debt-webpigment`, including `inc/` and
all current files) into version control to replace the stale partial `theme/`
mirror, so future edits diff against truth. This is a large one-time reconciliation
and should be its own reviewed commit.
