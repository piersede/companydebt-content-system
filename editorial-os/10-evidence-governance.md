# Evidence Governance

Hard rules for evidence honesty, claim support, and source integrity across all Company Debt content.

## 1. Core principle

Hedging is not evidence. A hedge makes a sentence feel safer. It does not make it true.

## 2. What is an evidence-carrying claim?

An evidence-carrying claim is any claim that materially supports:
- the main recommendation
- the core differentiation
- the buyer decision
- the cost case
- the compliance case
- the comparison outcome

These are the claims that carry the argument. If they fall, the article's conclusion falls with them.

## 3. The four treatments

Every evidence-carrying claim must receive one of these four treatments. No exceptions.

### Treatment 1: Verified
The claim is backed by a named, current, attributable source.

Example: "TaxDome's pricing starts at $25/month per user (TaxDome pricing page, March 2026)."

### Treatment 2: Labelled as editorial judgement
The claim is explicitly framed as a reasoned view, not a factual assertion.

Example: "Based on the feature set and pricing structure, smaller practices are likely to find the per-seat model disproportionately expensive relative to the coordination visibility it provides."

### Treatment 3: Marked for human confirmation
The claim is flagged with `[HUMAN CONFIRMATION NEEDED]` and not presented as settled.

Example: "Portal adoption rates in UK accounting practices typically settle between 40-60% [HUMAN CONFIRMATION NEEDED: source for this range?]."

### Treatment 4: Removed
If the claim cannot be verified, labelled, or flagged, it must not appear. Delete it.

### Treatment 5: Vendor-perspective assessment
The claim is framed as the publisher's assessment from a declared commercial position.

Example: "In our assessment, based on product design, workflow mechanics, and market positioning, Company Debt addresses the chasing layer more directly than tools designed primarily for internal workflow."

This treatment is distinct from Treatment 2 (editorial judgement) because it explicitly acknowledges commercial interest. It is required for evaluative claims about the house product's positioning relative to competitors.

### Required claim labels

Every evidence-carrying claim in comparison and review content should be mentally assignable to one of these labels:
- **Verified fact** — sourced, dated, attributable
- **Editorial judgement** — reasoned view with stated basis (Treatment 2)
- **Inference** — derived from available evidence but not directly sourced; must be flagged as such
- **Vendor-perspective assessment** — declared commercial position with reasoning (Treatment 5)

## 3a. What is a load-bearing claim?

A load-bearing claim is any claim that materially supports:
- the article's main recommendation
- the core differentiation between products or approaches
- the buyer decision or shortlist logic
- the cost or pricing argument
- the compliance or regulatory argument
- the comparison outcome or framework conclusion

If the claim were removed or shown to be false, the article's conclusion would weaken or collapse. These are the claims that carry the argument.

Claims that provide background context, define terms, or describe uncontested features are not load-bearing.

## 3b. Treatment 2 cap

Treatment 2 (editorial judgement) is a valid treatment. It is not a free pass.

Hard rules:
- No more than 30% of an article's load-bearing claims may rely on Treatment 2.
- Every Treatment 2 claim must state the reasoning basis in the text. "Based on the feature set and public pricing" is a reasoning basis. "In our view" is not.
- The Treatment 2 label must appear before or within the claim, not after it. A reader who stops reading before the label receives the claim as fact.
- If an article's central argument depends primarily on Treatment 2 claims, it fails evidence integrity regardless of individual claim quality.
- Editorial judgement may sharpen a conclusion. It may not carry the whole case.

**Detection test:** Count the load-bearing claims. Count how many use Treatment 2. If the ratio exceeds 30%, the article needs more sourced evidence or fewer assertions.

**Failure this prevents:** Editorial-judgement flooding. An article where every evaluative claim is labelled "editorial judgement" technically passes the four-treatment system but delivers no verifiable value to the reader.

### Per-article-type Treatment 2 modifiers

The 30% cap is the default. Some article types naturally carry more or less editorial judgement:

| Article type | Treatment 2 cap | Rationale |
|---|---|---|
| Tool review | 30% (default) | Readers expect sourced evidence for product claims |
| Comparison page | 30% (default) | Competitor claims must be verifiable |
| Category explainer | 40% | Category-level analysis requires more interpretive framing |
| Opinion-led post | 50% | The article's value is the argued position; readers expect judgement |
| Workflow / process guide | 25% | Process claims should be grounded in observable practice |

