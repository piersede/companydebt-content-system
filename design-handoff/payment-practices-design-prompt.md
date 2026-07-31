# Claude Design Prompt — "Payment Practices & Late Payment" data page

> Paste this whole file into Claude to generate the page. It is self-contained:
> visual identity, tokens, structure, real figures, the full sector table, chart
> rules, and the enrichment-only guardrail are all included. Output **one
> self-contained HTML file** named `payment-practices-late-payment.html`.

---

## What you are building

The next page in the **CompanyDebt — UK Company Insolvency Data** hub: a data page on
**UK payment practices and late payment to suppliers**. Late payment is a leading cause
of small-company cash-flow failure, so this page sits naturally alongside the insolvency
pages: it shows how slowly large companies pay, how many invoices are paid late, and
which sectors are worst — the upstream pressure that pushes suppliers toward insolvency.

The register is a **serious statistical publication** (ONS / FT data-journalism feel):
calm, factual, quotable. Not a blog, not a lead-gen page.

**Source:** the UK government statutory **Payment Practices Reporting** service
(Department for Business and Trade — "Check when large businesses pay their suppliers").
Large UK companies (turnover > £36m, balance sheet > £18m, or > 250 employees) must
report their payment performance every six months.

---

## CRITICAL — enrichment-only guardrail

You are **matching and extending an existing design system, not inventing one.** Do not
introduce new colours, fonts, type sizes, layout patterns, components, or copy tropes
beyond what is specified below. Every section must reuse the existing components
(masthead, header + colophon, data-sources strip, KPI cards, charts, caveat, cite block,
single CTA). No gradients, no emoji, no rounded-corner accent-border callout boxes, no
extra CTAs, no invented stats or decorative icons. If a section feels thin, solve it with
layout — not filler. One advice CTA only, at the very end.

---

## Visual identity (must match the other pages exactly)

**Wrapper:** all markup inside `<main class="cd-data-hub">`; all CSS scoped under
`.cd-data-hub`, inline in a single `<style>` in the file.

**Two container widths only** — define and reuse:
- `.cd-w-wide` → `max-width:1280px` (all data sections)
- `.cd-w-standard` → `max-width:1040px` (closing prose: cite, CTA, footer)
- both: `margin-inline:auto; padding-inline:24px`. "Data wider than prose."

**Shared 12-column grid**, 24px gutters, for every major section so column edges align.

**Masthead** (full-width, hairline bottom border) — copy verbatim from an existing page:
- `.cd-brand`: 38×38 rounded **navy** square with serif "CD", serif wordmark
  "CompanyDebt", muted uppercase sub-label "Insolvency Data Hub" (left hairline divider).
- right: `.cd-verified` green check + "Compiled from official sources".

**Header** (`.cd-hub-header`, wide): back-link "← UK Company Insolvency Data" to
`company-insolvency-data-hub.html`; then a two-column grid `minmax(0,1fr) auto`, 64px gap:
- **left:** eyebrow (with pulsing live-dot) "Supplier payment" · `<h1>` **"Payment
  Practices & Late Payment"** · standfirst (see copy below).
- **right:** `.cd-colophon` card — "Publication" accent label + `<dl>`: Series 2026 /
  Updated Six-monthly / Coverage United Kingdom / Compiled Independently.

