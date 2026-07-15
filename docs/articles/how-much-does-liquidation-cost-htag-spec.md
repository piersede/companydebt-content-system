# H-Tag Spec: How Much Does Liquidation Cost?

**Page:** `/liquidation/how-much-does-liquidation-cost/` (wp_page_id 23698)
**Page class:** `pricing_cost` (overlay: `runtime-packs/overlays/pricing-cost.md`)
**H-tag family:** Template 7 (liquidation overview / process / costs / timelines) — procedure-led title, so the H3-heavier budget applies.
**Spec date:** 14 July 2026

---

## Verified figures (source of truth for this page)

Do not restate any fee not on this list. Do not carry a figure over from the old draft.

| Figure | Value | Source | Verified |
|---|---|---|---|
| CVL practitioner fee | £4,000 to £7,000 + VAT | Company Debt pricing (owner-confirmed 14 Jul 2026) | Human |
| CVL disbursements | £500 to £1,500 | Company Debt pricing | Human |
| CVL all-in | £5,000 to £9,000 | Derived from the two rows above | Human |
| MVL | £2,000 to £4,000 + VAT | Company Debt pricing | Human |
| Winding-up petition court fee | **£352** (was £343) | [Civil court fees EX50](https://www.gov.uk/government/publications/fees-in-the-civil-and-family-courts-main-fees-ex50/civil-court-fees-ex50), updated 13 Jul 2026 | gov.uk |
| Petition deposit | £2,600 | Insolvency Proceedings (Fees) Order 2016 as amended 2024 | legislation.gov.uk |
| Strike-off (DS01) | **£13 online / £18 paper** (was £33 and £10) | [Companies House fees](https://www.gov.uk/government/publications/companies-house-fees/companies-house-fees), updated 2 Jul 2026 | gov.uk |
| Statutory weekly redundancy cap | £751 (from 6 Apr 2026) | Employment Rights (Increase of Limits) Order 2026 | legislation.gov.uk |
| Max statutory redundancy | £22,530 | £751 x 30 | Derived |

## Removed claims (do not reinstate)

- **"Average successful director redundancy claim is £9,000 to £12,000."** Not supported by the cited gov.uk guidance. Traced to `editorial-os/17-audience-and-persona.md` and Gemini research output, not to Company Debt caseload. Owner could not stand behind it (14 Jul 2026). Replace with the statutory calculation method, the £751 cap, the £22,530 maximum, and a link to the gov.uk redundancy calculator. **Do not substitute a different average.**
- The methodology line claiming redundancy figures are "based on average outcomes through the Insolvency Service's National Insurance Fund."

## Also removed (do not reinstate)

Owner decision, 14 Jul 2026: cut both of the following unverifiable first-person claims.

- The "£600 in the company account, £11,400 redundancy claim" director case.
- The "builder's quote, except the walls are already falling down" director quote.

Do not invent replacement anecdotes or colour of this kind. Where the funding section
previously leaned on the £11,400 case, it now leads with the statutory mechanism instead:
the eligibility test (employment contract, PAYE, two years' continuous service), the £751
weekly cap, the £22,530 maximum, and a link to the gov.uk redundancy calculator.

The page keeps its practitioner voice through working detail and operational specifics,
not through invented scenes. See `runtime-packs/stages/humanise.md` Part C.

---

## H-tag structure

```
H1: How Much Does It Cost to Liquidate a Company in the UK?

[Opening answer box - styled aside, NOT an H2]
  Direct cost answer within the first screen. CVL range, VAT status,
  who normally pays, and the quote CTA. Do not claim a universal total.

H2: Liquidation Costs at a Glance
  -> Comparison table only. No H3s. (Framework: "a list of costs or fees" = no H3s)
  -> Columns: Route / Typical cost / Statutory or professional fee / Who pays first / When it applies
  -> Rows: CVL, MVL, Compulsory (creditor petition), Strike-off
  -> Keep statutory fees (court, deposit, DS01) visually separate from indicative practitioner fees.

H2: How Much Does a Creditors' Voluntary Liquidation Cost?
  H3: The CVL Fee Range for a Straightforward Company
  H3: What Pushes a CVL Above the Standard Range
  H3: VAT and Disbursements on Top of the CVL Fee
  -> H3s earned: CVL cost is the core commercial intent of this exact title.

H2: What Does a Liquidation Quote Include?
  -> Two-column table (Included in the quote / May be charged separately). No H3s.

H2: Pre-Appointment and Post-Appointment Liquidation Costs
  H3: Pre-Appointment Work and What a Fixed Quote Covers
  H3: Post-Appointment Liquidator Remuneration
  H3: How the Fee Basis Is Approved
  -> NEW SECTION. This is the largest content gap vs the SERP (Greenfield's edge).
  -> Fee basis: fixed amount / time costs / percentage of realisations / combination.
  -> Approval by creditors, committee, or court. Reference SIP 9 and Insolvency Rules 2016 Part 18.
  -> H3s earned: distinct, regulatory, title-specific, not cannibalising.

H2: What Changes the Cost of Liquidating a Company?
  -> Bold-label bullets. No H3s. (Framework: cost factors must not each become an H3.)
  -> Creditor count / Employees / Records quality / Assets and debtor book / Leases and HP /
     Director loan account / Disputed transactions / Litigation / Overseas assets

H2: Who Pays for Company Liquidation?
  -> Decision layer. Bold labels, no H3s.
  -> Separate cleanly: liquidation costs vs director's personal contribution vs
     sums the director separately owes the company. Do NOT present personal guarantees
     or an overdrawn DLA as "liquidation fees" - they are not.

H2: Director Redundancy: How Most Directors Actually Pay for a CVL
  -> MANDATORY as its own H2. Persona red line (17-audience-and-persona, Red lines):
     "treats director redundancy as a footnote rather than a primary conversion lever".
     An earlier draft demoted this to a bullet inside the section below. That is a FAIL.
     Personas 2 (Spongebob) and 5 (Windfall Researcher) both convert on this lever.
  -> Eligibility, the statutory calculation, the £751 cap, the £22,530 maximum, the
     gov.uk calculator, assignment to the practitioner. NO average figure (banned).
  -> State the hard limit plainly: dividends-only directors do not qualify.

H2: What If You Cannot Afford to Liquidate the Company?
  -> Concise. Link prominently to /liquidation/cant-afford-to-liquidate/. Do not cannibalise it.
  -> Cover the remaining routes: asset realisations, instalments, and the compulsory fallback.
  -> Overlay rule: explain feasibility, do not hide behind a contact gate.

  H3: Will HMRC Find Out If I Start Asking Questions?
    -> MANDATORY. Persona red line: "fails to address the 'I can't afford it' and
       'Will HMRC find out?' objections explicitly". The persona names this fear directly
       ("Fear of triggering HMRC... staying under the radar via strike-off is safer").
       It is the objection that keeps directors sitting on an insolvent company.
    -> Answer plainly: speaking to an IP does not notify HMRC or trigger an investigation;
       nothing is filed until the director instructs and shareholders resolve.

H2: How to Compare Liquidation Quotes
  -> Checklist. No H3s. HIGH INFORMATION GAIN - no competitor offers this.
  -> Fixed or estimated? Pre-appointment work included? What post-appointment basis
     will be proposed? VAT in or out? Which disbursements? What triggers extra charges?
     Is the DLA handled separately? What is payable before appointment?

H2: Common Liquidation Cost Misunderstandings
  -> Bold-label bullets. No H3s. Retain from current draft - genuinely distinctive.

H2: What Liquidation Costs You, and What Waiting Costs You
  -> The decision layer. REQUIRED by the pricing-cost overlay ("end with a cost-check
     decision layer") and by the voice engine ("the verdict is a compression of the real
     decision... do not end with neutral equilibrium").
  -> Compress: the all-in number, the two funding routes most directors have without
     knowing, and the price of waiting (petition, frozen account, Official Receiver,
     a conduct review by someone you did not appoint).

H2: Frequently Asked Questions About Liquidation Costs
  -> FAQ accordion. Keep only questions not fully answered in the body.

H2: Related Guides
  -> MUST be the final H2 (framework rule 8, revised 2026-07-08).
  -> Gutenberg wp:list block. 3-6 links. No bespoke card classes.

[Methodology and Disclosure + Sources]
  -> Framework rule 12: these are NOT <h2> elements. Footer module / <aside> /
     styled label (e.g. <p class="methodology-label">). Content is gate-required;
     only the wrapping element changes.
```

## Structural rules for this page

- Title tag must lead with the number: the SERP competitors all run vague "How Much Does It Cost To..." titles. The figure is the differentiator.
- No em dashes anywhere (house rule). Fix the existing broken " , " artefacts left by a previous em-dash purge (three known instances).
- British spelling and UK legal terminology.
- Google shows a Reddit/UK Business Forums discussion block at position 4 on this query. Directors go to forums because IP firms will not state a plain number. The table and the quote-comparison checklist are the direct answer to that.
- Retain the full trust package: named IP reviewer, review date, methodology, commercial disclosure, primary sources.
- Do not add prose bulk. The page is already strong. This is a surgical revision, not a rewrite.
