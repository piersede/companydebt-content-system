# Runbook: the Custom push that launches the PPC pages

Written 2026-08-21. Follow top to bottom. Do not skip the checkpoint at step 4.

**Who runs this.** The table-by-table selection exists only in the WP Engine
dashboard. The API has one database switch, on or off, and its `db_tables`
option has never been used on this account. Nobody should experiment with it
against 7,654 live leads. So this is a browser job.

If Claude is to drive it, WP Engine must already be signed in on that Chrome
profile. Claude cannot sign in, and will not enter credentials.

**Provenance.** The environment IDs, table names and row counts below were
measured today. The dashboard click path comes from
`docs/wpe-custom-push-deployment.md`, not from a live inspection, because the
browser session was not authenticated when this was written. Read the labels on
screen rather than trusting the wording here exactly.

---

## What this push delivers

The four PPC landing pages, the enquiry form behind them, and the page template
and images they need. Nothing else in the release is outstanding.

| Already done, needs nothing from this push | |
| --- | --- |
| GTM conversion trigger | live in container version 88 |
| Referral-fee claim removed | 0 of 350 live records, verified |
| Zoho tagging PPC leads `PPC - CD` | on staging, travels with the plugin files |
| Staging in step with live | 186 pages pulled 2026-08-21, nothing lost |

---

## Environments

| | |
| --- | --- |
| Source | `comdebstage` / staging / `4d8ea02e-090f-482f-b982-2f701b0387a3` |
| Destination | `companydebtltd` / production / `87153507-ffe2-4d06-ba32-32c96d2b2791` |
| Destination serves | www.companydebt.com |

---

## 1. Pre-flight

**Stray script audit. Run it immediately before, not an hour before.**

    python scripts/audit_mu_plugins.py

Everything in `wp-content/mu-plugins` executes on every request on production.
71 leftovers were found in one sweep, several of them unauthenticated endpoints.
Last run 2026-08-21: **0 throwaway scripts, 27 kept. Clean.**

**Direction check.** Already run today, after rebuilding the cache and syncing
live into staging. 319 pages, 316 identical, and no page has live materially
larger than staging. Safe.

**Production media.** The file half of the copy has no exclusions. Anything
uploaded to production since the last clone is lost. Worth thirty seconds in the
media library if images have been added on live recently.

---

## 2. Start the push

WP Engine → **comdebstage** → **Actions** → **Copy environment** (labelled
"Push to" in some views) → destination **companydebtltd / production** →
choose **Custom**.

---

## 3. Set the options

**File system: INCLUDE.** This carries `templates/ppc-landing.php`, the five
images in `assets/ppc/`, and the three mu-plugins.

**Database: select all tables, then deselect exactly five.**

### DESELECT these five. Nothing else.

| Table | Rows | Why |
| --- | --- | --- |
| `wp_gf_entry` | 7,654 | the enquiries |
| `wp_gf_entry_meta` | 37,260 | their field values |
| `wp_gf_entry_notes` | 7,343 | notes on them |
| `wp_gf_draft_submissions` | 0 | part-completed forms |
| `wp_gf_rest_api_keys` | 2 | protects the PRODUCTION Gravity Forms API key |

That last one matters more than its row count suggests. A previous full push
invalidated the live key and everything reading live forms broke until it was
regenerated.

### LEAVE SELECTED. Getting this wrong is the worst outcome available.

| Table | Rows | Why |
| --- | --- | --- |
| `wp_gf_form` | 46 | the form records |
| `wp_gf_form_meta` | 46 | **form 47 lives here** — fields, notifications, confirmation |
| `wp_posts` | | the four PPC pages |
| `wp_postmeta` | | their template assignment AND the noindex flag |
| `wp_yoast_indexable` | | or Yoast serves stale robots and titles from its cache |

Deselect `wp_gf_form_meta` and the four pages go live with **no enquiry form on
them**. Paying for clicks that cannot convert is worse than not launching.

`wp_gf_form_view` and `wp_gf_addon_feed` are cosmetic either way.

**`wp_options`:** optional. It carries `cd_ppc_form_id`. The template was given
a hard-coded fallback of 47 on 2026-08-21 so this push does not depend on it.
Include it or not, the form still renders.

