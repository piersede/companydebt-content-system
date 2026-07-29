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

**Fix:** **Written and deployed to staging, 29 Jul** — `mu-plugins/cd-gform-hardening.php` (27 KB, on staging at 09:03) adds honeypot enforcement, email validation, UK phone validation and outreach-spam blocking. Confirmed present on staging by SFTP. **Not yet on live** — that is Piers's push to make.

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
- Test the form hardening on staging, then push it to live (it is on staging already)
- Do not switch on enhanced conversions for leads until that email validation is live, not merely on staging
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

---
---

# Addendum — Tag Manager and Google Ads read directly, 29 July 2026

**Method:** read-only, through Piers's own signed-in Chrome (`jamesonsmithandco@gmail.com`, authuser=1). Nothing was created, edited, paused, published or deleted. No GTM version was published. Two dialogs were opened and closed without saving (Ads default consent settings, GTM template-update list).

This addendum closes most of gap #2 above ("no read access to the Google Ads account") and **corrects two things the main audit got wrong.** Corrections are flagged inline.

---

## 1. What Google is actually reporting as a problem

There are two separate warning surfaces, and they are not the same thing.

### 1a. The GTM container warning (mild)

Inside container **GTM-5GTD9ZP → Workspace → Overview**:

> **Container quality: Needs Attention**
> Some issues are detected that may need your attention. — *View 1 issue*

**VERIFIED.** The single issue behind that banner is:

> **1 template update available** → *Available Template Updates:* **CookieYes CMP** (Tag template, last edited "a year ago")

That is the whole thing. The cookie-banner tag template has a newer version available. It is housekeeping, not a measurement fault. It does **not** indicate a broken tag, an unlinked container, or a consent failure.

### 1b. The Google tag warning (this is the "Urgent" one)

The screen reached by clicking through from Google Ads is the **Google tag** admin page for `AW-977276330` ("Company Debt"), which lives in its own Google-tag container, not in GTM-5GTD9ZP:

> **Tag quality: Urgent**
> Tag issues are likely impacting your measurement. — *View 2 issues*

**VERIFIED.** The two "action items" are:

1. ⚠️ **"Some of your landing pages are not tagged"** — *"There are untagged landing pages that may impact the performance of your measurement."*
2. ℹ️ **"Get better signals by enabling Google tag gateway in just a few clicks"** — *"Google tag gateway may help improve your conversion tracking and unlock deeper insights by routing your measurement through your website's Content Delivery Network."*

Item 2 is a **feature advert, not a fault.** Google tag gateway is an optional first-party-serving product. It is counted as an "action item" and it is inflating the severity score. The status is "Urgent" on the strength of one genuine item.

**INFERRED:** the word "Urgent" here is Google's own scoring of its own checklist, not a statement that conversions have stopped. Conversions are being recorded (see §6).

---

## 2. The "44 included pages" question — what that number actually means

**VERIFIED.** The Google tag's own coverage panel (`AW-977276330` → *See untagged pages*) reads:

| | |
|---|---|
| **Included pages** | **46** |
| Not tagged | **3** |
| No recent data | **2** |
| Tagged | **41** |

**This is not a count of the website.** "Included pages" here is the set of pages Google's tag diagnostics is monitoring for this Ads tag — overwhelmingly **ad landing pages** it has seen paid traffic arrive on, plus a handful it has otherwise observed. Twelve of the rows are explicitly labelled `Landing`. A site with 600+ URLs but only ~45 pages ever used as ad destinations will show ~45 here. Nothing is missing.

For contrast, the **GTM container's** own Tag Coverage (Admin → Tag Coverage, a different and broader list) shows **1,004 included pages: 412 tagged, 584 no recent data, 8 not tagged.** That list is polluted — most of the 584 are `comdebstage.wpengine.com` staging URLs and seven are `claudeusercontent.com` design-preview URLs, none of which should be measured at all.

**The three genuinely untagged pages on the Ads tag:**

| URL | Ad landing page? |
|---|---|
| `www.companydebt.com/about-us/` | **Yes** |
| `www.companydebt.com/company-rescue-solutions/` | **Yes** |
| `www.companydebt.com/liquidation/what-happens-to-directors-in-liquidation/` | No |

**And two showing "No recent data":**

| URL | Ad landing page? |
|---|---|
| `www.companydebt.com/advice/get-free-business-debt-advice/` | **Yes** |
| `www.companydebt.com/contact-us/` | No — but it is the main conversion page |

`/contact-us/` returning "no recent data" is the line worth staring at.

**INFERRED, and this matters:** the main audit established that on the live site *nothing loads until the visitor interacts* — no GTM, no dataLayer on first paint. Google's tag-coverage crawler does not scroll or move a mouse. A page that only injects GTM after interaction will therefore be reported as **"not tagged" even when it is correctly tagged for real humans.** That is the most likely explanation for all five rows, and it means the fix is on the site (make GTM load on page load, gated by Consent Mode rather than by JavaScript that waits for interaction), not in Google's interface. This should be confirmed by loading one of the three pages and watching the tag fire without touching anything.

---

## 3. Which container is linked to Ads 463-427-5788, and by whom

**VERIFIED.**

- GTM Admin → Container → **External Account Links: "No external account links."** There is **no formal link** between the GTM container and the Google Ads account. (This is normal and is not the cause of the warning — the connection is made by the `AW-977276330` Google tag being deployed inside the container, not by an account link.)
- Google Ads → Tools → **Data manager → Connected products: empty.** Nothing listed.
- The live container version is **Version 81, published 28 Jul 2026 by `jamesonsmithandco@gmail.com`** (Piers). 15 tags, 11 triggers, 5 variables. Workspace changes: 0 (nothing sitting unpublished).

**Publishing history — worth reading.** The container has been published by five different accounts over the years:

| Account | Period | Notes |
|---|---|---|
| `jamesonsmithandco@gmail.com` | v78–81, Jul 2026 | Piers, current |
| `jamesjohnson32@gmail.com` | v77, Jun 2024 | "Consent Manager Pushed Live" |
| `nikoladonevski@yandex.com` | v63–76, 2022–2024 | bulk of historical work |
| `emipajk@gmail.com` | v35–43, 2021–2022 | |
| `pitel.pasha1@gmail.com`, `alona.likhter.ppc@gmail.com` | 2021 | |

**Current user access on the CompanyDebt GTM account (5 users):**

| Email | Role |
|---|---|
| `companydebt01@gmail.com` | **Administrator** |
| `jamesonsmithandco@gmail.com` (Piers Ede) | **Administrator** |
| `jamesjohnson32@googlemail.com` | User |
| `nikoladonevski@yandex.com` | User |
| `nikoladppc@gmail.com` | User |

Two of those are former-agency addresses that still have live access. **Piers's call**, but it is worth deciding whether they should.

---

## 4. Everything in GTM-5GTD9ZP (15 tags)

**VERIFIED — full inventory, live version 81:**

| Tag | Type | Firing trigger | Last edited |
|---|---|---|---|
| **Conversion Linker** | Conversion Linker | **All Pages** (Page View) | 2 years ago |
| CookieYes Consent Manager | CookieYes CMP | Consent Initialization – All Pages | 2 years ago |
| **Google Tag AW-977276330** | Google Tag | Initialization – All Pages | a day ago |
| Google Analytics GA4 Configuration | Google Tag | All Pages | 2 years ago |
| **Google Ads – Form Submissions** | Google Ads Conversion Tracking | 7 × `gform_confirmation_message_*` | a day ago |
| Google Ads – Chat Started | Google Ads Conversion Tracking | Chat (Custom Event) | 2 years ago |
| Google Ads – Guide Tracking | Google Ads Conversion Tracking | Guide Download | 2 years ago |
| Google Ads – Calls from Website | Google Ads Calls from Website | All Pages | 2 years ago |
| Google Ads – Calls from Website (different format) | Google Ads Calls from Website | All Pages | 2 years ago |
| **Google Ads – Website Call Number Swap** | **Custom HTML** | All Pages | **20 hours ago** |
| GA4 Form Submission | GA4 Event | same 7 gform triggers | a day ago |
| GA4 Chat | GA4 Event | Chat | 2 years ago |
| GA4 – Download Guide Tracking | GA4 Event | Guide Download | 2 years ago |
| GA4 Phone Number Click | GA4 Event | GA Call Click (`tel:` links) | 19 days ago |
| LiveChat – Chat Started Bridge to dataLayer | Custom HTML | All Pages | a day ago |

### 4a. The form conversion does NOT use `generate_lead`

**VERIFIED, and this contradicts an assumption in the main audit.**

The Ads form conversion is fired by **`Google Ads - Form Submissions`** (Conversion ID `977276330`, label `knohCMOu9KUDEKqbgNID`), triggered by **seven Element Visibility triggers**:

