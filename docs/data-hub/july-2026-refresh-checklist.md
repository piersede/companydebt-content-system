# July 2026 insolvency data refresh - operator checklist

Prepared 13 August 2026. Nothing in this file has been run. No data file was
changed. The July 2026 figures were not published when this was written.

**Release date: 18 August 2026 - CONFIRMED.** The Insolvency Service states
"Next release: 18 August 2026" on the June 2026 commentary page
(https://www.gov.uk/government/statistics/company-insolvencies-june-2026/commentary-company-insolvency-statistics-june-2026).

`data/insolvency-statistics/release_metadata.json` currently carries
`"next_release_date": "21 August 2026 (estimated ... not yet confirmed)"`.
That is wrong. It was hand-edited after the last parser run. The parser's own
hard-coded value (18 August 2026) is the correct one.

Each step is marked:

- **AUTO** - a command does the whole job.
- **HUMAN** - a person must rewrite prose or check a judgement. No script does it.

---

## Part 0 - before the data lands

### 0.1 HUMAN - fix the two hard-coded date strings in the parser

`scripts/parse_insolvency_data.py`, function `build_release_metadata`
(line ~250). Three values are hard-coded, not read from the source:

```python
"latest_month_label": "June 2026",
"publication_date":   "17 July 2026",
"next_release_date":  "18 August 2026",
```

Set these to `July 2026`, `18 August 2026`, and the next release date printed
on the July commentary page. **If this is skipped, the parser silently rewrites
release_metadata.json back to June 2026 and every page below inherits it.**

### 0.2 HUMAN - fix the default source filenames in the parser

Same file, `main()` (line ~304). The defaults still point at June:

```python
--csv   default = data/insolvency-statistics/source_long_run_2026-06.csv
--xlsx  default = data/insolvency-statistics/source_data_tables_2026-06.xlsx
```

Either update the defaults or pass `--csv` / `--xlsx` explicitly at step 1.2.

---

## Part 1 - pull and parse the source data

### 1.1 HUMAN - download the July files

From the Insolvency Service July 2026 release, save into
`data/insolvency-statistics/`:

- `source_long_run_2026-07.csv`
- `source_data_tables_2026-07.xlsx`

Note: `source_industry_tables_*.xlsx` files also sit in that folder. **Nothing
reads them.** Both parsers read sheet `Table_1c` out of
`source_data_tables_*.xlsx`. Do not spend time sourcing an industry workbook.

### 1.2 AUTO - parse the headline series

```
python scripts/parse_insolvency_data.py --csv data/insolvency-statistics/source_long_run_2026-07.csv --xlsx data/insolvency-statistics/source_data_tables_2026-07.xlsx
```

Writes `monthly_series.json`, `rate_series.json`, `sector_breakdown.json`,
`uk_nations.json`, `release_metadata.json`.

### 1.3 AUTO - parse the by-industry series

```
python scripts/datahub/parse_sector_series.py
```

Picks the newest `source_data_tables_*.xlsx` by filename sort. Writes
`sector_series.json`. Needed by the sector, construction and all 20 trade pages.

### 1.4 AUTO - fetch Companies House flows (dissolutions page only)

```
python scripts/datahub/sources/companies_house.py --month 2026-07
```

Needs `COMPANIES_HOUSE_API_KEY` in `.env`. Writes
`data/companies-house/monthly_flows_series.json`.

### 1.5 AUTO - rebuild the chart SVGs

```
python scripts/build_insolvency_charts.py
```

Writes `data/insolvency-statistics/charts/*.svg`.

### 1.6 HUMAN - update the release ledger

`data/insolvency-statistics/dataset_release.json`. Add the July entry, set the
June entry `status` to `superseded`, record file hashes, note any revisions.
No script does this.

### 1.7 AUTO - self-check

```
python scripts/datahub/registry.py
```

---

## Part 2 - the hand-written prose, page by page

**This is the part that breaks silently.** The generators inject live numbers
into some strings and pass others through untouched. Every item below is a
literal month name or figure written into the code by hand. If it is not
rewritten, the page ships July charts beside June sentences and still passes
every gate.

Do all of Part 2 **before** running any generator in Part 3.

### 2.1 Flagship dashboard (post 77399)

File: `scripts/build_insolvency_dashboard.py`. 20 hand-written references.

| Line | Function | What to change |
|---|---|---|
| 77 | `hero_block` | Lede: "little changed from **May 2026** and 10% lower than **June 2025**" |
| 94-95 | `hero_block` | Change row: `0%` vs May 2026; `-10%` vs June 2025 |
| 99-102 | `hero_block` | Four mini-KPI literals: `1,364` CVLs / `74% of total`; `276` Compulsory / `-2% on May`; `191` Administrations / `+45% on May`; `50.5` rate / `1 in 198 companies` |
| 93 | `hero_block` | Class `cd-change-row--down` - flip if July rises |
| 168 | `latest_figures_block` | Eyebrow "Snapshot · June 2026" |
| 170 | `latest_figures_block` | Intro naming the ~60-company real-estate administration cluster |
| 174 | `latest_figures_block` | Table caption "June 2026 compared with May 2026 and June 2025" |
| 178-180 | `latest_figures_block` | Three column headers: June 2026 / May 2026 / June 2025 |
| 204 | `monthly_chart_block` | Intro: "Administrations spiked in June ... clusters in March and April" |
| 267 | `rate_block` | H2 "UK company insolvency rate (June 2026)" |
| 271 | `rate_block` | "12 months to 30 June 2026" and "one in 198 companies" |
| 272 | `rate_block` | "lower than the 52.4 per 10,000 ... for the 12 months to June 2025" |
| 275 | `rate_block` | Callout key "June 2026" |
| 300-302 | `procedure_cards_block` | Card literals `1,364` / `74%`; `276` / "Down 2% on May 2026"; `191` / "Up 45% after June's real-estate cluster" |
| 326 | `procedure_cards_block` | Eyebrow "By procedure · June 2026" |
| 341, 343, 349 | `sector_block` | "12 months to June 2026" x3, plus the sector ranking sentence naming construction, wholesale and retail, accommodation and food |
| 428, 435, 439 | `nations_block` | "June 2026" x3 |
| 498 | `source_citation_block` | "Company Insolvency Statistics, June 2026" |
| 520-537 | `faq_block` | All six answers. Contains `1,845`, `June 2026`, `May 2026`, `June 2025`, Scotland `104`, NI `18`, rate `50.5`, `one in 198`, `52.4`, CVLs `1,364` / `74%`, `276`, `191`, `14`, construction `3,805` / `17%`, wholesale and retail `3,463` / `15%`, accommodation and food `3,233` / `14%`, and next release `18 August 2026`. |
| 486 | `source_citation_block` | Citation year `(2026)` - only change in January |

### 2.2 The three procedure pages (79852 CVL, 79853 compulsory, 79854 administration)

File: `scripts/datahub/pages/procedure_stats.py`. Mostly data-driven. Two
hand-written items:

- **Line ~128-133**, `PROCEDURES["administration-statistics"]["trend_intro"]`.
  Names "March, April and June" as the 2026 cluster months and "around 41%
  above 2025 levels". Rewrite if July adds or removes a cluster.
- **Lines 74, 106, 141**, the three `citation` strings - year `(2026)` only.

Everything else on these pages (counts, share, rate, peak, 13-month table,
publication and next-release dates) comes from the JSON. AUTO.

### 2.3 Sector and construction pages (79855, 79856)

File: `scripts/datahub/pages/sector_pages.py`. Almost fully data-driven -
window labels, rankings, annual tables and the construction monthly span are
all read from the data. Hand-written items:

- **Lines 246-247 and 367-368**, the two `citation` strings - year only.
- **Line 235**, `build_sector` trend intro asserts "Construction leads every
  year". HUMAN check only if the July ranking changes the top sector.

### 2.4 Dissolutions vs insolvencies (79848)

File: `scripts/datahub/pages/company_dissolutions_vs_insolvencies.py`.

All month labels and figures are injected by `inject()` from live data. The
"June 2026"/"May 2026"/"April 2026" strings at lines 146-164 are **search
anchors against the static design file**
`design-handoff/company-dissolutions-vs-insolvencies.html` - do not update
them. `_sub()` raises `SystemExit` if an anchor is missing, so a silent drift
is not possible here. AUTO.

Depends on step 1.4 having run.

### 2.5 The 20 trade pages

File: `scripts/datahub/pages/sic_group_stats.py` (7,240 lines). This is the
biggest hand-written surface in the refresh. The `SECTORS` dictionary holds one
config per trade, and the narrative fields are free prose with numbers typed in.

Fields carrying hand-written figures, counted across the 20 sectors:

| Field | Sectors carrying numbers |
|---|---|
| `pressure` | 20 / 20 |
| `notes` | 20 / 20 |
| `longer_term_narrative` | 19 / 19 |
| `hero_note` | 18 / 18 |
| `extra_findings` | 18 / 18 |
| `comparison_intro` | 18 / 18 |
| `annual_intro` | 18 / 18 |
| `faq` | 17 / 17 |
| `latest_note` | 16 / 18 |
| `divergence` (heading, caption, intro) | 15 / 15 |
| `procedure_breakdown` | 7 / 7 |
| `exclusion_note` | 6 / 20 |
| `practitioner_view` | 3 / 20 |
| `related` | 3 / 20 |
| `commercial_transition` | 2 / 20 |
| `policy_update` | 2 / 2 |
| `spike_correction` | 2 / 2 |
| `citation` | 20 / 20 (year only) |

The dominant pattern to search for is the phrase **"January to June 2026"** /
**"between January and June 2026"** - it becomes "January to July 2026" and the
year-to-date counts, the same-period-2025 counts and every percentage beside
them all change. Search the file for `June 2026` and `May 2026`; roughly 60
matches.

Two bespoke sections need a fresh judgement, not just a number swap:

- **Line 2696**, `real-estate-letting-investment-insolvency-statistics`
  `spike_correction` - "Which part of real estate drove the 2026 increase?".
  Quotes SIC 681 rising from 116 to 363 cases.
- **Line 5286**, `retail-insolvency-statistics` `spike_correction` - "Was the
  2026 real estate insolvency spike caused by landlords?". Quotes "around 200
  connected real estate companies ... across March and April".

The 20 trade pages and their WordPress IDs:

```
80098 furniture-insolvency-statistics                        SIC 310
80134 restaurant-insolvency-statistics                       SIC 561
80136 road-haulage-insolvency-statistics                     SIC 494
80137 recruitment-agency-insolvency-statistics               SIC 781
80138 temporary-staffing-agency-insolvency-statistics        SIC 782
80139 motor-vehicle-repair-insolvency-statistics             SIC 452
80140 cleaning-company-insolvency-statistics                 SIC 812
80141 hotel-insolvency-statistics                            SIC 551
80260 estate-agency-insolvency-statistics                    SIC 683
80578 it-consultancy-insolvency-statistics                   SIC 620
80581 management-consultancy-insolvency-statistics           SIC 702
80584 architectural-engineering-insolvency-statistics        SIC 711
80587 personal-care-services-insolvency-statistics           SIC 960
80590 sports-facility-insolvency-statistics                  SIC 931
80593 medical-dental-practice-insolvency-statistics          SIC 862
80596 creative-arts-entertainment-insolvency-statistics      SIC 900
80597 amusement-recreation-insolvency-statistics             SIC 932
80601 real-estate-letting-investment-insolvency-statistics   SIC 682
80604 freight-forwarding-logistics-insolvency-statistics     SIC 522
80679 retail-insolvency-statistics                           SIC 47
```

### 2.6 The mu-plugin - search snippets, FAQ and schema

File: `mu-plugins/cd-insolvency-data-hub.php`. No script updates any of it.

**a. Search title and description snippets** - function `cd_datahub_seo_meta`,
the `$meta` array. Eight `desc` values quote a figure and the month window:

| Line | Slug | Hand-written content |
|---|---|---|
| 119 | furniture | "75 ... between January and June 2026 ... manufacturing overall fell 8.5%" |
| 123 | restaurant | "1,011 ... between January and June 2026, down from 1,078" |
| 127 | road-haulage | "184 ... between January and June 2026, down from 220" |
| 131 | recruitment-agency | "136 ... between January and June 2026, down 24.9%" |
| 139 | motor-vehicle-repair | "293 garages ... in 2025 ... 140 in the first half of 2026" |
| 143 | cleaning-company | "69 ... between January and June 2026, down 6.8%" |
| 147 | hotel | "80 ... between January and June 2026, down 10.1%" |
| 151 | estate-agency | "101 cases in the first half of 2026" |

Twelve more `desc` values quote a 2025 annual figure only. Those hold until
January.

**b. Flagship FAQ block** - function `cd_datahub_schema_graph`, lines 454-471.
Five answers duplicate the flagship FAQ prose word for word: `1,845`,
`June 2026`, Scotland `104`, NI `18`, `50.5`, `one in 198`, `52.4`, `1,364` /
`74%`, `276`, `191`, `14`, construction `3,805`, wholesale and retail `3,463`,
accommodation and food `3,233`, and **"The next scheduled release is 18 August
2026"**. These must be kept identical to `faq_block()` in
`scripts/build_insolvency_dashboard.py` (step 2.1) or the page and its schema
disagree.

**c. Dataset schema descriptions and coverage** - same function. Update:

| Line | Node | Hand-written content |
|---|---|---|
| 490, 495 | uk-insolvency-statistics | "June 2026 release published 17 July 2026 ... 1,845 ... 50.5"; `temporalCoverage` `2000-01/2026-06` |
| 582 | winding-up-petition-tracker | "Latest month (May 2026): 482 petitions, 373 orders, 25 dismissals" |
| 616, 621 | dissolutions-vs-insolvencies | "47,189 dissolutions and 63,572 incorporations (Companies House, June 2026) against 1,845 ... about 26 dissolutions for every insolvency"; coverage `2025-02/2026-06` |
| 650 | payment-practices-late-payment | "to May 2026 (6,882 companies) ... 34.5 days ... 22% ... 60%" |
| 684, 689 | cvl-statistics | "Latest month (June 2026): 1,364 CVLs, 74%"; coverage `2000-01/2026-06` |
| 712, 717 | compulsory-liquidation-statistics | "Latest month (June 2026): 276 ... 15%"; coverage `2000-01/2026-06` |
| 740, 745 | administration-statistics | "Latest month (June 2026): 191 ... 10%"; coverage `2000-01/2026-06` |

**d. Per-trade FAQ answers and coverage** - same function, lines ~827 to ~1974.
One `'a'` answer per trade page, each restating the January-to-June 2026
year-to-date count, the 2025 comparison, the percentage and the rolling
12-month total. Confirmed at lines 827, 947, 1039, 1103, 1167, 1227, 1304,
1368, 1432, 1496, 1559, 1623, 1687, 1751, 1815, 1942. Each trade node also
carries `temporalCoverage` ending `2026-06-30` or `2026-06`; roughly 20
occurrences, all needing `2026-07`.

### 2.7 Hub landing page (/data/)

File: `scripts/datahub/pages/company_insolvency_hub.py`, function
`inject_data` (lines 124-146). All month labels are injected from live data;
the `May 2026` / `April 2026` strings are **anchors against the design file**
and must not be changed. AUTO.

---

## Part 3 - regenerate the drafts

Only after Part 2 is done.

### 3.1 AUTO

```
python scripts/build_insolvency_dashboard.py
python scripts/datahub/pages/procedure_stats.py
python scripts/datahub/pages/sector_pages.py
python scripts/datahub/pages/sic_group_stats.py
python scripts/datahub/pages/company_dissolutions_vs_insolvencies.py
python scripts/datahub/pages/company_insolvency_hub.py
```

### 3.2 AUTO - rebuild the downloadable CSVs

```
python scripts/datahub/export_distributions.py
```

The Dataset schema in the mu-plugin points at these files. If they are not
rebuilt, the download does not match the page.

---

## Part 4 - gates

### 4.1 AUTO - the trade-page gate

```
python scripts/sector_data_audit.py --drafts drafts/
```

### 4.2 HUMAN - read the pages

The gate does not check whether a month name matches a figure. Open each
regenerated draft and read the prose against the new numbers. This is the only
thing that catches a July chart sitting beside a June sentence.

### 4.3 HUMAN - cross-check the duplicated FAQ

Diff the six flagship FAQ answers in `build_insolvency_dashboard.py`
`faq_block()` against lines 454-471 of the mu-plugin. They are maintained by
hand in two places.

---

## Part 5 - deployment (operator only)

Not covered by this checklist and not to be run by an assistant.

- These are `data_reference` pages using `<!-- wp:html -->`. **`wp_push.py`
  truncates them and still returns 200.** Use:
  `python scripts/build_page.py --page <slug> --publish --id <wp_id>`
- Live pushes need Piers's explicit per-push instruction.
- After any push, re-render the page and check the length and structure.
- The theme template also carried a stale chart caption at the June refresh
  that no build script tracks. Check `theme/templates/data-hub-template.php`
  and the live theme for a month label after the drafts are correct.

---

## Summary of steps that are now wrong in the existing documentation

`docs/data-hub/architecture.md`, "Monthly update workflow (Insolvency
Service)", steps 1-9:

