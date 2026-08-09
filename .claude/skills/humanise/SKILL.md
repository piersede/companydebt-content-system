---
name: humanise
description: Rewrite a Company Debt page so it reads as an experienced practitioner thinking, not as content written to sound human. Fixes manufactured hooks, neat reversals, borrowed empathy and decorative prose by rebuilding each paragraph on a real observation. Use for any page that passes the gate but still reads as AI, and for the site-wide voice rollout.
---

# Humanise

Most pages on this site have the same fault. They are accurate, well sourced,
correctly structured, and they read as though nobody with any experience wrote
them. This skill fixes that page by page.

Full reference: `runtime-packs/stages/humanise.md`. Read this file for the
method; open the pack when you need the detail behind a rule.

## The one rule that matters

**Make the writing human through insight, not decoration.**

The failure is imitating human *prose* when the target is imitating human
*thought*. Every marker the gate checks for, and every point in the Which?-style
spec, can be satisfied by decoration. Decoration is what gets pages sent back.

Before writing any paragraph, ask: **what would an experienced insolvency
practitioner notice here that a generic writer would miss?** Build the paragraph
on that. If there is no answer, the paragraph is padding and no amount of
rhythm, warmth or British texture will save it.

An expert usually writes more plainly, because the interesting thing is what
they know.

> Prefer: "There are actually two different timelines here."
> Over: "You may hear anything from ten days to five years, and both answers are right."

The first sounds like somebody explaining something. The second sounds like
somebody writing content.

## Diagnosing a page

Read it and mark every instance of these. They are the tells:

| Tell | Example |
|---|---|
| Manufactured hook | "Ask X and you'll hear anything from..." |
| Provocative line, neat explanation, clever closer | the single most recognisable AI paragraph shape |
| Neat reversal / clever final clause | "and nobody tells you which one you asked" |
| Dramatic one-line paragraph used for effect | a one-liner is fine when it carries a fact, not when it lands a point |
| Borrowed empathy | "the thing keeping you awake at night" |
| Decorative adverbs | "Sadly", "Unsurprisingly" dropped in for personality |
| Repeated rhetorical shape | the same "that is the [noun]" or "not X, Y" construction 3+ times |

Borrowed empathy is the hardest to see. The test: would this sentence sit
unchanged on a debt, legal, medical or divorce page? Then it is filler, however
kind it sounds.

## The rewrite method

For each flagged sentence, find the observation it was dressing up and write
that instead. Worked examples from the liquidation timeline page:

- "Ask how long it takes and you'll be told anything from ten days to five
  years. Both answers are given in good faith." became "There are really two
  answers to how long a company liquidation takes", followed by what each one
  measures. The insight was always the two timelines; the hook was in the way.
- "When does this stop being the thing you lie awake thinking about?" became
  "most directors are asking about the first date, not the second". Naming what
  the reader actually wants to know is more empathetic than describing their
  feelings.
- "You are a witness to it, not a participant" became "the liquidator makes the
  decisions in it; your role is to answer questions when asked". Same point,
  now useful.
- "Ask any firm making that claim what happens on day eight" became "adverts
  promising liquidation in seven days are describing this first stage only".
  The scepticism survives; the flourish does not.

**Do not add empathy. Demonstrate understanding** by identifying what the reader
is really trying to find out, then answering that.

Flat-rewrite test: rewrite the clever sentence plainly. If nothing is lost but
the flourish, keep it flat. Usually only the writer loses something.

## What must survive the pass

Voice work does not touch substance. Facts, figures, citations, structure,
headings, call-outs and links come out unchanged. If a rewrite needs a new
claim, that is a revise-stage change and it needs a source.

Two traps specific to this pass:

- **Having a point of view is not a licence for unsupported absolutes.** "Always",
  "never", "the single biggest factor" get pages sent back. Judgement must show
  its basis; practitioner estimates stay labelled as estimates. Where a source
  supports the judgement, quote the source and let it carry the weight. The
  strongest line on the timeline page is the Insolvency Service's own conclusion
  that the process "does not seem to be efficient", not anything invented.
- **Never invent casework.** No fabricated client stories. General practitioner
  observation is fine and earned; a specific anecdote is not. Keep first-person
  inside Company Debt's actual role: an advisory firm that refers to licensed
  practitioners, not the appointed practice.

## Running the pass

One page at a time. Register the page first if it is unknown to the pipeline.

```bash
python scripts/editorial_task_entry.py --page <slug> --task rewrite
```

Take the baseline before touching anything, so you know which failures you
inherited and which you caused:

```bash
python scripts/article_audit.py --slug <slug>
```

Then rewrite, re-gate, and record the voice audit. The gate will not pass
without a current audit record, and any prose change invalidates the last one:

```bash
python scripts/voice_audit.py --slug <slug> --record --by claude-opus-5 --scenes N --bite N --tone pass --rhythm pass --read-aloud pass --verdict pass --notes "..."
```

Write the notes properly. They are the record of what was actually checked, and
"passed voice audit" is worthless six months from now. Name the tells you found
and what replaced them.

**Patch twice, then redraft.** Layered corrections accumulate an AI signature of
their own, and softening an absolute usually deletes the judgement instead of
re-earning it. Past the second pass, rewrite the page from spec rather than
editing the edits. `--redraft-now` on the audit tool marks that honestly.

Then push and verify what landed, via the `staging-push` skill. A 200 response
is not proof.

## Gate constraints to bake in while writing

Do these during the rewrite, not afterwards, or the fixes flatten the voice you
just restored:

- **No em dashes anywhere.** Hard AI signal.
- Keep every `<p>` to 2 or 3 rendered lines, roughly 150-250 characters. The
  gate's 400-character limit is a ceiling, not a target.
- Lead paragraph carries no `<strong>`; the theme bolds it automatically.
- `you` density at or above 8 per 1,000 words; `we/our/us` at or above 5. Reach
  the second through genuine practitioner observation, never padding.
- Gloss every acronym and statutory reference at first mention in prose. Tables
  and headings do not count as an introduction.
- FAQ `panelTitle` attributes need `<` escapes, single backslash. Raw
  `<strong>` renders as visible junk.
- Related Guides must be the final H2, after the FAQ accordion.

## Rolling this out across the site

The corpus has this problem broadly, so work in batches by cluster rather than
alphabetically. Pages in the same cluster share phrasing, and fixing them
together stops the survivors contradicting the rewritten ones.

For each batch:

1. Baseline every page in the cluster first and record the scores. Some pages
   fail checks that predate this work; do not silently inherit the blame.
2. Rewrite one page at a time, all the way through gate, audit record and push,
   before starting the next.
3. Watch for shared claims across the cluster. Voice work surfaces factual
   contradictions between sibling pages surprisingly often. Fix them as you go
   rather than leaving a corrected page arguing with its neighbours.
4. Before starting, check nobody else is working the same cluster:
   `git status` and file modification times. This has collided before.
