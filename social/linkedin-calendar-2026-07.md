# Company Debt — LinkedIn Content Calendar
**Cycle 1 (rebuilt): 21 July to 13 August 2026**
Rebuilt 21 July 2026 on the evidence base. Supersedes the 17 July version (git `1285282`).
Channel: Company Debt Ltd company page.

---

## 1. What changed, and why

The first version of this calendar leaned almost entirely on the insolvency statistics hub: five of twelve posts were data posts and every post drove to the same page. It was authoritative and it was thin.

The rebuild follows evidence rather than instinct. The load-bearing study is the Money and Pensions Service randomised simulation (N=1,507):

| Condition | Sought debt advice |
|---|---|
| Control | 34.6% |
| Shown a **map of what the advice journey involves** | **54.0%** |
| Given a short **self-assessment checker** | **49.1%** |

Both significant at p<.001. Both also moved help-seeking to **earlier trigger points**, which is precisely the commercial outcome Company Debt wants: directors arriving before the position is unsalvageable.

So the two highest-evidence content formats are **process demystification** and **self-assessment**, and Company Debt already owns both assets (`/liquidation/uk-insolvency-flowchart/`, `/insolvency-calculator/`). They had never been pointed at LinkedIn.

Three further findings shape the copy:

- **52% of people who objectively need debt advice do not recognise themselves as having a debt problem.** Content addressed to "companies in trouble" misses half its audience by construction. Every post here uses **symptom framing**, never category labels.
- The two universal barriers are **embarrassment and feeling overwhelmed**. Avoidance is a confirmed self-reinforcing coping strategy, not laziness. Escalation copy feeds it.
- A debtor's **subjective** sense of how big the debt is predicts stress and avoidance better than the actual amount. Arguing about numbers misses the driver.

**Audience is unchanged.** Accountants, solicitors, brokers, and the ~115 journalists the outreach programme already emails. Written to the referrer and the journalist, in front of the director. The expansion is the **pre-crisis owner**: solvent but worried, on LinkedIn, badly served. Not the acute-crisis director, who is on Google at 23:00.

### What the platform actually does (primary sources only)

- The ranker optimises **Long Dwell** and **Contribution**. The dwell threshold is set **per post type**, so a carousel and a text post are scored against different bars. Carousels are not "boosted"; swiping holds the viewport.
- Since **March 2026 retrieval is LLM semantic embeddings, not keyword matching.** Topical consistency beats hashtags. Being narrowly and repeatedly about UK corporate insolvency is the whole strategy.
- Post popularity is **encoded directly into retrieval as percentile tokens**. Engineered rich-get-richer. At 241 followers this compounds against a company page, which is the strongest argument for the Chris Andersen route.
- Link penalty is ~19%, not the 60% folklore. Links go in the post.

---

## 2. Compliance rules, now binding

The IPA requires members to review and approve **all advertising including social media content**, and to ensure "vulnerable individuals are not targeted, exploited, or triggered by messaging" (IPA VIPP guidance).

**Every post in this calendar needs named practitioner sign-off before publication. That is Chris Andersen (IP No. 16070).** This is a professional obligation, not a preference.

ASA/CAP rulings that bear directly on this calendar:

- No implying anyone qualifies without stating eligibility.
- **A "60-second quiz to qualify" was ruled irresponsible.** The insolvency calculator must always be framed as **diagnostic** ("questions that tell you whether to take advice"), never as **qualifying** ("find out if you qualify"). This is the single sharpest line in the calendar.
- Never imply a process is free when charges follow. "No charge for the initial call" is fine. "Free liquidation" is not.
- No implied government or charity endorsement.

Caveat: this ASA guidance covers consumer debt management and IVAs. Company Debt does corporate insolvency, so treat it as directly relevant in spirit rather than exactly the governing regime.

**Still outstanding:** the ICAEW Insolvency Code of Ethics (in force 1 Oct 2025) has not been read. ICAEW web pages are JavaScript shells and could not be retrieved. If Andersen is ICAEW-licensed this is the binding document and someone should pull the PDF.

### Copy rules

