# Agent Workflow — Execution Modes and Decision Authority

Adapted from vinicius91carvalho/.claude compound engineering system.
This file governs agent behaviour during editorial and development tasks.
It does not override any editorial governance rules (09-18).

Runtime context rule:

- humans should not need to decide which runtime packs to use in routine work
- the system should resolve the smallest relevant context automatically
- if runtime compression weakens human authorship, decision usefulness, or trust, reject it

---

## Value Hierarchy

When two values conflict, higher rank wins:

1. **Editorial integrity** — Trust, evidence honesty, disclosure architecture are non-negotiable
2. **Functional correctness** — Content that is accurate > content that sounds polished
3. **Decision usefulness** — Reader can act on the content
4. **Authorship credibility** — Prose sounds human, not generated
5. **SEO performance** — Optimise only after editorial integrity is satisfied

## Autonomous Decision Authority

| Agent CAN decide alone | Agent MUST ask user | Agent NEVER does |
|---|---|---|
| Paragraph rewording within governance rules | Article structure changes | Publish to staging without approval |
| CSS/styling decisions within design tokens | New article types or templates | Delete existing governance rules |
| Sentence-level evidence treatment upgrades | Changes to comparison governance | Override evidence treatment requirements |
| Internal link placement | Tone or voice stance changes | Fabricate sources or testing claims |
| Fix typos, formatting, block markup | Pricing claim changes | Remove disclosure or trust architecture |
| Section reordering within an article | New SEO signal rules | Push to production |

## Escalation Logic

The agent MUST stop and ask when:

1. The task is ambiguous and there are 2+ reasonable interpretations
2. The proposed change conflicts with a documented governance rule
3. Actual scope is significantly larger than expected (>2x estimated files)
4. An unrelated problem is discovered during implementation
5. The decision falls in the "MUST ask" column above
6. A content claim cannot be verified and needs human confirmation

Question format: `[DECISION NEEDED] Context: [brief]. Option A: [X]. Option B: [Y]. My recommendation: [A/B], because [reason]. Proceed?`

---

## Execution Modes

Switch modes freely within a single task. Match ceremony to complexity.

### Quick Fix

**When:** Single file, <30 lines, no structural impact, clear fix.
**Process:** Fix directly, verify, capture learning if novel.
**Editorial examples:** Typo fix, single claim softening, formatting correction, block markup repair.

### Standard

**When:** Multi-file, clear scope, moderate complexity.
**Process:** Read existing state → plan approach → implement → verify with scripts → capture learnings.
**Editorial examples:** SEO signal fix pass across articles, voice governance enforcement, single article rewrite.

### PRD + Sprint (Checkpoint Workflow)

**When:** Large feature, multi-component, or >1h of work.
**Process:** Break into units → define exit criteria per unit → complete one → verify → next.
**Editorial examples:** Full system patch integration, new governance layer addition, 16-article content pass.

See `docs/checkpoint-workflow.md` for the checkpoint protocol.

---

## Compound Learning Capture

After completing a significant task:

1. **What was the hardest decision made here?**
2. **What alternatives were rejected, and why?**
3. **What are we least confident about?**

If the answers reveal a pattern:
- Project-specific learning → save to memory
- Repeated pattern → propose governance rule update
- Missing enforcement → propose script check

---

## Anti-Premature Completion Protocol

A task is not complete just because:
- "All scripts pass" — scripts can pass while content is broken
- "All edits applied" — edits can be applied while the article reads poorly
- "All items checked" — items can be checked while verification was skipped

Before claiming completion, verify:
1. Re-read the original brief or spec (not from memory)
2. Enumerate remaining unchecked items
3. Cite specific evidence for each acceptance criterion
4. Run relevant enforcement scripts and show output
5. If content: read the article as a sceptical reader and check it passes the lived-friction test

---

## Anti-Goodhart Verification

When a measure becomes a target, it ceases to be a good measure.

In editorial work:
- "SEO checker passes" ≠ article is good (checker catches signals, not quality)
- "No governance failures" ≠ article is trustworthy (governance catches patterns, not intent)
- "Word count met" ≠ article has depth (words can be padding)
- "FAQ section present" ≠ FAQs are useful (FAQs can be generic)

After every check, ask: "Does this article actually help a real reader make a better decision?" If the answer is uncertain, the article needs more work regardless of what the scripts say.

---

## Tradeoff Resolution by Content Type

| Content type | Optimise for | Acceptable to sacrifice |
|---|---|---|
| Comparison page | Trust, fairness, decision utility | Word count, SEO completeness |
| Review | Evidence depth, observed detail | Breadth of features covered |
| Guide | Practical usefulness, consequences | Exhaustive coverage |
| Roundup | Decision speed, honest fit/misfit | Detailed analysis per tool |
| Blog post | Authorship credibility, insight | SEO feature checklist |

---

*This file adapts the compound engineering principles from vinicius91carvalho/.claude for the Company Debt editorial workflow. It delegates to the editorial governance system (09-18) for all content-specific rules.*
