# 23. Prose Quality Gates

Ten enforcement modules for UK financial comparison copy. These gates run during the trust pass (Stage 5) and adversarial review (Stage 6) of any article containing product comparison, financial data, or buyer-decision content.

Origin: patch `business-credit-card-editorial-system/example-fix-001`.

---

## §1 Fact Pattern Gate

**Purpose:** Block mixed-confidence copy inside the same sentence or paragraph.

### Rules

- Do not allow a paragraph to combine hard figures with hand-wavy placeholders.
- If one card has a precise APR, all comparative rate references in that sentence cluster must be equally precise, explicitly ranged, or deliberately generalised.
- If precision is unavailable for one compared item, rewrite the whole comparison around eligibility, fee structure, reward type, or borrower fit instead of quoting uneven numbers.

### Banned phrases

- "whatever rate it offers"
- "sort of"
- "basically"
- "more or less"
- "pretty good"

### Enforcement

Flag any paragraph containing both:
1. numeric product data (APR, fee, limit, percentage)
2. vague filler language

Auto-rewrite to single-confidence mode:
- **precise mode:** all items carry verified figures with sources
- **explanatory mode:** no items carry figures; comparison is structural

---

## §2 Scenario Validity Gate

**Purpose:** Stop invented or over-specific reader scenarios that the evidence base does not fully support.

### Rules

- Do not open with a hypothetical business profile unless every key condition is explicitly grounded in verified provider criteria.
- Prefer eligibility patterns over fictionalised mini-case-studies unless the scenario is sourced from verified provider rules or real case studies.

### Allowed

- "Some cards are only available to existing business current account customers."
- "If you bank with a challenger, the cheapest revolving credit available without switching is Barclaycard at 25.5%." (verifiable eligibility rule + sourced rate)

### Not allowed without proof

- "A consultancy on Tide spending £5,000 a month cannot access Lloyds at 15.95%." (invented business profile, unsourced spend level)

### Rewrite priority

Replace unsupported scenarios with:
1. eligibility rule
2. structural market constraint
3. decision consequence

---

## §3 Meta-Copy Stripper

**Purpose:** Remove self-referential comparison-site filler. The article should help the reader decide, not narrate what the article is doing.

### Ban or rewrite

- "One thing the table reveals"
- "This article shows"
- "Below, we reveal"
- "Most comparisons miss"
- "We checked so you don't have to" (unless immediately followed by specific methodology or named source standard)
- "What this section covers"
- "Here's what you need to know"

### Rewrite pattern

Convert article-centric sentence → user decision sentence.

| Bad | Acceptable | Better |
|-----|-----------|--------|
| "One thing the table reveals that most comparisons miss..." | "A key distinction here is..." | "For businesses that may carry a balance, the important distinction is..." |
| "This article shows why..." | "The reason this matters is..." | "If you carry a balance, this directly affects..." |

---

## §4 Human-Impact Enforcer

**Purpose:** Force every finance paragraph to end in reader consequence, not product description. Matches the assertion → evidence → human impact structure.

### Rules

Each explanatory paragraph must contain:
1. **Market fact or product fact** — the assertion
2. **Constraint or nuance** — the evidence or qualification
3. **Explicit consequence for the reader** — the human impact

### Valid consequence forms

- cost consequence: "On a £5,000 balance, that difference costs roughly £40 a month."
- eligibility consequence: "If you bank with Starling, five of the cheapest cards are unavailable to you."
- operational consequence: "You will need to manage two separate portals for personal and business spending."
- repayment consequence: "Carrying a balance on this card means interest accrues from the transaction date, not the statement date."
- admin consequence: "Switching takes 2–4 weeks and assumes a clean credit history."

### Useful consequence starters

- "That means..."
- "In practice..."
- "For a business owner, that matters because..."
- "If you carry a balance..."
- "If you want employee spend controls..."

### Fail condition

A paragraph that ends on a product description without stating what it means for the reader = rewrite.

