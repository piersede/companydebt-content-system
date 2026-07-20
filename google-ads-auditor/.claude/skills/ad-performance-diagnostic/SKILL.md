---
name: ad-performance-diagnostic
description: Diagnose account-structure and delivery problems on the Company Debt Google Ads account — campaigns that can't spend at all, budgets accidentally shared across many campaigns, and campaigns genuinely constrained by budget or rank. Use when running the ad-performance-diagnostic stage of the weekly Google Ads audit, or when asked why a campaign isn't spending or delivering.
---

# ad-performance-diagnostic

Read `google-ads-auditor/CLAUDE.md` in full before running this — the "Performance judgement rules" section (especially "never recommend budget movement without checking available scale") governs every decision here and is not repeated in full below.

Unlike `negative-keyword-miner` and `search-terms-analyzer` (which mine search-term-level data), this skill works at **account-structure level**: it explains why campaigns aren't delivering, before any keyword- or ad-level optimisation can matter. A campaign losing budget/rank impression share, or one that literally cannot spend, makes every other finding about it moot.

## Inputs (from one `runs/YYYY-MM-DD-<account-slug>/` snapshot)

- `raw/campaigns.json` — from `queries/account-baseline/campaign-performance.gaql`. Used to find which campaigns are `ENABLED` and what they actually spent/converted in the 7-day audit window.
- `raw/account-baseline.json` — from `queries/account-baseline/budget-and-bidding.gaql`. Point-in-time budget/bidding config, no date filter — includes `campaign_budget.id`, `campaign_budget.amount_micros`, `campaign.bidding_strategy_type`, target CPA.
- `raw/impression-share.json` — from `queries/diagnostics/impression-share.gaql`. Search campaigns only, 7-day audit window. `metrics.search_impression_share`, `metrics.search_budget_lost_impression_share`, `metrics.search_rank_lost_impression_share`.
- `account-config.yml` (the copy saved inside the run folder) — supplies `targets.zero_conversion_spend_threshold` and other thresholds.

All three checks below use the 7-day `audit_start`/`audit_end` window (via `campaigns.json`/`impression-share.json`), not the search-term lookback window `negative-keyword-miner`/`search-terms-analyzer` use — this skill works at campaign level, where the 7-day window is the account's own primary comparison period.

## Checks

### 1. Zero-delivery `ENABLED` campaigns (`category: dormant-campaign`)

For every campaign where `campaign.status == "ENABLED"`, join `account-baseline.json` (has it got a budget above zero?) against `impression-share.json` (did it actually show, this period?).

