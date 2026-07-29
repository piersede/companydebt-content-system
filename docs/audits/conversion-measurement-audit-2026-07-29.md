# Conversion measurement audit — companydebt.com

**Date:** 29 July 2026
**Google Ads account:** 463-427-5788 (MCC 603-813-7400)
**Scope:** every route a lead can arrive by, and whether Google Ads can see it
**Method:** read-only. Nothing in the Ads account, the website or the CRM was changed.

---

## The one-paragraph version

Tracking on this site is better built than expected. There is a proper Google Ads conversion setup, Consent Mode v2, and website call tracking with number swapping — none of which anyone had confirmed. But almost all of it is switched off for most visitors, because **the site captures the Google click ID only for people who accept advertising cookies, and the cookie banner defaults to "no"**. That single gate explains the empty click IDs in the CRM, the dead offline-conversion pipeline, and a good part of why Google's reported conversions do not reconcile with real enquiries. The second problem is that I could not read the Ads account itself this session, so roughly a third of the coverage map below is honestly marked unverified rather than guessed at.

---

## Coverage map

| Lead channel | Measured? | Mechanism | Confidence |
|---|---|---|---|
| Web form — entry stored | **Yes** | Gravity Forms, working again as of 29 Jul | **Verified** |
| Web form — reaches CRM | **Yes** | Zoho lead created ~2s after submission | **Verified** |
| Web form — tied to an ad click | **Partial** | Only if visitor accepted ad cookies | **Verified** |
| Web form — fires an Ads conversion | **Likely** | `generate_lead` pushed to GTM on confirmation | Inferred |
| Phone — call from ad (call extension) | **Unknown** | Requires Ads account read | **Unverified** |
| Phone — call from website | **Yes, configured** | Google forwarding number on 0800 074 6757 | **Verified (deployed)** |
| Phone — visitor reads number, dials later | **No** | Not technically trackable | **Verified** |
| Phone — tied back to a specific ad click | **Partial** | Depends on consent + swap firing | Inferred |
| LiveChat — conversation happens | **Yes** | LiveChat present site-wide | **Verified** |
| LiveChat — reaches CRM | **Yes** | Zoho leads tagged "Live Chat - CD" | **Verified** |
| LiveChat — tied to an ad click | **Partial** | Same consent gate | Inferred |
| Calculator (form 38) | **Yes** | Stored + Zoho | **Verified** |
| Guide download (form 30) | **Yes** | Stored; Ads conversion action exists | Inferred |
| Direct email clicks | **No** | No tracking on mailto links | **Verified** |
| Feedback form (form 6) | **No** | Deliberately excluded from Zoho | **Verified** |

---

## Gaps, worst first

### 1. Cookie consent silently switches off ad attribution
**Cost: the largest single blind spot. It caps everything downstream.**

The site's own attribution script contains this gate:

```js
function runCapture(){ if (started || !hasConsent()) return; ... }
```

`hasConsent()` returns true only when the CookieYes cookie contains `advertisement:yes`, `analytics:yes` or `performance:yes`.

I loaded the live homepage with a Google click ID in the URL and did not accept cookies. Result:
- `cd_*` attribution cookies stored: **none**
- Google `_gcl` / `_ga` cookies stored: **none**
- Consent state: all six ad/analytics signals **denied**, only `security_storage` granted

So for any visitor who ignores or declines the banner, the click ID is never captured, never written to the form entry, never passed to Zoho, and can never be uploaded back to Google. This is exactly why the Zoho `GCLID` field arrives empty and why 453 of 456 click-ID leads were already outside the 90-day window.

The defaults are legally correct for the UK. The problem is that nobody has measured what they cost, and no fallback exists.

**Fix:** measure the consent acceptance rate first, then decide. Options include a clearer banner, and enabling Consent Mode modelling in Ads so Google estimates the unobserved conversions.
**Who:** Piers for the Ads-side setting. Claude can measure and prepare the banner change.

