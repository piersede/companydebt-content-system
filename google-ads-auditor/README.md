# Google Ads MCP Audit System

A local, read-only Google Ads audit system for the Company Debt account. Connects to Google Ads via Google's official Google Ads MCP server, pulls account data through a fixed GAQL query library, runs four specialist audit skills, and produces one prioritised weekly Markdown report.

This system **never** makes changes to Google Ads — no bid, budget, pause, negative-keyword, or asset changes. Read and report only.

## Status: Phase 1 (Foundation)

This is the foundation layer only — repo structure, account config, query library skeleton, schemas, and validation scripts. The five Claude Code skills (`negative-keyword-miner`, `search-terms-analyzer`, `ad-performance-diagnostic`, `performance-max-auditor`, `google-ads-weekly-audit`) are built in later phases once live MCP access is confirmed.

## Required setup before any live audit

1. **Google Ads MCP server** — install and configure Google's official `google-ads-mcp` server. See `MCP-SETUP.md` for the connection pattern; exact command/env vars must be checked against the installed server's own docs.
2. **Credentials** (never committed — see `.gitignore`):
   - A Google Ads developer token
   - A Google Cloud project with the Google Ads API enabled
   - OAuth credentials or Application Default Credentials for a Google identity with (ideally read-only) access to the Company Debt Google Ads account
   - The Company Debt Google Ads `customer_id` (and `login_customer_id` if accessed via a manager account)
3. **Account configuration** — fill in the real values in `accounts/company-debt.yml` (customer ID, targets, brand terms, protected terms). See that file's inline comments for what's still a placeholder.
4. **Validate config** — `python scripts/validate-config.py accounts/company-debt.yml`

## Directory guide

- `accounts/` — one YAML config per Google Ads account (currently: `company-debt.yml`)
- `queries/` — version-controlled GAQL query library, grouped by purpose
- `schemas/` — JSON Schemas for findings and the run manifest
- `templates/` — the weekly report Markdown template
- `runs/` — saved audit snapshots, one folder per run (`YYYY-MM-DD-account-slug/`); gitignored, contains real account data
- `scripts/` — validation and merge scripts (`validate-config.py`, `validate-snapshot.py`, `merge-findings.py`)
- `tests/` — fixtures and expected findings for testing specialist skills offline
- `.claude/skills/` — the five Claude Code skills (built in Phase 3–4)

## Build order

See `CLAUDE.md` for the project rules and the full build plan. Do not build the specialist skills before the data layer (queries + snapshot + validation) is working and reconciling against the Google Ads interface. Do not build the orchestrator before each specialist skill produces valid findings from a saved fixture.
