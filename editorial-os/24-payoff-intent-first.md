# 24. Payoff-Intent-First Gate

Every paragraph in editorial insolvency copy must pay off the user's likely intent in the first sentence or first 25 words. Do not spend the opening of a paragraph describing the article, the section, or a hypothetical setup before giving the answer.

Origin: ported from BusinessExpert editorial system patch `payoff-intent-first-v1`, adapted for Company Debt insolvency content.

Source basis: Which?-style human texture (assertion → evidence → human impact), strongest decision-support page patterns (immediate utility, segmented intent, concise problem-focused intros, decision-layer support).

---

## §1 First-Sentence Payoff Rule

**Purpose:** Reduce skim friction and match the strongest decision-support pages by front-loading utility and segmented relevance. Directors under financial pressure scan — they do not read linearly.

### Rules

The first sentence of every paragraph must contain at least one of:

- the decision
- the constraint
- the recommendation
- the user consequence
- the segmentation rule

### First-sentence utility scoring

Score each first sentence 0–5:

| Score | Meaning |
|-------|---------|
| 5 | Directly useful decision or constraint |
| 4 | Clear relevance, slight setup |
| 3 | Useful but delayed |
| 2 | Mostly scene-setting |
| 1 | Meta-copy |
| 0 | Empty filler |

**Hard fail:** any paragraph scoring below 4 in decision-stage pages, intros, consequence sections, options guides, or director-risk articles.

### Utility check

A first sentence passes only if at least one is true:

- names the audience segment or director situation
- names the barrier or deadline
- names the recommendation or route
- names the trade-off
- names the real-world consequence (financial, legal, personal)
- names the access limitation or timing constraint
- names the operational reality

### High-value payload tokens

The opening sentence must contain at least one of:

- the insolvency procedure or legal mechanism
- the eligibility constraint or director duty
- the cost or liability consequence
- the timing deadline
- the director risk or personal exposure
- the "best route for" classification
- the decision rule

---

## §2 Meta-Opening Stripper

**Purpose:** Reject paragraphs whose first sentence primarily describes the article, the section, or the methodology rather than helping the reader decide.

### Banned paragraph openings

Unless the paragraph is methodology-only, ban these openings:

- "This article explains..."
- "This section covers..."
- "Before you decide..."
- "One thing this guide reveals..."
- "We have written this page to..."
- "In this section..."
- "Here is how it breaks down."
- "Here is what we know from the available data."
- "Options are ordered by..."
- "The routes below are divided by..."
- "These options don't fit the main categories because..."

### Reject first sentences that primarily describe

- the existence of the guide
- the origin of the article
- what this section will do
- what readers commonly ask
- the ordering logic of the page
- the structure of what follows

### Rewrite target

Convert article-centric opening → decision-centric opening.

| Bad | Good |
|-----|------|
| "This section covers what happens when a creditor takes legal action." | "Once a creditor files a county court claim, you have 14 days to respond before a default judgement is entered against you." |
| "Here is how the CVL process breaks down." | "A CVL typically takes 6 to 12 weeks from the decision to appoint a liquidator to dissolution." |
| "Options are ordered by suitability for insolvent companies." | "If the company cannot pay its debts, a CVL is almost always preferable to compulsory liquidation — it gives the director more control and a cleaner conduct record." |
| "Before you decide on a route, consider the following." | "The right insolvency route depends on whether the company is solvent, how quickly creditors are likely to act, and whether there are assets worth realising." |

---

## §3 Paragraph Structure: Payoff → Evidence → Consequence

**Purpose:** Mirror the assertion → evidence → human impact structure that the strongest YMYL pages use.

### Rules

Paragraphs in decision-stage insolvency content must follow:

1. **Sentence 1:** payoff (the answer, constraint, or decision rule)
2. **Sentence 2:** proof / explanation (the evidence or legal basis)
3. **Sentence 3:** consequence / action (what it means for this director)

### Rewrite triggers

If a paragraph opens with:
- a hypothetical director scenario as framing rather than illustration
- a scene-setting sentence about the general landscape
- a meta sentence about the page structure

then rewrite so the first sentence states the answer or constraint directly.

