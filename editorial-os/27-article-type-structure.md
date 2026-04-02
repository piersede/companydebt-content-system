# 27. Article Type Structure

Canonical structure system for CompanyDEBT.com page types.

This file defines how Company Debt content types should behave under distress, legal sensitivity, anti-cannibalisation rules, and decision-stage search intent. It sits on top of the content registry and below execution-time templates.

---

## 27.1 Core rule

Every page type must have:

- a clear job
- explicit scope boundaries
- a decision-layer ending
- a structure that matches the user's distress stage and informational need

Article structure is not cosmetic. It is part of trust, retrieval accuracy, anti-cannibalisation, and conversion integrity.

---

## 27.2 Taxonomy and ownership alignment

The site map is the taxonomy of record.

Use article structures to express:

- entity ownership
- decision stage
- audience lane
- enforcement stage
- risk profile

Do not use article structures to create accidental duplicate owners for sibling concepts.

---

## 27.3 Page-type classes

The main Company Debt page-type classes are:

- provider reviews
- service reviews
- comparisons
- best-of roundups
- category and hub pages
- use-case and distress pages
- definition and glossary pages
- pricing and cost pages
- process guides
- recovery strategy guides
- debt-solution comparison pages
- legal and compliance explainers
- case insight pages
- template and letter pages

Each class must preserve intent locking and route to the canonical owner where appropriate.

---

## 27.4 Structural rules by page type

### Provider reviews

Job:
Assess a specific provider or firm with methodological clarity and commercial honesty.

Must not do:
- act like a generic review affiliate page
- bury methodology or disclosure
- skip fit, misfit, or eligibility boundaries

Required structure:
1. Bottom-line judgement
2. Best fit and not-a-fit
3. Methodology and disclosure
4. Verification note
5. What this provider actually does
6. Practical strengths
7. Constraints, risks, or trade-offs
8. Cost and commercial model
9. Decision layer ending

### Service reviews

Job:
Explain and evaluate a specific insolvency or debt solution as used in practice.

Must not do:
- duplicate the owner definition if the review is a narrower modifier
- treat the process as a sales brochure

Required structure:
1. Quick answer
2. What this service is
3. Who it is for
4. Who should not use it
5. How it works in practice
6. Risks and trade-offs
7. Cost and timing realities
8. Decision layer ending

### Comparisons

Job:
Help the reader choose between routes, providers, or strategies.

Must not do:
- delay the decision tension
- stack duplicate definitions
- force a predetermined winner

Required structure:
1. Bottom-line difference
2. Best for X / best for Y
3. Decision-trust module
4. Disclosure and verification
5. Quick comparison table
6. Differences that actually matter
7. Cost and contract comparison
8. Workflow and consequence comparison
9. House-product containment block if relevant
10. Decision layer ending

### Best-of roundups

Job:
Speed up shortlisting without flattening fit and risk.

Must not do:
- become a ghost listicle
- present all options as equally plausible

Required structure:
1. Methodology and inclusion rules
2. Best by scenario
3. Regulated versus non-regulated support where relevant
4. Exclusions
5. Decision layer ending

### Category and hub pages

Job:
Route readers into the right owner pages and help them choose the right kind of content path.

Must not do:
- become a second owner page for every entity in the cluster
- turn into encyclopedia copy

Required structure:
1. Start here
2. Situation chooser
3. Core options
4. Highest-risk mistakes
5. Tools and templates
6. Decision layer ending focused on what to do today

### Use-case and distress pages

Job:
Diagnose a live problem and stabilize the next 72 hours.

Must not do:
- force one solution too early
- drift into full process detail
- provide personalized legal advice

Required structure:
1. What this usually means
2. What to do in the next 72 hours
3. Options ranked from least irreversible
4. Director duties and personal risk
5. Decision layer ending with route selection

### Definition and glossary pages

Job:
Own a term cleanly and make it linkable and citable.

Must not do:
- become a generic how-to
- displace owner pages for procedures

Required structure:
1. Definition
2. Statutory anchor where relevant
3. Examples
4. Why it matters
5. Where it appears in procedures
6. Decision layer ending

### Pricing and cost pages

Job:
Answer cost intent directly and honestly.

Must not do:
- hide the answer behind a contact gate
- use bait pricing

Required structure:
1. Typical cost ranges
2. What the fee includes
3. What changes the cost
4. Who pays and when
5. What if you cannot afford it
6. Cost versus outcome trade-offs
7. Decision layer ending

### Process guides

Job:
Provide an execution-stage playbook that can actually be followed.

Must not do:
- compete with broad entity intent when an owner exists
- skip red flags or stakeholder impacts

Required structure:
1. Before you start
2. Step-by-step timeline
3. What can go wrong
4. Stakeholder impacts
5. Decision layer ending with execution checklist

### Recovery strategy guides

Job:
Map the route from informal stabilization to formal rescue or closure.

Must not do:
- drift into vague turnaround tips
- detach from UK creditor and insolvency reality

Required structure:
1. What restructuring means in practice
2. Early warning signals
3. Option map from informal to formal
4. Choosing based on constraints
5. Decision layer ending with next 10 actions

### Debt-solution comparison pages

Job:
Present a controlled matrix of routes and help the reader commit to a path.

Must not do:
- duplicate owner content
- present the matrix without scenario gating

Required structure:
1. Quick chooser
2. Informal options
3. Formal rescue options
4. Closure options
5. Decision layer ending with evidence-pack checklist

### Legal and compliance explainers

Job:
Explain director-risk and compliance issues precisely, with legal anchors and practical responses.

Must not do:
- speculate
- sensationalize
- imply guaranteed outcomes

Required structure:
1. What the law says
2. When it becomes a real risk
3. What good practice looks like
4. How it interacts with insolvency routes
5. Decision layer ending with stop-doing and start-doing guidance

### Case insight pages

Job:
Provide proof-of-work and realistic pattern recognition.

Must not do:
- imply typicality without basis
- invent numbers

Required structure:
1. Situation summary
2. Constraints
3. Chosen route and why
4. Timeline and actions
5. Outcome and lessons
6. Decision layer ending with similarity check

### Template and letter pages

Job:
Give practical scripts and boundaries for stabilizing pressure.

Must not do:
- encourage misleading statements
- imply that a template replaces advice

Required structure:
1. When this template is appropriate
2. When it is dangerous or inappropriate
3. The template
4. Director notes and risk boundaries
5. What to do after sending
6. Decision layer ending

---

## 27.5 Universal decision-layer rule

Every page type must end by helping the reader decide one of:

- what to do today
- what route is most plausible
- what risk requires immediate action
- what kind of help they actually need

No page should end as a neutral information dump.

---

## 27.6 Dragon's Den pressure test

All page types must survive scrutiny from these lenses:

- editorial quality
- SEO and information architecture
- distressed buyer psychology
- B2B conversion integrity
- legal and regulatory sensitivity
- advisory positioning

If the structure delays deadlines, personal risk, or the next plausible action, it fails.

---

## 27.7 Execution rule

This file defines canonical structure. Execution-time templates in `editorial-os/templates/` should implement these page types in concrete outline form.

Runtime packs should use this file when:

- briefing a new page
- choosing a page-type overlay
- reviewing scope drift
- checking whether a page structure matches its claimed intent
