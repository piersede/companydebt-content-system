# Claude Design prompt - UK Business Payment Practices data page

Copy everything in the block below into Claude Design. It is self-contained.

---

You are designing one new page for **Company Debt's insolvency data hub** (companydebt.com) - a data-product section, not a blog. The page is **"UK Business Payment Practices"**. Produce a polished, responsive front-end build: semantic HTML, CSS, and inline SVG charts (no chart library, no external JS dependencies).

## The single most important rule

This page shows **late-payment data, which is NOT insolvency data**. It is context about how slowly large companies pay suppliers. It must be **visually and editorially separated** from any insolvency figures - never present a payment metric as, or beside, an insolvency count, and never imply it is a company-failure rate. Carry a clear standing line near the top and in the caveats: *"Payment practices data is late-payment context only. It is not an insolvency statistic."*

## Visual identity (match the existing hub pages)

The hub already has three live pages with an established look: a UK Company Insolvency Data hub, a Winding-Up Petition Tracker, and a Dissolutions vs Insolvencies page. Match them: a serious, trustworthy "official data product" feel - clean, GOV.UK-adjacent clarity but on Company Debt's brand. Calm neutral background, generous whitespace, strong typographic hierarchy, a single restrained accent colour (Company Debt uses a warm orange accent - use it sparingly for emphasis, links and chart highlights, never as large fills). Data containers should be **wider** than prose containers. Charts and tables are first-class, not decoration.

If you can view the live pages for exact colours/spacing, mirror them. Otherwise use a restrained editorial-data palette and keep it consistent.

## Audience & tone

Journalists, accountants, lenders, business owners. British English. Plain, factual copy ("Large UK companies take 34.5 days to pay on average."). No hype, no emoji. Make trade-offs and caveats visible rather than hidden.

## The data (use these exact figures)

Source: UK statutory Payment Practices and Performance reporting. Window: Dec 2024 - May 2026. Basis: each company's most recent report (no double-counting). 6,882 reporting companies; industry resolved for 6,634 via Companies House.

Headline (means; show medians too where noted, because the data is right-skewed - a tail of very-late payers pulls the mean above the median):
- Average days to pay an invoice: **34.5 days** (median 31)
- Invoices NOT paid within agreed terms (i.e. paid late): **22%** (median 15%)
- Invoices paid within 30 days: **59.8%**
- Invoices paid in 31-60 days: **28.3%**
- Invoices paid later than 60 days: **11.9%** (median 5%)

Industry breakdown (by number of companies; slowest payers are the story):
| Industry | Companies | Avg days to pay | % paid late | % within 30 days |
|---|---|---|---|---|
| Manufacturing | 1,058 | 47.4 | 28.9% | 36.6% |
| Wholesale & retail | 874 | 38.5 | 23.7% | 48.5% |
| Finance & insurance | 839 | 24.3 | 17.9% | 79.7% |
| Admin & support | 660 | 29.9 | 19.7% | 67.3% |
| Professional services | 614 | 34.5 | 22.2% | 64.0% |
| Information & communication | 515 | 33.6 | 22.8% | 66.7% |
| Construction | 413 | 34.7 | 18.6% | 53.7% |
| Education | 307 | 24.8 | 19.3% | 79.0% |
| Transport & storage | 272 | 34.4 | 19.9% | 55.5% |
| Accommodation & food | 202 | 33.7 | 18.3% | 55.8% |
| Electricity & gas | 177 | 27.6 | 16.6% | 74.2% |
| Health & social work | 147 | 29.1 | 17.2% | 71.0% |

(There are 21 industry sections in total; the rest are smaller. Group any industry with fewer than ~30 companies into "Other" - too few to be reliable. Manufacturing is the slowest-paying major sector; finance and education are the fastest.)

## Page structure (top to bottom)

1. **Header / H1**: "UK Business Payment Practices". Subhead: "How long large UK companies take to pay their suppliers - and which industries pay slowest." Small "Last updated / data window" + "this is payment context, not insolvency data" line.
2. **Intro** (2-3 sentences): what statutory payment-practices reporting is (large UK companies and LLPs must report payment performance twice a year), what this page shows, and the not-insolvency caveat.
3. **KPI strip** (4 cards): Average days to pay (34.5), Invoices paid late (22%), Paid within 30 days (59.8%), Companies in the data (6,882). Each card: big number, short label, tiny source/window note.
4. **Chart A - payment speed**: a single horizontal segmented/stacked bar splitting invoices into within 30 days (59.8%) / 31-60 days (28.3%) / later than 60 days (11.9%). Clear legend. Source line beneath.
5. **Chart B - by industry (the centrepiece)**: a horizontal bar chart ranking industries by average days to pay (Manufacturing longest at 47.4, Finance shortest at 24.3). Highlight the slowest 1-2 bars in the accent colour. Beneath it, the **full industry table** (columns: Industry, Companies, Avg days to pay, % paid late, % within 30 days), visually sortable-looking even if static. Source line.
6. **Explainer - "What counts as late, and the Prompt Payment Code"**: plain definitions. Late = not paid within the agreed terms. Mention the voluntary Prompt Payment Code and that statutory interest can apply to late commercial debts. (This section targets real search terms - keep the headings clean and literal.)
7. **"Why this matters"** (bridge): slow payment higher up the supply chain drains smaller suppliers' cash flow; persistent late payment is a recognised stress signal. Keep it context, not causation. Include up to three contextual text links (cash-flow problems / can't afford to pay suppliers / the insolvency data hub) - styled as inline links, NOT a related-posts grid.
8. **Caveats block** (prominent, boxed): (a) **Payment practices data is late-payment context only - it is not an insolvency statistic and must not be blended into insolvency figures.** (b) Figures are self-reported by businesses and not independently audited, so individual reports can contain errors. (c) Only large companies and LLPs must report, so this describes big-business behaviour, not the whole economy. (d) Averages are right-skewed - the typical (median) company pays a bit faster than the mean suggests. (e) Industry is the company's primary registered SIC code.
9. **Methodology & citation**: one-line method, the source name and link, the data window, and a copy-ready citation line. A "copy citation" button is a nice touch.
10. **Single advice CTA** near the end (one only) - a calm prompt to Company Debt's business-debt advice. No second CTA, no generic content grid.

## Constraints / house rules

- Inline SVG charts only. **No pie charts.** No chart library. Keep charts legible on mobile (consider stacking/relabelling at narrow widths).
- Every chart and table has a source line.
- One advice CTA total. No related-content carousels.
- Accessible: semantic landmarks, table headers with scope, sufficient contrast, charts readable without colour alone (label values directly).
- Wider max-width for the data/chart sections than for the prose sections.
- British English throughout. Do not invent figures - use only the numbers above; if you need a placeholder, mark it clearly.

## Deliverable

A self-contained responsive page (HTML + CSS + inline SVG) I can drop into the hub. Keep the markup clean and well-commented so it can be wired into WordPress as a data-reference template afterwards.