`gform_confirmation_message_29`, `_31`, `_38`, `_39`, `_40`, `_41`, `_44`

There is **no trigger anywhere in the container listening for `generate_lead`.** The full trigger list is 11 items: 1 Custom Event (`Chat`), 1 Just Links (`GA Call Click`, `tel:`), 1 Form Submission (`GoogleAds - Download Directors Guide`, attached to 0 tags), and 8 Element Visibility triggers. The site's `generate_lead` dataLayer push is currently doing nothing.

This is not automatically broken — Element Visibility on the Gravity Forms confirmation `<div>` does work — but it is **fragile in three specific ways**:

1. It breaks silently if a form's confirmation markup or ID changes, or if a form is rebuilt with a new ID.
2. It only covers seven forms. Any form outside that list fires no Ads conversion at all.
3. It fires on *visibility*, so a confirmation block that renders off-screen, or renders twice, behaves unpredictably — whereas a `generate_lead` event fires exactly once at exactly the right moment.

**INFERRED:** switching the trigger to the existing `generate_lead` custom event would be more robust and would automatically cover every form. That is a change, so it is Piers's decision, not something to do while auditing.

### 4b. Conversion Linker — present and correct

**VERIFIED.** `Conversion Linker` tag exists, requires no configuration, fires on **All Pages / Page View**, with built-in consent checks on `ad_storage`, `ad_personalization`, `ad_user_data` and **no additional consent checks**. It is not the cause of the warning. The main audit's worry here can be closed.

---

## 5. Consent settings on the tags — where things really are suppressed

**VERIFIED, per tag:**

| Tag | Built-in consent checks | Additional checks | Behaviour when cookies declined |
|---|---|---|---|
| Google Ads – Form Submissions | `ad_storage`, `ad_personalization`, `ad_user_data` | **none** | Fires in cookieless mode → feeds modelling |
| Conversion Linker | same three | **none** | Fires in cookieless mode |
| Google Tag AW-977276330 | (Google Tag, handles internally) | none set | Fires in cookieless mode |
| **Google Ads – Calls from Website** | `ad_user_data` | **Requires `ad_storage` for tag to fire** | **Completely blocked** |
| **Google Ads – Calls from Website (different format)** | `ad_user_data` | **Requires `ad_storage` for tag to fire** | **Completely blocked** |
| Google Ads – Website Call Number Swap (Custom HTML) | **none** | **none** | **Fires regardless of consent** |

Three things follow.

**(i) The two call tags are the only ones hard-blocked.** Every other Google tag in the container degrades gracefully — when consent is denied it still sends a cookieless ping, which is what lets Google model the conversion. The two call tags carry an **extra, manually-added** requirement (`ad_storage` must be granted) which stops them dead. With the banner defaulting to "no", website call tracking is off for most visitors. The numbers in §6 confirm this: **4 conversions in 90 days** from website calls.

**(ii) The Custom HTML number-swap tag added on 28 July bypasses consent entirely.** Its contents:

```html
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}
gtag('config','AW-977276330/xrGGCKvV68gDEKqbgNID',{'phone_conversion_number':'0800 074 6757'});</script>
```

This is what the main audit saw on the live site. Note:
- it uses **the same conversion label** (`xrGGCKvV68gDEKqbgNID`) as the existing `Google Ads - Calls from Website` template tag, so it is a **duplicate**, not an addition;
- Custom HTML tags have **no consent checks**, so it runs for visitors who declined — which is presumably why it was added, but it is doing by hand what the template tag was deliberately configured not to do;
- **GTM itself flags it**: *"Any gtag commands in custom HTML may not work as intended due to how the data layer processes information."*

**INFERRED:** the correct fix is to remove the extra `ad_storage` requirement from the template tag and delete the Custom HTML duplicate — not to keep both. Two tags calling `config` on the same conversion label is a recipe for confusing behaviour.

**(iii) Two call conversion actions for one phone number.** The two template tags differ only in the displayed format they swap (`0800 074 6757` vs `08000 074 6757`) — but they use **different conversion labels** (`xrGGCKvV68gDEKqbgNID` and `svdpCKP2ms8DEKqbgNID`), so the same phone line reports into two separate conversion actions in Ads. Any page displaying both formats is a double-count risk.

---

## 6. Google Ads account — read directly (closes main-audit gap #2)

**VERIFIED.** Account 463-427-5788, last 90 days (30 Apr – 28 Jul 2026). **61 conversion actions exist; roughly 40 are "Removed".** Live ones:

| Conversion action | Source | Status | Pri/Sec | Count | Window | In account goals | Conv. (90d) |
|---|---|---|---|---|---|---|---|
| **[N] GoogleAds Phone Calls From Ads** | Call from Ads | **Active** | **Primary** | One | 30d | Yes | **124.00** |
| **[N] GoogleAds Form Submissions** | Website | **Active** | **Primary** | One | 30d | Yes | **40.00** |
| Local actions – Directions | Google hosted | Removed | Primary | Every | 30d | No | **41.00** |
| www.companydebt.com – GA4 (web) form_submission | GA4 | **Active** | Secondary | One | 90d | No | **37.00** |
| [N] GoogleAds Chat | Website | No recent conv. | **Primary** | One | 30d | Yes | **26.00** |
| **[N] GoogleAds Phone Calls** (website calls) | Website | No recent conv. | Secondary | One | 30d | No | **4.00** |
| [N] GoogleAds Phone Calls (different number format) | Website | No recent conv. | Secondary | One | 30d | No | 0.00 |
| [N] Guide Download | Website | **Needs attention** | Secondary | One | 30d | No | 0.00 |
| www.companydebt.com – GA4 (web) Chat | GA4 | **Inactive** | Secondary | One | 90d | No | 0.00 |
| Zoho CRM Sales | Import from clicks | No recent conv. | Primary | One | 90d | Yes | 0.00 |
| Zoho CRM Leads/Contacts | Import from clicks | No recent conv. | Primary | One | 90d | Yes | 0.00 |
| Zoho CRM Lead Qualification | Import from clicks | No recent conv. | Primary | One | 90d | No | 0.00 |
| Deals / Sales orders / Leads (5 Zoho stage actions) | Import from clicks | No recent conv. | Primary | Every | 90d | No | 0.00 |
| Lead form – Submit | Google hosted | No recent conv. | Secondary | One | **1 day** | No | 0.00 |
| Conversation started | Google hosted | No recent conv. | Primary | One | 30d | Yes | 0.00 |
| Calls from Smart Campaign Ads, Smart campaign ad/map clicks to call, Smart campaign map directions | Google hosted / Call from Ads | No recent conv. | mixed | mixed | 30d | mixed | 0.00 |

**Account total, all conversion actions: 272.00 conversions, value 78.00.**

Settings on the two that matter:

- **[N] GoogleAds Form Submissions** — created 01/03/2022; Primary; **no value**; count One; click-through window 30 days, engaged-view 3 days, view-through 1 day; attribution **Data-driven**; **Enhanced conversions: Off**.
- **[N] GoogleAds Phone Calls From Ads** — created 01/03/2022; Primary; no value; count One; **call length threshold 60 seconds**; 30-day window; attribution **Data-driven**.

### What the numbers say

1. **Phone is the business.** 124 of 272 conversions (46%) are calls placed straight from the ad. That single action outweighs every website conversion combined.
2. **Website call tracking is effectively dead: 4 conversions in 90 days**, against 124 from ad-click calls. Given §5(i), the consent block is the obvious cause. Two more call actions sit at zero.
3. **Forms are being counted twice** — 40 (Ads tag) and 37 (GA4 import) are almost certainly the same submissions arriving by two routes. The GA4 one is Secondary and excluded from account goals, so **bidding is not double-counting**, but the headline "All conv." figure of 272 is inflated by roughly 37.
4. **41 conversions are "Get directions"** from an action marked *Removed*. For an insolvency practice taking enquiries by phone and form, directions clicks are not leads. They are 15% of the reported total.
5. **Every Zoho import action reads 0.00 with "No recent conversions".** This confirms, from the Ads side, what the main audit inferred: **the CRM → Ads offline pipeline is not delivering anything.**
6. **Enhanced conversions is Off** on the primary form action — consistent with the main audit's warning not to switch it on until email validation is live.
7. **~40 dead conversion actions** accumulated across four agencies. Clutter, not damage, but it makes the account very hard to read.

---

## 7. CORRECTION — Consent Mode modelling is already on

**VERIFIED.** Google Ads → Goals → Conversions → *[N] GoogleAds Form Submissions* → **Diagnostics**:

> ✅ **Status: Consent mode is implemented and modelling is active.**

**The main audit's recommendation "Turn on Consent Mode modelling in Ads so declined-cookie conversions are estimated rather than lost" is already done.** Google is already estimating the conversions from visitors who declined cookies. That materially softens gap #1: the consent banner is *not* costing the full conversion count in Ads reporting.

