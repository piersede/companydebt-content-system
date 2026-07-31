# Logging phone enquiries in Zoho

## Why this matters

Company Debt takes roughly **100 phone calls a month** from Google Ads, and about **27 of those
are real conversations** lasting over two minutes. Zoho currently contains **3 phone leads in its
entire history**.

The phone is the single largest enquiry channel and it is almost completely unrecorded. Because of
that, nobody can answer the question that decides where the ad budget goes: *do the people who
ring us become clients?*

Google already knows which ad produced each call. What it cannot know is what happened next.
Only the person who answered the phone knows that, and right now they aren't writing it down.

## Which calls to log

**Genuine enquiries only.** Do not log everything that rings.

**Log it** when someone is asking about their company's debts, insolvency, HMRC arrears, a
winding-up petition or similar, and they are not already a client.

**Do not log** wrong numbers, recruiters, sales and marketing calls, or existing clients ringing
about a case already in progress. If a call lasts eleven seconds and they hang up, there is nothing
to record.

If you genuinely can't tell, log it. A slightly imperfect record costs little; a missed client costs
a lot.

Two reasons this matters, beyond keeping the CRM clean:

- **Nothing is gained by logging junk.** Only positive outcomes ever get sent back to Google.
  Poor calls teach the bidding by their absence, not by being recorded. And Google already counts
  total call volume for us, so the "how many were any good" ratio works without junk records.
- **Storing a stranger's phone number needs a lawful basis.** Somebody ringing about their
  company's debts gives us one. A recruiter or a misdial does not.

## The ask, in full

When you take a genuine enquiry call, create a Lead in Zoho with these four things:

| Field | What to put | Why |
|---|---|---|
| **Mobile** | The caller's phone number | **The critical one.** This is what links the call back to the ad that produced it. |
| **Last Name** (and First Name) | Their name | Zoho requires a surname |
| **Lead Source** | `Phone - CD` | Marks it as a phone enquiry. Pick it from the list, don't type it. |
| **Description** | A line or two on what they wanted | So the next person has context |

Everything else is optional. **If you only have thirty seconds, the number and the source are the
two that matter.**

Log it the same day. Zoho stamps the time it was created, and that timestamp is used to match the
record against Google's record of the call. A few hours' delay is fine; a week is not.

## What good looks like

There is a worked example in Zoho right now, lead ID `1974818000085606008`, named
"EXAMPLE PHONE LOG - safe to delete". It looks like this:

```
First Name        Template
Last Name         EXAMPLE PHONE LOG - safe to delete
Mobile            07700900999
Lead Source       Phone - CD
Insolvent Company Example Trading Ltd
Lead Status       Contacted
Description       Call received: 2026-07-28 16:27
                  Caller said: struggling to pay HMRC VAT, ~£40k,
                  personal guarantee on lease.
                  Next step: call back Thursday.
```

Delete it once the team has seen it.

## Then keep the status up to date

The Lead Status field is what eventually tells Google whether the call was worth anything. As the
enquiry progresses, move it along (`Contacted` -> `Pre Qualified` -> and so on).

Use `Junk Lead` for enquiries that were logged in good faith and then went nowhere: the company
turned out to be solvent, they were shopping for free advice, they never called back. That is
different from a spam call, which should never have been logged at all.

Keeping the status honest is what makes the whole thing work. At present Google believes every
60-second call is a success, and it will keep buying more of them until told otherwise.

## Withheld numbers

If the caller withholds their number, log the lead anyway. It still counts as a phone enquiry for
our own reporting. It just can't be matched back to an ad.

## Notes for whoever administers Zoho

The API token in this project has **Leads scope only**, so custom fields, layouts and required-field
rules cannot be set programmatically. Two changes worth making by hand in the Zoho admin UI:

1. A **Quick Create layout** for Leads exposing just Name, Mobile, Lead Source and Description, so
   logging a call takes seconds rather than scrolling a 125-field form.
2. A **saved view** filtered to `Lead Source = Phone - CD`, so call volume is visible at a glance
   and the habit is easy to audit.

Neither is required to start. The habit matters more than the tooling.

## How this feeds back to Google

Once calls are being logged, an outcome can be uploaded to Google Ads keyed on the **caller's
number plus the call time**, which is why the Mobile field is non-negotiable. Google matches it
internally against the call it already recorded, and the ad that produced it finally gets credit
for a real client rather than a 60-second ring.

That upload needs a conversion action of type **Import calls**, which does not exist in the account
yet. All seven current upload actions are the click-ID kind and will not accept call data. See
`runs/2026-07-24-company-debt/findings-v2/connection-3-status.md`.
