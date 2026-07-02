# CompanyDebt Outreach Conductor

Citation-gap outreach for Company Debt's data hub. **Auto-draft, human-send** — the conductor
never sends an email; it writes a draft into Outlook (and the Monday board) for a person to
review and send. Rebuilt from the BusinessExpert outreach spec, adapted for Company Debt.

**Phase 1 = `STATS_HUB_ONLY`.** It pitches only the
[UK Company Insolvency Statistics](https://www.companydebt.com/data/uk-insolvency-statistics/)
page: when a journalist cites *someone else's* insolvency figure, we offer our fresher, more
current UK cut of that specific point. The numbers are official (Insolvency Service + Companies
House), so we never imply they are proprietary — the value is the clearer monthly presentation.

## Strategy in one line

*Your article makes this point, you currently cite this source, and Company Debt keeps a more
current UK insolvency figure for that exact point.* Never "please link to us".

## The pipeline

`source` (Ahrefs backlinks → board rows) → **scan**: scrape → match the cited stat → find/verify
contact → draft (voice model) → run the guardrails → Outlook draft + `Ready to contact`.

Anything the conductor can't finish safely halts to a human instead of drafting from bad context:
blocked page → stays `Not started` + note; no verified contact → `To research`; weak fit →
`Defunct`. A daily cap (default 5) keeps volume low so we judge quality before scale.

## Guardrails (fail-closed, before anything is queued)

1. **Suppression** — opt-out emails/domains (`suppression.json`).
2. **Corporate-only** — free/personal inboxes held for manual approval.
3. **Contact-confidence** — no generic/role inboxes, no unverified/guessed, no departed authors.
4. **Claim ledger** — only the approved figures in the catalogue may appear; invented/rounded
   numbers are rejected.
5. **Dash gate** — no em/en dashes (an AI tell).
6. **Structural variation** — fingerprints each draft, rejects one too similar to a recent one.
7. **Citation framing** — must anchor on a captured cited point, not the topic.
8. **Regulated-claim gate** *(Company Debt-specific)* — no advice, no guaranteed outcomes, no
   false exclusivity on official stats, no fabricated affiliation/regulatory claims.

Run them all offline any time: `node conductor.js selftest`.

## Setup

1. **Node** ≥18 (uses global `fetch`; no `npm install` needed — zero runtime deps).
2. **Create a NEW Monday "Outreach" board.** Do **not** reuse the Content Rework Tracker.
   Add these columns: Status (labels: `Not started`, `Ready to contact`, `To research`,
   `Contacted`, `Responded`, `Defunct`), Contact email, Article URL (link), Asset URL (link),
   Cited source (text/link), Outreach notes (long text), **Rejection reason** (dropdown with the
   values in `config.js → rejectionCategories`), Last contacted (date).
3. Put the board id in `OUTREACH_BOARD_ID`, then run `node conductor.js boardcols` and paste each
   column id into the matching `OUTREACH_COL_*` var (see `.env.example`).
4. Add keys to the repo-root `.env` (or `outreach/.env`, gitignored):
   - **Drafting model** — auto-resolves: Anthropic if `ANTHROPIC_API_KEY` is set, else **Gemini**
     via the `GEMINI_API_KEY` already in the repo `.env` (default `gemini-2.5-pro`, no extra
     setup). Force with `OUTREACH_PROVIDER`; override the model with `OUTREACH_DRAFT_MODEL`.
   - `OUTREACH_SENDER_NAME` — the real person the emails are from (required for good drafts)
   - `HUNTER_API_KEY` (optional — auto contact-find; without it, no-email items halt to research)
   - `SCRAPINGBEE_API_KEY` (optional — fallback for bot-blocked pages)
   - `GRAPH_*` + `OUTREACH_MAILBOX` (optional — Outlook drafting; see below)
   `MONDAY_API_KEY` is already in the repo-root `.env`.

## Daily use

```
node conductor.js scan                 # dry-run: shows routing, no drafts, no writes
node conductor.js scan --process       # draft the good ones (writes only if OUTREACH_REVIEW=write)
node conductor.js source backlinks.csv # preview new rows from an Ahrefs export (--commit to create)
node conductor.js retry <itemId>       # re-queue after you add a contact email on the board
node conductor.js reject <itemId> <category>   # set the Rejection-reason column
```

Recommended: schedule one `scan --process` at ~6am with `OUTREACH_REVIEW=write`. Start with
`OUTREACH_REVIEW=print` for the first mornings to read drafts before it writes to the board.
Add a second `source` run around each monthly Insolvency Service release (the natural hook), and
**refresh `approvedFigures` + `updated`/`nextRelease` in `companydebt-asset-catalogue.json` each
month** from the live page.

### Outlook drafting (Microsoft Graph)

`GRAPH_AUTH=app` (client-credentials) for the unattended scheduler; `GRAPH_AUTH=delegated`
(device-code) for manual runs into your own mailbox. The conductor only ever creates a **draft**;
it never sends. If Graph is unconfigured, the draft still persists as a Monday note.

## Files

- `config.js` — all knobs (board, columns, flags, sender, thresholds).
- `companydebt-asset-catalogue.json` — the pitchable page(s) + the claim ledger (approved figures).
- `competitors.json` — data competitors + cited-slug hints for `source`.
- `suppression.json` — opt-out list.
- `lib/` — `scraper` · `match` · `gates` · `enrich` (Hunter) · `graph` (Outlook) · `claude`
  (voice) · `monday` · `state` · `util`.
- `state/` — local checkpoints + draft fingerprints (gitignored).

## Not yet built (Phase 2+)

- Widen past `STATS_HUB_ONLY` to the hub/pillar pages (already listed in `phase2Assets`).
- Reply tracking (poll the mailbox → `Responded`, classify, queue a follow-up).
- Ahrefs API sourcing (currently CSV export).
- Expert-source outreach — only if a real, named Insolvency Practitioner will go on record.
