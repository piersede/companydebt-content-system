# Cold-jargon audit: technical terms used before they are explained

**Date:** 2026-07-29  
**Scope:** all 308 `*.html` files in `drafts/` (editorial source of truth). Staging and live untouched.  
**Status:** audit only. No page content was edited. Fixes must go per-page through the Bernstein pipeline with a humanise pass on Opus.

## Why this audit exists

`drafts/7687_winding-up-petitions.html` passed `article_audit.py` at 25/25 and still failed its reader: fifteen technical terms appeared before any plain-English explanation, two of them in the opening paragraph ("advertisement" and "the Gazette"). The gate does not measure whether a stressed director can follow the sentence. This audit checks whether that failure is systemic.

**It is systemic.** 299 of 308 pages carry at least one cold term. 1671 findings in total: 198 HIGH, 531 MEDIUM, 942 LOW.

## Method

For each page: HTML comments, `<script>`/`<style>`, the `cd-sources` block and legislation/Gazette link anchor text were removed, then tags were stripped to running text. For each term, the first occurrence in prose, tables, callouts or FAQ answers was located and the surrounding window (-120 to +400 characters) was searched for a plain-English gloss: ordinary words a non-specialist would understand. A statutory cross-reference is not a gloss ("under section 127" does not explain a disposition). Where a gloss was found at first use, the term is not reported at all.

Severity:

- **HIGH** - the term is load-bearing for the page's main argument (it is in the page's own subject matter), or its first use is in the opening ~1,800 characters (hero, summary callout) or inside a decision table, and no explanation appears anywhere on the page.
- **MEDIUM** - unexplained in body prose, used more than once, or explained somewhere on the page but only *after* the reader has already met it cold.
- **LOW** - a single passing use, or first use inside an FAQ answer where the question carries the context.

Caveats, so the numbers are read honestly:

- Gloss detection is pattern-based. It recognises the phrasings the corpus actually uses; a genuinely novel explanation could be missed. Spot-checking against the fixed 7687 page cleared every term that page now explains (Gazette, advertised, statutory demand, disposition, winding-up order, Official Receiver, validation order), which is the intended behaviour.
- "Time to Pay" is discounted one severity level where it is not the page's subject: the words themselves carry most of the meaning. "TTP" used bare is not discounted.
- `IP` shows a large MEDIUM count rather than HIGH because nearly every page does expand "insolvency practitioner" somewhere. The failure is ordering, not omission: the reader meets `IP` first.
- Full row-level detail for all three severities is in the companion CSV: `cold-jargon-audit-2026-07-29.csv`.

## Terms unexplained across many pages

These are the house-definition candidates. Writing one agreed plain-English sentence for each and using it consistently at first mention is a better fix than re-deciding the wording on 299 separate pages.

| Term | Pages affected | of which HIGH | What the reader needs at first mention |
|---|---:|---:|---|
| wrongful trading | 156 | 21 | Carrying on trading after the point where you knew, or should have known, there was no realistic prospect of avoiding insolvency. It can make a director personally liable. |
| CVL | 118 | 19 | Creditors' Voluntary Liquidation - the directors choose to close an insolvent company, and the creditors have a say in who runs it. |
| IP (insolvency practitioner) | 116 | 0 | Insolvency practitioner - the licensed professional legally allowed to run a formal insolvency. Never use the bare initials first. |
| Time to Pay | 112 | 11 | An instalment plan with HMRC: you pay the tax off over months instead of in one go. |
| preference (unlawful) | 109 | 11 | Paying one creditor ahead of the others when the company was already in trouble. A liquidator can undo it and pursue the director. |
| CVA | 93 | 6 | Company Voluntary Arrangement - a deal to pay creditors part of what they are owed over time, while the company keeps trading. |
| misfeasance | 85 | 13 | A director misusing company money or breaking a duty owed to the company. The liquidator can sue personally to get it back. |
| advertised / advertisement (notice sense) | 78 | 14 | Nothing to do with marketing: it means a formal legal notice published in the Gazette so anyone can see it. |
| moratorium | 75 | 9 | A legal pause. Creditors cannot chase the company or take it to court while it lasts. |
| preferential debt / creditor | 65 | 9 | Debts that get paid before the ordinary ones when the money is shared out - mainly wages, holiday pay and some HMRC taxes. |
| the Gazette | 63 | 16 | The government's official journal of public notices. It is free, and anyone (including your bank) can search it. |
| transaction at an undervalue | 62 | 2 | Selling or transferring something for much less than it was worth, or for nothing. A liquidator can reverse it. |
| Official Receiver | 59 | 3 | A civil servant and officer of the court who takes control of the company when the court winds it up. |
| statutory demand | 58 | 6 | A formal written demand for payment. Ignore it for 21 days and the creditor can petition to wind the company up. |
| Schedule B1 | 56 | 7 | The part of the Insolvency Act 1986 that sets out how administration works. |
| floating charge | 41 | 5 | Security that sits over assets that keep changing - stock, cash, unpaid invoices - rather than one fixed item. |
| served / service | 33 | 9 | Formally delivered, usually to the registered office, so the law treats you as having received it. |
| presented (vs served) | 31 | 3 | Presented = filed at court. Served = delivered to you. The clock in law runs from presentation, which can be days before you know. |
| Schedule 6 | 31 | 6 | The part of the Insolvency Act 1986 that lists which debts get paid ahead of the rest. |
| winding-up order (vs petition) | 29 | 0 | The petition is the request. The order is the court's decision to close the company. They are days or weeks apart. |
| National Insurance Fund | 26 | 4 | The government fund that pays employees their arrears, redundancy and notice pay when the employer cannot. |
| officeholder / office-holder | 24 | 3 | Whichever licensed practitioner has been appointed - liquidator, administrator or supervisor. Name the role instead. |
| MVL | 22 | 5 | Members' Voluntary Liquidation - closing a solvent company that can pay everyone in full. |
| disposition | 20 | 2 | Any payment out, transfer or sale of company property. After a petition, these are void unless the court says otherwise. |
| Redundancy Payments Service | 20 | 1 | The government service that pays statutory redundancy when an insolvent employer cannot. |
| debenture | 18 | 5 | The legal document that gives a lender a claim over the company's assets if it cannot repay. |
| distraint / distrain | 17 | 2 | Enforcement agents taking goods from your premises and selling them to clear a debt. |
| IVA | 14 | 0 | Individual Voluntary Arrangement - the personal equivalent of a CVA, for an individual's own debts. |
| validation order | 14 | 1 | The court's permission to keep making specific payments (wages, suppliers) while a petition is live. |
| execution (enforcement sense) | 7 | 0 | A creditor enforcing a court judgment, typically by sending enforcement agents to take goods. |
| restrain / restraining advertisement | 6 | 3 | A court order stopping the petition being published in the Gazette, which is what triggers the bank freeze. |
| adjournment / adjourn | 5 | 1 | Postponing the hearing to a later date. |