- No em or en dashes.
- No "24/7". The helpline is not staffed 24/7.
- No "fixed fee" or "no surprise costs". **Note:** `data/statutory_fees.json` describes the CVL fee as a "standard fixed fee". That phrasing conflicts with the house rule and is not used here. Costs are given as typical ranges.
- "Confidential" in every director-facing CTA.
- Symptom framing, never category labels.
- Plain English before the technical term.
- No invented casework, no fabricated client stories.
- Links in the post. Hashtags 0 to 3. Hook inside the first ~140 characters.
- Every figure traceable to the Insolvency Service release, `data/statutory_fees.json`, `data/payment-practices/`, or legislation.

---

## 3. Pillars

| Pillar | What it is | Posts | Share |
|---|---|---|---|
| **The Process Map** | What actually happens, step by step. The highest-evidence format. | 2, 6, 7, 10 | 4/12 |
| **The Self-Check** | Diagnostic questions and symptom framing. Never qualifying. | 3, 8 | 2/12 |
| **Real Numbers** | What things actually cost. Rare in this market. | 4, 9 | 2/12 |
| **Who Pays Late** | Payment-practices data. The owner as victim, not accused. | 5, 11 | 2/12 |
| **The Data Desk** | The insolvency figures. The credential, not the programme. | 1, 12 | 2/12 |

Data Desk drops from 5 posts to 2. The Process Map, which did not exist in v1, becomes the largest pillar.

---

## 4. Visual system (unchanged)

| Element | Spec |
|---|---|
| Canvas | **1080 x 1350 (4:5 portrait)**. Non-negotiable. Vertical pixels are dwell. |
| Carousel | PDF, 9 to 10 slides, under 10MB |
| Base | Navy `#002856` |
| Accent (one per slide) | Orange `#f60` |
| Panel / chart fill | Light blue `#e7f6fd`, mid blue `#98b0c5` |
| Text on navy | White `#fff` |
| Typeface | Lato |
| Number scale | Headline figure 180 to 260px, readable as a thumbnail |
| Words per slide | Under 25 |
| Logo | Bottom right, small, every slide |

One idea per slide, one orange number per slide. If a slide needs a sentence to explain the number, the number is wrong.

**Asset status: none of these exist.** There is no slide tooling in `scripts/`. Six SVG charts sit in `data/insolvency-statistics/charts/` but are built on April 2026 data and must be regenerated on the June series before use.

---

## 5. The calendar

Cadence: Tue and Thu 08:00, Wed 12:00.

| # | Date | Format | Pillar | Working title |
|---|---|---|---|---|
| 1 | Tue 21 Jul, 08:00 | Carousel, 10 | Data Desk | The 80% that isn't what it looks like |
| 2 | Wed 22 Jul, 12:00 | Carousel, 10 | Process Map | The first 48 hours after a winding-up petition |
| 3 | Thu 23 Jul, 08:00 | Text + image | Self-Check | Six questions, none of which mention insolvency |
| 4 | Tue 28 Jul, 08:00 | Carousel, 9 | Real Numbers | What liquidation actually costs |
| 5 | Wed 29 Jul, 12:00 | Single image | Who Pays Late | 47 days |
| 6 | Thu 30 Jul, 08:00 | Text + image | Process Map | What a liquidator asks you for |
| 7 | Tue 4 Aug, 08:00 | Carousel, 10 | Process Map | The morning the account stops working |
| 8 | Wed 5 Aug, 12:00 | Poll | Self-Check | The first thing that slipped |
| 9 | Thu 6 Aug, 08:00 | Text + image | Real Numbers | £2,952 to end a company. £13 to close one. |
| 10 | Tue 11 Aug, 08:00 | Carousel, 9 | Process Map | Administration and liquidation are not alternatives |
| 11 | Wed 12 Aug, 12:00 | Single image | Who Pays Late | The 60 day tail |
| 12 | Thu 13 Aug, 08:00 | Single image | Data Desk | 1 in 198 |

**Timing note:** post 1 carries the June release published 17 July. It is already late and decays daily. Ship it as soon as an asset exists.

**Loop:** the July figures publish 18 August, just after post 12. Cycle 2 restarts on that release.

---

## 6. The posts, drafted

### POST 1 — Tue 21 July, 08:00
**Carousel, 10 slides. Pillar: Data Desk.**

