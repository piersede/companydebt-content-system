# Guide Article Type — Authorship and Structure Rules

Extends the base rules in `docs/human-authorship-voice-engine.md` with guide-specific requirements.

## Guide-specific authorship rules

- Explain the real-world friction of implementation, not just the abstract path
- Facts must repeatedly be translated into wallet, workflow, time, risk, or effort consequences (Rule C)
- Use "you" to keep service orientation visible
- Avoid high-level summary language without practical consequence
- Where guidance is strong, acknowledge the condition or trade-off that limits it (Rule E)
- If the topic involves unfairness, exploitation, opacity, or user harm, a morally evaluative stance is allowed and often required

## Guide structure requirements

- Opening must place the reader in a recognisable situation or name the problem they are trying to solve
- Each major section must make a claim, show why it is true, and explain why it matters
- Implementation steps must include friction: what takes time, what is awkward, what depends on human effort
- Ending must compress the decision or next step, not drift into summary

## Guide pronoun defaults

Primary: you
Secondary: we
Tone: useful, empathetic, practical
Human signal: consequences translated into daily reality, friction acknowledged, conditions stated

## Guide-specific fail conditions

- **FAIL** if implementation friction is absent (everything sounds easy and smooth)
- **FAIL** if facts remain abstract without wallet/workflow/time/risk translation
- **FAIL** if guidance lacks conditions or trade-offs
- **FAIL** if morally evaluative stance is suppressed where the reader faces exploitation or opacity

---

## Company Debt Decision Guide standard

For Company Debt, guides are decision guides, not general explainers.

Each guide must:
- serve one dominant persona-state
- help the reader make one core decision
- resolve top blockers before broad explanation
- maintain high decision density through the body
- offload secondary topics to supporting pages

A guide fails if:
- it behaves like a merged hub
- it explains too many adjacent subtopics in full
- it uses FAQ as a warehouse for unresolved core objections
- it contains more than 3 major informational branches after the opening

### Decision Guide body rules

A Company Debt guide is not a general explainer. It must help one persona-state make one core decision under legal, financial, or emotional pressure.

A Decision Guide must:
- identify the decision in the opening
- rank information by urgency and consequence
- resolve the top 3 blockers before adding background
- use short decision modules rather than long expository sections
- end with a next-step action, not a generic summary

A Decision Guide **FAIL**s if:
- it behaves like a merged content hub
- it contains more than 3 major informational branches after the opening
- it includes a long FAQ section covering secondary queries better suited to supporting pages
- it explains processes before resolving route selection

### Section function limit

Each section may perform only one primary function:
- explain
- compare
- warn
- quantify
- direct action

If a section contains more than one function, it must be split. A CVL section that covers process, employees, cost, and timeline is four functions — it needs splitting or demotion.

### Final action lock requirement

Every decision guide must end with a concrete action section:

```
## What to do now
- If HMRC has contacted you → [specific action] today
- If creditor pressure is escalating → [specific action] within 48h
- If you are unsure → [specific action]
```

This replaces soft emotional or generic closing sections. The reader must leave with a time-bound next step, not a summary.

---

## Insolvency guide archetypes

Do not draft a generic liquidation guide by default. Choose exactly one archetype before outlining:

**1. Crisis-defense page**
Reader state: statutory demand, HMRC warning, petition risk.
Goal: preserve control and force immediate action.

**2. Controlled-exit page**
Reader state: accepts closure, wants to choose CVL.
Goal: explain process, cost, timing, and conduct risk.

**3. Cost-comparison page**
Reader state: CVL vs strike-off vs compulsory liquidation.
Goal: resolve affordability and route confusion.

**4. Rescue-options page**
Reader state: business may still be viable.
Goal: compare CVA / administration / negotiation / liquidation.

### Fail conditions

- **FAIL** if more than one archetype is treated as primary
- **FAIL** if a page attempts to be a crisis-defense AND a controlled-exit AND a cost-comparison simultaneously

### Terminology bridge

A Company Debt guide must translate the reader's problem language into the correct legal route.

Do not assume route-name literacy. Do not make the reader decode acronyms in the first paragraph. Name the route after the page has already explained, in ordinary language, what the route actually is.