The per-type cap replaces the default 30% for that article type. All other Treatment 2 rules still apply: every Treatment 2 claim must state its reasoning basis, and the article's central argument must not depend primarily on Treatment 2 claims regardless of cap.

## 4. Hedging phrases that do not satisfy this rule

The following phrases do not convert a weak claim into a supported one:

- "tends to"
- "often"
- "usually"
- "from what I have seen"
- "can"
- "may"
- "typically"
- "in many cases"
- "for most practices"
- "generally speaking"

These are acceptable as natural language softeners in non-load-bearing sentences. They are not acceptable as the sole support for claims that carry the argument.

**Bad:** "From what I have seen, portal adoption rates often settle below vendor projections."

This sounds like evidence. It is not. The reader cannot verify it, challenge it, or build on it.

**Good:** "Portal adoption rates are not publicly benchmarked for UK accounting practices. Vendor projections vary, and independent data is limited. If your client base includes a high proportion of sole traders or clients over 50, expect adoption to be lower than headline figures suggest. [HUMAN CONFIRMATION NEEDED: can we source adoption benchmarks?]"

## 5. High-risk claim categories

These claim types require extra scrutiny because they frequently appear in Company Debt content and are frequently unsupported:

### Portal adoption rates
Claims about what percentage of clients use a portal. No public benchmark exists for UK accounting practices. Always flag or source.

### Response-rate uplifts
Claims that multi-channel chasing produces higher response rates than email alone. Vendor data exists but is not independent. Label the source and its limits.

### Time-saved claims
Claims like "200 hours drops to 15-20 hours." These require a calculation methodology, stated assumptions, and a link to the workings. Do not present as simple fact.

### Onboarding-duration claims
Claims about how long it takes to set up a tool. These vary by practice. State the range and the conditions.

### Channel-conversion claims
Claims that a specific percentage of clients respond to WhatsApp or SMS who did not respond to email. Vendor data is available but must be attributed with limits stated.

### Client-behaviour claims
Claims about how clients perceive automated messages, what motivates their delays, or how they respond to different channels. These are editorial interpretations unless backed by research. Label them.

### Market-behaviour claims
Claims about what "practices are doing" or how adoption is trending (e.g., "a growing number of practices are switching to X"). These require sourced evidence or a `[HUMAN CONFIRMATION NEEDED]` flag. Unsupported market-behaviour claims create false momentum narratives.

### Forward-looking negative claims
Claims that a competitor will not develop a capability or that a gap will persist (e.g., "the engagement capability does not fundamentally change"). These are predictions, not facts. Date them and add: "as of [date]; verify directly for current roadmap."

### Pricing comparisons
Claims that one tool costs more or less than another. Price the comparison with actual figures, stated assumptions, and a date.

### Compliance claims
Claims about GDPR, UK GDPR, data residency, or regulatory requirements. These must be accurate. Do not make compliance claims without checking current regulatory guidance or flagging for human confirmation.

### Product capability negatives
Claims that a competitor lacks a feature or capability. These must be verified from current documentation with a date, or flagged for confirmation.

## 5b. Evidence sensitivity rule for comparison pages

In comparison pages, the following claim types are high-sensitivity and must default to cautious phrasing unless directly verified:

- **best / strongest / only** — must be conditional (narrowed by use case), never universal
- **compliance-adjacent claims** — GDPR, UK GDPR, data protection, regulatory compliance
- **data residency / hosting claims** — must cite source documentation with date
- **exact pricing claims** — must cite pricing page with date
- **exact integration presence/absence claims** — must cite documentation with date
- **exact audit trail claims** — must cite product documentation, not marketing copy
- **exact competitor limitations** — must be verified or flagged

### Preferred phrasing for unverified sensitive claims

- "based on reviewed product documentation"
- "according to vendor materials reviewed in March 2026"
- "described by the vendor as..."
- "appears to..."
- "an audit trail designed to log contact and submission history" (rather than "MTD-compatible audit trail" unless verified)

### Disallowed smooth assertions

Do not write:
- "It's the only tool here that..."
- "It has UK data residency..."
- "It has an MTD-compatible audit trail..."

unless you are intentionally making a fully verified, publishable factual claim with source and date.

### Relationship to §5

This rule tightens the existing high-risk claim categories (§5) specifically for comparison pages, where smooth assertions are more damaging because they appear alongside competitor analysis and imply systematic evaluation.

