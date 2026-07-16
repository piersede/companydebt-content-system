# Search intent & customer journeys — companydebt.com growth audit (lens 3)

Date: 2026-07-10. Sources: GSC direct API (UK/GBR, 2026-01-06 to 2026-07-06 unless stated), Ahrefs foundation data (02), sitemap inventory (01), business-model map (04), competitor SERPs (05), plus live read-only WebFetch spot-checks of 6 pages on 2026-07-10. All monetary values GBP unless marked USD. "Verified" = fetched/queried today; "inference" flagged where used.

---

## 0. Headline finding

The site's query ladders are **strong at the top and broken at the bottom**. It captures directors early (fear, liability, "can't pay" problem queries at positions 6–14) and then disappears at exactly the point where intent turns commercial: CVL at position ~34, winding-up petition at ~35–39, MVL effectively invisible, liquidation-cost CTR 0.04%. The pages at the commercial end are, on inspection, well-built (verified below) — the deficit is *visibility of the bottom rungs*, not on-page handoff quality. Meanwhile ~40% of actual UK clicks land on pages with no journey at all (celebrity/news articles, a personal-guarantee-insurance page for a product the firm doesn't sell).

Six-month UK page-level clicks confirm the inversion (GSC, verified):

| Page | Clicks | Impressions | CTR | Pos |
|---|---|---|---|---|
| / (homepage) | 62 | 47,946 | 0.13% | 33.8 |
| /advice/personal-guarantee-insurance/ | 48 | 8,065 | 0.60% | 11.2 |
| /articles/bobby-davros-business-goes-bust/ | 34 | 2,151 | 1.58% | 6.7 |
| /articles/pub-closures-in-the-uk/ | 21 | 7,355 | 0.29% | 10.1 |
| /hmrc/cant-pay-vat/ | 18 | 11,906 | 0.15% | 13.5 |
| /liquidation/ (hub) | 17 | 61,685 | 0.03% | 22.0 |
| /liquidation/how-much-does-liquidation-cost/ | 6 | 14,026 | 0.04% | 19.6 |
| /winding-up-petitions/ | 2 | 32,559 | 0.006% | 39.2 |

The two largest impression pools on the site (/liquidation/ 61.7k, /winding-up-petitions/ 32.6k) produce 19 clicks between them in six months. That is the journey problem in one row pair.

---

## 1. Journey A — insolvent ltd director under HMRC pressure → CVL

The core revenue journey. Persona: director with VAT/PAYE/CT arrears, brown-envelope stage escalating to enforcement.

### Query ladder (GSC UK, 6 months, verified)

| Rung | Query (examples) | Impr | Pos | CTR | State |
|---|---|---|---|---|---|
| 1. Early anxiety | hmrc compliance checks / how long does a hmrc compliance check take | 438 | 11.3 | 0.46% | OK |
| | hmrc enforcement officer | 568 | 15.5 | 0.18% | OK |
| | hmrc threatening letters | 26 | 5.9 | 3.8% | Good |
| 2. Problem named | can't pay vat (+variants) | ~2,900 | 6.6–8.7 | 0.2–3.1% | **Strong** |
| | can't pay paye (+variants) | ~2,000 | 11.4–12.6 | 0.2–3.6% | OK |
| | can't pay corporation tax (+variants) | ~2,750 | 12.7–14.0 | 0.2% | Slipping (was 7.7 in the 12-mo view) |
| | not paying vat consequences | 346 | 6.6 | 0.58% | Good |
| 3. First remedy | time to pay arrangements | 1,384 | 11.6 | 0.65% | OK — best TTP performer |
| | hmrc time to pay corporation tax | 114 | 16.8 | 0.9% | Weak |
| 4. Crisis | hmrc winding up petition | 1,690 | 21.3 | 0.06% | **Broken** |
| | winding up petition | 3,913 | 35.6 | 0.03% | **Broken** |
| 5. Transaction | creditors voluntary liquidation | 4,910 | 33.8 | 0.04% | **Broken** |
| | company liquidation | 4,921 | 19.9 | 0.28% | Striking distance |
| | how much does liquidation cost (page-level) | 14,026 | 19.6 | 0.04% | **Broken** |
| | cheapest way to liquidate a company | 123 | 20.4 | 0.8% | Broken |

