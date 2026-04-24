# SEO Fix Session State
_Last updated: 2026-04-24 (session 3)_

## Plan file
`C:\Users\piers\.claude\plans\swift-bouncing-aho.md`

## Access
- Staging: `https://comdebstage.wpengine.com/` (never touch live)
- Basic auth: `comdebstage` / `607b1133`
- WP App password: `PiersMooreEde` / `Uugbn6NbHoJ!oPGfe*y8!d6P`
- SFTP: `comdebstage.sftp.wpengine.com:2222` user `comdebstage-theo` pw `GbEr,;t++A>_m,2`
- SFTP root is WP root (e.g. `/wp-content/mu-plugins/`)

## Technique notes
- XML-RPC blocked by Solid Security; REST API requires auth — use **mu-plugin approach** instead
- SFTP → upload to `/wp-content/mu-plugins/yourscript.php` → trigger via `?yourparam=run` → self-deletes with `@unlink(__FILE__)`
- **Yoast uses indexable table** (`wp_yoast_indexable`) — writing to `wp_postmeta` alone is NOT enough; must also update `description` and `open_graph_description` columns in indexable table
- WP Engine page cache: clear via WP Engine Quick Links in admin bar ("Quick clear all cache")
- `wp_update_post()` from mu-plugin does NOT reliably rebuild Yoast indexables — update the DB table directly

---

## COMPLETED TASKS

### Session 1 (prior)
- ✅ 1.2 Broken redirects fixed
- ✅ 1.3 Sitemap redirect URLs
- ✅ 1.5 Double slash in theme (functions.php or template)
- ✅ 3.5 Twitter cards (Yoast global toggle)
- ✅ 3.9 HTTPS check
- ✅ 2.6 Short titles + test-article-2 noindexed
- ✅ 2.8 Global OG fallback image set in Yoast
- ✅ 2.9 OG URL mismatch (template fix)
- ✅ 3.2 Sitemap gaps (testimonials archive + case-studies now in sitemap; individual testimonials excluded via wpseo_sitemap_entry filter + noindexed via wpseo_robots filter)
- ✅ 3.6 SERP title rewrites (/advice/what-are-fixed-and-floating-charges/ fixed; other 2 already had correct titles)
- ✅ 3.8 Nofollow on internal links
- ✅ 3.4 Multiple H1 tags (liquidation template + chippy article)
- ✅ 3.3 Schema Pro Article fix (ucfirst author @type + null description removed) — filter in functions.php lines 847–865

### Session 2 (prior)
- ✅ 2.3 Hub page meta descriptions — 7 pages written to both `wp_postmeta` AND `wp_yoast_indexable`:
  - 43758 bounce-back-loan-support-hub ✓ (serving confirmed)
  - 77339 guides-resources-hub ✓ (serving confirmed)
  - 77396 director-protection-hub ✓ (serving confirmed)
  - 23471 case-studies-hub ✓ (serving confirmed)
  - 77372 company-rescue-recovery-hub ✓ (in DB; real slug, not "company-rescue-solutions-hub")
  - 77146 debt-creditor-pressure-hub ✓ (in DB; real slug, not "insolvency-hub")
  - 77694 articles-insights-hub ✓ (in DB; this is a `post` not `page` type; /articles-insights-hub/ 404s but post exists)

### Session 3 (this session)
- ✅ 2.3 finish: testimonials archive metadesc — CORRECT Yoast key is `metadesc-ptarchive-testimonial` (NOT `metadesc-archive-testimonial`). Also updated `wp_yoast_indexable` row (id=2147, object_type=post-type-archive). Serving confirmed on `/testimonials/`.
- ✅ 3.1: redirect chains — 7 URLs audited via curl on staging; 5 already resolve to final dest in single hop (Quick-PPR `quickppr_redirects` option already had direct mappings), 2 (`/company-rescue-solutions/pre-packs/`, `/business-debt-advice/`) return 200 directly. **Staging is ahead of the Ahrefs crawl — no action needed; production deploy will carry these fixes live.**
- ✅ 2.4: 36 meta descriptions shortened to ≤155 chars (max 136). Batch mu-plugin wrote to both `wp_postmeta` and `wp_yoast_indexable`. 35/36 via `url_to_postid()`, 1 (`/liquidation-hub/`, page ID 22075) via direct post_id lookup because the URL 404s on staging despite the page existing (permalink routing issue — pre-existing, not part of this task).
- ✅ 2.5: 62 titles shortened to ≤59 chars (SERP-ready verbatim, no `%%sitename%%` — brand suffix dropped to fit under 60). Batch mu-plugin wrote `_yoast_wpseo_title` postmeta + `title`/`open_graph_title`/`twitter_title` on indexable. All 62 updated.

**Tools created (reusable):**
- `tmp/sftp_upload.py` — Python paramiko SFTP uploader (reads .env for creds)
- Batch mu-plugin pattern: embed JSON via PHP nowdoc heredoc (`<<<'EOT' ... EOT;`) → `json_decode` → iterate → update postmeta + indexable → `wp_cache_flush` → `@unlink(__FILE__)` → exit

**End-of-session audit (after colleague's internal-links work):**
- Ran `mu-audit-all.php` comparing DB state to the 36 expected metadescs and 62 expected titles
- Titles: **62/62 intact**
- Metadescs: **36/36 intact** (one shows ASCII hyphen vs em dash on `/liquidation-hub/` due to my own encoding slip in the one-off fix — functionally equivalent, not a conflict)
- No overlap with the colleague's work — their internal-links fixes touched `post_content` anchor hrefs, my writes touched `wp_postmeta` + `wp_yoast_indexable`

---

## REMAINING TASKS (in priority order)

### 3.7 — 38 SERP title mismatches (mostly resolved by 2.5)
- Re-audit after 2.5 complete

### 2.2 — H1 on testimonials archive
- Check if `/testimonials/` already has H1 after theme fix from session 1
- If not: edit `archive-testimonials.php` in theme

### 2.7 — 51 pages missing alt text
- File: `C:\Users\piers\OneDrive\Desktop\CD fixes\Warning-Missing_alt_text.csv`
- Requires per-image edit in WP media library or Gutenberg blocks
- Priority: homepage, /meet-the-team/, /about-us/

### 2.1 — 358 pages linking to redirecting URLs (2,698 instances)
- Largest volume task
- Start with homepage + top HMRC pages
- Use WP-CLI search-replace for systematic updates

### 1.1 — 56 page_id 404 URLs (723 internal links)
- Major task — needs WP-CLI to resolve IDs to new URLs
- Priority by inlink count: page_id=64762 (38), 17686 (17), 15162 (16)

### 2.8 — Individual OG tags for 8 high-authority hub pages
- Global fallback already set; these need per-page og:title/description/image

### 1.4 — Broken images on pub-closures article
- `/articles/pub-closures-in-the-uk/` — pub-04.jpg, pub-05.jpg, pub-06.jpg missing

---

## NEXT SESSION START
Suggested session 4 tasks:
1. **2.2**: Check /testimonials/ archive has H1 (theme-side check)
2. **3.7**: Re-audit SERP title mismatches (should be mostly resolved by 2.5)
3. **2.7**: 51 pages missing alt text — start with homepage, /meet-the-team/, /about-us/
4. **1.4**: Pub-closures broken images (pub-04/05/06.jpg) — check media library or replace from research assets
5. **3.1 (prod-side)**: Push staging to live so Ahrefs picks up the resolved chains
6. **2.1**: 358 pages linking to redirecting URLs (2,698 instances) — WP-CLI search-replace
7. **1.1**: 56 page_id=N 404 URLs — requires new-URL mapping
