# H-Tag Spec: Creditors' Voluntary Liquidation (CVL)

**Page:** `/liquidation/creditors-voluntary-liquidation/` (wp_page_id 7674)
**Page class:** `entity_owner` (overlay: `runtime-packs/overlays/entity-owner.md`)
**H-tag family:** Template 9 (Specific closure route or insolvency procedure) — CVL is named explicitly in that template's use-for list.
**Spec date:** 17 July 2026
**Registered:** 2026-07-08 (adopted existing content); this registration supersedes the 2026-07-08 Template 9 restructure note in the Bernstein stage history for factual-correction and information-gain purposes only. Section order is unchanged.

---

## Why this is a revision, not a rewrite

The page already carries 12 correctly-sequenced H2s matching Template 9's shape (at-a-glance panel, suitability table, process, requirements, costs/timelines, company debts, director risks, employees, alternatives, next steps, FAQ, related guides). The entity-patterns brief (17 July 2026, `CompanyDebt_CVL_Entity_Patterns_Assessment_and_Claude_Brief.md`) confirms this and recommends **surgical revision and factual consolidation**, not a new structure. No new H2 is added. Two small tables are added inside existing H2s to close specific information-gain and legal-precision gaps. The page must stay the same length or get shorter.

## Verified figures (source of truth — do not restate a different value)

All commercial and statutory figures below come from `data/statutory_fees.json`, extended 2026-07-17 with the non-fee facts this page also needs. The entity-patterns brief's own cost figures (£4,000–£6,000 / £4,000–£7,000) are **stale** — they predate the owner's 2026-07-15 correction to a flat fee. Use the values below, not the brief's.

| Figure | Value | Source |
|---|---|---|
| CVL practitioner fee | **£3,500 + VAT** (flat, not a range) | `data/statutory_fees.json` → `cvl_practitioner_fee`, owner-confirmed 2026-07-15 |
| CVL disbursements | £500 to £1,500 | `cvl_disbursements` |
| CVL all-in | £4,000 to £5,000 | `cvl_all_in` (derived) |
| Appointment clock | 10 to 21 days, first instruction to liquidator taking office | existing draft, Company Debt first-party range |
| Case clock (straightforward) | 6 to 12 months, appointment to dissolution | existing draft |
| Case clock (complex) | 12 to 24 months+ | existing draft |
| Statutory weekly redundancy/RPS cap | £751 (from 6 April 2026) | `statutory_weekly_pay_cap` |
| Max statutory redundancy | £22,530 | `statutory_redundancy_maximum` |
| Preferential wages limit (Schedule 6, estate ranking — NOT the RPS cap) | £800 per employee | `preferential_wages_limit` |
| Companies House filing deadline for the resolution | 15 days from the resolution | `creditor_decision_and_filing_deadlines` |
| Gazette advertisement deadline for the resolution | 14 days from the resolution | `creditor_decision_and_filing_deadlines` |
| Prohibited-name restriction | 5 years (s.216) | `prohibited_name_period_years` |
| Disqualification order length | 2 to 15 years (CDDA s.6) | `disqualification_range_years` |
| 2025 CVL count / total registered insolvencies / share | 18,525 / 23,938 / ~77% | `official_cvl_count_2025` |

## Required wording corrections (exact old → new)

Old strings quoted are from `drafts/7674_creditors-voluntary-liquidation.html` as of 2026-07-17.

1. **Wrongful trading** (opening para). Old: *"Trading while insolvent can expose directors to personal liability under section 214 of the Insolvency Act 1986."* New: continuing to trade while insolvent is not automatically wrongful trading; risk arises when a director knew or ought to have concluded there was no reasonable prospect of avoiding insolvent liquidation and did not take every step they ought to have taken to minimise creditor loss.

2. **Balance-sheet test**. Old: *"...including contingent and prospective liabilities such as personal guarantees and ongoing leases."* New: the company's own borrowing and lease obligations belong in that assessment; a director's personal guarantee is a separate personal obligation, not a company balance-sheet liability.

3. **Shareholder threshold**. Old (four instances): *"at least 75% of voting shareholders."* New: standardise to the statutory wording — at least 75% by value of the shares voted on the special resolution.

4. **Creditor procedure vs Companies House/Gazette deadlines**. The draft currently has no Companies House/Gazette deadline at all — only the 14-day creditor-notice step. Add, as a separate sentence in the process step (not merged into the creditor-notice step): the resolution is filed at Companies House within 15 days and advertised in The Gazette within 14 days; this filing/advertisement duty is separate from the creditor decision procedure described above it.

5. **Statement of Affairs**. Old: *"You prepare and swear a Statement of Affairs."* New: prepare and verify a Statement of Affairs by a statement of truth.

6. **s.210 offence**. Old: *"Inaccuracies or omissions are a criminal offence under section 210 of the Insolvency Act 1986."* New: qualify — deliberately false, misleading or non-compliant statements can carry serious consequences; the Statement of Affairs must be complete and accurate.

7. **Disbursement inconsistency**. Cost table row currently says £500–£1,000; FAQ says £500–£1,500. Fix the table row to £500–£1,500 to match the FAQ and `data/statutory_fees.json`.

