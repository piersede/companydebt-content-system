# Voice Governance

Hard rules governing authorship, first-person use, and editorial voice across all Company Debt content.

## 1. Authorship identity

The writer is part of the Company Debt team. Not the founder. Not the product builder. Not the technical architect.

Default perspective options:
- part of the Company Debt team
- editorial operator
- informed category analyst
- accountable reviewer
- informed editorial team member

Do not deviate from these unless a human explicitly confirms and supplies a different authority.

## 2. Banned founder and builder language

Never use any of the following unless a human has explicitly confirmed and supplied the authority:

- "I run Company Debt"
- "we built Company Debt"
- "when we started Company Debt"
- "our founding belief"
- "the problem we set out to solve"
- "we created Company Debt to solve this"
- "I did not build Company Debt as..."
- "when I started building this"
- "our original vision"
- any phrasing that implies personal ownership of the product or company
- any phrasing that implies first-hand product development experience
- any phrasing that implies founding-team membership

**Failure this prevents:** Founder drift. AI content frequently adopts founder authority because it sounds authoritative. It is not earned authority. It damages credibility when a reader discovers the writer is not the founder.

## 3. "We" usage rules

"We" may refer to:
- the Company Debt team's editorial judgement
- the platform's capabilities ("we handle multi-channel chasing")
- operational perspective ("we recommend starting with email")

"We" must never imply:
- founding-team authority
- product-building experience
- company-origin narratives
- design decisions ("we designed this because...")

**Test:** If a reader asked "who is 'we' here?", would "the Company Debt editorial team" be an honest answer? If not, rewrite.

## 4. First-person discipline

First person is not the default voice. Direct judgement is the default.

### Banned weak scaffolding

Do not use any of the following unless the sentence passes the two-part first-person test (see §4a below):

- "I think"
- "I believe"
- "in my view"
- "I would say"
- "I want to help you understand"
- "I find"
- "I should be clear"
- "from what I have seen"
- "I would not call this a dealbreaker"
- "I would recommend"
- "I want to be upfront"
- "if I am being honest"

### 4a. The two-part first-person test

First person is allowed only if BOTH of these are true:

**(a) Removing the first person changes the meaning, not just the tone.**
If "I think the per-seat pricing is steep" means the same as "The per-seat pricing is steep," the first person fails test (a). If removing "I" loses a genuine distinction — such as signalling that this is a contested judgement the writer is personally taking — it passes.

**(b) The claim introduced is either verifiable or explicitly backed by human-confirmed authority.**
The first-person framing must introduce something the writer can stand behind: a sourced observation, a labelled editorial judgement with stated reasoning, or a claim explicitly confirmed by a human. First person must not introduce unsupported assertions, simulated experience, or unearned authority.

If either test fails, remove the first person and state the judgement directly.

**Examples:**

Fails both tests: "I think Karbon is genuinely good at what it is designed to do."
Removing "I think" changes nothing. The claim is padded, not verifiable.

Fails test (a): "I believe the per-seat model is steep for micro-practices."
Removing "I believe" changes nothing. Direct statement is stronger.

Passes both tests: "I have not seen independent data on portal adoption rates for UK accounting practices — the figures vendors cite are their own."
Removing "I" loses the signal that this is a deliberate editorial observation about a data gap. The claim is verifiable (no independent benchmark exists).

### When first person is permitted (summary)

First person may be used when it passes the two-part test above AND does one of these:
1. Discloses first-hand experience explicitly supplied by a human
2. Signals a contested judgement the writer is personally taking, where the personal framing is editorially necessary
3. Introduces a genuine epistemic distinction (what is known vs what is uncertain)

### When first person is banned

Never use first person:
- to simulate humanity
- to add warmth to a generic sentence
- as a verbal tic or filler
- in the opening sentence of an article (unless it carries a real, distinctive interpretive lens that a human editor would genuinely write)
- to inflate authority beyond what is supported
- to fake product testing or implementation experience
- to attribute lived experience without human confirmation

### Authored judgement without first-person tics

Evaluative writing must feel clearly authored. The absence of first person should not produce anonymous affiliate-review prose.

Rules:
- Declarative judgement is preferred where authorship remains clear from context, specificity, and editorial stance
- Explicit first person is allowed but selective — reserved for verdicts, trade-off interpretation, recommendations, and explicit perspective where a different writer might disagree
- Repeated "I think" sentence openings are a failure pattern even when individual instances pass the two-part test
- "I think" must not appear as the opening phrase of more than one sentence in any article
- No paragraph may contain more than one first-person instance
- Weak sentences improved by removing filler self-signalling should have it removed