What the consent gate still costs, unchanged:
- the **click ID** is never captured, so nothing can be joined to a CRM record;
- the Zoho → Ads offline import stays dead;
- **website call tracking is fully blocked** (that one has no modelling fallback, because the tag never fires at all — §5(i));
- audience building and enhanced conversions remain capped.

## 8. CORRECTION — a companydebt.com GA4 property IS feeding the Ads account

**VERIFIED.** Two conversion actions named `www.companydebt.com - GA4 (web) form_submission` (Active, 37 conversions) and `www.companydebt.com - GA4 (web) Chat` (Inactive, 0) exist and are recording. The July claim that "GA4 is connected to the wrong site" is **wrong**, and the main audit was right to doubt it.

**Unexplained, flagged rather than guessed at:** Ads → Tools → **Data manager → Connected products** renders **empty**, showing no GA4 or Tag Manager link, while GA4-sourced conversions are demonstrably arriving. Either the link predates Data Manager and is not surfaced there, or the panel failed to load. Do not act on the empty panel.

Separately, Piers's Tag Manager shows **a second, older GA4 property for the same site**: `Keyword Hero - www.companydebt.com - GA4` (`G-BZVR9KP6N7`, `GT-PJ4J756`). It is not on the live site. Worth knowing it exists before anyone "tidies up" GA4 properties.

## 9. Ads account consent configuration — correct, do not change it

**VERIFIED.** Ads → Tools → Data manager → **Consent settings**:

- Website data → *"Tag data will be labelled as not having consent granted"*; setting is **"No. Do not automatically mark this data as consented."**
- Restricted data processing: **disabled**
- Imported and uploaded data → *"Imported and uploaded data will be labelled as not having consent granted."*

The dialog states: *"Any consent mode values specified on your website will override these settings."*

This is the **correct and lawful** configuration for a UK site running CookieYes. The "Yes, automatically mark this data as consented" option exists for sites that block the Google tag entirely until consent is given — which is not how this site works. **Do not flip it.** Doing so would tell Google that non-consented data is consented.

The second line does matter though: **uploaded/offline data is also labelled not-consented**, which limits what an offline import could do for personalisation even once it is working.

## 10. GTM-KT6M67T — still unresolved

**VERIFIED:** Piers's Google account can see exactly four GTM accounts and four containers:

| Account | Container | ID |
|---|---|---|
| AABRS | aabrs | GTM-5X92J4H |
| Business Expert | Business Expert | GTM-KKNZZTS |
| **CompanyDebt** | **Company Debt Web** | **GTM-5GTD9ZP** |
| Wealthmans | Wealthmans | GTM-N7DVTPD |

**GTM-KT6M67T is not among them.** It cannot be inspected, and therefore cannot be confirmed empty, from this account. The main audit's "do not retire it before checking its contents" still stands — but there is nothing to check *from here*.

There are **4 unopened Tag Manager invitations** on the account. One of them may be for that container. They were left unopened deliberately (accepting an invitation is a change).

**Practical position:** it is not on the live site, it is not in this account, and it cannot be archived by anyone here. Unless it turns up behind one of those invitations or under `companydebt01@gmail.com`, it is somebody else's container and can be left alone.

---

## Addendum summary — what to do, worst first

| # | Finding | Cost | Fix | Who |
|---|---|---|---|---|
| 1 | Website call tracking blocked by an extra `ad_storage` consent requirement on both call tags | 4 call conversions in 90 days vs 124 from ad-click calls | Remove the *additional* consent check from the two "Calls from Website" tags; delete the Custom HTML duplicate | **Piers, in GTM** (a change + a container publish) |
| 2 | Custom HTML number-swap tag added 28 Jul duplicates an existing conversion label and bypasses consent; GTM warns against it | Unpredictable double-config on `xrGGCKvV68gDEKqbgNID` | Delete once #1 is done | **Piers, in GTM** |
| 3 | 3 ad landing pages reported untagged (`/about-us/`, `/company-rescue-solutions/`, `/advice/get-free-business-debt-advice/`), `/contact-us/` shows no recent data | This is the entire "Urgent" warning | Almost certainly the interaction-gated tag loading, not the pages. Make GTM load on page load (consent-gated, not interaction-gated), then re-check | Claude to confirm the cause; Piers to approve the site change |
| 4 | Ads form conversion hangs off 7 Element Visibility triggers, not the `generate_lead` event that already exists | Silent breakage risk; no coverage for other forms | Repoint the tag to `generate_lead` | **Piers, in GTM** |
| 5 | Two call conversion actions for one phone number, different labels | Split/duplicated call reporting | Consolidate to one | **Piers, in Ads** |
| 6 | 41 "Get directions" conversions (15% of the reported 272) from a Removed action; 37 duplicate GA4 form conversions | Headline conversion count overstated by roughly a quarter | Report on Primary actions only, or clean the goal groupings | **Piers, in Ads** |
| 7 | ~40 dead conversion actions; 2 former-agency accounts still have GTM access | Confusion and unnecessary access | Tidy | **Piers** |
| 8 | CookieYes CMP tag template update available | Housekeeping | Accept the template update | **Piers, in GTM** |
| 9 | "Google tag gateway" prompt | **None — this is an advert, not a fault** | Ignore, or evaluate on its merits separately | — |

**Closed by this addendum:** Consent Mode modelling is already active (main audit item withdrawn); the GA4 "wrong site" claim is definitively wrong; the Conversion Linker is present and firing on all pages; the Ads account inventory is now on record.

**Still not verified:** whether GTM-KT6M67T exists at all; why Data Manager shows no connected products; the consent acceptance rate; whether the untagged-landing-page reports are caused by interaction-gated tag loading (stated above as the most likely cause, not proven).

---
---

# Addendum 2 — follow-up checks and the first changes made, 29 July 2026

Prompted by Piers's five-point list. Items 1–3 turned out differently from the first reading once the underlying data was checked; item 4 has been actioned; item 5 is closed by decision.

## A. "Get directions" and duplicate form conversions — already handled, no action needed

**VERIFIED.** Two independent checks:

1. **Last 7 days (22–28 Jul 2026): Get directions = 0.** Also Page views 0, Phone call leads 4, Submit lead forms 1. The action has stopped recording; the 41 in the 90-day window came from earlier in the period, before it was switched off. `Local actions - Directions` is already in the **Removed** state.
2. **The account-default goals are:** Purchase, Submit lead form, Sign-up, Phone call lead, Contact, Qualified lead, Leads from messages (plus 2 custom goals). **There is no "Get directions" account-default goal**, and the duplicate `www.companydebt.com - GA4 (web) form_submission` is Secondary and marked *not* included in account-level goals.

**So neither pollutes the conversions Google bids on.** Both appear only in the **"All conversions"** reporting column. The finding in Addendum 1 §6(3)–(4) stands as a *reporting* caveat, and is **withdrawn as a defect** — the account is configured correctly. The practical instruction is to read the "Conversions" column, not "All conversions".

Goal configuration detail worth recording:

| Account-default goal | Primary conversion actions | Campaigns using it |
|---|---|---|
| Purchase | 1 | 94 of 98 |
| Submit lead form | 1 | 95 of 98 |
| Sign-up | 1 | 94 of 98 |
| Phone call lead | 2 | 96 of 98 |
| Contact | 1 | 95 of 98 |
| **Qualified lead** | **5** | **0 of 98** |
| Leads from messages | 1 | 95 of 98 |

The Qualified lead goal holds the five Zoho CRM stage actions and **no campaign uses it** — consistent with §B below.

## B. Why the Zoho pipeline reads zero — it is not a new-setup teething problem

**VERIFIED.** Google Ads → Goals → Uploads. **34 uploads in total; the most recent was 8 April 2024.** All were manual CSV/XLSX files uploaded by the two former-agency accounts. Results:

| Date | File | Result |
|---|---|---|
| 8 Apr 2024 23:27 | Conversion_Import_by_GCLID.csv | 14 successful, **1,986 errors** |
| 8 Apr 2024 23:24 | Conversion_Import_by_GCLID.csv | No changes |
| 12 Feb 2024 17:16 | Conversion_Import_by_GCLID.csv | 1 successful, **1,999 errors** |
| 12 Feb 2024 16:40 | Conversion_Import_by_GCLID.csv | **2,000 errors** |
| 4 Dec 2023 16:38 | Conversion_Import_by_GCLID.csv | 1 successful, **1,999 errors** |
| 4 Dec 2023 16:36 | Conversion_Import_by_GCLID.csv | **2,000 errors** |
| 11 Oct 2023 | Conversion_Import_by_GCLID.csv | **2,000 errors** |
| 7 Sept 2023 22:37 | Company Debt - Conversion Import by GCLID.csv | No changes |
| 7 Sept 2023 22:36 | Conversion Import by GCLID.csv | 1 successful, **1,999 errors** |
| 12 Aug 2023 13:49 | Company Debt - Conversion Import by GCLID.xlsx | 2 successful, **3,999 errors** |

