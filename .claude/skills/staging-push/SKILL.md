---
name: staging-push
description: Push one or more Company Debt pages to staging safely - picks the correct push tool for the page type, then re-renders and verifies what actually landed. Use whenever pages need to go to comdebstage.wpengine.com. Never touches live.
---

# Staging push

Push pages to staging (`comdebstage.wpengine.com`) and prove the right content landed.

**Staging pushes never need permission.** Live pushes always do, and this skill never
does them. If the user says "live", stop and use `docs/staging-to-live-push.md` instead.

## Vocabulary trap - read this first

"Files only" is a **WP Engine environment copy** that moves *code*. It is not a page push.
People ask for "files only" meaning "don't wipe the form entries" - but a page push
cannot reach form entries, users or the database at large. It only touches the pages
named. If the user asks for a files-only copy when they actually want pages updated,
say so and do the page push instead.

(A real files-only copy has its own trap: it deactivates Gravity Forms, because the
plugin sits in a version-numbered folder. Reactivate via the plugins endpoint after one.)

## Step 1 - pick the tool by page type

Getting this wrong silently destroys the page while reporting success.

| Page type | Tool |
|---|---|
| Registered in `scripts/build_page.py` `PAGE_REGISTRY` (all `/data/` pages, dashboards, insolvency hub) | `python scripts/build_page.py --page <slug> --publish --id <wp_id>` |
| Ordinary article or guide wrapped in `<article>` | `python scripts/wp_push.py --id <id> --file <html>` |
| Page containing inline `<svg>` | `python scripts/wp_push_raw.py` (the normal path strips SVG) |

Check the registry before assuming:

```bash
python scripts/build_page.py --list
```

`wp_push.py` expects `<article>` markup. Point it at a passthrough or data page and it
truncates the content to a few hundred bytes of junk **and still returns 200 OK**. This
has wiped a staging page for real. Check the tool before running it, not after.

## Step 2 - push

Push one page first, verify it, then do the rest. Don't fire off twenty and check at the end.

Page IDs are usually the numeric prefix on the draft filename
(`drafts/79856_construction-insolvency-statistics.html` -> id `79856`).

## Step 3 - verify what landed (not optional)

A `200 OK` is not proof. Re-render each page and measure it. Staging sits behind two
gates: `WP_BASIC_AUTH_USER` / `WP_BASIC_AUTH_PASS` from `.env` gets you past the first.

```python
import os, re, requests
from dotenv import load_dotenv
load_dotenv()
a = (os.getenv('WP_BASIC_AUTH_USER'), os.getenv('WP_BASIC_AUTH_PASS'))
r = requests.get(url, auth=a, headers={'User-Agent': 'Mozilla/5.0'}, timeout=90)
```

Check every page for:

- **status 200** and a **plausible byte count** - a few hundred bytes means truncation
- **no `&lt;!--` or `u003c`** in the body - escaped markup means the content was mangled
- **the thing you actually changed** is present, and the thing you replaced is gone
- charts: the expected number of plotted points, and axis labels matching the caption

Report the byte count and the specific check per page. "Pushed successfully" on its own
is not a result.

## Step 4 - gates and clean-up

- Data pages: `python scripts/sector_data_audit.py` (not `article_audit.py`)
- Editorial pages: `python scripts/article_audit.py`
- If anything wrote via SFTP + a one-shot helper, run `python scripts/audit_mu_plugins.py`
  and confirm it reports zero throwaway scripts.

## Stored SEO snippets are separate

The search-result description lives in WordPress, not the page body, so a content push
never updates it. Editing the source that originally generated it changes nothing on the
already-created page. Use:

```bash
python scripts/wp_set_meta.py --id <id> --meta "_yoast_wpseo_metadesc=<text>"
```

That tool also drops the cached row the SEO plugin serves from - without that, the change
appears to save and nothing visible changes.

## Never

- Push staging to live via WP Engine's copy-environment. It replaces the whole live
  database. It destroyed roughly 160 real enquiries once already.
- Push to live from this skill at all.
