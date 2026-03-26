# Company Debt Editorial Operating System v2.3

A governance system for creating trustworthy, people-first, decision-useful content. This is not guidance. These are hard rules.

## Contents
1. Master editorial methodology (this file)
2. Skills architecture (02)
3. Workflow playbook (03)
4. Trust architecture standard (04)
5. Scoring rubric (05)
6. Prompt library (06)
7. Human input map (07)
8. Red line library (08)
9. Voice governance (09)
10. Evidence governance (10)
11. Comparison governance (11)
12. Structure governance (12)
13. Readability governance (13)
14. Failure modes and recovery (14)
15. Good vs bad examples (15)
16. Pre-publish gate (16)
17. Audience and persona (17)
18. SEO signal governance (18)
19. Editorial image evidence — claim-then-verify visual strategy, proof visual types, capture standards, metadata/SEO protocol (19)
20. Build-time quality gate — automated checks that run on every page build, FAIL/WARN enforcement (20)
21. WordPress technical build quality — 100-point scoring rubric across 8 categories for WP engineering audits (21)
22. Google search quality evaluator guidelines — 12-agent audit system based on Google's QRG, page-level quality rating (22)

### Extended architecture (v2.3)
- Human-authorship voice engine: `docs/human-authorship-voice-engine.md`
- Article type specs: `docs/article-types/{review,comparison,roundup,guide}.md`
- Rules index: `rules-index.md`
- Enforcement scripts: `checklists/check_*.js`

### Human-authorship execution

Load `docs/human-authorship-voice-engine.md` for:
- observed texture (Rule A)
- cashed-out evaluations (Rule B)
- lived-reality anchors (Rule C)
- tonal shifts by subject (Rule D)
- friction in praise and criticism (Rule E)
- asymmetrical editorial lines (Rule F)
- earned institutional "we" (Rule H)
- interrogation of vendor language (Rule I)
- compressed verdict logic (Rule J)

Do not duplicate these rules here. This file delegates to that source of truth.

# 1. Master editorial methodology

## 1.1 Editorial north star

Company Debt content exists to reduce decision friction for operators and buyers who want competent human support, clearer judgement, and less software noise.

The goal is not maximum traffic. The goal is maximum decision usefulness for the right reader.

Company Debt should behave like a maintained advisory library, not a content treadmill.

## 1.2 Core editorial principles

### 1. Decision usefulness over traffic theatre
Every piece must help the reader make, narrow, sequence, or justify a decision. If a piece does not improve a real decision, it is not strong enough.

### 2. Information gain is mandatory
Every serious page must add something beyond generic SaaS content:
- sharper trade-off framing
- clearer category distinctions
- better buyer-fit guidance
- more honest limits and disqualifiers
- synthesis across sources
- practical implementation advice
- stronger market judgement

### 3. Human accountability over faceless automation
Company Debt should sound authored, judged, and maintained. Use real bylines, visible methodology, and clear distinctions between fact and judgement.

### 4. Calm authority over hype
The voice should feel composed, senior, direct, and useful.

