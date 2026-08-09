# Standard deployment: WP Engine Custom push, staging to production

**Status:** agreed approach, 2026-08-07. Supersedes per-page pushing as the
*normal* route for a batch of work. Per-page pushing remains correct for one or
two pages, and for anything urgent.

## The workflow

In WP Engine: **Staging → Actions → Push to → Production → Custom**

1. **Files** - include only if themes, plugins, mu-plugins, CSS or JS changed.
2. **Database** - choose *Select database tables*.
3. Select the tables you want pushed.
4. **Deselect every `*_gf_*` table.** Gravity Forms keeps forms, entries,
   notifications, confirmations and feeds in its own tables - `gf_entry`,
   `gf_entry_meta`, `gf_entry_notes`, `gf_form`, `gf_form_meta`, `gf_addon_feed`.
   The actual leads live in the first three.
5. Also protect `wp_options` unless a site or plugin setting was deliberately
   changed on staging. Some Gravity Forms global settings, including licence
   information, live there rather than in the `gf_` tables.
6. Consider protecting `wp_users` and `wp_comments` if they hold live activity.

This keeps every lead that arrived on production since staging was last cloned.

## The condition that makes it safe

**A selective push is not a merge.** Selecting `wp_posts` means staging's entire
`wp_posts` table *replaces* production's. Every page edited on production since
the last clone is destroyed, silently.

So the cycle only works in this order:

```
production  ->  clone/pull to staging  ->  Claude works  ->  test  ->  custom push back
```

and **nobody edits production in between**.

### This is not theoretical

On 2026-08-07 a full 320-page comparison found:

- **232 pages where production was AHEAD of staging** - production carried the
  CTA button arrows and heading anchor ids that staging never received
- only ~8 pages where staging genuinely held newer work

Pushing staging's `wp_posts` over production that day would have destroyed the
CTA roll-out and the heading anchors across 232 pages. Nothing would have
reported an error.

Before any custom push, confirm which side is newer:

```bash
python scripts/push_site_content_live.py --changed-only     # read-only
```

If that reports pages held back because "live is newer", production has work
staging lacks. **Pull production to staging first**, or the push destroys it:

```bash
python scripts/sync_staging_from_live.py --confirm
```

## Two traps in the direction check itself (found 2026-08-09)

The check below is the guard the whole procedure rests on. It has two blind
spots, both of which report "safe" when the push is not.

### 1. It compares a snapshot, not staging

`push_site_content_live.py` does not read staging. It reads `content_cache.json`,
which only changes when `build_content_cache.py` is run. On 2026-08-09 that file
was two days stale, and the check reported **all 319 pages identical, nothing to
push** while live was in fact 202 pages behind. Nothing errored.

**Always rebuild the cache first, or the answer is meaningless:**

```bash
python scripts/build_content_cache.py          # refresh staging snapshot
python scripts/push_site_content_live.py --changed-only   # then compare
```

### 2. "live is newer" only catches one narrow case

`classify()` reports `live-newer` only when the two sides are identical *once the
CTA arrow is normalised away*. Any page where live carries other work staging
lacks is classed `staging-differs` and queued for push. On 2026-08-09 the check
reported `skipped: 0` — no page held back — while a sample of 36 of the 202
queued pages showed **35 would have lost content**: 185 heading anchor ids and
198 `cd-cta` blocks, including the "30-Second Insolvency Check" call to action
pointing at `/insolvency-calculator/`.

So `skipped: 0` does **not** mean live is safe. Check the sizes: a page where
staging is thousands of bytes smaller than live, at 86-95% similarity, is a page
where live holds work staging never received. Diff one before trusting the run.

### The consequence for a content-only sweep

When the change is wording only, neither a table push nor a whole-page content
push is the right tool: both replace the page wholesale and take the live-only
work with it. Either pull production to staging first, re-apply the change, and
then push — or apply the wording change to live surgically, replacing only the
affected sentences and leaving the rest of each page alone.

## The file-system limitation

A file-system copy is destructive and WP Engine offers no per-file exclusions:
production's files are replaced with staging's wholesale.

- Any Gravity Forms **file uploads** on production that do not exist on staging
  are lost. Low risk if the forms only collect names, emails and phone numbers -
  that data is in the protected tables.
- **Any media uploaded on production since the clone is also lost** - including
  images added through the WordPress admin. This is the wider risk, and it
  applies to editorial work, not just forms.
- Before any files copy, run `python scripts/audit_mu_plugins.py` and clear the
  throwaway one-shot scripts. Everything in `mu-plugins` runs on every request;
  71 leftovers were found in one sweep, several of them unauthenticated
  endpoints.

## Yoast tables

If `wp_posts` is pushed without the Yoast indexable table, SEO titles and
descriptions can fall out of step with the content: Yoast serves them from its
own cache table, not from post meta. Either push both or re-save affected pages
afterwards. (Hit on 2026-08-07 with the furniture data page.)

## The rule that does not change

**Never perform a full database overwrite of production.** The all-tables copy
is what destroyed ~160 enquiries between 23 Mar and 28 Jul 2026. A *custom*
push with the `gf_` tables excluded is a different, supported operation - the
blanket copy is not.

## After every push

1. Purge the live caches (page, object, CDN) via the WP Engine API - no
   dashboard step needed:
   install `87153507-ffe2-4d06-ba32-32c96d2b2791`, `POST /purge_cache`.
2. Re-render a sample of pushed pages and check what actually landed. A 200 is
   not proof.
3. `python scripts/check_live_form_entries.py`
4. If the files were copied, confirm Gravity Forms is still active - a files-only
   copy has deactivated it before, because the plugin sits in a versioned folder.
