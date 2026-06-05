# Answer-Engine Coverage Audit — Automation Spec

Goal: turn the audit from a mostly-manual, full-day process into a one-command
run a human reviews. Automate the mechanical half (capture, verify); keep the
judgement half (worth-it, voice, info-gain, apply-to-live) human.

See operational learning: `editorial-os/25-operational-learning-loop.md` (2026-06-05).

## Current state (pilot)

| Stage | Status |
|---|---|
| Capture (OpenAI + Gemini, provenance, immutable runs) | **Automated** (`capture` CLI) |
| Consolidate witnesses + our page | **Automated** (`corpus.py`) |
| Extract delta (nuggets we lack) | **Automated** (`extract.py` + `extract` CLI) — Gemini flash delta pass; already-covered guard checks page prose AND built JSON-LD |
| Verify each claim vs primary source | **Automated** (`verify.py` + `verify_cache.py`, `verify` CLI): cache-first, grounded against the provider's own domain, `--max-live` budget cap, human-check queue for the rest |
| Ledger schema (extract->verify->recommend) | **Built** — `ledger.py` (typed Nugget, JSONL/CSV) — single data contract across all stages |
| Recommend edits + display-format tag | **Automated** (`recommend.py` + `recommend` CLI): publishable nuggets -> render-aware edits via `RECOMMEND_EDITS` + `display_formats`; unverified quarantined; em-dash-scrubbed |
| Orchestration (capture -> ... -> recommend) | **Automated** (`audit` CLI): `--skip-capture` / `--incremental` TTL reuse, `--max-verifications` per-run budget; STOPS at the report, never edits a page |
| Apply to config + build + patch | Manual (human-reviewed) — **keep human** |

## Target CLI

```
python -m scripts.answer_engine_audit audit --page <slug>     # full pipeline -> reports
                                     capture  --page <slug>     # (exists)
                                     extract  --page <slug>     # witnesses -> nuggets-we-lack
                                     verify   --page <slug>     # nuggets -> verified ledger (+cache)
                                     recommend --page <slug>    # verified -> 06-recommended-edits.md
                                     report   --page <slug>     # regenerate reports from processed data
```

`audit` runs extract -> verify -> recommend and stops, emitting
`reports/06-recommended-edits.md` for human review. It never edits the page.

## Stage designs

### Auto-derive inputs from the page config
Remove the hand-passed flags. From `PAGE_CONFIG`:
- keyword: title head (already in `core.derive_keyword`).
- providers: from `card_ids` -> card JSON `short_name`/`bank`.
- sub-intent queries: from each card's `fit_label` / the "best for" sections, plus `priority_questions` if present.
- diff target ("our page"): build the page (or fetch the live URL) and run `corpus.consolidate_our_page`.

### Extract (delta)
- Single constrained model pass (cheaper model, e.g. Gemini flash) over `witnesses.md` + `our-page.txt` + the page's JSON-LD, emitting structured nuggets (schema in `display_formats`/ledger).
- **Already-covered guard:** check each candidate against body text AND JSON-LD, not just visible prose (prevents the Amex-29.1% false positive).

### Verify (the bottleneck — invest here)
- Group claims by provider; one verification pass per provider.
- **Verification cache** (`processed/verification/_cache.json` or SQLite, keyed by `(provider, normalised_claim)` -> `{verdict, verified_url, quote, verify_date}`). Skip re-verification if `verify_date` within TTL and the stored value is unchanged. Ties into the existing rates-verification / citation `verify_date` mechanism — do not build a parallel truth store.
- **Robust fetch:** try direct fetch -> headless (Playwright) on 403/JS -> Gemini-grounded lookup as a last resort. Record which tier confirmed it.
- **Human-check queue:** anything still unverifiable (or contradicted) goes to `04-provider-verification-needed.csv` with a ready-to-paste browser prompt. It must NOT block the run.

### Recommend
- Uses `prompts.RECOMMEND_EDITS` + `display_formats.py`: each verified nugget gets `recommended_display_format`, `recommended_action`, `priority`. Render-aware by construction.

## Cost & cadence controls
- Per-run token budget; `--engines` toggle; `--incremental` (re-capture only if last run older than TTL).
- Cheaper models for capture/extract; reserve Opus for final judgement + drafting (done by the human/main loop, not the tool).
- Cadence: schedule high-value commercial pages (quarterly or triggered), reusing the citation-refresh scheduler pattern and the Monday board.
- **Batch, never all-at-once.** `audit` is single-page by design. When sweeping
  many pages, run them in small batches (a handful at a time), not the whole
  site in one go: it keeps the shared verification cache warming usefully
  between runs, respects provider/API rate limits, and keeps each run's cost and
  failure surface reviewable. The `--max-verifications` budget caps live grounded
  calls per run as a backstop.

