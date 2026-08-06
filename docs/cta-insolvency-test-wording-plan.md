# Insolvency Test CTA — Wording Plan

**Status: proposal, for review.** Nothing below is deployed beyond the pilot page.
Companion files: `cta-rollout-plan.md` (placement and roll-out phases),
`cta-rollout-manifest.md` (per-page cluster mapping),
`design/insolvency-cta-blocks/` (the design handoff and screenshots).

Built and live on staging today: `/winding-up-petitions/` (post 7687), carrying the
`formal_action` wording, picked up automatically from the page map.
https://comdebstage.wpengine.com/winding-up-petitions/

---

## 1. The rule that governs every wording

A headline may only promise what the result screen actually delivers:

- which warning signs apply,
- how serious the position looks,
- how soon to act,
- which routes may fit (arrangement, restructuring, administration, CVL, or solvent
  closure where the answers support it).

It delivers nothing petition-specific, nothing about personal liability, and no verdict.
**If a wording cannot be honoured by the result screen, it does not ship.** This is the
constraint that kills most "better converting" headline ideas, and it should.

---

## 2. Why the topic clusters cannot drive this on their own

The existing manifest sorts pages by subject — liquidation, HMRC, cash-flow and so on.
The wording needs to track something different: where the reader already is.

Those two do not line up. Pages about enforcement (statutory demands, bailiffs, writs,
petitions) are spread across five clusters, including one filed under solvent closure
(`/liquidation/ccj-when-going-insolvent/`, which looks mis-classified in the manifest and
is worth fixing regardless).

So the mapping is per page, not per cluster.

---

## 3. Two questions decide what a page gets

### Question one: can this reader still act on the company?

If not, **the block does not go on that page at all.** This matters more than picking
between wordings: sending the wrong reader to the test is worse than showing the right
reader a flat headline. Three groups fail:

| Group | Why | Roughly |
|---|---|---|
| Company already in a formal process (in liquidation, in administration) | The question the test answers has already been answered for them | ~13 pages |
| Reader is not the director (creditor-facing, employee-facing) | The test asks whether *the company* can pay its bills. It is not their company | ~8 pages |
| Company is solvent (MVL, strike-off) | The test's first question has no "yes, comfortably" answer, so it forces a healthy company into a distress answer and returns a slightly wrong result | 8 pages |

The solvent-company point is a genuine defect in the tool for that audience, not a
presentation problem. Those readers belong on the members' voluntary liquidation pages.

### Question two: how far has it gone?

For everyone else, one of four:

| Reader's position | Big block headline | Small block headline | Button |
|---|---|---|---|
| **unsure** — suspects trouble, nothing formal yet *(default)* | Could Your Company Be Insolvent? | Not Sure Where Your Company Stands? | Check my company's position |
| **formal_action** — demand, petition, judgment, bailiffs already in play | How Serious Is It, and What Is Still Open? | Where Does the Company Actually Stand? | Check where the company stands |
| **closing** — already looking at closing the company | Is Closure the Right Route, or Is There Another? | Sure Closure Is the Right Step? | Check the company's position |
| **personal_risk** — worried about personal liability | How Bad Is the Company's Position? | Worried About Where This Leaves You Personally? | Check the company's position |

`personal_risk` is deliberately flat. The test assesses the company, not the director's
exposure, so the headline stays on the company and the body says the earlier the position
is clear the more room there is to act. Anything promising "see where you stand
personally" would be a promise the test cannot keep.

---

## 4. How a page gets its wording

In priority order:

1. What the page explicitly asks for — `[cd_test_cta variant="formal_action"]`
2. The reviewed page map in `mu-plugins/cd-cta-insolvency-test.php`
3. The neutral default, `unsure`

**No guessing from page names, deliberately.** The cost runs both ways:

- Guessing too low — asking a director holding a petition whether the company might be
  insolvent — reads as though we have not been listening.
