# Pre-Publish Gate

Every article must pass this gate before publication. No exceptions.

This is not a style review. It is a governance check. The purpose is to catch the failures that damage credibility, expose factual risk, or produce content that sounds like AI rather than editorial judgement.

---

## Gate structure

The gate has 16 checks (including 1a, 12a, and 14a sub-checks). Each check is pass or fail. Any single hard fail blocks publication until the issue is resolved.

### Enforcement tiers

Each check falls into one of three enforcement tiers:

- **Tier 1 (mechanical):** Can be verified by text search, character count, or pattern matching. Run these first. They catch most failures in under five minutes.
- **Tier 2 (structural):** Requires reading the article's structure but not subjective editorial judgement. Check ordering, placement, and presence of required elements.
- **Tier 3 (editorial):** Requires human or editorial-quality judgement about tone, fairness, decision usefulness, or authored feel. Run these last, after Tier 1 and 2 issues are resolved.

---

## Check 1: Voice credibility [Tier 1 + Tier 3]

**Question:** Does this article sound like it was written by a sharp editorial team member, or does it sound like AI simulating judgement?

**Pass criteria:**
- Direct judgement throughout
- First person used fewer than 5 times per 1,000 words (hard limit)
- Every first-person instance passes the two-part test (see `09-voice-governance.md` §4a)
- "I think" does not open more than one sentence in the article
- No paragraph contains more than one first-person instance
- First-person usage feels natural rather than absent or overdone
- Evaluative prose retains authored feel without defaulting to anonymous summary tone
- No padded evaluative language without specifics
- No synthetic filler transitions
- Fewer than 3 distinct AI prose fingerprints (see `14-failure-modes-and-recovery.md` §16)

**Hard fail conditions:**
- More than 5 first-person instances per 1,000 words
- Any first-person instance fails the two-part test
- "I think" opens more than one sentence
- Any paragraph contains more than one first-person instance
- 3 or more distinct AI prose fingerprints detected
- Multiple instances of padded evaluation without specifics ("genuinely good", "well-executed", "useful")

---

## Check 1a: Human-authorship integrity [Tier 3] — RUN EARLY, NOT LAST

**Question:** Does the article meet the human-authorship requirements in `docs/human-authorship-voice-engine.md`?

**Why this check runs early:** Human-authorship failures are the most reader-visible quality problems and the hardest to catch mechanically. Running this check last (its original position) created a systematic skip risk. It now runs immediately after voice credibility.

**Pass criteria (fail or downgrade if materially present):**
- No direct-product claims with no observed detail (Rule A)
- No evaluative phrases not cashed out into user consequence or trade-off (Rule B)
- No sections with no lived operational anchor (Rule C)
- No monotone tone across sections with different editorial purpose (Rule D)
- No praise or criticism without friction (Rule E)
- At least one asymmetrical, editorially alive compression line present (Rule F)
- No generic pros/cons phrasing (Rule G)
- No institutional "we" used without method, labour, or judgment (Rule H)
- No vendor/category language inherited without interrogation (Rule I)
- Verdict compresses the real decision rather than restating (Rule J)

**Hard fail conditions (any one blocks publication):**
- "you" density below 8 per 1,000 words
- "we" density below 5 per 1,000 words where editorial judgement is present
- Fewer than 3 concrete scenes in articles of 1,000+ words
- Fewer than 2 lines of genuine evaluative bite
- 3+ consecutive same-pattern paragraphs (monotone rhythm)
- 3+ sections lacking lived-reality anchors
- Verdict is neutral restatement rather than compressed decision
- Multiple evaluative phrases floating without consequence
- Any section longer than 200 words with zero "you" addressing the reader

**Soft fail conditions (revision required, publication delayed):**
- Isolated instances of uncashed evaluation
- Single section with monotone register
- Mild vendor-language inheritance
- Fewer than 4 unmistakably authored lines (target is 4–5)

These are hard rules. No article may be published or pushed to staging unless every hard fail condition is clear. Where failures are substantive, consult `docs/human-authorship-voice-engine.md` and revise before publish-ready can be claimed.