Rungs 1–3 rank; rungs 4–5 don't. The site walks the director from anxiety to remedy, then hands them to Begbies/RBR/Clarke Bell at the moment they're ready to instruct. Competitor evidence (foundation 05): CVL SERP is won by DR-22–25 firms with under 16 referring domains — this is a coverage/relevance problem, not authority.

### On-page handoff quality (verified live, /hmrc/cant-pay-vat/)

This page is genuinely good and should be treated as the template, not a fix target:
- "Work out your position in 30 seconds" self-triage (pay in 15 days? afford instalments? other debts overdue?)
- staged penalty timeline table; enforcement escalation sequence
- an options comparison table (TTP / CVA / liquidation / administration) with fit criteria
- escape-route links framed as progression (TTP → CVA → CVL), form at the bottom, phone throughout.

No sales-led drift; the decision frameworks carry the reader to the enquiry naturally. **The problem in journey A is not the handoff — it is that the pages the handoff points to (CVL, winding-up petition, cost) don't rank, so most journeys never start on companydebt.com at the rung where competitors intercept.**

### Break points

1. **Winding-up petition cluster is thin and mis-shaped.** Only 3 URLs for the highest-urgency commercial topic (inventory 01). The main page (verified) is ~4,000 words, written for a director recipient (right choice) but with *no stage triage*: statutory-demand-received (21 days), petition-served (7–14 days to hearing), petition-advertised (bank freeze in ~24h) are conflated in one linear read. A panicking director on a phone (55% of clicks are mobile, Lighthouse ~38) must read 4,000 words to find their branch. Position 39 on its own head term.
2. **CVL invisibility.** "creditors voluntary liquidation" 4,910 impressions at pos 33.8 with 2 clicks. The CVL page recently had its H-tags restructured (repo 06) — worth checking whether that shipped before or during this window — but the SERP evidence says the page needs the same treatment that won the cant-pay cluster: match the "what it costs / how long / what happens to me" intent in the first screen, not the statutory definition.
3. **Cost page CTR collapse.** 14,026 impressions, 6 clicks. Verified: figures are excellent and front-loaded (£4,000–£7,000 +VAT in paragraph one, redundancy-funding route, "can't afford it" fallback). At pos 19.6 nothing on-page fixes this; it needs the position-12→top-10 push (GSC 12-month data has it at 10.9–14.7 on some variants — it has *slipped* within the audit window; inference: the Sep–Oct 2025 impression cliff plus AI Overviews absorbing the "how much" answer).

---

## 2. Journey B — solvent closure → MVL

Persona: director/contractor with retained profits, price-shopping a tax-efficient exit. Second-highest-value journey (MVL £3,000–£5,000 +VAT, published).

### Query ladder — mostly missing

| Rung | Query | Impr (6mo UK) | Pos | State |
|---|---|---|---|---|
| 1. Decision | how to close a limited company | 1,130 | 32.7 | **Broken** |
| | best way to close a limited company | 1 | 34 | Absent |
| | cheapest way to close a limited company | (12-mo data: pos 14.2) | — | Striking distance |
| 2. Route comparison | strike off and dissolve a company | 63 | 11.1 | OK-ish |
| | apply to strike off and dissolve a company | 167 | 15.1 | Near miss |
| | advantages of members voluntary liquidation | 28 | 25.7 | Broken |
| 3. Transaction | members voluntary liquidation | — | absent from GB top-100 (Ahrefs) | **Invisible** |
| | accountants' guide to mvl and badr | 2 | 46 | Absent |

