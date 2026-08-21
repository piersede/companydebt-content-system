# PPC landing pages: plan to go live

Written 2026-08-21. Everything described here is already built and verified on
staging. This document is only about getting it onto production.

Read `docs/ppc-landing-deployment.md` for the staging build itself and
`docs/ppc-form-registration.md` for the form and GTM detail.

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

Staging URLs:

- https://comdebstage.wpengine.com/ppc-liquidate-company/
- https://comdebstage.wpengine.com/ppc-company-debt/
- https://comdebstage.wpengine.com/ppc-hmrc-debt/
- https://comdebstage.wpengine.com/ppc-winding-up-petition/

---

## The shape of the problem

Going live splits into two halves that travel by completely different routes.

**Files** (the page template, the five images, three mu-plugins) can only reach
production through a WP Engine **file-system-only** copy. Live has no SFTP by
design.

**Database** (the four pages, form 47, the noindex and Yoast meta) cannot come
by the same route. The standard selective database push excludes the Gravity
Forms tables, so form 47 would not travel, and pushing `wp_posts` REPLACES the
table, destroying anything edited on live since the last clone. On 2026-08-07
that was 232 pages.

So: files by copy, database by individual API calls. Never a blanket push.

---

## THE BLOCKER: noindex cannot be set on live

These are PPC-only pages. If they are indexed, Google serves them organically
and the paid landing pages start competing with the real guides.

`scripts/wp_set_meta.py` does this correctly, but it is staging-only: it works
over SFTP, and live has none. `scripts/publish_to_live.py` sends only content,
status and title. **Nothing in this repo can set noindex on live.**

Two candidate fixes, cheapest first:

1. **Add `--meta` to `publish_to_live.py`.** POST
   `{"meta": {"_yoast_wpseo_meta-robots-noindex": "1"}}` to
   `wp-json/wp/v2/pages/<id>`, then re-save the post. Memory note
   `reference_yoast_live_title_ordering.md` confirms `_yoast_wpseo_title` and
   `_yoast_wpseo_metadesc` are writable over live REST.
   **`_yoast_wpseo_meta-robots-noindex` is UNVERIFIED on this install.** It must
   be proved by reading back `yoast_head_json.robots`, not by trusting the write.
2. **A `wpseo_robots` theme filter**, following the worked example at
   `theme/functions.php` lines 1047-1056 which does exactly this for single
   testimonials. Slower (it is a code change, so it rides the file copy) but it
   cannot silently fail the way a meta write can, and it survives a post re-save.

If option 1 does not verify, option 2 is the answer. **Do not put the pages live
until one of them is proven on a real live page.**

---

## THE OTHER BIG RISK: the file copy is all-or-nothing

A file-system-only copy takes **every file on staging**, not the ones we changed.
Staging currently carries at least four other workstreams' file changes from the
last three weeks:

| When | What |
| --- | --- |
| 21 Aug | **ours**: `templates/ppc-landing.php`, `assets/ppc/*`, 3 mu-plugins |
| 20 Aug | `cd-gform-hardening.php` entry-post-save filter fix |
| 17 Aug | Insolvency Test redesign: `templates/insolvency-test.php`, its CSS and JS |
| 14 Aug | `header.php` logo relative URL; `cd-insolvency-data-hub.php` SEO meta dashboard |
| 6-7 Aug | CTA blocks, `page-map.php`, `cd-cta-insolvency-test.php`, `style.css`, `cd-rocket-flicker-fix.php` |

Plus roughly forty `.bak-*` files that would land on production as clutter. They
are inert (they do not end in `.php`, so mu-plugins will not auto-load them) but
they do not belong there.

**Every one of those workstreams must be signed off, or reverted on staging
first.** The 17 Aug Insolvency Test redesign is the one to look at hardest: it is
a visible, user-facing change to a page that already converts.

Note the 20 Aug hardening fix appears to be on live already. Evidence: website
form leads reaching Zoho stop on 3 Aug and resume on 20 Aug (see the finding
below). So the copy should not regress it, but its exact live content cannot be
read from here to be certain.

