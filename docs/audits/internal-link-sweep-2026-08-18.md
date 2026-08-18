# Internal link sweep, 18 August 2026

Result of the first run of the resolve mode in `scripts/audit_link_coverage.py`.

Command:

```
python scripts/audit_link_coverage.py --resolve --resolve-only --verify-all
```

Scope: every distinct root-relative link in `drafts/*.html` and
`internal-links/_all/`, each one fetched from staging and judged on the page it
actually returns.

## Current state: 0 dead, 1 redirect-only

242 distinct links. Nothing is dead. One still costs the reader a hop.

## Outstanding

`/uk-insolvency-statistics/` redirects to `/data/uk-insolvency-statistics/`.

It appears once, in `internal-links/_all/articles-insights-hub.txt`. That file
is a captured copy of the live Articles and Insights hub page, not a draft.
Editing the copy would only silence the sweep. The fix is on the hub page
itself, on staging: repoint the link, then push, then re-run the sweep to
confirm it drops to zero.

## What the first run found, before the fixes landed

Kept for the record, because none of it was caught by a gate.

Two dead links, each used 49 times inside the shared "your options" block
across the 25 sector guides:

| Dead URL | Correct URL |
| --- | --- |
| `/company-voluntary-arrangements/` | `/company-rescue-solutions/company-voluntary-arrangement/` |
| `/hmrc/time-to-pay-arrangement/` | `/hmrc/time-to-pay-hmrc/` |

Both were fixed in the drafts by 436f465, and both old URLs were given staging
redirects and redirect sentinels by b8933f0, which also catches inbound links
from other sites.

Five redirect-only links. 436f465 fixed the four that lived in drafts:

| Link | Final address |
| --- | --- |
| `/advice/cant-afford-to-pay-suppliers-what-are-the-options/` | `/company-cash-flow-problems/cant-afford-to-pay-suppliers-what-are-the-options/` |
| `/what-is-a-pre-pack-administration/` | `/company-rescue-solutions/pre-packs/` |
| `/liquidation/director-redundancy/` | `/director-redundancy/` |
| `/liquidation/voluntary-liquidation/` | `/liquidation/creditors-voluntary-liquidation/` |

The fifth is the outstanding one above.

## Two notes for whoever runs this next

The fast run and the thorough run are meant to disagree. Without `--verify-all`
the sweep trusts `staging_page_inventory_fresh.json`, which is a snapshot, and
it missed 3 of the 5 redirect-only links because the inventory still vouched
for pages that had moved. Use `--verify-all` before a batch push.

A 404 status is not proof of a dead link on this site, and a failed request is
not proof of a good one. Roughly 83% of reported broken links here are
bot-blocks that answer 200 to a browser and 404 to a crawler, so the script
judges on the real 404 page title and sends a browser user-agent. An early
version of it ran with no credentials, was refused on all 33 addresses, found
no 404 title in any refusal and reported a clean sweep. Both traps are handled
inside `resolve_one`. Do not reduce that back to a status-code check.
