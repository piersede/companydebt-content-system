# Tests

Fixture-based tests for the specialist skills, so they can be validated without hitting the live Google Ads MCP server.

- `fixtures/` — saved snapshot data shaped like `runs/*/raw/*.json`, one sub-folder per test scenario
- `expected-findings/` — the findings a correct skill run should produce for each fixture, validated against `schemas/finding.schema.json`

## Scenarios to cover (build once the specialist skills exist)

1. Low-volume lead-generation account
2. Ecommerce account with conversion values
3. Mixed primary and secondary conversions
4. Brand and non-brand campaigns
5. Recently launched campaigns
6. Long conversion lag
7. Search campaigns with irrelevant terms
8. Search campaigns with valuable untargeted terms
9. PMax without a product feed
10. Retail PMax with many products
11. Campaigns limited by budget
12. Campaigns limited by rank
13. Campaigns with broken conversion tracking
14. Campaigns with zero conversions but insufficient evidence
15. Accounts with different currencies

## Required assertions

A correct system:

- Never calls low-volume zero-conversion spend "waste"
- Never recommends protected terms as negatives
- Never describes secondary conversions as leads or sales
- Never recommends moving budget without available scale
- Applies conversion lag
- Labels PMax inferences correctly (observed / inferred / not measurable)
- Produces the same findings from the same snapshot (deterministic)
- Records missing data instead of inventing it
- Produces valid Markdown and JSON outputs
