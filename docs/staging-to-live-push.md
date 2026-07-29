# Pushing staging to live

**Read this before putting anything on companydebt.com.**

## The rule

Piers's standing instruction: **"always wait for my explicit instructions before pushing live."**

Live WordPress credentials are in `.env` (`CD_LIVE_URL`, `WP_LIVE_USERNAME`,
`WP_LIVE_APP_PASSWORD`). Their existence is **not** permission. Reads against live are
fine. Every write waits for Piers to ask for that specific push. Do not infer approval
from a finished page, a passing gate, or approval given for a previous push.

## The hazard this replaced

The old route was WP Engine's staging to live **"copy environment"**, which replaces the
LIVE database **wholesale**. Staging never receives real form submissions, so every
full-database push restored staging's stale snapshot over live and destroyed everything
real visitors had created since the previous push.

That ran undetected from **23 March to 28 July 2026**, destroying roughly **160 form
enquiries**, and was misread as a 45% drop in demand. The last surviving entry is dated
the day staging was last cloned from live. Nothing was ever broken; the push was doing
exactly what it is designed to do.

A full database push also destroys: user accounts, comments, the Stream activity log,
form view counts, and scheduled actions. It additionally **invalidates the Gravity Forms
API key** and leaves **stale Cloudflare 301s** pointing at the staging domain.

**So: do not push the database.** Use the routes below instead.

## Which route

| What changed | How it goes live |
|---|---|
| Page or post content, title, SEO fields | `scripts/publish_to_live.py` (REST API, one page at a time) |
| Theme files, mu-plugins, CSS, JS | WP Engine portal, **"file system only"** copy |
| Redirects, plugin settings, options | Manually in live `wp-admin`. These live in the database. |

`wp_push.py` **cannot** target live. It works over SFTP plus a one-shot mu-plugin, and
there is no live SFTP by design. It is a staging-only tool.

### Content to live

```bash
# 1. Dry run first. Reads only, writes nothing. ALWAYS do this.
python scripts/publish_to_live.py --id <LIVE_ID> --file preview/<page>.html

# 2. Only after Piers has explicitly asked for this push:
python scripts/publish_to_live.py --id <LIVE_ID> --file preview/<page>.html --confirm
```

Use `--post-type posts` for blog articles (a page ID and a post ID are different things).
The script refuses any push that shrinks a page below 50% of its current size, because a
truncated payload has silently wiped a live page before while returning `200 OK`. It
re-reads the page afterwards and warns if what landed is shorter than what was sent,
which is the signature of kses stripping inline SVG or scripts.

The live ID is usually **not** the staging ID. Find it:

```bash
python -c "import os,pathlib,requests;from dotenv import load_dotenv;load_dotenv(pathlib.Path('.env'));b=os.environ['CD_LIVE_URL'].rstrip('/');a=(os.environ['WP_LIVE_USERNAME'],os.environ['WP_LIVE_APP_PASSWORD']);print([(p['id'],p['link']) for p in requests.get(b+'/wp-json/wp/v2/pages',params={'search':'YOUR SLUG'},auth=a,headers={'User-Agent':'Mozilla/5.0'}).json()])"
```

### Code to live

Either route works. Both copy **every** file, not just the changed ones. Note that
mu-plugin and theme edits are made on *staging* via `scripts/sftp_edit.py`, so a
file-system copy is how they reach live.

#### MANDATORY pre-flight: clear throwaway scripts out of mu-plugins

**Because the copy takes every file, anything left in `wp-content/mu-plugins` goes live —
and everything in `mu-plugins` executes on every single request, with no way to disable
it from `wp-admin`.**

Sessions routinely leave one-shot helpers there: content pushers, batch fixers, dumpers,
inspectors. They are written to `@unlink(__FILE__)` after firing, but any that never fired
just sit there for ever. On 2026-07-29 a pre-flight check found **71** of them, some dating
to April, including four 50-60KB `codex-push-*.php` files holding base64-encoded article
bodies. Several were `wp_update_post()` endpoints reachable by anyone with the URL, guarded
only by a static query token — a few as weak as `?token=ch28apr`. There is no login check.

Run this before every code push and delete what it finds:

```bash
python scripts/audit_mu_plugins.py            # list one-shot / throwaway scripts
python scripts/audit_mu_plugins.py --delete   # back up to tmp/ then remove from staging
```

Rules:

- **Archive anything with a payload first.** The `codex-push-*` files carried real article
  content. Decoded copies live in `docs/archive/codex-push-payloads/`. Never delete a
  payload-bearing script without saving the payload.
