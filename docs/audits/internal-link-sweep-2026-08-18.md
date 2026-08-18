# Internal link sweep, 18 August 2026

Result of the first run of the new resolve mode in
`scripts/audit_link_coverage.py`, added on branch `claude/link-resolve-sweep`.

Command:

```
python scripts/audit_link_coverage.py --resolve --resolve-only --verify-all
```

Scope: 248 distinct root-relative links, gathered from `drafts/*.html` and
`internal-links/_all/`, each resolved against staging.

## Dead links: 2 (already fixed)

Both were fixed in `drafts/` by commit 436f465 on branch
`claude/vigorous-bhaskara-854930`. Listed here for the record, because no gate
caught them and they survived 49 copies each across the 25 sector guides.

| Dead URL | Correct URL |
| --- | --- |
| `/company-voluntary-arrangements/` | `/company-rescue-solutions/company-voluntary-arrangement/` |
| `/hmrc/time-to-pay-arrangement/` | `/hmrc/time-to-pay-hmrc/` |

## Redirect-only links: 5 (OUTSTANDING)

These resolve, so no reader hits a 404. Each costs one redirect hop. Repoint
them at the final address. Not yet done.

| Link in the drafts | Final address | Uses | Files |
| --- | --- | --- | --- |
| `/advice/cant-afford-to-pay-suppliers-what-are-the-options/` | `/company-cash-flow-problems/cant-afford-to-pay-suppliers-what-are-the-options/` | 25 | sector guides in `drafts/` |
| `/what-is-a-pre-pack-administration/` | `/company-rescue-solutions/pre-packs/` | 3 | `68115_rescue-your-business-from-insolvency.html`, `68183_funding-options-for-smes-in-the-uk.html`, `68356_advantages-and-disadvantages.html` |
| `/liquidation/director-redundancy/` | `/director-redundancy/` | 1 | `15010_what-happens-to-employees.html` |
| `/liquidation/voluntary-liquidation/` | `/liquidation/creditors-voluntary-liquidation/` | 1 | `79322_winding-up-petition-vs-compulsory-liquidation.html` |
| `/uk-insolvency-statistics/` | `/data/uk-insolvency-statistics/` | 1 | `internal-links/_all/articles-insights-hub.txt` |

Check the anchor text after each swap. The voluntary-liquidation one needs a
read: the old link said "voluntary liquidation" in general, and the target is
specifically the creditors' voluntary liquidation page.

## Two notes for whoever runs this next

The fast run and the thorough run disagree, by design. Without `--verify-all`
the sweep trusts `staging_page_inventory_fresh.json` and finds 2 redirect-only
links. With it, every link is fetched and it finds 5. The extra 3 are pages
that have moved since the inventory snapshot. Use `--verify-all` before a batch
push.

A 404 status is not proof of a dead link on this site, and a failed request is
not proof of a good one. Both are handled inside the script. Do not "simplify"
the verdict logic back to a status-code check.
