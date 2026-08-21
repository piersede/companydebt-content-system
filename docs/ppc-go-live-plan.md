# PPC landing pages: plan to go live

Written 2026-08-21. Everything here is already built and verified on staging.
This is only about getting it onto production, by the normal route: build on
staging, push staging to live.

Companion docs: `docs/ppc-landing-deployment.md` (the staging build),
`docs/ppc-form-registration.md` (form and GTM detail).

---

## What is already done

| Piece | State |
| --- | --- |
| Four pages on staging, noindex, render-verified | done |
| Page template + 5 assets on staging | done |
| Gravity Form 47, tested end to end | done |
| Lead email, all merge tags populated | done |
| Zoho tagging leads `PPC - CD` with intent and situation | done |
| GTM trigger, live in container version 88 | done |

- https://comdebstage.wpengine.com/ppc-liquidate-company/
- https://comdebstage.wpengine.com/ppc-company-debt/
- https://comdebstage.wpengine.com/ppc-hmrc-debt/
- https://comdebstage.wpengine.com/ppc-winding-up-petition/

---

## THE ONE THING THAT MATTERS: "don't overwrite Gravity Forms" splits in two

The standing rule in CLAUDE.md is to deselect **every** `*_gf_*` table. That
protects the leads, and it is the right instinct. But it is too broad for this
push, because the Gravity Forms tables do two completely different jobs, and
this release needs one group to travel while the other must not.

Measured on staging, 2026-08-21:

### EXCLUDE — the leads. Irreplaceable. Never push these.

| Table | Rows | Why |
| --- | --- | --- |
| `wp_gf_entry` | 7,654 | the enquiries themselves |
| `wp_gf_entry_meta` | 37,260 | their field values |
| `wp_gf_entry_notes` | 7,343 | notes on them |
| `wp_gf_draft_submissions` | 0 | part-completed forms |
| `wp_gf_rest_api_keys` | 2 | **excluding this protects the LIVE API key.** A previous full push invalidated it and everything reading live forms broke until it was regenerated. |

### INCLUDE — the form definitions. Without these, form 47 does not exist on live.

| Table | Rows | Why |
| --- | --- | --- |
| `wp_gf_form` | 46 | the form records |
| `wp_gf_form_meta` | 46 | fields, notifications, confirmations. **This is where form 47 actually lives.** |

If both of these are deselected along with the entry tables, the four pages go
live with no enquiry form on them. That is the single worst outcome available
here: paying for clicks that cannot convert.

### Either way, does not matter

| Table | Rows | Note |
| --- | --- | --- |
| `wp_gf_form_view` | 20,398 | view counters, cosmetic |
| `wp_gf_addon_feed` | 2 | check what these feed before deciding |

**No ID collision.** Live's highest form id is 46. Staging's form 47 lands in
free space and keeps its number.

---

## What else needs to travel

- `wp_posts`, `wp_postmeta` — the four pages, their template assignment, and the
  noindex flag. Because the meta travels, **noindex does not need setting on live
  separately.** It comes with the push. Verify it landed rather than assume it.
- `wp_yoast_indexable` — push this **with** `wp_posts`. If it is left behind,
  Yoast serves titles, descriptions and robots from a stale cache and the pages
  drift out of step with their own content.
- `wp_options` — carries `cd_ppc_form_id`. Optional now: the template was given
  a hard-coded fallback of 47 on 2026-08-21 precisely so this push does not
  depend on wp_options travelling. If wp_options does travel, the option wins.
- **Files**: the page template, the five images in `assets/ppc/`, and three
  mu-plugins (`cd-livechat-zoho.php`, `cd-gform-notification-fix.php`,
  `cd-gform-hardening.php`). These ride the file-system half of the copy.

---

## Pre-flight

**1. Direction check. Non-negotiable.**

    python scripts/push_site_content_live.py --changed-only

Read-only. If it reports pages held back because "live is newer", run
`python scripts/sync_staging_from_live.py --confirm` first. A `wp_posts` push
REPLACES the table: anything edited on live since the last clone is destroyed.
On 2026-08-07 that would have been 232 pages.

**2. Stray script audit. Immediately before, not hours before.**

    python scripts/audit_mu_plugins.py

Everything in `wp-content/mu-plugins` runs on every request on live. Clean at
the time of writing: 0 throwaway scripts, 27 kept.

**3. Production media.** The file half of the copy has no exclusions. Anything
uploaded to production since the last clone is lost. Worth a look if images have
been added on live recently.

---

## The push

WP Engine: Staging > Actions > Copy to > Production > **Custom**.

- Database tables: select all, then **deselect** the five EXCLUDE tables above.
  Leave `wp_gf_form` and `wp_gf_form_meta` SELECTED.
- File system: include.

Note the file copy also carries four other workstreams currently sitting on
staging (Insolvency Test redesign 17 Aug, header and data-hub changes 14 Aug,
CTA block work 6-7 Aug, the forms fix 20 Aug) plus roughly forty `.bak-*` files.
Per Piers, this is the normal working pattern and those changes are intended for
live. Recorded here only so nobody is surprised by what appears.

---

## After the push, verify. A 200 is not proof.

For each of the four live URLs:

- returns 200
- `<meta name='robots'` contains `noindex` — **single quotes on this install**
- the template marker `id="cd-ppc-styles"` is present
- `gform_wrapper_47` is present, and `class="cd-ppc-form-missing"` is not
- body over 20,000 bytes

`scripts/deploy_ppc_pages.py --verify-only` already does exactly these five
checks; point it at live or copy its logic.

Then:

1. Purge **Cloudflare** as well as WP Rocket and WP Engine. Stale Cloudflare 301s
   after a push have redirected live to the staging domain before.
2. `python scripts/check_live_form_entries.py` — confirms entries are still
   arriving and nothing was wiped.
3. Confirm the live Gravity Forms REST key still works. If it 401s, it was
   invalidated by the push and needs regenerating in Forms > Settings > REST API,
   then updating in `.env`.
4. One end-to-end test submission on live. It emails info@, tony@ and
   piers@companydebt.com, so repoint the notification to one mailbox first and
   restore it after, as was done on staging. Confirm the Zoho lead arrives with
   Lead_Source `PPC - CD`.

---

## Then, and only then, point the ads

Each ad group to its own URL. Two things that mislead when reading the results:
Google Ads credits a conversion to the **landing page of the ad click**, not the
page of the submission; and Gravity Forms timestamps are UTC while Ads reports in
London time.

---

## Separate, worth doing before this

Website form leads stopped reaching Zoho between **4 and 19 August**, resuming on
the 20th when the `gform_entry_post_save` filter fix landed. The fix is confirmed
working: `Website Form - CD` leads run 2-3 Aug, then nothing, then resume 20-21
Aug.

The fix stops future losses. It does not recover the window. Measured on live:
**35 lead-form entries were taken between 4 and 19 August** — 14 Contact-Advisors,
18 Insolvency Test, 2 Guide, 1 Home Page — and no `Website Form - CD` lead exists
in Zoho for any of those dates.

They are not lost, they are sitting in Gravity Forms. Nobody worked them as CRM
leads. `scripts/reconcile_forms_to_zoho.py` exists for exactly this comparison.