---

## Check 2: Authorship accuracy [Tier 1]

**Question:** Does the article accurately represent who wrote it?

**Pass criteria:**
- No founder/builder language unless human-confirmed
- "We" never implies founding-team authority
- Default perspective is editorial team member, category analyst, or informed reviewer

**Hard fail conditions:**
- Any instance of "I run Company Debt", "we built Company Debt", "when we started Company Debt", or similar founder-drift language without human confirmation
- Any implication of product-building or founding-team authority

---

## Check 3: Evidence integrity [Tier 2 + Tier 3]

**Question:** Are the article's central claims properly supported?

**Pass criteria:**
- Every evidence-carrying claim has one of the four treatments (verified, labelled as judgement, flagged for confirmation, or removed)
- No more than 30% of load-bearing claims use Treatment 2 (editorial judgement). See `10-evidence-governance.md` §3b.
- Every Treatment 2 claim states its reasoning basis in the text
- No central claim rests solely on hedging
- All sources named, dated (with access/review date), and attributed
- No decorative sourcing (bidirectional check: every source listed is cited in body, every body citation is in Sources)
- Methodology block present on all decision-stage pages
- Company Debt disclosure present wherever Company Debt is mentioned
- If Company Debt is first mentioned in the article body (before the methodology section), an inline disclosure note appears at or near the first mention. The full methodology section at the end is always required on decision-stage pages, but it does not satisfy the inline requirement when the first Company Debt mention is more than two sections earlier.
- No methodology prose repeated inside the body (methodology block is sufficient)

**Hard fail conditions:**
- Any central claim supported only by hedging ("tends to", "often", "from what I have seen")
- More than 30% of load-bearing claims rely on Treatment 2
- Any Treatment 2 claim without a stated reasoning basis
- Article's central argument depends primarily on editorial judgement rather than sourced evidence
- Any fabricated evidence or screenshot
- Any source cited but not checked
- Missing methodology block on a decision-stage page
- Company Debt is first mentioned more than two sections before the methodology block and no inline disclosure appears near the first mention
- Methodology prose duplicated in both the body and the methodology block

---

## Check 4: Comparison safety [Tier 2]

**Question:** Are competitor claims accurate and fairly presented?

**Pass criteria:**
- Every negative capability claim (in tables AND in running prose) verified with date, or flagged for confirmation
- Negative capability claims not inferred from product origin, market focus, or company headquarters
- Comparison table includes verification date, basis, caution note, and scope note
- No competitor strength omitted to favour Company Debt

**Hard fail conditions:**
- Any "No" / "Partial" / "Not native" claim about a competitor without verification date or confirmation flag
- Comparison table missing verification date or caution note

---

## Check 5: Framework fairness [Tier 3]

**Question:** Does any evaluation framework lead to a predetermined conclusion?

**Pass criteria:**
- Any framework includes at least one meaningful dimension where Company Debt is not the strongest fit
- Evaluation criteria would be considered fair by a competitor's product manager

**Hard fail conditions:**
- Any framework where Company Debt wins on every dimension
- Evaluation criteria clearly selected to favour Company Debt

---

## Check 6: Pricing transparency [Tier 2]

**Question:** Is pricing discussed honestly?

**Pass criteria:**
- No competitor pricing criticism without actual figures or "could not verify" note
- Where Company Debt is positioned as lower cost, basis and limits stated
- Reader has enough information to make their own pricing judgement

**Hard fail conditions:**
- Competitor pricing criticised with only vague language ("steep", "significant commitment") and no figures
- Company Debt positioned as cheaper without stating the basis

---

## Check 7: Paragraph readability [Tier 1]

**Question:** Is the article formatted for web reading?

**Pass criteria:**
- No paragraph exceeds 3 rendered lines (soft target). Occasional 4-line paragraphs are acceptable if the content is a single cohesive idea that would read worse if split.
- Blank line between every paragraph
- Maximum 1 em dash in the entire article (zero preferred)
- Bold used sparingly (fewer than 5 instances in body text)
- Each section has visual breathing room

