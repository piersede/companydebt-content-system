# Company Debt Insolvency Intelligence: product specification

Status: draft for review. Written 14 August 2026.
Supersedes nothing. Nothing in this document has been built yet.

This spec turns the "insolvency intelligence" proposal into something buildable:
every data source, every metric, the stress methodology, the page design, what a
machine does, what a human must do, and the order to build it in.

It is deliberately opinionated about what we should NOT do, because two of the
proposed features cannot be built as described and a third can only be built with
a caveat that changes how it must be presented.

---

## 1. What the product is

A continuously updated view of financial stress across UK industries, where the
official statistics are the raw material and Company Debt's interpretation is the
product.

The test for every feature: **would a journalist cite it, and would a director
change a decision because of it?** If neither, it is decoration.

The five questions each sector must answer:

| Question | Today | Target |
|---|---|---|
| How many companies are failing? | Strong | Keep |
| Is it improving? | Strong | Keep, add momentum |
| Better or worse than other sectors? | Partial | Core |
| Are conditions about to worsen? | Absent | Core, with honest limits |
| Why, and what should I watch? | Manual | Structured |

---

## 2. Constraints that shape everything

These are findings from the existing data layer, not opinions. Read this section
before designing anything, because three of them kill or reshape a proposed
feature.

### 2.1 Winding-up petitions lead only 15% of insolvencies

The proposal treats Gazette petition volume as a general early-warning signal.
It is not. A petition precedes a **compulsory liquidation**, which was 276 of
1,845 insolvencies in June 2026, about 15%. The dominant procedure is the CVL at
1,364, about 74%, and a CVL has **no petition stage at all**. Directors file it
themselves.

So petition activity is a leading indicator of one sixth of the market, and of the
creditor-enforcement route specifically. It is still worth publishing, because
creditor enforcement is exactly the pressure a distressed director feels first.
But it must be labelled as what it is:

> Winding-up petitions lead court-ordered liquidations, which are about 15% of
> company insolvencies. Most insolvencies are creditors' voluntary liquidations,
> which have no petition stage.

A panel headed "early warning" without that sentence would be misleading.

### 2.2 Gazette notices carry no company number and no SIC code

`data/the-gazette/petitions_latest.json` holds 764 records for the latest month,
each with exactly three fields: `company_name`, `published`, `notice_url`.

There is no company number and no industry code. **Sector-level petition counts
therefore cannot be produced from the Gazette alone.** The proposed "winding-up
activity in this sector" panel does not currently have the data behind it.

It is buildable, via a join: Gazette company name → Companies House search →
company number → SIC code. We already hold a working Companies House client. But
this is a fuzzy name match on roughly 9,000 notices a year, and it will produce
false matches on common and similar names. That is acceptable for an aggregate
trend and unacceptable for naming an individual company.

Design consequences, all mandatory:
- Publish only aggregate counts, never a list of petitioned companies.
- Publish the match rate on the page. If we match 71% of notices to a SIC code, say so.
- Treat unmatched notices as unknown, never distribute them pro rata across sectors.
- Never present a sector petition count as complete.
- Below a floor of matched notices per sector per month, suppress rather than publish noise. Proposed floor: 10.

### 2.3 Business Insolvency Demography is section level only

It gives a properly constructed rate per 10,000 businesses, but at one-digit SIC
section. Our trade pages are three-digit groups. We can therefore write:

> Accommodation and food service activities had an official insolvency rate of X
> per 10,000 businesses in 2025. This is the broader section, not a restaurant rate.

We can never write "restaurant insolvency rate: X per 10,000 restaurants". The
denominator for that does not exist in any published source.

The same limit applies to the ONS business population we already hold
(`data/ons-business/business_population.json`, from Nomis, by section).

### 2.4 We cannot currently detect connected-company clusters automatically

The record-level insolvency file carries an `is_bulk` flag, which would let us
detect and strip bulk events mechanically. **We do not hold that file.** Nothing
under `data/` matches it.

Until we ingest it, cluster detection is statistical inference (an outlier test)
plus reading the Insolvency Service commentary, which is a human step. Acquiring
the record-level file is the single highest-value data acquisition on this list,
because it turns the real-estate correction from hand-written prose into a
computed field.

### 2.5 What we already have

Better than assumed. The acquisition layer largely exists:

| Source | Module | Holds | Cadence | Granularity |
|---|---|---|---|---|
| Insolvency Service monthly | `parse_insolvency_data.py` | totals, procedures, rates, nations | monthly | E&W, procedure |
| Insolvency Service industry | `parse_sector_series.py` | 126 months to 2026-06, all groups | monthly | 3-digit SIC |
| The Gazette | `sources/the_gazette.py` | notice counts by type, petition records | monthly | national only |
| Companies House | `sources/companies_house.py` | register counts, incorporations, dissolutions | monthly | national |
| ONS business population | `sources/ons_business.py` | business counts | annual | SIC section |
| Payment practices | `sources/payment_practices.py` | 96MB, payment terms by reporting company | biannual | company level |

Two of these are badly underused. The industry series has **126 months of history
for every SIC group**, which is enough for percentile-based scoring. The payment
practices bulk file is company-level and largely untouched.

---

## 3. Data architecture: the canonical release object

This is the fix for the class of error found twice in August 2026: a page stating
two different values for the same thing because one came from the data and the
other was typed by hand.

### 3.1 The rule

**Every number that appears anywhere on a page must be read from one release
object. No figure may be typed into prose.**

Where prose needs a number, it interpolates a named field. Where prose needs a
comparison ("the largest trade in its section"), it interpolates a computed claim,
never a hand-written assertion.

### 3.2 Shape

One JSON object per monthly release, at
`data/releases/<YYYY-MM>/release.json`, immutable once published:

```
release:
  meta:      period, publication_date, next_release_date, geography,
             source_urls, vintage_hash
  headline:  total, by_procedure{}, rate_per_10k, rolling_12m, prior_12m
  sectors:   { "<sic>": {
                 label, parent_section, parent_division,
                 ytd, ytd_prior, ytd_change_pct,
                 rolling_12m, prior_12m, rolling_change_pct,
                 annual{2016..2025}, vs_2019_pct,
                 share_of_parent_pct, rank_in_parent, parent_total,
                 monthly[126],
                 stress{} , flags[]
             } }
  signals:   petitions{national, by_sector{}, match_rate}, ch_flows{}
  anomalies: [ {sector, kind, severity, evidence, human_note} ]
```

`vintage_hash` matters: the Insolvency Service revises history, and a chart
regenerated from a later vintage will not match a screenshot taken earlier. The
hash lets us say which vintage a published figure came from.

### 3.3 Assertions that block a publish

Extend `scripts/datahub/check_derived_values.py`, which already recomputes shares
and ranking claims, to a full assertion suite. Any failure exits non-zero and
blocks the push:

- every share quoted in prose equals the computed share, within rounding
- `sum(sector ytd) == parent ytd` for every parent
- superlatives ("largest", "only riser", "fastest falling") match the computed ranking
- no figure appears on a page that is absent from the release object
- month labels on the page match `meta.period`
- rolling windows are the same length on both sides of any comparison
- a page's vintage_hash matches the current release

That check already found two stale values in its first run that a careful human
reviewer had missed. This is the highest-value engineering on the list.

---

## 4. Metric dictionary

Every metric defined once, computed once, labelled the same way everywhere.

| Metric | Definition | Why |
|---|---|---|
| YTD | Jan to latest month, current year vs same months prior year | Removes seasonality, still recent |
| Rolling 12m | Latest 12 months vs preceding 12 | Best underlying direction |
| Momentum | Rolling change minus YTD change | Positive = improving faster recently |
| vs 2019 | Latest full year against 2019 | Distance from the last normal year |
| Share of parent | Sector YTD / parent YTD | Composition, and it moves |
| Rank in parent | Position by YTD | Backs every superlative |
| Percentile | Rolling 12m against that sector's own 126-month history | "How unusual is this for this trade" |
| Section rate | Business Insolvency Demography, per 10,000 | Only at section level, always labelled |

Rounding: one decimal place for percentages, stated to that precision everywhere.
The recruitment page currently rounds inconsistently; the dictionary fixes it.

---

## 5. Sector Stress: methodology

The proposal rightly says this must not be a mysterious score. The guard against
that is arithmetic simplicity and full inspectability.

### 5.1 Components

Five components, each scored 0 to 100, where higher means more stress.

| Component | Input | Scoring |
|---|---|---|
| Level | Rolling 12m as percentile of that sector's own 126-month history | Direct percentile |
| Direction | Rolling 12m change | Mapped: -20% or better = 0, +20% or worse = 100 |
| Momentum | Rolling change minus YTD change | Same mapping, narrower band |
| Distance from normal | Latest full year vs 2019 | 0% = 0, +100% or more = 100 |
| Enforcement | National petition trend, sector where match rate allows | Direct percentile |

Index = mean of available components. **If a component is unavailable, it is
dropped and the divisor changes.** It is never imputed, and the page states how
many components fed the score.