**Uploads → Schedules tab: "You don't have any entries yet."** No automated or recurring import has ever been configured.

**Conclusion.** Nothing has been sent to this account for over two years, and when it was, roughly 999 records in every 1,000 were rejected. The conversion actions themselves are correctly built — they are an empty pipe at both ends. This is consistent with the separately-verified position (`findings-v2/connection-3-status.md`, 27 Jul 2026) that the Zoho→Ads integration was never connected, and that 453 of 456 click-ID leads were already outside Google's 90-day import window.

**INFERRED:** the failures are the expected result of uploading click IDs that are either absent (never captured, per the consent gate) or older than 90 days. Re-uploading old data will not fix it.

### B2. CORRECTION to §B — the Uploads screen cannot see the new Zoho integration

**Raised by Piers, 29 July: the section above ignored the Zoho integration work done 26–28 July. That is a fair criticism and §B as originally written was wrong in its framing.**

**VERIFIED.** The **Uploads** screen logs **file-based imports only**. The Zoho→Google Ads integration reconnected on 28 July pushes through Google's conversion-upload **API**, which does not appear on that screen. So "nothing since April 2024" is a true statement about *manual CSV uploads* and tells us **nothing whatsoever** about the new pipeline. The conclusion "this is not a new-setup teething problem" was an overreach and is **withdrawn**.

**What is actually verifiable about the new integration:**

| Conversion action | Date created | Goal | Source | Window | Value rule | Data so far |
|---|---|---|---|---|---|---|
| `Zoho CRM Sales` | **28/07/2026** | Purchases, Primary | Import from clicks | 90 days | "Use different values. If there's no value, use £1." | none |
| `Zoho CRM Leads/Contacts` | **28/07/2026** | Sign-ups, Primary | Import from clicks | 90 days | same | none |
| `Zoho CRM Lead Qualification` | (same generation) | Qualified leads, Primary | Import from clicks | 90 days | same | none |

So **the reconnect did reach Google**: Zoho created its own conversion actions on 28 July, exactly as its documentation says it would. These are a **new generation**, distinct from the older stage-named actions (`Deals - Deals Stage becomes Closed Won`, `Leads - Leads Lead Status becomes Pre Qualified` and the `(1)`-suffixed duplicates) left behind by the earlier configuration.

**Both new actions currently show:** *"Start measuring conversions by connecting to a data source — This conversion action isn't receiving data because there aren't any associated connections."*

**INFERRED, and deliberately not called either way:** that banner is consistent with two different explanations — (a) Google's UI simply does not register an API-pushing partner integration as a "connection", which would make the banner cosmetic; or (b) the link is genuinely not registered on Google's side, which would tally with Data Manager → Connected products rendering empty (Addendum 1 §3). **Do not act on this until it has had a fair run.**

**Why zero is the expected reading right now, not evidence of failure:**

1. The integration was connected on **28 July**; Zoho's own note states it syncs **once every 24 hours**. The reporting window read in this audit was 30 Apr – 28 Jul, so effectively no elapsed time.
2. The acceptance-test lead (`1974818000085653001`) carries a **deliberately fake click ID** (`CDCONVTEST20260728A`). Google cannot match it to a real click, so even a perfectly successful export would not surface as a conversion. That test isolates whether **Zoho exports**, not whether **Google counts**.
3. Per the 28 July session record, the corrected Gravity Forms handler and the LiveChat v6 `get_chat` endpoint were **on staging only**, pending a live push. Until that push lands, live may still be running the earlier code, so genuinely new click-ID-carrying leads may not yet be reaching Zoho at all.
4. Of the 456 CD leads carrying a click ID, **453 are older than the 90-day import window** and the remaining 3 are test records.

**Correct conclusion, replacing §B's:** the *historical* manual pipeline is dead and re-uploading it is pointless — that part stands. But the *new* pipeline is roughly one day old, has correctly created its Google-side actions, and has had neither the time nor a single real recent click ID to prove itself. **It is too early to judge, and nothing here should be read as the integration failing.**

**The checkpoint is now due.** What to look at, in order:
1. Zoho's own integration sync/export log — that is the authoritative answer on whether Zoho is sending.
2. Whether the staging→live push of `cd-livechat-zoho.php` has happened, since without it live captures nothing usable.
3. Once a **real** ad click produces a lead: whether that lead's click ID reaches Zoho, and whether it appears against the Zoho conversion actions within 24–48 hours.

**Bidding caution when it does start working:** all three Zoho actions are **Primary**. `Zoho CRM Leads/Contacts` fires on lead creation, which is the *same event* the on-site `[N] GoogleAds Form Submissions` tag already counts as Primary. Once the pipe is live, that is a genuine double count in bidding — unlike the "Get directions"/GA4 pairs in §A, which are already excluded. Resolve before the flow becomes material: keep the on-site tag Primary for speed, and demote the Zoho lead-creation action to Secondary, keeping only the deeper outcomes (qualified, won) as Primary.

## C. "Deleting" dead conversion actions — mostly not possible

**VERIFIED.** In Google Ads, **"Removed" is the delete state** for a conversion action. They cannot be purged; they remain listed for historical reporting. The ~40 Removed actions therefore cannot be tidied further — only filtered out of the view (Status: Enabled).

What *can* be cleaned are the actions still **enabled but inert** (approximately 12):

| Action | Reason |
|---|---|
| Calls from Smart Campaign Ads | No Smart campaigns run |
| Smart campaign ad clicks to call | No Smart campaigns run |
| Smart campaign map clicks to call | No Smart campaigns run |
| Smart campaign map directions | No Smart campaigns run |
| Lead form – Submit | Google-hosted lead form not used; 1-day window |
| www.companydebt.com – GA4 (web) Chat | Status Inactive |
| [N] GoogleAds Phone Calls (different number format) | 0 conversions; duplicate |
| Zoho CRM Sales / Leads-Contacts / Lead Qualification | Keep only if the pipeline is to be fixed |
| Deals × 2, Sales orders, Leads (Zoho stage actions) | As above |

None of these affect bidding today. This is cosmetic tidying, not remediation.

## D. CHANGE MADE — three users removed from Tag Manager

**Done, 29 July 2026, on Piers's explicit instruction.** Google Tag Manager → CompanyDebt account → User Management. Removed direct account and container permissions for:

- `nikoladonevski@yandex.com` (User)
- `nikoladppc@gmail.com` (User)
- `jamesjohnson32@googlemail.com` (User)

**Verified after the change: 2 users remain**, both Administrator — `companydebt01@gmail.com` and `jamesonsmithandco@gmail.com` (Piers). Kept deliberately: `companydebt01@gmail.com`.

This is the only change made to any Google property in this session. No GTM container version was published, so the live tag configuration is untouched (still Version 81).

## E. Google Ads access — the ex-agency accounts were never there

**VERIFIED.** Google Ads → Admin → Access and security → Users. 5 users, and **neither Nikola account appears.** The former-agency exposure was Tag Manager only and is now closed.

| User | Access level | Email type | Last signed in | Added |
|---|---|---|---|---|
| `jamesonsmithandco@gmail.com` (Piers) | Admin | Personal | 29 Jul 2026 | 16 Nov 2016 |
| **Maria Waters** `mariawppc@gmail.com` | **Admin** | Personal | 29 Jul 2026 | 27 Feb 2024 |
| `ns@aabrs.com` | Admin | Unmanaged | 27 Jul 2026 | 14 May 2018 |
| `companydebt01@gmail.com` | Admin | Personal | 5 Jun 2026 | 12 Apr 2011 |
| `archy@cannon-digital.co.uk` | Standard | Business | 17 Jul 2026 | 24 Sept 2025 |

Google flags: *"4 personal or unmanaged email accounts are used to access accounts that you manage."* Four of the five have **passkeys disabled**; only Maria Waters has one enabled. Four of five hold **Admin**. Not urgent, but tighter than it needs to be for an account spending at this level — noted, no action taken.

## F. GTM-KT6M67T — closed off by decision

**Piers's decision, 29 July 2026: stop tracking it.**

Position of record: the container is **not on the live site** (verified across four pages, source and runtime), is **not in the CompanyDebt Tag Manager account**, and is **not visible to any Google account available here**. It cannot be inspected or archived from this side. It is treated as somebody else's container and is out of scope. The Addendum 1 §10 caution ("do not retire it before checking its contents") is moot — nobody here can retire it either way.

No further mention is required in future audit rounds.

## Addendum 2 — net position

