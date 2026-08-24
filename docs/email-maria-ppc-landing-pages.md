# Draft email: Maria Hilton (Online PPC by Maria Ltd) — new PPC landing pages

To: mariawppc@gmail.com
Subject: New landing pages, and where I'd put the budget first

---

Hi Maria,

We've built four dedicated landing pages for the paid campaigns, one per intent.
All four are live:

- Liquidation / CVL — https://www.companydebt.com/ppc-liquidate-company/
- Company debt — https://www.companydebt.com/ppc-company-debt/
- HMRC arrears — https://www.companydebt.com/ppc-hmrc-debt/
- Winding-up petition — https://www.companydebt.com/ppc-winding-up-petition/

I hadn't appreciated until we started measuring properly that every ad group was
landing on the same general guides, so there was no way to see which intent was
actually converting. We simply hadn't built the pages, so you were sending
traffic to the only thing there was.

**Where I'd start: liquidation. Which means turning it back on first.**

Tony wants us focused tightly around liquidation. When we last went through the
account, though, almost all the liquidation keywords were paused, so there's
very little running on the intent he cares most about.

I assume they were paused for a fair reason, which is that they weren't paying
their way. What I'd add is that until last week they were pointing at a general
guide with no dedicated form on it. A good part of that result was ours, not the
keywords'. That's the bit we've now fixed.

So the ask is: reopen the liquidation keywords, point them at the new page, and
let that cluster run properly for a few weeks before we judge it again. If
there's a cost-per-lead history there that I'm not seeing, say so and we'll
leave them where they are.

I'd rather do that than move all four ad groups across at once and spread the
clicks thin. The other three pages are built and waiting, so we can bring them
in as soon as there's a reason to.

**On dynamic keyword variants: not yet, and I'd hold off on keyword insertion in
the ad copy too.**

Two reasons. The first is simply that we have no baseline. The pages have been
live a matter of days and there isn't a week of data on any of them, so any
variant test would be reading noise.

The second matters more. These pages carry named insolvency practitioners and
their licence numbers, and people search things like "close company to avoid
paying HMRC". I don't want a searcher's own wording appearing in our headline or
our ad. That's a compliance problem rather than a performance one, and it's not
worth the upside.

If the liquidation cluster earns it, the right next step is another page rather
than dynamic text. The pages are built so that adding one is quick.

Four things worth knowing before you move anything:

**They are set to no-index.** Paid traffic only. They won't show up in organic
results and won't compete with the guides.

**Each carries its own enquiry form**, separate from the site's general contact
forms, so paid leads can now be counted on their own. The form pre-selects the
visitor's situation from whichever page they arrive on, so there's one less
question to answer.

**Conversion tracking is in place** — Tag Manager container version 88,
published. Both the Google Ads conversion and the GA4 event fire on the new form.
I'm doing a final check in Tag Manager preview this week, but there's nothing
needed at your end.

**Leads reach the CRM tagged "PPC - CD"**, carrying the ad intent and the
enquirer's own description of their situation. That means we can follow paid
enquiries through to instructions won, rather than stopping at form fills.

Two things that will mislead you when you read the numbers:

- Google Ads credits a conversion to the landing page of the ad click, not the
  page where the form was submitted. A report filtered to these URLs can look
  empty even while they're working. The hidden field on the form is the real
  record of which intent produced each lead.
- Gravity Forms timestamps are UTC, Google Ads reports in London time, so an
  entry and its conversion can appear an hour apart.

So: liquidation first, the other three held ready, and no keyword insertion for
now. If you'd rather run liquidation side by side with the current page for a
fortnight before committing, that works too. Tell me which and I'll leave things
alone until you've set it up.

Piers

---

## Notes for Piers, not part of the email

**Her name.** The previous draft of this said "Maria Waters". She is Maria
Hilton, Director of Online PPC by Maria Ltd. Corrected.

**The paused keywords are stated but not sourced either.** I could not find the
analysis in the repo, so the email says "almost all the liquidation keywords were
paused" without numbers or a date. If you have the figures to hand, they'd
sharpen it: how many, and how long they've been off. Don't let me guess at them.

**Tony's steer is stated but not sourced.** I could not find the correspondence
where he asked for the liquidation focus — I searched both mailboxes for Tony
against liquidation, ad groups and campaign terms, and the repo, and found
nothing. The email asserts it as your instruction. If Tony said something more
specific, or meant something narrower than "lead with liquidation", change that
paragraph before sending.

**One claim to check before sending.** "Conversion tracking is in place" is true
of the wiring, but the two tags have not yet been watched firing in Tag Manager
preview. I've written it as a check you're doing this week rather than as done,
which is honest without inviting her to wait. If you'd rather not mention it at
all, cut that clause.

**Voice moves applied**, per `feedback_email_drafting_in_piers_voice`:
- own gap named first ("I hadn't appreciated until we started measuring")
- Maria judged charitably in one clause ("you were sending traffic to the only
  thing there was"), not a paragraph
- decision handed back with the options priced, rather than an instruction

No soft preamble, because she is a supplier rather than a director.

**Deliberately left out.** `docs/measurement-go-live-checklist.md` line 118 has
other account-side items queued for "Maria's email": setting the Zoho
lead-creation action to secondary, removing the extra consent requirement on the
two call tags, leaving enhanced conversions off until forms hardening is live,
and the phone-lead drop. None of them are about the landing pages, and mixing
four unrelated asks into one email tends to get the first one done and the rest
lost. Worth a second email, or a call.
