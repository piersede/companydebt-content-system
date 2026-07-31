# CTA Roll-out Plan

Deploy a consistent, relevant call-to-action set across every Company Debt article,
carefully and reversibly. Companion file: `cta-rollout-manifest.md` (per-page mapping).

## Objective & scope (locked)
- **3 CTAs per article** — assessment · service · phone (the 2 July `/liquidation/` pilot pattern; trace: commit `806cf23`).
- **Category-driven**: only CTA 2 (service) varies by the article's topic; CTA 1 and CTA 3 are constant.
- **Core content only — the sidebar is never touched.**
- **Articles only.** Excluded: data/statistics pages, utility/legal pages, our landing pages, the homepage.
- Guardrails: title-case buttons · "Confidential · no obligation" · **no "24/7"** · **no "fixed fee"** · never pressure · attribution tag on every CTA.

## The 3-CTA model
| Slot | Role | Headline | Button | Destination |
|---|---|---|---|---|
| CTA 1 | Assessment (constant) | Not Sure Where the Company Stands? | Take the Free 30-Second Test | `/insolvency-calculator/` |
| CTA 2 | Service (**category-driven** — see library) | varies | varies | cluster hub |
| CTA 3 | Phone (constant) | Speak to a Licensed Insolvency Practitioner | Call 0800 074 6757 | `tel:08000746757` |

### CTA 2 library (by cluster)
| Cluster | Headline | Button | Destination |
|---|---|---|---|
| liquidation (insolvent) | A Company That Can't Pay Its Debts? | Get Liquidation Advice | `/liquidation/` |
| solvent-closure (MVL / strike-off) | Closing a Solvent Company? | Explore Your Closure Options | `/liquidation/members-voluntary-liquidation/` |
| hmrc / tax debt | Behind on Tax With HMRC? | Speak to a Tax-Debt Adviser | `/hmrc/` |
| rescue / restructuring | Is the Business Still Viable? | Explore Rescue Options | `/company-rescue-solutions/` |
| cash-flow | Struggling With Cash Flow? | Get Cash-Flow Advice | `/company-cash-flow-problems/` |
| director-liability | Worried About Personal Liability? | Get Confidential Advice | `/advice/` |
| bounce-back-loan | A Bounce Back Loan You Can't Repay? | Get Bounce Back Loan Advice | `/bounce-back-loan-support-hub/` |
| general | Worried About Your Company? | Get Confidential Advice | `/company-rescue-solutions/` |

All 8 destinations verified 200 (2026-07-30). `/hmrc/` used directly (avoids the `/hmrc-tax-problems/` 301 hop).

## Placement standard (from the pilot pattern — H2 boundaries)
Injected into the content body, evenly distributed, never two adjacent:
- **CTA 1** after the 1st substantive H2 (~¼ in)
- **CTA 2** after the middle H2 (options/process/costs, ~⅗ in)
- **CTA 3** after the last content H2, before the FAQ / Related Guides (~⅞ in)
- Articles with <4 H2s: place at 1st / middle / pre-FAQ proportionally, min. 2 sections apart. If a manual CTA already occupies a slot, skip it (no stacking).

## Mechanism — category-driven central injection
Rendered from one central library keyed by the article's category, inserted at the three
H2 boundaries by a content filter on article post-types only. One place to edit copy/links;
correct CTA 2 auto-appears per topic; **no per-page pasted blocks** (which caused today's
stale "Liquidation Quote" everywhere + duplicates). Per-article override retained.

## Phased roll-out
- **Phase 0 (this doc + manifest):** CTA library built · every page categorised into the manifest for review · existing 25-page cleanup listed (below). No deployment.
- **Phase 1 — pilot (~10 articles across 4 clusters):** deploy, full QA, sign-off on pattern + copy.
- **Phase 2 — cluster-by-cluster:** one cluster at a time, each batch QA-gated.
- **Phase 3 — long-tail / REVIEW items:** the 19 flagged pages + any unclustered.
- **Phase 4 — governance:** central registry as source of truth · attribution reporting · link-integrity checks.

## QA gate (every batch)
Right CTA 2 + working links per cluster · exactly 3 CTAs, none stacked · renders responsive
(mobile / tablet / desktop, no overflow) · **sidebar untouched** · FAQ/schema intact.

## Cleanup of the existing 25 pages (do in Phase 0/1)
Live now: a single mismatched "Get a Quick and Easy Liquidation Quote" Ultimate Blocks CTA
on 25 pages (32 blocks), with duplicates:
- **`/advice/the-risks-of-signing-a-personal-guarantee/` — 4×**
- **`/bounce-back-loan-support-hub/bounce-back-loan-fraud/` — 3×**
- **`/bounce-back-loan-support-hub/what-happens-if-i-default/` — 3×**
De-duplicate, and retire the mismatched liquidation-quote CTA on non-liquidation pages
(replace with the correct cluster CTA per the manifest).

## Open decisions (before Phase 1)
1. **19 REVIEW pages** — hubs (7), sample-letters (9), plus insolvency-news-commentary /
   debt-charities-uk / mental-health-debt-stress-support: include (which cluster?) or exclude?
2. **"general" bucket (58 pages)** is a catch-all — accept the generic CTA 2, or split further?
3. Copy sign-off on the CTA 2 library headlines/buttons above.
