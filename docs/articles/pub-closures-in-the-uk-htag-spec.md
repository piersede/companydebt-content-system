# H-Tag Spec: UK Pub Closures in 2026

**Page:** `/articles/pub-closures-in-the-uk/` (wp_post_id 24589, post type `post`, author 34, FM 70418)
**Page class:** `data_reference` (overlay: `runtime-packs/overlays/statistics.md`)
**Source of truth:** `drafts/24589_pub-closures-in-the-uk.html` (this is what is deployed). Do NOT build from `scripts/cc_builder/data/pages/pub_closures_in_the_uk.py` — that parallel module is stale and is not what ships.
**Gate command:** `python scripts/article_audit.py --slug 24589` from repo root. NOT `build_page.py`/`quality_check.py`.
**Design/JS/CSS:** all live in `mu-plugins/cd-pub-closures-hub.php` (post content is KSES-filtered: no `<style>`, `<script>`, `<svg>` or `data-*` in the draft). Charts are `<div class="cd-chart" id="...">` placeholders hydrated by the mu-plugin.
**Spec date:** 22 July 2026 (locked at the humanise stage, after the 8 Jul 2026 data-hub rebuild and the same-session content-restoration and humanise passes).

---

## Verified figures (source of truth for this page)

Every figure on the page must trace to a row below, and every row traces to the draft's own Sources & References block, `data/pub-closures/sources.json`, or `data/pub-closures/datasets.json`. Do not add a figure that is not here, and do not restate a figure with a geography or period it does not carry.

| Figure | Value | Geography | Period | Source |
|---|---|---|---|---|
| Pub closures, quarterly | 161 (up 26% from 128) | Britain | Q1 2026 vs Q1 2025 | BBPA (`bbpa_closures`) |
| Jobs lost with those closures | ~2,400 | Britain | Q1 2026 | BBPA (`bbpa_closures`) |
| Closures, annual | 289 | England & Wales | 2024 | BBPA (`bbpa_closures`) |
| Permanent pub losses | 366 | England & Wales | 2025 | Ryan rating-list analysis (`ryan_altus_permanent_loss`) |
| Counted pub stock, start → end of year | 38,989 → 38,623 | England & Wales | 2025 | Ryan rating-list analysis (`ryan_altus_permanent_loss`) |
| Hardest-hit regions (named, no exact counts) | East Midlands, North West, Yorkshire & the Humber | England & Wales | 2025 | Ryan rating-list analysis (`ryan_altus_permanent_loss`) |
| Remaining pub stock | ~45,000 (approx) | UK | 2024 | House of Commons Library, citing BBPA (`hoc_pub_stats`) |
| Pub stock, earlier points | 60,800 (2000); 55,400 (2010) | UK | 2000, 2010 | House of Commons Library, citing BBPA (`hoc_pub_stats`) |
| Pub/bar/nightclub operator insolvencies | 789 (up 2.6% from 769; vs 367 in 2020) | Britain | year to 31 Dec 2025 | UHY Hacker Young (`uhy` in draft Sources) |
| Accommodation & food services insolvencies | 3,296 | England & Wales | 12 months to May 2026 | Insolvency Service (`insolvency_service_company`) |
| Sector insolvency rate | 268 per 10,000 (peak 314 in 2023; all-industry avg 116) | England & Wales | 2025 | Insolvency Service (`insolvency_service_company`) |
| Technically insolvent / max credit risk | ~1 in 8 pubs (up from 1 in 10 a year earlier) | — | early 2026 | Price Bailey analysis (draft Sources) |
| Business births vs deaths, death rate | 30,360 births / 26,195 deaths / 12.9% | UK | 2024 | ONS business demography (`ons_business_demography`) |
| National Living Wage | £12.71/hr (+4.1%) | UK | from April 2026 | GOV.UK (`govuk_nmw_2026`) |
| Employer NIC rate / threshold | 15% (from 13.8%) / £5,000 (from £9,100) | UK | from April 2025 | HMRC (`hmrc_nic_2025`) |
| Pub rateable-value change at 2026 revaluation | +30% (pubs); +70% (pub with lodge); +19.4% all-property avg | England | 2026 revaluation | VOA via House of Commons Library (`hoc_business_rates_pubs`, `rates_revaluation_2026`) |
| Pub business-rates relief | 15% | England | 2026/27 | GOV.UK (`govuk_business_rates_relief`) |
| RHL multipliers | 38.2p (RV < £51,000); 43p (£51,000–£499,999) | England | 2026/27 | GOV.UK (`govuk_business_rates_relief`) |
| Alcohol duty uprating | +3.66% (RPI) | UK | from 1 Feb 2026 | HMRC (`hmrc_alcohol_duty_2026`) |
| Draught vs main beer duty | £19.45/litre (draught 3.5–<8.5% ABV) vs £22.58 (main beer) | UK | from 1 Feb 2026 | HMRC (`hmrc_alcohol_duty_2026`) |
| BICS: turnover affected by a challenge | 83% any; materials 48%; labour 48%; uncertainty 43% | UK | June 2026 | ONS BICS (`ons_bics`) |
| Adults not drinking in last 12 months | 24% (up from 19% in 2022) | England | 2024 | NHS England (`nhs_england_behaviours`) |
| 16–24 weekly drinking (lowest age group) | 30% | England | 2024 | NHS England (`nhs_england_behaviours`) |
| Average pint of draught lager | 200p → 477p (+139%) | UK | 2000 → 2024 | ONS RPI average-price series (`ons_rpi_lager`) |
| Freehold pubs sold for change of use | 34% | UK market | 2023 transactions / 2024 report | Fleurets Survey of Pub Prices (`fleurets_pub_prices`) |
| Community-owned / community-run pubs | 217 owned + 28 run (Apr 2025); 210+ trading (Jan 2026) | UK | 2025–26 | CAMRA / Plunkett UK (`camra_plunkett_community`) |

