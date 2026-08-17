# Company Debt Insolvency Intelligence: canonical product specification

**Status:** canonical. Supersedes both earlier drafts (the 14 August product
definition and the 14 August engineering draft). If those are still circulating,
this file wins.
**Written:** 14 August 2026
**Geography at launch:** England and Wales for detailed sector intelligence
**Core proposition:** turn official insolvency data into a continuously updated,
sector-specific intelligence system that explains where financial stress is
building, where it is easing, what is moving underneath the headline, and what a
business should watch next.

## How to read this document

Two drafts were written independently. This merges them. Where they disagreed,
the disagreement was settled by checking the actual data in this repository, not
by preference. Those checks are in **Part 3**, and three of them change what can
be built. Read Part 3 before designing anything.

Sections marked **[VERIFIED]** were confirmed against files in this repo or against
the primary source on 14 August 2026. Sections marked **[DECISION]** need a human
answer before the work they describe can start.

---

# PART 1: THE PRODUCT

## 1.1 What it is

> A sector-level financial stress intelligence platform built from official
> insolvency data and related economic indicators, interpreted by Company Debt.

Four layers, always distinguishable:

**Official data** → **Company Debt calculation** → **Company Debt analysis** →
**Company Debt practitioner interpretation**

The product answers a better question than "how many companies became insolvent".
It answers: *how financially stressed is this industry now, is that getting better
or worse, how unusual is the current position, what is changing underneath the
headline, and what should a business in this industry watch next?*

## 1.2 What it is not

Not a company credit score. Not a prediction that a named company will fail. Not a
substitute for Companies House or The Gazette. Not a generic economic dashboard.
Not a black-box risk score. Not an automated causal inference system. Not a
collection of near-duplicate sector articles.

It stays centred on corporate financial distress and insolvency.

## 1.3 The test for every feature

> Does this tell someone something useful that they would not learn by opening the
> Insolvency Service spreadsheet?

If no, it is not intelligence. Qualifying value: comparison, trend, context,
anomaly, change detection, historical significance, leading signals, practitioner
insight, operational relevance.

## 1.4 Users

| User | Question | Needs |
|---|---|---|
| Director or owner (primary) | Are businesses like mine failing more often? | Status, trend, peers, pressures, what to watch, route to help if distressed |
| Journalist | Which sectors are rising fastest? | Sortable table, context, anomaly explanations, CSV, citation, methodology |
| Adviser / IP | Where is distress emerging? | Cross-sector view, leading indicators, procedure mix, exports, alerts |
| Lender / supplier | Are conditions worsening among my customers? | Direction, early warning, relative comparison, method |
| Search and AI systems | — | Clean headings, definitions, structured data, provenance, stable URLs |

The public product stays **sector level**, never company level.

---

# PART 2: NON-NEGOTIABLE PRINCIPLES

## 2.1 Decision before detail

Every page answers the main question immediately. "Restaurant insolvency pressure
is easing, but remains elevated." Never "The latest statistics have been
published…".

## 2.2 No black box

Do not launch a "Sector Stress Score: 73/100" that a user cannot decompose.

The first public version uses transparent status classifications with the evidence
visible: Improving strongly, Improving, Broadly stable, Mixed, Deteriorating,
Deteriorating strongly.

*(Merge note: the engineering draft proposed a 0-100 percentile stress index. It is
dropped for v1. A composite number invites "what does 73 mean" and is harder to
defend than six bands with the components shown. Revisit only after the metric
layer is mature, and only if the bands prove insufficient.)*

## 2.3 Separate the four kinds of evidence

**Official data** (reported by an official source) · **Company Debt calculation**
(mathematically derived) · **Company Debt analysis** (interpretation across
indicators) · **Practitioner view** (insolvency practice experience).

Visually distinguishable. Never blurred.

## 2.4 Counts are not rates

Three-digit SIC data give insolvency **volumes**, not failure rates. Business
Insolvency Demography gives genuine rates but only at one-digit SIC section level.

**Allowed:** "Accommodation and food service activities had a broader-industry
insolvency rate of X per 10,000 businesses."
**Never:** "Restaurants had an insolvency rate of X per 10,000 restaurants."

## 2.5 One source of truth inside Company Debt

A number exists once. The same value feeds hero cards, key findings, tables,
charts, prose, comparison modules, hub tables and downloads.

The August 2026 failure where one page showed 44.0% in one block and 42% in
another must become **technically impossible**, not merely discouraged.

## 2.6 Revision aware by design

Official figures are provisional and get revised. Retain every source release,
detect revisions, never silently overwrite history, show significant revision
notes, keep source lineage.

## 2.7 Machine calculates, human interprets

Code calculates. AI may explain. AI must never be responsible for arithmetic.

AI must not: determine totals, calculate percentages, infer SIC codes, select
geography, copy values between page sections, or decide whether a mathematical
assertion is true.

## 2.8 No automated causation

The system may detect "insolvencies rose while fuel costs rose". It may never
assert "fuel costs caused insolvencies to rise".

Preferred: "Rising wage costs may help explain why pressure remains elevated."
Avoid: "Rising wage costs caused the increase."

---

# PART 3: VERIFIED GROUND TRUTH **[VERIFIED]**

