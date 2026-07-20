---
name: search-terms-analyzer
description: Find search terms on the Company Debt Google Ads account that are performing well but aren't yet their own dedicated keyword — genuine targeting opportunities picked up incidentally through broad/phrase matches. Use when running the search-terms-analyzer stage of the weekly Google Ads audit, or when asked to find keyword opportunities from search-term data.
---

# search-terms-analyzer

The mirror image of `negative-keyword-miner`: instead of finding traffic to block, this finds traffic worth deliberately targeting. Read `google-ads-auditor/CLAUDE.md` in full before running this — the "Evidence rules" and "Performance judgement rules" sections govern every decision here and are not repeated in full below.

## Inputs (from one `runs/YYYY-MM-DD-<account-slug>/` snapshot)

- `raw/search-terms.json` — from `queries/search-terms/search-terms.gaql`. The candidate pool (Search campaigns only — PMax exposes category-level insights, not full search terms, so it's out of scope here, same as for `negative-keyword-miner`). **Widened 2026-07-20, per Piers:** this now spans `comparison_periods.search_term_lookback_days` (365 days by default), not the 7-day audit window every other raw file uses — a single week was too thin a sample for keyword-level judgement on this low-volume account. The run manifest's `lookback_start`/`lookback_end` (not `audit_start`/`audit_end`) give the actual period this data covers — use those for the `period` field in every finding.
- `raw/keywords.json` — from `queries/search-terms/keywords.gaql`. Used to check whether a search term is already its own dedicated keyword (in which case there's no opportunity — it's already targeted).
- `account-config.yml` (the copy saved inside the run folder) — supplies `irrelevant_topics`, `brand_terms`, and the relevant `targets` thresholds. **Use `targets.search_term_minimum_clicks` (624 by default = 12/week × 52 weeks), not `targets.minimum_clicks_before_judgement` (12), for the evidence tiering below** — the latter was calibrated for the 7-day campaign-level window and is meaningless applied to a year's worth of search-term data.

**Known data-model gap: no finer-grained trend view within the lookback window.** Even at 365 days, `search-terms.gaql` returns one aggregate row per term for the whole window — there's no day-by-day or month-by-month breakdown at search-term level the way `daily-performance.gaql` gives campaign-level trend context. A term with 3 conversions could be steadily growing or could have had all 3 in one week eight months ago — this data can't distinguish those. Always state this plainly rather than implying more confidence than the data supports — this is exactly the kind of "record missing data instead of inventing it" situation `CLAUDE.md` requires.

## Algorithm

Process every row in `search-terms.json`. For each row:

1. **Skip if already excluded.** `search_term_view.status == "EXCLUDED"` — nothing to target, it's blocked.

2. **Skip if already its own keyword.** Case-insensitive match the search term text against `ad_group_criterion.keyword.text` in `keywords.json` for non-negative, `ENABLED` criteria in the same campaign. If it's already a dedicated keyword (any match type), there's no targeting opportunity — the account is already capturing this deliberately, not incidentally.

3. **Skip if it matches `irrelevant_topics`.** That's `negative-keyword-miner`'s finding, not this skill's — don't duplicate it as an "opportunity." (This also means the two skills' outputs are disjoint by construction: a term is never simultaneously a negative-keyword finding and a search-terms-analyzer finding.)

4. **Tier the remaining evidence** using `targets.search_term_minimum_clicks` (624 by default — see Inputs above, do not use `minimum_clicks_before_judgement` here) and the account's standing conversion-data caveat (`accounts/company-debt.yml` — only phone/email/chat conversions are trusted, and volume has been scant):
   - **Recommend** — `metrics.clicks >= search_term_minimum_clicks` AND `metrics.conversions > 0`. This is real, actionable evidence: enough volume across the full lookback window to not be noise, plus at least one trusted-category signal. `confidence: high`.
   - **Watch, don't recommend yet** — below the click threshold but `metrics.conversions > 0`. A conversion below the yearly volume bar is exactly the kind of thin signal the account's conversion-data caveat warns about, and there's no finer-grained history to check it against (see the data-model gap above). Emit a finding, but the `recommendation` field must say "monitor for another period before adding as a keyword" — not "add now." `severity: low`, `confidence: low`. **On this account specifically, expect most or all findings to land here** — it's genuinely too low-volume for any single search term to clear a properly-scaled yearly bar, and that itself is worth reporting rather than hiding.
   - **No finding** — zero conversions, regardless of click volume. Per the standing rule that a term is not "waste" or an "opportunity" based on volume alone without a conversion signal, and per the account's low trust in conversion data generally, clicks alone (no conversion) aren't enough evidence in either direction at the search-term level.

5. **Compare against the triggering keyword.** For context (not as a pass/fail gate), record which keyword/match-type triggered the impression (`segments.keyword.info.text`, `segments.keyword.info.match_type`) in the evidence. A BROAD or PHRASE match triggering a strong-performing, topically on-target search term is the clearest case for "this deserves its own keyword" — note that explicitly in the interpretation when it applies.

6. **Match type and level.** Recommend the narrowest suitable match type for the new keyword — normally **EXACT**, so it can be bid and tracked independently of the broader keyword that incidentally triggered it. Recommend ad-group level, in the same ad group the search term already appeared under.

7. **Brand vs non-brand.** If the search term matches `brand_terms`, say so explicitly in the finding — per `CLAUDE.md`, brand and non-brand performance must never be compared or presented without noting the distinction, since brand terms typically convert very differently.

## Output

One JSON array of findings, validated against `schemas/finding.schema.json`:

- `finding_id`: `OPP-001`, `OPP-002`, ... sequential.
- `source_skill`: `"search-terms-analyzer"`.
- `category`: `"untargeted-opportunity"`.
- `severity`/`confidence`: per the tiering above.
- `evidence`: search term, triggering keyword + match type, cost, clicks, conversions, impressions, whether it's a brand term.
- `observation`: factual only (e.g. "the search term '...' received N clicks and £X spend via the {match type} keyword '...', with M conversions").
- `interpretation`: kept separate — why this indicates an untapped opportunity (or, for watch-tier, why it's too early to say).
- `recommendation`: exact new keyword text, match type, and ad group — or, for watch-tier, an explicit "monitor, don't add yet" instruction.
- `estimated_impact`: plain-English and forward-looking only — dedicated-keyword targeting typically gives better bid control and Quality Score signal than incidental broad/phrase matches, but never invent a specific £ uplift figure that isn't in the evidence.
- `effort`: `"low"`.
- `caveats`: always include the no-context-window-at-search-term-level gap; add the account's conversion-data trust caveat for any finding resting on a conversion signal (which is all of them, by construction — this skill only fires on conversions).

If zero qualifying findings exist, report that explicitly — including how many rows were reviewed and how many fell into each skip category (already-targeted, irrelevant-topic, zero-conversion). An empty findings list is a valid, sometimes-correct output, same as for `negative-keyword-miner`.

## What this skill must never do

- Never recommend a term already covered by `negative-keyword-miner`'s territory (`irrelevant_topics` matches) as an opportunity — the two skills' scopes are disjoint by construction (step 3).
- Never treat a single low-volume conversion as confident evidence — route it to "watch," not "recommend."
- Never invent a context window this data doesn't have — state the gap instead of implying an opinion about trend/history at search-term level.
- Never claim the keyword has been added — this skill produces recommendations only, same restriction as `negative-keyword-miner` (see `CLAUDE.md` — "Never make or attempt Google Ads changes").