**Data-sources strip** (`.cd-srcstrip`, wide, top+bottom hairline, 28px vertical pad):
"DATA SOURCES" label + source logo(s) at 74px tall, `object-fit:contain`, no captions.
Use a fillable logo slot for the **Department for Business and Trade** source —
`<img src="assets/logo-dbt-trim.png" ...>` (the client will supply this licensed logo;
leave the `<img>` with that src and an `onerror` that hides it gracefully, matching the
other pages' logo handling).

**Type:**
- Display/serif = **Source Serif 4** (Google Fonts, 400/600/700) on: H1, panel/chart
  titles, caveat/CTA/cite headings, the brand wordmark, the scale/figure callout.
  Everything else stays the system sans stack.
- **Five sizes only:** `--fs-1` 12px · `--fs-2` 15px · `--fs-3` 19px · `--fs-4`
  clamp(34px,3vw,44px) · `--fs-5` clamp(40px,5vw,56px). H1 -0.02em; big figures -0.03em
  + `tabular-nums`.

**Colour tokens:** text `#101828`; soft `#1f2937`; muted `#667085`; hairline `#e4e7ec` /
soft `#eef0f3`; surface `#ffffff` / soft `#f8fafc`; navy figures `#0a1f44`; accent
`#0f4c81` / accent-soft `#e8f1f8`; positive `#166534` / dot `#16a34a`; caveat amber bg
`#fff7ed` / border `#fed7aa` / text `#7c2d12`; CTA orange `#ec6608` (CTA only).
For the late-payment bars use accent `#0f4c81` for the "paid late / slow" magnitude and a
soft neutral `#cdddee` for the "paid on time" remainder.

**Spacing** 8px grid: 8/16/24/40/64/96. **Radius** panel 24 / card 18 / pill 100.
**Shadow** one soft max: `0 16px 45px rgba(16,24,40,.06)`.

**Interactions to reuse:** eyebrow pulse (disabled under `prefers-reduced-motion`); card
hover lift; and the **copy-citation** behaviour — `.cd-cite` with `data-cite-title` and
`data-cite-url`, building `CompanyDebt (2026) '<title>'. Available at: <url> (Accessed:
<today en-GB long date>).` with `navigator.clipboard` + `execCommand` fallback and a
transient "Copied to clipboard" status.

---

## Page structure (top → bottom)

1. **Masthead**
2. **Header** + colophon
3. **Data-sources strip** (Department for Business and Trade)
4. **KPI strip** — wide, 12-col, four `span 3` cards (figures below)
5. **Chart A — "How long large companies take to pay"**: monthly/period **column chart**
   of average days to pay across reporting periods (representative series).
6. **Chart B (centrepiece) — "Where invoices land"**: a single **horizontal stacked bar**
   (or three stacked bars on a shared scale) showing the split *paid within 30 days /
   31–60 days / 61+ days*, with a bold serif callout: "About **1 in 3 invoices** are paid
   outside agreed terms." No pie chart.
7. **Sector table** — "Payment performance by sector" (full table below).
8. **Amber caveat** (`.cd-caveat`): "Payment-practices figures are self-reported by large
   businesses. They describe payment behaviour, not insolvency. Slow payment is a
   pressure on suppliers, not a measure of the reporting company's own solvency." Support
   stat: the headline % paid late.
9. **Cite this data** block (`.cd-cite`, standard width) — `data-cite-title="Payment
   Practices & Late Payment"`, `data-cite-url="https://www.companydebt.com/data/company-insolvency/payment-practices-late-payment/"`.
10. **One advice CTA** (standard width): heading e.g. "Chasing unpaid invoices and running
    out of road?" + one orange button "Talk to our insolvency team →" to `/contact-us/`.
11. **Footer** prose note (sources + the representative-data caveat).

Also: add a directory card for this page on `company-insolvency-data-hub.html` under a
"Supplier payment" section (badge: Latest), linking to
`payment-practices-late-payment.html`, matching the existing card markup.

---

## Copy

**Standfirst:** "Large UK companies must report how quickly they pay their suppliers.
Late payment drains cash from smaller firms and is a common trigger for insolvency. This
page tracks how long big companies take to pay, how many invoices are paid late, and
which sectors are slowest."

**Eyebrow:** "Supplier payment".

---

## Figures (representative — label as such, wire live data in)

These are coherent, realistic **representative** values consistent with how the other
pages handle data: build the page with them, and note in the footer that values are
representative sample data pending the live six-monthly series from the Payment Practices
service. Do not present them as a verified official release.

**KPI strip (latest reporting period, representative):**
- **36 days** — average time to pay an invoice · *Across all reporting businesses*
- **33%** — invoices paid **later** than agreed terms · *Not paid within agreed period*
- **54%** — invoices paid **within 30 days** · *Of all invoices reported*
- **~11,000** — payment reports filed this period · *Large UK businesses in scope*

**Chart A — average days to pay (representative period series, H1 2024 → H2 2026):**
`39, 38, 38, 37, 37, 36` days.

**Chart B — where invoices land (representative, % of invoices):**
within 30 days **54%** · 31–60 days **31%** · 61+ days **15%**. Paid outside agreed
terms (late) **33%** (this is the headline callout; it cuts across the bands).

---

## Full sector table — "Payment performance by sector"

Columns: **Sector** · **Avg days to pay** · **% paid late** (outside agreed terms) ·
**% paid within 30 days**. Right-align the three numeric columns, `tabular-nums`. Sort by
**Avg days to pay**, slowest first. Representative values:

| Sector | Avg days to pay | % paid late | % paid within 30 days |
|---|---:|---:|---:|
| Construction | 43 | 41% | 44% |
| Manufacturing | 41 | 38% | 47% |
| Wholesale & Retail Trade | 39 | 36% | 50% |
| Transport & Storage | 38 | 35% | 51% |
| Administrative & Support Services | 37 | 34% | 52% |
| Accommodation & Food Service | 36 | 33% | 54% |
| Real Estate | 35 | 32% | 55% |
| Energy & Utilities | 34 | 31% | 57% |
| Professional, Scientific & Technical | 33 | 30% | 58% |
| Information & Communication | 32 | 28% | 60% |
| Health & Social Work | 31 | 27% | 62% |
| Agriculture, Forestry & Fishing | 30 | 26% | 63% |

Table source line: "Source: Department for Business and Trade, Payment Practices
Reporting. Figures are self-reported by businesses above the reporting threshold and are
representative sample values pending the live series."

---

## Chart rules

- **Hand-build every chart — no chart library, no `<canvas>`, no pie/donut charts.**
- **Column charts:** CSS flex bars inside a fixed-height plot, hairline baseline, text
  labels under each column; value labels in navy `tabular-nums`.
- **Stacked/where-invoices-land bar:** CSS-width segments on a shared 100% track (reuse
  the `.cd-scalebar` pattern from the dissolutions page); long values can sit outside the
  segment with a connector, exactly as that page does.
- **Any line series:** inline `<svg>` with `<polyline>` + `<circle>` dots + hairline
  gridlines + `<text>` axis labels (reuse the `.cd-linechart` classes).
- Every chart needs a `role="img"` + descriptive `aria-label`, a `.cd-legend` where it
  has 2+ series, and a `.cd-source` line beneath citing Department for Business and Trade.
- Wrap charts in `.cd-scroll` so they scroll horizontally on narrow screens.

---

## Output

A single file `payment-practices-late-payment.html`, all CSS inline under `.cd-data-hub`,
reusing the exact token block and component CSS from the existing pages, plus the
directory-card addition to the hub. Footer must note the representative-data caveat.
