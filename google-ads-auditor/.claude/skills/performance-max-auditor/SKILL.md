---
name: performance-max-auditor
description: Audit the Company Debt Performance Max campaign — off-target category-level search insights, asset-group coverage, and dormant-campaign detection. Use when running the performance-max-auditor stage of the weekly Google Ads audit, or when asked about PMax performance.
---

# performance-max-auditor

Read `google-ads-auditor/CLAUDE.md` in full before running this — the "Performance Max" rules section is the core constraint on everything this skill does and is not repeated in full below. The single most important discipline: **PMax data is structurally less transparent than Search data**, and every finding must be honest about exactly how much less.

## The four PMax rules, applied concretely

1. **Label every finding `evidence_label: observed | inferred | not_measurable`.** `observed` = the underlying field is a direct fact (a category-label match, an impressions count). `inferred` = Google's own derived label (ad strength) or this skill's own read of the evidence. `not_measurable` = the data genuinely doesn't support the claim (per-category cost, per-placement cost).
2. **Never infer placement cost from impressions, or invent channel-level cost allocation.** `placements.gaql` returns impressions only — Google does not expose placement-level cost for PMax. Never present placement impression counts alongside a cost figure that implies they're related.
3. **Never claim complete search-term visibility.** `pmax-search-terms.gaql` returns category-level labels (`campaign_search_term_insight.category_label`), not literal search queries, and — unlike `search_term_view` for Search — **has no cost field at all**, only impressions and clicks. Any off-target finding here can state a topic concern; it cannot state a £ impact.
4. **Never treat asset-strength labels as proof of commercial performance.** `asset_group.ad_strength` is Google's own coverage/completeness heuristic, not a measure of whether the asset group is actually converting well.

## Inputs (from one `runs/YYYY-MM-DD-<account-slug>/` snapshot)

