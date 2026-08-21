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

**1. Direction check. FIRST RUN WAS INVALID. Rebuild the cache before trusting it.**

`push_site_content_live.py` does NOT read staging. It reads `content_cache.json`,
and that file only changes when `build_content_cache.py` is run. On 2026-08-21 it
was **twelve days stale** (last built 2026-08-09), so the first run's answer was
meaningless. This is the exact trap recorded in
`docs/wpe-custom-push-deployment.md`: on 2026-08-09 a stale cache reported all
319 pages identical while live was 202 pages behind.

    python scripts/build_content_cache.py                      # ALWAYS first
    python scripts/push_site_content_live.py --changed-only --pause 0.15

(The 1.5s default pause makes it time out over 319 pages.)

Second trap from the same doc: `skipped: 0` does NOT mean live is safe.
`classify()` only reports "live is newer" when the two sides match once the CTA
arrow is normalised away. Any page where live carries other work staging lacks is
classed "staging-differs" and queued for push. Read the byte counts: staging
thousands of bytes smaller than live, at 86-95% similarity, means live holds work
staging never received.

### Result, run properly 2026-08-21 after rebuilding the cache

**319 pages: 290 identical, 29 would push, skipped 0.**

`skipped: 0` is the false reassurance the deployment doc warns about. Reading the
byte counts instead, **live is meaningfully LARGER than staging on ten pages**,
which means live holds work staging never received:

| Page | live | staging | live ahead by |
| --- | --- | --- | --- |
| `/sector-specific-insolvency/` | 40,254 | 34,995 | 5,259 |
| `/director-protection-hub/` | 58,278 | 53,686 | 4,592 |
| `/liquidation/company-strike-off.../can-i-be-sued-after-my-company-is-dissolved/` | 27,942 | 23,949 | 3,993 |
| `/insolvency/how-to-reduce-insolvency-risk/` | 36,593 | 32,982 | 3,611 |
| `/liquidation/company-strike-off.../directors-responsibilities-after...struck-off/` | 28,013 | 24,578 | 3,435 |
| `/advice/what-is-limited-liability/` | 33,092 | 30,674 | 2,418 |
| `/debt-creditor-pressure-hub/` | 34,238 | 32,280 | 1,958 |
| `/insolvency/insolvent-company-owes-me-money/` | 25,491 | 23,536 | 1,955 |
| `/liquidation/can-a-director-be-sued-personally-by-creditors/` | 32,447 | 31,334 | 1,113 |
| `/insolvency/check-if-a-company-is-insolvent/` | 18,473 | 17,798 | 675 |

**Verified, not inferred.** Block-diffed `/sector-specific-insolvency/`: live has
68 content blocks, staging 66, and **22 blocks exist on live that staging does
not match**. Among them a whole "Sector-Specific Insolvency at a Glance" section
and a "Key Sector-Specific Insolvency Guides" section with substantive paragraphs
on care home insolvency (CQC and local authority placement teams) and energy
provider insolvency (Ofgem Supplier of Last Resort, the Energy Act 2011 Special
Administration Regime). That is real editorial work that exists only on live.

**A `wp_posts` push today deletes all of it, silently, across those ten pages.**

One page runs the other way and is expected: `/closing-a-limited-company/` is
64,107 live against 74,354 staging. That is page 65614, the full rewrite recorded
in `docs/open-items.md` as gating 34/34 and awaiting a live push.

### RESOLVED 2026-08-21. The sync was run.

    python scripts/sync_staging_from_live.py --confirm    # 186 synced, 1 held, 0 failed
    python scripts/build_content_cache.py
    python scripts/push_site_content_live.py --changed-only --pause 0.15

Held back, correctly: `/closing-a-limited-company/`, because staging has 1,417
more words there. That is the 65614 rewrite, and the guard protected it.

**Direction check after the sync: 319 pages, 316 identical, 3 differing, and
no page has live materially larger any more.**

| Page | live | staging | note |
| --- | --- | --- | --- |
| `/uk-insolvency-statistics/` | 537,951 | 537,945 | 6 bytes, a staging URL fix |
| `/liquidation/creditors-voluntary-liquidation/` | 51,577 | 51,572 | 5 bytes, a staging URL fix |
| `/closing-a-limited-company/` | 64,107 | 74,354 | staging AHEAD by 10,247, intended |

The ten pages where live held content staging lacked are resolved. From a
content-destruction standpoint the database push is now safe.

The four PPC pages were re-verified after the sync and still pass all five
checks.

### BUT: a blanket `wp_posts` push also puts page 65614 live

`/closing-a-limited-company/` is now the only page where staging is genuinely
ahead, so a `wp_posts` push publishes that rewrite too. `docs/open-items.md`
says it is not cleared to go:

- **item 1**, the referral-fee sentence in the commercial disclosure, is an
  unresolved compliance question
- **item 3**, named-IP sign-off from Chris Andersen, has not happened
- **item 4**, it "will not be pushed to live without an explicit instruction
  naming the page"

So either clear those first, or accept that this push publishes it. This is an
editorial and compliance gate, not a technical one, and nothing in the push
tooling will stop it.

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

## Separate finding: the August Zoho gap. DECIDED, no action.

Website form leads stopped reaching Zoho between **4 and 19 August**, resuming on
the 20th when the `gform_entry_post_save` filter fix landed. The fix is confirmed
working from the data: `Website Form - CD` leads run 2-3 Aug, then nothing, then
resume 20-21 Aug.

Reconciled the window on 2026-08-21 (`scripts/reconcile_forms_to_zoho.py`,
report-only, nothing written). 35 entries taken, 32 absent from Zoho, of which
roughly 17 were real enquiries and the rest were `@example.com` test submissions
from 5-6 Aug.

**Piers decided on 2026-08-21 not to load these into Zoho.** They received their
email notifications at the time. Do not re-raise this, and do not write the
recovered leads to the CRM.

The reconciliation CSV holds customer names and email addresses and was
deliberately kept out of this repo.
