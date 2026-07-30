# Citation Accuracy Audit — 30 July 2026

Systematic verification of statutory and official-guidance citations across all page drafts.
**Audit pass only. No page content was edited.** Fixes go per-page through Bernstein.

---

## Scope and method

| | |
|---|---|
| Drafts scanned | 310 (`drafts/*.html`) |
| Citation instances extracted | 1,759 raw / **1,035** unique page-citations |
| Distinct provisions verified | **217** |
| Official external URLs checked | **423** |
| Verification source | legislation.gov.uk (HTTP status + `/data.xml` provision titles) |

Extraction covered running prose, tables, callouts, FAQ answers, Methodology blocks and
Sources & References blocks. Provisions were only paired with an Act where the linkage was
explicit ("s.214 of the Insolvency Act 1986", "Insolvency Act 1986 (Part II…)"), so
proximity-based false pairings are excluded.

Acts and instruments in scope: Insolvency Act 1986, Companies Act 2006 and 1985, CDDA 1986,
Insolvency (England and Wales) Rules 2016, Finance Acts 1998–2021, F(No.2)A 2015, TMA 1970,
Limitation Act 1980, ERA 1996, CIGA 2020, Enterprise Act 2002, SBEEA 2015, VATA 1994,
ITEPA 2003, Fraud Act 2006, Theft Act 1968, Pensions Act 2004, TUPE 2006, plus HMRC
factsheet codes (CC/FS*), COP codes, SIP numbers and gov.uk publication references.

### Two systemic conclusions

1. **The Finance Act 2020 Crown-preference citation is the single biggest defect.** It is
   wrong on **8 pages** across **four different fabricated or mis-attributed provisions**
   (Sch 26, Sch 28, Sch 2, Sch 9). FA 2020 has only 16 Schedules, so Sch 26 and Sch 28
   cannot exist. **The previous cleanup made this worse, not better**: it converted
   "Schedule 28" into "Schedule 26", which is equally non-existent. `79342` was recorded as
   fixed on 2026-07-30 but still cites Schedule 26.
2. **Existence checking is not enough.** Six of the fifteen findings below cite provisions
   that *do* exist but say something entirely different (F(No.2)A 2015 Part 2 is inheritance
   tax rate bands, FA 2020 s.69 is Digital Services Tax, IR 2016 Part 4 is receivership).
   A link crawler will never catch these. Any recurring gate needs a provision-title
   comparison, not just a status check.

---

## HIGH — provision does not exist

| # | Page | Cited | Verdict | Correct citation |
|---|---|---|---|---|
| 1 | `74891_secured-vs-unsecured-creditors`<br>`7665_company-rescue-solutions`<br>`77146_debt-creditor-pressure-hub`<br>`77372_company-rescue-recovery-hub`<br>`79342_hmrc-as-a-creditor-in-liquidation` | Finance Act 2020, **Schedule 26** ("Crown preference reinstatement" / "HMRC secondary preferential status from 1 December 2020") | **Does not exist.** FA 2020 has 16 Schedules. `/ukpga/2020/14/schedule/26` → 404 | **FA 2020, s.98** — "HMRC debts: priority on insolvency" |
| 2 | `77739_which-creditors-get-paid-first` | Finance Act 2020, **Schedule 28** ("HMRC secondary preferential creditor status from 1 December 2020") | **Does not exist.** 404 | **FA 2020, s.98**. Note this page *also* cites s.98 correctly elsewhere — it contradicts itself |
| 3 | `9702_receivership-mean-business` | **Part 1A** of the Insolvency Act 1986 (the small-company moratorium) | **Does not exist.** 404 | **IA 1986, Part A1** — "Moratorium" (inserted by CIGA 2020) |
| 4 | `68120_can-you-sell-your-insolvent-company` | **Section 216 of the Company Directors Disqualification Act 1986** (re-use of a prohibited name) | **Does not exist.** CDDA 1986 has no s.216 | **IA 1986, s.216** — "Restriction on re-use of company names". Prose correctly describes the offence but attributes it to the wrong Act |

## HIGH — provision exists but does not support the claim

