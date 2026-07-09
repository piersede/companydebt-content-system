# Rework Brief: Can't Pay VAT (WP 9443, /hmrc/cant-pay-vat/)

Cycle: 2026-07 restructure. Page-class: trigger. Passthrough HTML draft.
Supersedes the June 2026 structure now live. Voice, humanising and gate rules unchanged.

## Intent
- Primary query: can't pay VAT
- Secondary: cannot pay VAT, VAT Time to Pay, HMRC VAT payment plan, VAT late payment penalties, unpaid VAT insolvency, VAT debt company director
- Audience: UK company directors who have missed, or expect to miss, a VAT payment.
- Answer the urgent practical question first, then HMRC payment options, penalties, enforcement risk, insolvency risk, director risk, next-step options.

## Final H-tag structure (build exactly)
- H1 Can't Pay VAT? What Happens and What Directors Should Do
  - byline + "Reviewed by [named IP]" + "Last updated [Month Year]" line under H1
- H2 Can't Pay VAT? Quick Answer
- H2 What to Do First If You Cannot Pay VAT
- H2 Can You Get a VAT Time to Pay Arrangement?
  - H3 Online VAT Payment Plan Eligibility
  - H3 What HMRC Will Ask For
  - H3 What Happens If Time to Pay Is Refused
- H2 VAT Penalties and Interest If You Pay Late
  - H3 Up to 15 Days Late
  - H3 16 to 30 Days Late
  - H3 31 Days or More Late
- H2 What Happens If You Still Do Not Pay VAT?
- H2 Can Unpaid VAT Lead to Insolvency?
- H2 Director Risks When VAT Is Unpaid
- H2 Options If the Company Still Cannot Pay VAT
- H2 Frequently Asked Questions
- H2 Related Guides

Counts: 1 H1, 12 H2, 6 H3. H3s only under Time to Pay and Penalties.

## Modules (NOT H3s)
1. Quick Answer: answer box (callout), 6 lines, snippet-targeted.
2. What to Do First: numbered checklist, bold lead-in per item, 6 items.
3. Penalties: table [How late the VAT is | Penalty position | Interest position | What the director should do].
4. What Happens If You Still Do Not Pay: enforcement timeline table [Stage | What it means | Director action | Risk level]; rows = payment missed, HMRC reminder/demand, debt management contact, payment-plan discussion, enforcement/recovery, statutory demand, winding-up petition. No H3s.
5. Can Unpaid VAT Lead to Insolvency: warning-signs box "Signs VAT debt may now be an insolvency issue", 5 bullets.
6. Director Risks: 6 warning cards, bold headings, one line each. No H3s.
7. Options: comparison table [Option | When it fits | Main risk | Next step]; rows = Renegotiate Time to Pay, Short-Term VAT Funding, CVA, CVL, Administration. Plus decision box (viable vs not viable). No H3s.
8. FAQs: accordion + FAQ schema, 8 Qs. Not H3 unless CMS forces it.
9. Related Guides: internal-link block, 7 links. No H3s.

## Verified facts (GOV.UK, checked 2026-07-07)
Sources:
- how-late-payment-penalties-work-if-you-pay-vat-late (gov.uk/guidance)
- late-payment-interest-if-you-do-not-pay-vat-or-penalties-on-time (gov.uk/guidance)
- VAT payment plan service (tax.service.gov.uk/set-up-a-payment-plan/vat-payment-plan)

- Days 1-15 late: NO first or second late payment penalty.
- Days 16-30 late: first late payment penalty = 3% of the VAT owed at day 15.
- Day 31+ late: first penalty = 6% total (3% of the day-15 balance + 3% of the day-30 balance). Second penalty = daily rate of 10% per year on the outstanding balance, from day 31 until paid.
- Rate history: current 3%+3% / 10% applies to periods due on/after Apr-May 2025; earlier periods were 2%+2% / 4%. Present the CURRENT rates only.
- Time to Pay: an agreed TTP can mean lower or no penalties and can cover VAT, penalties and interest. Requesting by day 15 can avoid penalties; TTP stops further penalty accrual from the date of the request, provided the arrangement is kept.
- Late payment interest: Bank of England base rate + 4% per year, from the first overdue day.

## Open facts to CONFIRM before publish
- Online self-serve VAT payment-plan eligibility exact thresholds (amount owed, days after deadline, max plan length). Not on public guidance; confirm via the live eligibility service. Do NOT publish specific numbers unconfirmed; frame conditionally until confirmed.
- Statutory demand / winding-up petition company debt threshold (currently understood as GBP 750). Confirm.
- HMRC secondary preferential creditor status for VAT (since 1 Dec 2020). Confirm wording.
- Director personal liability: VAT is normally a company debt; PLN possible for deliberate default/fraud. Confirm wording; do not overstate.
- Current BoE base rate for the interest figure (rate is base + 4%).

## Voice / rules
- British spelling. No em dashes anywhere.
- Company-authored IP voice (not single-practitioner narrative). "we" sparingly.
- Do NOT steer directors to DIY with HMRC or imply they do not need an IP. Keep TTP useful but route genuine insolvency risk to the firm.
- Practical director guide, not a generic VAT explainer. No "what is VAT" section. No full CVA/CVL/administration guides (link out). No provider-style funding comparisons. No overlong legal caveats.
- Tone: clear, calm, practical, for stressed directors. Direct verbs: file, contact, calculate, record, review, act. No scare tactics. No vague "seek help soon" without the concrete next action.
- Reviewed-by + last-updated line required (compliance-sensitive YMYL).
