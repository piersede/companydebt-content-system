# Data hub - page build specs

Build-ready blueprints for the next data-hub pages. Each page's data is already
fetched and stored (see architecture.md). These specs fix the structure,
figures, caveats, SEO and schema so the visual design step is purely visual.

House rules carried from the brief: British English; plain, factual copy
("There were...", "The rate was...", "This is not the same as..."); volumes are
not rates; one final advice CTA only, no generic related-content grids; every
chart and table carries a source line; wider containers for data than for prose.
Caveats are cited by id from data/_meta/caveats.json.

Latest figures available (as built):
- Insolvency Service, April 2026: 2,085 insolvencies E&W (SA); CVL 1,510, compulsory 371, administration 183, CVA 20, receivership 1; rate 51.8 per 10,000; Scotland 107, NI 40.
- Companies House, May 2026: 5,498,905 active companies; 62,523 incorporations; 59,296 dissolutions.
- The Gazette, May 2026: 482 winding-up petitions; 25 petition dismissals; 373 winding-up orders; 138 administrator appointments; 2,031 liquidator appointments; 1,868 CVL resolutions.
- ONS, 2025: 2,734,615 enterprises; by section M 419,570, G 396,505, F 384,830, N 222,055, J 187,705, I 176,690.

---

## 1. Insolvency data hub (landing page)

- URL: `/data/` (the hub lives at `/data/` itself; every data page sits flat beneath it as `/data/<slug>/`. The old nested `/data/company-insolvency/*` URLs 301 to the flat ones.)
- Search intent: the entry point and directory for all CompanyDebt insolvency data. Not an article; a data product index.
- Data: pulls one or two headline figures from each live source for the "at a glance" strip; otherwise links out.