## Close the loop (proof)
- On the next run, re-capture and check whether facts we added now appear in engine answers **with our citation**. Track alongside GSC / AI-referral signals. A simple "adopted by engines?" flag per nugget.

## Presentation-doc coverage (llm_friendly_content_presentation.md)
Where each rule from the presentation doc is enforced:

**In the audit recommend layer (automatic on every run):**
- The 13 `recommended_display_format` values + the `comparison_table_column`
  alias (-> `terms_table_column`) and other aliases (`display_formats.py`).
- Compound placements: a fact can be recommended into TWO homes (e.g. table
  column + provider-card field) via `split_formats`.
- "Classify each detail by best display format" + "smallest useful edit"
  (`RECOMMEND_EDITS`).
- Citation-ready fact pattern: commercial nuggets carry `source_required` +
  `last_checked_required`; the report prints a "Must show: Details last checked +
  primary source" line for them. `editorial_note` carries a one-line steer
  (e.g. label charge vs credit).

**In the page builder (enforced on every build, `presentation_checks.py`):**
- Visible last-checked / verification date on commercial pages (FAIL; measured
  0/197 existing pages affected).
- Stable `id="card-<slug>"` anchors on roundup provider cards (FAIL; 0/18).

**Stays human (editorial judgement, NOT mechanically enforced):**
- Consistent entity naming, charge-vs-credit labelling, "facts in blocks not
  prose", structured-data-matches-visible-content, the full Acceptance Checklist.
  These are surfaced in the doc and in `editorial_note` steers, but a human
  applies them.

## Explicitly NOT automated (quality gates)
- Drafting / voice and apply-to-live stay human-reviewed: Bernstein `patch --humanise-note`, staging-only, never production. The tool's output is verified recommendations, not page edits.

## Engine roles (why Gemini is the hard dependency, OpenAI is not optional for discovery)
Two distinct jobs:
- **Capture (discovery):** BOTH engines matter and are NOT redundant. ChatGPT and
  Gemini retrieve from different indexes (Bing-ish vs Google), rank differently,
  and cite different sources, so each surfaces nuggets and competitor citations
  the other misses. The AEO/GEO goal is to not be out-cited on EITHER engine, so a
  proper run uses `--engines openai,gemini` (the default). Gemini-only is a
  degraded fallback for someone with no OpenAI key, not the recommended mode.
- **Processing (extract / verify / recommend):** wired to Gemini ONLY, by choice.
  Verify needs grounded search constrained to a provider domain, and Gemini's
  `google_search` grounding is the transport already in the codebase; extract and
  recommend are pure reasoning where one cheap capable model (flash) suffices.
  Hence "Gemini required to run at all"; this is an implementation fact, not a
  judgement that OpenAI's discovery is weaker.

## Build order (milestones)
1. [done] `verify` + verification cache + human-check queue (the bottleneck). Added `--max-live` budget cap.
2. [done] `extract` with already-covered guard (page prose + built JSON-LD) + auto-derived inputs.
3. [done] `recommend` wired to `display_formats` + `RECOMMEND_EDITS`; em-dash scrub on all rendered text.
4. [done] `audit` orchestration + `--incremental` / `--max-verifications` controls.
5. [todo] Cadence/scheduling + close-the-loop measurement (adopted-by-engines flag).
6. [todo] **Second-source verification.** Add an OpenAI-grounded verifier as an
   independent second voice for contested commercial figures; agree only when
   both grounded lookups concur, else push to the human queue. Directly mitigates
   the geo-mismatch limitation below (the Amex US/UK FX case would have split).

## Known limitations (carry into next session)
- **Geo-mismatched grounded verification.** The grounded verify tier can confirm a
  claim against the provider's official site for the WRONG region. On the
  best-business-credit-cards run it returned "verified" for "Amex Platinum has no
  FX fee" (true for the US card, false for UK Platinum at 2.99%) from a US page.
  The human review gate catches it (recommendations are proposals, not edits), but
  the `verify.py` prompt should pin the UK product/domain harder before this is
  trusted unsupervised. This is the same false nugget the manual run flagged.
- **Gemini `gemini-2.5-flash` 503s on large-context calls.** The extract delta
  packs ~300KB (witnesses + page + JSON-LD); under load the model returns 503
  "high demand" and the SDK retries internally for a long time. `extract.py` adds
  bounded backoff, but a run can still stall. Batch pages, retry off-peak.
- **Run/config time-skew.** Extract reads the run's frozen `our-page.txt` (capture
  time) but builds JSON-LD from the CURRENT config. After the manual run's fixes
  were applied to the config, a re-extract correctly SUPPRESSED the now-covered
  facts (iwoca, Premium Plus core, Amex 29.1%) via the guard, proving it works, but
  it means a re-run will not reproduce a stale nugget list verbatim. Expected.