> Administrations rose 80% in the year to June. About 60 of last month's came from a single connected group in real estate.
>
> That caveat is in the Insolvency Service's own commentary, published on 17 July, and it changes the story.
>
> June 2026, England and Wales:
>
> Total company insolvencies: 1,845. Flat on May's 1,849. Down 10% on June 2025.
> Creditors' voluntary liquidations: 1,364. Down 15% on the year.
> Compulsory liquidations: 276. Down 15% on the year.
> Administrations: 191. Up 45% on May, up 80% on June 2025 (106).
> Company voluntary arrangements: 14. Down 44% on May.
>
> Take the roughly 60 connected real estate companies out of the administrations figure and you are left with about 130. That is level with May and around a quarter up on last June. A real rise, and a considerably duller one than 80%.
>
> This is worth knowing before the number gets quoted. One group failing in one sector is not a shift in how larger companies are failing, and the monthly series will look distorted for a year because of it.
>
> The line we would watch instead is the CVA. Fourteen in a month, down 44%, and the main legal route to rescuing a company without closing it. Across a national economy that is a rescue mechanism close to disuse, and unlike the administrations figure, nothing unusual is propping it up.
>
> Full figures by procedure, by sector, back to 2000:
> https://www.companydebt.com/data/uk-insolvency-statistics/
>
> Source: Insolvency Service, Company Insolvency Statistics June 2026 (accredited official statistics).
>
> #insolvency #ukeconomy

**Slides:**
1. Cover, navy. `80%` orange. Sub: "Administrations, year to June 2026. Mostly one group."
2. `1,845` total. Sub: flat on May, down 10% on the year.
3. Stacked bar: CVL 1,364 / Compulsory 276 / Admin 191 / CVA 14.
4. `191` administrations. Sub: up 45% on May.
5. `~60` orange. Sub: connected real estate companies inside that figure.
6. `~130` orange. Sub: administrations excluding them. Level with May.
7. Plain English: what administration is. Under 25 words.
8. `14` CVAs. Sub: down 44% in a month.
9. "The rise is real. It is a quarter, not 80%."
10. Source + hub URL + logo.

---

### POST 2 — Wed 22 July, 12:00
**Carousel, 10 slides. Pillar: Process Map. The flagship of the new approach.**

> Most directors who receive a winding-up petition spend the first day trying to work out what it is. That is the day that matters most.
>
> Here is the sequence, in order, with the deadlines that actually bite.
>
> A petition is not a demand for payment. It is an application to the court to close your company, and once it is advertised in The Gazette your bank will very likely freeze the account. That advertisement can come seven business days after service.
>
> So the window between the petition landing and the account stopping is usually about a week. Not the seven weeks people assume from the hearing date.
>
> What happens in that window decides most of it:
>
> Day 0. Petition served on the registered office. The clock starts here, not when you read it.
> Day 1 to 7. The only period in which most of the useful options exist. A validation order, a challenge to the debt, payment, or a voluntary liquidation that takes control of the process.
> Day 7 onward. Gazette advertisement. Bank accounts commonly frozen from this point. Suppliers and customers can now see it.
> The hearing. Typically six to ten weeks after service. By then most of the decisions have already been made for you.
>
> The part worth saying plainly: after the account freezes, any payment made out of it can be void under section 127 of the Insolvency Act 1986, which is why banks freeze rather than risk it. A validation order is what unlocks specific payments, and it has to be applied for.
>
> None of this requires you to have decided anything. It requires you to know what the dates are.
>
> The full process, with the documents involved:
> https://www.companydebt.com/winding-up-petitions/
>
> If a petition has been served, speak to a licensed insolvency practitioner while the options still exist. Free initial call, confidential, no obligation.
>
> #insolvency #restructuring

**Slides:**
1. Cover, navy. `7 DAYS` orange. Sub: "The real window after a winding-up petition."
2. What a petition actually is. Under 25 words. Not a demand for payment.
3. `Day 0` orange. Served at the registered office. The clock starts here.
4. `Day 1-7` orange. Where the options live.
5. The four options, as a simple list. No number.
6. `Day 7` orange. Gazette advertisement.
7. The freeze. Plain English, why the bank does it. Section 127.
8. `6-10 weeks` orange. The hearing. Sub: most decisions already made.
9. "The window is the first week, not the last."
10. Source + URL + logo.

**Note:** the seven-business-day advertisement convention and the six-to-ten-week hearing range must be checked against `drafts/7687_winding-up-petitions.html` before build. Everything else here is statutory.

---

### POST 3 — Thu 23 July, 08:00
**Text + image. Pillar: Self-Check.**

