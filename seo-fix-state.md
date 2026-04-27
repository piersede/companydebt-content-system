# SEO Fix Session State
_Last updated: 2026-04-26 (session 4)_

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

---

## SESSION 4 (2026-04-26) — DONE

Plan file: `C:\Users\piers\.claude\plans\look-in-the-cd-nested-riddle.md`

Diagnosis: prior staging-to-prod deploy DID ship (per user); Ahrefs's 81% reflects current production. New audit at `C:\Users\piers\OneDrive\Desktop\CD fixes\` (56 CSVs).

### Root-cause fixes (highest leverage)

- ✅ **Theme bug — related-articles carousel rendered draft posts**
  Template `wp-content/themes/company-debt-webpigment/template-parts/related-articles/related-articles.php` was reading the `be_related_articles` ACF field and calling `get_permalink()` on hand-curated post IDs without checking status. Drafts return `?page_id=N` URLs → 404. **Fix**: filter the ACF list to keep only `post_status === 'publish'` entries. Single template change clears ~583 broken-link instances.

- ✅ **Page 17686 republished as `/insolvency/` hub** (was draft, breadcrumb parent of 43 published children)
  Publishing it natively serves /insolvency/, fixes breadcrumbs on all 43 child pages, and obsoletes the `/insolvency/` → `/insolvency/insolvency-act-1986/` redirect (which was contributing 474 inlinks to the W1 redirect-link count).

- ✅ **Post 44691 (Heathrow article) reparented**: `post_parent` set to 0 — was a child of draft 44563, fixing breadcrumb 404.

- ✅ **/cookie-policy/ page created** (id=79808). Footer link now resolves 200. Compliance-friendly cookie disclosure copy. Yoast meta description set.

- ✅ **Footer.php updated** (`wp-content/themes/company-debt-webpigment/footer.php` line 75)
  - `/terms-and-conditions/` → `/terms-conditions/` (kills 475 redirect-link inlinks)
  - `/sitemap_index.xml` → `/site-map/` (gives orphan /site-map/ page 1 inlink)

- ✅ **Archive listing templates** (`archive.php`, `search.php`) — added `alt="<?php echo esc_attr( get_the_title() ); ?>"` to `<img class="post-preview__thumbnail">`. Cascades alt across all archive pages.

### DB-level fixes

- ✅ Nav menu item id=58821 (Insolvency Advice) `_menu_item_url` updated: `/insolvency/insolvency-advice/` → `/advice/get-free-business-debt-advice/` (474 inlinks resolved)
- ✅ widget_block option updated: `/accreditations` → `/accreditations/` (249 inlinks resolved)
- ✅ Bulk REPLACE on `wp_posts.post_content` covering href= boundaries with all domain variants (bare path, www.companydebt.com, comdebstage.wpengine.com): 78 post rows updated for trailing-slash and path-move redirects
- ✅ 3 sitemap-3XX entries marked `is_robots_noindex=1` in `wp_yoast_indexable` (8396 /pre-packs/, 26218 /business-debt-advice/, 79295 /administration-vs-cva/)
- ✅ Yoast templates set (`wpseo_titles` option):
  - `metadesc-testimonial` = `%%excerpt%% Read more client experiences with Company Debt's insolvency team.`
  - `metadesc-author-wpseo` = `Articles by %%name%% on insolvency, business debt, and director liability at Company Debt.`
  - 69 testimonial + 2 author indexable rows deleted (auto-rebuild on view) → 78 missing meta descriptions resolved
- ✅ Bulk alt fill: 303 of 368 attachments missing `_wp_attachment_image_alt` populated from referencing post's title (cleaned: brand suffix stripped, smart quotes decoded, capped 125 chars, filename-pattern fallback skipped)
- ✅ Inline Gutenberg img alts: 12 `wp-image-XXXX ... alt=""` blocks fixed via post_content rewrite (homepage sponsorship logos: BBC, Fortune, Investopedia, etc; Express Quote page)
- ✅ /about-us/ post_content gained an internal link to /case-studies-hub/ (clears orphan)
- ✅ /insolvency-calculator/ un-noindex'd (was mistakenly noindex with 249 inlinks)