---

## 5a. Authority fail state for commercial articles

This rule applies to commercial review, alternatives, comparison, and roundup articles.

### When it triggers
If a draft contains evaluative claims that cannot be supported by:
- public product information
- a stated reasoning chain
- comparison logic
- human-confirmed testing or experience

then the system must not fake confidence.

### Required response
When an evaluative claim lacks sufficient authority, do one of:
1. **Downgrade:** Rewrite the sentence into a clearly reasoned, narrower judgement with a visible reasoning basis
2. **Flag:** Insert `[HUMAN CONFIRMATION NEEDED]` or `[DEEP RESEARCH NEEDED]` where the article genuinely needs operator knowledge, testing, or stronger source-grounding

This is a quality-protection mechanism, not a last resort. Flagging for human input is better than bluffing.

### Specific triggers
- Avoid "The interface is more polished" unless there is a stated comparison basis
- Avoid "users find this frustrating" unless sourced or reframed as a reasoned inference
- Avoid "this works well for small firms" unless the buyer condition is specified (what size, what problem, what workflow stage)
- Avoid unqualified praise or criticism that could have been written without real familiarity

### Relationship to Treatment 2
Treatment 2 (editorial judgement) requires a stated reasoning basis. The authority fail state goes further: even with a reasoning basis, if the claim reads like it was generated from a product page rather than arrived at through analysis, it fails. The test is not just "is there a reason?" but "does the reader believe the writer actually thought this through?"

### Detection
For each major evaluative claim in a commercial software article, ask: "How does the writer know this?" If the answer is not visible in the surrounding prose, the claim fails the authority fail state and must be downgraded or flagged.

## 6. The sceptical reader test

For every evidence-carrying claim, ask: "If a sceptical reader asked 'how do you know that?', would the article give them a satisfying answer?"

If the answer is no, the claim fails evidence governance.

This test applies equally to first-party product claims about Company Debt. Claims like "migration cost is zero" must survive the same scrutiny as competitor claims. First-party claims can be just as misleading as third-party claims.

## 7. Source presentation rules

When citing evidence:
- Name the source
- State the date of the evidence
- State the type of source (product documentation, vendor data, independent research, editorial interpretation)
- State the limits of the evidence where relevant

Do not cite a source you have not checked or cannot attribute.

Do not fabricate screenshots, proof assets, or test results.

Do not present inferred points as verified facts.

Do not present editorial judgements as objective truth.

### 7a. Primary source rule (HARD RULE)

Product and financial data must be sourced from **primary sources only** — the banks, card issuers, financial providers, regulators (FCA, Bank of England, UK Finance, ONS, HMRC), and official industry bodies that originate the data.

**Never cite competitor comparison sites, affiliate aggregators, or third-party editorial sources as the basis for product claims.** This includes MoneySupermarket, MoneySavingExpert, NerdWallet, Finder, Forbes Advisor, TotallyMoney, CreditCards.com, and any equivalent.

Acceptable primary sources:
- The provider's own website (e.g., capitalontap.com, barclaycard.co.uk, americanexpress.com)
- The provider's Companies House filings or investor materials
- FCA register entries and regulatory submissions
- Bank of England statistical releases
- UK Finance industry data publications
- ONS or HMRC statistical publications
- The provider's Trustpilot or app store reviews (for user experience claims only, not product data)

Unacceptable sources for product claims:
- Comparison sites (MoneySupermarket, GoCompare, CompareTheMarket, etc.)
- Editorial aggregators (MoneySavingExpert, NerdWallet, Finder, Forbes Advisor, etc.)
- Affiliate review sites
- Other publishers covering the same product category

**Why:** Competitor sites introduce their own editorial framing, may carry outdated data, and citing them undermines Company Debt's authority as an independent source. A reader who sees us citing MoneySavingExpert for a rate that the bank publishes directly will question why we exist.

**Exception:** Academic research, FCA thematic reviews, and named industry reports (e.g., a UK Finance annual report) are acceptable even if they are technically third-party, because they are primary data producers in their own right.

**Detection test:** For every sourced claim, ask: "Did the data originate with this source, or did this source get it from somewhere else?" If the latter, go to the original source.

## 8. Decorative sourcing

Decorative sourcing is when a source is mentioned to create the appearance of evidence without actually supporting the specific claim.

