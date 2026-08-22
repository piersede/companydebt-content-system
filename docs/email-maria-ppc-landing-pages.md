# Draft email: Maria Waters — new PPC landing pages

To: mariawppc@gmail.com
Subject: New landing pages for the paid campaigns

---

Hi Maria,

We've built four dedicated landing pages for the paid campaigns, one per
intent. All four are live:

- Liquidation / CVL — https://www.companydebt.com/ppc-liquidate-company/
- Company debt — https://www.companydebt.com/ppc-company-debt/
- HMRC arrears — https://www.companydebt.com/ppc-hmrc-debt/
- Winding-up petition — https://www.companydebt.com/ppc-winding-up-petition/

I hadn't appreciated until we started measuring properly that every ad group
was landing on the same general guides, so there was no way to see which intent
was actually converting. We simply hadn't built the pages, so you were sending
traffic to the only thing there was.

Four things worth knowing before you move anything:

**They are set to no-index.** Paid traffic only. They won't show up in organic
results and won't compete with the guides.

**Each carries its own enquiry form**, separate from the site's general contact
forms, so paid leads can now be counted on their own. The form pre-selects the
visitor's situation from whichever page they arrive on, so there's one less
question to answer.

**Conversion tracking is already in place** — Tag Manager container version 88,
published. Both the Google Ads conversion and the GA4 event fire on the new
form. Nothing needed at your end.

**Leads reach the CRM tagged "PPC - CD"**, carrying the ad intent and the
enquirer's own description of their situation. That means we can follow paid
enquiries through to instructions won, rather than stopping at form fills.

Two things that will mislead you when you read the numbers:

- Google Ads credits a conversion to the landing page of the ad click, not the
  page where the form was submitted. A report filtered to these URLs can look
  empty even while they're working.
- Gravity Forms timestamps are UTC, Google Ads reports in London time, so an
  entry and its conversion can appear an hour apart.

Let me know how you'd like to play it: all four ad groups moved across at once,
or start with one and compare against the current pages before committing. If
you'd rather run them side by side for a fortnight first, that works too.
Whichever you prefer, tell me and I'll leave things alone until you've set it
up.

Piers

---

## Notes for Piers, not part of the email

**Voice moves applied**, per `feedback_email_drafting_in_piers_voice`:
- own gap named first ("I hadn't appreciated until we started measuring")
- Maria judged charitably in one clause ("you were sending traffic to the only
  thing there was"), not a paragraph
- decision handed back with the options priced, rather than an instruction

No soft preamble, because she is a supplier rather than a director.

**Deliberately left out.** `docs/measurement-go-live-checklist.md` line 118 has
other account-side items queued for "Maria's email": setting the Zoho
lead-creation action to secondary, removing the extra consent requirement on
the two call tags, leaving enhanced conversions off until forms hardening is
live, and the phone-lead drop. None of them are about the landing pages, and
mixing four unrelated asks into one email tends to get the first one done and
the rest lost. Worth a second email, or a call.

**One claim to check before sending.** "Nothing needed at your end" for
conversion tracking is true of the tracking itself, but she may still want to
confirm the conversion action shows data once traffic starts. Soften if you'd
rather not sound like it's fully hands-off.