Checked against this repository and primary sources, 14 August 2026. Three of these
change what is buildable.

## 3.1 What we already hold

Better than either draft assumed. The acquisition layer largely exists.

| Source | Module | Holds | Cadence | Granularity |
|---|---|---|---|---|
| Insolvency Service monthly | `scripts/parse_insolvency_data.py` | totals, procedures, rates, nations | monthly | E&W, procedure |
| Insolvency Service industry | `scripts/datahub/parse_sector_series.py` | **126 months to 2026-06**, all groups | monthly | 3-digit SIC |
| The Gazette | `scripts/datahub/sources/the_gazette.py` | notice counts by type; petition records | monthly | **national only** |
| Companies House | `scripts/datahub/sources/companies_house.py` | register counts, incorporations, dissolutions | monthly | national |
| ONS business population | `scripts/datahub/sources/ons_business.py` | business counts (Nomis) | annual | **SIC section** |
| Payment practices | `scripts/datahub/sources/payment_practices.py` | 96MB, payment terms by reporting company | biannual | **company level** |

Two are badly underused. The industry series holds **126 months of history for
every SIC group back to 2016**, enough for percentile and distribution work. The
payment practices bulk file is company-level and largely untouched; late payment is
a genuine upstream distress signal and we already have the data.

## 3.2 Gazette notices carry no company number **[VERIFIED — changes the design]**

`data/the-gazette/petitions_latest.json` holds 764 records for the latest month.
Each record has exactly three fields:

```json
{ "company_name": "…", "published": "2025-01-31", "notice_url": "https://…" }
```

No company number. No SIC code.

The product-definition draft's matching pipeline (its §20) assumes a company number
is present "where available", and its coverage metric counts "notices with company
number". In our data that count is always zero.

**Consequence:** sector-level petition counts cannot be produced from the Gazette
alone. The pipeline needs an additional fuzzy name-match stage:

```
Gazette notice → company_name → Companies House search → company number → SIC → sector
```

This is a name match on roughly 9,000 notices a year. It will produce false matches
on common and similar names. Mandatory design rules:

- Aggregate counts only. **Never publish a list of petitioned companies.**
- Publish the match rate on the page. If 71% match, say 71%.
- Unmatched notices are "unknown". Never distribute them pro rata.
- Never present a sector petition count as complete.
- Suppress below a floor of matched notices per sector per month. **Proposed floor: 10.**

## 3.3 Petitions lead only about 15% of insolvencies **[VERIFIED — missing from both drafts]**

A winding-up petition precedes a **compulsory liquidation**, which was 276 of 1,845
insolvencies in June 2026, about 15%. The dominant procedure is the CVL at 1,364,
about 74%, and **a CVL has no petition stage at all** — directors file it
themselves.

So petition activity is a leading indicator of one sixth of the market, and of the
creditor-enforcement route specifically. Still worth publishing: creditor
enforcement is the pressure a distressed director feels first. But every early
distress panel must carry, adjacent to the reading:

> Winding-up petitions lead court-ordered liquidations, which are about 15% of
> company insolvencies. Most insolvencies are creditors' voluntary liquidations,
> which have no petition stage.

Without that sentence the panel overstates its own reach.

## 3.4 We cannot yet detect connected-company clusters automatically **[VERIFIED]**

The record-level insolvency file carries an `is_bulk` flag that would make cluster
detection mechanical. **We do not hold that file.** Nothing under `data/` matches it.

Until it is ingested, cluster detection is a statistical outlier test plus reading
the official commentary, which is a human step. Acquiring the record-level file is
the highest-value single acquisition on this list.

## 3.5 Companies House rate limits are a non-issue **[VERIFIED — corrects the engineering draft]**

600 requests per five minutes is roughly 172,800 a day. At ~9,000 lookups a year
this never binds. The engineering draft wrongly listed it as an open question. It
is not a constraint and should not shape the design.

## 3.6 The connected real-estate cluster figures reconcile

Three figures are in circulation and they are consistent, not contradictory:

- ~200 connected companies across March and April 2026 (our real-estate pages)
- ~60 in June 2026 (our flagship dashboard)
- ~260 across March, April and June (the product-definition draft, matching the official total)

200 + 60 = 260. Same event, different windows.

But a reader comparing two of our pages has to do that arithmetic unaided. This is
precisely the case for a **stored anomaly record** (Part 8) rendered consistently
everywhere, rather than three hand-written sentences that happen to agree.

## 3.7 Honest scale assessment

Part 9's storage model is about fifteen relational tables plus an ETL layer, an
internal API and a QA framework. This is a software project measured in months, not
a content task. Phase 0 alone is most of it.

Half-building it would leave us worse off than today, because we would have two
sources of truth instead of one. **Either commit to Phase 0 properly or do not
start it.**

---

# PART 4: DATA SOURCES

## 4.1 Monthly company insolvency statistics

The core dataset. Ingest: total insolvencies; CVLs; compulsory liquidations;
administrations; CVAs; receiverships; insolvency rate; one-, two- and three-digit
SIC totals; historical monthly and annual values.

**Critical distinction:** headline monthly procedure totals may be seasonally
adjusted. Industry SIC data are **not**, and must never inherit the adjustment
label from the national procedure tables.

