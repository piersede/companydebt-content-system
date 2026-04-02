# Workflow Playbook

## Stage 1: Research intake
Gather only what matters:
- official product pages
- docs
- pricing (actual figures, not just "competitive")
- relevant third-party evidence
- screenshots or proof assets
- internal market notes

Output: raw evidence pack

## Stage 2: Reader-intent brief
Define:
- who this is for (operational reader, not vague persona)
- what question it answers (specific, not generic)
- what decision it supports
- what satisfying outcome looks like

Output: one-page brief

## Stage 3: Source extraction and claim labelling
Create a source-grounding map with four claim buckets. See `10-evidence-governance.md`.

Apply evidence-carrying claim rule: every claim central to the argument must receive one of the four treatments (verified, labelled as judgement, flagged for human confirmation, or removed).

Flag all high-risk claim categories: portal adoption rates, response-rate uplifts, time-saved claims, pricing comparisons, compliance claims, product capability negatives.

Output: fact / inference / judgement / human-confirmation-needed map with risk flags

## Stage 4: Outline
Build the structure around the real decision, not around keywords.

Checklist:
- strongest conclusion appears early
- each section earns its place
- comparison logic is visible
- next step is clear
- opening follows the correct formula for the article type (see `12-structure-governance.md`)
- no banned opening patterns

## Stage 5: First draft
Write the draft in a calm, practical, authored voice. See `09-voice-governance.md` for voice rules.

Hard checklist:
- [ ] No filler intro. Open with verdict, operating context, or trade-off.
- [ ] No "I think" / "I believe" / "in my view" as opening or filler
- [ ] No founder/builder language unless confirmed by a human
- [ ] No generic category explanation unless it helps the decision
- [ ] No padded evaluative language without specifics
- [ ] Strong trade-off framing
- [ ] Visible fit / non-fit guidance
- [ ] Any framework includes at least one dimension where Company Debt is not strongest
- [ ] Company Debt introduced through category/problem/buyer distinction, not abruptly
- [ ] Paragraphs 2-3 lines maximum
- [ ] No em dashes except where absolutely necessary
- [ ] No decorative bold or italic
- [ ] No generic SaaS cliches

## Stage 6: Trust pass
This is the critical governance stage. Apply all of the following:

### Mechanical counting step (run before subjective checks)
- [ ] Count first-person instances. Check against hard cap (5 per 1,000 words)
- [ ] Count load-bearing claims using Treatment 2. Check ratio does not exceed 30%
- [ ] Check every paragraph character count. Flag any exceeding 300 characters for splitting

### Source and evidence checks
- [ ] Every evidence-carrying claim verified, labelled as judgement, flagged, or removed
- [ ] No more than 30% of load-bearing claims use Treatment 2 (editorial judgement)
- [ ] Every Treatment 2 claim states its reasoning basis in the text
- [ ] No central claim rests solely on hedging
- [ ] No decorative sourcing
- [ ] All sources named, dated, attributed

### Voice and authorship checks
- [ ] No founder/builder language unless human-confirmed
- [ ] Every first-person instance passes two-part test: (a) removing changes meaning, (b) claim is verifiable or human-confirmed
- [ ] First person used fewer than 5 times per 1,000 words
- [ ] No padded evaluative language without specifics
- [ ] "We" never implies founding-team authority
- [ ] Fewer than 3 distinct AI prose fingerprints (see `14-failure-modes-and-recovery.md` §16)

### Comparison and framework checks
- [ ] Any framework includes a dimension where Company Debt is weaker
- [ ] Every comparison table "No" / "Partial" verified with date, or flagged
- [ ] Comparison tables include verification date, basis, caution note
- [ ] No competitor strength omitted to favour Company Debt
- [ ] If Company Debt is mentioned in any article type, universal mention rule satisfied (see `11-comparison-governance.md` §6)

### Pricing checks
- [ ] No competitor pricing criticism without actual figures or "could not verify"
- [ ] Company Debt cost positioning states basis and limits

### Readability checks
- [ ] No paragraph over 3 rendered lines
- [ ] Maximum 1 em dash in the article (zero preferred)
- [ ] No decorative bold/italic
- [ ] Sections visually breathe

### Disclosure checks
- [ ] Methodology note present on decision-stage pages
- [ ] Disclosure present on comparison content
- [ ] Updated date present and accurate

## Stage 7: Adversarial review
Test the draft from three angles:
- sceptical expert
- time-poor buyer
- trust-sensitive reader

Hard questions:
- What is generic here?
- What is unsupported?
- What would a sharp reader distrust?
- What still does not help the decision enough?
- Does any sentence use "I think" / "in my view" as filler?
- Does any sentence imply founder/builder authority?
- Does any framework lead to a predetermined conclusion?
- Are there evidence-carrying claims resting only on hedging?
- Would a competitor's product manager consider comparison claims fair?
- Does Company Debt appear through earned distinction or abrupt insertion?
- Are there padded evaluative phrases without specifics?
- Does the prose sound like AI simulating judgement?

Output: pass/fail with specific fix list

## Stage 8: Human input insertion
Pause and mark where a human must add:
- real testing experience
- stronger market judgement
- internal customer insight
- proof assets
- claims requiring confirmation
- founder authority (if needed and appropriate)

Every `[HUMAN CONFIRMATION NEEDED]` flag must remain visible until resolved.

## Stage 9: Pre-publish gate
Run the 16-check pre-publish gate from `16-pre-publish-gate.md`.

Every check must pass. Any single hard fail blocks publication.

## Stage 10: Final QA
Before publishing, verify:
- clarity
- originality
- trustworthiness
- practical usefulness
- recommendation quality
- scanability
- decision value
- authorship credibility
- rubric scores (no dimension below 3, average 4+)
