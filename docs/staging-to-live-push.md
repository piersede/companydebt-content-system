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

In the WP Engine portal, choose **"file system only"**. No database, no risk. Note that
mu-plugin and theme edits are made on *staging* via `scripts/sftp_edit.py`, so a
file-system copy is how they reach live.

### If a database push is genuinely unavoidable

Use **"select specific database tables"** and pick an **allowlist** of content tables, so
a table you forget defaults to safe rather than destroyed:

```
wp_posts  wp_postmeta  wp_terms  wp_termmeta
wp_term_taxonomy  wp_term_relationships  wp_options  wp_yoast_indexable
```

Never "select all". WP Engine does not save table selections between copies, and its API
cannot copy environments at all, so this is manual every time.

## After ANY push to live

1. **Purge caches**: WP Rocket, WP Engine, and **Cloudflare**. Cloudflare is a separate
   layer and will otherwise keep serving the old page and old 301s for up to a year.
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
