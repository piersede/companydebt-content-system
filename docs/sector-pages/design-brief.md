# Sector Pages — Design Brief (for Claude Design)

## What this is

A visual design for Company Debt's **/sectors/** pages. There are **25 of them**
(construction, care homes, restaurants, haulage, hotels, retail, manufacturing,
property, and so on). They are being rewritten from thin templated pages into
proper, researched articles. **Construction is the pilot and the mould** — design
it so the same styling drops onto all 25.

- Page type: WordPress `post` in the `sectors` category, template
  `templates/post-sectors.php`. Body carries `body.category-sectors`.
- Live pilot (staging): https://comdebstage.wpengine.com/sectors/construction/
  (behind WP Engine basic auth).
- **Content + structure reference file:** `construction-sector-template.html`
  (a clean, self-contained HTML export of the page content, with component
  classes intact). Design against this.

## Page structure (fixed — do not change the content or headings)

```
Breadcrumb  ·  H1  ·  author byline (photo, "Reviewed on <date>", read time)
Intro (2-3 paragraphs)
H2  Insolvency in the [Sector] Sector      -> leads with the SNAPSHOT box
H2  What's Driving [Sector] Insolvencies   -> H3 subsections
H2  Warning Signs a [Sector] Business Is Insolvent
H2  When a Main Contractor Fails ...        -> sector-specific deep-dive, H3s
H2  Your Options if a [Sector] Company Can't Pay
H2  Frequently Asked Questions ...          -> FAQ accordion
H2  Related Guides: ...                      -> final H2
Methodology & Disclosure  (aside)
Sources & References       (aside)
```

## Components to design (these are the whole job)

1. **`.cd-callout--summary` info boxes.** Used 4 times on Construction:
   - the dated **"snapshot"** box (the sector's key numbers, refreshed monthly),
   - a **"what could change"** reform box,
   - a **"figures to check"** box,
   - a **"first actions"** box.
   They are simple labelled boxes: a bold lead line then several short lines,
   each usually `<strong>Label:</strong> value`. Design ONE flexible box style
   that reads as an at-a-glance panel. The snapshot box is the hero of these;
   consider a distinct treatment (it holds the live data).
   IMPORTANT: a legacy global script (`cd-callout-summary-cards` in
   `theme/footer.php`) tries to re-card these into a `.cd-callout__grid`; on
   sector pages that is currently neutralised (see interim fix). Decide whether
   to design the card treatment properly for these pages or keep the clean box
   and leave the transform disabled here.

2. **FAQ accordion.** Ultimate Blocks `ub/content-toggle` (collapsible Q&A).
   Needs a clean, on-brand accordion: question row + chevron, expand/collapse,
   readable answer. NOTE: a legacy `cd-faq-icon` injection renders a ~946px icon
   with no sizing CSS on this template — currently hidden by the interim fix.
   Decide: a small, correctly-sized FAQ icon, or none.

3. **`.cd-methodology` and `.cd-sources` asides.** Footer trust blocks: a bold
   label then small-print body / a reference list. Quiet, credible styling,
   clearly separated from the article body.

4. **Author hero, breadcrumb, headings, links, lists.** Already render acceptably
   from the theme; bring them into the sector look.

## Known template issues to resolve in the design

- The sector template runs several **legacy transforms from the old design**
  (`cd-callout-summary-cards`, `cd-faq-icon`, `cd-pressure-points-icons`,
  `cd-faq-showonlyone`) that assume old markup and have no matching CSS here.
  The pressure-points one is now a no-op (its target markup is gone); the other
  two are neutralised by an interim fix. The proper design should either style
  these components correctly or confirm they stay disabled on sector pages.
- **~96px of horizontal overflow** on the page (minor). Track down and remove
  (likely a full-width element or the accordion inner width).
- Styling should be **responsive** and work as the shared mould for all 25 pages.

## Interim containment (remove when the design ships)

`mu-plugins/cd-sector-containment2.php` is a temporary, scoped CSS patch that (a)
hides the 946px FAQ icon and (b) reverts the callout-card transform to a clean
single box, so staging is presentable while this design is built. Delete it once
the sector styles land.

## The dated-snapshot pattern (build for updates)

The snapshot box holds every time-specific number ("England and Wales, 12 months
to <month>"). It is refreshed on each monthly Insolvency Service release. Style
it so a data refresh is just a content swap, and so a clear "as at <date>" line
always reads as current.