### 5.2 Bands

| Score | Label |
|---|---|
| 0-24 | Improving |
| 25-44 | Easing |
| 45-59 | Mixed |
| 60-79 | Deteriorating |
| 80-100 | Under acute pressure |

### 5.3 Rules that keep it honest

- Every component reading is shown next to the score. No black box.
- The score describes **the sector's insolvency statistics**, not any company's risk. The page must say: this is not a prediction about your company.
- Small sectors: below 100 insolvencies a year, publish components but suppress the composite. Percentage moves on tiny counts are noise, and medical/dental already shows why.
- A bulk-event flag suppresses the Level and Direction components for that month rather than letting one cluster spike the index.
- The methodology page shows the formula and links the code.

### 5.4 What it must never become

A company-level risk score, a credit rating, or an input to a lending decision.
If it drifts that way it acquires regulatory exposure we do not want and cannot
support from this data.

---

## 6. Anomaly detection

Runs on every release, output into `release.anomalies`.

| Kind | Test | Action |
|---|---|---|
| Bulk cluster | `is_bulk` count above threshold, or month > 3 standard deviations above a sector's trailing 24-month mean | Flag, suppress derived claims, require a human note |
| Procedure shift | One procedure's share moves more than 5 points in a month | Flag for commentary |
| Reclassification | A sector's history changes between vintages | Flag, do not publish the change as a trend |
| Revision | Prior month restated by more than 2% | Note on the page |
| Divergence | Rolling and YTD point in opposite directions | Force the "mixed" wording |
| New extreme | Rolling 12m at a series high or low | Candidate for the monthly bulletin |

Every anomaly is machine-detected and **human-confirmed before it becomes prose**.
The machine says "this month is a 4-sigma outlier for SIC 681". Only a human, with
the commentary in hand, may write "roughly 200 connected companies".

---

## 7. Page design

### 7.1 Sector page order

1. H1 plus an explicit England and Wales scope line
2. Stress banner: status word, score, and the five component readings
3. Four hero metrics: latest month, YTD, rolling 12m, percentile
4. Answer-first summary, two paragraphs
5. Early signals panel, with the 15% caveat and the match rate
6. Latest figures table
7. Monthly chart, then annual trend
8. Parent and peer comparison, with rank
9. Section-level rate context, clearly labelled as the broader section
10. Two to four sourced sector-context items
11. What directors should watch
12. Practitioner reading, clearly marked as Company Debt experience
13. How to interpret these figures
14. Methodology and sources, with the vintage
15. Cite and download panel

### 7.2 Dashboard hierarchy change

The current hero over-weights the single latest month. Replace the four primary
tiles with: latest month, YTD vs same period, rolling 12m vs preceding 12m,
rolling rate. Procedure mix moves immediately below. This matches the standard the
sector pages already use.

### 7.3 Hub

Becomes a discovery dashboard, not a directory:
- "What changed this month" bulletin at the top
- Sortable cross-sector monitor
- Then the directory of pages

### 7.4 Cross-sector monitor

One table, all sectors, sortable on every column: sector, SIC, YTD, YTD change,
rolling, rolling change, vs 2019, percentile, stress band. Client-side sort, no
framework, server-rendered so it is readable without JavaScript and citable by a
machine.

### 7.5 Geography labels

Keep "UK" in the H1 where the page genuinely covers the nations. Make every
statistical heading exact: "Latest company insolvency figures for England and
Wales", "Company insolvencies by sector: England and Wales". Keep the dedicated UK
nations comparison as the only place "UK" describes a table.

---

## 8. What changed this month

Generated on each release, drives the hub, the newsletter and outreach.

Machine-generated candidates: fastest improving and deteriorating by rolling
change, new series highs and lows, trend reversals of three or more consecutive
periods, anomalies, and any sector crossing a stress band.

**A human writes the bulletin's opening paragraph.** The machine ranks and
supplies evidence; it does not decide what the month means. This is the line
between a data product and an automated content mill, and it is also where the
Company Debt voice lives.

---

## 9. Per-sector context indicators

Each sector maps to two to four external indicators, defined once in a registry,
never pasted generically:

| Sector | Indicators |
|---|---|
| Restaurants, pubs | Hospitality output, food prices, consumer spending |
| Road haulage, freight | Freight volumes, diesel, transport output |
| Recruitment, staffing | Vacancies, temporary billings, hiring intentions |
| Construction trades | Construction output, new orders, payment terms |
| Retail | Retail sales volumes, consumer confidence |
| Real estate | Commercial values, refinancing rates |

