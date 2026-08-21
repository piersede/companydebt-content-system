# PPC landing pages: deployment runbook

Four paid-search landing pages, all on one shared template, all noindexed.

| Slug | Title |
| --- | --- |
| `ppc-liquidate-company` | Need to Liquidate Your Company? \| Company Debt |
| `ppc-company-debt` | Need to Close a Company That Can't Pay Its Debts? \| Company Debt |
| `ppc-hmrc-debt` | Can't Pay HMRC? \| Company Debt |
| `ppc-winding-up-petition` | Facing a Winding-Up Petition? \| Company Debt |

Template for all four: `theme/templates/ppc-landing.php`
Deploy script: `scripts/deploy_ppc_pages.py` (staging only, refuses any other host)

These pages exist to receive Google Ads traffic. They must never be indexed.
Every step below is on **staging**. Nothing here touches live.

---

## Order of work

Steps 1 and 2 are preconditions, not preliminaries. The deploy script in step 3
verifies the rendered page, and it fails if either one was skipped.

### 1. Push the template and the assets to staging

The page template file and the image assets must be on the server **before** the
pages are created. If the template file is missing, WordPress silently falls
back to the default page template and renders an empty page wrapped in full
theme chrome.

Files involved:

- `theme/templates/ppc-landing.php`
- `theme/assets/ppc/` (chris-andersen.webp, nicki-meadows.jpg, icaew.png,
  ipa.png, reviewsio.png)
- any stylesheet or script the template enqueues

Push them with the normal staging theme workflow (`scripts/sftp_edit.py`).
Confirm the file is present on the server before moving on.

Note on how the missing-template case is caught. The page-template body class
is **not** evidence. WordPress derives that class from the page's stored
`_wp_page_template` value, which the deploy script writes itself, so the class
appears whether or not the template file was ever uploaded. Step 4 therefore
looks for markup only `ppc-landing.php` can produce: the `cd-ppc-styles` style
block and the `cd-ppc` wrapper element.

### 2. Create the enquiry form and register its id

The template does **not** take a hard-coded form id. It reads the WordPress
option `cd_ppc_form_id` (`theme/templates/ppc-landing.php` line 208). If the
option is unset, the template renders a "The enquiry form is not configured on
this environment yet" placeholder and the page captures no leads at all.

Create the form with the script, not by hand in the admin:

```
python scripts/gf_create_ppc_form.py
```

It creates "PPC - Request a Confidential Call", stores the new id in
`cd_ppc_form_id` and prints it. It is idempotent, so running it twice does not
create a duplicate.

**Then work through `docs/ppc-form-registration.md` before going any further.**
That checklist is not optional housekeeping. Its step 1 registers the id in
`cd_gfn_owned_form_ids()`, and without it **every notification email arrives
with EMPTY merge tags** - the admin gets the boilerplate with no name, no
number and no email address. The rest of the checklist covers spam hardening,
the phone-field format (new phone fields default to the US format) and the
Google Ads and GA4 conversion triggers.

### 3. Run the deploy script

Dry run first. This is the default, and it writes nothing:

```
python scripts/deploy_ppc_pages.py
```

Read the plan. Then apply:

```
python scripts/deploy_ppc_pages.py --confirm
```

`--dry-run` overrides `--confirm`. Passing both writes nothing and says so.

For each of the four pages the script:

1. Finds the page by slug and creates it only if it is absent. It never
   duplicates. The output says `CREATED` or `FOUND` for each one.
2. Sets `_wp_page_template` to `templates/ppc-landing.php`.
3. Sets `_yoast_wpseo_meta-robots-noindex` to `1`.
4. Sets the Yoast SEO title and a per-page meta description.
5. Deletes the page's `wp_yoast_indexable` row.
6. Purges WP Rocket for the page.

Step 5 is the one that is easy to leave out and expensive to leave out.
Yoast serves the robots tag, title and description from its own cache table
at render time, not live from the page's stored fields. Without the delete,
the write reports success and the rendered page is unchanged. The same guard
sits in `scripts/wp_set_meta.py` (lines 53-71).

