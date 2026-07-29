# Winding-up petition: site-wide consistency audit

**Date:** 29 July 2026
**Trigger:** Section 6 ("Site-Wide Consistency Fixes") of the winding-up-petition master implementation brief.
**Scope:** every page in `drafts/` carrying one of the six claim patterns the brief flags, plus the stale petition fee.
**Source of truth used:** `research/winding-up-petitions/master-implementation-brief.md`, sections 6, 6A and 6B.

Note on scope: this audits the local drafts, which are the editorial source of truth. Some drafts are known to be
ahead of staging (see the draft/staging link deploy gap). Nothing here has been pushed anywhere.

---

## A. Fixed in this pass

Sentence-level factual corrections. No page was restructured and no page's argument changed.

| Page | Defect | Correction |
|---|---|---|
| `77146_debt-creditor-pressure-hub.html` | £343 court fee (stale); "Official Receiver deposit"; "debt over £750" | £352 court fee; "petition deposit"; "debt of £750 or more" |
| `67962_what-is-a-statutory-demand-against-a-company.html` | "Bank accounts freeze automatically under section 127"; advertisement stated as a single 7-working-day limb | Freeze reframed as a bank risk decision; both limbs of rule 7.10 stated; s127 made contingent on a later order |
| `79322_winding-up-petition-vs-compulsory-liquidation.html` | "all property dispositions after the petition presentation date are void"; banks freeze "immediately" | s127 made contingent on a later winding-up order; freeze timing de-absolutised |
| `79351_can-i-choose-my-liquidator.html` | "section 127 makes most dispositions void from the petition date" | Made contingent on a winding-up order following |
| `65614_closing-a-limited-company.html` | Freeze "within 24 hours"; Official Receiver appointed on the *petition* | Timing de-absolutised; OR appointment correctly tied to the order |
| `79379_business-bank-account-in-liquidation.html` (3 places, incl. an FAQ answer) | "within 24 hours", "often the same day" as a general rule | Replaced with "it varies, there is no fixed rule", mechanism retained |
| `79615_can-a-supplier-force-my-company-into-liquidation.html` | Freeze "within 24 hours of advertisement" | Timing de-absolutised |

The £343 fee was present only on the hub. It is the last instance in the cluster.

## B. Already correct, no action needed

- **CVA does not automatically stay a petition.** `15141_vs-cva.html` and
  `79295_...which-to-choose.html` both already state this correctly. The brief's concern does not apply to them.
- **s127 stated conditionally.** `79379` (the section-127 explainer H2), `79615:212` and
  `77181_energy-provider-insolvency.html` already use "potentially void" or tie the effect to a compulsory winding-up.
- **£800 preferential wage limit.** Ten pages carry this figure. It is correct as a Schedule 6 preferential limit and
  is not a defect in itself. The brief's objection is specific to the *main petition page*, which merged it with
  the RPS weekly cap. Only that page needed the fix, and the rewrite handles it.

## C. Flagged, NOT fixed: needs a decision or its own pipeline pass

These are real defects but each one changes a page's substantive advice, so a one-line patch is the wrong instrument.

### C1. Notice of Intention page contradicts Schedule B1 para 25(a) — highest priority

`drafts/74439_notice-of-intention-to-appoint-administrators.html`, lines 16, 36, 65, 73, 98.

The page presents the NOI as an "emergency brake" to pull when a winding-up petition is about to be heard:

> "If a winding-up petition is about to be heard [...] filing an NOI stops everything in its tracks."
> "Any petition already before the court is stayed."
> "If a petition has been advertised in the London Gazette and the hearing is days away, the NOI stays the petition."

Schedule B1 paragraph 25(a) of the Insolvency Act 1986 blocks a paragraph 22 appointment (by the company or its
directors) while a winding-up petition is presented and undisposed of. The out-of-court route the whole page
describes is the one route that is *not* available in the scenario the page recommends it for. A director following
this page's advice after a petition has been presented would be pursuing a route the statute closes to them; the
answer in that situation is an in-court administration application, which is a different process with different cost
and timing.

This is the single most consequential finding in the audit. It needs a solicitor-reviewed revision of that page, not
an edit from me.

### C2. Administration framed as automatic protection against a pending petition

`drafts/79295_company-voluntary-arrangement-vs-administration-which-to-choose.html:125`:

> "Administration provides automatic protection against petitions. If a petition is already filed, administration is
> usually the safer route."

Same underlying error as C1, expressed as a recommendation. Correct position: an outstanding petition determines
*which* appointment route is available, and the in-court route may be required. Related framing on
`65483_company-administration.html` (lines 12, 249, 264) is looser but reads as though the moratorium is
straightforwardly reachable once a petition is filed.

### C3. CVL sold as producing a cleaner conduct outcome

- `7669_liquidation.html:45, 124`
- `79537_can-a-director-be-sued-personally-by-creditors.html:305` ("directors who initiate voluntary liquidation
  consistently receive cleaner conduct reports than those forced into it by a creditor petition")
- `77207_manufacturing-insolvency.html:463, 637, 645`

Conduct is investigated and reported in both compulsory liquidation and CVL. What genuinely improves a conduct
report is acting early, because it changes the underlying facts, not the label on the procedure. The claims are
salvageable by re-anchoring them to timing rather than route, but that is a voice-and-argument edit on three pages
and several are commercially load-bearing, so it should go through the pipeline.

### C4. "Companies Court" naming

Eight pages use the former name: `24434`, `25310`, `68120`, `76323`, `7687` (fixed by the rewrite), `78673`,
`78707`, `79580`. The current name is the Insolvency and Companies List. Low priority, mechanical, but worth a
single sweep rather than drip-feeding.

## D. Not found

- No page states a **7 to 14 day** hearing window except the main petition page (fixed by the rewrite) and
  `68134_creditor-negotiations.html`, where the phrase relates to creditor response times, not a court listing.
- No page claims directors can use the **out-of-court administration route despite an outstanding petition** in
  those words; the defect appears as the implication documented at C1 and C2 instead.
- No remaining **£343** fee outside the hub.

---

## Recommended order of work

1. C1 (NOI page) — legally wrong advice on a decision page, and it is the kind of error a reader acts on.
2. C2 — same error class, smaller surface.
3. C3 — commercial claim that will not survive scrutiny.
4. C4 — mechanical sweep.