---

## §4 Reader Intent Matcher

**Purpose:** Ensure every paragraph serves one of the reader's actual intent clusters.

### Intent clusters for Company Debt insolvency pages

- What is my actual exposure here?
- Which route is right for my situation?
- What is the cheapest or fastest realistic option?
- What happens if I do nothing?
- What are the personal consequences for me as a director?
- What do I need to do, and by when?

### Rules

- Each paragraph must be assignable to one intent cluster.
- If no clear intent cluster is present, rewrite or delete.

---

## §5 Order by Decision Value

**Purpose:** Ensure paragraph ordering reflects what directors need first, not what the writer wants to explain first.

### Paragraph ordering rule

1. personal exposure / consequence
2. timing constraint / deadline
3. route fit / eligibility
4. caveat / limitation
5. secondary context or background

### Do not place ahead of decision value

- writer explanations of structure
- historical context
- general insolvency background
- process description without consequence
- article self-description

---

## §6 Caveat Promotion Rule

**Purpose:** If a caveat changes the director's decision, it cannot be buried late in the block.

### Rules

Promote decision-changing caveats into the first or second paragraph of the relevant section:

- personal liability exceptions (guarantees, overdrawn DLA)
- timing deadlines that expire before alternatives are available
- wrongful trading trigger points
- creditor escalation speed (HMRC vs trade creditors)
- the distinction between civil and criminal consequences

---

## §7 Segment-First Heading Support

**Purpose:** When a heading asks a segmentation question, the first paragraph must answer it immediately.

### Rules

For headings such as "Which Insolvency Route Is Right for My Company?", the first paragraph must answer the heading immediately with a segmentation rule.

**Template:**
> "Most directors do not need to evaluate every insolvency route. They need the right shortlist based on [segment rule: solvency status / creditor pressure / asset position]."

### Do not open with

- background on how insolvency procedures work generally
- abstract explanation of the regulatory landscape
- article housekeeping

---

## §8 Authoring Shortcuts

Preferred paragraph templates for payoff-intent-first writing in insolvency content:

### Constraint-first
> "[Constraint or deadline]. That means [director consequence]. [Action or decision]."

### Segment-first
> "[Director type or situation] should prioritise [criterion]. That narrows the realistic options to [routes]. [Trade-off or next step]."

### Caveat-first
> "[Caveat]. In practice, [operational consequence]. [What to do about it]."

### Consequence-first
> "[Consequence]. That matters if [director state or timing]. [Decision implication]."

---

## Detection and enforcement

### Patterns that trigger a WARN or FAIL

**FAIL patterns** (first sentence of non-methodology paragraphs):
- Starts with "This article" / "This guide" / "This section" / "In this section"
- Starts with "Before you decide" / "Before you choose"
- Contains "this section covers" / "this page explains"
- Starts with "Here is how it breaks down" / "Here is what we know"
- Starts with "Options are ordered by" / "Routes are divided by"

**WARN patterns:**
- First sentence has no high-value payload token (procedure, deadline, liability, route, consequence, decision)
- Paragraph not assignable to a reader intent cluster

### Test definitions

**TEST 1: paragraph_opening_must_payoff_intent**
- FAIL if: first sentence is meta-copy, hypothetical setup, or delays key decision
- PASS if: first sentence gives decision, rule, or constraint

**TEST 2: paragraph_no_article_self_reference**
- FAIL if first sentence contains: "this article", "this guide", "this section", "this page" (unless paragraph type == methodology)

**TEST 3: heading_answered_in_first_sentence**
- For decision-intent headings
- FAIL if paragraph 1 does not answer the heading directly

---

## Drop-in enforcement prompt

> "For all editorial insolvency copy, enforce payoff-intent-first. The first sentence of every paragraph must deliver immediate decision value: the answer, the constraint, the recommendation, the director consequence, or the segmentation rule. Reject meta openings about the article, section, or structure. Reject scene-setting openings that delay the useful point. Rewrite paragraphs to follow this order: payoff, evidence, human consequence. In decision-stage pages, front-load personal liability, timing, route fit, and practical caveats before commentary. Every paragraph must help the director decide or act faster."