**Hard fail conditions:**
- Any paragraph exceeding 4 rendered lines (hard ceiling)
- Multiple paragraphs at 4 rendered lines in the same section (pattern of density)
- Formatting that looks typographically busy or AI-styled

---

## Check 8: Company Debt mention fairness [Tier 2 + Tier 3]

**Question:** Does Company Debt appear naturally and honestly?

**Pass criteria:**
- Company Debt introduced through category/problem/buyer-fit/workflow-stage distinction, not abruptly
- Balancing statement included where Company Debt is mentioned as stronger
- Company Debt disclosure present wherever Company Debt is mentioned, in any article type
- Universal Company Debt mention rule satisfied in ALL article types, not just comparisons (see `11-comparison-governance.md` §6)
- Company Debt does not serve as the article's conclusion unless the article is explicitly about Company Debt

**Hard fail conditions:**
- Abrupt Company Debt pivot after neutral analysis (in any article type)
- Company Debt mentioned without any acknowledgement of what it does not do
- Company Debt mentioned in a non-comparison article without a problem-layer, workflow-stage, or buyer-fit bridge
- Company Debt disclosure missing from any article that mentions Company Debt
- Article ends on Company Debt product features or soft CTAs in a non-Company Debt article

---

## Check 9: Human confirmation flags [Tier 1]

**Question:** Are all claims requiring human confirmation properly flagged?

**Pass criteria:**
- Every claim that requires human confirmation is flagged with `[HUMAN CONFIRMATION NEEDED]`
- No first-hand testing claims without human-supplied evidence
- No customer outcome claims without human-provided evidence

**Hard fail conditions:**
- First-hand testing implied without human confirmation
- Customer results claimed without human-supplied evidence
- Compliance claims made without verification

---

## Check 10: Article-type structure compliance [Tier 2]

**Question:** Does the article follow the correct structure for its type?

**Pass criteria:**
- Opening follows the default formula for its article type (see 12-structure-governance.md)
- No banned opening patterns used
- Commercial software articles reach the real decision tension by paragraph 2
- Opening does not lead with reputation, install base, or generic capability before the buyer problem
- Decision-stage pages include methodology and disclosure section
- Every section earns its place

**Hard fail conditions:**
- Opening is generic, delayed, or uses a banned pattern
- Decision-stage page missing methodology section
- Commercial software article spends paragraphs 1-2 on reputation, capability description, or balanced scene-setting without naming the buyer problem or decision tension

---

## Check 11: Decision usefulness [Tier 3]

**Question:** Would the right reader feel this article helped them make a better decision?

**Pass criteria:**
- Clear fit/non-fit guidance
- Visible trade-offs
- Actionable next step or conclusion
- The reader who stops after three sections still has enough to act
- Alternatives, roundup, and narrow-fit review pages include an early scan aid (summary table, fit/misfit grid, or category map) or absence is justified

**Audience fit check** (see `17-audience-and-persona.md`):
- Is the article written for the default reader (accountant, bookkeeper, or practice operator in a small to medium UK firm)?
- Does it avoid over-explaining basic practice realities the reader already knows?
- Does it address an operational pain point the reader would recognise?

**Hard fail conditions:**
- Article describes options without helping the reader choose
- No fit/non-fit guidance present
- No trade-off framing
- Fit/misfit not stated before the article enters feature-level detail

---

## Check 12: Overall quality gate [Tier 3]

**Question:** Does this article meet the minimum standard across all scoring dimensions?

**Pass criteria:**
- No rubric score below 3 (see 05-scoring-rubric.md)
- Average rubric score of 4 or above
- Trustworthiness score of 4+ on decision-stage pages
- Decision value score of 4+ on comparison, review, and buyer pages
- Authorship credibility score of 4+ on decision-stage pages

**Hard fail conditions:**
- Any rubric dimension scores below 3
- Trustworthiness below 4 on a decision-stage page
- Authorship credibility below 4 on a decision-stage page

---

