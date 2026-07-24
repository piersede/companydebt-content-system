---
name: negative-keyword-miner
description: Mine search-terms.json for negative-keyword candidates on the Company Debt Google Ads account, applying protected-term and existing-negative checks before recommending anything. Use when running the negative-keyword-miner stage of the weekly Google Ads audit, or when asked to find wasted/irrelevant search spend to exclude.
---

# negative-keyword-miner

Finds search terms worth excluding as negative keywords, from a saved snapshot only — never calls the live Google Ads MCP server itself. Read `google-ads-auditor/CLAUDE.md` in full before running this; the rules there (especially "Negative keywords" and "Evidence rules") govern every decision this skill makes and are not repeated in full here.

## Inputs (from one `runs/YYYY-MM-DD-<account-slug>/` snapshot)

- `raw/search-terms.json` — from `queries/search-terms/search-terms.gaql`. The candidate pool.
- `raw/keywords.json` — from `queries/search-terms/keywords.gaql`. Used only to check for existing negative-keyword coverage (`ad_group_criterion.negative == true`) before recommending a duplicate. **Known gap: this only covers ad-group/campaign-level keyword criteria for ENABLED campaigns. Shared negative-keyword lists (`shared_criterion`/`campaign_shared_set`) are not in the current query library and are invisible to this skill — always caveat that existing-negative checking is best-effort, not exhaustive, until a shared-list query exists.**
- `account-config.yml` (the copy saved inside the run folder) — supplies `protected_terms`, `irrelevant_topics`, `brand_terms`, and the relevant `targets` thresholds. Never substitute the live `accounts/*.yml` file instead of the snapshot's own copy — the finding must be reproducible from the run folder alone.

## Algorithm

Process every row in `search-terms.json` in order. For each row:

1. **Skip if already excluded.** If `search_term_view.status == "EXCLUDED"`, the term is already blocked at the search-term level — nothing to recommend.