**No ID collision.** Production's highest form id is 46. Form 47 lands in free
space and keeps its number.

---

## 4. CHECKPOINT. Stop here.

Before pressing the button that starts the copy, read the selection back off the
screen and confirm, out loud or in writing:

- [ ] exactly five tables are deselected, and they are the five above
- [ ] `wp_gf_form` and `wp_gf_form_meta` are still ticked
- [ ] `wp_posts`, `wp_postmeta` and `wp_yoast_indexable` are still ticked
- [ ] file system is included
- [ ] the destination says **production**, not another staging environment

If Claude is driving, take a screenshot and read the checkbox states from it.
Do not infer them from the clicks that were sent. A click that did not register
looks identical to one that did, right up until the leads are gone.

This step is irreversible. There is no undo.

---

## 5. Immediately after: reactivate Gravity Forms

**A files copy deactivates Gravity Forms.** The plugin sits in a versioned
folder, so the copy renames it out from under WordPress. This has happened
before. Until it is reactivated, every form on the live site is down.

Check the plugins screen, or over the API:

    GET  /wp-json/wp/v2/plugins            # find gravityforms, read "status"
    POST /wp-json/wp/v2/plugins/<plugin>   # {"status": "active"}

Do this first, before the cache purge, before anything else.

---

## 6. Purge all three cache layers

Not the dashboard. The WP Engine API does all three:

```python
iid = "87153507-ffe2-4d06-ba32-32c96d2b2791"
for t in ("page", "object", "cdn"):
    requests.post(f"https://api.wpengineapi.com/v1/installs/{iid}/purge_cache",
                  auth=(WPENGINE_API_USER, WPENGINE_API_PASSWORD), json={"type": t})
```

All three return 202. Occasionally one returns 429 if purges were run recently;
re-run that one. Until this completes, visitors see the old site and it looks
like the push failed.

---

## 7. Verify. A 200 is not proof.

For each of the four live URLs:

- https://www.companydebt.com/ppc-liquidate-company/
- https://www.companydebt.com/ppc-company-debt/
- https://www.companydebt.com/ppc-hmrc-debt/
- https://www.companydebt.com/ppc-winding-up-petition/

check the rendered HTML for:

- HTTP 200
- `<meta name='robots'` containing `noindex` — **single quotes on this install**
- `id="cd-ppc-styles"` — proves the template rendered, not a fallback
- `gform_wrapper_47` present, and `class="cd-ppc-form-missing"` absent
- body over 20,000 bytes
- no `&lt;!--` or `u003c` escaped-markup junk

`scripts/deploy_ppc_pages.py --verify-only` already performs exactly these
checks against staging. Point it at production or copy its logic.

Then:

    python scripts/check_live_form_entries.py

Confirms entries are still arriving and nothing was wiped. If the live Gravity
Forms REST key now 401s, the push invalidated it: regenerate in
Forms → Settings → REST API and update `.env`.

Finally, one real submission on a live PPC page. It emails info@, tony@ and
piers@companydebt.com, so repoint the notification to a single mailbox first and
restore it afterwards, as was done on staging. Confirm the Zoho lead arrives
with Lead_Source `PPC - CD` and the ad intent in the description.

---

## 8. Only then, point the ads

Each ad group to its own URL. Two things that mislead when reading the numbers:
Google Ads credits a conversion to the **landing page of the ad click**, not the
page of the submission; and Gravity Forms timestamps are UTC while Ads reports in
London time.

---

## If it goes wrong

**Form entries missing.** Stop. Do not push again. WP Engine keeps automatic
restore points; a restore of the production database is the only recovery, and
it needs raising with them immediately.

**Pages render without a form.** `wp_gf_form_meta` was deselected. The pages are
fine; the form is simply absent on production. Recoverable: create the form on
live and set `cd_ppc_form_id`, or re-run the push with that table selected.

**Pages 404.** `wp_posts` was deselected, or the copy did not finish. WP Engine
emails on completion and exposes no job-status endpoint, so wait for the email
before concluding anything.

**Everything looks unchanged.** Almost always the cache. Do step 6 again.
