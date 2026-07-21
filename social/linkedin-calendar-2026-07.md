# Company Debt — LinkedIn Content Calendar
**Cycle 1: 21 July to 13 August 2026**
Built 17 July 2026. Channel: Company Debt Ltd company page only.

---

## 1. Where we're starting from

| Fact | Detail |
|---|---|
| Page | [uk.linkedin.com/company/companydebt](https://uk.linkedin.com/company/companydebt) |
| Followers | 241 |
| Employees listed | 5 |
| Posting history | One post ~mid-June (April figures). Before that, a 9-month gap. |
| Effective status | Dormant |

The page is not an audience yet. It is a placeholder. Cycle 1 is not a reach play; it is about establishing a publishing rhythm and a recognisable format so there is something worth following.

---

## 2. Strategy

### 2.1 The reframe that matters

The website audience and the LinkedIn audience are not the same people.

A director whose bank account froze this morning is on Google at 23:00, not scrolling LinkedIn. Writing the page as though distressed directors are the readership means writing crisis copy to an audience that is not in crisis.

Who is actually on LinkedIn and matters to Company Debt:

1. **Accountants** — the persona file already names them as "shadow decision-makers". They refer. They are on LinkedIn all day. They need to look competent in front of their client.
2. **Solicitors, brokers, lenders, IPs** — referral and professional network.
3. **Journalists** — the outreach programme is already pitching ~115 of them the stats hub by email. LinkedIn is the warming surface for the same people.
4. **Directors** — real, but secondary here, and mostly earlier in the journey than the site's crisis traffic.

So the calendar is written **to the referrer and the journalist, in front of the director.** Authoritative, data-led, legally precise. A director who finds it should feel they have found the grown-ups.

This also resolves the two constraints you set. Page-only and no-anecdote strip out the two biggest engagement levers on the platform. But referrers and journalists do not want war stories. They want figures they can cite and law they can rely on. The constraints and the audience point the same way.

### 2.2 What the research says (and how much to trust it)

Full brief informed this calendar. Load-bearing findings:

- **The only Tier 1 facts**: LinkedIn's ranker optimises "Long Dwell" (dwell past a threshold that varies *by post type*) plus "Contribution" (reactions/comments/shares). The graph is now an **Interest Graph**, not a relationship graph. Everything else in circulation is observational or invented. ([LinkedIn Engineering](https://www.linkedin.com/blog/engineering/feed/understanding-feed-dwell-time), [arXiv](https://arxiv.org/abs/2501.16450))
- **Document/carousel PDFs top every format study.** Not because they are "boosted" but because swiping mechanically holds the viewport, which is the ranker's actual objective. This is the highest-leverage format available and it is exactly the shape our data wants.
- **The Interest Graph is the whole ballgame for a niche brand.** Topical narrowness beats audience size. 241 focused followers is a worse starting point than 241 is flattering, but the mechanism rewards consistency, not scale.
- **The link penalty is ~19%, not the 60% folklore.** Links go *in the post*. A click from an accountant is worth more than 19% more impressions from nobody.
- **Hashtags: 0 to 3.** The best-controlled study finds no-hashtag posts slightly *outperform*. Treat as hygiene.
- **Company pages drive shares** where personal profiles drive comments. Shares are what data gets. Play to it.
- **Measure clicks and saves, not likes.** Reactions are down platform-wide while overall engagement is up. Vanity metrics will look flat while the thing works.

### 2.3 Honest limits of page-only

Company page organic reach has fallen sharply and only ~7% of pages grow enough to change follower tier. Personal profiles get 63% higher engagement at similar impressions. Page-only is a real ceiling, not a neutral choice.

That is a fine call for cycle 1 — prove the format with no colleague dependency. But the upgrade path is Chris Andersen (IP No. 16070). A licensed practitioner posting about insolvency outranks a brand account posting the same words, and it costs him a repost. Revisit at cycle 2.

### 2.4 Pillars

| Pillar | What it is | Posts |
|---|---|---|
| **The Data Desk** | The monthly figures and cuts from the hub. The moat. | 1, 2, 4, 5, 11 |
| **Myth vs Statute** | A common belief, then what the Act actually says. | 3, 9 |
| **The Legal Clock** | Statutory deadlines, thresholds, what a document means. | 6, 12 |
| **The Decision Table** | Trade-offs, side by side, honestly. | 7, 10 |
| **The Question** | One poll. A cheap experiment. | 8 |

### 2.5 Rules applied to every post

- Link in the post, never buried in the first comment.
- 0 to 3 hashtags.
- Hook must land inside the first ~140 characters.
- No em or en dashes (house voice rule, `outreach/lib/gates.js`).
- No "24/7" claims. The helpline is not staffed 24/7.
- No "fixed fee" or "no surprise costs" claims.
- "Confidential" appears in every director-facing CTA.
- Plain English before the technical term.
- Every figure traceable to the June 2026 Insolvency Service release, the verified figures whitelist, or legislation. Nothing invented.
- No first-hand casework, no invented clients.

---

## 3. Visual system

One recognisable look, so the feed starts to identify us before reading the name.

| Element | Spec |
|---|---|
| Canvas | **1080 x 1350 (4:5 portrait)**. Non-negotiable. Vertical pixels are dwell. |
| Carousel format | PDF, 9 to 10 slides (best-sourced optimum is ~9.2), under 10MB |
| Base | Navy `#002856` |
| Accent (one per slide, the number) | Orange `#f60` |
| Panel / chart fill | Light blue `#e7f6fd`, mid blue `#98b0c5` |
| Text on navy | White `#fff` |
| Typeface | Lato (site font). Bold for figures, Regular for body. |
| Number scale | The headline figure at 180 to 260px. It should be readable as a thumbnail. |
| Words per slide | Under 25. The number carries it. |
| Footer, every slide | `Source: Insolvency Service, June 2026` + `companydebt.com/data` |
| Logo | Bottom right, small, every slide |

**The rule that makes them stop:** one idea per slide, one orange number per slide. If a slide needs a sentence to explain the number, the number is wrong.

Existing SVG chart assets live in `data/insolvency-statistics/charts/`. **They are built from April 2026 data and must be regenerated on the June series before use in posts 5 and 11.**

---

## 4. The calendar

Cadence: 3 posts a week, Tuesday / Wednesday / Thursday. Tue and Thu 08:00, Wed 12:00. Timing is a second-order lever and the grids people sell are invented; do not over-tune it.

| # | Date | Format | Pillar | Working title |
|---|---|---|---|---|
| 1 | Tue 21 Jul, 08:00 | Carousel, 10 slides | Data Desk | Down 10%, up 80%: the June figures |
| 2 | Wed 22 Jul, 12:00 | Single image | Data Desk | 1 in 198 |
| 3 | Thu 23 Jul, 08:00 | Text + image | Myth vs Statute | Administration is not a rescue |
| 4 | Tue 28 Jul, 08:00 | Carousel, 9 slides | Data Desk | Why construction always tops the table |
| 5 | Wed 29 Jul, 12:00 | Single image | Data Desk | Six sectors, 72% of failures |
| 6 | Thu 30 Jul, 08:00 | Text + image | Legal Clock | £750 to start it, £2,943 to finish it |
| 7 | Tue 4 Aug, 08:00 | Carousel, 10 slides | Decision Table | The £10 closure and what it costs |
| 8 | Wed 5 Aug, 12:00 | Poll | The Question | The earliest sign |
| 9 | Thu 6 Aug, 08:00 | Text + image | Myth vs Statute | Why the bank freezes the account |
| 10 | Tue 11 Aug, 08:00 | Carousel, 9 slides | Decision Table | Fourteen |
| 11 | Wed 12 Aug, 12:00 | Single image | Data Desk | The strangest line on the chart |
| 12 | Thu 13 Aug, 08:00 | Text + image | Legal Clock | The £22,530 nobody mentions |

**Timing note:** post 1 carries the June release, published 17 July. News value decays fast. If you can ship it today or Monday, do. Tue 21 is the fallback, not the ideal.

**Loop:** the July figures publish ~mid-August, which lands just after post 12. Cycle 2 restarts the pattern on that release.

---

## 5. The posts, drafted

### POST 1 — Tue 21 July, 08:00
**Carousel, 10 slides. Pillar: Data Desk. Flagship.**

> Company failures fell 10% last month. Administrations rose 80%.
>
> Both numbers come from the same Insolvency Service release, published on 17 July.
>
> June 2026, England and Wales:
>
> Total company insolvencies: 1,845. Flat on May. Down 10% on June 2025.
> Creditors' voluntary liquidations: 1,364. Down 15% on the year.
> Compulsory liquidations: 276. Down 15% on the year.
> Administrations: 191. Up 45% on May, up 80% on June 2025.
> Company voluntary arrangements: 14. Down 44% on May.
>
> The headline reads like a recovery. The composition does not.
>
> Liquidation is mostly what happens to small companies. Administration is mostly what happens to larger ones, the kind with staff, contracts, and a business someone might still want to buy.
>
> So: fewer companies are failing, and the ones that do are bigger.
>
> Meanwhile CVAs, the main legal tool for rescuing a company without closing it, fell to 14 in a month. Across a national economy, that is not a rounding error. It is a rescue mechanism close to disuse.
>
> Full figures by procedure, by sector, back to 2000:
> https://www.companydebt.com/data/uk-insolvency-statistics/
>
> Source: Insolvency Service, Company Insolvency Statistics June 2026 (accredited official statistics).
>
> #insolvency #ukeconomy

**Slides:**
1. Cover, navy. `DOWN 10%` (white) / `UP 80%` (orange). Sub: "The same release. June 2026."
2. `1,845` total company insolvencies. Sub: flat on May, down 10% on the year.
3. Stacked bar: the composition. CVL 1,364 / Compulsory 276 / Admin 191 / CVA 14.
4. `191` administrations, orange, huge. Sub: up 80% on June 2025.
5. `14` CVAs, orange. Sub: down 44% in a month.
6. Plain English: what administration is. Under 25 words.
7. Plain English: what a CVA is. Under 25 words.
8. The point: "Fewer failures. Bigger ones."
9. `1 in 198` companies, 12 months to June.
10. Source + hub URL + logo.

---

### POST 2 — Wed 22 July, 12:00
**Single image. Pillar: Data Desk.**

> 1 in 198 companies on the register entered insolvency in the 12 months to June 2026.
>
> That is a rate of 50.5 per 10,000. A year earlier it was 52.4.
>
> So the risk is easing. Slightly.
>
> One thing worth holding onto about rates. The register keeps growing. A falling rate measured against a growing denominator is not the same thing as fewer companies in trouble, and it is not remotely what an individual director experiences. For the company that fails, the rate is 1 in 1.
>
> Where that rate sits against every year since 2000:
> https://www.companydebt.com/data/uk-insolvency-statistics/
>
> Source: Insolvency Service, June 2026.
>
> #insolvency

**Visual:** Navy. `1 in 198` in orange at 240px, centred. Beneath, small and white: "50.5 per 10,000 companies. 12 months to June 2026. Down from 52.4." Footer source line.

---

### POST 3 — Thu 23 July, 08:00
**Text + image. Pillar: Myth vs Statute.**

> Administrations rose 80% in the year to June 2026. So it is worth being precise about what one actually is.
>
> Administration gets described as a rescue process. Schedule B1 of the Insolvency Act 1986 is narrower than that. It gives an administrator three objectives, ranked, and they must pursue the first one that is reasonably practicable:
>
> 1. Rescue the company as a going concern.
> 2. Achieve a better result for creditors as a whole than winding up would.
> 3. Realise property to pay secured or preferential creditors.
>
> Only the first is rescue in the sense a director means it. Most administrations land on the second. The business may well survive, sold as an asset to a new owner. The company, the shares and usually the director's position do not.
>
> That distinction decides things. "We went into administration to save the business" and "the company was rescued" are different sentences, and staff, creditors and buyers all read them differently.
>
> What administration involves, and what it does not:
> https://www.companydebt.com/company-administration/
>
> If you are weighing it against liquidation or a CVA, speak to a licensed insolvency practitioner before you file anything. Free initial call, confidential, no obligation.
>
> #insolvency #restructuring

**Visual:** The three objectives as a ranked ladder, navy background, rung 1 in orange and rungs 2 and 3 in mid blue. Caption on the rung 2 block: "Most administrations end here."

---

### POST 4 — Tue 28 July, 08:00
**Carousel, 9 slides. Pillar: Data Desk.**

> Construction has topped the UK insolvency table for years. 3,805 failures in the 12 months to June 2026, 17% of every company insolvency in England and Wales.
>
> No other sector comes close on volume. Wholesale and retail is next at 3,463.
>
> The figure is down on the previous 12 months, along with most sectors. It is still the largest single block on the chart, and it has been for a long time.
>
> Why construction and not, say, manufacturing at 1,857? The data does not say. What the structure of the industry says, and this is editorial judgement rather than a statistic:
>
> Construction runs on long payment chains. A main contractor's failure travels down through subcontractors who have already bought the materials and paid the labour. Retentions hold cash for months after the work is done. Fixed price contracts signed before an inflation spike get delivered after it. None of that is a shock. It is the normal operation of the sector, which is why the number is stubborn rather than volatile.
>
> The full sector breakdown, updated monthly:
> https://www.companydebt.com/data/uk-insolvency-statistics/
>
> Source: Insolvency Service, June 2026.
>
> #construction #insolvency

**Slides:**
1. Cover: `3,805` orange. "Construction insolvencies, 12 months to June 2026."
2. `17%` of all company insolvencies.
3. Horizontal bar: construction against the other five top sectors. Construction in orange, rest mid blue.
4. "No other sector comes close on volume."
5. Payment chains. One line.
6. Retentions. One line.
7. Fixed price contracts. One line.
8. "Not a shock. The normal operation of the sector." (Label: editorial judgement.)
9. Source + hub + logo.

---

### POST 5 — Wed 29 July, 12:00
**Single image. Pillar: Data Desk.**

> Six sectors account for 72% of every company insolvency in England and Wales.
>
> 12 months to June 2026:
>
> Construction: 3,805 (17%)
> Wholesale and retail: 3,463 (15%)
> Accommodation and food: 3,233 (14%)
> Admin and support: 2,196 (10%)
> Professional and technical: 1,930 (8%)
> Manufacturing: 1,857 (8%)
>
> Most of these are down on the preceding 12 months, by between 1% and 10%. The order barely moves year to year. That stability is the interesting part. Insolvency is often reported as though it were weather, arriving and passing. The sector table reads more like geology.
>
> Full breakdown and the monthly series:
> https://www.companydebt.com/data/uk-insolvency-statistics/
>
> Source: Insolvency Service, June 2026.
>
> #insolvency #ukbusiness

**Visual:** League table, navy, six horizontal bars, orange to mid blue gradient by rank. Figures right-aligned in Lato Bold. Top strip: `72%`. **Regenerate `sector_bars.svg` on June data first.**

---

### POST 6 — Thu 30 July, 08:00
**Text + image. Pillar: Legal Clock.**

> It takes a debt of £750 to start a winding up petition. It takes £2,943 to see it through.
>
> The thresholds surprise people, so here they are plainly.
>
> £750 is the minimum debt for a statutory demand against a company, under section 123(1)(a) of the Insolvency Act 1986. Not £75,000. £750.
>
> A statutory demand gives the company 21 days to pay or reach an agreement. Miss it and the creditor has evidence the company cannot pay its debts, which is the ground for a petition under section 122.
>
> The petition itself costs the creditor £343 in court fees plus a £2,600 deposit for the Official Receiver. £2,943 in total, which is the real filter. Plenty of creditors are owed more than £750 and will not spend £2,943 to chase it. Some will, on principle.
>
> Then it is advertised in the Gazette, and the bank usually finds out before the hearing.
>
> The 21 days is the part that matters. It is the last cheap window in the process.
>
> What a petition is and what can still be done about one:
> https://www.companydebt.com/winding-up-petitions/
>
> If a demand has landed, get advice inside the 21 days. Free initial call, confidential, UK based.
>
> #insolvency #creditcontrol

**Visual:** Horizontal timeline, navy. Four stops: `£750 demand` → `21 days` → `£2,943 petition` → `Gazette`. The 21-day block in orange and twice the width, labelled "the last cheap window".

---

### POST 7 — Tue 4 August, 08:00
**Carousel, 10 slides. Pillar: Decision Table.**

> Striking a company off costs £10. Since 2021 it no longer puts a director out of reach of an investigation.
>
> The strike-off route is popular for an obvious reason. £10 against several thousand for a liquidation is not a close-looking decision, and for a genuinely clean company with no debts and no creditors, strike-off is the correct and cheap answer.
>
> It stops being the correct answer the moment there are debts.
>
> The Rating (Coronavirus) and Directors Disqualification (Dissolved Companies) Act 2021 gave the Insolvency Service power to investigate the directors of a dissolved company, and to seek disqualification, without first restoring the company to the register. Dissolution used to be a door closing. It is now a door that can be opened behind you.
>
> Creditors can also object to a strike-off, and HMRC does. A company with outstanding tax does not usually get quietly dissolved. It gets objected to, and the clock starts again with a worse story attached.
>
> The comparison, honestly:
> https://www.companydebt.com/liquidation/company-strike-off-and-dissolution/
>
> If there are debts and you are weighing the two, a licensed insolvency practitioner will tell you which one fits. Free initial call, confidential, no obligation.
>
> #insolvency #companylaw

**Slides:**
1. Cover: `£10` in orange, giant. Sub: "The cost of striking off a company."
2. "For a clean company with no debts, this is the right answer."
3. "With debts, it is a different question."
4. The 2021 Act, plain English. Investigation without restoration.
5. `2021`, orange. "Dissolution stopped being a door closing."
6. HMRC objects. One line.
7. Two-column table: strike-off vs CVL. Cost / creditors / investigation / redundancy eligibility / finality.
8. The redundancy line, flagged: a CVL can open a statutory redundancy claim. Strike-off does not.
9. "The £10 is real. It is just not the whole price."
10. Source + link + logo.

---

### POST 8 — Wed 5 August, 12:00
**Poll. Pillar: The Question.**

> A question for the accountants here.
>
> Company insolvencies ran at 1,845 in June. Every one of them was visible to someone before it was visible to the register.
>
> In your experience, what is the earliest reliable sign that a client company is in real trouble?
>
> [POLL, 4 options]
> - VAT payments going late
> - Payroll getting tight
> - Director's loan account growing
> - They go quiet
>
> Genuinely interested in the last one. The pattern we see reported most often is not a number moving. It is a client who used to call every month and now does not.
>
> Monthly figures, by procedure and sector:
> https://www.companydebt.com/data/uk-insolvency-statistics/
>
> #accounting #insolvency

**Notes:** Polls draw the highest average impressions on company pages and almost nobody uses them, so this is cheap arbitrage. But it is a **test, not a pillar** — poll impressions are low-intent, and some sources claim polls were hit in a 2026 authenticity update (thin evidence, but the risk is real). Run it once. Judge it on comment quality from actual accountants, not on impressions.

**Visual:** None. Polls render their own card.

---

### POST 9 — Thu 6 August, 08:00
**Text + image. Pillar: Myth vs Statute.**

> A winding up petition is advertised in the Gazette. Then the bank freezes the account. Most directors read that as the bank being cautious, or unhelpful, or both.
>
> It is neither. It is section 127.
>
> Under section 127 of the Insolvency Act 1986, if a winding up order is eventually made, any disposition of the company's property made after the petition was presented is void, unless the court validates it. Not reversible. Void, from the start.
>
> Which means a bank that keeps processing payments is potentially handling money that was never the company's to move, and can be asked to account for it. The freeze is not the bank judging you. It is the bank protecting itself from a statutory provision that operates with hindsight.
>
> This matters because it changes what you do about it. Arguing with the bank does not work, because the bank is not the decision maker. A validation order from the court is the mechanism, and it exists precisely because otherwise a company would be unable to pay wages or suppliers between petition and hearing.
>
> The point directors most often miss: the freeze can arrive before the hearing, off the back of the Gazette notice. Payroll can stop while you still believe you have time.
>
> What a petition triggers, and what can be done at each stage:
> https://www.companydebt.com/winding-up-petitions/
>
> If an account has frozen, this is same-day territory. Free initial call, confidential, UK based.
>
> #insolvency #companylaw

**Visual:** Split card. Left, mid blue, "What it looks like: the bank being difficult." Right, orange, "What it is: s.127 Insolvency Act 1986. Dispositions after the petition are void." Navy base.

---

### POST 10 — Tue 11 August, 08:00
**Carousel, 9 slides. Pillar: Decision Table.**

> Fourteen.
>
> That is how many UK companies used the main legal tool for rescuing a business without closing it, in the whole of June.
>
> 14 company voluntary arrangements. Down 44% on May. Against 1,364 liquidations in the same month.
>
> A CVA lets a company keep trading and repay creditors from future profits over an agreed term. It is the closest thing UK insolvency law has to a second chance for the company itself, as opposed to a sale of what is left of it.
>
> It needs 75% by value of voting creditors to approve it, under section 4(6) of the Insolvency Act 1986. That threshold is doing a lot of work in these figures.
>
> One structural reason, offered as judgement rather than data: since 1 December 2020 the Finance Act 2020 returned HMRC to preferential status for VAT, PAYE and NIC. A larger slice of any future recovery is spoken for before unsecured creditors see anything, which makes the arithmetic a CVA has to present to those creditors harder than it used to be.
>
> Whatever the cause, the effect is legible. The rescue tool is not being used.
>
> CVA against administration, side by side:
> https://www.companydebt.com/company-administration/vs-cva/
>
> Source: Insolvency Service, June 2026.
>
> #insolvency #restructuring

**Slides:**
1. Cover: `14`, orange, filling the slide. Nothing else.
2. "CVAs in June 2026. The whole month."
3. `1,364` liquidations in the same month. The contrast.
4. What a CVA is. Under 25 words.
5. `75%` by value. The threshold.
6. Crown preference, 1 December 2020. Plain English.
7. "The arithmetic got harder." (Label: editorial judgement.)
8. "The rescue tool is not being used."
9. Source + link + logo.

---

### POST 11 — Wed 12 August, 12:00
**Single image. Pillar: Data Desk.**

> Monthly company insolvencies, every month since 2000.
>
> The strangest thing on this chart is 2020.
>
> Insolvencies fell during the pandemic. Not rose. A national economy largely stopped trading and formal company failures went down, because government support was holding companies up and creditors were temporarily restricted from petitioning. The failures did not happen on the chart. They were deferred off it, and some of them arrived later.
>
> It is a useful thing to keep in view when reading any single month, including a good one. This series is not a thermometer. It is a record of when the law and the money allowed a failure to be formalised, which is not the same as when the business actually stopped working.
>
> June 2026 sits at 1,845. Read it against 26 years, not against May.
>
> The full series, monthly, back to 2000:
> https://www.companydebt.com/data/uk-insolvency-statistics/
>
> Source: Insolvency Service, June 2026.
>
> #insolvency #ukeconomy

**Visual:** The long-run line, navy base, white line, 2020 dip circled in orange and annotated "support and petition restrictions". **Regenerate `longrun_total_line.svg` on the June series first; the committed asset stops at April 2026.**

---

### POST 12 — Thu 13 August, 08:00
**Text + image. Pillar: Legal Clock.**

> A director on the payroll may be able to claim statutory redundancy when their own company closes. Most never find out, and it is often the thing that pays for the liquidation.
>
> The mechanics, plainly.
>
> If you are genuinely an employee of the company, with a contract, paid through PAYE, with at least two years' continuous service, you may qualify for statutory redundancy from the Redundancy Payments Service, funded by the National Insurance Fund. Being a director does not disqualify you. Being *only* a director, on paper, with no real employment, does.
>
> The statutory weekly cap is £751 from 6 April 2026. The maximum statutory redundancy payment is £22,530.
>
> Two honest caveats, because this gets oversold.
>
> Eligibility is assessed on the substance of the employment, not the job title, and nominal directorships get looked at closely. And no one can tell you what you will receive without looking at your service, age and pay. Anyone quoting you a figure before that has not done the work.
>
> The reason it matters is structural rather than financial. The perceived cost of doing this properly is what pushes directors toward a £10 strike-off they should not be using. A redundancy entitlement often removes that objection entirely.
>
> Eligibility and how the claim works:
> https://www.companydebt.com/director-redundancy/
>
> To check whether you qualify, speak to a licensed insolvency practitioner. Free initial call, confidential, no obligation.
>
> #insolvency #smebusiness

**Visual:** Navy. `£22,530` in orange, large. Beneath, white, smaller: "Maximum statutory redundancy. £751 per week cap from 6 April 2026." Bottom strip, mid blue: "Eligibility depends on real employment, not the title."

---

## 6. Measurement

Judge cycle 1 on these, in this order:

1. **Clicks to the data hub** — the actual objective. Referrers and journalists clicking through is the whole point.
2. **Saves and shares** — shares are the company page's structural strength, and data is what gets shared.
3. **Comment quality** — two accountants arguing about the earliest sign of distress beats forty reactions.
4. **Follower growth off 241** — slow is expected. Do not panic at week 2.

Explicitly do **not** optimise for reactions. Platform-wide, likes are down 13% and comments down 17% while overall engagement rose ~14%. The vanity metrics will look flat while the thing is working.

### The format test inside cycle 1

Five carousels, three single images, three text+image, one poll. That is enough to see whether the carousel advantage that every study reports holds on a 241-follower page. If carousels win on clicks and saves, cycle 2 goes heavier on them and drops the format experiments. If they do not, the studies were measuring accounts with audiences and we learn that early and cheaply.

---

## 7. Open items

1. **Regenerate the chart SVGs on June data.** `data/insolvency-statistics/charts/` is built from April 2026. Posts 5 and 11 depend on this. Blocking.
2. **The stats hub still shows May 2026.** The June release landed 17 July. Post 1 sends traffic to the hub, so the hub should carry June first. Blocking for post 1.
3. **Refresh the outreach claim ledger.** `outreach/companydebt-asset-catalogue.json` `approvedFigures` is pinned to May 2026, and `nextRelease` was today. Drafts citing May figures will be stale from now. Not blocking for social, but it is the same data and the same freshness problem.
4. **Cycle 2 decision: Chris Andersen.** The single highest-leverage upgrade available. A licensed IP posting this material will outperform the page posting it, and it costs him a repost.
5. **Persona file conflicts with standing rules.** `editorial-os/17-audience-and-persona.md` lists "24/7 availability" as a trust signal and "Get a Fixed-Price Liquidation Quote" as a CTA. Both are prohibited. Nothing in this calendar uses either. The persona file should be corrected at source so it stops re-seeding them.

---

## 8. Sources

- [Insolvency Service, Company Insolvency Statistics June 2026](https://www.gov.uk/government/statistics/company-insolvencies-june-2026/commentary-company-insolvency-statistics-june-2026) — every figure in this calendar
- [Company insolvency statistics releases](https://www.gov.uk/government/collections/company-insolvency-statistics-releases)
- [LinkedIn Engineering, feed dwell time](https://www.linkedin.com/blog/engineering/feed/understanding-feed-dwell-time)
- [360Brew ranking foundation model (arXiv)](https://arxiv.org/abs/2501.16450)
- [Metricool 2026 LinkedIn study, 673k posts](https://metricool.com/press-release-linkedin-study-2026/)
- [Socialinsider LinkedIn benchmarks 2026](https://www.socialinsider.io/social-media-benchmarks/linkedin)
- [Buffer, posting frequency, 2M+ posts](https://buffer.com/resources/how-often-to-post-on-linkedin/)
- Verified UK figures whitelist (internal, cross-checked against gov.uk / legislation.gov.uk)