### The opening sentence rule

Do not open any article with "I think", "In my view", "I believe", or similar weak first-person scaffolding.

The opening sentence must earn its place with substance, not with a voice marker.

Default opening modes:
1. Verdict: lead with the conclusion or sharpest judgement
2. Operating context: lead with the situation the reader is in
3. Trade-off: lead with the tension the reader is navigating

**Failure this prevents:** Synthetic first person. AI content uses first person to simulate authorship. Real human editors use first person sparingly and only when it passes the two-part test: removing it would change the meaning, and the claim it introduces is verifiable or human-confirmed.

## 5. Direct judgement over padded evaluation

*Cross-references: See Rule B in `docs/human-authorship-voice-engine.md` for implementation guidance. See FM-3 in `14-failure-modes-and-recovery.md` for common failure patterns.*

### Banned padded language

Do not use any of the following unless the sentence immediately specifies what exactly is good, useful, improved, or strong:

- "genuinely good at what it is designed to do"
- "well-executed"
- "useful"
- "genuine improvement"
- "robust solution"
- "strong offering"
- "compelling platform"
- "solid choice"
- "capable tool"
- "impressive feature set"
- "thoughtfully designed"
- "comprehensive solution"

These phrases carry no information. They sound like evaluation but deliver nothing.

### What to do instead

Say what the product is actually strong or weak at. Name the operating context. Name the trade-off. Name who should and should not care.

**Bad:** "Karbon is genuinely good at what it is designed to do."

**Good:** "Karbon's work management templates give five-person-plus practices repeatable job workflows with clear ownership. For two-person practices, the visibility it provides is not yet a real problem."

**Bad:** "The email triage is useful."

**Good:** "The email triage attaches incoming client emails to the relevant job, which saves time spent sorting and forwarding. It does not chase clients who have not replied."

### Disallowed as stand-alone evaluation

The following cannot appear without immediate explanation or consequence:
- genuinely good
- well-designed
- strong fit
- premium option
- clear improvement
- best-in-class
- powerful
- flexible
- useful
- robust
- seamless
- comprehensive
- innovative

### Disallowed authenticity markers

Avoid thin presence-claiming lines such as:
- we reviewed the interface directly
- we spent time in the platform
- we tested this directly

unless followed immediately by a specific observed detail that justifies the claim. (See Rule A in `docs/human-authorship-voice-engine.md`.)

### Disallowed review-template phrasing

Avoid generic, symmetrical constructions such as:
- earns its reputation
- hard sell
- strong option
- clear winner
- not for everyone
- it depends on your needs

unless narrowed into a precise buyer-fit judgment.

### The specificity test

For any evaluative sentence, ask: "What exactly is good or bad, and for whom?" If the sentence does not answer both questions, it fails.

### Misaligned support adjectives

Do not use vague positive adjectives where they do not semantically match the noun they modify. The most common offender is "strong" used as a default evaluator.

**Flag phrases:**
- "strong reputation" / "strong option" / "strong choice"
- "strong platform" / "strong capabilities" / "strong fit" / "strong feature set"

These are not false, but they are semantically lazy. They create tone without meaning and read like generic review-site filler.

**"Reputation" rule:** "Reputation" is already an evaluative term. "Strong" usually adds force rather than clarity. Treat "strong reputation" as a red-flag phrase.

**Preferred fixes:**
- Replace with a more precise adjective where genuinely needed: *established*, *growing*, *mixed*, *poor*
- Or state the underlying claim directly

| Instead of | Write |
|---|---|
| strong reputation | established reputation, or state the claim |
| strong reputation among small firms | well established among small firms |
| has a strong reputation in the UK | is widely used by UK practices |
| TaxDome has a strong reputation | TaxDome is well known for its all-in-one feature breadth |
| Karbon is a strong option for small firms | Karbon is best suited to firms with genuine internal workflow complexity |

**Mechanical check:** If "strong" can be removed without loss of meaning, rewrite. If "strong + abstract noun" appears, flag for review. If the sentence becomes clearer by naming the factual or fit-based claim directly, prefer that version.

**Scope:** Not a ban on the word "strong" everywhere. It is a ban on lazy support-adjective use where the adjective creates approval without precision.

## 5a. Insight signalling

### Rule
Evaluative claims should not default to impersonal blanket statements when a more authored formulation would better signal reasoned observation.

### Weak pattern (flat evaluative declaration)
- "Its statutory deadline tracking is solid."
- "The interface is polished."
- "The CRM is adequate."
- "The workflow visibility is strong."

These read as generic review-site prose. The reader receives a verdict but no sign that anyone thought it through.