Detailed **sector procedure** breakdowns are published **quarterly**, not monthly.
Display "Latest available sector procedure mix: Q2 2026", never "June 2026
procedure mix".

Recent industry figures carry more unknown-SIC cases because industry for
compulsory liquidations is often recorded late. Every sector page states this.

## 4.2 Business Insolvency Demography

A methodologically distinct annual product: insolvency volumes and **rates**, by
industry, age, employment, turnover, size and location. Identifies businesses
through the IDBR and can combine several companies into one business.

Industry results are **one-digit SIC section only**. Preserve as a separate
statistical product. Never join it in a way implying granularity the source does
not support (see 2.4).

## 4.3 ONS business demography

Annual: active businesses, births, deaths, survival, by area and SIC group.
Business-population **context**, not insolvency data.

Never describe an ONS "business death" as an insolvency; deaths include closures
well beyond formal insolvency.

Useful framings: births falling while insolvencies stay elevated; deaths exceeding
births; five-year survival below the national average.

## 4.4 The Gazette

The UK's official public record. Publishes winding-up petitions (company notice
code 2450) and practitioner appointments, with linked-data representations
(JSON-LD, XML, RDF).

See **3.2** for the missing company number and **3.3** for the 15% limit. Both
constrain this source more than either draft assumed.

**[DECISION] Licensing.** Reading notices is public. **Bulk or systematic access
may not be**, and the matching pipeline is systematic. The Gazette sells a Data
Service separately. Establish permitted access, licensing, historical availability,
update frequency, permitted caching and redistribution rights **before** Phase 3.
This is a legal question, not an engineering one.

## 4.5 Companies House

Live company data via API. Use as an **enrichment and classification layer** for
aggregated sector intelligence: company number, registered name, SIC codes, status,
incorporation date, region.

Do not expose company-level risk profiles.

## 4.6 Payment practices **[addition]**

Neither draft included it. We hold 96MB of company-level statutory payment data
with a biannual cadence. Large-company payment terms lengthening is an upstream
distress signal for their suppliers, and it is one of the few datasets we hold at
company level with a legitimate publication basis.

Candidate for the operating-conditions layer (Part 7.3), not the insolvency layer.

## 4.7 Licensing

The long-run Insolvency Service dataset is Open Government Licence 3.0. Store
licence at **source** level; do not assume every dataset shares terms.

**Outstanding:** our pages assert OGL in their structured data but carry no visible
OGL attribution. Add it.

---

# PART 5: CANONICAL SECTOR TAXONOMY

A major proprietary asset. One canonical record per sector:

```yaml
sector_id: temporary_staffing
display_name: Temporary Staffing Agencies
seo_name: UK Temporary Staffing Agency Insolvency Statistics
official_name: Temporary employment agency activities
primary_sic: ["782"]
sic_level: group
parent_section: "N"
parent_division: "78"
geography: England and Wales
included_activity: [temporary employment agencies]
excluded_activity: [permanent recruitment agencies]
peer_group: employment
related_sectors: [recruitment_agencies]
context_indicators: [vacancies, temp_billings, hiring_intentions]
tier: A
status: active
methodology_notes: …
```

Required: internal ID, display name, official statistical name, SEO name, SIC codes
and level, parent section and division, inclusion and exclusion wording, peer group,
related sectors, context indicators, publication tier, status, methodology notes.

Where a public sector spans multiple SIC codes, state each constituent code, the
aggregation rule, and why aggregation is appropriate. **No component may be counted
twice.**

## 5.1 Publication tiers

| Tier | Treatment |
|---|---|
| **A — Full intelligence** | Full page, commentary, operating indicators, practitioner insight |
| **B — Data sector** | Full statistical record and comparisons, minimal editorial |
| **C — Taxonomy only** | Included in parent calculations, no standalone page |

This is how coverage scales without producing hundreds of thin pages. A sector can
exist in the monitor without a landing page. Eventually the monitor should cover
most meaningful three-digit groups.

## 5.2 Peer groups

Employment (recruitment, temporary staffing) · Hospitality (restaurants, hotels,
pubs) · Logistics (road haulage, freight forwarding) · Professional services (IT
consultancy, management consultancy, architectural and engineering) · Leisure
(sports facilities, creative arts, amusement and recreation) · Property (letting and
investment, estate agency, property trading).

Membership lives in the taxonomy.

## 5.3 Sector expansion

Score candidates on: statistical definability, case volume, commercial relevance,
public interest, contextual richness, peer-network value.

**Do not add a sector because a keyword tool shows 50 searches.**

---

# PART 6: METRIC DICTIONARY

Defined once, computed once, labelled identically everywhere.

| Metric | Definition |
|---|---|
| Latest month | Most recent month, flagged provisional |
| YTD | Jan to latest month, vs same months prior year |
| Rolling 12m | Latest 12 months vs preceding 12 |
| Recent 3m | Latest 3 complete months vs same 3 a year earlier |
| vs 2019 | Latest **complete** year against 2019 |
| Parent share | Sector ÷ parent, identical period and geography |
| Rank in parent | Position by the stated measure, of N |
| Parent relative | Sector change minus parent change, in percentage points |
| Momentum delta | Rolling change minus YTD change |
| Percentile | Rolling 12m against that sector's own history |
| Section rate | Business Insolvency Demography, per 10,000, section level only |

