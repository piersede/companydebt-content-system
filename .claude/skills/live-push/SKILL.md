---
name: live-push
description: Put Company Debt content live safely - the correct alternative to a staging-to-live environment copy, which destroys form entries. Covers direction checking, staging URL rewriting, per-page pushing, cache purging and verification. Use whenever anything needs to go live on companydebt.com.
---

# Live push

Getting content onto `www.companydebt.com` without losing data or silently
undoing work.

**Every live push needs Piers's explicit say-so for that specific push.**
Credentials existing is not permission. Staging pushes are the opposite -
those are pre-approved and need no asking.

## The thing everyone asks for, and why it does not exist

"Just push the whole staging site live, but keep the Gravity Forms entries."

That is not an available operation. Page content and form entries live in the
**same database**. WP Engine's environment copy gives two choices:

| Copy option | Page content | Form entries, users, comments |
|---|---|---|
| Include database | moves | **destroyed** |
| Files only | does not move at all | safe |

There is no setting that does both. The full copy is what silently destroyed
~160 enquiries between 23 Mar and 28 Jul 2026, and the loss was misread as a
45% drop in demand for months. The files-only copy is safe but moves no page
content, and it deactivates Gravity Forms (versioned plugin folder) - reactivate
via the plugins endpoint afterwards.

**Never run a database copy from staging to live.** Not "carefully", not "just
this once". If asked, explain the table above and offer the per-page route.

## The route that works

`python scripts/push_site_content_live.py` writes each page's content over the
REST API. Only page records change; entries, users, comments and options are
untouched. Same end state for content, no data loss. Every page keeps its
WordPress revision history, so any page can be rolled back on its own.

```bash
python scripts/push_site_content_live.py --changed-only            # dry run
python scripts/push_site_content_live.py --changed-only --confirm  # write
python scripts/push_site_content_live.py --path /liquidation/ --confirm
```

For the registered `/data/` pages specifically, `push_data_pages_live.py` pushes
from the built drafts instead, and `publish_to_live.py --id --file` does one page.

## Four traps this has already hit

**1. Staging content carries staging URLs.** 90 of 320 pages had
`comdebstage.wpengine.com` image sources. The environment copy rewrites the
domain; a page-by-page push does not. Push raw and live points at a
password-protected site. The script rewrites these by default - do not pass
`--keep-staging-urls`.

**2. Live is often NEWER than staging.** Around 200 pages differed only because
live had the CTA button arrow ("Check My Company &rarr;") and staging did not -
a live-only roll-out that never went back. Pushing staging would have stripped
it from 200 live pages, reporting success on every one. The script now detects
this and skips those pages; `--include-live-newer` overrides, and almost never
should. **Check which side is newer before any bulk push.**

**3. The same page id can be different pages on the two sites.** `/business-debt-advice/`
is id 26218 on staging but `business-debt-advice-archived-26218` on live. The
script compares slugs and skips mismatches.

**4. A much smaller staging page is a warning, not an update.** `/hmrc/cant-pay-vat/`
is 16KB on staging against 30KB live. The script refuses anything under 60% of
the live size. Investigate before overriding - this is the truncation signature.

## Cache purging - automatable, no dashboard needed

The live `cf-cache` header is WP Engine's own CDN (Cloudflare underneath), not a
separate Cloudflare account. All three layers purge via the WP Engine API:

```python
iid = "87153507-ffe2-4d06-ba32-32c96d2b2791"   # companydebtltd, live
for t in ("page", "object", "cdn"):
    requests.post(f"https://api.wpengineapi.com/v1/installs/{iid}/purge_cache",
                  auth=(WPENGINE_API_USER, WPENGINE_API_PASSWORD), json={"type": t})
```

All three return 202. Until this runs, visitors keep seeing the old page and it
looks like the push failed. WP Rocket also holds a copy; if a change still will
not appear, clear WP Rocket from wp-admin.

## Verify, then check the forms

A 200 OK is not proof. Re-render each pushed URL and check byte count, the thing
you changed, the thing you replaced being gone, and no `&lt;!--` or `u003c`
escaped junk. Then, always:

```bash
python scripts/check_live_form_entries.py
```

## Before any CODE push to live

Different operation, different rules. A files-only copy takes **every** file, and
everything in `wp-content/mu-plugins` runs on every request. Run
`python scripts/audit_mu_plugins.py` and clear the throwaway one-shot scripts
first - 71 were found on one sweep, several of them unauthenticated endpoints.
Full procedure: `docs/staging-to-live-push.md`.

## Keep the two sites in step

Staging and live drift in both directions. After a live push, refresh staging
from live, or the next bulk comparison hits the same tangle again.