| Piers's item | Outcome |
|---|---|
| 1. Get directions + duplicate forms | **No action needed** — already excluded from the goals Google bids on; Get directions has stopped recording |
| 2. Zoho reads zero | **Partly explained, and my first answer was wrong** — the manual-upload history is dead (last Apr 2024, ~99.9% failures) but that screen cannot see the new API integration. The 28 Jul reconnect *did* create its Google-side actions. One day old, no real click ID yet, checkpoint due now. See §B2 |
| 3. Delete dead conversion actions | **Mostly impossible** — "Removed" is already the delete state. ~12 enabled-but-inert actions can be cleaned; cosmetic only |
| 4. Remove ex-agency emails | **DONE** — 3 removed from Tag Manager; verified. They were never in Google Ads |
| 5. Second container GTM-KT6M67T | **Closed** — out of scope, no longer tracked |

Unchanged and still outstanding from Addendum 1: the interaction-gated tag loading (§2), the Custom HTML number-swap duplicate (§5ii), the extra `ad_storage` requirement on the two call tags (§5i), the form conversion trigger design (§4a), and the unmeasured consent acceptance rate.

---
---

# Addendum 3 — cookie consent: acceptance rate, banner, and the click-ID question, 29 July 2026

Follow-on from the main audit's gap #1. Three questions were asked: what share of visitors accept
advertising cookies, what the banner actually looks like, and what the site really does with the
Google click ID when someone declines.

All live inspection in this addendum was read-only (HTTP fetch and browser observation). **No cookie
prompt was accepted, rejected or dismissed.** Nothing was changed on live, staging, Google Ads, Tag
Manager, GA4 or Search Console.

The headline: **the acceptance rate could not be measured with the access available**, and separately,
**it matters less than we assumed**, because the click ID is being captured for everyone regardless of
what they choose. §3 is the important section.

---

## 1. The acceptance rate — NOT MEASURED, and here is exactly why

**VERIFIED — every route was tried and each is genuinely blocked:**

| Route | Result |
|---|---|
| CookieYes dashboard | **No credentials.** The project `.env` was read in full; it holds WP, SFTP, WP Engine, Zoho, LiveChat, Gravity Forms, Gemini, Monday, Companies House, Bing and OpenAI keys. There is **nothing for CookieYes**. No login is available from this side |
| GA4 property G-P39KJ34V6G | **No access.** `get_account_summaries` returns exactly one property for this service account: `properties/328407537`, "www.businessexpert.co.uk GA4". The companydebt.com property is not visible here |
| Google Ads API | **Not connected this session** (`GOOGLE_APPLICATION_CREDENTIALS` unset). Separately, the Ads API does **not** expose an observed-versus-modelled conversion split at all, so even with access it would not yield a rate |
| Search Console | **Works** (`https://www.companydebt.com/`, siteFullUser). But GSC only supplies the cookie-free *denominator*. Without a consented *numerator* from GA4 it cannot produce a ratio |
| Server-side signal on WP Engine | **None exists.** Consent is logged by the browser to `log.cookieyes.com/api/v1/log`, a third party. The site itself stores no record of any consent decision |

The intended method was to divide a consent-dependent traffic count (GA4) by a consent-independent one
(Google Ads clicks, or GSC clicks). Losing GA4 access removes the numerator, and there is no substitute.

**No defensible number can be produced.** A figure quoted here would be a guess wearing a measurement's
clothes, which is worse than no answer.

**What would settle it, in order of speed:**

1. **A CookieYes dashboard login.** CookieYes records every banner interaction and reports accepted /
   rejected / no-action directly. This is a five-minute answer for whoever holds the account. It is the
   only route that gives the true rate rather than an estimate.
2. **GA4 read access to G-P39KJ34V6G** for the existing service account. That enables the
   clicks-versus-sessions estimate. Note this would be a *lower bound* on the acceptance rate, not the
   rate itself, because GA4 also loses visitors to the tag-delay problem in §2 — the two losses are
   confounded and cannot be separated from outside.

**INFERRED, and flagged as such:** the banner is non-blocking and does not appear until the visitor
interacts (§2). Both push the true rate down relative to a blocking banner. That is a direction of
travel, not a number, and it should not be quoted as one.

---

## 2. Banner review — VERIFIED by live inspection

Observed on `https://www.companydebt.com/` and `/contact-us/`, desktop 1280x720 and mobile 375x812.

### 2a. It is delivered through Tag Manager, and that is the biggest problem

**VERIFIED.** The CookieYes script appears nowhere in the served HTML of any page checked (a
case-insensitive search for "cookieyes" returns zero on the homepage and `/contact-us/`). It loads at
runtime from `cdn-cookieyes.com/client_data/75253ed13008cd18bc532356/`, immediately after `gtm.js`.
**CookieYes is deployed inside GTM-5GTD9ZP**, not as a WordPress plugin.