GSC returns essentially **zero MVL-branded impressions** in six months. Ahrefs confirms: MVL (994/mo, KD 1) is won by Clarke Bell at #4 with DR 22 and 10 referring domains. This is the single clearest "coverage, not authority" gap on the site.

### On-page reality (verified live, /liquidation/members-voluntary-liquidation/)

The page is commercially complete: £25,000 reserves threshold as the strike-off/MVL breakeven, BADR eligibility rules (5%/2yr/officer), the £17,750 worked saving on £100k reserves, Get a Quote button, free MVL assessment, timescales (initial distribution within weeks; 6–12 months overall). Pricing sits in section 5 — late for a price-shopper, but the page is not the constraint. **The constraint is that the ladder above it doesn't exist**: no page owns "how to close a limited company" (1,130 impressions going begging at pos 32.7), no dedicated "MVL vs strike-off" decision page, no MVL cost/tax-saving calculator to earn the comparison-stage click. Begbies' single best content asset is exactly this rung ("how to close a company with no money", ~$8.3k/mo value, 157 keywords) — proof the decision-stage query is where this market's traffic concentrates.

### Where the user leaves to compare

MVL is the one journey where comparison-shopping is certain (solvent, unhurried, price-sensitive). companydebt.com publishes fees — rare in this sector and its best comparison-stage weapon — but the Get a Quote path gives no instant number, while competitors advertise fixed prices on the button. With ~9 visible reviews on money pages (04) against a 5-star homepage widget, the site is weakest at exactly the trust-comparison moment. Fix order: (a) decision-stage content to get into the consideration set at all; (b) instant-quote/calculator to shorten the compare-loop; (c) surface review volume on money pages.

---

## 3. Journey C — personal-fear distress ("will I lose my house") → advice → enquiry

Persona: director googling at midnight about personal exposure. This is the site's **current de facto acquisition engine** — the top-clicked genuine pages are all in this cluster.

### Query ladder (verified, healthy at top)

| Query | Impr | Pos | CTR |
|---|---|---|---|
| personal guarantee insurance (+7 variants) | ~4,700 | 6.0–11.6 | 0.5–1.6% |
| if my ltd company goes bust will i lose my house | 901 | 9.1 | 0.33% |
| personal guarantee loopholes (+uk) | 974 | 10.5–10.6 | 0.25–1.2% |
| are directors liable for company debts (family of ~10 variants) | ~1,200 | 17–33 | ~0.1% |
| my husband signed a personal guarantee | 37 | 12.1 | 2.7% |
| trading while insolvent | 872 | 19.9 | 0.11% |

### Break points (verified live, /advice/losing-house-if-company-goes-bust/)

- **Answer speed is excellent** (fear named and answered in two paragraphs) but **self-triage is absent**: no "did you sign a PG? / is the loan account overdrawn? / is the house jointly owned?" branching. The four risk scenarios are listed, not asked.
- **CTA mismatch:** a "Get a Quote" button mid-article on a fear page — a quote for what? The reader hasn't decided to close anything. The right ask here is the confidential conversation ("talk through your guarantee exposure"), which the page only reaches at the end.
- **The personal guarantees guide is referenced but not hyperlinked** in the visible flow — a literal missing rung inside the site's strongest cluster.
- **The PG-insurance anomaly:** /advice/personal-guarantee-insurance/ is the most-clicked real page (48 clicks/6mo, pos 11.2) for a product Company Debt does not sell and (04) carries no affiliate links. As it stands it is high-intent traffic with no journey. Options: an honest editorial handoff ("insurance protects future guarantees; if you're worried about one you've already signed, that's a different conversation — ours") which fits the Which?-style voice, or a vetted-broker referral if commercially acceptable. Currently it just answers and stops.
- **Liability long-tail ranks 17–33** ("are directors of limited company liable for debts" 274 impr pos 23) despite the recent director-liability refresh (06) — the refresh may not yet have consolidated the ~10 query variants; check which URLs those variants land on (probable cannibalisation between /advice/are-directors-personally-liable…, /insolvency/shareholders-liable…, and /insolvency/personal-liability-spouses…).