**Rounding:** one decimal place for percentages, applied consistently. The
recruitment page currently rounds inconsistently; the dictionary fixes it.

Every displayed metric carries a `metric_id`.

---

# PART 7: THREE ANALYTICAL SYSTEMS

Kept separate. Never averaged into one number.

## 7.1 Insolvency momentum

*What are completed insolvencies doing?* Source: official sector counts. The
strongest and most reliable layer. Metrics per Part 6.

## 7.2 Early distress

*Are signs building before they reach completed insolvencies?* Source: Gazette
petitions and selected notices, subject to 3.2, 3.3 and 4.4.

Must stay separate from completed insolvencies. The contradiction is the
information:

> Completed insolvencies: improving
> Winding-up petition activity: deteriorating

That must never be hidden inside an average.

**Never** display `petitions + insolvencies = total distress events`. Gazette
publication timing and Companies House registration differ; the counts are not
additive.

## 7.3 Sector operating conditions

*What conditions are businesses facing?* Three to six researched indicators per
sector. **No universal generic list.** Each indicator gets a registry record:

```yaml
indicator_id: road_diesel_price
name: UK road diesel pump price
sector: road_haulage
source_type: official
frequency: weekly
publication_lag: low
direction: { increase: pressure }
role: operating_cost
geography: UK
licence: OGL
active: true
```

Activate only where the sector relationship is clear, the source reliable, the
frequency useful, the geography compatible, history exists, and it adds information
beyond the insolvency series.

---

# PART 8: STATUS, LEVEL AND ANOMALY

## 8.1 Status classification

Calculated from **insolvency data only**. Do not make it depend on external
indicators until those systems are mature.

Primary inputs: rolling 12-month change (greatest weight), YTD change, recent
three-month comparison (supporting).

| Status | Rule |
|---|---|
| Improving strongly | Both primary ≤ -15%, sufficient volume, no invalidating anomaly |
| Improving | Both primary ≤ -5% |
| Broadly stable | Both between -5% and +5% |
| Mixed | Primary measures point materially different ways |
| Deteriorating | Both primary ≥ +5% |
| Deteriorating strongly | Both ≥ +15%, sufficient volume, no invalidating anomaly |

**Thresholds must be backtested across the historical sector-month dataset before
public launch.** We hold 126 months × ~270 groups, which is ample. The aim is
classifications that stay understandable and defensible, not mathematically
impressive ones.

## 8.2 Volume confidence

| Band | Rolling 12m count |
|---|---|
| Higher confidence | ≥ 200 |
| Moderate | 50–199 |
| Low volume | < 50 |

For low-volume sectors: no "strongly" classifications; show absolute changes beside
percentages; add a volatility note; de-emphasise latest-month movements.

Six to nine cases is +50% and carries nothing like the weight of 600 to 900.

## 8.3 Longer-term level, separate from momentum

A sector can improve fast and still sit in a historically bad position. Show both:

> **Current momentum:** Improving
> **Longer-term level:** Still elevated

Bands against 2019: Well below · Below · Near · Above · Well above.

## 8.4 Parent comparison and rank

Compute `sector change - parent change` on both YTD and rolling. Compute
`sector ÷ parent` for the identical period. Compute rank of N among groups in the
parent.

**Never hard-code a superlative into editorial text.** Render
`{{sector.parent_rank_label}}`. Hard-coding "the largest single trade" is exactly
what produced the August real-estate error, where a page claimed to be largest at
37% when it was second at 22.7%.

## 8.5 Anomaly detection

Ask every month: *is this number unusual enough that users should not read it
normally?*

Types: volume anomaly · connected-company cluster · procedure anomaly ·
classification revision · source revision · denominator distortion (large percentage
on tiny counts).

Candidate rule, robust to outliers:

```
robust_z = 0.6745 × (latest - trailing_median) ÷ median_absolute_deviation
```

Flag where |robust_z| exceeds a calibrated threshold **and** the absolute case
movement exceeds a minimum count.

**An algorithm firing does not publish an anomaly.** It creates a review candidate.
Only a human, with the official commentary in hand, may write the causal sentence.

## 8.6 Official commentary override

Where the official source identifies an event, store it:

```yaml
anomaly_type: connected_company_cluster
verified_by: Insolvency Service
affected_sector: real_estate
periods: [2026-03, 2026-04, 2026-06]
approx_companies: 260
breakdown: { "2026-03+04": 200, "2026-06": 60 }
```

Every page touching that sector then renders the same caveat from the same record,
which is what would have prevented three differently-worded sentences (3.6).

## 8.7 Trend reversal detection

Store status by release so the system can say "first deterioration signal since
October 2025". Transitions worth flagging: Improving → Mixed, Mixed →
Deteriorating, Deteriorating → Improving.

---

# PART 9: DATA ARCHITECTURE

## 9.1 The rule

**Every number appearing anywhere must be read from the release model. No figure may
be typed into prose.** Where prose needs a number it interpolates a named field;
where it needs a comparison it interpolates a computed claim.

## 9.2 Global release pointer

The single most important engineering requirement. The whole site refers to
`current_insolvency_release_id`. A new release imports to staging; the pointer moves
**only after all QA passes**; hub, dashboard and every sector page switch together.