Terms found on fewer than five pages each (fix in place, no house definition needed): rescind / rescission (3), substitution (of petitioner) (3), CRAR (1), sealed / court-stamped (1).

## Worst offenders

Ranked by 3x HIGH + MEDIUM + 2x load-bearing-and-never-explained.

| # | Page | HIGH | MED | LOW | Why it needs work most |
|---:|---|---:|---:|---:|---|
| 1 | `67438_dealing-with-an-hmrc-winding-up-petition.html` | 8 | 3 | 5 | never defines its own subject vocabulary: served / service, adjournment / adjourn; first cold term lands in the opening |
| 2 | `79322_winding-up-petition-vs-compulsory-liquidation.html` | 7 | 3 | 2 | never defines its own subject vocabulary: presented (vs served), CVL, served / service; first cold term lands in the opening |
| 3 | `8324_cant-pay-paye.html` | 5 | 2 | 0 | never defines its own subject vocabulary: Time to Pay; first cold term lands in the opening |
| 4 | `68134_creditor-negotiations.html` | 4 | 3 | 10 | never defines its own subject vocabulary: preferential debt / creditor |
| 5 | `79342_hmrc-as-a-creditor-in-liquidation.html` | 4 | 1 | 7 | never defines its own subject vocabulary: preferential debt / creditor, CVL; first cold term lands in the opening |
| 6 | `79379_business-bank-account-in-liquidation.html` | 3 | 8 | 5 | opens cold on advertised / advertisement (notice sense), the Gazette, presented (vs served) |
| 7 | `15010_what-happens-to-employees.html` | 3 | 3 | 1 | never defines its own subject vocabulary: National Insurance Fund, Schedule 6; first cold term lands in the opening |
| 8 | `65483_company-administration.html` | 4 | 2 | 8 | never defines its own subject vocabulary: Schedule B1; first cold term lands in the opening |
| 9 | `7669_liquidation.html` | 3 | 7 | 6 | sustained unexplained vocabulary through the body: served / service, Redundancy Payments Service, moratorium |
| 10 | `7674_creditors-voluntary-liquidation.html` | 2 | 10 | 3 | sustained unexplained vocabulary through the body: misfeasance, moratorium |

## Ranked findings (HIGH)

All 198 HIGH findings, grouped by page, worst pages first. `gloss?` = does any plain-English explanation of the term appear anywhere on the page.

