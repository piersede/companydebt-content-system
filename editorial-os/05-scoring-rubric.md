# Scoring Rubric

Score each category from 1 to 5.

## 1. Clarity
Is the page easy to understand quickly?
- 5: Every section is immediately clear. No re-reading needed.
- 4: Mostly clear with minor ambiguity in one area.
- 3: Understandable but some sections require effort.
- 2: Multiple sections are unclear or convoluted.
- 1: Reader would struggle to extract the main point.

## 2. Originality / Information gain
Does it add real information beyond generic SaaS content?
- 5: Genuine insight. The reader learns something they would not find in five competitor pages.
- 4: Adds useful framing or synthesis, even if some elements are familiar.
- 3: Competent but mostly covers what other sources cover.
- 2: Largely generic with only minor additions.
- 1: Could be any SaaS content page. No information gain.

## 3. Trustworthiness
Are sourcing, confidence, and disclosures handled honestly?
- 5: Every claim sourced or labelled. Uncertainty visible. Disclosures present. No inflated certainty.
- 4: Strong sourcing with minor gaps. Disclosures present.
- 3: Adequate sourcing but some claims lean on hedging. Disclosures present.
- 2: Multiple unsupported claims. Missing disclosures.
- 1: Significant unsupported claims. No methodology note. Missing disclosures.

**Hard rule:** Trustworthiness must be 4 or 5 on decision-stage pages (reviews, comparisons, buyer guides).

## 4. Practical usefulness
Does it help a real reader act?
- 5: Reader can take a specific action or make a specific decision after reading.
- 4: Reader is significantly closer to a decision.
- 3: Reader has better understanding but still needs more information.
- 2: Provides context but no actionable guidance.
- 1: Reader leaves without knowing what to do differently.

## 5. Insight
Does it say something sharper than generic category content?
- 5: Contains at least one judgement or framing that a reader would genuinely find valuable.
- 4: Offers useful editorial perspective beyond the obvious.
- 3: Competent analysis but no standout insight.
- 2: Largely restates obvious points.
- 1: No editorial perspective. Pure description.

## 6. Recommendation quality
Are recommendations supportable, specific, and useful?
- 5: Clear, specific recommendation with stated reasoning and caveats.
- 4: Good recommendation with minor gaps in reasoning.
- 3: Recommendation present but vague or weakly supported.
- 2: Recommendation unclear or poorly supported.
- 1: No recommendation or recommendation contradicted by the analysis.

## 7. Authorship credibility
Does it feel written by a real accountable editor, or like AI simulating one?
- 5: Unmistakably authored. Sharp judgement. No synthetic patterns.
- 4: Mostly authored with minor synthetic patches.
- 3: Competent but reads like polished AI in places.
- 2: Frequently sounds like AI. Multiple synthetic patterns.
- 1: Reads entirely like AI-generated content.

**Scoring guidance:** Check for synthetic first person, padded evaluation, founder drift, generic transitions, and over-polished prose. See `14-failure-modes-and-recovery.md`.

## 8. Scanability
Can a busy reader extract the answer fast?
- 5: Main answer in first 3 sections. Clear subheads. Short paragraphs. Easy to navigate.
- 4: Good structure with minor scanning friction.
- 3: Adequate structure but some sections require full reading.
- 2: Dense sections. Subheads generic. Hard to scan.
- 1: Wall of text. Reader must read everything to find the answer.

## 9. Reader satisfaction
Would the right reader feel this page answered the real question?
- 5: Reader leaves satisfied. Question answered. Decision supported.
- 4: Reader mostly satisfied. Minor gaps.
- 3: Reader has a better understanding but feels something is missing.
- 2: Reader frustrated by vagueness or incompleteness.
- 1: Reader wasted their time.

## 10. Decision value
Does it improve a real decision?
- 5: Reader can make a better decision because of this page.
- 4: Reader's decision is meaningfully informed.
- 3: Reader has more context but the decision is not clearly supported.
- 2: Limited decision value.
- 1: No decision value.

**Hard rule:** Decision value must be 4 or 5 on comparison, review, and buyer pages.

