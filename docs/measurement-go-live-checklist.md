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

**Cache clear done (Piers, 29 Jul) — VERIFIED LIVE:**
- WP Rocket cache cleared + Cloudflare purged.
- `check_consent_tag_order.py --target live` = **4/4 PASS** on `/`, `/contact-us/`, `/quick-quote/`. Consent snippet present, before GTM, un-delayed; GTM loader freed; capture script delayed (intended).
- Form entries still identical (form 44 = 76, newest 2026-07-29 04:11:37). Database confirmed untouched end to end.

**The measurement/consent go-live is COMPLETE and verified.**

**STILL OPEN (follow-ups, not blockers):**
1. **End-to-end proof:** load a live page with `?gclid=CDLIVETEST0729`, accept cookies, submit a form → confirm a `Website Form - CD` lead in Zoho carrying that click id. Then delete the test lead. This is the one thing not yet proven from here (needs a real submission).
2. Once proven, turn `CD_LC_DEBUG` off in `cd-livechat-secrets.php` (staging) and re-copy files.
3. Account-side (Maria/Piers, separate): set the Zoho lead-creation action to secondary before real data flows; remove the extra consent requirement on the two call tags; leave enhanced conversions off until the forms-hardening is live; investigate the phone-lead drop.
4. Ship the held-back forms-hardening plugin (`cd-gform-hardening.php.off-hold-20260729`) as its own later step once the measurement change has bedded in.

---

## Follow-up: CookieYes banner fixes — staged 30 Jul, pending next live push

New file on staging: `wp-content/mu-plugins/cd-cookieyes-banner-fix.php`. Two fixes:
1. **Banner shows on load.** Excludes the CookieYes loader (`client_data/<id>/script.js`) from WP Rocket's delay, so the banner paints without waiting for interaction. Verified on live that this script IS currently delayed (`type=text/rocketlazyloadscript`, data-rocket-src `.../cache/min/1/client_data/387f1b54.../script.js`) and that the exclusion patterns match it. Consent stays safe: the denied-by-default snippet is already un-delayed and runs first.
2. **Preferences panel centred.** CSS override forcing `.cky-modal` to a full-viewport flex-centre overlay and constraining `#ckyPreferenceCenter` to 845px. Verified against the real live banner markup (injected in-session): panel moves from x:-1272 (half off-screen) to dead-centre, within 1px, fully on-screen at 2560px wide.

**UPDATE 25 Aug 2026 — the key in this file changed.** The CookieYes account behind
`387f1b54d36b6afe444ba7b09ed20e83` was suspended for non-payment, which took the banner off the site
completely. The replacement key is `fd66253e39627c5f6bcc131c`, and the loader now sits directly in
`header.php` rather than being injected by the `cookie-law-info` plugin. `cd-cookieyes-banner-fix.php`
hard-codes the key in its delay exclusion, so **live is currently carrying the dead key** and both
files must go live together. Changing one without the other leaves the banner delayed until the
visitor's first scroll, which is the exact fault this file was written to fix.

**IMPORTANT — cannot be tested on staging.** CookieYes runs only on live; its activation lives in the WP database, which is never copied. Staging shows no banner at all. So this fix was verified against live's markup in a browser session, and must be re-verified on live after the push:
- Load live in a fresh browser (incognito), do NOT interact: banner should appear on load.
- Click "Customise" on a wide screen: panel should be centred and fully visible.

This goes live on the **next** file-system copy (same method as the measurement push). It was NOT in this morning's push.

**PUSHED + VERIFIED LIVE, 30 Jul 2026.** Files-only copy (DB excluded, HTTP 202), WPE caches purged, WP Rocket + Cloudflare cleared by Piers. Verified on live at 2560px in a fresh browser:
- Banner appears on load with no interaction. ✓
- Shorter compliant wording live ("...improve your experience, measure our traffic and show relevant ads. Choose Accept, Reject or Customise below."). ✓ (published in CookieYes dashboard, not a file)
- Customise panel opens dead-centre (0px offset), fully on-screen. ✓
- Measurement guard still 4/4 PASS; form entries identical (form 44 = 76, newest 2026-07-29 04:11:37) — DB untouched. ✓

**Follow-up (harmless, staged): pattern narrowed.** The initial exclusion used a bare `cookieyes` pattern which also matched the click-id capture inline script (it references the `cookieyes-consent` cookie), un-delaying that script too. Harmless (the capture script is consent-gated), but not intended. Narrowed to `client_data` / `cdn-cookieyes.com` / the client id on staging (v3). Rides the next push; no dedicated push needed just for this.

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
