# Live push plan - chart wording fix, 21 data pages

**Date drawn up:** 2026-08-07
**Status:** awaiting Piers's approval. Nothing has been pushed to live.

## What this is

All 21 `/data/` sector and trade pages are already live. Every one of them currently
shows a chart covering January 2016 to June 2026, under a heading, intro, caption and
screen-reader description that all claim the figures start in January 2023.

This is a **content update to 21 existing live pages**. It is not a launch, and it needs
no new pages, no redirects and no code changes.

## What is NOT involved

- **No WP Engine environment copy.** Not the full copy (which replaces the live database
  and destroyed ~160 enquiries in 2026), and not the files-only copy either.
- **No code push.** Nothing in `mu-plugins`, the theme, or any plugin changes. The chart
  and its wording are stored in the page content itself.
- **No database operation** beyond the 21 individual page records being updated.

Form entries, users, comments and every other page on the site are untouched and out of
scope. There is nothing to "preserve" because nothing else is being written.

## Pages and their live IDs

Live IDs are identical to the staging IDs.

| ID | Page |
|---|---|
| 79856 | construction |
| 80098 | furniture |
| 80134 | restaurant |
| 80136 | road-haulage |
| 80137 | recruitment-agency |
| 80138 | temporary-staffing-agency |
| 80139 | motor-vehicle-repair |
| 80140 | cleaning-company |
| 80141 | hotel |
| 80260 | estate-agency |
| 80578 | it-consultancy |
| 80581 | management-consultancy |
| 80584 | architectural-engineering |
| 80587 | personal-care-services |
| 80590 | sports-facility |
| 80593 | medical-dental-practice |
| 80596 | creative-arts-entertainment |
| 80597 | amusement-recreation |
| 80601 | real-estate-letting-investment |
| 80604 | freight-forwarding-logistics |
| 80679 | retail |

All slugs take the form `<name>-insolvency-statistics` under `/data/`.

## Sequence

**Step 0 - preconditions (already met)**

- All 21 rebuilt drafts verified on staging: 126-point chart, axis 2016-2026, wording
  matching, no mangled markup. 21/21 clean.
- `sector_data_audit.py` passes 18/18 on every trade page.
- `audit_mu_plugins.py` reports zero throwaway scripts (checked, though not strictly
  required here since no code is being copied).
- Dry run against live page 79856: 97% similar, 107% of current size. Safe shape.

**Step 1 - one page, then stop**

```bash
python scripts/publish_to_live.py --id 79856 --file drafts/79856_construction-insolvency-statistics.html --confirm
```

Then re-fetch `https://www.companydebt.com/data/construction-insolvency-statistics/` and
confirm: page is a plausible size, the "since 2023" wording is gone, the chart still has
126 points, and there is no escaped or broken markup. **Stop and report before going on.**

**Step 2 - the remaining 20**

Same command per page, one at a time, with a short pause between each to avoid tripping
the rate limiter. The tool refuses any page whose new content is suspiciously shorter
than what is live, so a truncation cannot land silently.

**Step 3 - clear the caches**

Live pages are served from cache, so the fix is invisible until this is done:

- Cloudflare purge
- WP Rocket / WP Engine purge

Skipping this makes it look like the push failed.

**Step 4 - verify all 21 on the real URLs**

Re-fetch each live URL and check the same four things as Step 1. Report the byte count
and result per page. A success message from the push tool is not evidence.

**Step 5 - confirm nothing else broke**

```bash
python scripts/check_live_form_entries.py
```

Standing rule after any live push, even a content-only one.

## Known open item

The stored search-result snippet for the furniture page still reads "the monthly trend
since 2023". That text lives in WordPress separately from the page body, so this push
will not change it. On staging it was corrected with `wp_set_meta.py`, but that tool
works over SFTP and there is no live SFTP by design, so live needs a different route
(likely the `cd-seo-meta-rest.php` helper already present on live).

This affects one page's search snippet only - no visible page content - so it does not
need to block the push. Worth closing separately.

## Rollback

Each page's previous content stays in its WordPress revision history, so any page can be
reverted individually from the admin screen, or via `restore_from_revisions.py`. There is
no all-or-nothing step in this plan: every page is independent.
