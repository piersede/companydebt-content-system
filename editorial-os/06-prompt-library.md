# Prompt Library

## Reader-intent brief prompt

Define this content piece using four headings:
1. Who it is for (operational reader, not vague persona)
2. What real question it answers (specific, not generic)
3. What decision it helps with
4. What a satisfying outcome looks like

Reject vague persona language. Be operational and specific.

## Source-grounding prompt

Review the source material and extract all meaningful claims into four labelled buckets:
- verified facts (named source, date, attributable)
- inferred points (clearly labelled as interpretation)
- editorial judgements (supportable, not stated as fact)
- claims needing human confirmation (flagged with `[HUMAN CONFIRMATION NEEDED]`)

Apply the evidence-carrying claim rule: any claim that materially supports the argument must be verified, labelled as judgement, flagged, or removed. Hedging alone does not pass.

Flag all high-risk claim categories: portal adoption rates, response-rate uplifts, time-saved claims, pricing comparisons, compliance claims, product capability negatives, client-behaviour claims.

Downgrade certainty where support is weak. Do not flatten uncertainty.

## Outline prompt

Using the brief and source-grounding map, build an outline that:
- front-loads the main conclusion
- makes trade-offs visible
- helps a busy reader make a decision quickly
- follows the correct opening formula for the article type (see `12-structure-governance.md`)
- includes at least one dimension where Company Debt is not the strongest choice (if a framework is used)

## Draft prompt

Write the first draft. Follow these rules strictly:

**Voice rules (see `09-voice-governance.md`):**
- Calm, direct, expert voice. No hype, no filler.
- Do not use "I think", "I believe", "in my view", "I would say", "I find", "from what I have seen" unless the sentence genuinely needs it for nuance that cannot be carried any other way.
- Do not imply founder/builder authority unless explicitly confirmed by a human.
- Default perspective: part of the Company Debt team, editorial operator, category analyst, informed reviewer.
- Do not use padded evaluative language ("genuinely good", "well-executed", "useful", "robust solution") unless the sentence immediately specifies what exactly is good, for whom, and with what trade-off.

**Opening rules (see `12-structure-governance.md`):**
- Default to verdict, operating context, or trade-off.
- Do not open with "I think", "In my view", "I believe", or similar.
- Do not open with generic praise, "In this article", or dictionary-style definitions.

**Evidence rules (see `10-evidence-governance.md`):**
- Every evidence-carrying claim must be verified, labelled as judgement, flagged, or removed.
- Hedging alone does not satisfy this requirement.
- Do not use decorative sourcing.

**Framework rules (see `11-comparison-governance.md`):**
- Any buyer/comparison/category framework must include at least one dimension where Company Debt is not the strongest choice.

**Pricing rules:**
- Do not criticise competitor pricing without actual figures or a "could not verify" note.
- If Company Debt is positioned as more economical, state basis and limits.

**Company Debt mention rules (see `11-comparison-governance.md`):**
- Introduce Company Debt through category/problem/buyer-fit distinction, not abruptly.
- Include balancing statement where Company Debt is mentioned as stronger.

**Readability rules (see `13-readability-governance.md`):**
- Paragraphs: 2-3 lines maximum. Blank line between every paragraph.
- Avoid em dashes. Default to full stops, commas, or colons.
- Bold for lead terms in structured lists and decision-critical phrases only. No scattered bold in body prose. Each term bolded once on first introduction.
- Italic for editorial asides, caveats, source titles, and genuine emphasis. No decorative italic. No italicised sentences or clauses.
- Format like a human web editor. Sections should visually breathe.

**External link rules (see `13-readability-governance.md` §7):**
- Link to credible external sources when citing verifiable claims (salary data, policy changes, product documentation, industry reports).
- Use `target="_blank"` on all external links. CSS adds a subtle arrow indicator automatically.
- Anchor text must describe what the reader will find, not generic "click here" or "source".
- Maximum 3-5 external links per 1,000 words of body content.
- In the Sources section, link directly to the cited source. Domain name or publication title is acceptable anchor text.

**Authored authority rules (see `09-voice-governance.md` §5a, §5b):**
- For each major verdict, show how the judgement was formed. Do not state evaluative conclusions as flat facts.
- Introduce strengths and weaknesses as observations, not flat labels. Use insight signalling: "One thing that stands out is...", "Where it earns credit is...", "The practical advantage here is..."
- Where possible, make authority feel earned through comparison, reasoning, or workflow consequence. Every major evaluative claim should have a visible reasoning basis in the same paragraph.
- If the draft lacks enough grounded insight to sound genuinely expert, do not compensate with generic confidence. Narrow the claim or flag for human input / deep research.
- At least once in each major section, answer the silent reader question: "Why should I trust this judgement?"

**Prose-energy rules (see `09-voice-governance.md` §7):**
- Name at least one operational frustration in concrete, working-day terms in the first third.
- Use at least two approved compositional moves (promise vs reality, visibility vs workload, category mistake → consequence, feature → working-day consequence, sharp fit language).
- Ensure the sharpest claim is a short, declarative sentence that stands on its own.
- Every body paragraph must serve one of five purposes: identify pain, translate feature, expose gap, sharpen fit, advance decision.

## Trust pass prompt

Review the draft against every governance rule. Check for:

**Evidence integrity:**
- [ ] Unsupported claims: apply evidence-carrying claim rule
- [ ] Hidden uncertainty: is any uncertain claim presented as settled?
- [ ] Decorative sourcing: does every cited source actually support the specific claim?
- [ ] Disclosure needs: is the methodology note present? Is the Company Debt disclosure present?
- [ ] Methodology gaps: is the evidence basis stated?
- [ ] Overstatement: is any claim stronger than its evidence supports?

**Voice and authorship:**
- [ ] Founder/builder language: search for "I run", "we built", "we started", "our founding", "set out to"
- [ ] Artificial first person: search for "I think", "in my view", "I believe" used as filler
- [ ] Padded evaluation: search for "genuinely good", "well-executed", "useful", "robust" without specifics
- [ ] Synthetic prose: does any section read like AI simulating judgement?

**Comparison and framework:**
- [ ] Self-serving frameworks: does any framework lead to a predetermined conclusion?
- [ ] Missing balance: is there a dimension where Company Debt loses?
- [ ] Comparison table risk: is every "No" about a competitor verified with date?
- [ ] Abrupt Company Debt pivot: does Company Debt appear through earned distinction or insertion?

**Pricing:**
- [ ] Pricing criticism without figures: is competitor pricing criticised without actual numbers?
- [ ] Company Debt cost positioning: is the basis stated?

**Readability:**
- [ ] Em dash overuse: replace with full stops, commas, or colons
- [ ] Paragraph length: any over 3 lines? Split them.
- [ ] Formatting clutter: unnecessary bold or italic?
- [ ] Bold discipline: bold used only for lead terms in lists and decision-critical phrases? Each term bolded once?
- [ ] Italic discipline: italic used for asides/caveats/source titles only? No italicised sentences?
- [ ] Section breathing: do sections have visual space?

**External links:**
- [ ] Verifiable claims linked to credible sources where available?
- [ ] External links use `target="_blank"` and descriptive anchor text?
- [ ] External link density within 3-5 per 1,000 words?
- [ ] Sources section links directly to cited sources?

Recommend exact fixes for every failure.

## Adversarial review prompt

Attack this draft as:
- a sceptical expert who knows the category well
- a time-poor buyer who needs to decide this week
- a trust-sensitive reader who distrusts vendor content

Identify:
- What feels generic, unsupported, unclear, or not decision-useful enough
- Sentences where "I think" / "in my view" adds nothing and should be removed
- Sentences implying founder/builder authority without human confirmation
- Padded evaluative phrases that carry no information ("genuinely good", "well-executed")
- Evaluation frameworks designed to produce a predetermined outcome
- Evidence-carrying claims resting on hedging rather than sources
- Comparison claims a competitor might dispute
- Pricing criticisms without figures
- Abrupt Company Debt mentions that feel inserted rather than earned
- Prose that sounds like competent AI rather than sharp human editorial
- Em dashes that should be replaced with cleaner punctuation
- Paragraphs longer than 3 lines that need splitting
- Scattered bold or italic that does not aid comprehension

Run against all 24 failure modes in `14-failure-modes-and-recovery.md`.

State whether the page passes or fails. List exact fixes required.

## Final polish prompt

Tighten the draft for:
- stronger BLUF (is the verdict front-loaded?)
- better scanability (can a reader extract the answer in 60 seconds?)
- better trade-off visibility (are trade-offs explicit, not buried?)
- stronger fit / non-fit guidance (does the reader know if this is for them?)
- more obvious authorship (does this sound like a real person wrote it?)
- cleaner endings (decision summary, next step, or trade-off restatement?)
- shorter paragraphs (2-3 lines max, no walls of text)
- fewer em dashes (replace with full stops, commas, or colons)
- restrained emphasis (remove unnecessary bold or italics)
- visual breathing room in every section
- no synthetic prose patterns
- lived friction in the first third (see `09-voice-governance.md` §7d)
- at least two approved compositional moves used (see `09-voice-governance.md` §7c)
- sharpest claim stands as a short, declarative sentence

## Prose-energy prompt

After the draft passes mechanical and structural checks, test it for editorial energy:

**Lived-friction test (see `09-voice-governance.md` §7d):**
Does the article name at least one operational frustration in concrete, working-day terms the reader would recognise? If not, add one in the first third.

**Paragraph-purpose test (see `12-structure-governance.md` §3b):**
For each body paragraph, identify its purpose: identify pain, translate feature, expose gap, sharpen fit, or advance decision. Any paragraph that serves none of these is filler. Cut or rewrite.

**Approved-moves check (see `09-voice-governance.md` §7c):**
Does the article use at least two of the five approved compositional moves? If the prose is structurally sound but flat, inject:
- One promise-vs-reality move (vendor says X, in practice Y)
- One feature-to-consequence move (the feature does X, which means the reader stops doing Y)
- One sharp fit sentence (if your bottleneck is X, this solves it; if Y, it does not)

**Declarative snap check:**
Find the article's sharpest claim. Is it a short, declarative sentence? If it is buried in a longer paragraph or softened by qualifiers, extract it and let it stand alone.

---

## Insolvency article briefing prompt

When briefing an insolvency article:

1. Classify the page as one of:
   - Definition
   - Procedure
   - Decision
   - Problem-solution
   - Route-explainer

2. Generate the outline using the matching section order from `12-structure-governance.md` §29.

3. Expand that outline into a keyword-aware subheading plan that captures the major adjacent search questions relevant to the query.

Brief output must include:

- Target query
- Selected structure type
- One-line reader task
- Full section order
- Proposed H2/H3 plan
- Related search questions being absorbed

The outline should be structurally consistent and search-complete.