### 2. No read access to the Google Ads account
**Cost: prevents certainty on roughly a third of this audit.**

The `google-ads-mcp` server is not connected in this session, and the Google Ads Python library is not installed. OAuth credentials exist at `google-ads-auditor/credentials/` with the correct `adwords` scope, but the developer token is supplied via environment variables that are not set.

Unverifiable as a result: the conversion action inventory, which are primary vs secondary, counting settings (one vs every), attribution model, lookback windows, duplicate actions, whether enhanced conversions are switched on, and what Performance Max is reporting.

**Fix:** restore the MCP connection or install the library and set the developer token.
**Who:** Piers (needs the developer token and Basic Access state confirmed).

### 3. Forms accept junk, which pollutes the CRM and caps enhanced conversions
**Cost: moderate, and it blocks a feature you will want.**

Contact Us (form 41) and the homepage block (form 44) declare Name, Email **and** Telephone as plain text fields, with no spam protection. Nothing is validated.

- Contact Us: 18 of the last 200 entries have an unusable email
- Homepage block: 10 of 76 unusable; 45 of 76 phone numbers fail a UK format check

Enhanced conversions for leads works by matching a hashed email address. Every lead with no usable email is permanently unmatchable. Switching the feature on over this data would quietly under-report and look like poor ad performance.

**Fix:** **Done in code, 29 Jul** — `mu-plugins/cd-gform-hardening.php` adds honeypot enforcement, email validation, UK phone validation and outreach-spam blocking. Still needs deploying and verifying on staging, then live.

That job also confirmed and extended this finding:
- forms that already use a properly typed email field had **0 bad emails across 622 entries**, so field typing was the entire cause
- phone numbers are now stored in E.164 (`+447700900123`) rather than `07700900123`, because the readable form is the one Google cannot match on
- a knock-on effect not spotted in this audit: `cd-livechat-zoho.php` only accepts a value containing `@`, so junk emails reached Zoho blank, and a blank **defeats the duplicate check** — meaning every bot created a brand new lead rather than merging into an existing one

**Who:** Claude for the staging deploy, Piers to approve the live push.

### 4. Phone measurement is thinner than it looks
**Cost: unquantified, likely material, since phone is a primary channel.**

Good news first: website call tracking **is** deployed. The page runs

```js
gtag('config', 'AW-977276330/xrGGCKvV68gDEKqbgNID', { phone_conversion_number: '0800 074 6757' })
```

and Google's number-swap loader (`gstatic.com/wcm/loader.js`) loads. So the assumption that phone tracking was never set up is **wrong**.

What is still open:
- number swapping only applies to visitors Google identifies as ad clicks, so it inherits the same consent problem
- a visitor who reads the number and rings from a different phone is untrackable by any system
- call-from-ad conversions and any minimum-duration threshold cannot be checked without account access
- five `tel:` links on the homepage alone; clicks on these by non-ad visitors are not counted anywhere

**Fix:** verify call conversions in the account, confirm the duration threshold is sensible.
**Who:** Piers, or Claude once access is restored.

### 5. The "GA4 points at the wrong site" claim looks wrong
**Cost: it misdirected the previous audit round.**

The live site tags GA4 property **G-P39KJ34V6G**, which is a companydebt.com property, on every page checked. So the website is not sending its data to businessexpert.co.uk.

What I *can* see through the connected analytics account is only one property, `www.businessexpert.co.uk GA4` (328407537), and that one is linked to Google Ads customer **6811589135** — which is neither Company Debt (4634275788) nor its manager account. That is a different business's link, not Company Debt's.

The Ads account config also lists conversion actions literally named `www.companydebt.com - GA4 (web) form_submission` and `www.companydebt.com - GA4 (web) Chat`, which strongly suggests a companydebt.com GA4 property *is* linked to the Ads account.

