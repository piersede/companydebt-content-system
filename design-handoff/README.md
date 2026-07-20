# Handoff: CompanyDebt — UK Company Insolvency Data Hub

> **READ THIS FIRST — STATE AS OF THIS EXPORT.** This bundle was regenerated from the
> live files and supersedes any earlier copy. If you previously pulled this folder and
> the pages had a wider layout, a different/duplicated header, or no top nav menu — that
> was a stale snapshot. Rebuild from THESE files. Key facts that earlier copies got wrong:
> - There are **FIVE** pages, including **`payment-practices-late-payment.html`** (was
>   missing from earlier bundles entirely).
> - Every page is on a **single shared 1040px content rail** — there is NO separate
>   wider rail for charts anymore. One column, top to bottom.
> - Every page has a **masthead nav menu** (`.cd-mastnav`) with four tabs. Earlier copies
>   had no nav and a "Compiled from official sources" trust-mark in the masthead — that
>   mark has been **removed** from the masthead on all pages.
> - The dashboard's source logos are **real licensed files**, including DBT (no longer a
>   placeholder).

## Overview
A data product (not a blog or lead-gen site) presenting official, citable UK company
insolvency statistics for journalists, accountants, lenders and company directors. The
visual register is a serious statistical publication (think ONS / FT data journalism):
calm, factual, quotable. The bundle contains a **hub landing page** (directory + latest
headline numbers) plus **four data pages**.

## About the Design Files
These files are **design references created in HTML** — self-contained prototypes showing
the intended look, layout and behaviour. They are **not production code to copy directly**.
The task is to **recreate these designs in the target environment** (WordPress page
templates on companydebt.com) using its established patterns. Markup is deliberately clean
and CSS is scoped under a single wrapper class (`.cd-data-hub`) so it can drop into a
WordPress template with minimal change. The dashboard file (`uk-insolvency-statistics.html`)
is itself a real WordPress page export, so it shows exactly how the hub styles coexist with
the site chrome.

## Fidelity
**High-fidelity.** Final colours, typography, spacing, charts, grid and interactions are
all specified. Recreate pixel-accurately using the Design Tokens section.

## ⚠️ Data status — IMPORTANT
**All figures, charts and tables across the four data pages are representative SAMPLE
data**, flagged in each page footer. They are placeholders with realistic shapes, not real
statistics. Real official data must be wired in before publishing (see Data sources per
page below). Do not treat any number in these files as authoritative.

---

## The uniform grid (most important layout fact)
Every top-level block on every page — masthead, breadcrumb (dashboard only), hero/header,
data-sources strip, all section headings, KPI strips, **charts**, tables, chart captions,
caveats, citation block, CTA — sits on **one shared content column of `max-width: 1040px`,
centred, with 24px side padding**. All left and right edges line up vertically down the
whole page. There is intentionally **no "data is wider than prose" split** — an earlier
version had that and it was removed because the rails weren't concentric and looked broken.

- **Sibling pages** (hub landing, petition tracker, dissolutions, late payment): the rail
  is just `.cd-data-hub .cd-w-wide { max-width: 1040px; margin-inline:auto;
  padding-inline:24px }` and the same for `.cd-w-standard`. Simple and self-contained.
- **Dashboard** (`uk-insolvency-statistics.html`): because it's wrapped in WordPress
  container divs, the rail is enforced by an override block in `<head>` with id
  `#cd-hub-overrides`. Selectors are prefixed with `html ` purely to win specificity over
  the WP template's own rules. **This block lives in `<head>` on purpose** — placing it at
  end-of-body caused a visible layout flicker (FOUC) on load, because the page painted with
  the WP layout first and then reflowed. Keep override CSS in `<head>` when you reimplement.

When you rebuild in WordPress, the clean solution is to wrap every top-level block in one
container with a single `max-width: 1040px; margin: 0 auto` rather than re-deriving the rail
per block.

---

## Pages (in nav order)

All five share the same masthead: a **CompanyDebt brand lockup** (38×38 navy serif "CD"
square + serif "CompanyDebt" wordmark + muted "Insolvency Data Hub" sub-label) on the left,
and a **nav menu** (`.cd-mastnav`) of four tabs on the right:
Insolvency Statistics · Petition Tracker · Dissolutions · Late Payment. The current page's
tab carries `aria-current="page"` (accent pill). **The brand lockup links to `/`** (the main
site homepage), NOT to the hub landing page. The hub landing page is reached via the
directory cards and the "← UK Company Insolvency Data" back-links on the data pages. (If a
direct "back to hub" affordance is wanted in the menu, that's a known open option, not yet
built.)