### What works and should be copied

The cease-trading page (verified) is the best handoff on the site: explicit solvent/insolvent branch, a Route / When it fits / What it surrenders / Director risk table, "decide within weeks, not months" framing, and an ending that names the next step. It converts a definitional query ("ceased trading meaning", ~5,800 impr at pos 4.3–4.4) into a routed decision. This pattern — branch, table, named next step — is the house style at its best and is exactly what journeys A's petition page and C's fear pages lack.

---

## 4. Journey D — creditor-side and referrer journeys (unserved)

- **Creditors**: all winding-up-petition content is written for the recipient director. "how to issue a winding up petition" (35 impr, pos 17.8, 1 click) shows latent demand the site half-catches with no page purpose-built for it. Creditor work is real revenue for IP firms; even if out of scope commercially, a single "I'm owed money by an insolvent company" page would also catch "bringing a claim against a company in liquidation" (124 impr, pos 57) and "i owe money to a dissolved company"-type inversions.
- **Accountants/advisors**: "accountants insolvency support" (33 impr, pos 50), "accountant insolvency referral" (5 impr, pos 35), "accountants' guide to mvl and badr" (2 impr, pos 46). No partner/referrer landing page exists (04). For MVL specifically, accountants are the natural referral channel and the £25k/BADR content already speaks their language.

Both are deliberate-scope questions for the operator, but the query data says the doors are being knocked on.

---

## 5. Cross-journey structural findings

### 5.1 Dead ends (traffic with no journey)
- Celebrity/news articles: Bobby Davro (34 clicks, #2 real page), Orla Kiely (8), wine scammers (9), Wayne Rooney, Rivington Biscuits, USC — none has a conversion-relevant next step, and their readers aren't directors. They pad E-E-A-T/freshness at best. Contrast: pub-closures (21 clicks) *was* given journey blocks in the redesign and is the model for the few worth keeping.
- /insolvency/personally-liabilty-of-company-secretary/ (typo slug) earns 9 clicks at pos 31 — real demand for company-secretary liability, currently served by a defective URL.
- /county-court-judgements/ 17,397 impr, 3 clicks, pos 27.4 — CCJ-against-my-company is a rung-2 distress query that should feed journey A; page needs the cant-pay treatment.
- /what-is-a-pre-pack-administration/ 14,664 impr, 6 clicks, pos 29.5 — same.

### 5.2 Forms and capture
- The 4-field unqualified form appears at the bottom of every page — fine placement, but it is the *only* capture on most pages and qualifies nothing.
- The 30-Second Test is the only qualified capture and the sidebar buries it; its output is generic (04) rather than route-specific. It asks for contact details before results, which is a fair trade at crisis intent but a hard gate for journey-B price-shoppers.
- No journey-specific capture exists: no MVL instant quote, no petition-deadline triage, no PG-exposure check. Each maps to an existing high-traffic entry with an obvious tool shape.
- The ungated Stressed Directors Guide means no email nurture for the (majority) of visitors not ready to call — journey A directors often lurk for weeks between rung 2 and rung 4.

### 5.3 Where forms appear too early
Only one instance found: Get a Quote mid-article on fear pages (5.1 above / journey C). Money pages sequence CTAs correctly (educate → compare → quote → form).

### 5.4 Missing decision frameworks (site-wide)
1. **Interactive closure-route triage.** The /liquidation/ hub (verified) has two good comparison tables but reads as hybrid hub/encyclopedia; the branching logic exists in prose only. The 30-Second Test could *become* this: solvent branch → strike-off vs MVL (with the £25k rule); insolvent branch → CVL/CVA/TTP by creditor pressure. All the logic already exists on static pages.
2. **MVL vs strike-off tax calculator** — inputs: reserves, BADR eligibility; output: saving vs dividend/strike-off and a fixed-quote handoff. The £17,750 worked example proves the content is signed off; a calculator makes it linkable (journalists/accountants) and captures the comparison click.
3. **Petition stage triage** — three-branch entry at the top of /winding-up-petitions/ (received demand / served / advertised) each with deadline, consequence, and the one action to take today.
4. **Cost comparison table** on the cost page — currently prose-only (verified); a route × fee × who-pays × timeline grid is also the AI-Overview-citable format.

### 5.5 Voice constraint respected
None of the above requires sales-led copy. The house pattern that already works (cant-pay-vat, cease-trading) is: name the reader's position, give the branch logic honestly (including the routes that don't involve paying Company Debt — TTP first on the TTP page, strike-off when reserves are under £25k), and put the confidential-conversation ask at the decision point, not before. The fixes are mostly *adding rungs and triage*, not changing tone. The one editorial-integrity watch-item: an MVL instant-quote flow must keep the "strike-off is cheaper below £25k" steer intact, or it stops being Which?-style.