| # | Page | Cited | What the provision actually is | Correct citation |
|---|---|---|---|---|
| 5 | `11788_frozen-bank-account`<br>`13029_understanding-hmrc-debt-collection`<br>`24434_what-is-a-freezing-order-or-injunction`<br>`67809_hmrc`<br>`77162_hmrc-enforcement-action`<br>`77205_hmrc-debt-enforcement-hub`<br>`79563_what-happens-if-hmrc-freezes-your-business-bank-account`<br>`79580_can-hmrc-shut-down-my-business`<br>`79588_what-happens-if-you-ignore-hmrc-letters`<br>`79596_what-happens-if-hmrc-rejects-your-time-to-pay-arrangement` | **F(No.2)A 2015, Part 2** for HMRC's Direct Recovery of Debts | Part 2 is **"Inheritance tax — Rate bands"**. Nothing to do with DRD | **F(No.2)A 2015, s.51 and Schedule 8** — "Enforcement by deduction from accounts" |
| 6 | `77157_construction-insolvency` | "HMRC may seek a Personal Liability Notice under **section 69 of the Finance Act 2020**, attaching personal liability to the director for the unpaid CIS deductions" | FA 2020 **s.69 is "Recovery of DST liability"** (Digital Services Tax) | Compound error. PLNs are **SSAA 1992, s.121C**, and they cover **unpaid NIC only — not CIS deductions**. There is no PLN route for CIS. This sentence needs rewriting, not just re-citing |
| 7 | `79342_hmrc-as-a-creditor-in-liquidation` | "the Finance Act 2020 (Schedule 26 reinstating HMRC secondary preferential status **and introducing Personal Liability Notices** and Joint and Several Liability Notices)" | FA 2020 did not introduce PLNs — they date from **SSAA 1992, s.121C**, 28 years earlier | Split the claim: **s.98** (secondary preference), **s.100 + Sch 13** (Joint and Several Liability), **SSAA 1992 s.121C** (PLNs) |
| 8 | `20428_vs-liquidation` | Finance Act 2020, **Schedule 2** ("Crown preference reinstatement, in force 1 December 2020") | FA 2020 Sch 2 is **"The loan charge: consequential amendments"** | **FA 2020, s.98** |
| 9 | `79498_pay-hmrc-or-suppliers-first` | Finance Act 2020, **Schedule 9** ("HMRC secondary preferential status") | FA 2020 Sch 9 is **"DST payment notices"** | **FA 2020, s.98** |

## MEDIUM — mis-attributed within the right instrument

| # | Page | Cited | Issue | Correct citation |
|---|---|---|---|---|
| 10 | `79445_list-of-liquidation-documents` | "Insolvency (England and Wales) Rules 2016, **Part 4** (statement of affairs in CVL)" | IR 2016 **Part 4 is RECEIVERSHIP** | **IR 2016, Part 6** — "Creditors' Voluntary Winding Up" |
| 11 | `79360_ccj-when-going-insolvent` | "**section 126** on stay of proceedings **in voluntary liquidation**" (repeated in the Sources block as "stay of proceedings, voluntary") | s.126 sits in **Part IV Chapter VI, "Winding Up by the Court"** — it is the compulsory track, operating between presentation of a petition and the order. The page's paired s.130 gloss ("compulsory") is correct, so the two are the wrong way round | s.126 = power to stay/restrain proceedings **after a petition is presented**; there is no automatic equivalent in voluntary liquidation |
| 12 | `7676_members-voluntary-liquidation` | "Under **section 94** of the Insolvency Act 1986, the company is then dissolved three months after that account is registered" | s.94 is **"Final account prior to dissolution"** — it governs the account and the filing, not the dissolution effect | The three-month dissolution is **IA 1986, s.201** — "Dissolution (voluntary winding up)". The s.94 reference for the final account is correct; only the dissolution effect is mis-attributed |
| 13 | `41082_can-personal-assets-of-directors-be-seized-from-a-ltd-company` | Links SSAA 1992 s.121C to `legislation.gov.uk/ukpga/1992/**4**/section/121C` (404) | 1992 c.4 is the Social Security **Contributions and Benefits** Act | s.121C is in **1992 c.5**, the Social Security **Administration** Act: `/ukpga/1992/5/section/121C` |

