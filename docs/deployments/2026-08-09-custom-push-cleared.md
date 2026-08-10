# Custom push staging → production, 2026-08-09: CLEARED

**Supersedes `2026-08-09-custom-push-blocked.md`, which was wrong.**

## The correction

The earlier document claimed ~183,000 characters of production-only content
would be destroyed. That figure was an artefact of two bugs in my own
measurement, not a property of the site:

1. **Non-greedy content match.** `<main[^>]*>(.*?)</main>` stopped at the first
   closing tag rather than the last, truncating pages and making staging look
   systematically shorter.
2. **Asymmetric normalisation.** Live text was compared against staging text
   using two different clean-up rules, so identical sentences failed to match.

Re-run with the same extraction on both sides and a real word-sequence diff.

## What the full scan actually found

All 331 live URLs, live vs staging, `<main>` region, word-level diff.

| Measure | Result |
|---|---|
| Pages scanned | 331 (0 errors) |
| **Median similarity** | **0.991** |
| Pages with no differing run of 12+ words | 177 |
| Pages with at least one differing run | 154 |
| Pages where **live is newer** than staging | **7** |
| Pages where staging is newer | 147 |

Direction was settled by `dateModified`, not word count, per the lesson in
commit 51b8c1a: trimming text makes staging smaller, which a size-based check
misreads as "live is newer".

On all 23 pages with 150+ differing words, staging is newer, typically
2026-07-15 on live against 2026-08-09 on staging. The differing text is the old
wording being correctly superseded, including the manufactured hooks the
redrafts removed and the referral wording this batch corrected.

## The seven live-newer pages are not a content risk

All seven are `/data/` statistics pages, all at 0.99 similarity, and all differ
by the same 58 words:

> Contact us / Get Called Back by an Expert / Let us explain your options /
> Practical solutions to your situation / We're licensed and regulated / Our
> advice is free and without obligation

That block renders inside `<div id="after-breadcrumbs-area">` as
`section-cd-gravity-form-widget`, embedding Gravity Form 41. It is a **widget in
a widget area, not page content**. WordPress stores widget assignment and
settings in `wp_options`.

**Excluding `wp_options` from the push preserves it.** It is not in `wp_posts`
and a `wp_posts` push cannot remove it.

## Verified clear

- `/insolvency-calculator/` — similarity **1.000**, zero differing words. The
  rebuilt conversion tool is identical on both sides and is unaffected.
- `cd-cta` blocks — parity on every sampled page. The CTA roll-out is safe.
- Heading anchors — parity on 64 of 70 in the earlier sample; the six
  exceptions were staging redrafts that renamed a section.
- `python scripts/audit_mu_plugins.py` — 0 throwaway scripts, 27 legitimate.
  The file-system half is safe to include.
- The 202-page live push logged in `site_push_report.json` was a **dry run**
  (`confirmed: false`). Nothing was written to live. The owner's account that
  production is never edited by hand is consistent with the evidence.

## Table selection

Select all, then deselect:

- every `*_gf_*` table — `gf_entry`, `gf_entry_meta`, `gf_entry_notes`,
  `gf_form`, `gf_form_meta`, `gf_addon_feed`. Leads live in the first three.
- `wp_options` — protects Gravity Forms global settings and licence key, and
  the widget config behind the `/data/` page CTA above.
- `wp_users`, `wp_comments` if they hold live activity.

Push `wp_posts` and the Yoast indexable table together or SEO titles drift.

## Files half

Include. Staging carries theme work not yet live. The only exposure is media
uploaded through the production admin since staging was last cloned, and
Gravity Forms file uploads, since a file copy has no exclusions.

## After the push

1. Purge live caches via the WP Engine API: install
   `87153507-ffe2-4d06-ba32-32c96d2b2791`, `POST /purge_cache`. Purge Cloudflare too.
2. Re-render a sample and confirm what landed. A 200 is not proof.
3. `python scripts/check_live_form_entries.py`
4. Confirm Gravity Forms is still active. A files-only copy has deactivated it
   before, because the plugin sits in a versioned folder.
