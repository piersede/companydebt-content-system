---
name: google-ads-weekly-audit
description: Orchestrate the four specialist skills into one prioritised weekly Markdown report for the Company Debt Google Ads account. Use when asked to run the full weekly audit, produce the audit report, or combine all the specialist findings.
---

# google-ads-weekly-audit

Read `google-ads-auditor/CLAUDE.md` in full before running this — every rule in it applies to the report this skill produces, not just to the specialist skills. This is the synthesis step: it doesn't gather new evidence or make new judgements about individual findings, it combines what the four specialists already produced into one document a human can act on.

## Pipeline (mechanical steps — run in order, do not skip or reorder)

1. `python scripts/run_specialists.py <run-folder>` — runs all four specialist scripts, saves output to `<run-folder>/specialist-findings/{negative-keywords,search-opportunities,campaign-diagnostics,pmax-findings}.json`.
2. `python scripts/merge-findings.py <run-folder>` — validates against `schemas/finding.schema.json`, deduplicates, ranks by severity/confidence, flags `conflicting_groups` (same campaign/ad_group/category, different recommendations). Writes `reconciled-findings.json`.
3. `python scripts/build_report_data.py <run-folder>` — computes headline numbers (with a real previous-period comparison from `daily-performance.json`, or explicitly suppressed if the comparison window isn't fully covered — never a misleading percentage), selects the top `reporting.maximum_priority_actions` findings, groups findings by skill. Writes `report-data.json`.

**Only after all three of those succeed** does the actual writing step happen — reading `report-data.json` and `reconciled-findings.json`, filling in `templates/weekly-audit-report.md`. This part is not mechanical; it requires judgement, but a narrowly scoped kind: organising and phrasing evidence that already exists, never generating new figures.

## Writing rules

- **Every number in the report must trace back to `report-data.json` or a specific finding's `evidence` field.** Do not compute anything by hand from raw snapshot files — if a number you want isn't in `report-data.json`, that's a sign the report-data builder needs extending, not a cue to calculate it inline (calculation errors are exactly what the mechanical step exists to prevent).
- **Every recommendation in "Highest-Priority Actions" and the section tables must cite its `finding_id`** (e.g. `NEG-001`, `ADP-013`), so a reader can trace it back to the underlying evidence.
- **Distinguish real conflicts from co-located distinct findings.** `reconciled-findings.json`'s `conflicting_groups` count includes both: most "conflicts" are actually just several different search terms recommended in the same ad group (not a contradiction — each has its own valid recommendation). A genuine conflict is two findings giving *opposite* practical guidance about the *same specific thing* — e.g. one finding says a campaign is budget-constrained and worth more spend, another says that same campaign is entangled in a shared-budget cluster with dormant siblings and needs untangling first. Genuine conflicts belong in "Items Requiring Human Judgement"; co-located-but-compatible findings just go in their normal section tables.
- **Executive Verdict is five short paragraphs, no more.** Cover: what changed (using the headline numbers, and stating plainly if the previous-period comparison was suppressed rather than presenting a partial figure as complete), where money appears to be leaking (cite the highest-severity findings), the strongest growth opportunity (search-terms-analyzer/opportunity findings, honestly caveated per the account's standing low-confidence conversion flag), whether tracking can be trusted (state the account's standing conversion-data caveat explicitly here, every time — it's structural to this account, not a one-off note), and what should happen first (usually the highest-severity, highest-confidence finding, but use judgement if a lower-ranked finding is genuinely more urgent, e.g. cheap-to-fix and high-value).
- **Performance Max section must separate Observed / Inferred / Not measurable**, per the template — pull each PMax finding's `evidence_label` directly, don't re-derive it.
- **British English, direct, no marketing language** (no "game-changer", "unlock", "leverage", "robust") — per `CLAUDE.md`'s writing-style rules.
- **"Actions Not Recommended"** — use this section for anything a naive reading of the data might suggest but the evidence doesn't actually support (e.g. "why not just add negative keywords for every zero-conversion term" — explain why that's wrong given the account's low-confidence conversion tracking and the `zero_conversion_spend_threshold` rule).
- **Only show headline-number rows that apply** — this account has no tracked conversion value, so omit the ROAS/conversion-value rows entirely rather than showing them as zero or blank (per the template's own instruction).
- **Methodology section must be filled from real config/manifest values** — reporting periods (`audit_start`/`audit_end`/`comparison_start`/`comparison_end` from `report-data.json`), `conversion_lag_days`, `primary_conversion_actions` (and the standing low-confidence flag on them), the thresholds actually used by each skill (`zero_conversion_spend_threshold`, `search_term_minimum_clicks`, etc. — pull from `account-config.yml`, don't restate from memory), and known data limitations (`data_completeness_notes` from `report-data.json`, plus each skill's own standing caveats — shared negative-list visibility gap, no PMax cost-per-category, etc.).
- **Query Appendix**: list every query file actually run (from the manifest's implicit list — the 17 files in `queries/**/*.gaql`) and any `failed_queries` from the manifest, verbatim.

## What this skill must never do

- Never state a headline number, percentage, or trend that isn't traceable to `report-data.json`.
- Never resolve a genuine conflict silently by picking one recommendation over another — surface it in "Items Requiring Human Judgement" and explain both sides.
- Never soften or omit the account's standing conversion-data trust caveat — it must appear in the Executive Verdict and the Methodology section every single run, not just when convenient.
- Never imply anything in the report has been implemented — this is a report, not a change log (see `CLAUDE.md` — "Never make or attempt Google Ads changes").