## Removed / deliberately not-claimed (do not reinstate)

- **On-trade vs off-trade drinking shift as a hard causal claim.** The page carries an explicit caveat (in "Are Pubs Closing Because People Are Drinking Less?"): current, openly published data on how far drinking has moved from the pub to the supermarket is **thinner than the closure and cost figures**. This is deliberate. Do NOT convert the NHS abstention/weekly-drinking trend or the pint-price series into a sourced statement that "X% of drinking has moved off-trade" or that supermarket competition caused a specific share of closures. The trend data (`nhs_england_behaviours`, `ons_rpi_lager`) supports *demand has softened and affordability has shifted*; it does not support an on-trade-to-off-trade migration percentage. Keep the caveat sentence intact.
- **Exact regional closure counts.** `regional_hotspots_2025` is confidence `low`: the source names the hardest-hit regions but publishes no exact regional pub counts. The page names the three regions and says so explicitly. Do NOT invent regional numbers or a regional chart with fabricated values.
- **Adding measures together.** Pub closures, permanent losses, company insolvencies and technical insolvency are four different events over different geographies and periods. Never sum them, and never restate a Britain/GB or England & Wales figure as "UK". Community-owned and community-run pubs are separate categories and must not be summed either.
- **2025 annual closures as fact.** The BBPA 2025 annual figure (378) is a Great Britain *forecast*, not final outturn, and is not presented on the page as an actual. Do not promote it to a confirmed count.

---

## H-tag structure