---

## 6. Recommendations (ranked)

1. **Rebuild the crisis end of journey A: winding-up petition cluster.** Expand from 3 pages to a stage-triaged set (statutory demand received / petition served / petition advertised / frozen bank account), add the three-branch triage block at the top of the main page, and internally link every rung-2 HMRC page's escalation table to the matching stage page. Target: "winding up petition" (3,913 impr, pos 35.6) and "hmrc winding up petition" (1,690, pos 21.3). SERP incumbents are DR 3–22 (05).
2. **Build the solvent-closure decision layer.** One master "How to close a limited company" guide (1,130 impr at pos 32.7 today) with the solvent/insolvent, debts/no-debts, over/under-£25k branch; a dedicated MVL-vs-strike-off comparison page; an MVL tax-saving calculator feeding the existing Get a Quote. This is the Begbies playbook applied to the site's most invisible high-value journey, and it gives accountants something to cite.
3. **Get CVL and the cost page back to page one.** Diagnose /liquidation/creditors-voluntary-liquidation/ against the cant-pay pattern (first-screen intent match: cost, timeline, what happens to me), consolidate the liability-variant cannibalisation, and treat the /liquidation/ hub's 61.7k impressions at 0.03% CTR as the single biggest CTR-recovery pool (title/meta sharpened for urgent intent, per the GSC finding that urgent queries still click while definitional ones are AI-absorbed).
4. **Convert the fear cluster from answers into journeys.** Add PG/loan-account/joint-ownership self-triage checklists to losing-house and PG pages; replace mid-article Get a Quote with a "talk through your exposure" ask; hyperlink the PG guide; decide the PG-insurance page's handoff (editorial bridge to exposure advice, or vetted referral). ~100 clicks/6mo already land here — the cheapest conversions available.
5. **Route-specific capture.** Fork the 30-Second Test output by branch (solvent → MVL/strike-off result page; insolvent → CVL/TTP result page) and gate the Stressed Directors Guide with an optional email for a short nurture sequence aimed at the rung-2-to-rung-4 lurker gap.
6. **Stop-loss the dead ends.** Add pub-closures-style journey blocks to the 3–4 news/celebrity pages that genuinely earn clicks (Bobby Davro, Orla Kiely, wine scammers); fix the company-secretary typo slug via Quick Redirects; give /county-court-judgements/ and pre-pack pages the cant-pay decision-framework treatment.
7. **(Scope decision) Open the accountant-referrer door.** A single MVL/BADR partner page for accountants would compound with rec 2's calculator. Creditor-side is a bigger strategic call; the data shows demand but it changes the site's persona.

File written by intent-journeys lens agent, growth audit 2026-07-10.