## Publish threshold

Hard rules (no exceptions):
- No score below 3 in any category
- Average target: 4+
- Trustworthiness must be 4+ on decision-stage pages
- Decision value must be 4+ on comparison, review, and buyer pages
- Authorship credibility must be 3+ on all content (hard minimum), 4+ on decision-stage pages (reviews, comparisons, buyer guides)

Note: authorship credibility of 3 means "competent but reads like polished AI in places." On decision-stage pages where trust is critical, this is not good enough. These pages require 4+ ("mostly authored with minor synthetic patches").

If any dimension scores below 3, the article must not be published until it is revised upward.

See `16-pre-publish-gate.md` for the full pre-publish gate.

---

## Commercial comparison trust checks

*Apply this section to any vendor-authored comparison, alternatives, review, or decision-stage page.*

| # | Check | Pass | Fail |
|---|---|---|---|
| T1 | Is the page mode explicit? | Mode declared (independent-style or vendor-perspective) before drafting | No mode declaration; posture unclear |
| T2 | Is the commercial relationship disclosed early? | Perspective disclosure appears before substantive comparison begins | Disclosure buried below the analysis or absent |
| T3 | Is the category frame fair? | Frame tested for neutrality; distinctions justified | Frame defines the problem only in terms most favourable to the publisher |
| T4 | Does the page preserve real reader choice? | Multiple valid paths presented with conditions | Only one commercially convenient path preserved |
| T5 | Does the house product have explicit not-fit conditions? | Best fit, not a fit, and required conditions all present | House product presented without limiting conditions |
| T6 | Would the article still be useful without the house product section? | Article coherent and valuable if house-product section removed | Article collapses conceptually without the house product |

### Trust-failure cap

Any failure on T1–T6 caps the Trustworthiness dimension (§3) at a maximum of 3, regardless of other trust signals. This means:
- The article cannot meet the hard rule (Trustworthiness 4+ on decision-stage pages)
- Publication is blocked until the trust failure is resolved
- Strong structure, expertise, and depth do not compensate for weak trust design

**Scoring logic:**
- 0 failures: trust architecture passes
- 1 failure: trust architecture warning; fix before publish
- 2+ failures: trust architecture fail; structural rewrite required

---

## Alternatives-page integrity scoring

*Apply this section only to articles of type: alternatives, competitor comparison, or BOFU category pages.*

Score each item 1 (fail) or 0 (pass). Any 2 failures caps the article at "needs rewrite". Any 4 failures triggers structural fail and blocks publication.

| # | Criterion | Pass | Fail |
|---|---|---|---|
| A1 | Replacement vs augmentation distinguished before naming any tool | Decision frame explicit before first product mention | First product appears without prior classification |
| A2 | First fold contains a usable decision block | At-a-glance block (keep / replace / add) present within first screen | No decision block; reader must read the article to understand their path |
| A3 | Article avoids vendor-summary drift | Structure follows decision logic, not a catalogue of tool descriptions | Article is effectively a series of vendor summaries |
| A4 | Market-pattern claims sourced or marked as judgement | All frequency/trend claims either cited or labelled Treatment 2 with stated basis | Banned phrases present without source or bounded judgement |
| A5 | House product introduced after decision frame | BusinessExpert appears after replacement-vs-augmentation is explicit | BusinessExpert introduced as a natural next step before frame is established |
| A6 | House product includes "not the right fit if…" condition | At least one explicit limiting condition for BusinessExpert | BusinessExpert presented as universally appropriate |
| A7 | Conclusion answers buyer question before CTA | Editorial conclusion complete before any call to action | Conclusion collapses into pitch |
| A8 | Sceptical reader test | A reader who does not use BusinessExpert can understand the category and make a decision | Article only makes sense if reader is already predisposed to BusinessExpert |

**Thresholds:**
- 0–1 failures: passes alternatives integrity check
- 2–3 failures: article capped at draft; requires rewrite before publish
- 4+ failures: structural fail; article must be rebuilt from the alternatives-page-outline template