**Bad:** "Industry research from Gartner suggests that SMS open rates exceed 90%." (The Gartner research may exist, but does it say what you are claiming, in the context you are claiming it?)

**Good:** "Gartner's 2023 Mobile Marketing Survey reported SMS open rates of 98% across consumer messaging. Business messaging rates may differ, and UK-specific data is limited."

**Detection question:** Does the cited source actually support this specific claim in this specific context? If you are not sure, flag it.

### Bidirectional sourcing check

Every source listed in the Sources section must be cited at a specific claim in the article body. Every in-text citation must appear in the Sources section. Orphaned sources (listed but never referenced in the body) are decorative sourcing regardless of whether the source is real.

## 9. Evidence governance checklist

Before finalising any article:

- [ ] Every evidence-carrying claim has one of the four treatments applied
- [ ] No more than 30% of load-bearing claims use Treatment 2 (editorial judgement)
- [ ] Every Treatment 2 claim states its reasoning basis in the text
- [ ] No central claim rests solely on hedging
- [ ] All sources are named, dated (with access/review date), and attributed
- [ ] All high-risk claim categories have been reviewed
- [ ] No decorative sourcing (bidirectional check: every source listed is cited in body, every body citation is in Sources)
- [ ] No fabricated evidence
- [ ] All comparison claims verified or flagged
- [ ] Compliance claims checked or flagged
- [ ] The sceptical reader test passes for every load-bearing claim
- [ ] Commercial software articles: authority fail state applied where evaluative claims lack sufficient grounding (§5a)

---

## 10. Corroboration requirement for comparison content

### Rules

- Comparative claims about what tools do, where they struggle, who they suit, or what practices are choosing must be assigned an evidence class (verified fact, editorial judgement, inference, or vendor-perspective assessment)
- Vendor-authored comparison pages should include corroborating external sources where useful (vendor pricing pages, feature documentation, independent reviews)
- Methodology must distinguish between product-page verification and editorial judgement
- Where a claim is based solely on product-page review, state that explicitly rather than implying hands-on testing

### Detection test

For each comparative claim, ask: "What type of evidence supports this?" If the answer is unclear, the claim needs an explicit label or a corroborating source.

---

## 11. Market-pattern claim controls

### Banned phrases (unless source-backed or explicitly marked as editorial judgement)

The following phrases introduce market-wide claims that are routinely asserted without evidence. They are banned unless they meet the replacement rules below.

| Banned phrase | Why banned |
|---|---|
| most common | market-wide frequency claim without data |
| growing number | trend claim without evidence |
| typically | statistical generalisation without source |
| tend to | frequency claim without source |
| often | frequency claim without source |
| consistent frustration | aggregate experience claim without data |
| common choice | market share assertion without source |
| large installed base | market position claim without source |

### Replacement rules

**If the claim is market-wide:** cite a named, dated source. If no source exists, the claim cannot be made as stated.

**If no source exists:** convert to bounded editorial judgement using the approved pattern.

**Approved pattern:**
> "In our assessment, based on product design, market positioning, and the workflow gap these firms are trying to solve, …"

**Disallowed patterns:**
> "A growing number of practices are…"
> "The most common frustration is…"
> "Searches for X tend to come from…"

## 12. Information gain check

Every article must pass an information gain audit before final draft approval. The purpose is to ensure the article adds value beyond what a reader could find by scanning the first page of search results.

### Per-article requirement