This makes the August state — hub on May while the dashboard was on June — structurally
impossible rather than merely detectable.

## 9.3 Storage model

Append-only wherever possible. Core tables:

`source_release` (release_id, source, title, release_date, period_end, retrieved_at,
source_url, file_hash, licence, provisional, parser_version) ·
`source_file` (file_id, release_id, filename, mime_type, sha256, archive_location) ·
`sic_taxonomy` (sic_code, level, official_name, parent_code, effective_from/to) ·
`sector` (sector_id, slug, display_name, statistical_name, parent_id, geography, tier, active) ·
`sector_sic_mapping` (sector_id, sic_code, mapping_type, inclusion_note, effective_from) ·
`insolvency_observation` (observation_id, release_id, period, geography, sic, procedure, value, adjustment_status, provisional, source_table, source_row) ·
`derived_metric` (metric_id, sector_id, release_id, metric_type, value, numerator, denominator, formula_version) ·
`sector_signal` (sector_id, release_id, momentum_status, longer_term_status, confidence, methodology_version) ·
`anomaly` (anomaly_id, sector_id, release_id, type, severity, automated_flag, review_status, evidence) ·
`context_indicator` / `context_sector_mapping` / `context_observation` ·
`gazette_notice` (notice_id, notice_code, company_name, company_number, publication_date, sector_id, match_method, match_confidence) ·
`claim` (claim_id, release_id, sector_id, claim_type, rendered_text, source_metric_ids, reviewer, status) ·
`qa_result` (release_id, test_id, severity, status, details).

Note `gazette_notice.match_method`: an addition, because per 3.2 matching is by name,
not number, and the method must be recorded per notice.

## 9.4 Never overwrite history

When July restates June, retain June-as-first-reported, June-as-revised, and the
current canonical value. This enables a public revision log.

## 9.5 Raw source archive

Retain every original input file with download date, source URL, release, hash and
parser version. Do not depend on a government URL persisting. Subject to licence
terms.

---

# PART 10: INGESTION WORKFLOW

1. **Detect** new official publication
2. **Archive** source files with URL, timestamp, size, SHA-256
3. **Parse** into structured data
4. **Validate source schema** — sheets, columns, period, table names, row labels, SIC codes
5. **Load staging** — no public change
6. **Calculate** every derived metric
7. **Compare** against previous release, same period last year, history
8. **Revision check** — identify changes to published periods
9. **Anomaly check** — generate review candidates
10. **Narrative draft** — AI drafts from approved structured facts only
11. **Human review** — anomalies, unusual movements, causal wording
12. **QA** — run all automated tests
13. **Atomic publish** — switch the global release pointer
14. **Post-publish validation** — crawl every product page, compare displayed values against the database

## 10.1 Schema change behaviour

If the source changes a sheet name, table structure, category label or layout, the
importer **stops**. Never guess. Never silently map a new column to an old field.

## 10.2 Failure behaviour

**Never partially publish.** Keep the previous complete release live. Alert
internally. The public page keeps saying "Data through June 2026". Never display
"Updated August 2026" over June values.

---

# PART 11: QA FRAMEWORK

Every test blocks publication on failure.

**Arithmetic:** `YTD = sum(monthly)`; `rolling_12 = sum(latest 12)`;
`parent_share = sector ÷ parent`; `pct_change = (current - comparison) ÷ comparison`;
`sum(sector) = parent total`.

**Direction:** if `current > previous` the rendered direction cannot say "down", and
vice versa. Trivial-sounding, explicitly tested.

**Content consistency:** every displayed metric carries a `metric_id`; rendered value
must equal canonical value. Do not regex for duplicate percentages across
hand-written paragraphs if the architecture removes the duplication.

**Geography:** every metric has a geography field; components declare accepted
geography; a component headed "UK" receiving England and Wales fails the build or
relabels.

**Period:** comparison windows generated automatically. Prevents Jan–Jun 2026 vs
Jan–May 2025, rolling vs calendar year, June data under a May label.

**SIC:** validate codes, verify no overlap, verify parent, confirm mapping active,
confirm scope explanation exists.

**Parent share:** `0 ≤ share ≤ 1`, numerator and denominator sharing period,
geography and methodology.

**Ranking:** largest, smallest, fastest, highest, lowest, only, record, peak — all
must derive from structured calculation. Not permitted in hard-coded copy without a
deliberately approved exception.

**Historical claims:** "highest since 2016" must carry metric, comparison period,
evaluated history and start year, and be reproducible by the test engine.

**Release freshness:** every page exposes source publication, period, publication
date and release ID; the audit verifies all pages share the current release.

## 11.1 What exists today **[VERIFIED]**

`scripts/datahub/check_derived_values.py` already implements the parent-share and
ranking tests against the live series, and exits non-zero. On its first run it found
two stale values a careful human reviewer had missed. It is the seed of this
framework, not a placeholder.

---

# PART 12: AI RULES

**AI may:** draft "what changed" explanations; summarise a series; suggest
comparisons; draft plain-English methodology; draft sector interpretation from
approved context; identify possibly contradictory prose; suggest contextual sources
for human approval.