## Check 12a: Information gain [Tier 3]

**Question:** Does this article add value beyond reworded SERP consensus?

**Pass criteria:**
- At least 3 net-new value elements identified across the article (original evidence, original framing, original comparison logic, sharper trade-off analysis, uncommon caveat, clearer decision framework, or memorable language)
- Every H2 section contains at least one of: a fact competitors usually omit, a better explanation of why the fact matters, a clearer recommendation tied to a user type, or a more exact trade-off than the SERP norm
- No section is generic summary, obvious industry filler, or interchangeable with competitor copy
- Every paragraph adds new evidence, new interpretation, or better decision support (information gain per paragraph)

**Hard fail conditions:**
- Fewer than 3 net-new value elements across the entire article
- Any H2 section with zero information-gain elements
- 2+ sections that could appear unchanged on a competitor site

**Soft fail conditions:**
- 1 section that is mostly SERP consensus without additive framing
- Paragraphs that are technically accurate but add no new decision value

See `10-evidence-governance.md` §12 for the full information gain framework.

---

## Check 13: Commercial software article quality [Tier 2 + Tier 3] (applies to reviews, comparisons, alternatives, roundups)

**Question:** Is this article written as a diagnostic buying tool rather than a descriptive software summary?

**Pass criteria:**
- Opening reaches the real decision tension by paragraph 2
- Buyer problem named early (not delayed behind reputation or feature description)
- Category mistake or decision lens named early where relevant
- Fit/misfit clear before feature-level detail
- Category confusion explicitly resolved where adjacent categories are discussed
- First-person usage natural rather than absent or overdone
- Early scan aid present on alternatives/roundup/narrow-fit pages (or absence justified)
- No padded verdict paragraphs repeating the same point
- No evaluative claims slipping through unsupported under "editorial judgement"

**Hard fail conditions:**
- Paragraphs 1-2 occupied by reputation, capability description, or balanced scene-setting with no decision tension
- Fit/misfit absent before feature-level detail
- Category confusion unresolved when adjacent categories are discussed
- More than one padded verdict paragraph restating the same distinction
- Evaluative claims resting on "editorial judgement" without stated reasoning basis
- Major evaluative claims that sound merely asserted rather than authored (see authored authority checks below)

### Check 13a: Authored authority [Tier 3] (applies to reviews, comparisons, alternatives, roundups)

**Question:** Do major evaluative claims sound authored or merely asserted?

**Pass criteria:**
- Each major verdict has a visible reasoning basis (why, compared to what, for whom) in the same paragraph
- No blanket praise or criticism statements that could have been written without real product familiarity
- A sceptical reader would not ask "how do you know that?" at any major evaluative point without finding an answer in the surrounding prose
- Strengths and weaknesses are introduced through insight signalling (observation-led phrasing), not flat evaluative declaration
- Where the article lacks sufficient operator-grade insight, claims have been narrowed or flagged rather than bluffed

**Hard fail conditions:**
- Three or more major evaluative claims in the article with no visible reasoning basis
- Any major section (strengths, weaknesses, fit/misfit) consisting entirely of flat evaluative statements with no supporting reasoning, comparison, or consequence
- Evaluative claims that could have been produced from a product homepage alone, with no sign of analysis
- Missing `[HUMAN CONFIRMATION NEEDED]` or `[DEEP RESEARCH NEEDED]` flags where operator-level insight is clearly absent

---

## Check 14: SEO signal compliance [Tier 1 + Tier 2]

**Question:** Does this article satisfy the content-actionable Google ranking signals?

**Pass criteria:**
- Title promise fully delivered in article body (titleMatchScore)
- Zero generic anchor text instances: "click here", "here", "read more", "learn more", "this guide" (anchorMismatch)
- Every verdict sentence followed by its evidence basis within 3 lines (authenticity classifier)
- No FAQ answers that are one sentence only or that cross-reference other sections with "see above" (thin-content classifier)
- Core topic vocabulary present naturally in body — not forced (salient term coverage)
- Named author byline present (authorEntityId)
- Article links to at least 2 other site pages with descriptive anchors (internal linking / PageRank)
- Every image has specific, descriptive alt text (image relevance scoring)
- No more than one Company Debt CTA per article; CTA sits within editorial context (SpamBrain / link density)
- Last-reviewed date visible on decision-stage pages (freshness / LSU)