Structure:
- H1: UK Company Insolvency Data
- Intro (2-3 lines): what this hub is, who it is for (journalists, accountants, lenders, directors), how often it updates.
- "Latest at a glance" KPI strip: latest monthly insolvencies (2,085), 12-month rate (51.8), winding-up petitions last month (482), active companies (5.5m). Each with source + month label.
- Card sections (the brief's groups), each card = title, one-line description, freshness label, link:
  1. Latest dashboard: UK Company Insolvency Statistics (live)
  2. Formal statistics: CVL / Compulsory liquidation / Administration stats (planned)
  3. By sector: Company Insolvencies by Sector, Construction Insolvency (planned)
  4. Legal pressure: Winding-Up Petition Tracker (build below)
  5. Company population: Dissolutions vs Insolvencies (build below)
  6. Methodology and sources: source notes + how to cite
- Final advice CTA (single).
- Do NOT make it look like a blog archive.

SEO: title "UK Company Insolvency Data and Statistics"; meta describing the hub. Schema: WebPage + BreadcrumbList + ItemList (the cards). Internal links: out to each data page; each data page links back here.
Freshness labels per card: Latest / Provisional / Planned.

---

## 2. Winding-Up Petition Tracker

- URL: `/winding-up-petition-tracker/`
- Search intent: how many winding-up petitions are being advertised, and the trend. The early-warning / legal-pressure page.
- Data: The Gazette (data/the-gazette/). Headline = winding-up petitions (2450). Supporting = petition dismissals (2461), winding-up orders (2452).
- Data prep needed: backfill `the_gazette.py` for the last 12-24 months so the trend chart has history (currently only May 2026 is stored). One command per month.

Structure:
- H1: Winding-Up Petition Tracker
- Intro: what a winding-up petition is in one plain line, and that this counts notices advertised in The Gazette.
- KPI: latest month petitions (482), change vs prior month, 12-month total.
- Chart A: monthly winding-up petition notices (line/bars) - needs backfill.
- Chart B: petitions vs winding-up orders (two series) - shows how many petitions convert to orders/compulsory liquidation.
- Section: Gazette notice-type breakdown for the latest month (table: petitions, orders, administrator/liquidator appointments, CVL resolutions).
- Caveats (prominent): `gazette_not_outcome` (legal notices, not outcomes; petitions may be dismissed/withdrawn/settled). Show petition dismissals (25) as supporting evidence.
- Note: do NOT claim this is an official Insolvency Service statistic.
- One advice CTA near the end (link to compulsory liquidation / winding-up petition advice page once).

SEO: title "Winding-Up Petition Tracker (UK)"; "tracker" intent. Schema: WebPage + Dataset + BreadcrumbList. Cross-check note: Gazette winding-up orders (~373) align with Insolvency Service compulsory liquidations - good to state for credibility.

---

## 3. Company Dissolutions vs Insolvencies

- URL: `/company-dissolutions-vs-insolvencies/`
- Search intent: the difference between ordinary company closures and formal insolvency, shown with data. Protects the main insolvency pages from "company closures" intent.
- Data: Companies House dissolutions + incorporations (data/companies-house/) and Insolvency Service insolvencies (data/insolvency-statistics/).
- Data prep needed: a small combined dataset/series joining monthly dissolutions, incorporations and formal insolvencies, plus the ratio.

Structure:
- H1: Company Dissolutions vs Insolvencies
- Intro: most companies that close are not insolvent; here is the difference in numbers.
- KPI row: dissolutions last month (59,296), formal insolvencies last month (2,085), ratio (~28:1), incorporations (62,523).
- Chart A: incorporations vs dissolutions (monthly) - business formation vs closure.
- Chart B: dissolutions vs formal insolvencies - scale comparison (most closures are solvent strike-offs).
- Section "Why most closures are not insolvencies": plain explanation, then the data.
- Caveats (prominent): `dissolutions_not_insolvencies` (strike-offs and MVLs are not insolvency), `ons_denominator` if ONS context used.
- One advice CTA.

SEO: title "Company Dissolutions vs Insolvencies (UK Data)"; targets "company closures statistics". Schema: WebPage + Dataset + Table + BreadcrumbList. Clear line: "This is not the same as insolvency."

---

## 4. UK Business Payment Practices (ENRICHMENT ONLY)

- URL: `/data/business-payment-practices/` (nested under the `/data/` parent, like the hub).
- HARD RULE: this is late-payment ENRICHMENT/CONTEXT, NOT insolvency data. It must be visually and editorially separated from insolvency figures - never a KPI next to insolvency counts, never implied as a failure rate. Frame as the cash-flow-pressure context layer that sits alongside the insolvency data.
- Search reality (Ahrefs, gb, Jun 2026): low volume, but low difficulty and on-topic. Winnable terms: "payment practices reporting" (700, KD 3), "prompt payment code" (500, KD 1), "late payment of commercial debts" (400, KD 15), "supplier payment times" (30). The high-volume "late payment" terms are tax-penalty / credit-score intent (different, covered elsewhere) - do NOT chase them. Value of this page = citation/answer-engine asset (unique 6,882-company dataset) + low-KD captures + internal-link glue to cash-flow / cant-pay-suppliers / insolvency hub.
- Data: data/payment-practices/payment_practices_summary.json (built by scripts/datahub/sources/payment_practices.py --with-sectors). Window 2024-12-07 to 2026-05-31; latest report per company (no double-counting); 6,882 reporting companies; SIC resolved for 6,634 via Companies House.

Headline figures (means; medians in brackets where the skew matters):
- Average days to pay: 34.5 days (median 31).
- Invoices NOT paid within agreed terms: 22.0% (median 15%) - right-skewed; a tail of very-late payers pulls the mean up. Show both.
- Invoices paid within 30 days: 59.8%; 31-60 days: 28.3%; later than 60 days: 11.9% (median 5%).

Sector (SIC section, by company count; slowest payers first matters most):
- Manufacturing: 1,058 cos, 47.4 days, 28.9% late (SLOWEST).
- Wholesale and retail: 874, 38.5 days, 23.7% late.
- Finance and insurance: 839, 24.3 days, 17.9% late (FASTEST of the big sectors).
- Admin and support: 660, 29.9 days, 19.7% late.
- Professional services: 614, 34.5 days, 22.2% late.
- Information and communication: 515, 33.6 days, 22.8% late.
- Construction: 413, 34.7 days, 18.6% late.
- Education: 307, 24.8 days, 19.3% late.
- (full table: 21 SIC sections in the summary JSON; sections with <30 companies e.g. Households/Extraterritorial should be dropped or grouped as "Other" - too thin to be reliable.)

Structure:
- H1: UK Business Payment Practices. Sub: how long large UK companies take to pay suppliers, and which sectors pay slowest.
- Intro (2-3 lines): what statutory payment-practices reporting is (large companies report twice a year), what this page shows, that it is payment context, NOT insolvency data.
- KPI strip (4): average days to pay (34.5), % invoices paid late (22%), % paid within 30 days (59.8%), companies in dataset (6,882). Source + window label.
- Chart A: the three payment-speed bands (within 30 / 31-60 / 60+ days) as one stacked/segmented bar.
- Chart B (the star): horizontal bar chart ranking SIC sectors by average days to pay (or % late) - manufacturing top. + full sortable table of sections (companies, avg days, % late, % within 30).
- Explainer: "What counts as late, and the Prompt Payment Code" - plain lines (captures prompt-payment-code / commercial-debts intent). Late = not within agreed terms; statutory interest on late commercial debts exists.
- "Why this matters" bridge: slow payment up the chain drains supplier cash flow; sustained late payment is a distress signal. Careful: context, not causation; link out (once each) to cash-flow problems / cant-afford-to-pay-suppliers / the insolvency hub.
- Caveats (prominent block): `payment_practices_enrichment` (FRONT AND CENTRE), `payment_self_reported`, `payment_large_companies_only`. State means are right-skewed; sector = primary SIC only.
- One advice CTA.

SEO: title "UK Business Payment Practices: How Long Companies Take to Pay (Data)"; meta on average payment times + slowest sectors. Schema: WebPage + Dataset + Table + BreadcrumbList. Page class: `data_reference` (passthrough draft + CD-NO-AUTOEDIT guard + mu-plugin for schema/JS).

---

## Cross-cutting (all pages)
- Journalist features: latest-figure block, "last updated / next release" dates, copy-citation button, source line on every chart/table, short quotable summary lines.
- Persistent URLs (update monthly, do not mint a new URL per month).
- Charts: reuse the SVG approach in scripts/build_insolvency_charts.py (no chart library, no pie charts).
- Page class: register each as `data_reference` (passthrough draft + CD-NO-AUTOEDIT guard + mu-plugin for schema/JS).
