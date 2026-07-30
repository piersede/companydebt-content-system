# Measurement go-live checklist

**Date:** 29 July 2026
**Purpose:** get the conversion-measurement work from staging onto live, safely.
**Verified live-vs-staging state before writing this** (read-only, `tmp/audit_live_vs_staging.py`).

---

## What is already live, and what is not

| Piece | Live now | Staging | Needs pushing? |
|---|---|---|---|
| Consent Mode default snippet (header.php) — sets "deny everything until they answer" | **NO** | yes | **Yes** |
| Keeps that snippet un-delayed (cd-consent-mode-defaults.php) | **NO** | yes | **Yes** |
| Frees the Google tag from WP Rocket's delay (cd-measurement-no-delay.php) | **NO** (still delayed — safe) | yes | **Yes** |
| Click-ID capture is consent-gated (in cd-livechat-zoho.php) | **NO** (old version: captures regardless of consent) | yes | **Yes** — this is a compliance improvement |
| Form → CRM handler for the two biggest forms (Contact Us #41, Home #44) | **NO** (old version live: those forms create no CRM lead) | yes | **Yes** |
| LiveChat → CRM webhook endpoint (cd-livechat/v1) | yes, but **stale** | yes (newer) | **Yes** (update) |

**Plain reading:** the LiveChat pipeline foundation is live but out of date. The three things that matter most — the consent safety net, freeing the tag so we can measure at all, and the fix that makes the two busiest forms create CRM records — are **not live**. Pushing does not weaken compliance; it strengthens it (the consent-gated capture replaces the old capture-regardless version).

---

## Files to push (all on staging, all tested, guard passes 4/4)

1. `wp-content/themes/company-debt-webpigment/header.php` — consent default snippet
2. `wp-content/mu-plugins/cd-consent-mode-defaults.php` — keeps it un-delayed
3. `wp-content/mu-plugins/cd-measurement-no-delay.php` — frees the Google tag
4. `wp-content/mu-plugins/cd-livechat-zoho.php` — consent-gated capture + form→CRM + chat→CRM
5. `wp-content/mu-plugins/cd-livechat-secrets.php` — credentials the above needs (confirm live copy is current)

---

## How it goes live

**Sanctioned method (CLAUDE.md): WP Engine "file system only" copy, staging → live.**

- This is **atomic**: all five files land together. So the one dangerous window — the tag freed while the consent default is missing — cannot occur. The strict push *order* only matters if files are placed individually; with a bulk copy it is automatic.
- **Never** include the database. A DB copy wipes live form entries/users. File-system-only only.

**Pre-push prep completed on staging (29 Jul):**
- `cd-resave.php` — inert one-off maintenance file — **disabled** (renamed to `.bak-preLive-20260729`) so it will not ride along.
- `header.php` — **diffed live vs staging** (`tmp/diff_head.py`): staging's static header is live's header plus the consent snippet plus the un-delayed GTM, and nothing else. Overwriting live's header drops nothing.
- Credentials (`cd-livechat-secrets.php`) — all Zoho + LiveChat keys present. `CD_LC_DEBUG = true`, intentionally, so the first live run surfaces any failure as a visible debug lead. **Turn off after the end-to-end test passes.**
- Guard passes 4/4 on `/`, `/contact-us/`, `/quick-quote/`.

**Blast radius — one deliberate decision remains.** A file-system copy ships the ENTIRE staging filesystem, not just the five files above. The one rider that changes behaviour:
- `cd-gform-hardening.php` — forms spam/validation (honeypot, email/phone validation, outreach blocking). Built and tested for live, but it switches on stricter validation at the same time; overly strict rules could reject a genuine submission. **Decide before the copy:** ship it in this push, or move it aside on staging first.
- Otherwise, staging code is expected to be ahead of or equal to live (staging-first workflow); no live-only hotfixes are known. Live theme/plugin files cannot be read from here to diff exhaustively, so this is reasoned, not proven.

**Surgical alternative (Piers's own WPE access only):** place files 1–5 on live via SFTP/SSH/WPE file manager, then purge once. If done this way, upload all five *before* purging so they go live together.

---

## GO-LIVE RECORD — 29 July 2026

**Pushed:** files-only copy staging → production via `scripts/wpe_copy_files_to_live.py --confirm` (destination verified as www.companydebt.com; `include_db: false` asserted). API returned **HTTP 202** (queued). Forms plugin held back (`.off-hold-20260729`), `cd-resave` held back.

**Verified after the push:**
- **Database untouched.** `check_live_form_entries.py` identical before and after — form 44 still 76 entries, newest 2026-07-29 04:11:37; all other counts unchanged. The copy did not touch a single row.
- **Code correct at origin.** Cache-busting fetch of live shows the consent snippet present and the GTM loader freed (`<script>`, not `rocketlazyloadscript`).
- **WP Engine caches purged** (object, page, cdn — all 202).
- **Cached page, partial:** the consent snippet is now live AND un-delayed (the compliance-critical piece), but the GTM loader still shows delayed on the cached page. This is WP Rocket's page cache, not a code problem.
- **Interim state is safe:** consent defaults denied + GTM delayed = no tags fire without consent.

**STILL REQUIRED — manual, live wp-admin / dashboards only (cannot be done from here):**
1. **Live wp-admin → WP Rocket → Clear cache.** Regenerates cached pages with the freed tag. App passwords can't reach wp-admin and there's no purge route, so this is Piers's click.
2. **Cloudflare dashboard → Caching → Purge Everything** (no Cloudflare API creds in .env by design).
3. After both: re-run `python scripts/check_consent_tag_order.py --target live` → should read **4/4 PASS**.
4. **End-to-end proof:** load a live page with `?gclid=CDLIVETEST0729`, accept cookies, submit a form → confirm a `Website Form - CD` lead in Zoho carrying that click id. Then delete the test lead.
5. Once proven, turn `CD_LC_DEBUG` off in `cd-livechat-secrets.php` (staging) and re-copy files, or edit live via the portal.

---

## After the push — do NOT trust a 200

1. `python scripts/check_consent_tag_order.py --target live` → must read **4/4 PASS**
2. Purge caches: WP Rocket + WP Engine + **Cloudflare** (CLAUDE.md: Cloudflare too after any live push)
3. Re-run the guard after the purge (stale cached HTML can hide the change)
4. Clean mobile browser, do **not** touch the banner, then in the console:
   - `window.cdConsentDefaultApplied` → `true`
   - `google_tag_data.ics.entries.ad_storage` → `default:false`
   - `document.cookie` → no `_ga`, no `_gcl_*`
5. `python scripts/check_live_form_entries.py` (CLAUDE.md: after any live push)
6. **End-to-end proof:** submit a real test form with `?gclid=CDLIVETEST...` in the URL → confirm a `Website Form - CD` lead appears in Zoho with the click ID attached. This proves the two-big-forms fix and the capture together. (Delete the test lead afterwards.)

---

## Not part of this push — account-side, separate owners

These are Google Ads changes, not code, and mostly wait until the loop is proven:
- Set the Zoho lead-creation action to **secondary** before real data flows (stops one enquiry being counted twice). In Maria's email.
- Remove the extra consent requirement on the two website-call tags; delete the Custom HTML number-swap duplicate.
- Leave enhanced conversions **off** until forms validation (hardening) is live.
- Investigate the phone-lead drop (128 in 90 days → 21 in 30 → 4 in 7). Biggest open question; not a measurement fix.