2. **Protected-term check (hard stop).** Case-insensitive substring match the search term against `protected_terms`. If it matches, do **not** recommend a negative under any circumstances, regardless of performance. This is a hard rule, not a judgement call — do not override it even for a clearly-zero-conversion protected term. Do not emit a finding for these rows at all (they are not a finding; they are correctly-excluded-from-consideration and don't need reporting unless the run has zero other findings, in which case note in caveats that N terms were skipped as protected).

3. **Existing-negative check.** Build a lowercased set of `ad_group_criterion.keyword.text` where `ad_group_criterion.negative == true` from `keywords.json`, scoped to the same campaign where possible (fall back to account-wide if campaign-level match isn't found — over-matching here is safe, it just means fewer redundant recommendations). If the search term already matches an existing negative (exact text match, or the negative is a shorter phrase fully contained in the search term, which is how Google's own negative matching works for broad/phrase negatives), skip — do not re-recommend.

4. **Classify relevance** using `irrelevant_topics` (case-insensitive substring/keyword match against the configured list) and `brand_terms`:
   - **Clearly irrelevant** — the term matches a configured `irrelevant_topics` entry. This is a topical judgement, independent of spend or click volume: even a single low-cost click on a term like "insolvency practitioner jobs" when `irrelevant_topics` includes job-search terms is worth flagging, because the evidence is the term's own meaning, not its performance. → eligible for a finding.
   - **Topically relevant but zero-converting** — the term does *not* match `irrelevant_topics`, but has spend/clicks with zero conversions. **Do not recommend this as a negative.** Per `CLAUDE.md`'s negative-keyword rule, a term is not "waste" solely because it has zero conversions, and per the account's standing low-confidence flag on conversion data (`accounts/company-debt.yml`), a zero-conversion read here is especially weak evidence. This pattern belongs to `ad-performance-diagnostic` or `search-terms-analyzer` (landing page, bidding, or genuine audience-fit questions), not to this skill. Do not emit a negative-keyword finding for these rows.
   - **Below evidence thresholds** — regardless of topic, if `metrics.clicks < targets.minimum_clicks_before_judgement` and the term isn't a clear `irrelevant_topics` match, there usually isn't enough evidence to act on. Low-volume clearly-irrelevant terms can still be flagged (see above) but should be marked `confidence: low` and the low volume stated plainly in `caveats`.

5. **Match type.** Always recommend the narrowest suitable match type for the negative: **EXACT**, matching the literal search term text. Do not recommend broad or phrase negatives from this skill — a broader negative risks blocking legitimate traffic this skill hasn't evidenced, and CLAUDE.md requires recommending the narrowest suitable type.

6. **Blocking-risk assessment** (required field, `blocking_risk: low|medium|high`):
   - `low` — the term shares no words with `brand_terms` or the account's core commercial phrases (e.g. "insolvency", "liquidation", "company debt", "creditors"), and an EXACT negative on this literal string cannot plausibly catch a valuable query.
   - `medium` — the term shares a word with a core commercial phrase but the overall intent still reads as clearly off-target (e.g. contains "debt" but is clearly a jobs-board query).
   - `high` — do not recommend at all if blocking risk would be high; if the topical match is that ambiguous, treat it as insufficient evidence instead (fall through to no finding) rather than emitting a high-risk recommendation.

7. **Aggregate before reporting.** If the same literal search term appears more than once (different ad groups/campaigns), combine into one finding with summed evidence rather than duplicate findings, and list every `campaign`/`ad_group` it appeared under in `evidence`.

## Output

One JSON array of findings, each validated against `schemas/finding.schema.json`:

- `finding_id`: `NEG-001`, `NEG-002`, ... sequential.
- `source_skill`: `"negative-keyword-miner"`.
- `category`: `"irrelevant-topic-negative"`.
- `severity`: scale by cumulative spend on the term — `low` under the account's `zero_conversion_spend_threshold`, `medium` up to 3x that, `high` above.
- `confidence`: `high` if the topic match is unambiguous and volume is meaningful; `low` if volume is thin (state why in `caveats`).
- `blocking_risk`: required, as above.
- `evidence`: raw rows — search term, per-campaign/ad-group breakdown, cost, clicks, conversions, impressions, matched `irrelevant_topics` entry.
- `observation`: factual only — what the data shows, no judgement (e.g. "the search term '...' received N clicks and £X spend across M campaigns in the audit period, with 0 conversions, and matches the configured irrelevant-topic category '...'").
- `interpretation`: kept separate from the observation — why this indicates off-target traffic.
- `recommendation`: the exact negative to add, match type, and level (ad group vs campaign — recommend ad-group level unless the term showed up across every ad group in a campaign, in which case recommend campaign level).
- `estimated_impact`: plain-English, forward-looking only (e.g. "would prevent further spend on this exact query going forward; historical spend already incurred is not recovered by adding a negative"). Never imply the recommendation has been implemented — it hasn't; this skill only reports.
- `effort`: `"low"` (adding a negative keyword is a small manual action).
- `caveats`: always include the shared-negative-list visibility gap from the Inputs section above; add volume/confidence caveats where relevant.

If zero qualifying findings exist in a run (as happened with the live 2026-07-20 snapshot — no `irrelevant_topics` matches in that week's `search-terms.json`), report that explicitly as a clean result, not as a failure: state how many search-term rows were reviewed, how many were skipped as protected, and that none matched the configured irrelevant-topic list. An empty findings list is a valid, sometimes-correct output.

## What this skill must never do

- Never invent a new `irrelevant_topics` entry or protected term mid-run — if a term looks off-target but isn't covered by the configured list, that's a **configuration gap to report**, not a judgement to make unilaterally. Note it in `caveats` on a lower-confidence finding, or in the run's summary, and suggest the account owner review whether `irrelevant_topics` needs extending — don't just add it as a negative anyway.
- Never recommend a `protected_terms` match, even at zero conversions and high spend.
- Never call zero-conversion spend "waste" for a topically relevant term.
- Never claim the negative has been added — this skill produces recommendations only. Adding negatives to the live account is out of scope entirely (see `CLAUDE.md` — "Never make or attempt Google Ads changes").