- Guessing too high — asking someone worried about a slow month whether closure is the
  right route — is alarming, and could push a viable company toward a decision it does
  not need to make.

An unreviewed page therefore gets the neutral wording, not a guess.

---

## 5. What this needs from a human

The table in section 8 lists all 230 pages with a suggested wording. **The suggestions
come from scanning page names, so treat them as a starting point, not a decision.**

How much is actually settled by that scan:

| Suggested | Count | Confidence |
|---|---|---|
| unsure (the default) | 168 | Low — this is mostly "the scan could not tell" |
| formal_action | 14 | Good — enforcement words in the page name are reliable |
| NONE (already in a process) | 13 | Fair — needs checking |
| personal_risk | 10 | Good — comes from the existing cluster |
| closing | 9 | Low — under-counted, see below |
| NONE (not the director) | 8 | Fair — needs checking |
| NONE (solvent company) | 8 | Good — comes from the existing cluster |

How crude the scan is, by example: the first version of it classed
`/advice/writing-off-a-directors-loan-account/` as an enforcement page, because "writ"
appears inside "writing". Corrected — but it is a fair illustration of why the third
column is a suggestion and not a decision.

The 168 defaults are where the real review sits, and the 66-page liquidation cluster is
the bulk of it. Those pages split between "thinking about closing" and "already in it" in
a way the page name does not reveal, so `closing` is certainly under-counted at 9.

Suggested approach: work down the liquidation cluster first, since it is the largest
block of genuine decisions; the rest can stay on the default without embarrassment.

---

## 6. Open questions for review

1. **Is four wordings the right number?** More gets us closer per page and harder to keep
   honest and consistent. Fewer is blunter but easier to govern.
2. **Do the three "no block" groups get nothing, or a softened block?** The argument for
   nothing is that the test genuinely does not serve them. The argument for something is
   that a page with no call to action converts at zero.
3. **Should the two blocks on a page carry the same wording?** They do now — the small
   block is the short form of the same idea. The alternative is a second angle lower down
   the page.
4. **Does the wording need a compliance read** before it goes site-wide, given the
   `personal_risk` variant touches liability?

---

## 7. How we would know it is working

Every button carries its wording in its tracking tag
(`data-cd-cta="insolvency-test-full-formal-action"` and so on), so reporting will show
which wording earns clicks on which kind of page. If the enforcement wording
underperforms the default on enforcement pages, that is an answer rather than a matter of
taste.

Worth agreeing before roll-out: how long a page needs to run before its numbers mean
anything, given the site sees roughly 22 UK clicks a day.

---

## 8. Per-page suggestions

Ordered by suggested wording, defaults last. Correct the third column and add a note in
the fourth where the suggestion is wrong.

