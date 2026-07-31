# Stage Pack: Humanise

Runs after `revise`, before `gate` (bernstein.js requires `humanise_complete`
before the gate stage). This is the pass that turns a correct-but-flattened
draft into one that reads as genuinely authored AND clears `article_audit.py`
on the first attempt. If the humanise output needs a round of gate-chasing
afterwards, this pack was not applied fully.

Load alongside: `writer-core.md`, `editorial-os/docs/human-authorship-voice-engine.md`,
`editorial-os/09-voice-governance.md`, `editorial-os/23-prose-quality-gates.md`.

Goal: restore voice, authorship texture, and human markers after structural
revision, without changing structure, claims, or facts, and while landing
inside the mechanical gate.

## Why this pass exists

Structural revision and expert-review corrections flatten prose. Auto-splitting
long paragraphs to satisfy the gate makes it staccato. The result reads
AI-edited: even sentence length, hedged balance, generic openings, tricolons
everywhere. Humanise counters that. It is a voice pass, not a rewrite of what
the article says.

## Part A -- voice restoration (the "what")

- Reintroduce concrete scenes and lived operational friction where they were
  flattened. Humanise through WORKING DETAIL, not chattiness. "sitting in
  someone else's account for eighteen months" beats "which can be frustrating".
- Make evaluative lines earn their place. Cut hedged balance that dilutes the
  point. Say which thing is worse, for whom, and why.
- Restore rhythm: vary sentence length deliberately. Let a short, hard sentence
  land after a longer one. Break the uniform cadence that revision produces.
- Add asymmetrical lines where the prose is too even. Not every sentence needs
  three parallel clauses; kill the reflexive tricolon.
- Watch specifically for a repeated aphorism-label tic: "that/this is the
  [adjective] [noun]" (e.g. "that is the trap", "the blunt backdrop", "the
  quiet mechanism behind X"), and self-announcing honesty ("worth stating
  plainly", "the honest read comes from..."). Either can appear once and be
  fine. The actual tell is REPETITION of the same device across one page --
  invisible if you read any single sentence on its own, obvious once you
  count instances. Caught on the pub-closures page 2026-07-22: the same
  labelling construction appeared five times and passed a sentence-by-sentence
  read. Before marking `humanise_complete`, scan the whole page for repeats of
  the same rhetorical shape, not just for guardrail patterns (em dashes,
  banned openings) or presence/absence of "we"/"you". A page can pass every
  mechanical check and still fail this.
- Recover mild UK texture where natural. Apply moral clarity where the evidence
  supports it.
- Restore earned "you" and "we". Company-authored voice (see 09-voice): the
  team, not the founder. Never invent first-hand testing, screenshots, or
  customer experience.

## Part C -- practitioner voice and persona depth (MANDATORY, the reason pages get sent back)

This is the part most passes under-deliver, and the most common reason a page
that clears the mechanical gate still reads as competent-but-synthetic. Do NOT
treat it as optional polish. A sector or advice page is not done until it reads
as though an experienced Company Debt insolvency practitioner, who has personally
handled these cases, is speaking directly to a specific reader in that trade.

Load alongside: `editorial-os/17-audience-and-persona.md`,
`editorial-os/24-payoff-intent-first.md`, `editorial-os/15-good-vs-bad-examples.md`.

Four things must be present, verifiable by re-reading before the gate:

1. **Concrete scenes (>= 3 per 1,000 words).** A scene is a specific, recognisable
   moment in the reader's actual world, not a category label. "The fuel card
   declined at the pump on a Monday, and by Friday two trucks had not moved"
   beats "cashflow pressure mounts". If the page can be understood without
   picturing a single real moment, it has none, and it fails. One scene per major
   section minimum.