| Page | Term | First-use context | Gloss anywhere? | Why HIGH |
|---|---|---|---|---|
| `67438_dealing-with-an-hmrc-winding-up-petition.html` | advertised / advertisement (notice sense) | . From the day the petition is served, you have roughly seven days before HMRC can advertise it in the London Gazette. O... | **no** | opening/hero |
| `67438_dealing-with-an-hmrc-winding-up-petition.html` | the Gazette | e day the petition is served, you have roughly seven days before HMRC can advertise it in the London Gazette. Once that ... | **no** | opening/hero |
| `67438_dealing-with-an-hmrc-winding-up-petition.html` | Official Receiver | tcome, if granted, is compulsory liquidation and the immediate transfer of control to the Official Receiver. When an HMR... | **no** | opening/hero |
| `67438_dealing-with-an-hmrc-winding-up-petition.html` | statutory demand | very steps have failed. Those earlier steps usually include a Time to Pay rejection, a statutory demand, distraint, or a... | **no** | opening/hero |
| `67438_dealing-with-an-hmrc-winding-up-petition.html` | distraint / distrain | iled. Those earlier steps usually include a Time to Pay rejection, a statutory demand, distraint, or a visit from field-... | **no** | opening/hero |
| `67438_dealing-with-an-hmrc-winding-up-petition.html` | preference (unlawful) | ollectors. PAYE, VAT and Corporation Tax arrears trigger the most petitions. Crown preference, reinstated on 1 December ... | **no** | opening/hero |
| `67438_dealing-with-an-hmrc-winding-up-petition.html` | served / service | der Schedule B1 paragraph 22. Can You Stop an HMRC Winding Up Petition Once It Has Been Served? Legal Position on Stoppi... | **no** | page subject |
| `67438_dealing-with-an-hmrc-winding-up-petition.html` | adjournment / adjourn | of why the previous default will not repeat. Where granted, the petition is typically adjourned, not withdrawn, and reac... | **no** | page subject |
| `79322_winding-up-petition-vs-compulsory-liquidation.html` | disposition | of the Insolvency Act 1986 is why banks act. If the court later makes a winding-up order, dispositions of company proper... | **no** | opening/hero, decision table/callout |
| `79322_winding-up-petition-vs-compulsory-liquidation.html` | presented (vs served) | er makes a winding-up order, dispositions of company property made after the petition was presented can be void unless t... | **no** | page subject, opening/hero, decision table/callout |
| `79322_winding-up-petition-vs-compulsory-liquidation.html` | the Gazette | he petition was presented can be void unless the court validates them. Banks that pick up the Gazette notice commonly re... | **no** | opening/hero, decision table/callout |
| `79322_winding-up-petition-vs-compulsory-liquidation.html` | advertised / advertisement (notice sense) | opportunity to act, but the bank freeze can cut that window short the moment the Gazette advertisement is published. Dir... | **no** | opening/hero, decision table/callout |
| `79322_winding-up-petition-vs-compulsory-liquidation.html` | CVL | ng the petition Can you stop it? Yes: pay the debt, negotiate, dispute, or convert to CVL Extremely difficult: requires ... | **no** | page subject, decision table/callout |
| `79322_winding-up-petition-vs-compulsory-liquidation.html` | served / service | ry demand or a county court judgement that has not been paid. The petition must be served on the company at its register... | **no** | page subject |
| `79322_winding-up-petition-vs-compulsory-liquidation.html` | restrain / restraining advertisement | Directors who receive a petition can use these 7 days to pay the debt, obtain a restraining order, or begin CVL proceedi... | **no** | decision table/callout |
| `8324_cant-pay-paye.html` | served / service | k Answer: What to Do When You Cannot Pay PAYE Call HMRC's Business Payment Support Service on 0300 200 3835 immediately.... | **no** | opening/hero |
| `8324_cant-pay-paye.html` | Time to Pay | Call HMRC's Business Payment Support Service on 0300 200 3835 immediately. Request a Time to Pay arrangement. PAYE is du... | **no** | page subject, opening/hero |
| `8324_cant-pay-paye.html` | statutory demand | y instruct enforcement agents (bailiffs) under Taking Control of Goods powers, or serve a statutory demand for debts ove... | **no** | decision table/callout |
| `8324_cant-pay-paye.html` | advertised / advertisement (notice sense) | referrals as early as 3 months in. Months 6 and beyond Winding-up petition filed and advertised in the London Gazette. Y... | **no** | decision table/callout |
| `8324_cant-pay-paye.html` | the Gazette | arly as 3 months in. Months 6 and beyond Winding-up petition filed and advertised in the London Gazette. Your bank freez... | **no** | decision table/callout |
| `68134_creditor-negotiations.html` | preferential debt / creditor | ment freeze needed; rescue or sale possible. Outcome ranked under preferential and non-preferential creditor priority. A... | **no** | page subject, decision table/callout |
| `68134_creditor-negotiations.html` | Schedule 6 | VL Underlying business non-viable; controlled wind-down preferred. Distribution under Schedule 6; unsecured creditors of... | **no** | decision table/callout |
| `68134_creditor-negotiations.html` | MVL | ution under Schedule 6; unsecured creditors often single-digit pence. CVL guide MVL Solvent surplus available; tax-effic... | **no** | decision table/callout |
| `68134_creditor-negotiations.html` | wrongful trading | Risk Why It Matters During Negotiations What Directors Should Do Wrongful trading (s.214 IA 1986) Negotiating while plai... | **no** | decision table/callout |
| `79342_hmrc-as-a-creditor-in-liquidation.html` | preferential debt / creditor | istribution and the conduct review. The Finance Act 2020 restored HMRC's secondary preferential creditor status for "tru... | **no** | page subject, opening/hero |
| `79342_hmrc-as-a-creditor-in-liquidation.html` | floating charge | YE, employee NIC, and CIS withholdings; which means HMRC now collects ahead of the bank's floating charge and well ahead... | **no** | opening/hero |
| `79342_hmrc-as-a-creditor-in-liquidation.html` | CVA | hanged the distribution outcome on most insolvent SME estates and made HMRC's vote at any CVA or creditor decision proce... | **no** | opening/hero |
| `79342_hmrc-as-a-creditor-in-liquidation.html` | CVL | floating charge holders for owner-managed companies, lost recovery share. Where a typical CVL might previously have paid... | **no** | page subject |
| `79379_business-bank-account-in-liquidation.html` | advertised / advertisement (notice sense) | Once a winding-up petition is advertised in the London Gazette, banks that become aware of it commonly freeze the compan... | **no** | opening/hero |
| `79379_business-bank-account-in-liquidation.html` | the Gazette | Once a winding-up petition is advertised in the London Gazette, banks that become aware of it commonly freeze the compan... | **no** | opening/hero |
| `79379_business-bank-account-in-liquidation.html` | presented (vs served) | he company account. How quickly that happens varies. Outflows made after the petition was presented are potentially void... | **no** | opening/hero |
| `15010_what-happens-to-employees.html` | National Insurance Fund | ncy law gives employees of insolvent employers a statutory safety net: claims against the National Insurance Fund for un... | **no** | page subject, opening/hero |
| `15010_what-happens-to-employees.html` | wrongful trading | lvent grows the creditor pool, shrinks the recoverable assets, and pushes you closer to a wrongful trading claim under s... | **no** | opening/hero |
| `15010_what-happens-to-employees.html` | Schedule 6 | claim form. Preferential Creditor Status for Employees in Liquidation Under Schedule 6 of the Insolvency Act 1986, emplo... | **no** | page subject |
| `65483_company-administration.html` | Schedule B1 | Administration at a Glance What it is: a formal insolvency process under Part II and Schedule B1 of the Insolvency Act 1... | **no** | page subject, opening/hero, decision table/callout |
| `65483_company-administration.html` | floating charge | on in practice. Used when the directors decide rescue is the right call. Qualifying floating charge holder The lender (t... | **no** | decision table/callout |
| `65483_company-administration.html` | debenture | Qualifying floating charge holder The lender (typically a bank with an all-assets debenture) appoints directly out of co... | **no** | decision table/callout |
| `65483_company-administration.html` | Official Receiver | sory liquidation A creditor has already petitioned the court. Director loses control; Official Receiver runs the case. C... | **no** | decision table/callout |
| `7669_liquidation.html` | served / service | y route What to do next You cannot pay your debts, but no winding-up petition has been served CVL Take advice before you... | **no** | decision table/callout |
| `7669_liquidation.html` | Redundancy Payments Service | he full CVL fee in many cases Statutory weekly cap £751 from 6 April 2026. Funded by the Redundancy Payments Service, no... | **no** | decision table/callout |
| `7669_liquidation.html` | moratorium | ontrol; business may continue to trade; a sale or restructuring plan follows. Statutory moratorium pauses creditor actio... | **no** | decision table/callout |
| `7674_creditors-voluntary-liquidation.html` | misfeasance | reasonably be avoided, and what steps were then taken to minimise creditor losses. Misfeasance Section 212 IA 1986 Keep ... | **no** | decision table/callout |
| `7674_creditors-voluntary-liquidation.html` | moratorium | y under supervision. CVA guide Administration Business has rescuable value or moratorium needed urgently. Administrator ... | **no** | decision table/callout |
| `79295_company-voluntary-arrangement-vs-administration-which-to-choose.html` | moratorium | appoints a professional to manage the company's affairs, and buys time under a statutory moratorium. A CVA is a negotiat... | **no** | page subject, opening/hero |
| `79295_company-voluntary-arrangement-vs-administration-which-to-choose.html` | CVL | te Outcome if it fails Usually transitions to liquidation Terminates; company enters CVL or compulsory liquidation When ... | **no** | opening/hero, decision table/callout |
| `79295_company-voluntary-arrangement-vs-administration-which-to-choose.html` | Schedule B1 | stressed company. We have drawn on the Insolvency Act 1986 (Part I on CVAs, Part II and Schedule B1 on administration in... | **no** | page subject |
| `79455_insolvency-vs-bankruptcy.html` | CVL | k Insolvency Act 1986 (Parts I-VII) Insolvency Act 1986 (Parts VIII-XI) Main routes CVL, MVL, administration, CVA, compu... | **no** | opening/hero, decision table/callout |
| `79455_insolvency-vs-bankruptcy.html` | MVL | solvency Act 1986 (Parts I-VII) Insolvency Act 1986 (Parts VIII-XI) Main routes CVL, MVL, administration, CVA, compulsor... | **no** | opening/hero, decision table/callout |
| `79455_insolvency-vs-bankruptcy.html` | CVA | rts I-VII) Insolvency Act 1986 (Parts VIII-XI) Main routes CVL, MVL, administration, CVA, compulsory liquidation Bankrup... | **no** | opening/hero, decision table/callout |
| `79455_insolvency-vs-bankruptcy.html` | the Gazette | ed company debts or face a personal contribution order Public record Companies House, London Gazette Individual Insolven... | **no** | opening/hero, decision table/callout |
| `79580_can-hmrc-shut-down-my-business.html` | the Gazette | d "HMRC Urgent". Minutes later a colleague mentions that the company name has appeared in The Gazette. The question the ... | **no** | opening/hero |
| `79580_can-hmrc-shut-down-my-business.html` | advertised / advertisement (notice sense) | Winding-up petition presented to the court if the demand is unpaid. Petition advertised in The Gazette (typically 7 work... | **no** | opening/hero |
| `79580_can-hmrc-shut-down-my-business.html` | Official Receiver | order made unless petition is settled, dismissed, or replaced by administration. Official Receiver appointed as liquidat... | **no** | opening/hero |
| `14914_director-redundancy.html` | officeholder / office-holder | laim depends on one question: were you genuinely employed by the company, or only ever an officeholder? The distinction ... | **no** | opening/hero |
| `14914_director-redundancy.html` | National Insurance Fund | Actually Is Director redundancy pay is statutory redundancy pay accessed through the National Insurance Fund, administer... | **no** | page subject, opening/hero |
| `14914_director-redundancy.html` | wrongful trading | m your employment entitlements. Personal guarantees are enforced through their own terms. Wrongful trading concerns are ... | **no** | page subject |
| `22277_insolvent-company-owes-me-money.html` | the Gazette | Insolvent Before you file anything, check the position. Search the debtor's name on the London Gazette. A formal notice ... | **no** | opening/hero |
| `22277_insolvent-company-owes-me-money.html` | advertised / advertisement (notice sense) | e London Gazette. A formal notice of liquidation, administration, or receivership must be advertised there. Then cross-r... | **no** | opening/hero |
| `7687_winding-up-petitions.html` | restrain / restraining advertisement | e hearing. Source: . Both limbs matter. The first is the gap in which urgent work to restrain advertisement is realistic... | **no** | decision table/callout |
| `7687_winding-up-petitions.html` | substitution (of petitioner) | ven permission to withdraw, where the procedural requirements for that have been met. Substitution or support Another cr... | **no** | page subject, decision table/callout |
| `78578_intellectual-property-and-trading-assets-in-liquidation.html` | CVL | tion. The "IP I created is mine" assumption is the misunderstanding that converts a CVL into a wider misfeasance investi... | **no** | page subject, opening/hero |
| `78578_intellectual-property-and-trading-assets-in-liquidation.html` | misfeasance | P I created is mine" assumption is the misunderstanding that converts a CVL into a wider misfeasance investigation. Quic... | **no** | opening/hero |
| `78578_intellectual-property-and-trading-assets-in-liquidation.html` | MVL | 143 of the Insolvency Act 1986 , with operative sections varying by procedure: MVL : s.91 IA 1986 CVL : s.103 IA 1986 Co... | **no** | opening/hero |
| `20268_retail-industry-insolvency-trends.html` | wrongful trading | e day of appointment. Risk What triggers it in retail What protects you Wrongful trading (s.214 IA 1986) Continuing to o... | **no** | decision table/callout |
| `20268_retail-industry-insolvency-trends.html` | preference (unlawful) | 't fund autumn quarter rent Dated board minutes, IP advice on file, defined stop-date Preferences (s.239 IA 1986) Paying... | **no** | decision table/callout |
| `20268_retail-industry-insolvency-trends.html` | misfeasance | or pattern of failed retail vehicles Take advice early; document the decision to stop Misfeasance (s.212 IA 1986) Lease ... | **no** | decision table/callout |
| `20380_making-employees-redundant-cva.html` | Schedule 6 | ages owed to employees at the time the CVA begins are treated as preferential debts under Schedule 6 of the Insolvency A... | **no** | page subject |
| `20380_making-employees-redundant-cva.html` | National Insurance Fund | ers liquidation, employees made redundant during the arrangement can still claim from the National Insurance Fund via th... | **no** | page subject |
| `47772_insolvency-act-1986.html` | moratorium | about has its source in this Act: wrongful trading liability, compulsory winding-up, the moratorium in administration, t... | **no** | opening/hero |
| `47772_insolvency-act-1986.html` | disposition | case law, section 214 wrongful trading, section 123 the insolvency test, section 127 void dispositions, you will find li... | **no** | opening/hero |
| `74891_secured-vs-unsecured-creditors.html` | floating charge | terms. The bank, which sold its overdraft as "secured", finds it never registered the floating charge at Companies House... | **no** | page subject, opening/hero |
| `74891_secured-vs-unsecured-creditors.html` | debenture | mechanical, not commercial. A high-street bank that lent £400,000 without registering the debenture inside 21 days is un... | **no** | page subject |
| `79332_what-happens-if-a-cva-fails-mid-term.html` | CVA | st received a formal Notice of Breach from your supervisor? The clock has started. Once a CVA defaults and is formally t... | **no** | page subject, opening/hero |
| `79332_what-happens-if-a-cva-fails-mid-term.html` | wrongful trading | ition for liquidation or administration. That chain reaction can expose directors to wrongful trading claims under s.214... | **no** | opening/hero |
| `79545_what-happens-if-a-director-transfers-assets-before-insolvency.html` | CVL | s value. A third pays off their personal loan account from company funds weeks before the CVL. Each of these is a transa... | **no** | opening/hero |
| `79545_what-happens-if-a-director-transfers-assets-before-insolvency.html` | preference (unlawful) | liquidator a two-year lookback window for transactions at undervalue and connected-party preferences, and for fraud ther... | **no** | opening/hero |
| `79545_what-happens-if-a-director-transfers-assets-before-insolvency.html` | wrongful trading | f the Insolvency Act create criminal offences carrying up to seven years' imprisonment Wrongful trading: If you transfer... | **no** | page subject |
| `79615_can-a-supplier-force-my-company-into-liquidation.html` | advertised / advertisement (notice sense) | ion context, see our liquidation hub . Risk Warning Once a Petition Is Advertised, Your Bank Account Freezes the Same Da... | **no** | opening/hero, decision table/callout |
| `79615_can-a-supplier-force-my-company-into-liquidation.html` | the Gazette | es on the date the petition is presented, not the date the order is made. Banks monitor the London Gazette and freeze co... | **no** | opening/hero, decision table/callout |
| `13766_preferential-non-preferential-creditors.html` | Schedule 6 | olvency runs on a waterfall fixed by the Insolvency Act 1986, principally section 175 and Schedule 6. Where your claim s... | **no** | page subject, opening/hero |
| `13766_preferential-non-preferential-creditors.html` | officeholder / office-holder | xed-charge creditors are paid from their specific asset. The expenses of liquidation (the office-holder's fees and litig... | **no** | opening/hero |
| `79596_what-happens-if-hmrc-rejects-your-time-to-pay-arrangement.html` | moratorium | depending on size Administration Rescue or sale Handed to administrator Statutory moratorium; rescue or sale £15–50k+ CV... | **no** | decision table/callout |
| `79596_what-happens-if-hmrc-rejects-your-time-to-pay-arrangement.html` | CVL | scue or sale Handed to administrator Statutory moratorium; rescue or sale £15–50k+ CVL No, orderly closure IP takes cont... | **no** | decision table/callout |
| `25310_validation-order.html` | advertised / advertisement (notice sense) | It is Wednesday morning. The winding-up petition was advertised in the London Gazette yesterday. The accounts team logs ... | **no** | opening/hero |
| `25310_validation-order.html` | the Gazette | It is Wednesday morning. The winding-up petition was advertised in the London Gazette yesterday. The accounts team logs ... | **no** | opening/hero |
| `25310_validation-order.html` | presented (vs served) | mechanically, is section 127 of the Insolvency Act 1986. From the moment the petition is presented, and certainly once i... | **no** | opening/hero |
| `46222_what-happens-to-directors-in-liquidation.html` | misfeasance | examination if required. After liquidation, you may face wrongful trading claims, misfeasance claims, personal guarantee... | **no** | opening/hero |
| `46222_what-happens-to-directors-in-liquidation.html` | CVL | who assume wrongful trading claims are rare. They are not. The liquidator assesses every CVL and compulsory liquidation ... | **no** | page subject |
| `68120_can-you-sell-your-insolvent-company.html` | transaction at an undervalue | ning you are thinking "sale". The liquidator appointed six months later will be thinking "transaction at undervalue". Th... | **no** | opening/hero |
| `68120_can-you-sell-your-insolvent-company.html` | CVA | The formal processes, administration pre-pack, asset sale in liquidation, and (rarely) a CVA-based sale, exist to put th... | **no** | opening/hero |
| `77916_voluntary-vs-compulsory-liquidation.html` | the Gazette | ths to 3+ years Public record Filed at Companies House Filed at Companies House plus London Gazette advertisement Percep... | **no** | decision table/callout |
| `77916_voluntary-vs-compulsory-liquidation.html` | advertised / advertisement (notice sense) | Public record Filed at Companies House Filed at Companies House plus London Gazette advertisement Perception Director ac... | **no** | decision table/callout |
| `78797_what-happens-if-a-director-resigns-before-liquidation.html` | misfeasance | aken while you were a director. The liquidator can pursue wrongful trading claims, misfeasance claims, and transaction a... | **no** | opening/hero |
| `78797_what-happens-if-a-director-resigns-before-liquidation.html` | CVL | t will note the timing of your resignation. A director who resigned two weeks before the CVL was initiated raises more q... | **no** | page subject |
| `79351_can-i-choose-my-liquidator.html` | advertised / advertisement (notice sense) | n nominate a licensed insolvency practitioner you trust. Wait until after a petition is advertised and you lose that rig... | **no** | opening/hero |
| `79351_can-i-choose-my-liquidator.html` | the Gazette | a licensed IP while you still have the luxury of choice. Once a petition is advertised in the London Gazette, that choic... | **no** | opening/hero |
| `16106_vs-administrative-receivership.html` | floating charge | ared Administration Administrative Receivership Who appoints Directors, floating charge holder, or court A debenture hol... | **no** | opening/hero, decision table/callout |
| `16106_vs-administrative-receivership.html` | debenture | nistrative Receivership Who appoints Directors, floating charge holder, or court A debenture holder (secured creditor wi... | **no** | opening/hero, decision table/callout |
| `16106_vs-administrative-receivership.html` | moratorium | 03) Who they serve All creditors (statutory duty) The appointing secured creditor Moratorium Yes, automatic freeze on al... | **no** | opening/hero, decision table/callout |
| `24760_what-are-fixed-and-floating-charges.html` | debenture | ause most do not understand what their bank actually holds over the company. You signed a debenture when you took out th... | **no** | page subject, opening/hero |
| `68111_what-to-do-about-customer-insolvency.html` | the Gazette | Days After a Customer Goes Insolvent Confirm the formal status on Companies House and the Gazette. Pull every open invoi... | **no** | opening/hero |
| `68356_advantages-and-disadvantages.html` | Schedule B1 | strator immediately on appointment, often within hours. The legal framework sits in Schedule B1 of the Insolvency Act 19... | **no** | opening/hero |
| `68356_pre-pack-advantages-and-disadvantages.html` | Schedule B1 | strator immediately on appointment, often within hours. The legal framework sits in Schedule B1 of the Insolvency Act 19... | **no** | opening/hero |
| `74264_challenge-a-statutory-demand.html` | served / service | out the real, time-critical options available to your company once a statutory demand has been served: when you can seek... | **no** | page subject, opening/hero |
| `77205_hmrc-debt-enforcement-hub.html` | distraint / distrain | (No. 2) Act 2015. See What Happens If HMRC Freezes Your Business Bank Account . Distraint (Taking Control of Goods) , ce... | **no** | page subject, opening/hero |
| `79404_uk-insolvency-glossary.html` | preferential debt / creditor | achieve a better result for creditors than liquidation, or realise assets for secured and preferential creditors. See al... | **no** | opening/hero |
| `79423_insolvency-checklist.html` | preference (unlawful) | 214 wrongful-trading clock is ticking. Stop making selective creditor payments. s.239 preference exposure is automatic. ... | **no** | opening/hero |
| `79423_insolvency-checklist.html` | debenture | Every personal guarantee signed, charges registered under s.859A CA 2006 (MR01 filings), debentures Contingent liabiliti... | **no** | decision table/callout |
| `79489_seek-insolvency-advice-before-missing-payments.html` | statutory demand | Should You Seek Insolvency Advice? Before you miss a payment. Before HMRC sends a statutory demand. Before a supplier lo... | **no** | opening/hero |
| `79489_seek-insolvency-advice-before-missing-payments.html` | served / service | e company's position. Directors who call after the first statutory demand has been served often find the CVA route is al... | **no** | opening/hero, decision table/callout |
| `79529_what-happens-if-a-director-hides-company-assets.html` | CVL | ock Directors commonly believe that transferring assets several months before the CVL commences puts those transactions ... | **no** | decision table/callout |
| `79529_what-happens-if-a-director-hides-company-assets.html` | wrongful trading | g up. We have also drawn on sections 212 to 214 on misfeasance, fraudulent trading, and wrongful trading; sections 235 t... | **no** | page subject |
| `11788_frozen-bank-account.html` | advertised / advertisement (notice sense) | ur company's bank account has been frozen, the most likely cause is a winding-up petition advertised in the London Gazet... | **no** | opening/hero |
| `11788_frozen-bank-account.html` | the Gazette | ank account has been frozen, the most likely cause is a winding-up petition advertised in the London Gazette. Banks moni... | **no** | opening/hero |
| `13513_statement-of-affairs.html` | preferential debt / creditor | nd Wales) Rules 2016, and the content requirements are non-negotiable: secured creditors, preferential creditors, floati... | **no** | opening/hero |
| `13513_statement-of-affairs.html` | Schedule 6 | ting-charge creditors, unsecured creditors, and the statutory order of distribution under Schedule 6 of the Insolvency A... | **no** | opening/hero |
| `79246_can-i-liquidate-my-company-with-a-bounce-back-loan.html` | preferential debt / creditor | any other unsecured debt in the liquidation, ranking alongside trade creditors and behind preferential claims. Because t... | **no** | opening/hero |
| `79537_can-a-director-be-sued-personally-by-creditors.html` | misfeasance | s entered liquidation: the liquidator can bring claims against you for wrongful trading, misfeasance, preferences, or ov... | **no** | opening/hero |
| `79537_can-a-director-be-sued-personally-by-creditors.html` | preference (unlawful) | uidation: the liquidator can bring claims against you for wrongful trading, misfeasance, preferences, or overdrawn direc... | **no** | opening/hero |
| `79588_what-happens-if-you-ignore-hmrc-letters.html` | Time to Pay | al window. Formal demand , Debt Management letter indicating internal escalation. Time to Pay still usually available. C... | **no** | page subject, opening/hero |
| `8350_hmrc-threatening-letters.html` | Time to Pay | nagement formal demand. In our caseload, that is usually the last window in which a clean TTP is still cheap, and occasi... | **no** | page subject, opening/hero |
| `8414_time-to-pay-hmrc.html` | served / service | ingle phone call. Directors who call six months late, after statutory demands have been served and field officers instru... | **no** | opening/hero |
| `8414_time-to-pay-hmrc.html` | moratorium | ny Administration HMRC has filed a winding-up petition or business needs the statutory moratorium. Heavier process; admi... | **no** | decision table/callout |
| `9702_receivership-mean-business.html` | floating charge | eivership is a secured creditor's enforcement mechanism. A bank or lender with a fixed or floating charge over your comp... | **no** | opening/hero |
| `9702_receivership-mean-business.html` | moratorium | the power to appoint out of court, the appointment is immediate. There is no automatic moratorium. Other creditors, incl... | **no** | opening/hero |
| `14158_hmrc-fraud-investigations.html` | Time to Pay | cases extend further. Yes, in principle. HMRC's Debt Management unit can agree Time to Pay on CDF settlements, typically... | **no** | page subject |
| `21122_shareholders-liable-company-debts.html` | misfeasance | ble as a shareholder, but director risks may apply Wrongful trading, fraudulent trading, misfeasance, overdrawn loan acc... | **no** | decision table/callout |
| `21122_shareholders-liable-company-debts.html` | transaction at an undervalue | ue, not ordinary liability Assets moved to a connected party before failure Possible transaction at undervalue or prefer... | **no** | decision table/callout |
| `23698_how-much-does-liquidation-cost.html` | the Gazette | In addition to the practitioner's fee, the case may incur an insolvency bond, required Gazette notices, postage and othe... | **no** | decision table/callout |
| `23698_how-much-does-liquidation-cost.html` | preference (unlawful) | at the first call. It will be found regardless. Disputed transactions Where possible preferences or transactions at unde... | **no** | decision table/callout |
| `44055_cant-pay-staff-wages.html` | Time to Pay | Renegotiate supplier and tax payment terms to free up cash for payroll. HMRC Time to Pay arrangements can release cash q... | **no** | page subject |
| `46674_what-is-a-creditor.html` | preferential debt / creditor | and the Insolvency Rules 2016 define those categories precisely. The difference between a preferential claim and an unse... | **no** | page subject, opening/hero |
| `49618_creditors-meeting.html` | preferential debt / creditor | sworn under section 99, sets out assets at estimated realisable value, secured creditors, preferential creditors, and a ... | **no** | page subject |
| `67962_what-is-a-statutory-demand-against-a-company.html` | restrain / restraining advertisement | through a summary application. The only corporate remedy for dispute is an injunction to restrain a petition. Cost-effic... | **no** | opening/hero |
| `68101_dealing-with-creditor-pressure.html` | MVL | iable; directors want a controlled, statutory wind-down. Solvent surplus available (use MVL instead); ongoing trade can ... | **no** | decision table/callout |
| `68115_rescue-your-business-from-insolvency.html` | misfeasance | Act 1986 finds unfit conduct Disqualification 2 to 15 years; cannot act as a director Misfeasance (IA 1986 s.212) Breach... | **no** | decision table/callout |
| `73778_alternatives-to-company-liquidation.html` | CVL | ratorium. If the business model is broken, none of the rescue routes will hold and a CVL on your terms is the cleaner ex... | **no** | page subject |
| `7665_company-rescue-solutions.html` | CVL | l levers (HMRC Time to Pay, creditor negotiation), and the route-of-last-resort closures (CVL, MVL) that sometimes serve... | **no** | opening/hero |
| `7685_company-voluntary-arrangement.html` | preferential debt / creditor | t it cannot touch a secured creditor (a bank with a charge over company assets, say) or a preferential creditor without ... | **no** | opening/hero |
| `76920_hmrc-penalties-investigations.html` | Time to Pay | nquiry is ongoing, compounds penalty exposure and signals cash-flow insolvency . TTP breach or refusal during the enquir... | **no** | page subject |
| `79445_list-of-liquidation-documents.html` | CVL | of incorporation, and any security documents (charges, guarantees, debentures). For a CVL , you must also prepare a form... | **no** | page subject, opening/hero |
| `79563_what-happens-if-hmrc-freezes-your-business-bank-account.html` | validation order | ncy Act 1986 s.127 Winding-up petition advertised in The Gazette Hearing of petition or validation order Your bank shoul... | **no** | decision table/callout |
| `8396_pre-packs.html` | Schedule B1 | set of cases. Both of those things are true at once. The legal scaffolding sits in Schedule B1 of the Insolvency Act 198... | **no** | opening/hero |
| `8408_problems-paying-corporation-tax-hmrc.html` | served / service | If you can see the shortfall coming before the due date, HMRC's Business Payment Support Service on 0300 200 3835 is the... | **no** | opening/hero |
| `8408_problems-paying-corporation-tax-hmrc.html` | statutory demand | Formal insolvency action Where the tax is still unpaid and ignored, HMRC can serve a statutory demand and, ultimately, p... | **no** | decision table/callout |
| `24434_what-is-a-freezing-order-or-injunction.html` | served / service | risk you will dissipate assets before the claimant gets judgment. If you have just been served one, the calendar matters... | **no** | opening/hero |
| `65614_closing-a-limited-company.html` | wrongful trading | Waiting too long to start a CVL Each week of further trading while insolvent grows wrongful trading exposure under secti... | **no** | decision table/callout |
| `68216_what-is-a-directors-responsibility-for-accountancy-errors.html` | wrongful trading | have also drawn on the Insolvency Act 1986 (section 212 on misfeasance and section 214 on wrongful trading), the Company... | **no** | page subject |
| `68221_get-free-business-debt-advice.html` | wrongful trading | ion itself, because every week of delay narrows your options and increases your personal wrongful trading exposure . Qui... | **no** | opening/hero |
| `70501_preferential-payments-during-insolvency.html` | Schedule 6 | worth separating, because the language confuses directors. "Preferential creditor" under Schedule 6 IA 1986 is a statuto... | **no** | page subject |
| `76323_insolvency-advice-for-directors.html` | statutory demand | insolvency under section 123 of the Insolvency Act 1986 . Not when HMRC issues a statutory demand. Not when the bank pul... | **no** | opening/hero |
| `77883_liquidation-vs-dissolution-strike-off.html` | the Gazette | 13 filing fee (DS01 form) £3,500 + VAT (MVL) or £5,000+ (CVL) Timeline 3 months from Gazette notice 6 to 18 months typic... | **no** | decision table/callout |
| `78129_directors-conduct-report-2.html` | wrongful trading | eposits, or incur liabilities after the point where insolvency was probable? This is the wrongful trading territory unde... | **no** | page subject |
| `78825_paying-staff-but-not-hmrc-before-liquidation.html` | preference (unlawful) | t just a moral instinct. It is a legal risk. The liquidator can claw that payment back as a preference, and you personal... | **no** | opening/hero |
| `79396_director-conduct-review.html` | wrongful trading | pear in the bank statements and all of them go into the report. See our guides on wrongful trading and director payments... | **no** | page subject |
| `79472_should-i-close-my-company-or-try-to-save-it.html` | moratorium | administration) Control transfers to the liquidator Creditor pressure Can be paused (moratorium, CVA, administration) Re... | **no** | opening/hero, decision table/callout |
| `79507_what-happens-if-i-stop-paying-company-debts.html` | CVA | ctors who enter a formal insolvency process before creditors start enforcement; through a CVA, administration, or CVL; r... | **no** | decision table/callout |
| `79507_what-happens-if-i-stop-paying-company-debts.html` | CVL | insolvency process before creditors start enforcement; through a CVA, administration, or CVL; retain control of the rout... | **no** | decision table/callout |
| `79515_can-directors-go-to-prison-for-company-debt.html` | wrongful trading | company property (section 208), and fraud by false representation (Fraud Act 2006). Wrongful trading (section 214) is a ... | **no** | page subject |
| `79553_can-directors-pay-themselves-before-liquidation.html` | preference (unlawful) | ector's loan account to yourself ahead of trade creditors is one of the fastest routes to a preference claim under secti... | **no** | opening/hero |
| `79571_what-happens-if-hmrc-sends-bailiffs-to-a-business.html` | Time to Pay | authorised to attend after 7 clear days. Days 1–7 , last cheap window. Pay, agree Time to Pay, dispute formally, or ente... | **no** | page subject, opening/hero |
| `79845_data.html` | advertised / advertisement (notice sense) | nsolvency Service 482 Winding-up petitions Advertised in May 2026 The Gazette 5,498,905 Active companies The registe | **no** | opening/hero |
| `79845_data.html` | the Gazette | 482 Winding-up petitions Advertised in May 2026 The Gazette 5,498,905 Active companies The register, May 2026 Companies ... | **no** | opening/hero |
| `11193_hmrc-compliance-checks.html` | Time to Pay | is formal and the procedural rules change. Where a settlement cannot be paid, Time to Pay arrangements are usually avail... | **no** | page subject |
| `11384_hmrc-tax-investigations.html` | Time to Pay | nvestigation runs, compounds penalty exposure and signals cash-flow insolvency . Time to Pay breach or refusal , see Wha... | **no** | page subject |
| `14619_hmrcs-ir35-investigations-different.html` | Time to Pay | to a licensed insolvency practitioner about whether the company can absorb it or whether Time to Pay or other options ar... | **no** | page subject |
| `16353_hmrc-follower-notice.html` | Time to Pay | thdraw the appeal in writing. Pay the underlying tax , or arrange payment through Time to Pay where funds are insufficie... | **no** | page subject |
| `16662_what-is-an-individual-voluntary-arrangement.html` | advertised / advertisement (notice sense) | f distributions Throughout 5-year term Disbursements £150-400 total Statutory advertising, Bond of Indemnity, court fees... | **no** | decision table/callout |
| `20681_can-director-criminal-record.html` | misfeasance | You cannot get a criminal record for wrongful trading (section 214, civil only), misfeasance (section 212, civil only), ... | **no** | opening/hero |
| `42739_what-happens-if-a-company-cannot-pay-its-debts.html` | misfeasance | r disqualification CDDA 1986 Up to 15 years' ban from directorship for unfit conduct Misfeasance s.212 Insolvency Act 19... | **no** | decision table/callout |
| `66834_what-is-a-pre-pack-administration.html` | Schedule B1 | circumstances. Creditors can challenge the administrator's conduct under paragraph 74 of Schedule B1, and the court can ... | **no** | page subject |
| `68117_how-to-save-a-struggling-business.html` | misfeasance | wn debts, trading on) Take advice early; the timing of the call is what gets recorded Misfeasance (s.212 IA 1986) Breach... | **no** | decision table/callout |
| `68189_how-to-legally-take-money-out-of-a-limited-company.html` | wrongful trading | The most common way we see directors get themselves into trouble is not fraud, wrongful trading, or any of the louder in... | **no** | opening/hero |
| `71514_directors-duties-to-creditors.html` | misfeasance | ors every week because it is the legal foundation of almost every wrongful trading claim, misfeasance action, and disqua... | **no** | opening/hero |
| `74382_when-employers-cant-afford-redundancy-payments.html` | National Insurance Fund | ments Service, a government-backed safety net that pays statutory entitlements out of the National Insurance Fund when a... | **no** | page subject, opening/hero |
| `77693_insolvency-news-commentary.html` | preferential debt / creditor | change how you should think about your own position. HMRC's reinstatement as a secondary preferential creditor in Decemb... | **no** | opening/hero |
| `78613_how-to-prove-your-debt-in-company-liquidation.html` | CVL | claimed. This should be the amount owed at the date of the winding-up resolution (for a CVL) or the date of the winding-... | **no** | page subject |
| `78673_liquidators-powers-and-duties.html` | wrongful trading | or the business as a going concern, by private treaty or auction. Pursue legal claims: wrongful trading (s.214), fraudul... | **no** | page subject |
| `78771_liquidating-a-charity-or-non-profit.html` | preference (unlawful) | 6 provisions as any limited company; this includes wrongful trading under section 214 and preference claims under sectio... | **no** | opening/hero, decision table/callout |
| `78812_redundancy-payments-for-directors-in-an-mvl.html` | MVL | If you are closing a solvent company through an MVL (a form of voluntary liquidation ), you may be entitled to a statuto... | **no** | page subject, opening/hero |
| `79313_light-touch-administration.html` | Schedule B1 | inistration The legal framework is identical. The administrator is appointed under Schedule B1 of the Insolvency Act 198... | **no** | page subject |
| `79436_directors-responsibilities-after-a-company-is-struck-off.html` | wrongful trading | specific transactions. That letter is the moment to take advice. See our guide on wrongful trading for the broader direc... | **no** | page subject |
| `79853_compulsory-liquidation-statistics.html` | CVL | is winding-up petition statistics . See also the UK company insolvency statistics and CVL statistics . Recent months UK ... | **no** | page subject |
| `8358_what-is-an-insolvency-practitioner.html` | CVA | untant or a "company doctor". Without it, you cannot be a liquidator, an administrator, a CVA supervisor, or a trustee i... | **no** | opening/hero |
| `38597_losing-house-if-company-goes-bust.html` | wrongful trading | r property, then applies for an order for sale. Slower but reaches the same outcome. A wrongful trading contribution ord... | **no** | opening/hero |
| `48170_creditors-guides-to-insolvency-practitioners-fees.html` | officeholder / office-holder | onths later, the IP’s progress report lands in your inbox. Asset realisations of £58,000. Office-holder remuneration of ... | **no** | opening/hero |
| `52771_what-is-the-companies-act-2006.html` | wrongful trading | act in the interests of creditors, not shareholders. This is the duty shift that creates wrongful trading exposure . The... | **no** | opening/hero |
| `68192_preventing-company-director-disputes.html` | CVL | s insolvent, letting the insolvency practitioner make the decision for you by entering a CVL or administration . Common ... | **no** | opening/hero |
| `74390_when-a-cva-fails.html` | wrongful trading | tion. Directors who continue trading without taking advice face the additional risk of wrongful trading under section 21... | **no** | opening/hero |
| `79480_when-should-a-director-stop-trading.html` | CVL | A director who called an insolvency practitioner, received a recommendation to enter CVL, and then continued trading for... | **no** | decision table/callout |
| `79847_winding-up-petition-tracker.html` | advertised / advertisement (notice sense) | a creditor's application to the court to close a company. This page counts the petitions advertised against UK companies... | **no** | opening/hero |
| `22554_limited-company-bankruptcy.html` | wrongful trading | lsory) Discharged after 12 months (usually) What survives Personal guarantees, DLA, wrongful trading orders Most debts w... | **no** | decision table/callout |
| `26298_misfeasance.html` | wrongful trading | d themselves at the company's expense. The claim is separate from and in addition to any wrongful trading or disqualific... | **no** | opening/hero |
| `26902_biggest-struggles-for-small-business-owners.html` | statutory demand | to the Small Business Commissioner for persistent late-payers. Formal recovery , statutory demand, county court claim, w... | **no** | opening/hero |
| `55381_writing-off-a-directors-loan-account.html` | preference (unlawful) | near insolvency , the write-off itself can be unwound by a liquidator and reassessed as a preference or a distribution t... | **no** | opening/hero |
| `68153_advice-hub.html` | misfeasance | What is limited liability? What the protection actually covers Misfeasance The civil claim liquidators use most Personal... | **no** | opening/hero |
| `79360_ccj-when-going-insolvent.html` | CVL | t a fresh proof of debt; the judgement itself is the proof. If the company enters a CVL , enforcement of the CCJ is stay... | **no** | opening/hero |
| `79498_pay-hmrc-or-suppliers-first.html` | preference (unlawful) | purely commercial. Once your company is on the edge of insolvency, paying one creditor in preference to another can be u... | **no** | opening/hero |

