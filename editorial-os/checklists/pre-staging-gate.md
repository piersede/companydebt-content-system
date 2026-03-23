# Pre-Staging Gate

Run this checklist before pushing any content to the WordPress staging database. Every item must pass. Any failure = revise before pushing.

This is not the full pre-publish gate. It is the minimum quality floor for staging pushes. The full pre-publish gate (`16-pre-publish-gate.md`) must still pass before production publication.

---

## Pass 1: Human-authorship integrity (run first)

Source: `docs/human-authorship-voice-engine.md` Rules A–J

| # | Question | Pass/Fail |
|---|----------|-----------|
| H1 | Does the article contain observed detail rather than just evaluation? (Rule A) | |
| H2 | Does every major evaluation get explained into consequence? (Rule B) | |
| H3 | Does each major section contain lived operational reality? (Rule C) | |
| H4 | Does tone change appropriately by subject? (Rule D) | |
| H5 | Do praise and criticism both include friction? (Rule E) | |
| H6 | Is there at least one asymmetrical, editorially alive compression line? (Rule F) | |
| H7 | Is "we" earned wherever used? (Rule H) | |
| H8 | Have vendor/category labels been interrogated rather than inherited? (Rule I) | |
| H9 | Does the verdict compress the real decision? (Rule J) | |

Failure threshold: any "fail" on H1–H9 = revise the relevant section before pushing.

---

## Pass 2: SEO signal checklist

Source: `18-seo-signal-governance.md` §Pre-publish SEO signal checklist

| # | Check | Pass/Fail |
|---|-------|-----------|
| S1 | Title promise fully delivered in article body | |
| S2 | Zero generic anchor text ("click here", "read more", etc.) | |
| S3 | Zero banned authenticity phrases | |
| S4 | Every verdict sentence followed by evidence basis within 3 lines | |
| S5 | No one-sentence FAQ answers; no "see above" cross-references | |
| S6 | Core topic vocabulary present naturally | |
| S7 | Named author byline present | |
| S8 | Article links to at least 2 other site pages with descriptive anchors | |
| S9 | Article linked from at least one existing page (or scheduled) | |
| S10 | Every image has specific, descriptive alt text | |
| S11 | Last-reviewed date visible on decision-stage pages | |
| S12 | No more than one BusinessExpert CTA per article | |

---

## Pass 3: Comparison page readiness (if applicable)

Source: `16-pre-publish-gate.md` Checks 14a + 15

Only run this pass on comparison, roundup, alternatives, and review articles.

| # | Check | Pass/Fail |
|---|-------|-----------|
| C1 | No direct-product claims without observed detail or desk-based framing | |
| C2 | No floating evaluative phrases without consequence | |
| C3 | No sections lacking lived-reality anchors (max 1 weak section) | |
| C4 | No monotone across sections with different editorial purpose | |
| C5 | No generic pros/cons phrasing | |
| C6 | Opener is not winner-first | |
| C7 | Early decision module present | |
| C8 | BusinessExpert misfit appears before first product deep dive | |
| C9 | Verdict language not repeated more than twice (intro + conclusion) | |
| C10 | Product sections do not all expose identical template scaffold | |

---

## Execution rule

This gate fires at the point of action — before the staging push command runs. Not at the abstract end of a workflow. Not after push. Before.

If the content was a rewrite (>20% of body changed), the full workflow from Stage 5 onward must have been completed before this gate is reached.