8. **Director redundancy funding**. Existing "may fund some or all... where the director qualifies" phrasing is broadly fine but appears without the eligibility detail nearby in two spots (key-facts panel, alternatives table). Where it appears without the eligibility test stated in the same section, add a one-clause pointer to the eligibility test (PAYE contract, two years' continuous service) so the claim never reads as automatic entitlement in isolation.

9. **"Almost always" disqualification claim**. Old: *"the cases that produce disqualification orders almost always involve trading on after the position was clearly hopeless, BBL misuse, unrecorded director loan repayments, or active concealment."* Remove the unsupported empirical framing (`almost always`); keep the factual list of conduct that triggers scrutiny, framed as what the conduct review specifically looks for, not a proportion claim.

10. **"Majority of CVLs do not result in disqualification" claim**. Old, in the director-risks table: *"The majority of CVLs do not result in disqualification proceedings."* Remove (uncited numerical implication). Replace with the routine-review-vs-exposure distinction (new table, item 13 below) doing the reassurance work instead.

11. **£800 preferential cap vs RPS cap conflation**. Both employee-facing passages currently state the £800 preferential figure and the £751/£22,530 RPS figures in the same sentence without distinguishing the mechanism. Split explicitly: £800 is a Schedule 6 preferential-ranking cap on wage arrears *within the liquidation estate*; £751/£22,530 is the separate RPS/National Insurance Fund claim cap paid direct to the employee. State both, but as two distinct mechanisms, not one blended figure.

12. **HMRC blocking claim**. Old: *"HMRC cannot block a CVL; the decision to enter one is made by the shareholders, not creditors."* New: HMRC does not vote on the shareholders' winding-up resolution; it can exercise creditor rights in the liquidator-appointment process and continue an existing petition or enforcement action, so an advanced winding-up petition can remove practical control of timing.

13. **CVL vs compulsory "better" and "cleaner conduct report"**. Old: *"For most directors, yes... voluntary action tends to produce a cleaner conduct report than waiting for a creditor petition."* New: where both routes remain available, a CVL normally gives the director more control over timing and the proposed IP; it does not reduce the liquidator's statutory duty to review conduct, and conduct is assessed on the facts regardless of route.

## Additions (fold into existing slots — no new H2s)

14. **Jurisdiction scope box.** Add near the top, after the opening paragraphs, before the key-facts panel: a short styled callout — *"Scope: the core legal principles apply across Great Britain, but the procedure on this page follows the England and Wales rules. Scotland and Northern Ireland use different procedural rules."* Not an H2; a callout aside, matching the existing `cd-callout` pattern.

15. **2025 CVL statistic.** One sentence near the opening definition: 18,525 of the 23,938 registered company insolvencies in England and Wales in 2025 were CVLs (about 77%), and the four years to 2025 contain the four highest annual CVL totals since the series began in 1960. Cite the Insolvency Service directly.

16. **Two clocks, made explicit.** The existing "Costs and Timelines" table already carries the appointment-speed and dissolution-time rows. Add one framing sentence ahead of that table naming them as two separate clocks (appointment clock; case clock) with a one-line methodology note that the appointment-speed range is Company Debt's own first-party range, not a statutory timetable. No new table needed — reframe the existing one.

17. **Routine review vs actual personal exposure table.** New second table inside the existing "What Happens to Directors" H2, alongside (not replacing) the current risk/statutory-basis/defence table. Two columns: *Happens in Every CVL* (conduct report, books and records review, asset and transaction review, director questionnaire, cooperation duty) vs *Requires Particular Facts* (wrongful trading claim, preference claim, undervalue claim, disqualification proceedings, personal contribution order). This table is what earns back the reassurance that items 9–10 removed, without an unsupported proportion claim.

18. **SEO metadata.** Set SEO title to *"Creditors' Voluntary Liquidation (CVL): Costs, Process & Director Risks"* and meta description to *"Learn how a Creditors' Voluntary Liquidation works, what it costs, how long it takes and when directors may remain personally liable. Reviewed by a licensed insolvency practitioner."* (currently empty). The on-page H1/title text is unchanged — it is already strong; only the SEO title/meta fields are weak.

19. **Stable section IDs.** Add anchor IDs to the H2 headings for AI/search sourceability: `cvl-definition` (suitability H2, since there is no separate standalone definition H2 — the opening paragraphs plus this H2 are the definition block), `is-cvl-right`, `cvl-process`, `cvl-timeline` (on the costs/timelines H2), `cvl-cost` (same H2, id takes priority on definition slot naming — if the H2 combines cost and timeline, use `cvl-cost` as the primary id and add a `<span id="cvl-timeline">` anchor at the timelines table), `cvl-company-debts`, `cvl-director-risks`, `cvl-employees`, `cvl-alternatives`, `cvl-faq`.

## Not changed

- No new H2s. No new page. No change to the 12-H2 sequence or their order.
- The existing risk table, debt table, process step-cards, and FAQ accordion structure are kept — only the specific sentences and rows named above change.
- The "Related Guides" list, methodology aside, and sources aside keep their current structure (rule 12: not H2s).
- Review date: only one date exists in the draft (8 July 2026) and it is already consistent across the draft, the page config, and the Bernstein state file — update it to the actual date of this revision at publish time, in all three places at once.

## Gate-relevant notes

- Keep the disbursement/fee figures inside the drift-pattern regexes in `data/statutory_fees.json` — do not reintroduce £4,000–£6,000, £4,000–£7,000, or £500–£1,000-as-disbursement anywhere.
- No em dashes (house rule).
- `panelTitle` FAQ escapes must stay single-backslash (`<strong>`), not double-escaped.
- This is a `we`-density-bearing page already (practitioner "we" language present throughout); do not dilute it while making corrections — tighten wording, don't strip voice.