---

## §5 Product-Type Clarity Rule

**Purpose:** Handle hybrid or non-standard financial products cleanly.

### Rules

- When a product crosses categories, state the base type first, then the exception, then the user impact.
- Never compress this into jargon.
- Never assume reader knowledge of charge vs credit vs pay-over-time distinctions.

### Template

> "[Product] is [base type] first, but [feature] means it can also behave like [secondary type] in [specific circumstance]."

### Example

- **Good:** "Amex Business Gold is a charge card first, but Pay Over Time at 29.1% variable APR means it can now work more like a hybrid charge-and-credit product for eligible spending."
- **Bad:** "Amex Business Gold is a hybrid charge-credit card with PYOT functionality."

---

## §6 Generic-Intensifier Ban

**Purpose:** Delete empty emphasis. Every intensifier must be replaced with the exact mechanism.

### Banned phrases

| Banned | Replace with |
|--------|-------------|
| "changes everything" | the specific mechanism: "can narrow the shortlist from market-wide options to account-linked products only" |
| "huge difference" | the quantified difference: "nearly 10 percentage points, or roughly £40 a month on a £5,000 balance" |
| "game changer" | the operational consequence |
| "very important" | what specifically it determines or prevents |
| "really useful" | what task it completes or time it saves |
| "worth noting" | the direct consequence: "means you may face a fee even when the first-year headline offer looks free" |
| "key thing to know" | state the thing directly without the preamble |
| "matters more than it sounds" | state the cost, eligibility, or operational consequence directly |

---

## §7 Opening Paragraph Router for YMYL Comparisons

**Purpose:** Make intro-paragraph logic match top-performing finance pages: concise, problem-led, utility-first, and segmented by real decision needs.

### Rules

For comparison intros, use this order:
1. Real market constraint
2. Why generic rankings can mislead
3. What this table or section helps the reader decide

### Template

> "[Constraint]. That matters because [decision risk]. This table/section helps you compare [relevant dimensions] so you can identify [practical outcome]."

### Example

> "Not every business can choose from the full market. Some of the lowest-rate cards are only available to existing business current account customers, so your realistic shortlist may be much narrower than a generic 'best business credit cards' table suggests. That matters because the gap between a lower-rate bank card and a more widely available rewards card can be the difference between manageable borrowing and expensive borrowing if you carry a balance."

---

## §8 Financial Objectivity Check

**Purpose:** Protect trust and avoid affiliate-shaped distortion.

### Rules

- If a provider is commercially important, the copy must still state:
  - at least one drawback
  - at least one eligibility limit
  - at least one trade-off
- Every promoted card must have at least one limiting condition or non-ideal use case.
- This applies regardless of commercial relationship.

### Fail condition

Any card presented without a drawback, limit, or trade-off = rewrite.

---

## §9 Sentence Texture Calibrator

**Purpose:** Reduce AI cadence. Prevent monotonous declarative prose.

### Rules

- Avoid back-to-back high-density declarative sentences with identical length.
- In each 2-paragraph block, require:
  - one short sentence (under 12 words)
  - one medium analytical sentence (15–25 words)
  - one sentence with direct reader framing ("you", "your", "if you")

### Prefer concrete nouns over abstract nouns

| Use | Avoid |
|-----|-------|
| shortlist, APR, account requirement, annual fee, balance | landscape, consideration, factor, dynamic |
| eligibility page, application form, statement date | ecosystem, paradigm, framework (in prose) |

---

## §10 Source Constraint: Original Sources Only

**Purpose:** Ensure all sourced claims reference original providers, regulators, and primary data sources — never competitor comparison sites.

### Hard rule

Sources must be one of:
- **Provider direct:** the bank, card issuer, or fintech's own website, terms, or disclosure documents
- **Regulator:** FCA, Bank of England, PRA, ICO
- **Industry body:** UK Finance, British Business Bank, Finance & Leasing Association
- **Government / statistics:** ONS, HMRC, Companies House, GOV.UK
- **Credit reference agency:** Experian, Equifax, TransUnion (for methodology or public data)
- **Recognised independent body:** Moneyfacts, Defaqto, Which? (for market-wide data or methodology, not editorial opinion)