> Six questions. None of them use the word insolvency, and that is deliberate.
>
> Roughly half of people who objectively need financial advice do not recognise themselves as having a problem, because the label does not match how it feels from inside. It does not feel like insolvency. It feels like a difficult month that has lasted three quarters.
>
> So, plainly:
>
> 1. Have you paid a supplier late this quarter in order to pay wages?
> 2. Is there VAT or PAYE sitting in the account that is doing other work?
> 3. Have you personally lent the company money, or put company costs on a personal card?
> 4. Do you know, today, what the company owes in total?
> 5. Has a payment run been decided by who is chasing hardest rather than who is owed longest?
> 6. Would the company survive one significant customer paying sixty days late?
>
> Answering yes to some of these does not mean a company is insolvent. Insolvency has two statutory tests, the cash flow test and the balance sheet test, both in section 123 of the Insolvency Act 1986, and neither is a feeling.
>
> What these questions do tell you is whether it is time to look properly. That is a different and much lower bar, and it is the one most directors leave far too late.
>
> The two statutory tests, explained without the jargon:
> https://www.companydebt.com/insolvency-calculator/
>
> #insolvency

**Visual:** Navy. The six questions as a numbered list, white, generous leading. One orange element only: the numeral `6` at the top. No imagery of distress. Deliberately calm.

**Compliance note:** this post is diagnostic, never qualifying. It must never suggest the questions determine eligibility for anything. The ASA ruled a "60-second quiz to qualify" irresponsible.

---

### POST 4 — Tue 28 July, 08:00
**Carousel, 9 slides. Pillar: Real Numbers.**

> Almost nobody in this industry publishes what liquidation costs. Here are our actual numbers.
>
> A straightforward creditors' voluntary liquidation, the process used when a company cannot pay its debts and the directors choose to close it:
>
> Practitioner fee: £3,500 plus VAT for a straightforward case.
> Disbursements: £500 to £1,500. Bond, Gazette notices, Companies House filing, statutory mailings.
> Typical all in: £4,000 to £5,000.
>
> Two things worth being honest about.
>
> First, that range holds for straightforward cases. Complexity moves it. A company with disputed assets, multiple sites, employee claims or an overdrawn director's loan account is not a straightforward case and will not cost the same. Anyone quoting a single number without asking about those things is guessing.
>
> Second, the money usually does not come from the director personally. Where the company has assets, realisations fund the process. Where it does not, there are still routes, and that conversation is worth having before assuming it is unaffordable. "We cannot afford to liquidate" is one of the most common reasons directors do nothing, and it is often wrong.
>
> The cost breakdown in full, including what changes it:
> https://www.companydebt.com/liquidation/how-much-does-liquidation-cost/
>
> If you want a straight answer on what your situation would cost, ask. Free initial call, confidential, no obligation.
>
> #insolvency

**Slides:**
1. Cover, navy. `£4,000-£5,000` orange. Sub: "What a straightforward CVL costs. Published."
2. `£3,500` orange. Practitioner fee, plus VAT.
3. `£500-£1,500` orange. Disbursements, itemised in under 25 words.
4. What the disbursements actually are. List. No number.
5. "Straightforward" defined. Under 25 words.
6. What moves the price. Four items, no number.
7. Where the money comes from. Realisations, not the director's pocket.
8. "Cannot afford to liquidate is usually wrong."
9. Source + URL + logo.

**Data source:** `data/statutory_fees.json` (`cvl_practitioner_fee`, `cvl_disbursements`, `cvl_all_in`), verified 2026-07-14. Do not use the phrase "fixed fee" even though the data file uses it.

---

### POST 5 — Wed 29 July, 12:00
**Single image. Pillar: Who Pays Late.**

> Manufacturers wait 47 days to be paid. The finance sector waits 24.
>
> We pulled the government's payment practices data: every large UK company has to report how fast it actually pays its suppliers. 6,882 companies, reporting between December 2024 and May 2026.
>
> Average days to pay an invoice, by sector:
>
> Manufacturing: 47.4
> Wholesale and retail: 38.5
> Construction: 34.7
> Professional services: 34.5
> Transport and storage: 34.4
> Information and communication: 33.6
> Accommodation and food: 33.7
> Admin and support: 29.9
> Education: 24.8
> Finance and insurance: 24.3
>
> Across all sectors the average is 34.5 days and 22% of invoices are not paid within the agreed terms.
>
> Worth being precise about what this measures. The reporting duty falls on large companies, so this is a picture of how big businesses treat their suppliers, not how small ones behave. If you are a small manufacturer waiting a month and a half, the data says that is normal rather than personal.
>
> It is also the single most common route into corporate insolvency that has nothing to do with how well a business is run. A profitable company with a 47 day payment cycle and a 30 day cost cycle is one delayed invoice from a serious problem.
>
> Full sector data:
> https://www.companydebt.com/data/payment-practices-late-payment/
>
> Source: UK payment practices reporting, 6,882 companies, Dec 2024 to May 2026.
>
> #latepayment #insolvency