All from `raw/pmax.json`, which nests four query results under sub-keys (see `scripts/run_snapshot.py`'s `QUERY_MAP`):
- `pmax.json["search_terms"]` — from `queries/performance-max/pmax-search-terms.gaql`. Category-level insights, 7-day audit window.
- `pmax.json["asset_groups"]` — from `queries/performance-max/asset-groups.gaql`. Ad strength, status, cost/impressions/clicks, 7-day window.
- `pmax.json["campaigns"]` — from `queries/performance-max/pmax-campaigns.gaql`. Campaign-level budget and performance, 7-day window.
- `pmax.json["placements"]` — from `queries/performance-max/placements.gaql`. Impressions only, no cost. Often empty for accounts without significant Display/YouTube placement volume — an empty result is `not applicable`, not a failure (per that query file's own purpose comment).
- `pmax.json["products"]` — from `queries/performance-max/products.gaql`. Shopping/product performance. Empty for accounts with no Shopping feed (Company Debt has none) — `not applicable`, not a failure.
- `account-config.yml` (the copy saved inside the run folder) — supplies `irrelevant_topics` (the same list `negative-keyword-miner` uses for Search — reused here for consistency, not duplicated as a separate PMax-specific list).

## Checks

### 1. Off-target category-level search insights (`category: pmax-off-target-category`)

For every row in `search_terms`, case-insensitive substring-match `campaign_search_term_insight.category_label` against `irrelevant_topics` (same list, same mechanism as `negative-keyword-miner` — reused deliberately for consistency across Search and PMax). This is `evidence_label: observed` — the category label match itself is a fact.

**Do not estimate cost impact.** There is no cost field on this query. State impressions/clicks as the evidence, and mark any cost-adjacent claim `not_measurable` explicitly in the caveats, rather than silently omitting the point.

**Recommendation is mechanically different from `negative-keyword-miner`'s.** PMax does not support ad-group or campaign-level EXACT-match negatives the way Search does. Recommend adding the matched term to the account-level Performance Max negative keyword list (Google Ads Settings → Account-level negative keywords), or a brand exclusion list if the match is a competitor/brand name — never phrase the recommendation as an "EXACT match ad-group negative," that mechanism doesn't exist for PMax.

**Categories that don't match `irrelevant_topics` are not this skill's job to classify.** If a category label looks off-target but isn't covered by the configured list, that's a configuration gap to flag for human review (list it in a caveat/note), not a judgement to make unilaterally — same discipline as `negative-keyword-miner`'s "never invent a new irrelevant_topics entry mid-run."

### 2. Asset-group coverage (`category: pmax-asset-strength`)

For every row in `asset_groups` where `asset_group.status == "ENABLED"` **and** the parent campaign (cross-reference `campaigns`) is also `ENABLED` — a `PAUSED` asset group, or one in a `PAUSED` campaign, isn't costing any live coverage right now regardless of its strength label, so it's not a finding.

Flag `POOR` or `AVERAGE` strength asset groups among the remaining (live, in-scope) set. This is `evidence_label: inferred` — always include the mandatory caveat that ad strength is a coverage/completeness signal, not proof of commercial performance, and that a `POOR`/`AVERAGE` asset group could still be converting fine, or an `EXCELLENT` one could be underperforming — this check has no visibility into which.

If every live asset group is already `EXCELLENT`/`GOOD`, that's a valid clean result — report it as such, don't force a finding.

### 3. Dormant `ENABLED` PMax campaigns (`category: pmax-dormant-campaign`)

Same logic as `ad-performance-diagnostic`'s Check 1, but simpler: PMax doesn't have the Search-specific `impression-share.gaql` data or shared-budget cross-referencing built for it yet in this query library. Flag any `campaigns` row where `campaign.status == "ENABLED"`, `campaign_budget.amount_micros > 0`, and `metrics.impressions == 0` for the audit period. `evidence_label: observed`. Do not guess why — state plainly that a deeper diagnosis (ads/asset-group status, policy holds) would need the same cross-referencing `ad-performance-diagnostic` does for Search, which this skill doesn't yet replicate for PMax.

### 4. Placements and products — report presence/absence honestly

If `placements` is non-empty, do not produce a cost-based finding from it (no cost field exists) — at most, note which placements got meaningful impressions as `observed`, `not_measurable` for any spend implication. If empty, state plainly "no placement data this period" — not a failure, not evidence of anything.

If `products` is non-empty, treat it like a mini version of Check 1/2 for Shopping-specific issues. If empty (as for Company Debt, which has no Shopping feed), state plainly "not applicable — no Shopping feed" — never a failure or a gap.

## Output

One JSON array of findings, validated against `schemas/finding.schema.json`. Every finding requires `evidence_label` (`observed`/`inferred`/`not_measurable`) in addition to the standard required fields.

- `finding_id`: `PMX-001`, `PMX-002`, ... sequential.
- `source_skill`: `"performance-max-auditor"`.
- `category`: one of `pmax-off-target-category`, `pmax-asset-strength`, `pmax-dormant-campaign`.
- `severity`/`confidence`: scale by impressions/clicks (Check 1, 3) or by how many live asset groups are affected (Check 2) — there's no cost figure to scale by for Check 1.
- `recommendation`: per-check, as described above — never phrase a PMax recommendation using Search-specific mechanisms (ad-group EXACT negatives, campaign-level negative keyword lists that don't apply to PMax the same way).
- `caveats`: always restate the specific PMax limitation relevant to that finding (no cost on search-term categories; ad strength ≠ performance; no placement cost).

If a check produces zero qualifying findings, report that explicitly, same as the other three skills — including for Check 2 when the account's live asset groups are all already strong, which is the actual real-account result here.

## What this skill must never do

- Never present a category-level finding with an implied £ cost — the data doesn't have one.
- Never treat `POOR`/`AVERAGE` ad strength as proof of underperformance, or `EXCELLENT` as proof of good performance.
- Never recommend a Search-style ad-group EXACT negative for a PMax off-target category — the mechanism doesn't exist there.
- Never invent a new `irrelevant_topics` entry to classify an unmatched category — flag it as a config gap for human review instead.
- Never imply any of this has been changed — recommendations only (see `CLAUDE.md` — "Never make or attempt Google Ads changes").