## LOW — verified correct, no action

These were flagged by automated checks and cleared on inspection. Recording them so a future
pass does not re-open them.

| Item | Why it is fine |
|---|---|
| **IA 1986, Part II** (9 pages: `15141`, `16106`, `65483`, `66834`, `73778`, `79295`, `79313`, `79412`, `79472`) | `/ukpga/1986/45/part/II` returns 404, but Part II **does exist** — it now contains only s.8, which gives effect to Schedule B1. The part-level URL is a legislation.gov.uk quirk for single-section Parts. The citation "Part II and Schedule B1 on administration" is substantively correct. **Do not "fix" these.** |
| **CIGA 2020 / Part 26A** (`20268_retail-industry-insolvency-trends`) | Page reads "the Restructuring Plan introduced by CIGA 2020 (Part 26A Companies Act 2006)" — correct. Part 26A is in CA 2006, inserted by CIGA 2020 |
| **IA 1986, Sch B1 para 43** (`68115_rescue-your-business-from-insolvency`) | Verified: `/schedule/B1/paragraph/43` = the administration moratorium. Correct |
| **CC/FS7a** (`11384`, `28761`) | The factsheet is real ("Penalties for inaccuracies in returns and documents"). Only the gov.uk URL is stale — see Appendix |
| **CC/FS40** | **Confirmed absent from all 310 drafts.** That cleanup is complete |
| **SIP 1, 3.1, 9, 16; COP1, COP8, COP9** | All real. SIP 3.1 (IVAs) is correctly used on the IVA page; SIP 3.2 (CVAs) correctly on the CVA page |
| **FA 2020, Sch 13** (10 pages) | Correct — "Joint and several liability of company directors etc" |
| **FA 2020, s.98** (8 pages) | Correct — "HMRC debts: priority on insolvency" |
| **"the 2021 Dissolved Companies Act"** (5 pages) | Not a real short title, but **all five pages carry the full title** (Rating (Coronavirus) and Directors Disqualification (Dissolved Companies) Act 2021) elsewhere on the page. Style point at most |
| The 190 remaining provisions | Verified to exist; inline glosses match the official provision titles. Includes the high-traffic core: IA 1986 ss.123, 175, 212, 213, 214, 216, 217, 235, 238, 239, 240, 241, 245, 423, Sch 6, Sch B1; CA 2006 ss.172, 386, 993, 1003, 1029; CDDA 1986 ss.6, 7, 7A, 9; IR 2016 Parts 14/18 and rr.14.25, 18.16 |

---

## Appendix — dead official URLs (link health, 47 URLs / 59 pages)

Adjacent to the citation brief and worth a separate remediation pass. All were re-tested with
browser headers to rule out bot-blocking, and a control set of live gov.uk URLs returned 200,
so these are genuine failures. Most are gov.uk pages that have moved rather than fabrications
— e.g. `/bailiffs` is now `/your-rights-bailiffs`, `/debt-relief-orders` is now under
`/options-for-dealing-with-your-debts`.

Two entries overlap with the findings above and should be fixed with them:
`legislation.gov.uk/ukpga/2020/14/schedule/26` (finding 1) and
`legislation.gov.uk/ukpga/1992/4/section/121C` (finding 13).