**AI may not:** calculate; alter source data; determine release completeness; select
a SIC code from memory; invent missing values; publish automatically; state
causation from correlation; describe a figure as current without release metadata.

## 12.1 Structured input, always

Never ask "update the restaurant page for June". Supply the facts and ask only for
interpretation:

```yaml
sector: restaurants
latest_period: 2026-06
ytd: { current: 1011, previous: 1078, change_pct: -6.2 }
rolling_12: { current: 2070, previous: 2171, change_pct: -4.7 }
status: improving
long_term: { baseline_year: 2019, change_pct: … }
parent: { status: …, relative_pp: … }
anomalies: []
approved_context: [ … ]
```

This is a fundamental architecture change, and it is what makes the editorial layer
safe.

## 12.2 Evidence ledger

Every non-trivial sentence traceable:

```yaml
claim_id: REST-2026-07-004
text: Restaurant insolvencies are falling on both YTD and rolling measures.
type: analysis
evidence: [metric:ytd_change, metric:rolling12_change]
methodology_version: 1.0
```

Machine-readable editorial provenance is unusual and defensible.

---

# PART 13: INFORMATION ARCHITECTURE

Seven areas: `/data/` hub · `/data/uk-insolvency-statistics/` national dashboard ·
sector intelligence pages · procedure intelligence · sector comparison tool · monthly
intelligence report · methodology and dataset centre.

## 13.1 Hub

A. National status · B. What changed this month (3–6 findings) · C. Sector monitor
(sortable) · D. Fastest deterioration · E. Fastest improvement · F. Unusual events ·
G. Compare industries · H. Procedure monitor · I. Data and methodology.

## 13.2 Sector monitor

| Sector | Status | YTD | YTD change | Rolling 12m | Rolling change | vs 2019 | Parent comparison |

Sortable by all columns. Later filters: parent industry, size, status, geography,
procedure. Server-rendered so it is readable without JavaScript and citable by a
machine.

**Keep "fastest deterioration" (relative movement) separate from "most
insolvencies" (raw volume).** A large sector can produce far more insolvencies
without the fastest deterioration.

## 13.3 Sector page

Title · scope line (England and Wales) · current reading · explanation · four hero
cards (current year, underlying trend, longer-term stress, relative performance;
a fifth for early distress when production-ready) · what changed in the latest data ·
core chart · parent and peer comparison · early distress (with 3.3 caveat and match
rate) · operating conditions · what to watch next · procedure mix (quarterly) ·
business demography context · practitioner insight · how to interpret · methodology
and sources · cite and download.

**"What changed" compares this release with the last Company Debt release**, not
merely restating the hero. That gives returning users a reason to return.

## 13.4 Dashboard hierarchy

Replace the four primary tiles with: latest month, YTD vs same period, rolling 12m
vs preceding 12m, rolling rate. Procedure mix moves immediately below.

## 13.5 Geography labels

Keep "UK" in an H1 where the page genuinely covers the nations. Make every
statistical heading exact: "Latest company insolvency figures for England and
Wales"; "Company insolvencies by sector: England and Wales". Keep the dedicated UK
nations comparison as the only place "UK" heads a table.

## 13.6 Comparison module

Up to four sectors. Views: raw counts, percentage change, index (start = 100),
relative to 2019. Always state what has been normalised.

## 13.7 Front-end principles

Fast (core answer above the fold) · dense but understandable (closer to FT data
presentation than a marketing article) · mobile-friendly (tables collapse
intelligently) · accessible (charts need data tables or text alternatives) ·
printable · stable (no gratuitous animation) · serious (avoid warning lights;
"deteriorating" is not "crisis").

Status signalling never relies on colour alone: text, icon and direction together.

---

# PART 14: PROVENANCE, REUSE AND DISCOVERY

Every chart: PNG, CSV, copy data, cite. Exported images carry Company Debt, title,
period, geography, source and update date. Avoid decorative infographics that lose
statistical context when shared.

Every sector offers a CSV: period, sector, SIC, geography, insolvencies, yoy change,
rolling 12, rolling change, source release, provisional. The hub offers the full
sector monitor.

Citation utility on every page, with copy-citation, copy-source-link,
download-data and copy-chart.

`Dataset` structured data with name, description, creator, temporal and spatial
coverage, update date, licence, distributions and variables measured. **Do not
publish structured metadata for anything a user cannot actually see or download.**

Stable dataset URLs: `/data/datasets/…`, `/data/methodology/`, `/data/revisions/`.
Historical snapshots separately addressable.

## 14.1 Public revision log

Date, sector, old figure, new figure, source, whether source revision or Company
Debt correction, affected pages. Publishing corrections builds more trust than
never appearing to make any.

---

# PART 15: TECHNICAL ARCHITECTURE

```
Official sources → Python ETL / validation → canonical store →
metrics + signals engine → Company Debt data API →
WordPress intelligence components → pages / hub / downloads
```

**WordPress handles:** URLs, editorial commentary, templates, SEO, navigation,
user-facing components, commercial CTAs.

**WordPress does not handle:** parsing government workbooks, rolling totals,
anomaly algorithms, revision detection.