1. **Step 2 is incomplete.** It names `parse_insolvency_data.py` only. Three
   further parse/fetch steps are now required: `parse_sector_series.py`,
   `sources/companies_house.py`, and (for the petition tracker)
   `sources/the_gazette.py`.
2. **Step 3 is incomplete.** "the dashboard builder" is now six separate page
   builders, not one.
3. **The whole workflow omits Part 2 of this file.** There is no mention that
   the generators do not update hand-written prose. That is the single largest
   risk in the refresh and it is undocumented.
4. **`export_distributions.py` is missing** from the workflow entirely.
5. **Step 7 ("update the last updated / next release labels") is misleading.**
   Those labels are generated from `release_metadata.json`, which is itself
   generated by the parser from hard-coded strings. The real action is editing
   `build_release_metadata()` in `scripts/parse_insolvency_data.py`.
6. **The source-fetcher table is stale on file naming.** It implies an industry
   workbook is needed. Both parsers read `Table_1c` from
   `source_data_tables_*.xlsx`; `source_industry_tables_*.xlsx` is unused.
7. **No gate is named.** `scripts/sector_data_audit.py` is the pre-publish gate
   for the 20 trade pages and is not mentioned.
8. **No push guidance.** The `wp_push.py` truncation hazard for these pages is
   recorded in the root `CLAUDE.md` but not here.