| URL | Pages | Examples |
|---|---|---|
| https://www.gov.uk/bailiffs | 4 | 10930_distraint-order-notice, 11644_notice-of-enforcement, 12958_controlled-goods-agreement, 12979_what-can-hmrc-bailiffs-take |
| https://www.gov.uk/check-if-an-insolvency-practitioner-is-authorised | 1 | 26218_business-debt-advice |
| https://www.gov.uk/complain-about-bailiffs | 1 | 77097_bailiffs-high-court-enforcement-officers |
| https://www.gov.uk/courts-tribunals/insolvency-and-companies-court | 6 | 25310_validation-order, 26234_debt-management-guide, 31237_cant-pay-a-commercial-lease-or-rent, 77097_bailiffs-high-court-enforcement-officers +2 |
| https://www.gov.uk/debt-relief-orders | 1 | 53166_i-cannot-afford-to-repay-my-debt |
| https://www.gov.uk/government/collections/hmrc-compliance-checks-factsheets | 4 | 11193_hmrc-compliance-checks, 11384_hmrc-tax-investigations, 14775_tax-penalties, 76920_hmrc-penalties-investigations |
| https://www.gov.uk/government/collections/reporting-on-payment-practices-and-performance | 1 | 49778_construction |
| https://www.gov.uk/government/news/bulb-energy-to-be-placed-into-special-administration | 1 | 49898_energy |
| https://www.gov.uk/government/organisations/hm-revenue-customs/about/our-organisation | 1 | 14158_hmrc-fraud-investigations |
| https://www.gov.uk/government/organisations/hm-revenue-customs/contact/debt-management-and-banking | 1 | 16565_hmrc-offices-contact-guide |
| https://www.gov.uk/government/organisations/redundancy-payments-service | 1 | 15010_what-happens-to-employees |
| https://www.gov.uk/government/publications/a-guide-to-the-work-of-the-official-receiver | 1 | 47550_what-is-the-insolvency-service |
| https://www.gov.uk/government/publications/accelerated-payments-and-follower-notices | 2 | 16353_hmrc-follower-notice, 67828_accelerated-payment-notices-apn |
| https://www.gov.uk/government/publications/bounce-back-loan-scheme | 1 | 43675_what-happens-if-i-default |
| https://www.gov.uk/government/publications/business-asset-disposal-relief-hs275-self-assessment-helpsheet | 1 | 78851_voluntary-liquidation |
| https://www.gov.uk/government/publications/charity-inquiry-guidance | 1 | 49906_schools |
| https://www.gov.uk/government/publications/code-of-practice-9 | 1 | 11384_hmrc-tax-investigations |
| https://www.gov.uk/government/publications/companies-house-forms | 1 | 29543_lpa-receivership |
| https://www.gov.uk/government/publications/compliance-checks-penalties-for-inaccuracies-in-returns-and-documents-ccfs7a | 2 | 11384_hmrc-tax-investigations, 28761_corporation-tax-penalties |
| https://www.gov.uk/government/publications/compulsory-liquidation-court-fees | 1 | 74390_when-a-cva-fails |
| https://www.gov.uk/government/publications/direct-recovery-of-debts | 1 | 12958_controlled-goods-agreement |
| https://www.gov.uk/government/publications/form-n293a-combined-certificate-of-judgment-and-request-for-writ-of-control | 1 | 39500_what-is-a-high-court-writ |
| https://www.gov.uk/government/publications/hmrc-code-of-practice-9 | 2 | 14158_hmrc-fraud-investigations, 14460_hmrc-criminal-investigations |
| https://www.gov.uk/government/publications/insolvency-practitioner-regulation-regulatory-objectives-and-oversight-arrangements/statements-of-insolvency-practice | 1 | 68120_can-you-sell-your-insolvent-company |
| https://www.gov.uk/government/publications/insolvency-practitioner-regulation-statements-of-insolvency-practice | 1 | 8396_pre-packs |
| https://www.gov.uk/government/publications/insolvency-practitioner-services-sip-16 | 1 | 68115_rescue-your-business-from-insolvency |
| https://www.gov.uk/government/publications/insolvency-practitioner-statements-of-insolvency-practice-sip | 1 | 20268_retail-industry-insolvency-trends |
| https://www.gov.uk/government/publications/insolvent-company-investigations-what-happens-when-a-company-is-liquidated | 1 | 7687_winding-up-petitions |
| https://www.gov.uk/government/publications/national-insurance-fund-account | 1 | 14914_director-redundancy |
| https://www.gov.uk/government/publications/report-misconduct-as-a-director-of-a-company-in-liquidation | 1 | 68387_insolvent-company-investigations |
| https://www.gov.uk/government/publications/wind-up-a-company-that-owes-you-money | 1 | 79507_what-happens-if-i-stop-paying-company-debts |
| https://www.gov.uk/guidance/breathing-space | 1 | 77681_mental-health-debt-stress-support |
| https://www.gov.uk/guidance/company-secretarial-services | 1 | 28545_personally-liabilty-of-company-secretary |
| https://www.gov.uk/guidance/insolvency-and-the-directors-of-a-limited-company | 1 | 76904_am-i-solvent |
| https://www.gov.uk/guidance/insolvency-proceedings-fees | 1 | 47550_what-is-the-insolvency-service |
| https://www.gov.uk/guidance/penalties-for-late-payment-and-interest-harmonisation | 1 | 14912_vat-penalties |
| https://www.gov.uk/guidance/register-information-about-a-receiver-for-a-company | 1 | 9702_receivership-mean-business |
| https://www.gov.uk/guidance/registering-company-charges-mortgages | 1 | 74891_secured-vs-unsecured-creditors |
| https://www.gov.uk/guidance/registration-of-charges-created-by-companies-and-limited-liability-partnerships | 1 | 68111_what-to-do-about-customer-insolvency |
| https://www.gov.uk/guidance/security-for-tax-payments | 1 | 10564_security-bond-notices |
| https://www.gov.uk/guidance/traffic-commissioners | 1 | 77161_transport-haulage-insolvency |
| https://www.gov.uk/guidance/vat-domestic-reverse-charge-procedure-hmrc-notice-735 | 1 | 77157_construction-insolvency |
| https://www.icaew.com/regulation/find-a-firm | 2 | 76323_insolvency-advice-for-directors, 79423_insolvency-checklist |
| https://www.icaew.com/regulation/insolvency/insolvency-resources/sips | 2 | 66834_what-is-a-pre-pack-administration, 8358_what-is-an-insolvency-practitioner |
| https://www.legislation.gov.uk/ukpga/1986/45/part/IV/chapter/IX | 1 | 78191_leases-and-contracts-in-liquidation |
| https://www.legislation.gov.uk/ukpga/1992/4/section/121C | 1 | 41082_can-personal-assets-of-directors-be-seized-from-a-ltd-company |
| https://www.legislation.gov.uk/ukpga/2020/14/schedule/26 | 3 | 7665_company-rescue-solutions, 77146_debt-creditor-pressure-hub, 77372_company-rescue-recovery-hub |