Internal API from the start, versioned `/v1/` even while private:
`/releases/latest`, `/releases/{id}`, `/sectors`, `/sectors/{slug}`,
`/sectors/{slug}/{summary|series|signals|context}`, `/compare`, `/procedures`,
`/revisions`. Parameters: period, from, to, metric, geography, release_id.

Never let WordPress presentation details become the public data contract.

Relational storage is appropriate. Keep identifiers, storage interfaces and API
independent enough that Gazette volume can later move to its own database without
changing public URLs.

---

# PART 16: OUTPUTS

## 16.1 Monthly intelligence report

Permanent URL per month. National position · five things that changed ·
fastest-rising · fastest-falling · trend reversals · unusual events · procedure
changes · early warning · what we watch next month.

Feeds newsletter, LinkedIn, press outreach, journalist briefings, internal
practitioner briefing and homepage. **One dataset, one editorial workload, many
outputs.**

Candidates are machine-ranked by magnitude, absolute case movement, status change,
historical significance, anomaly and sector importance. **An editor chooses the
five that matter and writes the opening.** That is the line between a data product
and an automated content mill, and it is where the Company Debt voice lives.

## 16.2 Alerts

Follow a sector. Options: monthly update, status change only, significant movement.
Data-first content: status, YTD, rolling, what changed, early warning, what to
watch, link.

## 16.3 Press engine

Press-ready table after each release, every statement already supported by the data
model. Greatly reduces risk in reactive press work.

---

# PART 17: THE HUMAN LAYER

## 17.1 Practitioner insight

Retain one genuinely useful human layer per Tier-A sector: how cash pressure
develops, which liabilities accumulate, what healthy turnover can hide, what
directors should watch, why acting earlier widens the options.

Sector-specific, short, **reviewed by a licensed practitioner**, clearly marked as
practitioner experience. Never masquerading as a statistical finding.

**[DECISION] Outstanding now.** Existing practitioner blocks need either a named
practitioner's sign-off, recorded in the repo, or rewriting as neutral operational
analysis. This blocks nothing else but should not drift.

## 17.2 Do not pretend anecdotes are data

Until a structured internal sample exists: "in our experience", never "the data
shows".

## 17.3 Future internal case dataset

Phase 4 or later. Anonymised dimensions: sector, turnover band, employee band,
primary debt type, HMRC debt, cash-flow status, procedure outcome, time from first
distress to instruction.

If ever incorporated: aggregate only, suppress low counts, never identifiable,
privacy and legal review, published sampling methodology, kept separate from
national population statistics.

## 17.4 Commercial transition

Near the bottom. "Sector conditions may be improving while an individual company is
still insolvent", then cash-flow and balance-sheet insolvency, HMRC arrears, rescue
options, liquidation where appropriate.

Avoid contaminating the intelligence experience with aggressive lead generation.
**Trust is part of the product.**

---

# PART 18: OPERATIONS

## 18.1 Source registry

| Source | Frequency | Latest period | Latest fetch | Status |
|---|---|---|---|---|

Immediate view of stale inputs.

## 18.2 Operational dashboard

Current release · latest official release detected · pages current (n/n) · critical
QA errors · warnings · source revisions · status changes · anomalies for review ·
stale context sources.

## 18.3 Health alerts

Source release appears · import fails · schema changes · critical QA fails · a
public page does not match the API · a context dataset goes stale · a source URL
disappears · Gazette match rate drops materially.

## 18.4 Human review queue

The editor should not inspect 20 pages monthly. Surface only judgement:

**Critical:** schema changed, major revision, unusual anomaly.
**Review required:** status changed, new peak or trough, unusual movement, AI-suggested causal explanation.
**Automatic:** ordinary number refresh, tables, hero cards, charts, share calculations.

## 18.5 Editorial release checklist

What actually changed? Is anything statistically unusual? Did an official source
explain an anomaly? Is a classification misleading despite being mathematically
correct? Are the context indicators still relevant? Is any causal language too
strong? Does a practitioner observation add something? Is there a national story?

**The human should never spend time copying figures between paragraphs.**

## 18.6 Methodology versioning

`momentum_methodology_version = 1.0`, incremented on change, documenting what
changed, why and when. Store both status-as-published-at-the-time and
status-recalculated-under-current-methodology, so methodology can evolve without
rewriting history.

---

# PART 19: BUILD SEQUENCE

## Phase 0 — Lock the statistical foundation

Canonical sector taxonomy · source archive · release model · database · importer ·
calculation library · QA framework · global release pointer.

**Success condition:** every existing sector statistic can be recreated
automatically, and no page can display a figure absent from the release model.

Nothing more sophisticated precedes this. Per 3.7, this is the bulk of the
engineering.

## Phase 1 — Intelligence MVP

All current sectors · sector monitor · momentum classification · longer-term status ·
parent comparison · peer comparison · what changed · charts · CSV · cite-this-data ·
revision history · monthly report.

This alone transforms the current hub.

## Phase 2 — Operating conditions

Per Tier-A sector: research three to six indicators, build the registry, ingest,
add "what to watch" and the context dashboard. Sector by sector. **Never a generic
economic template.**

## Phase 3 — Early distress

**Only after the licensing decision in 4.4.** Ingest notices · name-match stage
(3.2) · Companies House enrichment · SIC matching · coverage calculation · petition
trend · display with the 15% caveat (3.3) · alerts.