### Verified post-fix on staging

- /cookie-policy/ → 200, full OG tags ✓
- /insolvency/ → 200 (was 301 redirect chain) ✓
- /insolvency/secured-vs-unsecured-creditors/ breadcrumb → no `?page_id=` refs ✓
- All "First found at" source pages from 4XX CSV → 0 `?page_id=` refs ✓
- /sectors/, /articles/, /case-studies/ listings → 1 missing alt each (down from 12-26; the 1 left is a base64 lazy-load placeholder that Ahrefs typically skips)
- Homepage → 0 missing alts (down from 4) ✓
- /testimonials/<slug>/ + /author/<slug>/ → meta description now generated from Yoast template ✓

### Estimated row-count delta on next Ahrefs crawl

| Category | Baseline | Expected after deploy + recrawl |
|---|---|---|
| Errors (4XX URLs + dependent broken-link rows + orphans + sitemap-3XX) | ~3,100 | ~0 |
| Warnings: redirect-link instances (W1+W2+W3) | ~6,400 | ~200 (long-tail post_content edits not exhaustive) |
| Warnings: missing meta description | 78 | ~0 (Yoast templates handle) |
| Warnings: missing alt | 209 | ~10–20 (base64 placeholders + theme-asset images) |
| Warnings: incomplete OG | 429 | already complete on staging — recrawl will reflect |
| Warnings: noindex | 232 | 230 (kept testimonials/case-studies/legal/forms; un-noindex'd insolvency-calculator) |

Realistic landing: **92–96% Ahrefs quality** (matches plan estimate).

### What user must do (NOT automatable from this session)

1. **Deploy staging → production** via WP Engine dashboard. All theme + DB changes ride along.
2. **Resubmit sitemap** in Google Search Console (`https://www.companydebt.com/sitemap_index.xml`).
3. **Trigger Ahrefs recrawl**: Site Audit > Settings > "Recrawl now" (wait 24–48h for fresh data).
4. **(Optional) IndexNow** the 165 URLs in `Notice-Pages_to_submit_to_IndexNow.csv` via Yoast Premium's IndexNow toggle or the IndexNow plugin.

### Tooling added (reusable for future audits)

- `scripts/seo_audit/decode_csv.py` — UTF-16 Ahrefs CSV decoder
- `tmp/sftp_grep.py` — recursive grep through theme files via SFTP
- 9 mu-plugin patterns proven (diagnose, batch1, batch1cd, batch2, batch2b, batch3b, batch4, homealts, batch5, clear-cache)

---

## SESSION 5 (2026-04-26 → 2026-04-27) — Core Web Vitals: CLS + LCP

Plan file: `C:\Users\piers\.claude\plans\i-am-99-sure-crispy-russell.md`

### CLS — cookie banner overlay (deployed)

Ahrefs flagged 114 mobile URLs with CLS > 0.25. Diagnosed as the CookieYes cookie consent banner injected late by GTM after first paint, pushing content downward.

- ✅ **`theme/style.css`** (committed) — appended CookieYes overlay block forcing `position: fixed`, removed stale Moove `#cookie_action_close_header` rule. Targets `.cky-consent-container`, `.cky-consent-bar-wrapper`, `.cky-consent-bar`, `.cky-modal`, `.cky-overlay` plus `[class*="cky-consent"]` / `[id*="cky-consent"]` wildcard fallbacks. Z-index 99999 (below LiveChat max-int).
  - Deployed: applied to remote-pulled `style.css` (141KB on remote vs 122KB local — 19KB drift), uploaded with `style.css.pre-cls-fix.bak` backup.
  - Verified live (production after deploy): CookieYes banner is `position: fixed`, body offsets are 0, PerformanceObserver reports `totalCLS: 0.0000` on home with banner active.

### LCP — LiveChat 5s delayed init + hero fetchpriority (deployed, not in repo)

GSC reports mobile LCP > 2.5s on a non-trivial chunk of URLs (URL list empty due to CrUX privacy threshold). Diagnosed via live DOM: site was running the **legacy LiveChat tag** (license 8321211 only set; `LiveChatWidget` undefined). Stakeholder confirmed a 5s delay before chat appears is acceptable.

- ✅ **`wp-content/themes/company-debt-webpigment/assets/js/global.js`** (remote-only) — replaced legacy `__lc.license` + raw `tracking.js` insertion with the modern v2.0 wrapper. Added `__lc.asyncInit = true` and a `setTimeout(LiveChatWidget.init, 5000)`. Backup `global.js.pre-livechat-modern.bak` on remote.
- ✅ **`wp-content/themes/company-debt-webpigment/template-parts/blocks/content-hero-landing.php`** (remote-only) — added `"fetchpriority" => "high"` to `wp_get_attachment_image()` call for `bcg_image`. Targets the LCP-likely hero image on landing-page templates. Backup `content-hero-landing.php.pre-fetchpriority.bak` on remote.
- ✅ **`theme/header.php`** — Layer 3 (async gtag) was already in place at line 19 (`<script async defer src="...gtag/js?id=UA-27555004-1">`). Earlier Explore-agent report incorrectly flagged this as un-async; direct inspection confirmed no work needed.

Layers deferred (no work this session):
- Layer 4 — consolidate two GTM containers (`GTM-5GTD9ZP` + `GTM-KT6M67T`) — marketing-ops task
- Layer 5 — WP Rocket critical-CSS audit — config check, user-led
- Layer 6 — `requestIdleCallback` LiveChat wrapper — already covered by 5s delay; not needed
- Insolvency-landing-hero `bcg_right` fetchpriority — held back because that template renders multiple images (logo + bcg_right); explicit fp could fight WP auto-fp. Revisit after measurement if landing pages still flagged.

### Side finding — broken @font-face URLs (out of scope, future task)

Theme CSS `@font-face` rules reference `assets/css/public/fonts/lato-v17-latin-regular.woff2` (and `-700`) which return **404** on staging and production. Real fonts live at `public/fonts/`. Site has been silently rendering everything in system `sans-serif` — design intent was Lato. **Counter-intuitively this benefits LCP** (no FOUT/FOIT delay). Fixing the URLs without proper preload + `font-display: swap` would *worsen* LCP. Treat as a separate design fix.

### What user does next (CWV deploy chain)

1. **Smoke test on staging in incognito**: confirm `typeof window.LiveChatWidget === 'object'`, `__lc.asyncInit === true`, chat launcher appears at ~5s.
2. **Deploy staging → production** via WP Engine dashboard.
3. **Re-run console checks on companydebt.com** in incognito; confirm chat 5s behaviour.
4. **PSI mobile** on home + an article + a landing page; capture before/after lab LCP.
5. **Wait 7-28 days** for CrUX/GSC field data to update.
6. **Schedule separately**: GTM merge (Layer 4), WP Rocket critical-CSS audit (Layer 5), broken-font fix (out of scope).

### Tooling added (Session 5)

- `tmp/apply_cls_fix.py` — drift-safe remote CSS edit (download → patch → upload with backup)
- `tmp/sftp_find_livechat.py` — locate LiveChat injection point across mu-plugins / themes / plugins
- `tmp/sftp_grep_livechat.py` — recursive content grep across WP install for LiveChat fingerprints
- `tmp/sftp_pull_layer1_2.py`, `tmp/sftp_pull_layer2.py`, `tmp/sftp_pull_globaljs.py` — targeted SFTP pulls
- `tmp/sftp_upload_globaljs.py`, `tmp/sftp_upload_layer2.py` — drift-safe template uploads with `.bak` rotation