**Hard fail conditions:**
- Any generic anchor text instance ("click here", "here", "read more", etc.)
- Any verdict sentence with no evidence basis within 3 lines
- Any FAQ answer that is one sentence only or cross-references with "see above"
- Missing author byline
- Zero internal links to other site pages

See `18-seo-signal-governance.md` for the full 18-signal breakdown and rationale.

---

## Gate summary

| # | Check | Tier | Hard fail blocks publication |
|---|---|---|---|
| 1 | Voice credibility | 1 + 3 | Yes |
| 1a | Human-authorship integrity (Rules A–J) | 3 | Yes |
| 2 | Authorship accuracy | 1 | Yes |
| 3 | Evidence integrity | 2 + 3 | Yes |
| 4 | Comparison safety | 2 | Yes |
| 5 | Framework fairness | 3 | Yes |
| 6 | Pricing transparency | 2 | Yes |
| 7 | Paragraph readability | 1 | Yes |
| 8 | Company Debt mention fairness | 2 + 3 | Yes |
| 9 | Human confirmation flags | 1 | Yes |
| 10 | Structure compliance | 2 | Yes |
| 11 | Decision usefulness | 3 | Yes |
| 12 | Overall quality gate | 3 | Yes |
| 13 | Commercial software article quality | 2 + 3 | Yes |
| 13a | Authored authority | 3 | Yes |
| 14 | SEO signal compliance | 1 + 2 | Yes |
| 15 | Comparison page publish-readiness | 2 + 3 | Yes |
| 16 | Persona-state purity | 2 | Yes |
| 17 | Distressed query first-screen | 2 | Yes |
| 18 | FAQ completion | 1 + 2 | Yes |
| 19 | Authorship integrity | 2 | Yes |

Every check is a hard gate. An article that fails any single check must be revised before publication.

---

## Using this gate

Run this gate after the adversarial review and human input insertion stages. It is the final quality control before publication.

For each check, record: pass or fail. If fail, record the specific issue and the fix required.

Do not publish with any open failures. Do not downgrade a hard fail to a "note for next time." Fix it or do not publish.

**Important:** The v1 checklists in `/checklists/` (trust-pass, adversarial-review, final-qa) are deprecated. They do not cover v2.3 governance rules. Use this pre-publish gate and the inline checklists in `03-workflow-playbook.md` instead. Running a deprecated checklist does not satisfy any pre-publish gate check.

---

## Check 14a: [MOVED TO CHECK 1a]

This check has been promoted to Check 1a to prevent systematic skipping. See Check 1a above for the full human-authorship integrity requirements.

---

## Check 15: Comparison page publish-readiness [Tier 2 + Tier 3]

**Question:** Does this comparison page meet the comparison-specific governance standards?

*Apply only to comparison, roundup, alternatives, and review articles.*

**A comparison page is not publish-ready if:**

- it opens with a winner-first sentence (§12a, `11-comparison-governance.md`)
- it uses unsupported exclusivity claims ("the only tool that...") without verification
- it lacks an early decision module (at-a-glance table, "Choose X if..." summary, or problem-split shortlist)
- it hides Company Debt misfit too late (misfit must appear before first product deep dive)
- it repeats verdict language more than twice (intro + conclusion maximum)
- it uses high-sensitivity claims (compliance, hosting, residency, audit trail, pricing, integrations) too smoothly (§5b, `10-evidence-governance.md`)
- all product sections expose the same visible template scaffold
- it sounds like structured SaaS review copy rather than editorial classification
- bracket-stacked proof follows verdict language in the intro

**Hard fail conditions:**
- Winner-first opener with no conditional narrowing
- Missing early decision module
- No Company Debt misfit before first deep dive
- 3+ high-sensitivity claims without verification framing