### Better pattern (reasoned observation)
- "One thing that stands out is its statutory deadline tracking."
- "What it does better than many small-practice tools is..."
- "Where it earns credit is..."
- "The practical advantage here is..."
- "The issue is not that it lacks X. It is that..."

### Rule
When introducing a strength, weakness, or trade-off, prefer phrasing that signals reasoned observation over flat evaluative declaration.

### Constraint
Do not overuse first person. Stay within existing first-person limits (§4). The goal is authored authority, not repeated "I think" phrasing. Insight signalling works through sentence structure, not through first-person markers.

### Detection
Read each evaluative sentence. Ask: "Could this sentence have been written by someone who only read the product's homepage?" If yes, rewrite with a formulation that shows the judgement was arrived at, not merely stated.

## 5b. Earned authority

### Rule
Authority in Company Debt articles must come from one or more of these sources:
- stated reasoning
- comparison logic
- observed practical consequence
- explicit limitation acknowledgement
- evidence of having thought through the buyer's real workflow

Authority must not come from unsupported tone alone.

### Sentence-level test
Any sentence that makes a judgement should ideally do at least one of the following within the same paragraph:
1. Explain why
2. Compare against an alternative
3. Show the workflow consequence
4. Narrow the claim to a specific buyer or context

### Overlap with existing rules
This rule works alongside Treatment 2 (§3, `10-evidence-governance.md`) and the first-person controls (§4). It does not override them. A sentence can pass Treatment 2 and still fail earned authority if the reasoning basis is not visible in the prose. Earned authority is about how the judgement reads, not how it is classified.

### Detection
For each major evaluative claim, ask: "Would a sceptical reader accept this judgement from someone they have never met?" If the sentence offers no reasoning, no comparison, and no workflow consequence, it fails earned authority.

**Failure this prevents:** Flat authority. Articles that state correct conclusions but sound like they were written by a summariser rather than someone who understands the territory.

## 6. Synthetic prose detection

Common symptoms of AI-generated prose that must be caught and rewritten:

- Vague praise without specifics
- Padded evaluation that sounds like analysis but says nothing
- Over-explaining concepts the reader already understands
- Abstract summary instead of commercial judgement
- Polished but bloodless prose with no editorial edge
- Sentences that sound authoritative but carry no information
- Balanced-sounding language that avoids taking a position
- Filler transitions ("That said", "It is worth noting", "To be fair")

**Detection question:** Would a sharp human editor at a B2B publication write this sentence? Or does it read like competent AI filling space?

## 7. Prose energy

The anti-AI guardrails in §1-6 prevent bad writing. This section defines what good writing sounds like. Structurally correct, evidence-grounded prose can still be lifeless. The goal is editorial content that a reader would want to finish, not just content that passes governance checks.

### 7a. What prose energy is

Prose energy is the quality that makes a reader keep going. It comes from:
- **Controlled personality:** The writer has a point of view that shapes word choice, not just claim selection. The voice is calm and direct, but it is not neutral.
- **Concrete friction:** The article names real operational pain in terms the reader recognises from their own working day, not in abstract category language.
- **Working-day reality:** Sentences ground claims in what actually happens in a practice: the email that sits unanswered, the spreadsheet that has not been updated since January, the phone call that interrupts advisory work.
- **Declarative snap:** The strongest sentences are short, declarative, and take a position. They do not hedge, qualify, or balance. They say the thing.

### 7b. What prose energy is not

Prose energy is not:
- Hype, breathlessness, or urgency language
- Colloquialisms, slang, or forced informality
- Loosening of evidence rules (every claim still needs proper treatment)
- An excuse to weaken readability (paragraphs still 2-3 lines, em dashes still banned)

### 7c. Approved compositional moves

These are patterns that reliably produce prose with editorial energy. Use them as tools, not templates.

1. **Promise vs reality:** "The vendor says X. In practice, Y happens." Ground the gap in a specific operational scenario.
2. **Visibility vs workload:** "This tool shows you who has not sent documents. It does not chase them." Distinguish monitoring from action.
3. **Category mistake → consequence:** "Buying a portal when you need a chasing tool means the clients who are ignoring email will now ignore a portal login too." Name the mistake and its working-day cost.
4. **Feature → working-day consequence:** "The email triage attaches incoming messages to the right job. That means the partner stops forwarding emails manually at 7am." Translate the feature into the change the reader would feel.
5. **Sharp fit language:** "If your bottleneck is X, this solves it. If your bottleneck is Y, it does not." Binary, operational, no hedge.

### 7d. The lived-friction test

For every article, ask: "Does this article name at least one operational frustration in concrete, working-day terms that the reader would recognise from their own practice?"