**Visual:** Navy. Horizontal bar chart, sector days-to-pay, bars in `#98b0c5`. Manufacturing bar alone in orange `#f60` with `47.4` called out large. Sector labels white. Footer source line.

---

### POST 6 — Thu 30 July, 08:00
**Text + image. Pillar: Process Map.**

> If you appoint a liquidator, the first thing they ask for is a statement of affairs. Most directors have never seen one and assume it is worse than it is.
>
> It is a sworn document listing what the company owns and what it owes, on a specific date. That is all it is. It is not a confession and it is not an assessment of your conduct.
>
> What goes in it:
>
> Assets, at realisable value rather than book value. What things would actually fetch, not what they cost.
> Creditors, every one, including HMRC, trade suppliers, landlords, lenders, and any amount owed to you personally.
> Charges, secured lending and who holds it.
> Employees, and what they are owed.
> The directors' loan account position, in both directions.
>
> The part directors most often get wrong is the last one. If the company owes you money you are a creditor and should be listed. If you owe the company money, that is an asset the liquidator has to pursue, and leaving it out does not make it disappear. It is the single most common reason a straightforward liquidation stops being straightforward.
>
> The document is prepared with the practitioner, not by you alone, and it is normal to arrive without the figures in order. Turning up with a shoebox is not unusual and it is not a problem.
>
> What the statement of affairs covers, in full:
> https://www.companydebt.com/insolvency/statement-of-affairs/
>
> #insolvency

**Visual:** Navy. The five contents as a clean document-shaped panel in `#e7f6fd`, with the directors' loan account line highlighted in orange. No number on this one, deliberately. Caption: "The one line directors get wrong."

---

### POST 7 — Tue 4 August, 08:00
**Carousel, 10 slides. Pillar: Process Map.**

> The card is declined at the fuel station. That is how most directors find out the company account has been frozen.
>
> Nobody rings to tell you. Here is what has actually happened, and what can still be done.
>
> A bank freezes a business account when it learns of a winding-up petition, usually from the Gazette advertisement. The bank is not making a judgement about your business. It is protecting itself, because under section 127 of the Insolvency Act 1986 any disposition of company property after the petition is presented can be void, and the bank could be required to repay it.
>
> What stops working, usually the same day:
>
> Card payments and standing orders.
> Wages, including the run that is already scheduled.
> Direct debits, which then generate their own defaults.
> Incoming payments, which are held rather than returned.
>
> What can still be done:
>
> A validation order. An application to the court to authorise specific payments, most commonly wages, rent and suppliers essential to continued trading. It is not automatic and it is not quick, but it is the mechanism that exists for exactly this, and it is routinely granted where the payments keep a viable business running.
>
> Practical sequence: find out whether a petition has been advertised, get the petition documents, and take advice the same day. Every day the account is frozen without an application is a day of avoidable damage.
>
> What to do when an account freezes:
> https://www.companydebt.com/advice/frozen-bank-account/
>
> If this has happened, do not wait for the hearing. Speak to a licensed insolvency practitioner today. Free initial call, confidential, no obligation.
>
> #insolvency #restructuring

**Slides:**
1. Cover, navy. `DECLINED` white, large. Sub: "How most directors learn the account is frozen."
2. Why the bank did it. Under 25 words. Not a judgement.
3. `s.127` orange. Insolvency Act 1986, in plain English.
4. What stops. Four items.
5. Wages. The one that hurts first.
6. `VALIDATION ORDER` orange. What it is.
7. What it can authorise. Three items.
8. What it is not. Not automatic, not instant.
9. "The damage is done by waiting, not by the freeze."
10. Source + URL + logo.

---

### POST 8 — Wed 5 August, 12:00
**Poll. Pillar: Self-Check.**