**Read this carefully:** the earlier finding appears to have come from looking at the only GA4 property the service account could see and assuming it was the linked one. That is the same class of mistake the previous round was weakened by. It needs confirming in the Ads interface, not inferring.

**Fix:** open Google Ads → linked accounts and read which GA4 property is attached.
**Who:** Piers (two minutes in the interface).

### 6. Second GTM container appears to be dead already
**Cost: low. Listed so nobody retires the wrong one.**

Across the homepage, /contact-us/, /quick-quote/ and /company-liquidation/, only **GTM-5GTD9ZP** loads. **GTM-KT6M67T does not appear in any page's source or runtime.** The live container carries the Ads conversion ID AW-977276330 and the GA4 ID.

**Fix:** confirm inside GTM that KT6M67T holds no active tags, then archive it.
**Who:** Piers.

### 7. Tracking only starts after the visitor interacts
On first load, no GTM, no dataLayer, nothing. Tags appeared only after I simulated scroll and mouse events. I could not isolate whether this is the consent tool, WP Rocket, or this browser — WP Rocket was not parking scripts, so consent is the most likely cause. A fast bouncer may be invisible to all measurement.

**Fix:** re-test in a normal browser with cookies accepted.
**Who:** Claude, if you want it chased.

---

## What I verified versus what I am reasoning about

**Verified — I read this directly from the live site, database or CRM today:**
- Gravity Forms storage is working again (entries 8293, 8294 on 29 Jul)
- Form → Zoho handoff, ~2 second latency, `Lead_Source = "Website Form - CD"`
- Zoho has a `GCLID` field and it arrived empty
- Attribution capture is gated on cookie consent (read the deployed source)
- With consent denied and a click ID present, nothing is captured
- Consent Mode v2 is implemented, all seven signals, defaults denied
- Website call tracking is configured on 0800 074 6757
- One GTM container is live; the site's GA4 is a companydebt.com property
- Form field types, spam settings, and the invalid email/phone counts

**Inferred — reasoning from evidence, not confirmed:**
- That form submissions fire an Ads conversion (the `generate_lead` push exists; I did not watch one land in Ads)
- That a companydebt.com GA4 property is linked to the Ads account (based on conversion action names)
- That the three deleted entry records were the 28 Jul test submissions
- That consent, not caching, is what delays tag loading

**Not verified at all — no access this session:**
- Every in-account setting: conversion inventory, primary/secondary split, counting, attribution, lookback, duplicates, enhanced conversions, Performance Max reporting
- The consent acceptance rate
- Whether the Zoho → Ads offline import has since been connected

The specific claim from the July round that conversion tracking *overstates* volume could not be confirmed or quantified without account access. What I can say is that spam submissions do create real Zoho leads, so if form submissions fire a conversion, bot traffic is inflating the count.

---

## Recommendations

**Do first**
- Check what the cookie banner is costing you — measure the acceptance rate before changing anything else
- Confirm in Google Ads which GA4 property is actually linked; do not act on the "wrong site" claim until you have looked
- Restore Google Ads API access so the account settings can be audited properly

**Do next**
- Deploy and verify the form hardening (written 29 Jul, not yet on staging or live)
- Do not switch on enhanced conversions for leads until that email validation is actually live, not merely written
- Fix `scripts/check_unmerged_branches.py` — it crashes on any repo using worktrees, so the safety net for unmerged work is currently dead
- Confirm the phone conversion settings in the account, including any call-duration threshold
- Check inside GTM that container KT6M67T is empty, then archive it

**Do after that**
- Turn on Consent Mode modelling in Ads so declined-cookie conversions are estimated rather than lost
- Get one real ad click through a form end to end and confirm the click ID reaches Zoho
- Decide whether the Zoho → Ads offline import is worth reconnecting once click IDs are actually being captured

**Do not do**
- Do not retire either GTM container before checking its contents
- Do not read anything into "no click ID" until the consent gate is fixed — it is the cause, not the symptom
- Do not push the database from staging to live, under any circumstances
