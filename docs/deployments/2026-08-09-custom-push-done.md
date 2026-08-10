# Custom push staging → production, 2026-08-09: DONE

Executed via the WP Engine API, which exposes the same table selection as the
dashboard Custom push (`POST /install_copy`, `custom_options.db_tables` is an
**include** list).

- source: `comdebstage` `4d8ea02e-090f-482f-b982-2f701b0387a3`
- destination: `companydebtltd` `87153507-ffe2-4d06-ba32-32c96d2b2791` (production)
- files: included
- database: 127 of 142 tables

## Excluded (15)

All ten Gravity Forms tables: `wp_gf_entry`, `wp_gf_entry_meta`,
`wp_gf_entry_notes`, `wp_gf_form`, `wp_gf_form_meta`, `wp_gf_form_revisions`,
`wp_gf_form_view`, `wp_gf_addon_feed`, `wp_gf_draft_submissions`,
`wp_gf_rest_api_keys`.

Plus `wp_options`, `wp_users`, `wp_usermeta`, `wp_comments`, `wp_commentmeta`.

The build asserted no `gf` table could reach the include list before firing.
`wp_posts` and `wp_yoast_indexable` went together so SEO titles stayed in step.

## Before

- Fresh production restore point taken and confirmed `completed` before the
  copy: backup `9c4d90c2-29f4-47fe-a56e-cbe59906ed76`.
- Lead baseline recorded: 23 / 1612 / 678 / 6 / 164 / 58 / 1395 / 1580 / 89 / 18.
- `audit_mu_plugins.py` clean: 0 throwaway scripts, 27 legitimate.

## Note on the API call

The first `POST /install_copy` returned an empty body, so acceptance was
ambiguous. Re-sending returned `429 Install copies create operations are
rate-limited to one request every 60 seconds`, which confirmed the first call
had been accepted. No duplicate copy ran. **An empty body from this endpoint
means accepted; do not re-fire on it.**

## After

- Copy landed on live 4m30s after the request.
- Caches purged: WP Engine object, page and CDN, all HTTP 202.
- **Leads intact.** All ten forms identical to the pre-push baseline, and the
  Gravity Forms REST API answers, so the plugin is active.
- **Regulated-status wording: all 333 live URLs swept, zero hits** for any of
  refer/connect/introducer/advisory-firm/referral-network/referral-fee wording.
- `/insolvency-calculator/` intact and rendering its form.
- `/liquidation/` serving the corrected page: £352, £6,000, statement of truth,
  section 216 exceptions, the rewritten opening.

## The one thing that changed appearance, and why it is correct

The `/data/` statistics pages no longer show the "Get Called Back by an Expert"
form above the data. That is not a loss. The data-hub template deliberately
suppresses it:

> Hide the theme's auto-injected "Get Called Back" gravity-form widget that the
> after-breadcrumbs-area hook prepends to every page. The dashboard provides its
> own CTA at the bottom and the form above the data is noise.

Live had not yet received that template change; staging had. Each data page
still carries a Gravity Form, five `cd-cta` blocks and the phone number, so the
conversion path is intact and the form has simply moved below the data.

My earlier prediction that `wp_options` would protect this block was wrong in
its reasoning: the block is theme-CSS-suppressed, not widget-config driven.
Excluding `wp_options` was still correct, for the Gravity Forms licence and
settings.