---

## Recommended remediation order

**19 pages** need a citation fix. Group them so related prose is touched once:

1. **FA 2020 Crown-preference family — 8 pages** (findings 1, 2, 8, 9). One correct target:
   `FA 2020, s.98`. `79342` and `77739` also need the PLN/JSL claim untangled (findings 7, 2).
2. **DRD family — 10 pages** (finding 5). One correct target:
   `F(No.2)A 2015, s.51 and Sch 8`. Two of these (`13029`, `77162`) have the wrong citation in
   running prose, not just the Sources block, so they need the humanise pass most.
3. **Single-page substantive rewrites — 4 pages** (findings 3, 4, 6, 10). Finding 6
   (`77157_construction-insolvency`) is the one where the underlying legal claim is wrong, not
   just the reference; it needs a genuine rewrite of that paragraph.
4. **Single-page reference corrections — 3 pages** (findings 11, 12, 13).
5. **Link-health pass** on the 47 dead URLs, separately from the citation work.

Every fix routes through `bernstein.js` for the page, gates on `scripts/article_audit.py`,
takes a humanise pass on Opus for any prose change, and goes to staging only.

## Suggested standing guard

The two accidental discoveries and this audit share one root cause: nothing in the pipeline
checks a citation's *content*. A `scripts/check_citations.py` guard modelled on
`check_statutory_fees.py` would close it — extract provisions on the explicit-linkage pattern
used here, resolve each against `legislation.gov.uk/<base>/<seg>/<num>/data.xml`, and fail
when a provision 404s or when the page's inline gloss shares no significant term with the
official provision title. Worth noting for the guard: single-section Parts (IA 1986 Part II)
404 at part level and must be allow-listed, or the guard will generate exactly the kind of
false "fix" that produced Schedule 26.
