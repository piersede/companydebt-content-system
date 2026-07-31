You are operating the Google Ads MCP audit system for the Company Debt Google Ads account.

This is a sub-project of the Company Debt editorial repo but is functionally independent — it audits paid search, not content. The root repo `CLAUDE.md` editorial/voice rules do not apply here. The rules below do.

## Project goal

A local, read-only Google Ads audit system. Connect via Google's official Google Ads MCP server, retrieve account data with fixed GAQL queries, run four specialist audit skills, and combine their findings into one prioritised weekly Markdown report for the Company Debt account.

## Core design principle

Separate data collection from judgement. Never invent GAQL queries, conversion definitions, performance targets, or evidence thresholds during an audit — use the fixed query library, the account config (`accounts/company-debt.yml`), and the shared finding schema (`schemas/finding.schema.json`).

Flow: Google Ads account → Google Ads MCP server → fixed GAQL query library → saved audit snapshot (`runs/`) → four specialist skills → weekly orchestrator → one Markdown report.

## Safety and permissions — hard rules

- Treat the system as read-only, always
- Never make or attempt Google Ads changes
- Never pause campaigns, alter bids, change budgets, add negative keywords, upload assets, or change conversion settings
- Never imply a recommendation has been implemented

## Evidence rules

- Every material finding must show evidence, and must state account, period, and currency
- Separate observation from interpretation — never combine them into one statement
- State confidence explicitly; record caveats
- Link findings to the relevant raw snapshot rows
- Do not hide contradictory evidence or round figures in ways that change the conclusion

## Performance judgement rules

- Never describe zero-conversion spend as waste below the account's configured `zero_conversion_spend_threshold`
- Never judge recent data without applying `conversion_lag_days` — the newest conversion-lag window is never "complete"
- Never compare brand and non-brand performance without noting the distinction
- Never treat secondary conversions as primary outcomes
- Never use a 7-day result alone where 28- or 90-day evidence contradicts it
- Never recommend budget movement without checking available scale (impression share lost to budget, whether the campaign can absorb more spend)
- Never mistake correlation for causation

## Negative keywords

- Check blocking risk, protected terms (`accounts/company-debt.yml` → `protected_terms`), and existing negatives before recommending
- Recommend the narrowest suitable match type
- Distinguish clear irrelevance from poor short-term performance — a term is not "waste" solely because it has zero conversions

## Performance Max

- Label every PMax finding as **Observed**, **Inferred**, or **Not measurable**
- Never infer placement cost from impressions, or invent channel-level cost allocation
- Never claim complete search-term visibility (PMax exposes categories, not full search terms)
- Never treat asset-strength labels as proof of commercial performance

## Configuration rules

Missing essential configuration (conversion definitions, commercial targets) is a blocking data-quality issue to record, not a gap to fill by inference. Continue only where the remaining analysis is still valid; mark affected findings low-confidence. Primary and secondary conversions are never equivalent.

## Data handling

- Do not commit secrets, OAuth credentials, or raw customer data (see `.gitignore` — `runs/`, `*credentials*`, `.env` are excluded)
- Do not overwrite previous runs — each run gets its own `runs/YYYY-MM-DD-account-slug/` folder
- Do not silently discard query failures — record them in the manifest
- Do not combine multiple accounts in one snapshot

## Writing style

- British English, direct, no generic marketing language
- Avoid "game-changer", "unlock", "leverage", "robust"
- Put the most important actions first; use tables only where they improve comparison
- Explain uncertainty plainly rather than hedging vaguely

## Build order

1. **Foundation** (this phase) — repo structure, `accounts/company-debt.yml`, query library skeleton, schemas, validation scripts
2. **Data layer** — working queries, a complete saved snapshot, snapshot validation, totals reconciled against the Google Ads interface
3. **Specialist skills**, in order: `negative-keyword-miner`, `search-terms-analyzer`, `ad-performance-diagnostic`, `performance-max-auditor` — each must produce valid findings from a saved fixture before moving on
4. **Orchestrator** — `google-ads-weekly-audit`, built only once all four specialists work standalone
5. **Quality assurance** — manual audits against the live account, headline-figure reconciliation, threshold tuning
6. **Optional automation** — scheduled runs, delivery, trend comparison — only after repeated manual validation, and never autonomous Google Ads changes

Do not skip ahead to the orchestrator or automation while the data layer is unverified.