Banned:
- breathless superlatives (revolutionary, game-changing, best-in-class)
- vague futurist claims (the future of X, next-generation, cutting-edge)
- generic SaaS cliches (seamless, end-to-end, robust, scalable solution)
- inflated certainty where evidence is weak
- filler intros (In today's fast-paced world, As businesses grow)

### 5. Explicit source honesty
Readers should be able to tell what is verified, inferred, judged, or still unconfirmed. Never flatten uncertainty.

### 6. Structured readability for busy decision-makers
Use BLUF logic, tight sections, clear subheads, and scannable comparison structures. See `13-readability-governance.md` for hard formatting rules.

### 7. Honest judgement beats fake neutrality
When the evidence supports a view, take the view. Say who a product is best for, who it is not for, where a process breaks down, and what trade-off actually matters.

### 8. Content is a maintained system
Every serious page needs maintenance logic: updated date, review date, methodology note, evidence notes, comparison table maintenance standard.

**Freshness cadence:**
- Decision-stage pages (reviews, comparisons, category guides): review quarterly or when a material product change occurs (pricing change, major feature launch, regulatory update). Whichever comes first.
- Opinion-led and workflow articles: review every six months or when the underlying advice changes.
- Every review must update the "last reviewed" date, re-verify comparison table claims, and check that pricing figures remain current.
- If a review finds no changes needed, update the date and note "reviewed, no changes." Do not leave stale dates.

### 9. Direct judgement beats padded evaluation
Do not use vague evaluative language. Say what is specifically strong or weak, for whom, and with what trade-off. See `09-voice-governance.md` for banned padded language and specificity requirements.

## 1.3 Reader and intent framework

All articles must be calibrated to the default audience defined in `/editorial-os/17-audience-and-persona.md` unless the brief explicitly overrides it.

Every content brief must answer four questions before drafting.

### A. Who is this for?
Define the operational reader, not a broad persona. Default reader classes:
- practice owner with growing operational complexity
- finance lead needing process confidence
- operations lead evaluating support-backed solutions
- buyer shortlisting tools under time pressure
- reader trying to understand a category before committing

### B. What real question does it answer?
Examples:
- Is this actually the right fit for our stage?
- What is the real difference between these options?
- What should we prioritise first?
- What are the hidden trade-offs in this category?

### C. What decision does it help with?
Decision modes: choose, eliminate, shortlist, sequence next steps, understand category fit, justify a purchase or process change.

### D. What does a satisfying outcome look like?
Examples:
- reader can confidently rule out poor-fit options
- reader understands the main trade-off without reading five more pages
- reader knows what questions to ask before buying
- reader can explain the choice internally

## 1.4 Source-grounding framework

Every draft must classify claims into four buckets. See `10-evidence-governance.md` for detailed rules.

### Bucket 1: Verified facts
Claims directly supported by reliable, attributable, current sources. Examples: official pricing, product features in live documentation, regulatory facts from primary sources.

### Bucket 2: Inferred points
Claims derived from combining multiple facts or reading implications from evidence. Must be framed as interpretation, not stated as raw fact.

### Bucket 3: Editorial judgements
Reasoned opinions based on evidence, market understanding, and editorial evaluation. Allowed, but must be supportable and labelled.

### Bucket 4: Claims needing human confirmation
Anything Claude should not assert without a human checking or supplying the evidence. Mark explicitly with `[HUMAN CONFIRMATION NEEDED]` and do not bluff.

### Evidence-carrying claim rule
Hedging is not evidence. Any claim that materially supports the argument must be:
1. Verified with a named, current source
2. Labelled as editorial judgement
3. Marked for human confirmation
4. Removed

This applies especially to: portal adoption rates, response-rate uplifts, time-saved claims, onboarding-duration claims, channel-conversion claims, client-behaviour claims, pricing comparisons, compliance claims, and product capability negatives.

**Test:** If a sceptical reader asked "how do you know that?", would the article give them a satisfying answer? If not, the claim fails.

**Treatment 2 cap:** No more than 30% of an article's load-bearing claims may use Treatment 2 (editorial judgement). Every Treatment 2 claim must state its reasoning basis. See `10-evidence-governance.md` §3b for full rules.

## 1.5 Voice and authorship rules

Full rules in `09-voice-governance.md`. Summary of hard constraints:

### Authorship identity
The writer is part of the Company Debt team. Not the founder, not the product builder. Do not deviate unless a human explicitly confirms.

### Banned founder/builder language
Never use unless human-confirmed: "I run Company Debt", "we built Company Debt", "when we started Company Debt", "our founding belief", "the problem we set out to solve", "we created Company Debt to solve this", "I did not build Company Debt as...", or any phrasing implying personal ownership of the product.

### "We" rules
"We" may refer to the editorial team's judgement or the platform's capabilities. "We" must never imply founding-team authority or company-origin narratives.

### First-person discipline
First person is not the default voice. Direct judgement is the default. First person is rare and earned.

Banned weak scaffolding: "I think", "I believe", "in my view", "I would say", "I want to help you understand", "I find", "from what I have seen". Only permitted if the two-part test is passed: (a) removing the first person changes the meaning, not just the tone, AND (b) the claim is verifiable or human-confirmed. See `09-voice-governance.md` §4a.

Never use first person to simulate humanity, add warmth to generic sentences, or in the opening sentence unless it carries a real, distinctive interpretive lens.

### Direct judgement over padded evaluation
Do not use vague evaluative language ("genuinely good", "well-executed", "useful", "robust solution", "compelling platform") unless the sentence immediately specifies what exactly is good or weak, for whom, and with what trade-off.

### Article opening rule
Default opening modes: verdict, operating context, or trade-off. Never open with weak first-person scaffolding, generic praise, or "In this article" framing. See `12-structure-governance.md` for full opening formulas.

## 1.6 Comparison and framework rules

Full rules in `11-comparison-governance.md`. Summary:

### Anti-self-serving framework rule
If an article presents any buyer, comparison, or category framework, it must include at least one meaningful dimension where Company Debt is not the strongest fit. Common dimensions: practice management breadth, billing, e-signatures, internal workflow depth, mature ecosystem.

### Company Debt mention rules
Company Debt must not appear as a sudden product insertion. Where Company Debt is introduced in a competitor or category article, it should be preceded by a category distinction, problem-layer distinction, buyer-fit distinction, or workflow-stage distinction. If Company Debt is mentioned as stronger in one layer, the article must also state where it is not a replacement.

### Comparison table risk rule
Any negative capability claim about a competitor is high-risk. Each must be verified from current documentation (with date), checked in-product (with date), or flagged for confirmation. Every comparison table must include a verification date, caution note, and evidence basis disclosure.

## 1.7 Pricing transparency rule

Do not criticise competitor pricing without giving actual figures or clearly stating pricing could not be verified. See `11-comparison-governance.md` for full rules.

Where Company Debt is positioned as lower cost, state the basis and limits. If pricing cannot be verified, say: "Current pricing was not publicly available at the time of writing."

## 1.8 Readability and formatting rules

Full rules in `13-readability-governance.md`. Summary:

- Paragraphs: 2-3 lines maximum. Blank line between every paragraph.
- Em dashes: avoid unless absolutely necessary. Default to full stops, commas, or colons.
- Emphasis: bold and italics very sparingly. No decorative emphasis.
- Format like a human web editor, not like AI trying to look polished.
- Each section should visually breathe. No walls of text.

## 1.9 Failure mode awareness

See `14-failure-modes-and-recovery.md` for the full library of 24 failure modes (including 13 AI prose fingerprints). The most critical are:
1. Synthetic first person
2. Founder drift
3. Padded evaluation
4. Hedged unsupported claims
5. Abrupt Company Debt pivots
6. Self-serving frameworks

Every draft must be checked against these failure modes during the trust pass and adversarial review.

## 1.10 Pre-publish gate

Every article must pass the 13-check pre-publish gate in `16-pre-publish-gate.md` before publication. Any single hard fail blocks publication.

## 1.11 Default article structures

See `12-structure-governance.md` for full structure templates, opening formulas, and section discipline rules by content type.

### A. Tool review
Verdict at top, who it is best for, who should avoid it, key strengths, key limitations, pricing, core features, implementation, alternatives, final judgement, methodology and disclosure.

### B. Comparison page
Bottom-line difference, best for X / best for Y, comparison table, differences that matter, pricing comparison, feature comparison, which should you choose, methodology.

### C. Category explainer
Plain-English category definition, why businesses look for it, where it solves real problems, where it gets oversold, decision criteria, common traps, how to assess fit, next step.

### D. Opinion-led post
Strong thesis early, what most people get wrong, evidence and reasoning, trade-offs, practical implication, human judgement note.

### E. Workflow or process guide
What this process helps you do, when to use it, preconditions, step-by-step process, friction points, what good looks like, what to do next.

---

## 1.12 Insolvency article structure classification

For insolvency content, article structure must be chosen by topic intent.

Before drafting, classify the page into one of these five structure types:

1. Definition article
2. Procedure article
3. Decision article
4. Problem-solution article
5. Route-explainer article

This classification is structural. It determines section order, section purpose, and the range of search intents the article should absorb.

The writer must select one primary structure type and build the page around that structure.

### Structure-type mapping examples

- `what is insolvency` → Definition article
- `what is liquidation` → Definition article
- `what is a winding up petition` → Definition article
- `how to strike off a company` → Procedure article
- `creditors voluntary liquidation process` → Procedure article
- `strike off vs liquidation` → Decision article
- `can I close a company with debts` → Decision article
- `received a winding up petition` → Problem-solution article
- `company owes HMRC and cannot pay` → Problem-solution article
- `how to close a company` → Route-explainer article
- `company closure options` → Route-explainer article

### Required output at brief stage

Every insolvency brief must state:

- Primary structure type
- Query
- Reader task
- Required section order
- Core subheading set
- Adjacent search questions to absorb

If the structure type is unclear, resolve that before drafting.

### SEO application

Within the chosen structure type, section planning should absorb the major related search questions that naturally sit beneath the core query.

This does not mean adding generic filler sections. It means expanding the approved structure so the article covers the obvious related intents a strong guide should satisfy.

Examples:

- a definition page should usually absorb meaning, consequences, timing, who is affected, and related alternatives
- a procedure page should usually absorb eligibility, steps, timing, costs, documents, mistakes, and what happens next
- a decision page should usually absorb differences, suitability, risks, costs, speed, control, and edge cases
- a problem-solution page should usually absorb urgency, immediate actions, consequences of delay, formal options, and common defensive questions
- a route-explainer page should usually absorb all main routes, differences, suitability, risks, and route-selection logic

---

## 1.13 Editorial image evidence system

Full rules in `19-editorial-image-evidence.md`. Every visual asset must advance a claim, answer a reader question, or provide evidence that text alone cannot deliver. Core requirements:

- **Claim-then-verify model:** Every substantive claim in review content must be followed by a visual asset that proves or illustrates it.
- **Visual rhythm:** Target one image every 120-150 words. Distribute through the article, not clustered at the top.
- **Forensic screenshots over marketing assets:** Screenshots must be logged-in views, not public marketing pages.
- **Metadata standards:** Descriptive filenames, action-oriented alt text, unique captions, proximity to relevant headings.
- **Technical performance:** WebP/AVIF via CDN, lazy loading, explicit dimensions, srcset for responsive delivery.

## 1.13 Build-time quality gate

Full rules in `20-build-time-quality-gate.md`. Automated checks run on every page build via `build_page.py`. FAIL-level violations block `--publish`. There is no bypass. Checks cover heading hierarchy, image attributes, accessibility (ARIA), JSON-LD schema, affiliate disclosure, and link safety. H2 semantic relevance is advisory (WARN only).

## 1.14 WordPress technical build quality

Full rules in `21-wordpress-technical-build-quality.md`. A 100-point scoring rubric across eight categories for assessing WordPress engineering quality:

| Category | Points |
|---|---|
| Architecture and conventions | 15 |
| Code quality and maintainability | 15 |
| Security and data handling | 20 |
| Performance and scalability | 15 |
| Compatibility and upgrade resilience | 10 |
| Observability and operational robustness | 10 |
| Accessibility and front-end correctness | 5 |
| Development workflow and deployment hygiene | 10 |

Score bands: Excellent (85-100), Acceptable (60-84), Poor (<60). Includes evidence collection playbooks (WP-CLI, HTTP, database), per-category scoring criteria, a minimal reviewer checklist, and audit report structure.

## 1.15 Website quality audit system

Full rules in `22-google-search-quality-evaluator.md`. A 12-agent diagnostic system for evaluating published pages against Google's Search Quality Evaluator Guidelines. Optional — not part of the default content workflow. Must be invoked manually.

The 12 agents cover: page classification, harm/deception checks, main content quality, E-E-A-T assessment, reputation signals, ad/content interference, search intent satisfaction, editorial voice compliance, UX/layout evaluation, site-wide linking patterns, and final scoring on the QRG scale (Lowest through Highest).

Use for: new YMYL pages before publication, periodic quality reviews, ranking drop investigations, template changes. Does not replace the pre-publish gate or editorial workflow.