> A question for the accountants and advisers here.
>
> When a client's company is heading for trouble, what is the first thing you see slip?
>
> [ ] VAT or PAYE paid late
> [ ] Suppliers stretched beyond terms
> [ ] Management accounts stop arriving
> [ ] The director stops returning calls
>
> There is a reason for asking. Directors rarely present at the point the numbers turn. They present much later, usually when something external forces it, and the gap between those two moments is where most of the avoidable damage happens.
>
> Advisers see the early signal. Directors, understandably, experience it as a difficult month rather than a pattern.
>
> Interested in what people actually see first, and in any order of events that does not appear on the list.
>
> #insolvency

**Visual:** None. Native LinkedIn poll.

**Note:** the poll is the cheapest experiment in the cycle and the only post that asks the audience to contribute. Contribution is a separately modelled ranking objective, so a poll that gets comments is doing something the carousels cannot. Read the comments properly; the fourth option is the one worth watching.

---

### POST 9 — Thu 6 August, 08:00
**Text + image. Pillar: Real Numbers.**

> It costs a creditor £2,952 to try to close your company. It costs you £13 to close it yourself.
>
> Both numbers are current and both are public, and the gap between them explains a lot about how these situations unfold.
>
> To present a winding-up petition, a creditor pays a £352 court fee and a £2,600 deposit to the Insolvency Service. £2,952 before any legal costs. That is a real commitment, which is why petitions are usually a last resort rather than an opening move, and why a creditor threatening one has often already decided.
>
> To apply to strike a company off the register, a director pays £13 online, or £18 on paper, to Companies House.
>
> The £13 route is where directors get into trouble. Striking off is for companies that have no debts and no ongoing obligations. Using it to walk away from creditors does not work: any creditor can object and stop it, the company can be restored to the register afterwards, and the conduct is reportable. It is also the route that most reliably turns a closable situation into a disqualification question.
>
> The honest summary. £13 is the right price when a company genuinely has nothing outstanding. When it has creditors, £13 buys a delay and a problem, not an ending.
>
> The difference between striking off and liquidation:
> https://www.companydebt.com/liquidation/how-much-does-liquidation-cost/
>
> #insolvency

**Visual:** Navy, split panel. Left: `£2,952` orange, caption "What a creditor pays to petition." Right: `£13` orange, caption "What a director pays to strike off." Below, one white line: "Only one of them ends the debt."

**Data source:** `data/statutory_fees.json` (`winding_up_petition_court_fee` £352, `winding_up_petition_deposit` £2,600, `strike_off_ds01_online` £13, `strike_off_ds01_paper` £18), verified 2026-07-14. **The v1 calendar used £750 and £10 for these. Both were wrong.**

---

### POST 10 — Tue 11 August, 08:00
**Carousel, 9 slides. Pillar: Process Map.**

> Administration and liquidation get discussed as if they are two options on the same menu. They are not, and choosing between them is rarely the actual decision.
>
> Administration is a rescue and realisation process run by an administrator who takes control of the company. Schedule B1 of the Insolvency Act 1986 gives them three objectives, ranked, and they must pursue the first that is reasonably practicable:
>
> 1. Rescue the company as a going concern.
> 2. Achieve a better result for creditors as a whole than winding up would.
> 3. Realise property to pay secured or preferential creditors.
>
> Only the first is rescue in the sense a director means. Most administrations land on the second. The business often survives, sold as an asset to a new owner. The company, the shares and usually the director's position do not.
>
> Liquidation ends the company. It does not attempt rescue. A creditors' voluntary liquidation is director-initiated, which means the timing and the choice of practitioner sit with you. A compulsory liquidation is court-imposed and neither does.
>
> What actually decides it is not preference. It is whether there is a business worth buying, whether there is secured lending, whether trading can continue without personal exposure, and how much time is left. A company with no assets and no buyer does not have an administration option, whatever anyone would prefer.
>
> The realistic version: by the time most directors ask which process they want, the facts have already narrowed it to one. The value of asking early is that they have not.
>
> What administration involves, and what it does not:
> https://www.companydebt.com/company-administration/
>
> If you are weighing these against each other, speak to a licensed insolvency practitioner before filing anything. Free initial call, confidential, no obligation.
>
> #insolvency #restructuring

**Slides:**
1. Cover, navy. "Not two options on the same menu." No number.
2. `3` orange. Administration's three statutory objectives.
3. Objective 1. Rescue the company. Orange rung.
4. Objective 2. Better result for creditors. Mid blue. Caption: "Most land here."
5. Objective 3. Realise property. Mid blue.
6. What survives, what does not. Business vs company.
7. Liquidation. Ends the company. CVL vs compulsory in under 25 words.
8. What actually decides it. Four factors.
9. Source + URL + logo.