- **Keep-list is authoritative.** Real functionality (`cd-insolvency-data-hub.php`,
  `cd-gform-hardening.php`, `cd-consent-mode-defaults.php`, `cd-livechat-zoho.php`,
  `cd-server-render.php`, WP Engine's own `wpe-*`/`slt-*`) is never touched. The script
  aborts if a keep-list name is ever classified for deletion.
- **A one-shot that already ran is still safe to delete.** Scripts like
  `cd-livechat-wpr-exclude.php` wrote their result into the database (WP Rocket settings,
  redirect rules); the settings persist without the file.
- **`.bak-*` files do not execute** (WordPress only loads `*.php` from the `mu-plugins`
  root), so they are clutter rather than risk. They are the rollback path — leave them.
- **Verify after deleting, before copying**: re-render the homepage, `/contact-us/` and
  `/uk-insolvency-statistics/` and check for `Fatal error` / `critical error`, then confirm
  the consent default still renders un-delayed and above the GTM snippet.

Do not skip this because the diff "is only one file". The diff is never only one file — the
copy is the whole file system.

**Scripted (preferred):**

```bash
python scripts/wpe_copy_files_to_live.py            # dry run
python scripts/wpe_copy_files_to_live.py --confirm  # only when Piers has asked
```

Needs `WPENGINE_API_USER` **and** `WPENGINE_API_PASSWORD` in `.env`, generated together
in the portal under Profile > API Access. The username alone returns `401 Bad Credentials`.

> The API's `POST /install_copy` **defaults `include_db` to true**. A request that
> omits `custom_options` copies the whole database and does exactly the damage described
> above. `wpe_copy_files_to_live.py` hard-codes `include_db: false`, never sends
> `db_tables`, and asserts both before the request leaves. Do not hand-roll this call.

**Portal:** Copy environment, Staging to Production, **"file system only"**.

### If a database push is genuinely unavoidable

Use **"select specific database tables"** and pick an **allowlist** of content tables, so
a table you forget defaults to safe rather than destroyed:

```
wp_posts  wp_postmeta  wp_terms  wp_termmeta
wp_term_taxonomy  wp_term_relationships  wp_options  wp_yoast_indexable
```

Never "select all". WP Engine does not save table selections between copies, so in the
portal this is manual every time. The API accepts a `db_tables` allowlist on
`/install_copy`, but `wpe_copy_files_to_live.py` deliberately refuses to send one: any
database copy should be a slow, deliberate, human decision.

## After ANY push to live

1. **Purge caches**: WP Engine, **Cloudflare**, and **WP Rocket**. Cloudflare is a
   separate layer and will otherwise keep serving the old page and old 301s for up to a
   year. WP Engine's caches can be purged from here:

   ```bash
   python -c "import os,pathlib,requests;from dotenv import load_dotenv;load_dotenv(pathlib.Path('.env'));a=(os.environ['WPENGINE_API_USER'],os.environ['WPENGINE_API_PASSWORD']);[print(t,requests.post('https://api.wpengineapi.com/v1/installs/87153507-ffe2-4d06-ba32-32c96d2b2791/purge_cache',auth=a,json={'type':t}).status_code) for t in ('object','page','cdn')]"
   ```

   > **WP Rocket is a manual click and it matters.** Live pages load WP Rocket's minified
   > copy of the stylesheet (`wp-content/cache/min/1/.../style.css`), **not** the theme
   > file. Until that is rebuilt, `style.css` can match staging byte for byte and the
   > change still will not render. Nothing here can trigger it: `wpe_purge.py` is
   > staging-only, the WP Engine API's `purge_cache` does not touch it, `wp-rocket/v1`
   > has no purge route, and application passwords do not authenticate `wp-admin`.
   > Go to live `wp-admin` > WP Rocket > **Clear cache**.
2. **Re-render the page** in a browser and check length and structure. A `200 OK` is not
   proof the right content landed.
3. **Check form entries survived**:
   ```bash
   python scripts/check_live_form_entries.py
   ```
   Non-zero exit means entries have stopped arriving, which almost always means someone
   pushed the full database.
4. **If the database was pushed**: regenerate the Gravity Forms REST key
   (Forms > Settings > REST API) and update `CD_GF_CONSUMER_KEY` / `CD_GF_CONSUMER_SECRET`.
   The consumer key must be 43 characters starting with a **single** `ck_`; a pasted
   `ck_ck_` prefix gives a "Consumer key is invalid" error identical to an expired key.

## Recovering the lost entries

WP Engine's automatic backup points captured live *before* each push. June and July 2026
enquiries may still be retrievable via a WP Engine support ticket. April and May are
likely outside retention.