2. **Earned practitioner "we" (the lived-caseload voice).** Company Debt IS an
   insolvency practice, so "in the cases we handle", "by the time a director
   calls us", "the pattern we see", "what catches operators out, in our
   experience" are earned, company-authored operational voice, not founder drift
   (09-voice test still applies: "who is we?" must answer "the Company Debt
   insolvency team"). This voice is REQUIRED, not sprinkled. Use it to open or
   close the driver sections and the distinctive-issue section. It is also how
   the page reaches a natural we/our density near the 5/1k floor -- reached by
   genuine practitioner observation, never by padding.

3. **Warmth from recognition of reader stress (persona connection).** The reader
   is a director under real pressure (see 17-persona: shame, the guarantee on the
   house, the sleepless night, the brown HMRC envelope). Acknowledge that reality
   before or alongside the legal content, at least once near the top and once at
   the decision point. Calm, specific, non-judgemental. Never pep, never
   authority-first credentials over understanding.

4. **Asymmetrical editorial lines (1-3 per page) and tonal modulation.** Include
   at least one line that could only be written by someone who has thought hard
   about this trade and this failure mode -- it compresses the real truth of how
   these businesses go under. And shift tone by section: warning signs firmer,
   options calmer and protective, the distinctive-issue section more precise and
   sceptical. One evenly polished register across the whole page is the AI tell.

The mechanical gate does NOT measure any of this. A 23/25 or 24/25 score with
these four absent is a FAIL for the purpose of this pass. Re-read for all four
before handing to the gate; if any is missing, the pass is not finished.

## Part B -- gate-aware constraints (the "how", so it passes first time)

Bake these in WHILE humanising so the output clears `article_audit.py`:

- **No em dashes anywhere in prose** (hard AI signal). Use commas, colons, full
  stops. Hyphenated compounds (fixed-price, tier-one) are fine.
- **Openings (P1-P3) must not use banned patterns.** No "This page is for/about",
  "In today's", "When it comes to", "Whether you are", rhetorical throat-clearing,
  or a delayed/generic first line. Open on a concrete claim or observation.
- **Keep `you` density high (>= 8/1k)** and reach `we/our/us` through the earned
  practitioner voice in Part C, not padding. The check-04 we-density miss is only
  an acceptable exception when Part C is genuinely satisfied -- i.e. the page is
  already carrying the lived-caseload "we", the concrete scenes, and the persona
  warmth, and still lands a touch under 5/1k. It is NOT a licence to write a thin,
  practitioner-light page and wave the miss through. If the page is under 5/1k
  because the practitioner voice is absent, that is a Part C failure to fix here,
  not an accepted miss. Never pad hollow "we" to chase the number.
- **Write in self-standing sentences, and keep every `<p>` to 2-3 rendered
  lines (roughly 150-250 chars).** This is tighter than the mechanical gate's
  ~400-char/~4-line hard limit -- treat the gate as the absolute ceiling, not
  the target. A page that merely clears 400 chars per paragraph still reads
  as a wall of text and overwhelms the reader; split at sentence boundaries,
  never mid-clause, whenever a paragraph runs past 2-3 lines. This applies
  everywhere on a page, including the hero -- a hero stacking a subtitle,
  scope note, auto-lede and a long hero_note in a row is exactly the failure
  mode to avoid; cut hero_note to one tight 2-3 line paragraph and push any
  supporting detail down into the section that already covers it, rather
  than repeating it at the top.
- Lead paragraph carries no `<strong>`/`<b>` (the theme auto-bolds it).
- Preserve FAQ accordion `panelTitle` escapes: `<` built via chr(92), never
  raw `<strong>` (renders as literal junk) and never double-backslash.

## Sequence (this order matters)

1. Humanise the prose in full, writing for rhythm and voice, ignoring paragraph
   length for the moment.
2. THEN reconcile with the gate: split any `<p>` over 2-3 rendered lines
   (roughly 150-250 chars, and always before ~380 chars) at a sentence
   boundary (never inside a tag or mid-clause). Humanise first, split second --
   never pre-flatten the voice to dodge the splitter.
3. Re-read P1-P3 specifically for banned openings introduced during humanising.

## Definition of done (self-check before handing to gate)

- **Part C is satisfied and re-read for:** >= 3 concrete scenes per 1,000 words
  (one per major section), earned practitioner "we" carrying the driver and
  distinctive sections, persona warmth near the top and at the decision point,
  and 1-3 asymmetrical editorial lines with tone modulated by section. If a
  reader could not tell an experienced practitioner wrote this to them
  specifically, the pass is NOT done, whatever the gate score says.
- Reads as authored: concrete detail, earned judgement, varied cadence, a few
  asymmetrical lines. It would not be mistaken for AI-balanced copy.
- Checked for REPEATED rhetorical devices across the whole page (aphorism
  labels, self-announced honesty, the same contrastive "not X, Y" shape used
  more than 2-3 times) -- not just verified sentence-by-sentence. A pass that
  only checks guardrails and per-sentence voice markers will miss this; it
  has before.
- Facts, claims, structure, headings, callouts, links UNCHANGED from the revised
  draft. Voice only.
- `article_audit.py` passes except, at most, the two documented exceptions:
  we/our density (voice floor) and the soft 3+ H3 advisory. Any OTHER gate fail
  means the pass is not finished -- fix it here, not after.
- No em dashes. No banned openings. No invented experience. No first-person
  founder voice.
