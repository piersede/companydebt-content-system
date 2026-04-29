# Component Pack: Distress / Use-Case Pages

Apply 2–3 of the following. Never all. Full specs: `editorial-os/28-readability-components.md`.

## Recommended stack

**1. Orientation Block** (`.cd-orientation-block`) — Primary
- Place near the top, after the opening paragraphs, before the first major H2.
- Why: Blueprint 2 triage pages serve directors at different stages of the same crisis. The orientation block tells them immediately whether this page applies to their specific situation.
- Skip if: the opening already names the exact audience clearly enough that a separate block adds nothing.

**2. Risk Warning or Legal Exposure callout** — Primary
- Place in the top third of the page, where the statutory exposure first appears.
- `cd-callout--risk-warning`: use where a deadline or enforcement threshold is the primary risk.
- `cd-callout--legal-exposure`: use where director liability (wrongful trading, preference, disqualification) is the subject.
- Evidence level A only. Cite the statute. QA gate applies for Legal Exposure.
- Do not use both on the same page.

**3. Recovery Path callout** (`.cd-callout--recovery-path`) — Primary
- Place after the options section, before the closing CTA.
- Why: Triage pages map multiple routes. A Recovery Path box anchors the multi-route framing so the reader doesn't feel pushed toward one answer prematurely.
- Skip if: only one route is realistically available — use prose in that case.

**Process Steps** (`.cd-process-steps`) — Secondary
- Use where "what happens next" needs to feel clear and reassuring.
- 3–5 steps. Not adjacent to Recovery Path callout.

**Inline CTA** (`.cd-inline-cta`) — Secondary
- Place after the highest-intent section, well before the closing CTA.
- One per page. Not within two sections of the page-end CTA.

## Rhythm constraint

Max 3 components. Never two same-type blocks adjacent. No component in the first two paragraphs. At least one prose section between any two components.