### Never source from

- Competitor comparison sites (MoneySupermarket, NerdWallet, Finder, TotallyMoney, Forbes Advisor, etc.)
- Affiliate content aggregators
- Press releases that only restate a competitor's editorial claim
- Social media posts or forums (unless the post is from a verified provider account)

### Enforcement

- Every sourced claim in a page config must include a `source` field
- The source must pass the whitelist above
- If the only available source is a competitor site, the claim must be independently verified against the provider's own documentation, or flagged with `[VERIFY — only competitor source found]`
- During the trust pass, any competitor-sourced claim without independent verification = fail

---

## Drop-in enforcement prompt

For use in the editorial enforcement layer during trust pass and adversarial review:

> "For UK financial comparison copy, reject any paragraph that relies on unsupported hypothetical business scenarios, mixes precise figures with vague filler, or explains what the article is doing instead of what the reader needs to decide. Rewrite around verified market constraints, eligibility logic, and direct borrower impact. Each paragraph must follow this structure: assertion, evidence/nuance, human consequence. Replace generic emphasis with mechanism. Where a product crosses categories, state the base type, the exception, and the real-world implication in plain English. Maintain authoritative, specific, British, non-hype prose. Source all claims from original providers, regulators, industry bodies, or recognised independent data sources — never from competitor comparison sites."

---

## Output contract for example-based patches

For each bad example submitted:
1. Diagnose the exact failure modes
2. Output the corrected copy
3. Output the architecture patch needed to stop recurrence
4. Output only patch-ready instructions, not commentary

---

## §11 Distress reassurance statistics constraint

Do not use sector-level statistics primarily to calm the reader unless:
- the statistic is directly relevant to the decision at hand
- the limit of the inference is stated
- the risk category is defined narrowly

**Allowed:** "Liquidation does not automatically mean disqualification. The Insolvency Service investigates conduct, not the fact of liquidation itself."

**Restricted:** Broad ratio-based reassurance implying personal safety from aggregate market data.

### Enforcement

If a reassurance claim relies on a population-level statistic, the next 1-2 sentences must state the boundary of the inference. If the boundary is missing, fail this gate.

---

## §12 Body decision density gate (distressed pages)

After the first screen, no body section on a distressed-director page may exceed 180-220 words before one of the following appears:
- a comparison block
- a checklist
- a threshold box
- a timeline
- a consequence summary
- a next-step instruction
- a warning box

If two consecutive sections exceed this limit without decision-support formatting, fail readability and structure.

### Cross-reference

This gate enforces the structural requirement from `12-structure-governance.md` §18. It runs as part of the prose quality gate sequence, after §10 (original-source-only) and before the output contract.

---

## §13 Human authority gate — YMYL distress pages

Each major section must contain, within its first 120 words:

1. A direct claim or judgment
2. A concrete mechanism, consequence, or factual trigger
3. The practical effect on the reader

At least once in the first 30% of the page, include:
- institutional accountability ("we help directors...", "we usually see...")
- direct reader framing ("if you've received...", "if HMRC has...")
- explicit editorial judgment ("this is usually the better route when...")

### Pattern: assertion → mechanism → human impact

**Pass:** "If you act now, you choose the IP and control the timing. If a creditor petitions first, the court appoints the Official Receiver — you lose the ability to choose, and the investigation is more intensive."

**Fail:** "Liquidation is a legal process that can be initiated voluntarily or by court order. The process involves the appointment of a liquidator who manages the company's affairs."

### Fail conditions

- **FAIL** if the page sounds correct but disembodied (no accountable voice)
- **FAIL** if expertise is implied but no institutional or practitioner presence is visible
- **FAIL** if sections explain without judging or recommending
