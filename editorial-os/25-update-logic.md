# 25. Update Logic and Freshness Governance

Governance layer for freshness, volatility tracking, and review triggers. In insolvency content, stale claims are a trust, liability, and reputational risk.

---

## 25.1 Volatility model

Every page is assigned a volatility level:

| Level | Label | Description | Base review interval |
|---|---|---|---|
| V4 | Event-driven | Can change within days | 7-14 days after trigger |
| V3 | Fast-moving | Rates, fees, scheme terms, active enforcement | 21-30 days |
| V2 | Moderately stable | Procedural detail and standard processes | 90-180 days |
| V1 | Slow-changing | Statutory frameworks and established case law | 6-12 months |
| V0 | Evergreen | Conceptual foundations | Annual review |

---

## 25.2 Hard triggers

Affected pages must be reviewed within 72 hours when these occur:

- statutory threshold changes
- HMRC enforcement-tool or rate changes
- Insolvency Service guidance changes
- SIP or ethics-standard changes
- major case-law affecting director duties or insolvency tests
- government-backed loan enforcement changes

---

## 25.3 Soft triggers

These bring the next review forward by 14 days:

- Insolvency Service statistics releases where cited
- HMRC manual archiving warnings
- Companies House guidance updates
- provider licensing or merger changes
- new sector insolvency data relevant to the page

---

## 25.4 Freshness tiers by page type

| Tier | Page types | Review cadence | Trigger sensitivity |
|---|---|---|---|
| Critical | Director duties, insolvency tests, creditor priority, HMRC enforcement, government-loan risk | 90-180 days plus hard triggers | V3-V4 |
| High | Core procedures and major creditor-action pages | 6-9 months | V2-V3 |
| Standard | General guides and sector overviews | Annual | V1-V2 |
| Commentary | News and topical analysis | No evergreen expectation | V0 |

---

## 25.5 Refresh classes

| Class | Label | Scope |
|---|---|---|
| L0 | No change | Review confirms current state |
| L1 | Light refresh | Dates, links, threshold checks |
| L2 | Moderate refresh | Volatile facts updated |
| L3 | Substantial refresh | Section-level rewrite plus cannibalisation review |
| L4 | Full rebuild | Full workflow restart |

L2 and above trigger the workflow from Stage 5 onward. L3 and above require a registry and overlap review.

---

## 25.6 Volatile facts ledger

Claims that can expire must be tracked at claim level with:

- `fact_id`
- `page_url`
- `claim_text`
- `volatility_tag`
- `last_verified`
- `verification_source`
- `expiry_in_days`

Claims that belong in the ledger include:

- statutory thresholds
- HMRC enforcement practices
- pricing and fee claims
- scheme terms
- creditor priority order
- disqualification ranges
- Time to Pay norms

---

## 25.7 Guardrails

Standing review requirements:

- statutory-threshold changes: 72 hours
- winding-up consequence changes: 72 hours
- HMRC negotiation shifts: quarterly
- creditor-priority changes: annual plus triggers
- provider trust changes: 30 days
- standards changes: 30 days

---

## 25.8 Update workflow

1. trigger detected
2. review ticket tied to `node_id`
3. reviewer assigned by freshness tier
4. content updated by refresh class
5. `last reviewed` date updated visibly
6. change logged in registry
7. post-update re-index monitoring

---

## 25.9 Trust signal updates by refresh class

- `L0`: update last-reviewed date only
- `L1`: update last-reviewed date and reviewer block
- `L2`: verify sources and methodology note
- `L3-L4`: full trust-pack review
