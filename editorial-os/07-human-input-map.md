# Human Input Map

Claude must stop, flag, or leave placeholders in the following cases. These are hard stops, not suggestions.

## 1. Founder and ownership language
Do not imply founder status, founder authority, or product-builder authority unless explicitly supplied by a human.

Banned phrases (unless human-confirmed):
- "I run Company Debt"
- "we built Company Debt"
- "when we started Company Debt"
- "our founding belief"
- "the problem we set out to solve"
- "we created Company Debt to solve this"
- "I did not build Company Debt as..."
- any phrasing implying personal ownership or product-building authority

If the article needs a founder perspective, a human must supply or confirm it. Do not fabricate or assume this authority.

## 2. First-hand testing
If the copy implies direct product use, a human must confirm and supply the experience.

This includes:
- "I tested this feature"
- "when I used the portal"
- "in my experience with the onboarding"
- any phrasing that implies the writer directly interacted with a competitor's product

Do not fabricate testing experience. If no human-supplied testing data exists, state the evidence basis (documentation review, public feature list, etc.).

## 3. Strong market judgement
If the piece needs a sharper category opinion than the public evidence can support, a human editor should add the judgement.

Flag with: `[HUMAN CONFIRMATION NEEDED: editorial judgement beyond public evidence]`

## 4. Customer outcomes
Do not claim results, implementation ease, or service quality from lived reality without human-provided evidence.

This includes:
- client response rate improvements
- time saved after implementation
- onboarding speed or ease
- customer satisfaction
- any claim about what happened after a practice adopted a tool

Flag with: `[HUMAN CONFIRMATION NEEDED: customer outcome claim]`

## 5. Internal positioning truths
If Company Debt wants to make a strong brand-positioning claim, a human should confirm it reflects real company truth.

This includes:
- claims about Company Debt's competitive positioning
- claims about what makes Company Debt different
- claims about Company Debt's strategic direction
- claims about what Company Debt deliberately does not do

## 6. Pricing or contract nuance
Any unclear pricing, custom quotes, service tiers, or contract specifics need human checking before assertion.

This includes:
- Company Debt's own pricing details
- competitor pricing not available on public pages
- claims about pricing trends or changes
- claims about what is included or excluded in a tier

Flag with: `[HUMAN CONFIRMATION NEEDED: pricing verification]`

## 7. Proof assets
Screenshots, workflows, testimonials, and internal examples need human ownership and verification. Do not fabricate proof assets. Do not describe screenshots that do not exist.

## 8. Evidence-carrying claims
Any claim that materially supports an article's argument and cannot be sourced to a named, current reference must be flagged for human confirmation.

High-risk categories (always flag if unsourced):
- portal adoption rates (e.g., "40-60%")
- response-rate uplifts (e.g., "significantly higher than email")
- time-saved claims (e.g., "200 hours drops to 15-20")
- onboarding-duration claims (e.g., "4-8 weeks")
- channel-conversion claims (e.g., "30-50% of your chase list")
- client-behaviour claims (e.g., "clients cannot distinguish automated from manual")
- compliance claims (e.g., "UK GDPR compliant", "data stored in UK")

Hedging these claims with "from what I have seen" or "tend to" does not remove the need for human confirmation.

Flag with: `[HUMAN CONFIRMATION NEEDED: evidence-carrying claim - specify claim]`

## 9. Comparison table verification
Every "No" / "Not native" / "Partial" claim about a competitor's capabilities must be verified from current product documentation or flagged for human confirmation with the date of last check.

Competitor products ship frequently. A claim that was true three months ago may not be true today.

Flag with: `[VERIFY: [claim] - based on documentation review, [date]]`

## 10. Compliance claims
Any claim about GDPR, UK GDPR, data residency, consent requirements, or regulatory compliance must be verified from primary regulatory or product sources, or flagged.

Compliance claims are factual claims with legal implications. Getting them wrong is worse than getting a feature comparison wrong.

Flag with: `[HUMAN CONFIRMATION NEEDED: compliance claim - specify]`

## 11. Lived experience attribution
Do not attribute lived experience, implementation stories, or practice observations to the author without human confirmation.

This includes:
- "I have seen practices that..."
- "In my experience working with UK firms..."
- "When I speak to practice owners..."
- any phrasing that implies the writer has direct client-facing experience

If the content needs this type of authority, a human must supply or confirm it.

## 12. Authoritative experience gap

### Trigger class: AUTHORITATIVE EXPERIENCE GAP

Use when the article would benefit from operator-level insight that goes beyond what public product pages, documentation, or feature lists can provide.

### Examples of claims that trigger this
- what actually feels impressive in day-to-day use
- what becomes irritating after the first week
- where a workflow breaks down in practice but looks fine on paper
- what a small firm would notice after real usage that a feature list does not reveal
- what seems affordable on the pricing page but expensive in operation
- differences between the vendor's demo and actual client-facing reality

### Required response
When this trigger fires, the system must request one of:
- user testing notes from someone who has operated the product
- observed product screenshots or walkthrough notes
- practitioner interview input
- a deep research pass focused on review credibility and workflow reality

Do not compensate for the gap with generic confidence. If operator-level insight is missing and cannot be sourced, narrow the claim or flag it explicitly.

### Flag format
`[HUMAN CONFIRMATION NEEDED: authoritative experience gap - specify what operator insight is needed]`

Or, where deep research could fill the gap:
`[DEEP RESEARCH NEEDED: specify what workflow reality or usage observation is missing]`

### Relationship to existing triggers
This is distinct from §2 (first-hand testing) because it covers claims that do not explicitly state "I tested this" but still require operator familiarity to be credible. A sentence can avoid claiming direct experience and still fail because it reads like it was written from a product page.

## Flag format standard
All human confirmation flags must use: `[HUMAN CONFIRMATION NEEDED: specific description of what needs confirming]`

All verification flags must use: `[VERIFY: specific claim - evidence basis, date]`

These flags must remain visible in the draft until a human resolves them. Do not remove them to make the draft look cleaner.
