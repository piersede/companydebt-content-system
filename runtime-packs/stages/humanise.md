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

1. **Concrete detail where it earns its place. No quota.** This rule previously
   demanded three scenes per 1,000 words and one per major section. That was
   wrong and it caused active harm: on a 3,000-word page it mandates ten
   scenes, no page holds ten genuine ones, and the pass invents the shortfall.
   Fabricated colour (the loan from a father-in-law, the midnight search, the
   bank ringing the home phone) is what makes a page read as over-humanised,
   and it is an evidence problem as well as a voice one.

   The test is not how many, it is where the detail comes from. Specificity
   reads as human only when it arises from knowledge. Ask of each one: does
   this reveal something a practitioner knows, or does it merely show that the
   writer can write? Keep the first. Cut the second, however good it sounds.

   Prefer practitioner knowledge to invented scenes every time. Not "the bank
   which financed the fit-out starts ringing the home phone", but "personal
   guarantees sit outside the liquidation, so once the company cannot meet the
   guaranteed debt the lender can pursue the director personally, which is why
   we ask about guarantees at the first conversation rather than later".

2. **Earned practitioner "we" (the lived-caseload voice).** Company Debt IS an
   insolvency practice, so "in the cases we handle", "by the time a director
   calls us", "the pattern we see", "what catches operators out, in our
   experience" are earned, company-authored operational voice, not founder drift
   (09-voice test still applies: "who is we?" must answer "the Company Debt
   insolvency team"). This voice is REQUIRED, not sprinkled. Use it to open or
   close the driver sections and the distinctive-issue section. It is also how
   the page reaches a natural we/our density near the 5/1k floor -- reached by
   genuine practitioner observation, never by padding.

3. **Warmth shown by removing the problem, never by describing the feeling.**
   The reader is a director under real pressure (see 17-persona: shame, the
   guarantee on the house, the brown HMRC envelope). That is context for YOU.
   It is not material to write back at them.

   **Rewritten 2026-08-13.** This item previously said "acknowledge that
   reality... at least once near the top and once at the decision point". That
   instruction produced exactly the failure it was meant to prevent. On
   company-ccj-mortgage-lender-criteria it generated "If you are reading this
   late, with an application already moving and a letter on the desk you did
   not want" -- an invented evening, an invented letter and an invented mood,
   none of which the page could know. A reviewer cut all of it.

   You do not know the time of day, what is on the reader's desk, whether they
   have slept, or what they are afraid of. Asserting any of it is fabrication
   wearing empathy's clothes, and it is indistinguishable from the same
   sentence on a divorce or medical page.

   Demonstrate understanding instead, by naming what they are actually trying
   to find out and answering it early. On this page the useful move was not
   "we know this is frightening" but telling the reader the judgment does not
   reach their personal credit file, and then that a lender may still ask.
   Prevention beats sympathy: "establish whether the lender asks before you
   apply" does more for a worried director than any sentence about worry.

   Test: could this sentence appear unchanged on a page about a different
   crisis entirely? If yes, it is filler. Cut it.

   **The strongest single warmth mechanism is proportion, added 2026-08-18.**
   Give the SIZE of a risk, never just its existence. A page that names three
   routes to personal liability and quantifies none of them reads as
   frightening even when every word is true, because the gap is where a
   worried reader's imagination goes to work. State the exposure, then its
   limits, in the same passage: most conduct reports lead to nothing further;
   the liquidator has to prove both limbs, so wrongful trading claims are not
   routine; a few deadlines can be extended if you ask before they expire.
   This is more reassuring than any softer adjective, and unlike sympathy it
   is information. A stranger read of the liquidation-deadlines page named
   this as the reason the page still felt like it was ratcheting up threat
   after the dramatic sentences had already been removed.

4. **Asymmetrical editorial lines (1-3 per page) and tonal modulation.** Include
   at least one line that could only be written by someone who has thought hard
   about this trade and this failure mode -- it compresses the real truth of how
   these businesses go under. And shift tone by section: warning signs firmer,
   options calmer and protective, the distinctive-issue section more precise and
   sceptical. One evenly polished register across the whole page is the AI tell.

The mechanical gate does NOT measure any of this. A 23/25 or 24/25 score with
these four absent is a FAIL for the purpose of this pass. Re-read for all four
before handing to the gate; if any is missing, the pass is not finished.

## Part D -- Which?-style editorial voice (the register, MANDATORY)

Parts A and C say what markers must be present. This part says what the page
should SOUND like. Write as an experienced British consumer journalist, not a
content writer. The reader should feel there is a knowledgeable person behind
every sentence who has examined the subject, noticed things, questioned claims
and reached a view.

### The governing rule: human through insight, not decoration

Read this before the eight points below, because it overrides all of them.
Every one of the eight can be satisfied by decoration, and decoration is the
failure this rule exists to stop.

**Do not confuse "human" with conversational or emotional writing.** Before
writing a paragraph, identify the specific observation an experienced
practitioner would make that a generic writer would miss. Build the paragraph
around that observation. If there isn't one, the paragraph is padding, and no
amount of rhythm or warmth will fix it.

**Ban the surface techniques that read as trying to sound human:**

- manufactured hooks: "Ask X and you'll hear...", "There are two kinds of...",
  provocative opener followed by a neat reveal
- neat reversals and clever final clauses: "and nobody tells you which one you
  asked", "not a participant, a witness"
- dramatic one-line paragraphs used for effect rather than to carry a fact
- borrowed empathy: "the thing keeping you awake at night", "we know this is
  stressful". Generic emotional phrasing that would sit unchanged on a debt,
  legal, medical or divorce page is not warmth, it is filler
- the pattern provocative statement, then neat explanation, then clever closer.
  This is the single most recognisable AI paragraph shape

**An expert usually writes more plainly, because the interesting thing is what
they know.** Prefer "There are actually two different timelines here" over "You
may hear anything from ten days to five years, and both answers are right." The
first sounds like somebody explaining something. The second sounds like somebody
writing content.

**Do not add empathy. Demonstrate understanding instead**, by identifying what
the reader is actually trying to find out. On the liquidation timing page the
useful observation is not that directors are worried. It is that when a director
asks how long liquidation takes, they usually mean "when am I no longer
responsible for dealing with this?", while every published duration figure
describes the much longer legal process. Naming that is more empathetic than any
sentence about lying awake.

**The test.** Every few paragraphs the reader should think: that is exactly what
I was actually wondering. Remove any clever phrasing that does not add
knowledge. If a sentence would survive being rewritten flatly, rewrite it
flatly and see whether anything was lost. Usually only the writer loses
something.

1. **Have a point of view.** Do not present advantages and disadvantages
   symmetrically. Assess them. Say what matters, what does not, what is poor
   value, what is unusually good, what is misleading, and what you would
   choose. Be willing to say "avoid", "poor", "rip-off" or "marketing hype"
   where the evidence justifies it. Expertise is judgement, not endless
   qualification.

2. **Turn facts into consequences.** Never leave a figure, fee, feature or rule
   hanging. The pattern is fact, then interpretation, then practical
   consequence: what the reader will pay, notice, gain, lose, have to do, or
   regret. The purpose of the information matters more than displaying it.

3. **Concrete detail beats abstract adjectives.** Ban "excellent
   functionality", "competitive pricing", "robust features", "good customer
   experience". Describe the actual thing. Specific detail is what makes a
   writer look like they met the real world rather than synthesised other web
   pages.

4. **Show the work.** Authority comes from visible effort: we checked, we
   compared, we calculated, we found, we asked. Never manufacture first-hand
   experience, but where genuine research or analysis has been done, expose
   some of the process. "We" must mean an organisation doing something, not a
   corporate pronoun.

5. **Speak directly to the reader.** Use "you" freely. Do not describe an
   abstract "consumer" when you can say what this reader pays or what happens
   when their circumstances change. Second person turns information into
   advice.

6. **Allow small signs of personality.** Natural British expressions where they
   genuinely fit: eye-watering, whittle down, stung, bide your time. Occasional
   "sadly", "unsurprisingly", or a short rhetorical question showing the
   writer's reaction. Do not sprinkle idioms mechanically. One precise,
   slightly colloquial phrase beats paragraphs of forced chumminess.

7. **Warm towards the reader, sceptical towards the market.** A knowledgeable,
   sceptical friend on the reader's side: understanding their confusion, cost
   and risk, while interrogating provider claims, marketing language and
   inconvenient terms. Evidence-led scepticism, not cynicism.

8. **Do not polish away the texture.** Mix short conclusions with longer
   explanatory sentences. Ask the occasional obvious question. Make a judgement
   and then explain it. Avoid mechanically balanced paragraphs, repetitive
   sentence structures, compulsory three-item lists, constant
   however/furthermore/additionally, and summaries that repeat what was just
   said.

The failure mode this part exists to prevent: trying to "sound human" by
becoming chatty. This voice sounds human because somebody appears to have done
the work, understood the reader's problem, and formed an opinion. Institutional
evidence gives the writing authority; personal judgement gives it life.

Note the interaction with the evidence rules. A point of view is not a licence
for unsupported absolutes. "Avoid" and "poor value" must be earned by the
evidence on the page, and a practitioner judgement must still be labelled as
one. Judgement with its basis shown is the target; judgement asserted flatly is
the thing reviewers send back.

## Part E -- the sentence classification (MANDATORY, run last)

Added 2026-08-13 after four failed humanise passes on one page. Parts A, C and
D describe what good looks like. This part is the mechanical way to find what
is wrong, and it is the fastest of the lot. Do it as a separate pass with the
draft in front of you, not from memory.

Classify every substantive sentence:

| Code | Meaning |
|------|---------|
| **F** | **Fact.** Directly supported by the research or the cited source. |
| **D** | **Derived insight.** Follows logically from two or more facts on the page. |
| **E** | **Established experience.** Genuine Company Debt practitioner knowledge that could be defended if challenged. |
| **J** | **Editorial judgement.** A reasoned conclusion with its basis visible in the sentence. |
| **P** | **Performance.** Anecdote, drama, assumed emotion, clever line or invented scenario, present mainly to make the page feel human. |

Keep F, D, E and carefully-used J. **Cut most P.**

D is where the value usually sits and it is the class most often missing.
"Two of the three sit inside the same banking group, so the sample contains two
independently established approaches rather than three" is D: nobody told us
that, it fell out of the comparison. A page rich in F and thin in D is a data
dump. A page rich in P is a performance.

### The four questions that produce the classification

Ask them section by section, not sentence by sentence, or you will polish
individual lines and miss the shape:

1. **What did the research actually establish?** Write that first.
2. **What is the non-obvious distinction?** This is nearly always where the
   human value is.
3. **What practical consequence follows?** What to check, disclose, compare or
   ask.
4. **Is anything here only because it sounds vivid?** Delete it.

### Specific P-class failures, with the fix

- **Inventing the reader's circumstances.** Their evening, their desk, their
  mood, the time on their phone. You do not know any of it. Fix: answer the
  question earlier instead.
- **Turning plausible experience into fact.** "Rarely sinks an application",
  "plenty of directors", "most directors get this wrong". Unless it is F, D, E
  or labelled J, remove it. Sounding like experience is not having it.
- **Mind-reading the subject.** "Lenders evidently accept that...", "the rule
  is aimed at...". Published criteria show WHAT, not WHY. Fix: compare two
  criteria and state the difference, which is stronger anyway.
- **Manufacturing stakes in headings.** "The One Lender That Can Stop You" is a
  content headline. "Barclays Has a Specific Company-CCJ Decline Rule" is an
  expert one. Let the facts carry the urgency.
- **Landing every paragraph.** Fact, then dramatic interpretation, then
  quotable closer. Each one works alone; stacked, they are the clearest
  signature of prose written to sound authored. Let most sections end quietly
  when the explanation is finished.

### Keep the domain boundary visible

Where the page speaks on insolvency -- winding-up petitions, personal
guarantees, what happens when a company cannot satisfy a judgment -- Company
Debt has practitioner authority and should use it. Where it speaks on another
trade's territory -- whether a mortgage will be approved, how an underwriter
will behave, what a lender will accept -- ground the statement in the published
criteria or send the reader to their broker. Holding that line makes the page
sound more expert, not less.

### The standard

Do not aim for the reader thinking "this writer understands how stressful this
is". Aim for: **"they have actually checked this, they noticed the distinction I
was missing, and now I know what to ask."**

The research creates the personality. The writer does not add one on top.

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

## Stranger-read step (mandatory from pass 3 onward)

Before recording the voice audit on pass 3 or later, run an outside-eye check
on the opening. The writer cannot see clever prose after several iterations;
a fresh reader can. Two commands:

    python scripts/stranger_read.py --slug <slug>

This prints a persona-anchored prompt and writes a template file. Paste the
prompt into a fresh agent (a new Agent tool call is fine; make sure it has
not been in the drafting session). Take the agent's response verbatim and
paste it into the template file under the `---` separator. Then:

    python scripts/stranger_read.py --fill editorial-os/stranger-reads/<file>.md

That validates the response (rejects empty stubs, requires at least two of the
five numbered answers). Finally, reference the report in the audit record:

    python scripts/voice_audit.py --slug <slug> --record ... \
        --stranger-read-report editorial-os/stranger-reads/<file>.md

If the stranger-read report flags a term the reader had to look up or a point
where they would have closed the tab, fix the prose before recording the audit
with a `pass` verdict. Do not record the audit with `pass` and known unresolved
issues in the stranger-read report; that defeats the check.

## Definition of done (self-check before handing to gate)

- **Part D is satisfied:** the page takes a view rather than balancing
  symmetrically; every figure carries its consequence for the reader; the
  detail is concrete; the research is visible; the texture is uneven in the way
  human prose is. If a reader could not tell what the writer thinks, the pass
  is not done.
- **Part D's governing rule is satisfied, checked separately and last.** Re-read
  every paragraph asking: what does this know that a generic writer would not?
  Then hunt the specific tells: manufactured hooks, neat reversals, clever
  final clauses, dramatic one-line paragraphs, borrowed empathy. A page can
  satisfy all eight Part D points and still fail here, and this is the failure
  reviewers actually notice. Imitating human prose is the error; imitating
  human thought is the target.
- **Part C is satisfied and re-read for:** concrete detail that comes from
  knowledge rather than invention (no quota -- see Part C item 1, and do not
  reinstate one), earned practitioner "we" carrying the driver and distinctive
  sections, understanding shown by answering the reader's real question rather
  than by describing their feelings, and 1-3 asymmetrical editorial lines with
  tone modulated by section. If a reader could not tell an experienced
  practitioner wrote this to them specifically, the pass is NOT done, whatever
  the gate score says.

  This bullet demanded ">= 3 concrete scenes per 1,000 words (one per major
  section)" until 2026-08-13, contradicting Part C item 1 on the same page,
  which had already removed the quota as actively harmful. On a 3,000-word
  page the quota demands nine scenes, no page holds nine genuine ones, and the
  pass invents the shortfall. Both halves of the contradiction now agree: the
  test is where the detail comes from, never how much of it there is.
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