```
H1: UK Pub Closures in 2026
  -> Hero H1 only. Kept short by design; the head term "UK Pub Closures" leads.
     KPI cards, byline (Company Debt / reviewed by Chris Andersen IP / updated date)
     and the sources strip sit under it, NOT as headings. No H2 in the hero.

H2: Latest UK Pub Closure Figures for 2026  [#sec-latest-figures]
  -> No H3s. Opens on the four headline numbers, then the comparison table
     (Measure / Latest figure / Period / Geography / What it means).
  -> MANDATORY framing: state that the four datasets measure different things and
     are not interchangeable. This is the page's spine (overlay: "distinguish what
     the data counts from what it omits"). Carries the "where we start when we look
     at a pub's finances" practitioner line.

H2: How Many Pubs Are Left in the UK?  [#sec-stock]
  -> No H3s. Long-run stock: 60,800 (2000) / 55,400 (2010) / ~45,000 (2024).
     chart-decline + "Show the data" <details> table.
  -> Must state the 2024 figure is the most recent reliable estimate, not a
     confirmed 2026 total. "Roughly a pub in four lost since 2000" is the framing.

H2: How Many Pubs Closed in 2025 and 2026?  [#sec-2025-2026-closures]
  H3: Pub Closures in the First Quarter of 2026   -> BBPA 161, ~two a day, +26%, ~2,400 jobs. chart-quarter.
  H3: Permanent Pub Losses in 2025                -> Ryan 366 E&W, 38,989 -> 38,623. Statrow + <details> table.
  H3: Which UK Regions Lost the Most Pubs?        -> Named regions only, chips, no exact counts (data gap stated).
  -> H3s EARNED: three distinct measures/questions under one closures H2 (a quarterly
     count, a permanent-loss count, a regional breakdown). Not a list; keep as H3s.
     (Gate check 25 flags this cluster as a soft advisory; reviewed as coherent — keep.)

H2: Pub and Bar Insolvencies in 2025 and 2026  [#sec-insolvency]
  -> No H3s. UHY 789 (Britain, to 31 Dec 2025); Insolvency Service 3,296 accom & food
     (E&W, wider than pubs); rate 268/10,000 (peak 314); Price Bailey ~1 in 8 technically
     insolvent; ONS births/deaths 30,360/26,195. charts: chart-rate, chart-churn + tables.
  -> MANDATORY definitional separation: closure != insolvency; company insolvency !=
     technical insolvency; accom & food != pubs alone. Carries the earned practitioner
     "in the pub failures that reach us" caseload line (this is genuine practice territory).

H2: Why Are UK Pubs Closing in 2026?  [#sec-why]
  H3: Higher Staffing Costs                              -> NLW £12.71, employer NIC 15% / £5,000.
  H3: Business Rates and Alcohol Duty                    -> RV +30%/+70%, 15% relief, multipliers; duty +3.66%, draught £19.45 vs £22.58. chart-rates.
  H3: Higher Materials and Operating Costs               -> BICS 83%/48%/48%/43%. chart-challenges.
  H3: Are Pubs Closing Because People Are Drinking Less? -> NHS 24% abstain, 16-24 at 30%; pint 200p->477p. chart-pint. HOLDS the on-trade/off-trade caveat.
  H3: Redevelopment and Change of Use                   -> Fleurets 34% freehold for change of use.
  -> H3s EARNED: five distinct cost/demand drivers, each a parallel part of one
     "why" topic, each with its own dataset. (Gate check 25 soft-flags this cluster;
     reviewed as coherent subheadings — keep. Do not demote to bullets: each carries
     a chart or a discrete policy dataset.)
  -> Intro MANDATORY point: a pub stands in the path of almost every increase at once
     (labour-heavy + property-heavy + sells alcohol). "A pub cannot stop being a pub."

H2: What Pub Closures Mean for Local Communities  [#sec-communities]
  -> No H3s. Community-owned/run table; buyout is not the usual outcome; where the
     site is worth more as flats/a shop the loss becomes permanent.

H2: What to Do If Your Pub Is in Financial Distress  [#sec-help]
  -> No H3s. THE DECISION POINT. This is the one section where humanise Part C applies
     with full weight on this page class: persona warmth / recognition of reader stress
     (the deferred VAT bill, the rent quarter, "it does not mean you have run the place
     badly") near the top of the section, earned practitioner "we", and the viability
     question first. CTA (contact + phone) and option links: Time to Pay, CVA,
     Administration, CVL, winding-up petition. These are the internal links the gate needs.

H2: FAQs About UK Pub Closures  [#sec-faq]
  -> Native <details>/<summary> accordion (cd-faq). Gate check 16 does NOT recognise this
     as an accordion (block-pattern detector miss) — accepted exception, the accordion is
     real and works. Questions must not contradict body figures.

H2: Methodology, Sources and Definitions  [#sec-method]
  -> Styled aside (cd-method), NOT H2 flow of content (overlay: "methodology and sources
     sit in a styled aside"). Holds: per-metric source map, the three kept-separate
     definitions (pub stock / permanent loss / company insolvency), the geography-varies
     note, refresh cadence, named-IP review, commercial disclosure, and the <ul> source list.
  -> Gate check 18 does not detect this as a "Sources & References" block (class/wrapper
     mismatch) — accepted exception; the sources list is present and complete.
```