| Page | Cluster | Suggested wording | Confirmed? |
|---|---|---|---|
| /company-cash-flow-problems/challenge-a-statutory-demand/ | cash-flow | formal_action | |
| /company-cash-flow-problems/what-is-a-statutory-demand-against-a-company/ | cash-flow | formal_action | |
| /hmrc/distraint-order-notice/ | hmrc | formal_action | |
| /hmrc/hmrc-debt-enforcement-hub/ | hmrc | formal_action | |
| /hmrc/hmrc-enforcement-action/ | hmrc | formal_action | |
| /hmrc/notice-of-enforcement/ | hmrc | formal_action | |
| /hmrc/what-can-hmrc-bailiffs-take/ | hmrc | formal_action | |
| /hmrc/what-happens-if-hmrc-sends-bailiffs-to-a-business/ | hmrc | formal_action | |
| /insolvency/what-is-a-high-court-writ/ | general | formal_action | |
| /liquidation/bailiffs-high-court-enforcement-officers/ | hmrc | formal_action | |
| /liquidation/winding-up-petition-vs-compulsory-liquidation/ | liquidation | formal_action | |
| /winding-up-petitions/ | liquidation | formal_action | |
| /winding-up-petitions/dealing-with-an-hmrc-winding-up-petition/ | hmrc | formal_action | |
| /winding-up-petitions/what-is-a-winding-up-order/ | liquidation | formal_action | |
| /bounce-back-loan-support-hub/dissolving-a-company-with-bounce-back-loan/ | bounce-back | closing | |
| /liquidation/can-i-liquidate-a-dormant-company/ | liquidation | closing | |
| /liquidation/can-i-liquidate-my-company-with-a-bounce-back-loan/ | bounce-back | closing | |
| /liquidation/can-you-liquidate-to-avoid-paying-suppliers/ | liquidation | closing | |
| /liquidation/cant-afford-to-liquidate/ | liquidation | closing | |
| /liquidation/company-strike-off-and-dissolution/directors-responsibilities-after-a-company-is-struck-off/ | liquidation | closing | |
| /liquidation/creditors-voluntary-liquidation/ | liquidation | closing | |
| /liquidation/cva-vs-strike-off-vs-liquidation/ | rescue | closing | |
| /liquidation/should-i-close-my-company-or-try-to-save-it/ | liquidation | closing | |
| /advice/can-personal-assets-of-directors-be-seized-from-a-ltd-company/ | director-liability | personal_risk | |
| /advice/directors-disqualification/ | director-liability | personal_risk | |
| /advice/directors-personal-guarantees/ | director-liability | personal_risk | |
| /advice/misfeasance/ | director-liability | personal_risk | |
| /advice/overdrawn-directors-loan-accounts/ | director-liability | personal_risk | |
| /advice/personal-guarantee-insurance/ | director-liability | personal_risk | |
| /advice/the-risks-of-signing-a-personal-guarantee/ | director-liability | personal_risk | |
| /advice/unenforceable-personal-guarantee/ | director-liability | personal_risk | |
| /advice/what-are-phoenix-companies/ | director-liability | personal_risk | |
| /advice/writing-off-a-directors-loan-account/ | director-liability | personal_risk | |
| /closing-a-limited-company/ | solvent-closure | NONE (solvent company) | |
| /liquidation/am-i-solvent/ | solvent-closure | NONE (solvent company) | |
| /liquidation/ccj-when-going-insolvent/ | solvent-closure | NONE (solvent company) | |
| /liquidation/company-restoration-after-liquidation/ | solvent-closure | NONE (solvent company) | |
| /liquidation/company-strike-off-and-dissolution/ | solvent-closure | NONE (solvent company) | |
| /liquidation/company-strike-off-and-dissolution/can-i-be-sued-after-my-company-is-dissolved/ | solvent-closure | NONE (solvent company) | |
| /liquidation/liquidation-vs-dissolution-strike-off/ | solvent-closure | NONE (solvent company) | |
| /liquidation/redundancy-payments-for-directors-in-an-mvl/ | solvent-closure | NONE (solvent company) | |
| /company-administration/ | rescue | NONE (already in a process) | |
| /company-administration/light-touch-administration/ | rescue | NONE (already in a process) | |
| /company-administration/notice-of-intention-to-appoint-administrators/ | rescue | NONE (already in a process) | |
| /company-administration/vs-administrative-receivership/ | rescue | NONE (already in a process) | |
| /company-administration/vs-cva/ | rescue | NONE (already in a process) | |
| /liquidation/business-bank-account-in-liquidation/ | liquidation | NONE (already in a process) | |
| /liquidation/company-property-and-real-estate-in-liquidation/ | liquidation | NONE (already in a process) | |
| /liquidation/company-vehicles-and-equipment-in-liquidation/ | liquidation | NONE (already in a process) | |
| /liquidation/compulsory-liquidation/ | liquidation | NONE (already in a process) | |
| /liquidation/intellectual-property-and-trading-assets-in-liquidation/ | liquidation | NONE (already in a process) | |
| /liquidation/leases-and-contracts-in-liquidation/ | liquidation | NONE (already in a process) | |
| /liquidation/voluntary-vs-compulsory-liquidation/ | liquidation | NONE (already in a process) | |
| /liquidation/what-happens-to-directors-in-liquidation/ | liquidation | NONE (already in a process) | |
| /company-cash-flow-problems/cant-pay-staff-wages/ | cash-flow | NONE (not the director) | |
| /company-cash-flow-problems/when-employers-cant-afford-redundancy-payments/ | cash-flow | NONE (not the director) | |
| /company-rescue-solutions/company-voluntary-arrangement/making-employees-redundant-cva/ | rescue | NONE (not the director) | |
| /director-redundancy/ | liquidation | NONE (not the director) | |
| /liquidation/creditor-meetings-in-liquidation/ | liquidation | NONE (not the director) | |
| /liquidation/hmrc-as-a-creditor-in-liquidation/ | hmrc | NONE (not the director) | |
| /liquidation/paying-staff-but-not-hmrc-before-liquidation/ | hmrc | NONE (not the director) | |
| /liquidation/what-happens-to-employees/ | liquidation | NONE (not the director) | |
| /advantages-and-disadvantages/ | rescue | unsure | |
| /advice/ | general | unsure | |
| /advice/are-directors-personally-liable-for-company-debts/ | general | unsure | |
| /advice/business-restructuring/ | rescue | unsure | |
| /advice/can-a-director-be-made-bankrupt-if-a-business-fails/ | general | unsure | |
| /advice/can-director-criminal-record/ | general | unsure | |
| /advice/debt-management-guide/ | general | unsure | |
| /advice/directors-duties-to-creditors/ | general | unsure | |
| /advice/frozen-bank-account/ | general | unsure | |
| /advice/funding-options-for-smes-in-the-uk/ | general | unsure | |
| /advice/get-free-business-debt-advice/ | general | unsure | |
| /advice/hmrcs-ir35-investigations-different/ | hmrc | unsure | |
| /advice/how-to-legally-take-money-out-of-a-limited-company/ | general | unsure | |
| /advice/insolvency-advice-for-directors/ | general | unsure | |
| /advice/losing-house-if-company-goes-bust/ | general | unsure | |
| /advice/personal-liability-for-cbils-loans/ | general | unsure | |
| /advice/preventing-company-director-disputes/ | general | unsure | |
| /advice/what-are-a-company-directors-duties-to-avoid-and-disclose-conflicts-of-interest/ | general | unsure | |
| /advice/what-are-fixed-and-floating-charges/ | general | unsure | |
| /advice/what-are-the-duties-and-responsibilities-of-a-company-director/ | general | unsure | |
| /advice/what-is-a-directors-responsibility-for-accountancy-errors/ | general | unsure | |
| /advice/what-is-limited-liability/ | general | unsure | |
| /advice/what-is-the-companies-act-2006/ | general | unsure | |
| /bounce-back-loan-support-hub/bounce-back-loan-fraud/ | bounce-back | unsure | |
| /bounce-back-loan-support-hub/can-i-lose-my-house-with-a-bounce-back-loan/ | bounce-back | unsure | |
| /bounce-back-loan-support-hub/cant-pay-coronavirus-business-interruption-loan-cbils/ | bounce-back | unsure | |
| /bounce-back-loan-support-hub/directors-liability-for-bounce-back-loans/ | bounce-back | unsure | |
| /bounce-back-loan-support-hub/what-happens-if-i-default/ | bounce-back | unsure | |
| /care-home-insolvency/ | liquidation | unsure | |
| /charity-non-profit-insolvency/ | liquidation | unsure | |
| /company-cash-flow-problems/ | cash-flow | unsure | |
| /company-cash-flow-problems/biggest-struggles-for-small-business-owners/ | cash-flow | unsure | |
| /company-cash-flow-problems/cant-afford-to-pay-suppliers-what-are-the-options/ | cash-flow | unsure | |
| /company-cash-flow-problems/cant-afford-to-repay-business-loan/ | cash-flow | unsure | |
| /company-cash-flow-problems/cant-pay-a-commercial-lease-or-rent/ | cash-flow | unsure | |
| /company-cash-flow-problems/cant-pay-a-company-mortgage/ | cash-flow | unsure | |
| /company-cash-flow-problems/cant-pay-business-energy/ | cash-flow | unsure | |
| /company-cash-flow-problems/cant-pay-business-rates/ | cash-flow | unsure | |
| /company-cash-flow-problems/company-is-having-financial-difficulties/ | cash-flow | unsure | |
| /company-cash-flow-problems/why-debt-is-not-always-a-bad-thing-for-your-business/ | cash-flow | unsure | |
| /company-rescue-solutions/ | rescue | unsure | |
| /company-rescue-solutions/company-voluntary-arrangement/ | rescue | unsure | |
| /company-rescue-solutions/company-voluntary-arrangement/director-guarantees-in-a-cva/ | rescue | unsure | |
| /company-rescue-solutions/company-voluntary-arrangement/pros-and-cons/ | rescue | unsure | |
| /company-rescue-solutions/company-voluntary-arrangement/use-a-cva-to-close-a-company/ | rescue | unsure | |
| /company-rescue-solutions/company-voluntary-arrangement/vs-liquidation/ | rescue | unsure | |
| /company-rescue-solutions/company-voluntary-arrangement/what-happens-if-a-cva-fails-mid-term/ | rescue | unsure | |
| /company-rescue-solutions/company-voluntary-arrangement/when-a-cva-fails/ | rescue | unsure | |
| /company-rescue-solutions/partnership-voluntary-arrangements/ | rescue | unsure | |
| /company-rescue-solutions/pre-packs/ | rescue | unsure | |
| /construction-insolvency/ | rescue | unsure | |
| /county-court-judgements/ | hmrc | unsure | |
| /energy-provider-insolvency/ | liquidation | unsure | |
| /hmrc/ | hmrc | unsure | |
| /hmrc/accelerated-payment-notices-apn/ | hmrc | unsure | |
| /hmrc/can-hmrc-shut-down-my-business/ | hmrc | unsure | |
| /hmrc/cant-pay-paye/ | hmrc | unsure | |
| /hmrc/cant-pay-vat/ | hmrc | unsure | |
| /hmrc/controlled-goods-agreement/ | hmrc | unsure | |
| /hmrc/corporation-tax-penalties/ | hmrc | unsure | |
| /hmrc/hmrc-compliance-checks/ | hmrc | unsure | |
| /hmrc/hmrc-criminal-investigations/ | hmrc | unsure | |
| /hmrc/hmrc-follower-notice/ | hmrc | unsure | |
| /hmrc/hmrc-fraud-investigations/ | hmrc | unsure | |
| /hmrc/hmrc-offices-contact-guide/ | hmrc | unsure | |
| /hmrc/hmrc-penalties-investigations/ | hmrc | unsure | |
| /hmrc/hmrc-tax-investigations/ | hmrc | unsure | |
| /hmrc/hmrc-threatening-letters/ | hmrc | unsure | |
| /hmrc/joint-and-several-liability-for-unpaid-vat/ | hmrc | unsure | |
| /hmrc/pay-hmrc-or-suppliers-first/ | hmrc | unsure | |
| /hmrc/personal-liability-notices/ | hmrc | unsure | |
| /hmrc/problems-paying-corporation-tax-hmrc/ | hmrc | unsure | |
| /hmrc/security-bond-notices/ | hmrc | unsure | |
| /hmrc/security-bonds/ | hmrc | unsure | |
| /hmrc/tax-penalties/ | hmrc | unsure | |
| /hmrc/time-to-pay-hmrc/ | hmrc | unsure | |
| /hmrc/understanding-hmrc-debt-collection/ | hmrc | unsure | |
| /hmrc/vat-penalties/ | hmrc | unsure | |
| /hmrc/what-happens-if-hmrc-freezes-your-business-bank-account/ | hmrc | unsure | |
| /hmrc/what-happens-if-hmrc-rejects-your-time-to-pay-arrangement/ | hmrc | unsure | |
| /hmrc/what-happens-if-you-ignore-hmrc-letters/ | hmrc | unsure | |
| /hospitality-restaurant-insolvency/ | rescue | unsure | |
| /insolvency/ | general | unsure | |
| /insolvency/antecedent-transactions/ | general | unsure | |
| /insolvency/business-recovery-services/ | general | unsure | |
| /insolvency/can-we-trade-out-of-insolvency/ | general | unsure | |
| /insolvency/can-you-sell-your-insolvent-company/ | general | unsure | |
| /insolvency/cease-trading/ | general | unsure | |
| /insolvency/check-if-a-company-is-insolvent/ | general | unsure | |
| /insolvency/creditor-negotiations/ | general | unsure | |
| /insolvency/creditors-guides-to-insolvency-practitioners-fees/ | general | unsure | |
| /insolvency/creditors-meeting/ | general | unsure | |
| /insolvency/dealing-with-creditor-pressure/ | general | unsure | |
| /insolvency/find-a-liquidator-near-me/ | general | unsure | |
| /insolvency/how-to-reduce-insolvency-risk/ | general | unsure | |
| /insolvency/how-to-save-a-struggling-business/ | general | unsure | |
| /insolvency/insolvency-act-1986/ | general | unsure | |
| /insolvency/insolvency-test/ | general | unsure | |
| /insolvency/insolvent-company-investigations/ | general | unsure | |
| /insolvency/insolvent-company-owes-me-money/ | general | unsure | |
| /insolvency/limited-company-bankruptcy/ | general | unsure | |
| /insolvency/lpa-receivership/ | rescue | unsure | |
| /insolvency/personal-liability-spouses-business-debts/ | general | unsure | |
| /insolvency/personally-liabilty-of-company-secretary/ | general | unsure | |
| /insolvency/preferential-non-preferential-creditors/ | general | unsure | |
| /insolvency/preferential-payments-during-insolvency/ | general | unsure | |
| /insolvency/rescue-your-business-from-insolvency/ | rescue | unsure | |
| /insolvency/retail-industry-insolvency-trends/ | general | unsure | |
| /insolvency/secured-vs-unsecured-creditors/ | general | unsure | |
| /insolvency/shareholders-liable-company-debts/ | general | unsure | |
| /insolvency/statement-of-affairs/ | general | unsure | |
| /insolvency/stop-or-avoid-insolvency/ | general | unsure | |
| /insolvency/transactions-at-undervalue/ | general | unsure | |
| /insolvency/validation-order/ | liquidation | unsure | |
| /insolvency/what-are-the-warning-signs-of-an-insolvent-company/ | general | unsure | |
| /insolvency/what-happens-if-a-company-cannot-pay-its-debts/ | general | unsure | |
| /insolvency/what-is-a-creditor/ | general | unsure | |
| /insolvency/what-is-a-freezing-order-or-injunction/ | general | unsure | |
| /insolvency/what-is-an-individual-voluntary-arrangement/ | rescue | unsure | |
| /insolvency/what-is-an-insolvency-practitioner/ | general | unsure | |
| /insolvency/what-is-the-insolvency-service/ | general | unsure | |
| /insolvency/what-is-wrongful-trading/ | general | unsure | |
| /insolvency/what-to-do-about-customer-insolvency/ | general | unsure | |
| /liquidation/ | liquidation | unsure | |
| /liquidation/alternatives-to-company-liquidation/ | rescue | unsure | |
| /liquidation/can-a-director-be-sued-personally-by-creditors/ | liquidation | unsure | |
| /liquidation/can-a-supplier-force-my-company-into-liquidation/ | liquidation | unsure | |
| /liquidation/can-directors-go-to-prison-for-company-debt/ | liquidation | unsure | |
| /liquidation/can-directors-pay-themselves-before-liquidation/ | liquidation | unsure | |
| /liquidation/can-i-choose-my-liquidator/ | hmrc | unsure | |
| /liquidation/can-i-start-a-new-company-after-liquidating-my-old-one/ | liquidation | unsure | |
| /liquidation/company-pensions-and-liquidation/ | liquidation | unsure | |
| /liquidation/director-conduct-review/ | liquidation | unsure | |
| /liquidation/directors-conduct-report-2/ | liquidation | unsure | |
| /liquidation/how-much-does-liquidation-cost/ | liquidation | unsure | |
| /liquidation/how-to-challenge-a-liquidators-decisions-or-fees/ | liquidation | unsure | |
| /liquidation/how-to-choose-the-right-insolvency-procedure/ | liquidation | unsure | |
| /liquidation/how-to-prepare-for-company-liquidation/ | liquidation | unsure | |
| /liquidation/how-to-prove-your-debt-in-company-liquidation/ | liquidation | unsure | |
| /liquidation/insolvency-checklist/ | liquidation | unsure | |
| /liquidation/insolvency-myths-debunked/ | liquidation | unsure | |
| /liquidation/insolvency-vs-bankruptcy/ | liquidation | unsure | |
| /liquidation/liquidating-a-charity-or-non-profit/ | liquidation | unsure | |
| /liquidation/liquidating-a-company-with-no-assets-or-bank-account-uk/ | liquidation | unsure | |
| /liquidation/liquidating-a-group-company-or-holding-company-in-the-uk/ | liquidation | unsure | |
| /liquidation/liquidating-a-limited-liability-partnership/ | liquidation | unsure | |
| /liquidation/liquidation-deadlines-and-time-limits/ | liquidation | unsure | |
| /liquidation/liquidation-hub/ | liquidation | unsure | |
| /liquidation/liquidators-powers-and-duties/ | liquidation | unsure | |
| /liquidation/list-of-liquidation-documents/ | liquidation | unsure | |
| /liquidation/members-voluntary-liquidation/ | liquidation | unsure | |
| /liquidation/seek-insolvency-advice-before-missing-payments/ | liquidation | unsure | |
| /liquidation/timeline/ | liquidation | unsure | |
| /liquidation/uk-insolvency-flowchart/ | liquidation | unsure | |
| /liquidation/uk-insolvency-glossary/ | liquidation | unsure | |
| /liquidation/what-happens-after-company-liquidation/ | liquidation | unsure | |
| /liquidation/what-happens-if-a-creditor-takes-me-to-court/ | liquidation | unsure | |
| /liquidation/what-happens-if-a-director-hides-company-assets/ | liquidation | unsure | |
| /liquidation/what-happens-if-a-director-resigns-before-liquidation/ | liquidation | unsure | |
| /liquidation/what-happens-if-a-director-transfers-assets-before-insolvency/ | liquidation | unsure | |
| /liquidation/what-happens-if-i-stop-paying-company-debts/ | liquidation | unsure | |
| /liquidation/whats-the-risk-of-being-disqualified-as-a-director/ | liquidation | unsure | |
| /liquidation/when-should-a-director-stop-trading/ | liquidation | unsure | |
| /liquidation/which-creditors-get-paid-first/ | liquidation | unsure | |
| /manufacturing-insolvency/ | liquidation | unsure | |
| /professional-services-insolvency/ | liquidation | unsure | |
| /receivership-mean-business/ | rescue | unsure | |
| /transport-haulage-insolvency/ | liquidation | unsure | |