Flag a campaign if:
- `campaign_budget.amount_micros > 0` (it has *some* budget — a genuinely £0 budget is a different, more obvious problem, not really a "diagnosis"), AND
- `metrics.search_impression_share == 0` for the whole audit period (Search campaigns only — PMax doesn't report this metric the same way and is out of scope here, same reasoning as the other two skills).

**Do not guess the root cause.** This skill has evidence for exactly three possible explanations and must check all three before writing the `interpretation`, stating plainly whichever apply and leaving the rest as open questions rather than invented certainty:
1. **Budget effectively zero or shared into oblivion** — check `campaign_budget.id` against every other `ENABLED` campaign's budget ID (see Check 2). If it's part of a shared-budget cluster, or the amount itself rounds to near-zero (e.g. under £1/day), say so as the likely explanation.
2. **Ads not running** — cross-reference `raw/ads.json` (if present in the snapshot) for `ad_group_ad.status`. If every ad in the campaign is `PAUSED` or `REMOVED`, say so. If `ENABLED` ads exist (even with `PENDING`/`UNSPECIFIED` strength), this explanation doesn't apply — say that explicitly rather than staying silent.
3. **Keywords not running** — cross-reference `raw/keywords.json` for the campaign. If every keyword is `PAUSED`/negative, say so. If `ENABLED` non-negative keywords exist, this doesn't apply — state that too.

If none of the three explanations are evidenced, say so plainly: "budget, ads, and keywords all appear active for this campaign, but it shows zero delivery — the cause isn't visible in this data (could be ad schedule, geo/language targeting, policy/billing hold, or campaign start/end dates, none of which the current query library captures)." This is exactly the kind of "record missing data instead of inventing it" situation `CLAUDE.md` requires — do not guess between these.

### 2. Shared campaign budgets (`category: shared-budget-cluster`)

Group every `ENABLED` campaign's `account-baseline.json` row by `campaign_budget.id`. Any `campaign_budget.id` used by more than one `ENABLED` campaign is a finding, regardless of the `campaign_budget.explicitly_shared` flag's value (real accounts can have campaigns sharing a budget ID without that flag reading `true` — treat the shared ID itself as the evidence, not the flag).

This is not automatically "wrong" — deliberately shared budgets are a legitimate strategy — but it's always worth surfacing, especially when combined with Check 1 (zero delivery for most of the cluster) or when the shared amount is small relative to the number of campaigns drawing on it.

### 3. Budget/rank-constrained active campaigns (`category: impression-share-constraint`)

For every `ENABLED` Search campaign with `metrics.search_impression_share > 0` (i.e. genuinely delivering, not caught by Check 1):

- If `metrics.search_budget_lost_impression_share` is large (no fixed number in this account's config yet — use judgement and state the raw percentage; a good rule of thumb is that anything losing more impression share to budget than it's currently winning is worth flagging) **and** the campaign is converting at a plausible cost (cross-reference `campaigns.json` — don't call a campaign "worth more budget" if it's also showing signs of poor conversion efficiency; per `CLAUDE.md`, never recommend budget movement without checking available scale), note this as a genuine budget-constrained scale opportunity. Frame the recommendation as "worth testing a higher budget" — never a specific number, this skill has no evidence for what the right new budget would be.
- If `metrics.search_rank_lost_impression_share` dominates over budget loss, say explicitly that a budget increase alone won't help — the constraint is bid/Quality Score/ad relevance, a different problem this skill doesn't have the ad-level evidence to fully diagnose (that's closer to ad-strength/Quality Score territory — note it as an observation, not a budget recommendation).
- Never claim a campaign "can absorb more spend" without citing the actual budget-lost percentage as evidence.

## Output

One JSON array of findings, validated against `schemas/finding.schema.json`:

- `finding_id`: `ADP-001`, `ADP-002`, ... sequential.
- `source_skill`: `"ad-performance-diagnostic"`.
- `category`: `"dormant-campaign"`, `"shared-budget-cluster"`, or `"impression-share-constraint"`.
- `severity`: for dormant campaigns, scale by the campaign's own budget size (a dormant £0.01/day test campaign is much lower severity than a dormant £100/day one). For shared-budget clusters, scale by combined budget and cluster size. For impression-share constraints, scale by the estimated missed volume (budget-lost % × current spend, stated as a rough proxy, not a precise forecast).
- `confidence`: `high` when the account-structure evidence (budget/ads/keywords all checked) supports a specific explanation; `low` when none of the three explanations in Check 1 are evidenced and the cause is genuinely unknown.
- `evidence`: campaign name/ID, budget amount and ID, impression-share figures, and (for Check 1) the ads/keywords cross-reference results.
- `observation`: factual only.
- `interpretation`: kept separate — and must state explicitly which of the candidate explanations were checked and ruled in/out, not just the ones that applied.
- `recommendation`: plain-English next step — for dormant campaigns, "investigate and either fix delivery or pause/remove this campaign" (never assume which is right); for shared-budget clusters, "review whether this is intentional; if not, give each campaign its own budget"; for impression-share constraints, "worth testing a higher budget" (no specific figure) or "budget increase won't help here, the constraint is elsewhere."
- `estimated_impact`: plain-English, and explicit about uncertainty — e.g. "unknown until investigated" for dormant campaigns (this skill cannot estimate the value of fixing an unknown problem), not an invented figure.
- `effort`: `"low"` for shared-budget fixes (splitting a budget is quick), `"medium"` for dormant-campaign investigation (requires manual digging Google's UI, not something this skill's data alone resolves).
- `caveats`: always note that Check 1's three explanations aren't exhaustive (see the "record missing data" note above); for Check 3, always restate that no specific new budget figure is being recommended.

## What this skill must never do

- Never claim to know why a campaign is dormant beyond what budget/ads/keywords data actually shows — state what was checked and ruled in/out, not a single confident guess.
- Never recommend a specific new budget number — there's no evidence in this data for what the right number would be, only that current budget is (or isn't) a binding constraint.
- Never recommend a budget increase without citing `search_budget_lost_impression_share` as evidence, per `CLAUDE.md`.
- Never call a shared budget "wrong" outright — it can be deliberate. Flag it as worth reviewing, not as an error.
- Never imply any of this has been changed — this skill produces recommendations only (see `CLAUDE.md` — "Never make or attempt Google Ads changes").