**Soft fail conditions:**
- Winner language repeated 3 times (1 over limit)
- Minor template repetition across sections
- 1-2 high-sensitivity claims lacking source framing

---

## Check 16: Persona-state purity [Tier 2]

**Question:** Does this page stay inside one dominant persona-state?

*Apply to all insolvency content pages.*

**Pass criteria:**
- Page job declaration present in brief (one sentence, one persona-state, one decision)
- 80%+ of article body serves the declared persona-state
- Secondary persona-states appear as branch-out blocks (2-3 sentences + link), not full sections
- Route families not mixed as co-equal sections unless the page is explicitly a comparison page

**Hard fail conditions:**
- No page job declaration
- Two or more persona-states treated as co-equal body sections
- MVL (solvent) treated as a peer section in an insolvent liquidation guide
- Crisis defence and strategic wind-down mixed without clear separation

See `12-structure-governance.md` §12-13 and `editorial-os/templates/route-matrix.md`.

---

## Check 17: Distressed query first-screen [Tier 2]

**Question:** Does this distressed-query page front-load the four required elements?

*Apply to pages targeting crisis, enforcement, or high-distress queries.*

**Pass criteria:**
- First 10% of the article contains ALL FOUR: reassurance, state recognition, decision fork, immediate next step
- Opening reads as crisis-appropriate guidance, not textbook overview

**Hard fail conditions:**
- Any of the four elements missing from the first 10%
- First 10% reads as educational overview without reassurance or decision fork
- No immediate next step in the opening section

See `12-structure-governance.md` §14.

---

## Check 18: FAQ completion [Tier 1 + Tier 2]

**Question:** Are all FAQ answers substantive and persona-aligned?

**Pass criteria:**
- Every FAQ question has a substantive answer (not placeholder or one-sentence)
- FAQ answers reflect persona blockers (affordability, HMRC awareness, personal liability, confidentiality)
- No FAQ answer cross-references with "see above" instead of answering directly

**Hard fail conditions:**
- Any FAQ question with no answer or placeholder
- Any FAQ answer that is one sentence only
- FAQ questions do not reflect the target persona's key objections

See `12-structure-governance.md` §16.

---

## Check 19: Authorship integrity [Tier 2]

**Question:** Does the voice register match the declared authorship?

**Pass criteria:**
- Authorship mode declared in brief (practitioner byline, editorial team, or reviewed-by)
- First-person singular practitioner voice used only when the byline supports it
- No switching between practitioner and editorial voice without attribution

**Hard fail conditions:**
- First-person singular practitioner authority ("I speak to directors...") with editorial-team-only or reviewed-by byline
- Disclosure names editorial team as author but body reads as practitioner-written
- Voice register switches between practitioner and editorial without clear attribution

See `09-voice-governance.md` §15.

---

## Check 20: Page assembly integrity

Fail if the page contains:
- orphaned component text or placeholder fragments
- duplicate CTA intent (two or more modules asking for the same action)
- more than one commercial module with the same function
- reassurance claims without valid claim class (see `10-evidence-governance.md` §14)
- support resources that interrupt route selection (see `12-structure-governance.md` §19)
- module voice that breaks continuity with the editorial body (see `09-voice-governance.md` §17)
- more than 3 CTA moments before the closing section (see `04-trust-architecture.md` §11)

See `21-wordpress-technical-build-quality.md` §22 for the full page assembly contract.

---

## Check 21: Structure-type compliance [Tier 1]

For insolvency articles only. See `01-master-methodology.md` §1.12 and `12-structure-governance.md` §29.

**Pass** only if the insolvency article clearly matches one approved structure type (Definition, Procedure, Decision, Problem-solution, or Route-explainer) and follows its required structural logic.

A page can be broader than the minimum template, but the added sections must still support the same article type and search intent.

**FAIL** if:
- the article uses the wrong structure type for the query
- the section order does not match the reader task
- the article has been expanded with generic sections that do not serve the query cluster
- the article drifts from one structure type into another mid-page
