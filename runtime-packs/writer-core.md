# Writer Core

Compact drafting pack for Company Debt article production.

This pack is an execution layer, not the canonical source of truth. Canonical ownership remains in `editorial-os/`.

## Use this during

- first drafts
- substantive rewrites
- structural rewrites
- voice passes where the body changes materially

Add an article-type overlay on top of this pack when relevant.

## Non-negotiable quality bar

- Write people-first, decision-useful, trustworthy content.
- Optimise for clarity, authorship, and decision value.
- Make trade-offs visible.
- Distinguish verified facts from judgement, inference, and unresolved claims.
- Do not invent first-hand testing, screenshots, customer experience, or feature certainty.

## Rule priority (when two voice rules conflict)

Payoff-intent-first (`editorial-os/24-payoff-intent-first.md`) beats voice cleverness (`docs/human-authorship-voice-engine.md` Rule F, asymmetrical editorial lines). If a compressed clever line would ask the reader to hold context they have not yet been given, cut the cleverness. The reader is a stressed director with reduced cognitive capacity; a metaphor about a route they have not been introduced to is cognitive load, not authored voice.

Two hard consequences of this priority, checked mechanically by `article_audit.py`:

- **Never reference jargon before its first introduction.** Every acronym, form number, statutory section, or invented shorthand (`DS01`, `MVL`, `CVL`, `BADR`, `£13 route`, `s216`, `bona vacantia`, etc.) must be introduced with a plain-English gloss or a link in the same paragraph, or a sentence adjacent to its first appearance. Later mentions are free.
- **Never open a body paragraph with a meta-reference to the article itself.** Openings like "This page covers…", "In this section…", "Both readers get served below", "The routes below are divided by…", "Options are ordered by…" are banned across the whole body, not just P1–P3. Lead with the decision, the constraint, the recommendation, or the reader consequence.

## Reader service

- Write for a real director under real pressure, not a vague audience.
- Translate facts into consequences for the reader's working situation.
- Every major section should help the reader decide, avoid a mistake, understand a trade-off, or defend a course of action.
- If a paragraph does none of those jobs, cut or rewrite it.
- Make each major heading pay off its promise from the first sentence of the section. Do not spend the first paragraph clearing your throat (see `24-payoff-intent-first.md`).

## Voice

- The writer is part of the Company Debt team, not the founder or product builder.
- Do not imply founder or builder authority unless explicitly human-confirmed.
- Use direct judgement rather than padded evaluation.
- If something is good, say what exactly is good, for whom, and with what trade-off.
- Do not use vague support adjectives like `strong` when a clearer claim is available.

## First person

- First person is not the default voice.
- Use it only if removing it changes meaning and the claim is verifiable or human-confirmed.
- Do not use `I think`, `I believe`, `in my view`, or similar scaffolding as filler.
- Do not open with first-person scaffolding.

## Evidence

- Hedging is not evidence.
- Every load-bearing claim must be verified, labelled as judgement, flagged for human confirmation, or removed.
- Do not use decorative sourcing.
- If support is weak, narrow the claim rather than bluffing confidence.

## Decision usefulness

- Every major section should help the reader decide, avoid a mistake, understand a trade-off, or defend a shortlist.
- If a paragraph does none of those jobs, cut or rewrite it.
- Reach the real buyer tension early.
- Respect canonical entity ownership and scope. Do not let a page drift into owning a sibling topic it should only reference.
- Keep the page's primary intent clear: definition, decision, execution, or escalation.
- Match the page structure to its canonical page type. Do not improvise a structure that conflicts with the article-type system.

## Human-authorship texture

These markers are non-compressible in execution:

- include concrete scenes from the reader's working reality
- use earned `you` to translate facts into consequence
- use earned `we` only for method, labour, independence, or editorial judgement
- show operational friction, not just category labels
- include evaluative bite where supported
- vary rhythm and sentence texture
- include at least a few asymmetrical editorial lines that sound unmistakably thought-through
- allow mild UK texture where natural
- allow moral clarity where unfairness, cost, or buyer harm is real
- where call-out boxes are used, they must shift judgement rather than repeat nearby copy
- call-out boxes must respect audience lane, evidence level, and placement rules

Do not let the article become bloodless, over-balanced, or taxonomic.

## Readability