If the article discusses problems only in category language ("document collection challenges", "workflow inefficiencies"), it fails the lived-friction test. Rewrite with specifics: "the client who has been asked three times and still has not sent their P60."

## 7a. Voice quality checklist

Before finalising any article, check:

- [ ] No founder/builder language unless human-confirmed
- [ ] "We" never implies founding-team authority
- [ ] First person used fewer than 5 times per 1,000 words (hard limit, not a guideline)
- [ ] Every first-person instance passes the two-part test: (a) removing it changes meaning, (b) claim is verifiable or human-confirmed
- [ ] No padded evaluative language without specifics
- [ ] Opening sentence leads with substance, not a voice marker
- [ ] No synthetic filler transitions
- [ ] "I think" does not open more than one sentence in the article
- [ ] No paragraph contains more than one first-person instance
- [ ] Evaluative prose retains authored feel without defaulting to anonymous summary tone
- [ ] The article sounds like it was written by a sharp editorial team member, not by AI simulating one
- [ ] At least one operational frustration named in concrete, working-day terms (lived-friction test, §7d)
- [ ] Prose has declarative snap: strongest claims are short and direct, not hedged or padded
- [ ] Major evaluative claims use insight signalling, not flat evaluative declarations (§5a)
- [ ] Every major judgement has a visible reasoning basis, comparison, or workflow consequence in the same paragraph (earned authority, §5b)
- [ ] Vendor-perspective tone: no inflated neutral-review posture on vendor-authored pages (§8)
- [ ] Conclusion answers the decision question before any CTA (§9)
- [ ] Decision blocks use guided scenario language, not taxonomy labels (§10, Rule K)
- [ ] Alternatives list contains only alternatives; retention guidance is separate (§11, Rule L)
- [ ] Workflow problems anchored in human consequences, not abstract labels (§12, Rule M)
- [ ] Section headings orient the reader immediately (§13)

---

## 8. Vendor-perspective tone discipline

### Core rule

Do not posture as an independent market referee if the publisher is a vendor. Authority must be grounded in scope actually earned:

- workflow expertise
- direct product knowledge
- sector-specific understanding
- declared methodology

### Rules

- Avoid inflated neutral-review posture
- Product mention should feel earned through analysis, not inserted as destination copy
- Authority claims must match the publisher's actual position in the market
- "We assessed" is honest if you actually assessed. "The market is moving toward" is not yours to declare without evidence.

### Detection test

Read the article as a competitor's product manager. Does the tone claim more neutrality than the publisher has earned? If yes, it fails.

---

## 9. Comparison-page conclusion discipline

### Rules

- Conclusion must answer the reader's decision question before any CTA
- CTA must follow the conclusion, not replace it
- Final analytical summary must preserve optionality:
  - who should keep the incumbent
  - who should switch
  - who should add a specialist layer if relevant

### Fail conditions

- **FAIL** if the CTA appears before or instead of the editorial conclusion
- **FAIL** if the conclusion names only one path (the house product)
- **FAIL** if the conclusion and CTA are in the same paragraph

---

## 10. Rule K: Guided scenario language

Decision blocks must be written in guided human language, not compressed taxonomy labels. Lead with the reader's situation, not the system's internal category.

### Disallowed

- "Full platform switch:"
- "Specialist add-on:"
- "Stay put:"

### Required patterns

- "If you want to replace [incumbent] entirely:"
- "If you want to keep [incumbent] but fix [specific problem]:"
- "If [incumbent] is still broadly working for your firm:"

---

## 11. Rule L: Alternatives means alternatives

An alternatives block may only contain actual alternatives to the incumbent.

Retention guidance belongs in a separate adjacent block, not inside the alternatives list:
- "You may not need an alternative if…"
- "When staying on [incumbent] still makes sense"

### Detection test

Would a reader scanning the alternatives list find a "stay put" option confusing? If yes, it does not belong there.

---

## 12. Rule M: Human consequence anchoring

When naming a workflow problem, tie it to lived work and visible friction. Do not leave claims at the level of abstract labels.

### Disallowed

- "workflow inefficiencies"
- "document collection challenges"
- "client communication gaps"
- "operational bottlenecks"

### Required

Ground the problem in a recognisable working-day scenario:
- "the client who has been asked three times and still has not sent their P60"
- "the spreadsheet that says 'chased' next to 40 names but does not say when, how, or what happened"
- "the partner who interrupts advisory work to call a client about a missing bank statement"

---

## 13. Human tone and reader handling

*For detailed authorship engine, see `docs/human-authorship-voice-engine.md`. This section is a quick-reference summary.*

### Rules