---

### POST 11 — Wed 12 August, 12:00
**Single image. Pillar: Who Pays Late.**

> About 12% of invoices from large UK companies are paid more than 60 days after they are issued.
>
> That is the tail, and the tail is what kills otherwise healthy businesses.
>
> The averages look survivable. 34.5 days to pay, 59.8% of invoices settled within 30 days. A business can plan around an average. What it cannot plan around is the small proportion that goes very long, because those are the invoices that turn a working capital gap into a solvency question.
>
> One number for context. Company insolvencies in June 2026 ran at 1,845, and the great majority were creditors' voluntary liquidations, the process used by small companies that run out of cash rather than large ones that fail dramatically. Running out of cash and being unprofitable are different conditions with different remedies, and they get treated as the same thing far too often.
>
> If you are chasing an invoice past 60 days, two things are worth knowing. Statutory interest under the Late Payment of Commercial Debts (Interest) Act 1998 applies automatically whether or not it is in the contract, and if the customer is heading for insolvency the date you act materially affects what you recover.
>
> Sector by sector payment data:
> https://www.companydebt.com/data/payment-practices-late-payment/
>
> What to do when a customer that owes you money is going under:
> https://www.companydebt.com/insolvency/insolvent-company-owes-me-money/
>
> Sources: UK payment practices reporting, 6,882 companies, Dec 2024 to May 2026. Insolvency Service, June 2026.
>
> #latepayment #insolvency

**Visual:** Navy. `11.9%` orange at 240px. Beneath, white: "of invoices from large UK companies are paid later than 60 days." Small distribution strip along the bottom: within 30 days 59.8%, 31 to 60 days 28.3%, over 60 days 11.9%, the last segment in orange.

---

### POST 12 — Thu 13 August, 08:00
**Single image. Pillar: Data Desk. Cycle close.**

> 1 in 198 companies on the register entered insolvency in the 12 months to June 2026.
>
> That is a rate of 50.5 per 10,000. A year earlier it was 52.4.
>
> So the risk is easing. Slightly.
>
> One thing worth holding onto about rates. The register keeps growing. A falling rate measured against a growing denominator is not the same thing as fewer companies in trouble, and it is not remotely what an individual director experiences. For the company that fails, the rate is 1 in 1.
>
> The July figures publish on 18 August and we will run them the same way: what the number says, and what it does not.
>
> Where that rate sits against every year since 2000:
> https://www.companydebt.com/data/uk-insolvency-statistics/
>
> Source: Insolvency Service, June 2026.
>
> #insolvency

**Visual:** Navy. `1 in 198` orange at 240px, centred. Beneath, white, small: "50.5 per 10,000 companies. 12 months to June 2026. Down from 52.4." Footer source line.

---

## 7. Open items

| Item | Status | Blocks |
|---|---|---|
| Practitioner sign-off loop with Chris Andersen | Not set up | Everything. IPA requirement. |
| Visual assets | None exist. No slide tooling in `scripts/`. | All 12 posts |
| ICAEW Code of Ethics (1 Oct 2025) | Not retrieved | Compliance confidence |
| Chart SVGs on June data | Still April 2026 | Any chart reuse |
| Repo insolvency data refresh | Pinned at May 2026 (live hub is on June) | Cycle 2 |
| `editorial-os/17-audience-and-persona.md` | Still lists "24/7" and "Fixed-Price" | Re-seeds banned claims |
| Gazette petition tracker as a content pillar | Awaiting Théo's decision | Cycle 2 planning |
| Post 2 hearing-window figures | Verify against `drafts/7687_winding-up-petitions.html` | Post 2 build |

## 8. What to measure

Clicks and saves. Not reactions.

Likes are down platform-wide while overall engagement has risen, so a working programme will look flat on the vanity metrics. The signals that matter for this calendar specifically:

- **Click-through to `/insolvency-calculator/` and the flowchart.** The MaPS trial predicts these should outperform. If they do not, the hypothesis is wrong and cycle 2 should change.
- **Saves on the Process Map carousels.** A save is the clearest evidence an adviser intends to send it to a client.
- **Comment quality on post 8**, not comment count.
- **Referral conversations that begin "I saw your post"**, which will not appear in any dashboard and have to be captured manually.