### 1. Hub landing — `company-insolvency-data-hub.html`
Directory + latest headline numbers. Masthead → header (eyebrow, serif H1, standfirst,
publication colophon card) → data-sources strip → "Latest at a glance" KPI strip (4 cards)
→ directory sections of cards (single-item sections = full-width row card; the four live
data pages each link out; planned pages carry a "Planned" badge) → "Cite this data" block
→ one advice CTA. Its tab has no active state (it's the directory, not a peer page).

### 2. Monthly dashboard — `uk-insolvency-statistics.html`
The big one (real WP-page export). Breadcrumb → hero (H1 + standfirst + **stat-card**:
headline 2,085 with +2%/+3% deltas, a thin divider, then a demoted 2×2 grid of supporting
figures) → snapshot table → **monthly-by-procedure stacked column chart** (with a Post-Covid
/ 5-year segmented toggle — it owns *recent composition*) → **long-run line chart since 2000**
(owns the *historical arc*; has a quiet "what this means" side note) → insolvency-rate
section → "Learn about each procedure" compact link strip → sector chart → UK-nations table →
methodology → source/citation card → FAQ accordion → one adviser CTA. WP **footer kept**.
Data source: Insolvency Service (+ Companies House for register size).
- Snapshot table change columns use **directional colour** (muted red = rise in insolvency,
  muted green = fall) via `.cd-chg--bad/good/flat`, with `-webkit-text-fill-color` set
  because an ancestor sets it; `n/a` is light/inert (`.cd-chg--na`). Count columns are NOT
  coloured — only the deltas carry direction.
- The view-range toggle is a real segmented control (filled accent "selected" state).

### 3. Winding-Up Petition Tracker — `winding-up-petition-tracker.html`
Petitions advertised against UK companies. Header → data-sources strip → KPI strip (4) →
Chart A (monthly petitions, columns) → Chart B (petitions vs winding-up orders, two-series
line — the centrepiece) → lower two-column block (12-col grid, span 6 + span 6: left = a
latest-month notice breakdown table, right = stacked amber caveat + credibility note) →
cite block → CTA. Data source: The Gazette.

### 4. Company Dissolutions vs Insolvencies — `company-dissolutions-vs-insolvencies.html`
Shows most company closures are NOT insolvencies. Header → data-sources strip → KPI strip
(4) → Chart A (incorporations vs dissolutions, two-series line) → **Chart B (centrepiece):
shared-scale horizontal comparison** — dissolutions bar full width, formal insolvencies a
~3.5% sliver with its value rendered outside the sliver, plus a "28 companies for every
insolvency" callout → "Why most closures are not insolvencies" (lead + three reason cards,
12-col span 4) → amber caveat → cite block → CTA. Sources: Companies House + Insolvency
Service.

### 5. Payment Practices & Late Payment — `payment-practices-late-payment.html`
How slowly large companies pay suppliers. Header → data-sources strip (DBT) → KPI strip (4:
36 days / 33% late / 54% within 30 days / ~11,000 reports) → Chart A (avg days to pay, column
chart, 39→36) → **Chart B (centrepiece): horizontal stacked bar** (54% within 30 days / 31%
31–60 / 15% 61+) with a serif "1 in 3 invoices paid outside agreed terms" callout — **no pie
charts** → sector table (12 sectors, slowest first, three right-aligned numeric columns;
slowest three rows carry a quiet accent tick) → amber caveat (self-reported, behaviour not
insolvency) → cite block → CTA. Data source: Department for Business and Trade (Payment
Practices Reporting).

---

## Shared components
- **Masthead** (`.cd-masthead`) + **nav** (`.cd-mastnav`) — see Pages intro above.
- **Data-sources strip** (`.cd-srcstrip`): full-width band, top+bottom hairline, "DATA
  SOURCES" label + real source logos (`.cd-srclogo img`, ~74px tall, `object-fit:contain`,
  no captions — the logos self-label). Late-payment page keeps a text-chip fallback that
  shows only if the image 404s.
- **Publication colophon** (`.cd-colophon`): bordered card, "Publication" accent label, a
  `<dl>` of Series / Updated / Coverage / Compiled.
- **KPI card** (`.cd-kpi-card`): white, hairline, 18px radius, soft shadow; value in navy
  `#0a1f44`, tabular-nums.
- **Freshness badge** (`.cd-badge`): pill with leading dot — Latest (green), Provisional
  (amber), Planned (muted).
- **Caveat** (`.cd-caveat`): amber (`#fff7ed` bg, `#fed7aa` border, `#7c2d12` text) — the
  only warm panel, so it can't be missed. On the dashboard, "what this means" / "about" /
  "important note" callouts are standardised to a quiet muted **left-rule** treatment;
  filled panels are reserved for the citation block and the adviser CTA.
