# Skills Architecture (v1 — DEPRECATED)

> **DEPRECATED as of v2.1.** This file describes the v1 skill stack and does not reflect v2 governance rules.
> Use instead: `03-workflow-playbook.md` (10-stage workflow with hard checklists) and `06-prompt-library.md` (v2 prompts with governance cross-references).
> Do not use this file as a compliance reference. The v2 workflow playbook and governance files (09-16) supersede everything below.

Claude Skills are useful only where they enforce quality or repeatability.
## Recommended skill stack
### 1. Audience & Intent
Purpose:
Define reader, real question, decision type, and satisfying outcome.
Inputs:
- topic
- content type
- target page or brief
Decision rules:
- reject vague audience framing
- force one core question
- force one decision outcome
Outputs:
- reader-intent brief
- decision statement
- outcome statement
Limits:
- cannot invent business priorities
### 2. Source Grounding
Purpose:
Turn source material into labelled claim sets.
Inputs:
- notes
- URLs
- screenshots
- docs
- product pages
Decision rules:
- classify every important claim as fact, inference, judgement, or human-confirmation-needed
- downgrade unsupported certainty
Outputs:
- source-grounding map
- risk flags
- missing evidence list
Limits:
- cannot verify hidden or private facts
### 3. Editorial Judgement
Purpose:
Turn evidence into a clear, supportable editorial line.
Inputs:
- source-grounding map
- topic
- reader-intent brief
Decision rules:
- force a point of view
- identify strongest trade-off
- identify who should and should not choose the option
Outputs:
- editorial angle
- recommendation logic
- thesis line
Limits:
- no unsupported strong claims
### 4. Voice DNA
Purpose:
Apply Company Debt's authored, calm, expert voice.
Inputs:
- outline or draft
Decision rules:
- remove fluff
- remove filler intros
- tighten judgement
- improve scanability
- preserve uncertainty markers
Outputs:
- revised draft in Company Debt voice
Limits:
- voice must not override evidence honesty
### 5. Trust Architecture
Purpose:
Apply sourcing, disclosure, byline, updated-date, and credibility standards.
Inputs:
- draft
- source-grounding map
Decision rules:
- check source honesty
- check methodology note
- check disclosures
- check labelling of comparisons and claims
Outputs:
- trust pass notes
- corrected draft elements
Limits:
- cannot fabricate proof assets
### 6. Adversarial Review
Purpose:
Stress-test the draft like a sceptical expert and a time-poor buyer.
Inputs:
- draft
- brief
- source-grounding map
Decision rules:
- identify generic sections
- identify weak logic
- identify unsupported claims
- identify where the draft fails to help a real decision
Outputs:
- attack notes
- rewrite priorities
- pass/fail judgement
Limits:
- still bound by evidence base
## Skill order by content type
Default order:
1. Audience & Intent
2. Source Grounding
3. Editorial Judgement
4. Outline
5. Draft
6. Voice DNA
7. Trust Architecture
8. Adversarial Review
9. Human input insertion
10. Final revision