---

## Structural rules for this page

- **British spelling and UK terminology throughout.** "pub", "landlord/publican", "wet-led", "on-trade", rateable value, RPI.
- **No em dashes anywhere** (house hard rule, zero tolerance). Verified 0 in body. No en dashes either.
- **KSES constraints are absolute.** No `<style>`, `<script>`, `<svg>` or `data-*` attributes in the draft. All CSS/JS lives in `mu-plugins/cd-pub-closures-hub.php`. The `<!-- wp:html -->` wrapper must stay intact. Do not touch the `<div class="cd-chart" id="...">` placeholders or the JSON-LD/structured data.
- **Chart-plus-static-text duplication is required, not redundant.** Every `cd-chart` visual must be shadowed by a static `<details class="cd-data">` table (or an inline stat block) carrying the same figures, so the data survives with JS off and is machine-readable. Do not delete the "Show the data" tables as duplication.
- **Every chart/table figcaption states its own geography and period.** Geographies genuinely differ (UK vs Britain/GB vs England & Wales vs England only). Never launder one into another.
- **Paragraphs 2–3 rendered lines (~150–250 chars), hard ceiling ~400.** Split at sentence boundaries only; never mid-clause, never inside a tag.
- **`data_reference` calibration on humanise Part C (practitioner voice).** This is a data/data-journalism page, not a distressed-director advice page. Apply Part C with a light touch: persona warmth, concrete reader-recognisable scenes and earned practitioner "we" belong at the DECISION POINT ("What to Do If Your Pub Is in Financial Distress") and, lightly, in the insolvency section (genuine practice territory). Do NOT retrofit "we've seen" scene-setting into the closure-rate, stock or cost-driver sections to chase a numeric quota — that fights the register.
- **Accepted, documented gate exceptions (do NOT hack around by renaming classes or reverting structure):** check 12 (hero image in body — bespoke hero, intentional); check 13 (template mismatch — bespoke full-width template); check 16 (FAQ accordion — native `<details>`, detector miss); check 18 (Sources block — wrapper/class mismatch, section is present); check 25 (3+ H3s under one H2 — reviewed as coherent, soft/advisory). Check 04 (we/our ≥ 5/1k) may land marginally short (currently ~4.8/1k) ONLY because Part C is genuinely satisfied; it is not a licence to pad hollow "we". Every OTHER check must pass cleanly.
- **Reviewer and disclosure are load-bearing.** Named IP reviewer (Chris Andersen), review/update date, methodology, and the commercial disclosure ("Company Debt is a commercial insolvency practice and is not independent of the procedures described here") stay on the page. This is a YMYL data page authored by an interested party; the disclosure is mandatory.
- **Refresh cadence:** closures and insolvency figures at least quarterly; policy figures (rates, duty, NIC, wage floor) immediately on change. Re-verify the "verify"-status source URLs in `sources.json` at each refresh before the citation goes live.
