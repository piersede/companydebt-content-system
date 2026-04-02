# 25. Update Logic and Freshness Governance

Governance layer for content freshness, volatility tracking, and review triggers. In insolvency content, stale claims are not just an SEO problem — they create liability and reputational risk.

---

## 25.1 Volatility model

Every page is assigned a volatility level based on how quickly its claims can become wrong:

| Level | Label | Description | Base review interval |
|---|---|---|---|
| V4 | Event-driven | Claims can change within days (enforcement actions, statutory thresholds, HMRC policy) | 7-14 days after trigger |
| V3 | Fast-moving | Rates, fees, scheme terms that shift quarterly or on announcement | 21-30 days |
| V2 | Moderately stable | Procedural detail, creditor priority, standard processes | 90-180 days |
| V1 | Slow-changing | Statutory frameworks, established case law, structural definitions | 6-12 months |
| V0 | Evergreen | Conceptual foundations unlikely to change without legislative reform | Annual review |

---

## 25.2 Hard triggers (72-hour review requirement)

When any of these occur, all affected pages must be reviewed within 72 hours:

- statutory changes to insolvency thresholds (e.g., winding-up petition minimum debt level)
- HMRC enforcement tool or rate changes
- winding-up guidance changes from the Insolvency Service
- Insolvency Service consultation outcomes affecting procedure
- Statement of Insolvency Practice (SIP) or ethics standard changes
- major case law affecting director duties or insolvency tests (e.g., Supreme Court decisions)
- changes to government-backed loan scheme enforcement or treatment

---

## 25.3 Soft triggers (14-day review acceleration)

These bring the next review forward by 14 days:

- monthly Insolvency Service statistics releases (where the page cites statistics)
- HMRC internal manual archiving warnings
- Companies House guidance updates
- provider entity changes (IP firm mergers, licensing changes)
- new sector-specific insolvency data relevant to page content

---

## 25.4 Freshness tiers by page type

| Tier | Page types | Review cadence | Trigger sensitivity |
|---|---|---|---|
| Critical | Director duties, insolvency tests, creditor priority, HMRC enforcement, government loan scheme risk | 90-180 days rolling + all hard triggers | V3-V4 |
| High | Core procedure explainers (CVA, CVL, administration), major creditor action pages | 6-9 months | V2-V3 |
| Standard | General guides, sector overviews (unless tied to current policy) | Annual | V1-V2 |
| Commentary | News, topical pieces, date-specific analysis | No refresh expectation | V0 |

Commentary-tier pages must be clearly date-stamped and labelled as time-specific. They must never be presented as evergreen guidance.

---

## 25.5 Refresh classes

When a review is triggered, the scope of work depends on what has changed:

| Class | Label | Scope | Typical effort |
|---|---|---|---|
| L0 | No change | Review confirms all claims current; update "last reviewed" date | Minutes |
| L1 | Light refresh | Hygiene: update dates, verify links, confirm pricing/thresholds still current | 30-45 minutes |
| L2 | Moderate refresh | Volatile facts need updating: rates, fees, enforcement practices, statistics | Half day |
| L3 | Substantial refresh | Section-level rewrite; new information changes the decision framing; cannibalisation check required | 1-2 days |
| L4 | Full rebuild | Page structure no longer serves the intent; requires new brief, SME review, and full workflow from Stage 1 | 2-5 days |

L2 and above trigger the full workflow from Stage 5 onward (trust pass through pre-publish gate). L3 and above require cannibalisation review against entity registry.

---

## 25.6 Volatile facts ledger

Claims that can expire must be tracked at the claim level:

| Field | Purpose |
|---|---|
| fact_id | Unique identifier for the claim |
| page_url | Where the claim appears |
| claim_text | The specific assertion |
| volatility_tag | V0-V4 |
| last_verified | Date of last verification |
| verification_source | Primary source used |
| expiry_in_days | Maximum days before re-verification required |

### Claims that must be in the ledger

- statutory thresholds (winding-up petition minimum, CVA voting percentage)
- HMRC enforcement practices and preferential creditor status
- pricing and fee claims about any provider or service
- government scheme terms (BBL, CBILS treatment)
- creditor priority order
- disqualification period ranges
- Time to Pay norms and duration limits

---

## 25.7 Guardrails

These are standing review requirements that override normal cadence:

| Guardrail | Trigger | Maximum age before forced review |
|---|---|---|
| Statutory threshold | Any legislative change affecting thresholds | 72 hours |
| Winding-up consequence | Changes to winding-up petition process or outcomes | 72 hours |
| HMRC negotiation | Time to Pay policy changes | Quarterly |
| Creditor priority | Changes to priority order or prescribed part | Annual + any trigger |
| Provider trust | IP firm licensing, accreditation, or regulatory changes | 30 days |
| Standards | SIP or ethics standard changes | 30 days |

---

## 25.8 Update workflow

1. Trigger detected (hard, soft, or scheduled cadence)
2. Review ticket created, tied to node_id in content registry
3. Reviewer assigned based on freshness tier (IP review for critical tier; editorial for standard)
4. Content updated per refresh class
5. "Last reviewed" date updated visibly on page
6. Change logged in content registry (what changed, why, reviewer, date)
7. Re-index monitoring for 7 days post-update

---

## 25.9 Trust signal updates by refresh class

| Refresh class | Trust signal requirements |
|---|---|
| L0 | Update "last reviewed" date only |
| L1 | Update "last reviewed" date; verify reviewer block still accurate |
| L2 | Update "last reviewed" date; verify all source citations still valid; update methodology note if evidence basis changed |
| L3-L4 | Full trust pack review: author, reviewer, methodology, sources, scope statement, commercial disclosure |