Each carries source, period, geography, and an explicit statement that it is
context and not a measured cause. The strongest sentence this unlocks:

> Restaurant insolvencies have fallen 6.2% year to date, but the demand indicator
> weakened over the latest quarter. On that basis the improvement should be read
> as fragile rather than a clear recovery.

That is an analytical judgement built on two sourced series. It is the product.

---

## 10. Provenance and reuse

Four-level hierarchy, visually distinct on every page, never blurred:

1. **Official fact** — Insolvency Service, ONS, Companies House
2. **Company Debt calculation** — derived from official data
3. **External context** — named third party, dated
4. **Company Debt practitioner observation** — our casework, human-signed

Every chart: download PNG, download CSV, copy figures, cite. Every table: source,
calculation attribution, vintage, update date. Every derived number traceable from
official source, through source row, through the calculation, to the display.

Practitioner blocks need a named insolvency practitioner's sign-off, recorded in
the repo, or they are rewritten as neutral operational analysis. This is
outstanding on the existing pages and blocks nothing else.

---

## 11. Automated versus editorial

| Automated | Human |
|---|---|
| Ingestion, parsing, vintage capture | What the month means |
| Every metric and derived figure | Bulletin opening, sector narrative |
| Shares, ranks, superlatives | Confirming an anomaly's cause |
| Anomaly detection and flagging | Practitioner observation and sign-off |
| Consistency assertions | Choosing context indicators |
| Chart and table rendering | Judging whether a signal is fragile |
| Bulletin candidate ranking | Legal and compliance wording |

The dividing line: **machines produce figures and candidates, humans produce
claims about causation and meaning.** Every failure found in the two August audits
was a human claim that outran the data, or a hand-typed figure that drifted from
it. This split addresses both.

---

## 12. Build order

Staged so each phase ships something usable and nothing depends on an unbuilt
phase.

**Phase 1: make the current pages incapable of contradicting themselves.**
Release object, migrate all 25 pages to read from it, extend the assertion suite,
wire it into the gate. No visible change. This is the foundation and it retires
the whole class of error found in August.

**Phase 2: the analytical layer.** Metric dictionary, percentiles from the 126
months of history, cross-sector monitor on the hub, dashboard hierarchy change,
geography labels. First visible upgrade.

**Phase 3: what changed this month.** Bulletin generator plus human opening.
Turns one dataset into a publishing operation.

**Phase 4: stress index.** Only after phases 1 and 2, because it depends on the
metric dictionary and percentiles. Ship with the methodology page from day one.

**Phase 5: acquisition.** Record-level file with `is_bulk` for real cluster
detection. Business Insolvency Demography for section rates. ONS births and deaths.
Each lands behind the assertion suite.

**Phase 6: the enforcement signal.** Gazette to Companies House join, match rate
published, aggregates only, floor of 10. Last because it is the hardest to do
honestly and the easiest to get wrong.

**Phase 7: more sectors.** Only now. Adding sectors before phase 1 multiplies the
maintenance burden of the error class we just fixed.

---

## 13. Risks

| Risk | Mitigation |
|---|---|
| Stress index read as company risk scoring | Explicit disclaimer, components always shown, never company level |
| Petition signal misread as covering all insolvencies | The 15% sentence, mandatory, next to the panel |
| False sector attribution from name matching | Aggregates only, match rate published, floor of 10, never name a company |
| Section rate read as a trade rate | Fixed wording, never "restaurant rate" |
| Bulk events distorting every derived figure | Detection, suppression, human confirmation |
| Revisions making old citations wrong | Vintage hash, stable historical URLs |
| Automation drifting into causal claims | The automated/editorial split, enforced in review |
| Maintenance load growing with sectors | Phase 1 before phase 7 |

---

## 14. What this is worth

The government spreadsheet is not the asset; anyone can download it. The asset
after two years is the cleaned historical database, the sector taxonomy, the
cross-source mappings, the derived metrics, the anomaly record, the longitudinal
signal history, and the interpretation methodology.

That is defensible, and because every figure traces to a primary source, it does
not require anyone to trust an opaque score.

---

## 15. Open questions for a human

1. Gazette licensing. Reading notices is public. **Bulk or systematic access may not be**, and the join in phase 6 is systematic. Legal check needed before building.
2. Does a named insolvency practitioner sign off the practitioner blocks, or do they become neutral analysis?
3. Is the stress index published at all, or held as internal editorial input first?
4. Companies House API rate limits against roughly 9,000 name lookups a year.
5. Who owns the human half of the monthly bulletin, and by when each month?
