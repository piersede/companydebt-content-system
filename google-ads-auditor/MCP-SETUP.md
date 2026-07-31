# Google Ads MCP Server Setup

This project uses Google's official Google Ads MCP server. Configure it as a **local stdio** server first — do not add Cloud Run, remote hosting, or scheduling until the local version is verified working.

## Suggested config pattern

Add to Claude Code's MCP config (project-level `.mcp.json` or user-level settings — not committed if it contains secrets):

```json
{
  "mcpServers": {
    "google-ads-mcp": {
      "command": "pipx",
      "args": [
        "run",
        "--spec",
        "git+https://github.com/googleads/google-ads-mcp.git",
        "google-ads-mcp"
      ],
      "env": {
        "GOOGLE_PROJECT_ID": "${GOOGLE_PROJECT_ID}",
        "GOOGLE_ADS_DEVELOPER_TOKEN": "${GOOGLE_ADS_DEVELOPER_TOKEN}",
        "GOOGLE_APPLICATION_CREDENTIALS": "${GOOGLE_APPLICATION_CREDENTIALS}"
      }
    }
  }
}
```

The exact command and environment variable names must be checked against the currently installed MCP server's own documentation before relying on this — the server's interface may have changed since this was written.

## Required access

- A Google Ads manager account (if accessing Company Debt's account via MCC)
- A Google Ads developer token
- A Google Cloud project with the Google Ads API enabled
- OAuth credentials or Application Default Credentials
- A Google identity with access to the Company Debt Google Ads account — use read-only account permissions wherever Google Ads' permission model allows it

## Credential storage

Store developer token, project ID, and credential file path as environment variables (e.g. in this project's own `.env`, gitignored) — never in a committed file. `GOOGLE_APPLICATION_CREDENTIALS` should point to a service-account JSON key stored outside the repo, or to a path excluded by `.gitignore`.

## Initial connection test (do this before building anything else)

1. List accessible Google Ads customers
2. Query the Company Debt customer directly
3. Return campaign names and statuses
4. Return cost, clicks, and conversions for a fixed 7-day period
5. **Match those totals against the Google Ads web interface exactly** — do not proceed to build the query library or skills until they reconcile