- **Cite block** (`.cd-cite`, dashboard `#cd-citation-text`): builds a Harvard-style citation
  on load — `CompanyDebt (2026) '<title>'. Available at: <url> (Accessed: <today, en-GB long
  date>).` URL from `data-cite-url` (fallback canonical → og:url → location.href); access
  date generated live with `toLocaleDateString('en-GB', …)`. Copy button uses
  `navigator.clipboard.writeText` with an `execCommand('copy')` fallback and a transient
  "Copied to clipboard" status. **Set `data-cite-url` per page in WordPress** (or drop it to
  use the live canonical URL). Verify the access date renders dynamically so it never goes
  stale.
- **Charts:** hand-built, **no chart library**. Column charts = CSS flex bars; line charts =
  inline `<svg>` polyline + circle dots + hairline gridlines + text axis labels; scale-gap
  and stacked bars = CSS-width horizontal bars. **Do not add chart libraries or new chart
  types when wiring in real data** — populate these structures.

## Interactions & responsive
- Card hover: lift (`translateY(-2px)`), border darkens, arrow nudges 3px. Eyebrow live-dot
  pulses (disabled under `prefers-reduced-motion`).
- Dashboard view-range toggle switches chart panes (generic `[data-cd-view]` /
  `[data-cd-view-pane]` JS).
- Responsive: KPI grids 4→2→1 at ~980/600px; lower two-column blocks stack at 980px; header
  two-column stacks at 900px; source logos shrink at 560px. **The masthead nav** can crowd
  on narrow widths — verify it wraps or collapses acceptably on mobile when reimplementing.
- This design environment previews at ~924px wide, so true desktop (≥1280px) behaviour
  should be re-checked on a real screen.

## Design Tokens
**Colour** — text `#101828`; text-soft `#1f2937`; muted `#667085`; hairline `#e4e7ec`;
hairline-soft `#eef0f3`; surface `#fff`; surface-soft `#f8fafc`; navy figures `#0a1f44`;
accent `#0f4c81`; accent-soft `#e8f1f8`; positive `#166534` / dot `#16a34a`; caveat amber bg
`#fff7ed` / border `#fed7aa` / text `#7c2d12`–`#9a3412`; CTA orange `#ec6608` (CTA buttons
only); directional deltas red `#b42318` / green `#15803d`, inert `#aab4c0`; scale-bar fills
dissolutions `#cdddee`, insolvencies `#0f4c81`; stacked-bar fills `#cdddee` / `#6a98c4` /
`#0f4c81`.

**Type** — body/sans: system stack. Display/serif: **Source Serif 4** (Google Fonts,
400/600/700) for H1s, chart/panel titles, caveat/CTA/cite headings, the brand wordmark, and
scale callouts; everything else stays sans. **Five-size scale only:** `--fs-1` 12px ·
`--fs-2` 15px · `--fs-3` 19px · `--fs-4` clamp(34px,3vw,44px) · `--fs-5` clamp(40px,5vw,56px).
H1 letter-spacing −0.02em; big figures −0.03em, tabular-nums.

**Spacing** — 8px grid: 8 / 16 / 24 / 40 / 64 / 96 (`--cd-s1`…`--cd-s6`).
**Radius** — panel 24px, card 18px, pills 100px. **Shadow** — one soft panel shadow max:
`0 16px 45px rgba(16,24,40,0.06)`. **Grid** — single 1040px rail (see grid section).

## Assets (`assets/`)
Real, licensed UK source logos, white margins auto-trimmed, no captions:
- `logo-companies-house-trim.png` — Companies House
- `logo-insolvency-service-trim.png` — The Insolvency Service
- `logo-gazette-trim.png` — The Gazette
- `logo-dbt-trim.png` — **Department for Business & Trade (real logo, in place)**
- `logo-ons.svg` — ONS, supplied but **not placed** (ONS isn't a source on any current page;
  add only where ONS data is actually used)
- Untrimmed originals are also present.
These are official Crown-copyright marks carrying the GOV.UK Royal Arms, supplied by the
client. Use the client's licensed files; do not recreate the crests. Fonts: Source Serif 4
via Google Fonts `<link>` (self-host in production).

## Files in this bundle
- `company-insolvency-data-hub.html` — hub landing
- `uk-insolvency-statistics.html` — monthly dashboard (large; real WP-page export)
- `winding-up-petition-tracker.html`
- `company-dissolutions-vs-insolvencies.html`
- `payment-practices-late-payment.html`
- `assets/` — source logos
- `payment-practices-design-prompt.md` — original brief for the payment page

All CSS is inline per file, scoped under `.cd-data-hub`. The four sibling pages share an
identical token block, type scale, and component CSS; the dashboard mirrors the same tokens
plus its own dashboard-specific styles and the `#cd-hub-overrides` grid block in `<head>`.

