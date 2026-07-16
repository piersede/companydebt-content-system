# Growth Audit — Section 14: Conversion Rate Optimisation
**companydebt.com | audited 2026-07-10 | read-only live spot-checks via WebFetch**

## 0. Scope and evidence base

Live templates spot-checked (all fetched 2026-07-10, read-only):

1. Service/money page: https://www.companydebt.com/liquidation/creditors-voluntary-liquidation/
2. HMRC money page (site's #2 traffic page): https://www.companydebt.com/hmrc/cant-pay-vat/
3. Solvent-director money page: https://www.companydebt.com/liquidation/members-voluntary-liquidation/
4. Urgency page: https://www.companydebt.com/winding-up-petitions/
5. Top informational page (904 clicks/yr, site #1): https://www.companydebt.com/insolvency/shareholders-liable-company-debts/
6. Data-journalism article: https://www.companydebt.com/articles/pub-closures-in-the-uk/
7. Statistics hub: https://www.companydebt.com/uk-insolvency-statistics/
8. Lead tool: https://www.companydebt.com/insolvency-calculator/
9. Contact page: https://www.companydebt.com/contact-us/

Context that raises the stakes: GSC clicks collapsed ~89% (5,232/mo Mar 2025 → 576/mo Jun 2026), UK commercially relevant traffic is roughly 22 clicks/day. At that volume, conversion architecture is the single highest-leverage variable on the site: every incremental percentage point of visitor-to-enquiry conversion is worth more than most content projects. It also means A/B testing is statistically impossible — changes must be judgement-led and measured via before/after call and form volumes.

---

## 1. Inventory of conversion routes (verified)

| Route | Where | Friction | Expectation-setting | Verified state |
|---|---|---|---|---|
| Phone 0800 074 6757 ("Free Director Helpline") | Every page, 3–8 instances | Lowest | Hours Mon–Fri 8am–8pm shown inconsistently (absent on /contact-us/) | Single number sitewide; no visible call tracking (inference from rendered pages; not verified in GTM) |
| 4-field contact form (Name*, Email*, Phone*, Message, CAPTCHA) | Embedded on nearly every page + /contact-us/ | Low fields, zero qualification | "We aim to respond the same day" on /contact-us/ only; inline forms show "100% Confidential · Real Experts · Same-Day Support" but no what-happens-next; submit button rendered lowercase "submit" on CVL page | Verified on 6 templates |
| 30-Second Insolvency Test (/insolvency-calculator/) | Sidebar widget on all content pages | Medium-high: 3 debt sliders + assets + PG question, then Name*/Email*/Phone* mandatory BEFORE results | "Complete the test and a member of our team will be in touch" — i.e. results are effectively a callback, not an instant answer, despite sidebar promising "Instant assessment. See your result immediately" | Verified; contradiction between sidebar promise and tool behaviour |
| LiveChat | "use our live chat during working hours" text mention | Low | Working hours only | Mentioned in contact sections; widget itself not exercised (read-only audit) |
| Email info@companydebt.com + "Email Chris" | Footers, author bios | Low | None | Verified; "Email Chris" actually links to /contact-us/, not a mailto — mild bait-and-switch |
| Stressed Directors Guide PDF | Sidebar on all pages | Zero (ungated) | n/a | Verified ungated; no email capture anywhere on site |
| "Get a Quote" | MVL page only | Unknown (not exercised) | None visible | Verified present on MVL |
| Callback booking / WhatsApp / SMS / out-of-hours | — | — | — | Verified ABSENT sitewide |

---

## 2. The central finding: one conversion stack for every intent stage

The same four-piece furniture set — helpline number, 4-field form, Stressed Directors Guide, 30-Second Test sidebar — appears identically on:

- a director staring at a winding-up petition (hours from a frozen account),
- a solvent director price-shopping an MVL to save tax,
- a shareholder idly checking whether they can be made liable,
- a journalist reading pub-closure statistics,
- an accountant checking insolvency numbers on the data hub.

This is the classic "every visitor into the same funnel" anti-pattern, and on a regulated, high-anxiety YMYL site it costs in both directions: the panicked director gets no faster route than the browser, and the researcher gets an emotionally mismatched pitch ("Stressed Directors Guide" offered to a solvent MVL shopper — verified on the MVL page) that quietly signals the page wasn't built for them.

What's genuinely good and should be kept:
- Phone-first architecture is right for this audience. A distressed director wants a human, today. 4–8 instances per page is not too aggressive given the intent.
- Pricing transparency (CVL £4,000–£6,000+VAT; MVL £3,000–£5,000+VAT with the £17,750 worked example) is a sector-unusual trust asset sitting right next to CTAs.
- Credential wrapping is strong: named licensed IPs with IP numbers, IPA/ICAS/TMA logos, "Reviewed by Chris Andersen" bylines.
- Tone is broadly appropriate: "confidential, no-obligation", "Get advice while you still have options" — reassuring, not predatory. The disclosure ("We are not independent of the process described on this page") is honest and rare.

---

## 3. Route-by-route assessment

### 3.1 Phone (primary route) — right strategy, unmeasured and capped at 8pm

- **Visibility:** excellent; header, hero, summary boxes, footer on every page.
- **Attribution blindness:** a single static 0800 number sitewide, with no visible dynamic number insertion, means the dominant conversion route cannot be attributed to page, query, or channel. With ~22 UK clicks/day, per-page call data is the ONLY way to know which content earns revenue. (Rendered-page inference; GTM internals not inspected — flagging as high-confidence but unverified in tooling. The colleague's cta_origin_url form-attribution work on staging shows the team already values this; phone is the bigger gap.)
- **Hours mismatch with anxiety cycles:** Mon–Fri 8am–8pm, no weekend, no out-of-hours story. Distressed-director panic famously peaks at night and on Sunday evening (inference, but strongly supported by the persona doc's "brown HMRC envelope" framing and by mobile click skew). Currently an out-of-hours visitor hits a dead number with no fallback promise.
- **/contact-us/ omits opening hours entirely** — verified. The one page whose only job is contact fails to say when the phone is answered.

### 3.2 Contact form — low friction, zero qualification, weak expectation-setting

- 4 fields is appropriately light for anxiety context. Keep it light.
- Zero qualification means every submission needs a human triage call; it also means the MVL price-shopper, the £5k-debt micro-company, and the £500k-creditor case all arrive identical. One optional dropdown ("What best describes your situation?" — can't pay HMRC / winding-up petition received / want to close solvent company / creditor pressure / other) would route and prioritise without adding real friction.
- Expectation-setting is thin and inconsistent: "We aim to respond the same day" appears on /contact-us/ but not beside the embedded forms; nothing anywhere says WHO calls back (a licensed IP? a salesperson?), from what number, or that the call is discreet. For a director hiding this from staff and co-directors, "what happens after I press submit" is the conversion moment. Verified absent on CVL, MVL, shareholders-liable templates.
- Cosmetic but real: lowercase "submit" button (CVL page). "Submit" is also the weakest possible verb in this context — "Request a confidential callback" does more work.

### 3.3 30-Second Test — the best asset on the site, strangled by its gate

Verified flow: sliders (Bank/HMRC/Creditors debt) → assets → personal guarantee Y/N → mandatory Name/Email/Phone → "a member of our team will be in touch."

- The sidebar sells it as "Instant assessment. See your result immediately… No signup required, 100% confidential." The tool then demands name, email and phone before any result, and the result is a callback. This is a direct promise-break at the moment of highest engagement, and the classic pattern that produces near-total step-2 abandonment.
- No privacy reassurance on the details step itself (verified) — exactly where the anxious user hesitates.
- The fix is not to remove capture but to reorder it: show the insolvency verdict instantly (it's computable client-side from the inputs already given), THEN offer "Want a licensed IP to talk you through your options? Leave your number — same-day, confidential." Users who have just been told "your company appears insolvent" convert at far higher intent than users asked to pay contact details for an unseen answer.
- Nice touch worth keeping: the "best time to contact" dropdown (ASAP / weekday AM/PM) — the only place on the site the user gets control over the callback.

### 3.4 Winding-up petition page — urgent copy, business-hours conversion

Verified: copy escalates correctly ("the bank account is likely to freeze within hours", "call a licensed IP today. Not tomorrow.", "The cases we see go cleanest are the ones where the director called us the same day the petition arrived") — but the conversion options are the standard stack: same number, Mon–Fri 8–8, same footer form, guide download mid-page.

- A "call today, not tomorrow" page with no out-of-hours route is a cheque the phone can't cash. Even without staffing a 24/7 line, an emergency-specific promise closes the gap: "Petition received? Submit before 8am and a licensed IP calls you first thing — priority queue." A dedicated short form (petition date + hearing date + phone) would let triage genuinely prioritise.
- Offering the Stressed Directors Guide PDF mid-page here is a downgrade CTA: it invites the most valuable, most time-critical visitor on the site to leave and read a PDF.
- This 3-page cluster is also the site's highest case-value traffic; the CRO gap and the SEO gap (thin cluster) compound.

### 3.5 MVL page — the one persona-matched CTA, surrounded by mismatch

- "Get a Quote" exists (verified) — correct for a price-shopper. But the sidebar still runs the distress stack: 30-Second INSOLVENCY Test and Stressed Directors Guide offered to a solvent director closing a company with £100k in it. Verified mismatch.
- The £17,750 tax-saving worked example is the strongest conversion copy on the site and is inert — it should be an interactive "MVL savings calculator" (reserves in → estimated saving + all-in fee out → quote request). That is a qualified, high-intent capture for the exact segment that price-shops across Clarke Bell et al.
- No expectation-setting after "Get a Quote" (how fast, what's needed, fixed-fee or estimate).

### 3.6 Informational pages — generic CTAs against specific worries

Shareholders-liable (site's top click earner, verified): the visitor is a worried shareholder/possibly-director; the guide is titled for directors; the sidebar test asks about company debts they may not control. End-of-page conversion is the standard form. What's missing is the intent-bridge micro-CTA: "Worried you're personally exposed? A licensed IP will tell you in one call — free, confidential." Same pattern applies across the 190 informational URLs: the CTA never names the fear the page just described.

### 3.7 Data assets — CTAs for the wrong audience entirely

- /uk-insolvency-statistics/ (verified): NO cite-this-data block, no CSV/download, no press contact, no newsletter, no methodology link — while the helpline appears twice. For the stated audiences (journalists, accountants, lenders) the conversion events should be: copy a citation, download data, email the press contact, subscribe to monthly updates. All absent. The pub-closures article (verified) already has cite-this-data blocks — the pattern exists and just wasn't carried to the hub.
- The accountant/referrer audience — the highest-LTV relationship this firm could build — has no capture anywhere: no partner page, no "refer a client" route, no stats-update list. (Consistent with the business-model finding of unserved segments.)

### 3.8 Email / nurture — a leak with no bucket

Verified: guide is ungated, no newsletter, no email capture of any kind. Directors typically lurk for weeks before calling (inference from persona doc + long consideration cycles in the category). Today the site's only options are "call now" or "vanish". A soft-gated guide ("Download instantly, or have it emailed with a 5-part what-happens-next series") and a monthly insolvency-statistics email (journalists + accountants) are the two obvious buckets. Given the anxiety context, keep instant access available — optional email delivery, never a hard gate.

### 3.9 Mobile

55% of clicks are mobile at 2x desktop CTR (GSC), against a known mobile Lighthouse ~38. Two CRO consequences: (a) any slow-loading form or CAPTCHA hits the majority audience hardest; (b) the highest-value mobile pattern for this site — a sticky click-to-call bar on money/urgency templates — could not be verified present from fetched markup and should be checked in the browser; if absent, it is likely the single cheapest conversion win available. (Unverified: rendered mobile viewport not inspected in this read-only pass.)

### 3.10 Trust wrapping at the decision point

- "Read our 9 reviews" adjacent to money-page CTAs (verified CVL/MVL) actively undercuts the 5-star homepage widget. Nine reviews for a firm claiming "thousands of directors helped" reads as a red flag to a sceptical director comparing against Begbies-scale competitors. Either grow the count deliberately (post-case review ask is standard in this sector) or stop surfacing the number next to the form until it's defensible.
- One case study sitewide (/case-studies/chinese-takeaway/). Nothing beats "a company like mine" proof at the decision point; the caseload exists, the content doesn't. Anonymised sector-matched outcome vignettes ("Construction, £180k HMRC arrears → CVL, directors clear in 6 weeks") next to CTAs on sector and money pages would work harder than logos.

---

## 4. Stage-appropriate CTA matrix (recommended target state)

| Page type | Visitor state | Primary CTA | Secondary | Remove/demote |
|---|---|---|---|---|
| Urgency (winding-up petition, statutory demand, cant-pay-* with enforcement) | Panic, hours-days horizon | Phone + priority same-day/first-thing callback promise; sticky mobile call bar | Short emergency form (petition/hearing date) | Guide PDF mid-page; generic test |
| Distress service (CVL, administration, TTP) | Anxious, days-weeks | Phone + "Request a confidential callback" form with what-happens-next 3-step | 30-Second Test (result-first) | — |
| Solvent service (MVL, strike-off) | Rational price-shopper | Get a Quote + MVL savings calculator | Phone | Stressed Directors Guide; insolvency test |
| Informational (190 pages) | Worried, researching, weeks-months | Intent-bridged micro-CTA naming the page's specific fear + phone | Guide with optional email delivery; test | Full contact form as the only closer |
| Data/statistics | Journalist, accountant, lender | Cite-this-data + CSV download + press contact | Monthly stats email signup | Helpline prominence |
| Articles/news | Mixed | Route to the matching money page first | Phone | — |

Tone rule for all of it: this is a regulated, shame-laden context. CTAs should promise discretion, speed and a named licensed human — never pressure. The site's existing register ("confidential, no-obligation") is right; the changes above are about matching the offer to the moment, not turning the volume up.

---

## 5. Prioritised recommendations

1. **Instrument the phone before touching anything else.** Dynamic number insertion (or at minimum distinct numbers for money vs info vs data templates) + form/chat/quote events. With ~22 UK clicks/day, judgement-led CRO is the only kind available, and it needs call-level ground truth. Everything below should be evaluated on before/after call+form volume per template. [Impact: high | Effort: low-medium]
2. **Reorder the 30-Second Test: result first, contact optional.** Fix the verified promise-break ("see your result immediately" vs mandatory details-for-callback). Show the verdict, then convert on the back of it. Add privacy line at the details step. [Impact: high | Effort: low]
3. **Build the emergency tier on winding-up-petition/statutory-demand pages:** priority-callback promise with explicit out-of-hours handling ("submit before 8am, first call of the day"), petition/hearing-date micro-form, sticky mobile call bar; pull the PDF download off these pages. [Impact: high | Effort: medium]
4. **Give MVL its own funnel:** interactive savings calculator feeding "Get a Quote"; strip the distress-branded sidebar from solvent pages. [Impact: medium-high | Effort: medium]
5. **Add what-happens-next to every form:** "Submit → a licensed insolvency practitioner (not a salesperson) calls you the same working day from a discreet number → free, no-obligation." Rename buttons from "submit" to "Request a confidential callback". Add hours to /contact-us/. [Impact: medium | Effort: low]
6. **Fix trust at the decision point:** systematic post-case review generation to retire "9 reviews"; 5–10 anonymised sector-matched outcome vignettes deployed beside money-page CTAs; hide the review count until defensible. [Impact: medium | Effort: medium]
7. **Convert the data hub for its actual audiences:** cite-this-data (pattern already exists on pub-closures), CSV download, press contact, monthly stats email — the last doubling as the site's first nurture list and an accountant-referrer hook. [Impact: medium (second-order: links, referrals) | Effort: low]
8. **Soft email capture for lurkers:** optional email delivery of the guide + a light what-happens-next sequence; never hard-gate. [Impact: medium | Effort: medium]

Verified vs inferred: all on-page observations above marked "verified" were confirmed in the 2026-07-10 fetches; call-tracking absence, night-time anxiety peaks, sticky-bar absence on mobile, and step-2 test abandonment are explicitly flagged as inference/unverified and are the first things the new instrumentation should confirm.
