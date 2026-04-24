# 25. Operational Learning Loop

This file governs how Company Debt absorbs workflow learnings from repeated production work.

It does not change editorial doctrine.
It does not lower the quality bar.
It exists to improve execution reliability without letting the system drift into weaker writing, softer evidence, or laxer gates.

Origin: ported from BusinessExpert editorial system, domain-neutral sections only.

---

## Core distinction

There are two kinds of learning:

1. **Editorial doctrine**
   Voice, evidence, trust, disclosure, and reader-service standards.
   These live in the canonical governance files and should change rarely.

2. **Operational learning**
   Repeated failure patterns, recovery moves, checkpoint gaps, packet-shaping improvements, and thread-management tactics.
   These can and should improve as the system runs.

Only the second category belongs here.

If a proposed "learning" would weaken sourcing, flatten trade-offs, soften disclosure, or excuse generic prose, reject it.

---

## What counts as a valid operational learning

A valid operational learning usually does one of these jobs:

- prevents a repeated failure before it happens
- makes a recurring fix more bounded and repeatable
- reduces wasted context without thinning the quality kernel
- improves stage handoffs and checkpoint clarity
- makes review output easier to act on
- preserves authored quality under longer-running workflows

Examples of valid operational learnings:

- "refresh the packet instead of continuing a bloated thread"
- "fix only the named failed surfaces rather than rewriting the whole page"
- "treat repeated paragraph monotony as an early drafting issue, not a final-polish issue"
- "surface heading-payoff failures at draft stage, not after final review"
- "promote repeated fix patterns into worker guidance only after they succeed multiple times"

Examples of invalid operational learnings:

- "allow weaker sourcing if the page reads well"
- "drop balancing language to improve conversion"
- "skip trust checks when the comparison feels obviously right"
- "reduce reader-consequence language because it takes tokens"
- "treat generic confidence as acceptable if the structure is clean"

---

## Conductor rule

The orchestration layer stays the conductor.
Its job is to preserve sequence, checkpoints, and standards.
It must not become an improvising writer that decides the rules are optional.

Operational consequence:

- routing tools route
- runtime packs execute
- canonical governance resolves ambiguity
- gates decide publish readiness

If a workflow improvement blurs those roles, do not adopt it.

---

## Checkpoint discipline

Every substantive page task should have visible exit criteria before the next stage begins.

Minimum checkpoint logic:

- **Research** is not complete until the brief, source-grounding map, and decision question are all usable
- **Outline** is not complete until the structure shows a clear decision path and no placeholder logic remains in the key sections
- **Draft** is not complete until the page has a real verdict, fit/misfit logic, and required end-matter
- **Review** is not complete until findings are specific enough to revise without reopening the whole system
- **Revision** is not complete until the named failures were actually addressed, not merely rephrased
- **Pre-publish** is not complete until the formal gate has run and the remaining risks are explicit

Do not advance stages on vibes.
Advance them on evidence.

---

## Fresh-thread rule

Long-running threads degrade judgment, hide unresolved assumptions, and encourage broad rewrites instead of precise fixes.

When a task becomes context-heavy:

- regenerate the compact packet
- start a fresh thread
- carry forward only the live page, the current task, the active stage pack, and the relevant notes

Do not treat accumulated thread history as an asset by default.
Very often it is where avoidable drift begins.

---

## Quality-kernel preservation rule

Context may be compressed.
Standards may not.

Whenever workflow context is trimmed, the following must remain intact:

- the writer core
- the relevant stage pack
- the page-class overlay
- the human-authorship / trust layer

Operational compression that removes these is not optimisation.
It is quality loss.

---

## Failure logging rule

Repeated failures should be named consistently.

Good operational learning depends on normalising failures into stable buckets such as:

- heading-payoff miss
- pronoun starvation
- paragraph monotony
- repeated-phrase drift (see `14-failure-modes-and-recovery.md` §28)
- unsupported comparison claim
- weak fit/misfit guidance
- verdict neutrality
- revision overshoot
- packet bloat
- ambiguous review note

If a failure cannot be named, it is hard to improve systematically.

---

## Promotion rule

Do not promote a fix into default system behaviour because it worked once.

Promote only when all three are true:

1. the same failure appeared more than once
2. the same fix materially improved the result more than once
3. the fix does not weaken doctrine or narrow editorial honesty