Identify at least 3 net-new value elements that are not reworded SERP consensus. Qualifying elements:
- first-hand testing detail or observed behaviour
- original comparison logic (a framework the reader hasn't seen elsewhere)
- proprietary scoring or classification
- clearer decision framework than the current SERP norm
- stronger trade-off analysis (naming what you lose, not just what you gain)
- uncommon but relevant caveat that other sources omit
- sharper language that makes the insight memorable and quotable

### Per-section (H2) requirement

Every H2 section must contain at least one of:
- a fact competitors usually omit
- a better explanation of why the fact matters
- a clearer recommendation tied to a specific user type
- a more exact trade-off than the current SERP norm

### Reject or rewrite triggers

Reject or rewrite any section that is:
- generic summary with no additive insight
- obvious industry filler ("business credit cards are an important financial tool")
- interchangeable with competitor copy (could appear on any comparison site unchanged)
- only "comprehensive" but not additive (listing everything without evaluating anything)

### Paragraph-level test

Measure information gain per paragraph. If a paragraph does not add new evidence, new interpretation, or better decision support, cut it. Every paragraph must earn its place.

### What this is NOT

Do not chase novelty for its own sake. Prefer:
- original evidence over empty contrarianism
- original framing over manufactured hot takes
- original synthesis over surface-level disagreement with consensus

If the consensus is correct, say so — but say it better, with more precision, for a more specific reader.

### Detection

During trust pass and adversarial review, score each H2 section: does it contain at least one information-gain element? Tally across the article. Fewer than 3 net-new elements across the entire article = hard fail. Any H2 section with zero information-gain elements = rewrite that section.

---

### Hard rule: inference is not evidence

- **Search-intent inference is not evidence.** Stating what readers "tend to be looking for" based on a keyword or category is not a factual claim.
- **Category knowledge is not evidence.** Knowing the category does not constitute data about how many firms behave in a particular way.
- **Plausible market logic is not evidence** unless it is explicitly framed as editorial judgement using the approved pattern.

### Detection test

For every sentence containing a banned phrase, ask: "What is the basis for this claim?"

- If the basis is a named, dated source: acceptable.
- If the basis is editorial judgement with a stated reasoning chain: acceptable with Treatment 2 label.
- If the basis is category familiarity, inference, or plausible logic presented as fact: **fail**.

---

## §12 Source constraint: original sources only

**Hard rule.** All sourced claims must reference original providers, regulators, industry bodies, or recognised independent data sources. Never source from competitor comparison sites.

**Acceptable sources:** provider direct (bank, issuer, fintech), FCA, Bank of England, UK Finance, British Business Bank, ONS, HMRC, Companies House, GOV.UK, Experian/Equifax/TransUnion (methodology or public data), Moneyfacts, Defaqto, Which? (market-wide data, not editorial opinion).

**Never acceptable:** MoneySupermarket, NerdWallet, Finder, TotallyMoney, Forbes Advisor, or any competitor comparison/affiliate aggregator site.

If the only available source is a competitor site, the claim must be independently verified against the provider's own documentation, or flagged with `[VERIFY — only competitor source found]`.

Full rules and enforcement: `23-prose-quality-gates.md` §10.

---

## §13 Distress reassurance evidence rule

Do not use broad market statistics to imply low personal risk.

If a statistic is used to reassure a distressed reader, the copy must:
- state what the statistic does and does not show
- avoid derived emotional conclusions
- tie the number to a concrete legal or process point

**Allowed:** "Liquidation does not automatically mean disqualification. The Insolvency Service investigates conduct, not the fact of liquidation itself."

**Restricted:** Broad ratio-based reassurance implying personal safety from aggregate market data (e.g. "only 4% of directors face action, so your odds are good").

### Rationale

Population-level statistics can easily become over-comforting or legally imprecise. A director reading this content needs to understand that outcomes depend on their specific conduct, not on sector averages. Using aggregate data primarily to calm fear creates a trust risk and a potential regulatory exposure under YMYL standards.

---

## §14 Reassurance claim classes

Classify reassurance claims before publication.

**Class A: legal/process reassurance**
Example: "Liquidation does not automatically mean disqualification."
Allowed with sourced legal/process basis.

**Class B: population-level directional reassurance**
Example: "Thousands of directors go through this every year."
Allowed with attribution and no personal inference.

**Class C: experiential reassurance**
Example: "Most directors find the process more manageable than expected."
Not allowed unless based on named internal research, surveys, or attributable case evidence.

### Rule

Do not use Class C reassurance in YMYL pages without an explicit evidence source. If evidence is absent, replace with process-based reassurance (Class A), not emotional assertion.

### Enforcement

If a reassurance claim cannot be evidenced, remove it or convert it into a concrete process statement. Class C claims without sources fail this gate.

### Reassurance standard

All reassurance on distressed-director pages must be:
- tied to a legal or process reality (not just emotional comfort)
- bounded (state what it does NOT guarantee)
- followed within 1-2 sentences by a concrete action or condition

Disallow vague reassurance based on "most" or "many" without:
- a named source
- a stated limit of inference
- an adjacent operational fact

**Allowed:** "Liquidation does not automatically mean disqualification. The Insolvency Service investigates conduct, not the fact of liquidation itself. But if you traded while insolvent or paid yourself preferentially, those are the areas of exposure."

**Not allowed:** "Most directors find the process easier than they expected." (No source, no boundary, no action.)
