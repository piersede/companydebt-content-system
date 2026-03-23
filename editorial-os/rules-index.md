# Rules Index — Company Debt Editorial OS v2.3

One source of truth per rule. If a future rule overlaps with an existing entry, extend the existing source rather than creating a parallel rule elsewhere.

---

## Human-authorship rules (A-J)

| Rule | Name | Source |
|------|------|--------|
| A | Observed detail in product claims | `docs/human-authorship-voice-engine.md` |
| B | Cashed-out evaluations | `docs/human-authorship-voice-engine.md` |
| C | Lived-reality anchors | `docs/human-authorship-voice-engine.md` |
| D | Tonal modulation by subject | `docs/human-authorship-voice-engine.md` |
| E | Friction in praise and criticism | `docs/human-authorship-voice-engine.md` |
| F | Asymmetrical editorial lines | `docs/human-authorship-voice-engine.md` |
| G | Generic pros/cons ban | `docs/human-authorship-voice-engine.md` |
| H | Earned institutional "we" | `docs/human-authorship-voice-engine.md` |
| I | Vendor/category language interrogation | `docs/human-authorship-voice-engine.md` |
| J | Compressed reality-based verdicts | `docs/human-authorship-voice-engine.md` |
| K | Guided scenario language | `09-voice-governance.md` §10 |
| L | Alternatives means alternatives | `09-voice-governance.md` §11 |
| M | Human consequence anchoring | `09-voice-governance.md` §12 |

## Article-type specific rules

| Rule cluster | Source |
|--------------|--------|
| Review-specific humanisation | `docs/article-types/review.md` |
| Comparison disarmament and vendor-language interrogation | `docs/article-types/comparison.md` |
| Roundup anti-ghost-listicle rules | `docs/article-types/roundup.md` |
| Guide friction / consequence translation | `docs/article-types/guide.md` |

## Commercial comparison governance

| Rule family | Source |
|-------------|--------|
| Commercial comparison page mode | `11-comparison-governance.md` §8 |
| Trust-first vendor comparison | `11-comparison-governance.md` §9 |
| Category-framing neutrality | `11-comparison-governance.md` §10 |
| House-product containment | `11-comparison-governance.md` §11 |
| Disclosure architecture | `11-comparison-governance.md` §12 |
| Alternatives-page integrity | `11-comparison-governance.md` §13 + `05-scoring-rubric.md` A1-A8 |

## Evidence governance

| Rule family | Source |
|-------------|--------|
| Five claim labels | `10-evidence-governance.md` §3 (Treatments 1-5) |
| Corroboration requirement | `10-evidence-governance.md` §10 |
| Market-pattern claim controls | `10-evidence-governance.md` §11 |

## Voice and tone governance

| Rule family | Source |
|-------------|--------|
| Vendor-perspective tone discipline | `09-voice-governance.md` §8 |
| Conclusion-before-CTA | `09-voice-governance.md` §9 |
| Human tone and reader handling | `09-voice-governance.md` §13 |
| Buyer-trigger intros | `09-voice-governance.md` §14 |
| Floating evaluative phrase bans | `09-voice-governance.md` §5 (disallowed stand-alone evaluation) |
| Thin authenticity-marker bans | `09-voice-governance.md` §5 (disallowed authenticity markers) |

## Comparison page prose discipline (v2.3 patch 3)

| Rule family | Source |
|-------------|--------|
| Winner-first opener ban | `11-comparison-governance.md` §12a |
| Conditional verdict rule | `11-comparison-governance.md` §12a |
| Bracket-stacked proof ban | `11-comparison-governance.md` §12b |
| Repeated verdict phrasing limit | `11-comparison-governance.md` §12b |
| Template visibility rule | `11-comparison-governance.md` §12b |
| Generic intensifier ban (comparison-specific) | `11-comparison-governance.md` §12b |
| Evidence sensitivity for comparison pages | `10-evidence-governance.md` §5b |
| Comparison page publish-readiness | `16-pre-publish-gate.md` Check 15 |
| Checkpoint workflow for large refactors | `docs/checkpoint-workflow.md` |

## Scoring and evaluation

| Rule family | Source |
|-------------|--------|
| Commercial comparison trust checks (T1-T6) | `05-scoring-rubric.md` |
| Trust-failure cap | `05-scoring-rubric.md` |
| Alternatives-page integrity scoring (A1-A8) | `05-scoring-rubric.md` |

## Failure modes

| Rule family | Source |
|-------------|--------|
| False neutrality (FM-13) | `14-failure-modes-and-recovery.md` |
| Taxonomic human-flattening (FM-25) | `14-failure-modes-and-recovery.md` |
| Alternatives page collapse (FM-26) | `14-failure-modes-and-recovery.md` |
| Mixed-confidence and meta-copy (FM-27) | `14-failure-modes-and-recovery.md` |

## Prose quality gates (YMYL financial copy)

| Gate | Purpose | Source |
|------|---------|--------|
| §1 Fact Pattern Gate | Block mixed-confidence copy in same paragraph | `23-prose-quality-gates.md` §1 |
| §2 Scenario Validity Gate | Stop unsupported hypothetical reader scenarios | `23-prose-quality-gates.md` §2 |
| §3 Meta-Copy Stripper | Remove self-referential comparison-site filler | `23-prose-quality-gates.md` §3 |
| §4 Human-Impact Enforcer | Force reader consequence in every finance paragraph | `23-prose-quality-gates.md` §4 |
| §5 Product-Type Clarity Rule | Handle hybrid/non-standard products cleanly | `23-prose-quality-gates.md` §5 |
| §6 Generic-Intensifier Ban | Replace empty emphasis with exact mechanism | `23-prose-quality-gates.md` §6 |
| §7 YMYL Comparison Opening Router | Problem-led, utility-first comparison intros | `23-prose-quality-gates.md` §7 |
| §8 Financial Objectivity Check | Ensure promoted cards show drawbacks/limits | `23-prose-quality-gates.md` §8 |
| §9 Sentence Texture Calibrator | Reduce AI cadence, vary sentence structure | `23-prose-quality-gates.md` §9 |
| §10 Source Constraint | Original sources only, never competitor sites | `23-prose-quality-gates.md` §10 |

## Enforcement scripts

| Script | What it checks | Source |
|--------|---------------|--------|
| check_comparison_integrity.js | A1-A7, Rule K, Rule L | `checklists/` |
| check_trust_architecture.js | T1-T6, methodology | `checklists/` |
| check_intro_quality.js | Banned openers, buyer trigger, decision frame, vague market language | `checklists/` |
| check_human_tone.js | Taxonomy labels, headings, clipped sentences, noun repetition, abstract shorthand, lived-friction | `checklists/` |

## Script enforcement gaps (registered, not yet mechanical)

The following checks are not yet covered by scripts. Prefer extending existing checks over creating new scripts.

- Floating evaluative phrases without concrete consequence (extend `check_human_tone.js`)
- Direct-experience claims without observed detail (extend `check_human_tone.js` or new `check_authorship.js`)
- Generic pros/cons bullets (extend `check_human_tone.js`)
- Verdict neutrality / over-balanced endings in review and comparison pieces (extend `check_comparison_integrity.js`)
- Sections lacking lived operational anchors in substantive commercial-software articles (extend `check_human_tone.js`)

---

*Last updated: v2.3 patch integration, March 2026*