Promotions should normally take one of these forms:

- add a reminder to a runtime pack
- tighten a stage checklist
- clarify a checkpoint
- improve revision instructions
- add or extend a deterministic check

Do not promote one-off preferences into system law.

---

## Revision containment rule

Most revisions should be narrower than the instinct suggests.

When review finds bounded failures:

- fix the named surfaces first
- preserve what is already working
- avoid full rewrites unless the structure, trust posture, or core argument is broken

This is especially important after a draft has already developed authored texture.
Broad rewrites often remove exactly the qualities the system is trying to preserve.

---

## Transfer rule for learnings from other systems

Before migrating a learning from another repo or vertical, test it against these questions:

1. Is this about execution reliability rather than domain content?
2. Does it improve decision-useful writing, trust, or workflow control in a domain-neutral way?
3. Can it be stated without importing niche voice, persona, or subject-matter assumptions?
4. Would it still help if the topic changed completely?

If the answer is no to any of these, do not import it as a system-level rule.

---

## What to do with a new learning

Use this order:

1. Classify the issue as doctrine, operations, or one-off
2. If operational, decide whether it belongs in:
   - a stage pack
   - a runtime pack
   - a checklist
   - a script check
   - or this governance file
3. Keep the change as small and local as possible
4. Re-benchmark the workflow if the change affects runtime-pack behaviour
5. Reject the change if quality improves only by making the voice flatter or the evidence softer

---

## Batch vs single-page boundary

Mechanical quality fixes (payoff-intent openers, paragraph-length variation, H2 keyword insertion, lived-reality anchor insertion) can be batched across pages. They are pattern-matching problems with deterministic verification.

Editorial-judgement fixes MUST NOT be batched. This includes:

- **concrete_scenes**: Operational moments must be specific to the page's subject, reader, and argument. A "director receives a statutory demand on Friday" scene that works on a winding-up page is meaningless on an MVL page. Batching produces identical templated scenes across multiple articles — the opposite of authored voice.
- **evaluative_bite**: Compressed-truth sentences must stake a position that only makes sense in context. "The gap is real" means something different on a wrongful trading page than a CVL page. Batch-inserted bites are decorative filler, not editorial judgement.
- **ai_fingerprints**: Rewriting synthetic patterns requires reading the surrounding prose to find a replacement that carries the same meaning in sharper language. Find-and-replace produces flat, generic rewrites.
- **concrete_scenes_distribution**: Spreading scenes requires understanding which sections carry the article's argument. Mechanical distribution produces even spacing, not editorial emphasis.

**Rule: If the fix requires reading the article to get right, it cannot be batched.**

Process editorial-judgement fixes one page at a time through the Bernstein per-page workflow. Load the full config, read the prose in context, write fixes that fit this specific article. Verify, then move to the next page.

---

## Scope discipline on mechanical tasks

When a task is scoped to a single mechanical operation (e.g. update a meta field, fix a title tag, push a CSS change), do only that operation. Do not expand into rebuilding pages, regenerating content, or triggering adjacent workflows unless explicitly instructed.

**The anti-pattern:** Asked to fix a meta description → updated the field (correct) → then rewrote the article introduction because it "felt weak" (wrong). Each unrequested expansion adds risk and wastes context.

**The rule:** Match tool to task. Do not escalate tool scope beyond what the task requires.

---

## Title tag quality: hooks must be specific

When writing or reviewing SEO title tags, the hook (the part after the colon) must name the actual decision tension of that specific page — not describe its format.

**Weak hooks:**
- "Explained" — describes format, not content
- "Your Options" — generic across every advice page
- "What You Need to Know" — defers the decision rather than framing it

**The test:** Could this hook appear on any other page in the same section? If yes, it is not specific enough. The hook should name the trade-off, the condition, or the differentiator.

**Examples of the correction:**
- "CVL: Explained" → "CVL: Director Control vs Compulsory Liquidation"
- "Wrongful Trading: Your Options" → "Wrongful Trading: When Civil Liability Becomes Personal"
- "Bounce Back Loans: What You Need to Know" → "Bounce Back Loan Default: Personal Liability and Your Options"

---

## Non-negotiable outcome

The system should become easier to run, easier to recover, and harder to derail.

It should not become easier to publish thin, generic, under-evidenced, or over-smoothed content.