- Keep paragraphs to 2-3 lines in normal article formatting.
- Leave a blank line between paragraphs.
- Prefer full stops, commas, or colons over em dashes.
- Use bold with measured intent: actively identify decision-critical chunks (statutes, deadlines, thresholds, the reader's next action, the hard fact that overturns assumption) and bold them in 1–8 word chunks. Aim for 2–6% body-text bold density, ceiling 8%. Each H2 should contain at least one bolded chunk; sections with zero bolded chunks are usually padding. Full rules: `editorial-os/13-readability-governance.md` §3 / §3a.
- Use italics sparingly.
- Format like a human web editor, not polished AI output.

## Heading discipline

Headings are earned, not defaulted. The test is semantic coherence, not count.

- For each H2, choose the section format *before* writing any H3 (no H3s / bold-label bullets / table / checklist / link cards). Default to the lightest format that carries the content.
- **Keep H3s** when they are clear, logical, semantically related subheadings that each genuinely subdivide the parent H2 — parallel parts of one coherent topic (distinct steps of a process, distinct options, distinct consequences). There the H3s carry real navigational and search value.
- **Demote** to bold labels, bullets, a table, or links when the "H3s" are really just a list, or drift onto a subject separate from the H2's core. Demote too if a bold inline label or table row would carry the point equally well, or if the topic has its own dedicated page (cannibalisation — reference and link instead).
- A count of 3+ H3s under one H2 is only a *trigger* to apply this test, never a verdict on its own.
- Full test and per-page-type H3 budgets live in `editorial-os/28-htag-semantic-framework.md` (Heading Promotion test, H3 Demotion list, section-format decision tree).

**Flag it at the point of writing.** When a cluster of H3s reads as a list or a tangent rather than coherent subheadings of its H2, point it out to the human as you write and offer the lighter format (bold labels, bullets, or a table) instead of waiting to be asked.

## Information gain

Every article should contain genuinely useful material the reader would not get from a generic competitor page. Prioritise:

- sharper trade-off logic (not just "here are your options" but "here is why one option is worse than it looks")
- better scenario framing rooted in real director situations
- stronger evidence handling — named statutes, named practitioners, dated sources
- more decision-useful consequences — not "this can happen" but "this is what it costs you if it does"
- clearer fit and not-a-fit guidance

## Hard bans

- Do not invent first-hand testing, customer experience, or feature certainty without human confirmation.
- Do not use generic hype, filler transitions, or empty evaluative language.
- Do not let the article read like neutral taxonomy when the reader needs a decision.
- Do not default to anonymous summary when the article needs authored judgement.

## If the draft feels weak

- add a concrete scene from the director's working reality
- sharpen the trade-off — make the cost of each option visible
- replace abstraction with lived operational consequence
- add evaluative bite where support exists
- shorten the sharpest claim into a declarative line
- rewrite any paragraph that sounds like AI simulating judgement
- check the first sentence of every paragraph: does it pay off immediately? (see `24-payoff-intent-first.md`)

## Voice Calibration Targets

- "A debt solution that looks tidy on paper can still become unworkable once directors, creditors, and cash flow pressures collide."
- "The practical question is not whether this route exists, but whether it still makes sense when time, leverage, and stress are all running against you."
- "A cheaper-looking option is not necessarily the lower-cost one if it makes the next mistake more likely."
- "Some advice sounds reassuring until you ask who carries the risk if the plan fails. That answer belongs in the copy."
- "When a page is about rescue, the reader needs honest friction, not calm abstraction."
- "If a recommendation only works in the best-case version of events, that limitation is part of the verdict."

## Canonical source map

This pack compresses material primarily from:

- `editorial-os/09-voice-governance.md`
- `editorial-os/10-evidence-governance.md`
- `editorial-os/11-comparison-governance.md`
- `editorial-os/12-structure-governance.md`
- `editorial-os/13-readability-governance.md`
- `editorial-os/17-audience-and-persona.md`
- `editorial-os/23-prose-quality-gates.md`
- `editorial-os/24-content-registry.md`
- `editorial-os/24-payoff-intent-first.md`
- `editorial-os/25-update-logic.md`
- `editorial-os/25-operational-learning-loop.md`
- `editorial-os/26-call-out-box-governance.md`
- `editorial-os/27-article-type-structure.md`
- `editorial-os/28-htag-semantic-framework.md` (load when the article is UK insolvency / liquidation / HMRC / creditor / recovery)
- `editorial-os/docs/human-authorship-voice-engine.md`