- The prose must sound like an informed person helping a reader think, not a taxonomy engine sorting options
- Use "you" when helping the reader decide
- Use "we" only for method, judgement, or declared publisher perspective
- Reduce repeated noun phrases when a pronoun would sound more natural
- Major section labels should orient the reader immediately rather than require translation from internal category language
- Vary sentence length; avoid chains of clipped declarative sentences unless used deliberately for emphasis
- Operational problems should be written in human terms, not abstract SaaS shorthand

### Disallowed patterns

- compressed taxonomic labels as section headings
- repeated noun-heavy phrasing
- flat memo-like cadence
- abstract labels without felt work underneath

### Preferred moves

- reader-led section labels
- humane transitions
- practical consequence language
- rhythm variation
- first-person method where earned

---

## 14. Alternatives page voice discipline

### Core rule

Alternatives pages must not be written as neutral product summaries. The reader has a specific problem. The article must engage with that problem, not describe options at arm's length.

### Required voice moves

- State the real buyer tension early — the switching trigger, not the category description
- Use direct category language that distinguishes the problem type:
  - internal workflow tool
  - outbound chasing layer
  - client-engagement problem
  - replacement vs augmentation
- Make the decision structure visible — reader must understand what kind of choice they are making before any product appears
- Commercial intent must not flatten the analysis — the article must give a sceptical reader a reason to trust it before it makes any recommendation

### Banned opening patterns

Do not open an alternatives page with any of the following:

- "[Vendor] has a large installed base…"
- "[Vendor] is familiar and stable…"
- "[Vendor] handles X, Y, Z…"
- "Searches for [vendor] alternatives tend to come from…"

These patterns delay the buyer problem, open with the incumbent rather than the reader's situation, and signal that the article is structured around the product rather than the decision.

### Preferred opening pattern

1. **Buyer problem** — the specific situation or trigger that brings a reader to this page
2. **Category clarification** — what kind of problem this is and what kind of solution it needs
3. **Decision frame** — replacement, augmentation, or process change

The first product mention must feel earned by the preceding analysis, not inserted as a destination.

### Detection test

Read the opening 200 words without knowing the house product. Ask:

- Is the reader's problem clear?
- Is the category distinction visible?
- Would a reader who chose to stay on the incumbent feel the article understood their situation?

If the answer to any of these is no, the opening fails the voice discipline check.

---

## 15. Authorship Integrity Rule

### Rule

The voice register of the article must match the declared authorship. Mixed authorship states are a voice governance failure.

### Three permitted authorship modes

1. **Practitioner byline** (e.g. "By Chris Andersen, Licensed Insolvency Practitioner")
   - First-person singular practitioner authority is permitted
   - "I speak to directors every week who..." is acceptable
   - The practitioner's lived experience can ground claims

2. **Editorial team byline** (e.g. "By Company Debt Editorial Team")
   - Firm voice or first-person plural only
   - "We" refers to the team's editorial/operational perspective
   - First-person singular practitioner voice is NOT permitted

3. **Reviewed-by model** (e.g. "Written by Editorial Team, Reviewed by Chris Andersen")
   - Default to firm voice (first-person plural)
   - First-person singular permitted ONLY in clearly attributed practitioner asides or quotes
   - The body text must not read as if the practitioner wrote it unless they did

### Fail conditions

- **FAIL** if the article uses first-person singular practitioner voice ("I speak to directors...", "I've sat across the table from...") but the byline is editorial-team-only or reviewed-by
- **FAIL** if the article switches between practitioner voice and editorial voice without clear attribution
- **FAIL** if the disclosure section names the editorial team as author but the body reads as practitioner-written

### Detection

Read the first-person instances in the article. For each one, check: does the byline support this level of personal authority? If the byline says "Reviewed by" but the prose says "I speak to directors every week," there is a mismatch.

---

## §16 Human authority pattern for insolvency pages

Use:
- "you" to frame the reader's practical exposure, deadlines, and next decisions
- firm "we" only where it signals real institutional capability, repeated practice, or process clarity
- named reviewer signals only where they anchor accountability, not as decorative credentials

Avoid:
- generic reassurance without operational detail
- abstract authority claims not tied to what the firm actually does
- repeating "free, confidential, no obligation" as a substitute for substance

Every reassurance sentence on a distressed page must be paired with one concrete operational fact, threshold, or next step within the next 1 to 2 sentences.

### Fail conditions

- **FAIL** if reassurance appears without adjacent operational detail
- **FAIL** if "we" is used more than twice without anchoring to a specific practice or process
- **FAIL** if the page relies on generic brand warmth rather than grounded, specific consequences