## MEDIUM and LOW by page

Full detail in the CSV. Pages with the largest MEDIUM counts:

| Page | MEDIUM | LOW |
|---|---:|---:|
| `7674_creditors-voluntary-liquidation.html` | 10 | 3 |
| `77146_debt-creditor-pressure-hub.html` | 9 | 6 |
| `79379_business-bank-account-in-liquidation.html` | 8 | 5 |
| `22277_insolvent-company-owes-me-money.html` | 7 | 5 |
| `26888_stop-or-avoid-insolvency.html` | 7 | 7 |
| `7669_liquidation.html` | 7 | 6 |
| `79256_liquidating-a-company-with-no-assets-or-bank-account-uk.html` | 7 | 4 |
| `47772_insolvency-act-1986.html` | 6 | 7 |
| `67747_antecedent-transactions.html` | 6 | 1 |
| `68111_what-to-do-about-customer-insolvency.html` | 6 | 8 |
| `68130_business-recovery-services.html` | 6 | 6 |
| `68356_advantages-and-disadvantages.html` | 6 | 3 |
| `68356_pre-pack-advantages-and-disadvantages.html` | 6 | 3 |
| `77162_hmrc-enforcement-action.html` | 6 | 6 |
| `79404_uk-insolvency-glossary.html` | 6 | 3 |
| `79580_can-hmrc-shut-down-my-business.html` | 6 | 7 |
| `79615_can-a-supplier-force-my-company-into-liquidation.html` | 6 | 10 |
| `13029_understanding-hmrc-debt-collection.html` | 5 | 7 |
| `67960_cant-afford-to-pay-suppliers-what-are-the-options.html` | 5 | 2 |
| `68123_what-are-the-warning-signs-of-an-insolvent-company.html` | 5 | 7 |
| `68207_are-directors-personally-liable-for-company-debts.html` | 5 | 1 |
| `7680_compulsory-liquidation.html` | 5 | 9 |
| `7687_winding-up-petitions.html` | 5 | 9 |
| `77396_director-protection-hub.html` | 5 | 4 |
| `78690_liquidation-deadlines-and-time-limits.html` | 5 | 2 |
| `79246_can-i-liquidate-my-company-with-a-bounce-back-loan.html` | 5 | 1 |
| `79596_what-happens-if-hmrc-rejects-your-time-to-pay-arrangement.html` | 5 | 3 |
| `24760_what-are-fixed-and-floating-charges.html` | 4 | 1 |
| `26218_business-debt-advice.html` | 4 | 5 |
| `26279_cease-trading.html` | 4 | 7 |

## Recommended sequence

1. Agree the house definitions in the systemic-terms table above and put them somewhere the writing stages actually load - the humanise pack, not a governance file that is only read on conflict.
2. Fix the ten worst offenders per-page through Bernstein, humanise pass last, on Opus.
3. Add a first-use check to the humanise stage: for every term in the house list, the first appearance on the page must carry the gloss. This is a stage instruction, not an `article_audit.py` check - the gate scores structure, and this is a reader-comprehension property it cannot see.
4. Re-run this scan after the first batch to confirm the pattern-based detector agrees with the human read.

---

*Generated by a one-off scan of `drafts/`; no page content was modified.*