### 4. Verify

The script verifies automatically after `--confirm`. To re-run the checks on
their own at any time:

```
python scripts/deploy_ppc_pages.py --verify-only
```

It re-fetches each public URL and reads the returned HTML for:

- HTTP 200
- a `<meta name="robots">` tag that contains `noindex`
- markup only the ppc-landing template emits, which proves the template file is
  on the server and actually rendered
- a rendered Gravity Forms wrapper, with an explicit failure if the template's
  "form is not configured" placeholder is on the page instead
- a response over 20,000 bytes

Then it prints a PASS/FAIL table.

A 200 on its own is not proof. A push in this repo has returned `200 / OK` and
landed a truncated fragment. The byte floor catches that. The template marker
and the form check catch the two ways a page can look complete and be useless:
the wrong template rendering, and a landing page with no lead capture on it.

Staging URLs:

- https://comdebstage.wpengine.com/ppc-liquidate-company/
- https://comdebstage.wpengine.com/ppc-company-debt/
- https://comdebstage.wpengine.com/ppc-winding-up-petition/
- https://comdebstage.wpengine.com/ppc-hmrc-debt/

### 5. What is still manual

The script does not do any of this. Do it by hand after step 4 passes.

- **Full mobile QA on all four pages.** Standing rule, every new page.
- **Submit the form once on each page** and confirm the entry arrives and the
  notification email carries real values, not empty merge tags. If the values
  are empty, step 1 of `docs/ppc-form-registration.md` was missed.
- **Google Ads final URLs.** Point each ad group at its page. Confirm the
  conversion action fires from the ad landing page, not from a later page.
- **Tracking parameters.** Confirm the lead-source fields capture the click
  ID and the campaign.
- **Sitemap.** Confirm the four pages are absent from the Yoast XML sitemap.
- **Internal links.** These pages should not be linked from site navigation.
- **Human sign-off** on the copy before any of it goes live.

---

## NOT YET POSSIBLE ON LIVE

**The noindex flag cannot be set on live from this repo today.** Do not treat
the live rollout as a repeat of the staging steps above.

`scripts/publish_to_live.py` is the only sanctioned per-page writer for live.
Its arguments are `--id`, `--file`, `--post-type`, `--status`, `--title`,
`--confirm` and `--force`. There is no `--meta` option, so it cannot write
`_yoast_wpseo_meta-robots-noindex`. The staging path used above cannot be
reused either: it works by uploading a one-shot plugin file over SFTP, and
that transport is staging-only.

The practical effect: if these four pages are pushed to live as they stand,
they go live **indexable**. For a paid-search page that is a real problem.
Duplicate thin pages compete with the organic guides they were cloned from.

Two candidate fixes. Pick one before any live push.

**Option A: add a `--meta` flag to `publish_to_live.py`.**
Post `meta: {"_yoast_wpseo_meta-robots-noindex": "1"}` to the live REST
endpoint alongside the content, then re-save the page so Yoast rebuilds its
indexable row. Verify by reading back `yoast_head_json.robots` from the REST
response and confirming it says `noindex`. This follows the same
meta-then-resave ordering already proven for the live Yoast title. The
meta key must be registered as REST-visible, or the write is accepted and
silently dropped, so the read-back is not optional.

**Option B: a `wpseo_robots` filter in the theme.**
Force `noindex, follow` for these page slugs in PHP, following the precedent
at `theme/functions.php` lines 1047-1056, where individual testimonial pages
are pushed back to noindex the same way. This needs no REST change and it
cannot be undone by an editor in the admin, which for PPC pages is an
advantage. It does mean the rule lives in code and travels with the theme
file push.

Option B is the smaller change and the harder one to break by accident.
Option A is the more general fix and unblocks every future page that needs a
meta value set on live.

Either way, verify on live by fetching the rendered page and reading the
robots tag out of the HTML. Do not trust the response code.