**Also destructive:** the file half of the copy has no exclusions, so **any media
uploaded on production since the last clone is lost**. Check that before copying.

---

## Pre-flight, mandatory

    python scripts/audit_mu_plugins.py

Run immediately before the copy, not hours before. It was clean at the time of
writing (0 throwaway scripts, 27 kept). Everything in `wp-content/mu-plugins`
executes on every request on live, so a stray one-shot is a live security issue,
not untidiness. 71 were found on 2026-07-29.

---

## The plan

### Phase 0 — build the missing capability (no live changes)

1. Add `--meta` to `scripts/publish_to_live.py`, with read-back verification of
   `yoast_head_json.robots`.
2. Write a create-page-on-live script. `publish_to_live.py --id` can only UPDATE
   an existing page; nothing here creates one.
3. Write a create-form-on-live routine. `scripts/gf_create_ppc_form.py` is
   staging-only because it uses SFTP. Live has a working Gravity Forms REST API
   (it is already read from), so `POST /wp-json/gf/v2/forms` is the likely route.
   **Verify GF REST permits form creation on this install before relying on it.**
   Fallback: build the form by hand in the live admin from the field list in
   `docs/ppc-form-registration.md`.
4. Prove noindex on live against a single throwaway page before touching the
   real four.

### Phase 1 — decide what else travels

Go through the file table above. For each workstream: ship, or revert on staging
first. This is a human decision and it gates Phase 2.

### Phase 2 — files

Confirm no production media has been uploaded since the last clone. Run the
mu-plugin audit. Then WP Engine: Staging > Actions > Copy to > Production,
**file system only**.

### Phase 3 — database, in this order

1. Create form 47's live equivalent. Note the live form ID; it will very likely
   NOT be 47.
2. Set `cd_ppc_form_id` on live to that ID.
3. Register the live form ID in `cd_gfn_owned_form_ids()` and the
   `cd-gform-hardening.php` maps. **These are file changes, so they need a second
   file copy, or do Phase 2 after this step.** Without this the lead emails
   arrive with every field blank.
4. Create the four pages on live, assign `templates/ppc-landing.php`.
5. Set noindex and the Yoast title/description on each.

Sequencing note: steps 3 and 4-5 pull in opposite directions, because the form ID
is not known until the form exists, and the registration lives in a file. Cleanest
order is: create the live form first, then register the ID, then run the single
file copy, then create the pages.

### Phase 4 — verify, and do not trust a 200

For each of the four live URLs:

- returns 200
- `<meta name='robots'` contains `noindex` (single quotes on this install)
- the template marker `id="cd-ppc-styles"` is present
- `gform_wrapper_<live id>` is present and the "not configured" placeholder is not
- body over 20,000 bytes

Then purge **Cloudflare** as well as WP Rocket and WP Engine, and run:

    python scripts/check_live_form_entries.py

Then one end-to-end test submission on live. It emails info@, tony@ and
piers@companydebt.com, so repoint the notification to one mailbox first and
restore it after, as was done on staging. Confirm the Zoho lead arrives with
Lead_Source `PPC - CD`.

### Phase 5 — point the ads

Only once Phase 4 passes. Each ad group to its own URL. Remember Google Ads
credits a conversion to the **landing page of the ad click**, not the page of the
submission, and Gravity Forms timestamps are UTC while Ads reports London time.

---

## Separate finding, not part of this work

Website form leads stopped reaching Zoho between **4 and 19 August**. The most
recent `Website Form - CD` leads run 2 Aug, 3 Aug, then nothing until 20 Aug,
when they resume. That matches the `gform_entry_post_save` fault described in the
20 Aug fix comment exactly, and confirms the fix worked.

Roughly 17 days of website enquiries are therefore in Gravity Forms but never
reached the CRM. They are not lost, just not in Zoho.
`scripts/reconcile_forms_to_zoho.py` exists for precisely this comparison and
could recover them. Worth doing before the trail goes cold.
