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

**Blast radius — read before copying.** A file-system copy ships the ENTIRE staging filesystem, not just these five. Also currently active on staging and would ride along:
- `cd-gform-hardening.php` — forms spam/validation (honeypot, email/phone validation, outreach blocking). Intended for live eventually, but decide deliberately: overly strict validation could reject genuine submissions. Either accept it in this push or move it aside on staging first.
- `cd-resave.php` — inert one-off (only fires on `?cd_resave=run`, then self-deletes). Clutter; ideally delete from staging before the copy. Not a blocker.
- Anything else changed on staging since the last live file copy.

**Surgical alternative (Piers's own WPE access only):** place files 1–5 on live via SFTP/SSH/WPE file manager, then purge once. If done this way, upload all five *before* purging so they go live together.

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