Run privately first and test whether the signal historically leads completed
insolvency movements. If it does not lead, do not publish it as a leading indicator.

## Phase 4 — Proprietary internal data

Anonymised enquiry patterns, debt composition, sector case signals, structured
practitioner observations. Where the product moves from excellent interpretation of
public data toward unique primary intelligence.

## Phase 5 — External data product

Documented public API, embeddable charts, licensing, bespoke reports, partner
feeds. **Do not start here.**

## Sector expansion

Runs alongside from Phase 1 using tiers (5.1), not as a separate phase. Adding
Tier-A pages before Phase 0 multiplies the maintenance cost of the error class we
fixed twice in August.

---

# PART 20: MVP DEFINITION

The product earns the name **Insolvency Intelligence** when a user can:

1. see all supported sectors together
2. immediately identify improvement or deterioration
3. understand why a status was assigned
4. compare sectors
5. see historical context
6. identify unusual events
7. see what changed since the last release
8. download the data
9. trace every statistic to its source
10. trust that every page uses the same release

It does **not** need Gazette data or predictive modelling to launch.

---

# PART 21: PRIORITY TICKETS

**P0:** canonical source ingestion · release versioning · sector taxonomy · central
metric engine · atomic release publishing · page consistency tests · revision
detection

**P1:** sector monitor · signal classification · comparison API and UX · what-changed
engine · downloadable data · citation utility · dataset metadata

**P2:** context source registry · context ingestion · sector indicator components ·
monthly report automation

**P3:** Gazette licensing decision · Gazette ingestion · name-match stage ·
Companies House enrichment · early distress model

---

# PART 22: RELEASE QA CHECKLIST

- [ ] Official release identified; period and geography verified
- [ ] Source files archived; hashes stored
- [ ] Parser completed with no schema warnings
- [ ] All target SIC codes present
- [ ] YTD, rolling and parent calculations validated
- [ ] Historic revisions identified and logged
- [ ] Rankings and statuses recalculated
- [ ] Low-volume rules applied
- [ ] Anomalies reviewed by a human
- [ ] "What changed" reviewed and opening written
- [ ] All public pages carry the new release ID
- [ ] Hub matches sector pages
- [ ] Downloads and chart values match the database
- [ ] Citation metadata and structured data updated
- [ ] Post-publish crawl passed

---

# PART 23: FIRST PRODUCTION TEST — 18 AUGUST 2026

The July 2026 release publishes **18 August 2026 at 09:30**, four days from
writing. Phase 0 will not exist by then. The achievable test is smaller and still
worth running:

1. Ingest July through the current pipeline
2. Run `check_derived_values.py` against the refreshed series **before anything publishes**
3. Record every stale hand-written value it catches
4. Record every value it misses that a human then finds
5. Do not publish automatically

That measures how much of the QA framework we actually need, against a live
release rather than a hypothetical one. The count of misses is the argument for
Phase 0 funding, or against it.

---

# PART 24: SUCCESS MEASURES

**Trust:** published numerical errors (target: zero), correction frequency, source
coverage, QA failures.
**Freshness:** time from official release to complete update; percentage of pages on
the current release.
**Usefulness:** repeat visits, comparison-tool use, chart interaction, downloads,
alert subscriptions.
**Authority:** citations, backlinks, journalist references, dataset links, branded
searches for Company Debt data.
**Commercial:** assisted enquiries, intelligence-to-service journeys, qualified
consultations.

**Do not optimise commercial conversion at the cost of data credibility.**

Product analytics tracked separately from content analytics: `sector_view`,
`compare_open`, `compare_sector_added`, `chart_period_changed`, `csv_download`,
`citation_copy`, `methodology_open`, `alert_signup`, `related_sector_click`,
`commercial_cta_click`.

---

# PART 25: OPEN DECISIONS **[DECISION]**

1. **Gazette licensing.** Reading notices is public; systematic bulk matching may not be. Legal review required before Phase 3. **Blocking for that phase only.**
2. **Practitioner sign-off.** Does a named licensed practitioner sign the practitioner blocks, or do they become neutral analysis? Outstanding now.
3. **Phase 0 commitment.** Months of engineering (3.7). Committing halfway is worse than not starting.
4. **Record-level file.** Acquire it for `is_bulk` cluster detection (3.4)? Highest-value single acquisition.
5. **Monthly bulletin ownership.** Who writes the human half, and by when each month?
6. **Scotland and Northern Ireland.** Detailed sector data is England and Wales. Is that permanent scope, or a stated limitation to revisit?

---

# PART 26: THE STRATEGIC POSITION

The moat is not the government data. Anyone can download today's spreadsheet.

The moat is the intelligence architecture around it, and it compounds monthly: a
cleaned historical sector database, revision history, sector mappings, peer
relationships, methodology, historical status classifications, anomaly annotations,
early-distress series, operating-condition mappings, sector narratives, practitioner
observations, citation infrastructure and user preferences.

A competitor can download the spreadsheet. It cannot instantly recreate years of
that.

## The standard

A director understands the situation in **30 seconds**. An analyst can investigate
it for **30 minutes**. A journalist can **cite it**. A search engine can
**understand it**. And every number survives an audit back to its original source.