That matters because WP Rocket delays all JavaScript until first interaction (main audit gap #7).
Resource timings from a controlled load of `/contact-us/?gclid=…`:

| Time | What loaded |
|---|---|
| 631 ms | `cdn.livechatinc.com/tracking.js` — LiveChat, **excluded from the delay** |
| 1,192–2,240 ms | LiveChat API calls, chat session opens |
| **10,629 ms** | `gtm.js?id=GTM-5GTD9ZP` — only after interaction |
| 10,776 ms | CookieYes `script.js` |
| 10,832 ms | CookieYes `banner.js` |
| 11,309 ms | Banner images render |

At first paint the page has **zero cookies, no `dataLayer`, no `gtag`, no GTM and no banner in the DOM
at all** (verified directly). The visitor reads the page first and is asked afterwards — if they ever
move the mouse. Anyone who lands, reads and leaves is never asked anything.

**The cookie banner is behind the same delay as the tags it is supposed to govern.** LiveChat has
already been given an exemption from that delay (`cd-livechat-wpr-exclude.php` adds `cdn.livechatinc.com`,
`secure.livechatinc.com` and `livechatinc.com` to WP Rocket's `delay_js_exclusions`). CookieYes has not.

### 2b. Placement — it does not block anything

**VERIFIED.** Container `cky-consent-container cky-box-bottom-left`, `position: fixed`.
Desktop: 440 px box, bottom-left. Mobile: full-width strip at the bottom.

The overlay element carries the class `cky-hide` and computes to `display: none`; `document.body`
computes `overflow: visible`. **The page is fully readable and scrollable without answering.** This is a
bar people scroll past, not a modal.

Consequence, seen in the cookie itself: after loading two pages without touching the banner, the stored
value was

```
consentid:…,consent:no,action:,necessary:yes,functional:no,analytics:no,performance:no,advertisement:no
```

`action:` is **empty** — no decision was made — and everything is already recorded as `no`. Ignoring the
banner produces the same tracking outcome as pressing Reject All.

### 2c. Buttons — Reject is one click, same size as Accept

**VERIFIED, computed styles and geometry.**

Desktop, all on one row, all 44 px tall:

| Button | Size | Fill | Text |
|---|---|---|---|
| Customize | 127 x 44 | transparent, blue outline | blue |
| **Reject All** | 120 x 44 | transparent, blue outline | blue |
| **Accept All** | 123 x 44 | **solid blue `#1863dc`** | white |

Mobile, stacked full width (325 x 44 each), in this top-to-bottom order:
**Accept All → Customize → Reject All.**

On the test that matters for the ICO's stated expectation — that rejecting is **as easy as** accepting —
**Reject All is a single click, at the same size, at the same level, never hidden behind Customize.**
That test is met on both desktop and mobile.

Two softer points, which are style rather than the hard rule:
- Accept is solid-filled while Reject is outline-only, so Accept is visually weightier.
- On mobile Accept is first and Reject is last.

**Not a ruling on lawfulness.** The equal-ease requirement appears to be satisfied; the visual weighting
is the kind of thing the ICO has commented on in guidance. Whoever owns the cookie policy should form
their own view.

### 2d. Copy

**VERIFIED, exact text:**

> We value your privacy
> We use cookies to enhance your browsing experience, serve personalized ads or content, and analyze
> our traffic. By clicking "Accept All", you consent to our use of cookies.

This is CookieYes's stock wording, unedited: American spelling ("personalized", "analyze"), and it
describes what the site wants rather than anything the visitor gets. The preference centre offers five
categories: Necessary, Functional, Analytics, Performance, Advertisement.

### 2e. Page coverage

**VERIFIED.** The CookieYes targeting config (`6KMpOrCv.json`) reads `[{"targetBanner":1945786,
"condition":"all"}]` — all pages, no exclusions. The banner was observed on the homepage and
`/contact-us/`. **No page-type gap was found.** (An earlier apparent gap on an `/insolvency/` URL was my
error — the URL I tried returns 404, so nothing loaded. Recorded here so it is not mistaken for a finding.)

---

## 3. The open compliance question — RESOLVED, and the answer is not what the earlier flag said

This is the section that changes the picture.

### 3a. The browser-side script is correctly gated

**VERIFIED.** The live minified `cd-attribution.js` still gates capture:

```js
function runCapture(){ if (started || !hasConsent()) return; … }
```

Live test: loaded `/?gclid=TESTCONSENTAUDIT2026` and did not touch the banner. Result: **no `cd_*`
cookies were written at all.** The earlier flag — that this script had at times run regardless of consent
— does **not** describe the deployed code today. On this path, it behaves correctly.

**One genuine mismatch remains.** The gate is:

```js
/(?:advertisement|analytics|performance):yes/
```

Any **one** of three categories opens it. A visitor who accepts Analytics but explicitly declines
Advertisement still has their Google click ID stored. The gate is named for advertising but is not
keyed to it.

### 3b. But a bare `gclid` cookie is set for everyone, consent or not

**VERIFIED, twice, on two different pages.** Loaded `/?gclid=TESTCONSENTAUDIT2026` and
`/contact-us/?gclid=TIMINGPROBE7788` without touching the banner. In both cases the consent cookie read
`consent:no, action:, analytics:no, performance:no, advertisement:no` — and a first-party cookie named
**`gclid` held the exact test value**. It **persisted across navigation** to a page with no `gclid` in
the URL.

**Setter identified by elimination on resource timing.** At the moment the cookie was first observed,
`window.google_tag_manager` and `window._googCallTrackingImpl` were both `undefined` and
`cd-attribution.js` had not yet loaded. The only tracker that had run was **LiveChat's
`tracking.js`, loaded at 631 ms** — because LiveChat is deliberately excluded from WP Rocket's JS delay.

So the sequence for a Google Ads visitor is: **LiveChat loads and stores the click ID at well under one
second; the cookie banner does not exist for another ten seconds.**

It is not set by the server — `Set-Cookie` on a cache-busted live request returns only Cloudflare's
`__cf_bm`. It is set in the browser.

### 3c. That cookie reaches the CRM

**VERIFIED** in `cd-livechat-zoho.php` (pulled from staging). In the Gravity Forms handler:

```php
$url   = rgar($entry,'source_url');
$gclid = cd_lc_from_url($url,'gclid');
if ($gclid==='' && isset($_COOKIE['gclid'])) $gclid = $_COOKIE['gclid'];
…
if ($gclid) $fields['Google_Click_ID'] = $gclid;
```

**There is no consent check anywhere in this file.** Three things follow:

1. The click ID is read from the un-gated `gclid` cookie and written to Zoho as `Google_Click_ID`.
2. It is *also* parsed straight out of `source_url`, so a visitor who lands on `/?gclid=…` and submits
   the form on that same page is captured even with no cookie involved at all.
3. `Website_URL` stores the full `source_url`, which carries the click ID in the query string.

The LiveChat chat path (`cd_lc_hook`) does the same from chat custom variables, also with no consent check.

### 3d. The factual position, for whoever owns the cookie policy

**A visitor who has not answered the banner — or who has actively pressed Reject All — still has their
Google click ID stored in a first-party cookie on their device, and still has it written into their
Zoho CRM record if they submit a form or start a live chat.**

That is the fact. **This addendum does not rule on whether it is lawful.** It is a decision for whoever
owns the cookie policy, and it needs one of two outcomes: either the capture is brought behind consent,
or the cookie policy is updated to disclose it. What is not tenable is a banner that says one thing while
the code does another.

Worth noting in fairness: the practical effect today is small, because the Zoho pipeline is delivering
nothing anyway (Addendum 1 §6, Addendum 2 §B2) and 453 of 456 click-ID leads were already outside
Google's 90-day import window. The exposure is procedural, not a live flood of data.

### 3e. Two related findings

**VERIFIED — Consent Mode has no explicit default.** Google's internal consent state shows
`implicit: true` on `ad_storage`, `ad_user_data`, `ad_personalization` and `analytics_storage`. That
means **no `gtag('consent','default',…)` runs before the tags**. The denial arrives afterwards, as an
`update`. Observed `dataLayer` order:

1. `gtm.js` starts
2. **`config AW-977276330/xrGGCKvV68gDEKqbgNID` with `phone_conversion_number`** — the consent-unchecked
   Custom HTML tag added 28 July (Addendum 1 §5ii)
3. `gtm.dom`
4. `gtm.load`
5. `consent update` — everything denied
6. `cookie_consent_update`

**The number-swap tag fires before any consent signal exists.** This is the concrete harm of the missing
default, and it is a second reason to remove that duplicate tag.

**VERIFIED — the cookieless ping carries the click ID.** A request to
`pagead2.googlesyndication.com/ccm/collect` including `&gclid=TIMINGPROBE7788` fires for declining
visitors. This is normal, documented Consent Mode behaviour — no cookie is set and it is what feeds
modelling — but it is recorded here for completeness.

---

## 4. Options, with realistic upside

### 4a. Settle the contradiction in §3 — do this first

No measurement upside; it removes an inconsistency between the stated policy and the code. Either:

- **Gate the capture:** hold LiveChat's tracker until consent (the same exclusion mechanism already
  exists, in reverse), and add a consent check to `cd-livechat-zoho.php` before `Google_Click_ID` and
  before storing `source_url` with its query string; or
- **Disclose it:** update the cookie policy to state that a click identifier is stored.

**This is the policy owner's call, not a technical default.** Flagging only — no change made.

### 4b. Let people actually see the banner — the biggest banner lever

Not copy, not colour: **the banner does not exist until the visitor interacts**, because it sits inside
GTM behind WP Rocket's delay (§2a). Taking CookieYes out of the delay — exactly the exemption LiveChat
already has — would let visitors answer at all. **INFERRED:** this should move the acceptance rate more
than any wording change, because the current rate includes everyone who was never asked. It also fixes
the §3e ordering problem, since consent would be established before the tags fire.

Trade-off, stated honestly: it makes the banner appear earlier and more visibly, which is a slight
first-impression cost on a site where visitors arrive stressed.

### 4c. Banner copy and layout — modest

Replace CookieYes's stock American text with something specific and British; on mobile, move Reject out
of last place. Keep Reject as one click, which it already is. Real but small.

### 4d. Ask people directly — best value for the effort

**VERIFIED: no form has a "how did you hear about us?" field.** Checked live via the Gravity Forms API:

| Form | Fields |
|---|---|
| 40 Quick Quote | Name, Email, Phone, Amount Bank, Amount HMRC, Amount Creditors, Amount Assets, CAPTCHA |
| 41 Contact Us | Name, Email, Telephone, Comments, HTML Block, CAPTCHA |
| 44 Home Page - Contact Block | Name, Email, Telephone, CAPTCHA |
| 29 Contact Us - Advisors | Name, Email, Phone, Message, HTML Block, CAPTCHA |

At roughly two enquiries a day this is entirely viable, and it is **completely unaffected by cookies,
consent, ad blockers or browser privacy changes**. It will not reconcile to Google click IDs, so it
cannot feed offline conversion imports — but it answers the business question ("where do our clients
come from") which the click ID only ever answered indirectly.

**Blocker to fix first — VERIFIED:** `check_live_form_entries.py` shows only **form 44** receiving new
entries (newest 29 Jul 2026). Forms 29, 40 and 41 have newest entries of 13 Mar, 23 Mar and 16 Mar 2026.
Adding a field to a form that is not storing submissions achieves nothing. **This needs its own
investigation** and is out of scope here.

### 4e. Server-side call tracking — the largest measurable upside

Phone is the business: **124 of 272 conversions (46%) are calls placed straight from the ad** (Addendum 1
§6). Website call tracking is effectively dead at **4 conversions in 90 days**, because Google's number
swapping needs `ad_storage` granted and the two call tags additionally carry a manual `ad_storage`
requirement (Addendum 1 §5i).

A dedicated call-tracking provider swaps the number **server-side, at page render**, and reports the call
back from its own switchboard. It does not depend on the visitor's browser, cookies, or Google's consent
state. The account's **removed "Infinity Calls" conversion action** indicates Infinity was used here
before, so this is a return to something that already worked rather than a new experiment.

**Stated honestly:** this is not a consent loophole. It still involves assigning and storing an identifier
against a visitor, and it carries its own privacy position that has to be settled the same way §3 does.
What it does is make the measurement work *independently of the Google tag*, which is a different and
more durable thing.

### 4f. What will not work — say this plainly

- **There is no lawful technical trick to track people who declined.** Anything that captures them
  anyway is the §3 problem with extra steps.
- **Consent Mode modelling does not help the CRM loop.** It is already on and working (Addendum 1 §7).
  It estimates conversions Google could not observe. It **never returns a click ID**, so it can never
  feed an offline conversion import back from Zoho.
- **Google tag gateway does not change any of this.** It changes where the tag is *served from*
  (a first-party endpoint instead of Google's domain). It does not change whether consent was given, and
  it does not recover declining visitors.

---

## Addendum 3 — net position

| Question | Answer |
|---|---|
| What is the acceptance rate? | **Unmeasured, and not measurable from here.** No CookieYes credentials exist in `.env`; GA4 access covers only businessexpert.co.uk. Needs a CookieYes dashboard login (direct answer) or GA4 access to G-P39KJ34V6G (estimate only) |
| Is Reject as easy as Accept? | **Yes** — one click, same size, same row, never hidden behind Customize. Accept is solid-filled and sits first on mobile; styling weighting only |
| Does the banner block the page? | **No.** Bottom-left box, overlay disabled, page fully scrollable. Ignoring it records the same as Reject All |
| Does the banner always appear? | Targets all pages — but **does not exist until the visitor interacts**, because CookieYes sits inside GTM behind WP Rocket's JS delay |
| Is the click ID captured from people who declined? | **Yes.** Not by `cd-attribution.js`, which is correctly gated, but by an un-gated first-party `gclid` cookie set by LiveChat at 631 ms, which `cd-livechat-zoho.php` then writes to Zoho with no consent check |
| Is that lawful? | **Not ruled on here.** Facts are laid out in §3d for the cookie-policy owner to decide |
| Biggest realistic upside | **Server-side call tracking** (§4e) — phone is 46% of conversions and website call tracking reads 4 in 90 days |
| Best value for effort | **A "how did you hear about us?" field** (§4d) — but only after fixing why forms 29/40/41 stopped storing entries |

Nothing in this addendum was changed. No live, staging, Ads, GTM, GA4 or Search Console setting was
modified, and no cookie prompt was answered.

---
---

# Addendum 4 — consent platform: stay on CookieYes or move to a free plugin? 29 July 2026

Prompted by Piers: the CookieYes account appears to be on the free tier, so is there any reason not to
switch to a free plugin?

Read-only throughout. Nothing installed, activated, deactivated or changed.

---

## A. CORRECTION to Addendum 3 §2a — the plugin *is* installed and active

Addendum 3 §2a said CookieYes was "deployed inside GTM-5GTD9ZP, **not as a WordPress plugin**". The
second half of that is **wrong** and is corrected here.

**VERIFIED, live plugin list read via the WordPress REST API (read-only):**

```
active   CookieYes | GDPR Cookie Consent  v3.4.2   [cookie-law-info/cookie-law-info]
active   WP Rocket                        v3.21.2
active   Gravity Forms                    v2.6.4
```

The plugin is present and **active**. What was right is the operative half: **the banner is not being
delivered by the plugin.** It is delivered by the CookieYes tag template inside GTM.

**VERIFIED by reading the public container** (`https://www.googletagmanager.com/gtm.js?id=GTM-5GTD9ZP`):
the container contains the CookieYes website key `75253ed13008cd18bc532356` and code that builds
`https://cdn-cookieyes.com/client_data/<websiteKey>/script.js` and calls `inject_script`. It also
contains the category-to-signal mapping (`"advertisement"` → `ad_personalization` and so on) — **the
Consent Mode v2 signals are emitted by the GTM template**, not by the plugin.

Correspondingly, the served HTML contains **no** reference to `cookieyes`, `cdn-cookieyes`,
`client_data`, the website key, `cookielawinfo` or `cookie-law-info` (all counts zero on a cache-busted
fetch of the homepage). The plugin is active but silent on the front end.

**Minor correction while here:** Addendum 3's early note of `cky-nav` / `cky-sidebar` strings in the HTML
was a false positive — those are substrings of `sticky-nav` and `is-position-sticky`. There is no
CookieYes markup in the served HTML. This does not change any conclusion.

**So the current state is a split installation:** an active plugin that renders nothing, and a GTM tag
that renders everything, both pointed at the same CookieYes account. That is worth tidying regardless of
which platform is chosen.

---

## B. What the free CookieYes tier actually includes

**VERIFIED from CookieYes's own pricing page, 29 July 2026:**

Free plan **includes**: 5,000 pageviews/month; 100 pages per scan; basic customisation; cookie
auto-blocking; granular cookie control; consent expiry and renewal; **"Consent log"**; **"Consent trends
& pageviews"**; Google Certified CMP; privacy and cookie policy generators.

Free plan **excludes**: **Google Consent Mode v2**; custom colours; multilingual banner; popup layout;
geo-targeting; staging site; scheduled scanning; multi-user access; chat support.

Two consequences, and they pull in opposite directions.

### B1. Good news for the unanswered question in Addendum 3 §1

**"Consent log" and "Consent trends & pageviews" are included on the free tier.** The acceptance rate
Piers asked for should therefore be readable from the CookieYes dashboard **without paying anything** —
it only needs the login. That strengthens Addendum 3 §1's first recommendation.

### B2. The trap — Consent Mode v2 is a paid feature, and it is currently working

Consent Mode v2 is **demonstrably live** on the site (Addendum 3 §3e verified the six-signal `consent`
update firing, and Addendum 1 §7 confirmed Google reports modelling as active). Yet CookieYes lists
Consent Mode v2 as **excluded from the free plan**.

**INFERRED, and it matters:** the signals are coming from the **GTM template**, which emits them
regardless of plan tier. That is very likely *why* someone put CookieYes into GTM in the first place —
whether deliberately or by accident, the GTM route is delivering a paid-tier behaviour on a free account.

**The practical warning: moving the banner from GTM to the plugin could silently switch off Consent Mode
v2**, unless the account is upgraded or the replacement tool emits the signals itself. That would be a
real regression — Google Ads would lose the cookieless pings that currently feed conversion modelling.
This is exactly the kind of change that returns HTTP 200 and looks fine while quietly costing data, so it
must be verified in the browser after any switch, not assumed.

### B3. The pageview cap is close

**VERIFIED via Search Console:** 663 organic clicks in the 28 days to 22 July 2026 (~24/day). Add roughly
22 UK ad clicks/day plus direct, brand and referral traffic, and the site is plausibly in the region of
**3,000–6,000 pageviews a month** — i.e. **around or just over the free plan's 5,000 cap**.

**Not verified**, because it needs the dashboard: which plan the account is actually on, and whether the
cap is being hit. If it is being exceeded, banner or logging behaviour may already be degrading. Worth
checking at the same time as the acceptance rate.

---

## C. Is there a reason to stay on CookieYes?

**No strong one, and no cost argument either way** — the account is already free, so switching saves
nothing. The honest position:

| Consideration | Assessment |
|---|---|
| Cost | **Neutral.** Already on a free tier. A move saves £0 |
| The acceptance-rate number | **Slight reason to stay, short term.** The consent log already exists on this account. Switching resets that history |
| Consent Mode v2 | **Reason for caution.** Currently supplied by the GTM template on a free account. Any replacement must be confirmed to emit all six signals, in the browser, before the old one is removed |
| The actual problem (§2a, §4b) | **Vendor-neutral.** The banner being invisible until interaction is caused by *delivery through GTM behind WP Rocket's delay*, not by CookieYes. Changing vendor does not fix it. Changing delivery does |
| Tidiness | **Reason to change something.** An active plugin that renders nothing alongside a GTM tag that renders everything is a confusing setup for whoever inherits it |

**INFERRED recommendation:** the vendor is not the problem, so do not lead with a vendor swap. In order:

1. **Read the consent log first** (free, no change, answers Addendum 3 §1 and confirms the plan and cap).
2. **Then fix delivery** — one tool, loading early, not behind the JS delay. If the existing plugin can
   render the banner *and* keep Consent Mode v2, that is the smallest change available, since it is
   already installed and active.
3. **Only then consider a different plugin**, if step 2 turns out to need a paid CookieYes tier. Several
   free plugins advertise Consent Mode v2 without an upgrade; **none of those claims were verified here**
   — they come from vendor and affiliate pages, which are not a sound basis for a compliance decision.
   Any candidate must be tested on staging and the six consent signals confirmed in the browser before it
   goes near live.

**Do not swap vendor and change delivery in the same step.** If measurement breaks, there would be no way
to tell which change caused it.

**Not a recommendation on legal sufficiency.** Whether any given tool meets the site's obligations is for
whoever owns the cookie policy, as in Addendum 3 §3d.

---
---

# Addendum 5 — the 29 July consent incident, and the fix built on staging

Same day as Addenda 3 and 4. This records a live incident that happened *during* the audit, a
correction to Addendum 3, and the remediation now sitting on staging awaiting a live deploy.

---

## A. CORRECTION to Addendum 3 §3b — the `gclid` cookie setter was misidentified

Addendum 3 §3b attributed the un-gated `gclid` cookie to **LiveChat's `tracking.js`**, reasoning by
elimination from resource timings. **That was wrong.**

**VERIFIED:** the setter is CompanyDebt's own code — an inline script printed into `wp_head` at
priority 1 by `cd-livechat-zoho.php`, which was stored base64-encoded in the source. Decoded, it read:

```js
var p = new URLSearchParams(location.search), K = ['gclid','gbraid','wbraid'];
K.forEach(function (k) { var v = p.get(k);
  if (v) document.cookie = k + '=' + encodeURIComponent(v) + ';path=/;max-age=' + (90*86400); });
```

No consent check of any kind. It also pushed those values, plus `landing_page` (which carries the click
id in its query string), into LiveChat as session variables.

The conclusion in §3d is unchanged and if anything firmer: click ids were being stored and forwarded to
the CRM for visitors who had not consented. Only the mechanism was misattributed. The practical
difference is favourable — it is our own code, so it was directly fixable.

Lesson worth keeping: elimination-by-timing is not proof of authorship. The base64 encoding hid the real
setter from every text search performed in §3.

---

## B. INCIDENT — 29 July 2026: consent gate removed for roughly one hour

**Sequence, all VERIFIED:**

1. The CookieYes WordPress plugin (`cookie-law-info` v3.4.2, active but previously unlinked) was linked
   to the CookieYes account. It immediately began injecting its own banner script into the page HTML,
   using website key `387f1b54…`.
2. The site was now running **two different CookieYes properties**: the plugin's `387f1b54…` in the HTML,
   and the pre-existing GTM tag's `75253ed1…`. They overwrote each other's `cookieyes-consent` cookie.
   Observed result: cookie written with **every value blank**
   (`consent:, necessary:, analytics:, advertisement:`), **no banner rendered at all**, and **zero
   consent events reaching Google**.
3. The GTM tag `CookieYes Consent Manager` (type: CookieYes CMP, trigger: Consent Initialization – All
   Pages) was **paused and published** to leave the plugin as the single source.
4. That removed the only thing setting Consent Mode **defaults**. The free CookieYes tier sends the
   `update` but not the `default`. With no default, Google's tags initialised unrestricted.

**Measured state after step 4**, on a clean browser profile with nothing clicked:

```
_gcl_aw = GCL.1785334251.FRESH88213     <- Google Ads click cookie, holding the test click id
_gcl_au = 1.1.1613826582.1785334250
_ga     = GA1.1.857543448.1785334251
_ga_P39KJ34V6G = GS2.1.s1785334250...
cookieyes-consent = ...advertisement:no
```

The banner correctly recorded a refusal **and Google's cookies were written anyway**, because the
refusal arrived after the tags had already initialised (`google_tag_data.ics` showed `update: false`).

**This was worse than the pre-incident state**, where the GTM tag's Consent Initialization trigger put a
denial in place before any tag ran and no `_ga`/`_gcl_*` cookies appeared.

**INFERRED (unresolved):** how many visitors were affected. Traffic is roughly 50–60 visits/day, the
window was about an hour in UK afternoon, so the order of magnitude is a few dozen. Cloudflare was also
serving hour-old cached HTML during the window, so some visitors got older markup. No precise figure is
available and none should be invented.

---

## C. Expert review of the proposed fix

The remediation was stress-tested against a six-perspective panel before implementation. The
substantive changes it forced, all incorporated:

| Challenge | Change made |
|---|---|
| WP Rocket delays inline scripts and would silently void the fix | Snippet excluded from delay via `rocket_delay_js_exclusions` **and** `rocket_excluded_inline_js_content`; verified un-delayed in rendered HTML |
| `ads_data_redaction` would degrade modelling | Explicitly set to `false`, with the reasoning recorded in-file |
| Click id must survive page-to-page without storage | `url_passthrough: true` |
| Existing 90-day cookies do not expire because the setter was fixed | Active deletion of `gclid`/`gbraid`/`wbraid` on any load without advertising consent |
| Click ids reach Zoho via `source_url` even when the cookie is withheld | `cd_lc_strip_click_ids()` applied to the stored `Website_URL` |
| The chat webhook cannot read visitor cookies | Explicit `ad_consent` session variable, set only on consent; URL fallback skipped without it |
| Consent Mode governs Google only, not the wider storage surface | Acknowledged, not solved — see §F |

---

## D. What was changed on staging

**Three files. Backups taken on the server for the two that existed.**

**1. `wp-content/themes/company-debt-webpigment/header.php`**
(backup: `header.php.bak-a11y-consent-default-20260729`)

Consent Mode v2 defaults inserted immediately above the GTM snippet. **This placement is not
negotiable**: GTM is hardcoded in `header.php` and printed *before* `wp_head()`, so no WordPress hook
can precede it. Snippet held in the repo at `theme-snippets/consent-mode-defaults.header.html`.

All six signals denied, `security_storage` granted, `wait_for_update: 500`, `url_passthrough: true`,
`ads_data_redaction: false`.

**2. `wp-content/mu-plugins/cd-consent-mode-defaults.php`** (new)

Sole job: keep the snippet out of WP Rocket's delayed-JS handling. This is the single highest-risk
failure mode — a delayed consent default is not a consent default, and it fails silently.

**3. `wp-content/mu-plugins/cd-livechat-zoho.php`**
(backup: `cd-livechat-zoho.php.bak-a11y-consent-gate-20260729`)

- Base64 inline script replaced with readable, consent-gated JavaScript.
- Nothing stored or forwarded unless `advertisement:yes`; stale click-id cookies deleted when it is not.
- Re-runs on `cookieyes_consent_update`, so accepting on the landing page still captures.
- New `cd_lc_ad_consent()` and `cd_lc_strip_click_ids()` helpers.
- Gravity Forms handler: both the cookie route and the `source_url` route gated; click ids stripped from
  the stored URL when consent is absent.
- Chat webhook: gated on the explicit `ad_consent` session variable.

**Accepted trade-off, recorded deliberately:** a visitor who accepts only after navigating away from the
landing page loses the click id, because it is no longer in the URL. Stashing it pre-consent "just in
case" would be the same problem in a different container.

---

## E. Verification on staging — VERIFIED, clean browser profile

| Check | Result |
|---|---|
| PHP renders without error | 257,562 bytes, no parse/fatal error |
| JavaScript syntax (both blocks) | `node --check` passes |
| Order in page | consent default (char 17,936) → **GTM (19,345)** → cd-lc inline (19,556) |
| Snippet delayed by WP Rocket? | **No** — renders as `<script data-cd-consent-default="1">`, no `type` attribute |
| Default reaches the dataLayer | **Position 0**, ahead of `gtm.start` |
| Google's registered state after GTM loads | `ad_storage`, `ad_user_data`, `ad_personalization`, `analytics_storage` all `default=false`; `security_storage` `default=true` |
| Cookies before consent, with `?gclid=` | **None.** No `_ga`, no `_ga_*`, no `_gcl_au`, no `_gcl_aw`, no `gclid` |
| Modelling input preserved | **Yes** — `pagead2.googlesyndication.com/ccm/collect?…&gclid=…` and `region1.google-analytics.com/g/collect` both still fire |
| Stale click-id cleanup | Seeded `gclid`+`gbraid` 90-day cookies; both **deleted** on next no-consent load |
| Consent-granted path | With `advertisement:yes`: `gclid` cookie stored, LiveChat receives `gclid`, `landing_page`, `ad_consent=yes` |

**What staging could NOT prove, and why.** CookieYes website keys are domain-bound and the staging
install is not linked to the account, so no banner loads there. The granted path was therefore tested by
seeding a `cookieyes-consent` cookie by hand, which exercises our code but **not** CookieYes's own
`update` call. The one thing still unproven is that CookieYes's update correctly flips the defaults to
granted on live. That must be checked in the browser immediately after the live deploy — if it fails,
consenting visitors would be tracked as if they had refused, and conversions would fall.

---

## F. Still open after this fix

- **Live deploy.** Everything above is on staging only. It does nothing until it reaches live, and the
  live exposure in §B continues until then.
- **Post-deploy verification is mandatory**, not optional: confirm the un-delayed snippet in view-source,
  confirm no `_ga`/`_gcl_*` before consent, confirm the update flips on accept, then purge WP Rocket
  **and** Cloudflare and re-check.
- **Baseline conversions before deploying.** Conversions will fall. That fall is mostly correction, not
  breakage, but without a baseline the two are indistinguishable.
- **Non-Google storage is untouched.** LiveChat still loads at ~631 ms, before any consent exists,
  deliberately excluded from the JS delay. Consent Mode does not govern it. Unresolved.
- **`cd-attribution.js` still gates on "any of three categories"** (`advertisement|analytics|performance`),
  so accepting analytics alone still opens click-id capture there. The new code is keyed to
  `advertisement` specifically. The theme script should be brought into line.
- **The CookieYes cookie scan has never run**, so the declared cookie inventory is empty against at least
  six in evidence. The banner cannot describe what it does not know about.
- **The paused GTM tag** remains paused, not deleted, and is restorable in one click if needed.