## Known non-issue
The dashboard logs a benign cross-origin `Script error. at ?:0:0` from its bundled
WordPress/jQuery scripts (note `jquery-migrate` loading). It has no line number, is not
produced by any hub markup, and can be ignored.

---

## Addendum — flagship page refinements (2026-07 session)

Applies to **`uk-insolvency-statistics.html`** only. This copy is current; rebuild the
flagship from it. Companion spec: **`sector-trade-links-generator-spec.md`** (registry-driven
trade table — read it before implementing the generator).

### 1. Layout system — single content rail + spacing rhythm
- Every band (masthead, hero, source strip, sticky nav, all sections, method band, final
  CTA, breadcrumb) sits on **one 1040px content column with an identical left edge**.
  Full-bleed sections span `100vw` but pad their content in to the rail via
  `padding-inline: max(24px, calc(50vw - 520px))`. Do NOT reintroduce per-section widths.
- Section rhythm: **104px between sections** (`.cd-section` margin-top) vs **16px between
  paragraphs** — the large gap is what signals a new section. Section-head bottom margin 40px.
  Keep section gap ≫ paragraph gap.
- Eyebrows are uniformly **12px / weight 750 / uppercase / 0.08em**. Note the methodology
  eyebrow is a `<p class="cd-eyebrow">` inside `.cd-method-inner`, so it is caught by the
  19px `.cd-method-inner p` rule — it needs a higher-specificity override
  (`body.page-template-data-hub-template .main-content .cd-data-hub .cd-method-inner .cd-eyebrow`)
  to stay 12px. Replicate that override in the port.
- Content-section backgrounds are all transparent (white). The **only** tinted band is the
  methodology band. Do not add alternating tints. (A stray dangling selector previously leaked
  the chart-controls `#eef2f7` tint onto `#longrun` — its eyebrow then sat flush on the tint
  edge. Gone now; don't recreate it.)

### 2. Reading-text scale (bumped from 14px)
- Body copy **16px / line-height 1.7**; data tables **15px**; source list, side-notes and
  FAQ answers **15px**; section intro/lede **18–19px**. True micro-labels (eyebrows, captions,
  chart tabs, legend, meta) stay **12px**. Row headers in tables weight 550.

### 3. "Get the insolvency data for your trade" — `#sector-pages`
- Replaced an earlier hidden `<details>` disclosure with an **always-visible two-column
  table**: col 1 = trade name + one-line scope note (`.cd-sectorlinks__name` /
  `.cd-sectorlinks__desc`), col 2 = solid navy **View data** button linking to that trade's
  page. Left-aligned; stacks to block rows below 700px.
- **Must be generated from the page registry** so new trade pages appear automatically —
  see `sector-trade-links-generator-spec.md`. Couple the sticky nav to emitted sections only
  (an absent section must not get a nav link — that class of bug produced a dead `#procedures`
  link earlier).
- The theme appends its own link arrow via `::after`; the button pins
  `.cd-sectorlinks__btn::after{content:none}` and forces `color:#fff !important`. Keep both.

### 4. Mid-page advisory (`.cd-advisory`) in `#rate`
- A single calm CTA bar, a **direct child of the `#rate` section** (full rail width, below
  the two-column rate grid — NOT inside the left text column). Layout is
  `display:flex; justify-content:space-between; align-items:center`: message left, solid navy
  button pinned right. Stacks to column below 640px. This is the only mid-page advisory;
  the primary advice CTA remains the final band.

### 5. Side-notes card (`.cd-side-notes`, "What this means")
- Rendered as a **card**: surface-soft background, 3px navy left border, 14px radius,
  padding `36px 28px 30px` (top padding matches the chart panel so the heading aligns with
  the chart top). It was excluded from the minimalist transparent/slate-border override that
  still applies to `.cd-caveat` / `.cd-side-note--single`. Keep that exclusion.

### 6. Mobile QA (320 / 360 / 390 / 430 / 768px) — all pass
- No horizontal page scroll at any width. Data tables use **contained horizontal scroll**
  (`.cd-tablewrap{overflow-x:auto}`, table `min-width:560px`) — they never push the page.
- All desktop grids stack to one column on phones (long-run, rate, mini-KPI, inline
  section-head, citation, meta); mini-KPI and meta go 2-up at 768.
- **Tap targets ≥ 44px** on the sector button, chart toggle tabs and sticky-nav links.
  Important: the WP theme forces `a { display:inline }`, so the sector button needs
  `display:inline-flex !important` for its `min-height:44px` to take effect. Preserve this
  in the port (or use the codebase's button component, which should already satisfy 44px).

### 7. Data note
- Construction is stated as **3,827 (16%)** everywhere; this matches the sector bar's own
  geometry and is internally consistent. (An external brief said 3,803/17%; that value is not
  used on the page.) All figures remain **representative sample data** per the data-status
  warning above.

