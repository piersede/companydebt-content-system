# Brief for Claude Design: insolvency data hub (visual alignment + flagship redesign)

Company Debt (companydebt.com). Prepared 17 July 2026. Everything below is on **staging**, not live.

---

## What you are looking at

18 statistics pages under `/data/`, covering UK company insolvency data. They are the site's
data hub. They were built as a standalone design and have drifted away from the rest of the
site. Nine of them are detailed sector pages (hotels, garages, recruitment agencies and so on).

**Two jobs:**

1. Bring the whole `/data/` section into line with the rest of the site: fonts, the pale blue
   hero band, and one consistent spacing rhythm.
2. Redesign the flagship page, `/data/uk-insolvency-statistics/`, from scratch. It is the most
   important page in the section and it is not good enough.

---

## Links

Staging sits behind two gates: an nginx basic-auth prompt, then a WordPress login. Piers will
supply both separately. Do not put credentials in a URL.

| What | URL |
|---|---|
| **Flagship (redesign this one)** | https://comdebstage.wpengine.com/data/uk-insolvency-statistics/ |
| Hub / section index | https://comdebstage.wpengine.com/data/ |
| Sector page (recent, good content) | https://comdebstage.wpengine.com/data/hotel-insolvency-statistics/ |
| Sector page (heavy on tables) | https://comdebstage.wpengine.com/data/motor-vehicle-repair-insolvency-statistics/ |
| Sector overview | https://comdebstage.wpengine.com/data/company-insolvencies-by-sector/ |
| **Reference: a normal site page** (this is the look to match) | https://comdebstage.wpengine.com/liquidation/creditors-voluntary-liquidation/ |

---

## Read this first: why the section looks different

This is not a few stray CSS values. It is an architectural split.

- Every normal page on the site carries the body class **`cd-ttt-design`**. The theme's design
  system is scoped to that class (`body.cd-ttt-design .col-12.page-header { ... }`).
- **No `/data/` page carries `cd-ttt-design`.** They render on a separate page template
  (`data-hub-template.php`) and ship their own inline `<style>` block with a complete, parallel
  design language.

So the data hub is a design island. Aligning it means reconciling two systems, and the first
decision to make is whether `/data/` should adopt `cd-ttt-design` or keep its own scope and
merely match it visually. Please give a recommendation with your reasoning. It is the biggest
call in this job.

### The divergence, concretely

| | Rest of the site | `/data/` pages |
|---|---|---|
| Body class | `cd-ttt-design` | (absent) |
| Font | `Arial, sans-serif !important` | `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif` |
| Second font | none | `--cd-serif: "Source Serif 4", Georgia, "Times New Roman", serif` (used for figures/headings) |
| Hero | Full-bleed pale blue band, `.col-12.page-header::before`, `width:100vw; margin-left:-50vw` | White / near-white panels. No band. |
| Hero spacing | `padding-top:35px; padding-bottom:54px; margin-bottom:72px` | `--cd-space-section: 96px` / `--cd-space-section-small: 64px` |
| H1 | `font-size:48px; line-height:1.05; max-width:800px` | own scale |

---

## Job 1: alignment

### 1a. Fonts

Target: **Arial, sans-serif**, matching the rest of the site.

The data hub currently uses a system-UI stack plus **Source Serif 4** for large figures and some
headings. Dropping the serif is a real visual change to every data page, not a find-and-replace.

**Question for Piers (please confirm before doing the work):** does the serif go entirely, or is
it kept as a deliberate accent for the big numbers only? Our steer is that "in line with the rest
of the site" means Arial throughout and the serif goes, but say if you disagree.

### 1b. The hero colour

The rest of the site renders its hero as a full-bleed pale blue band. The colour has been
overridden three times in the theme stylesheet; the one that actually wins is:

```
#f4f7fe    <- the hero band the rest of the site actually renders (use this)
```

Superseded values still present in the stylesheet, listed so you do not resurrect one by mistake:
`#EAF2F8`, then `#f8f9fd`, then `#f4f7fe` (last wins).

There is also a theme token `--c-blue-light: #e7f6fd`, which is a slightly different pale blue and
is **not** what the hero currently renders. Use `#f4f7fe` unless Piers says otherwise.

The mechanism to copy:

```css
body.cd-ttt-design .col-12.page-header::before {
  content: '';
  position: absolute;
  top: 0; bottom: 0; left: 50%;
  width: 100vw; margin-left: -50vw;
  background: #f4f7fe;
  z-index: -1;
}
```

Note the `100vw` full-bleed pattern. There is a comment in the data-hub CSS warning that this
pattern is the known cause of horizontal scroll on that section, so if you reuse it, check for
overflow at narrow widths.

### 1c. Spacing

Pick one rhythm and apply it across all 18 pages. Site hero is 35/54/72; the data hub works in
96/64. They should not both exist.

### 1d. Colour tokens

Two parallel palettes currently say almost the same thing in slightly different values. Worth
collapsing.

**Theme (the rest of the site):**
```
--c-blue-dark    #002856      (also the link colour, rgb(0,40,86))
--c-blue-light   #e7f6fd
--c-blue-medium  #98b0c5
--c-orange       #f60
--navy-900       #102A43      --navy-800  #1F3C5A      --navy-700  #2F4F6F
--text-primary   #1F2933      --text-secondary #52606D  --text-muted #7B8794
--accent-blue    #2B6CB0
--bg-soft        #F7FAFC
```

**Data hub (the island):**
```
--cd-accent       #0f4c81     --cd-accent-soft  #e8f1f8
--cd-figure       #0a1f44
--cd-text         #101828     --cd-text-soft    #1f2937     --cd-muted  #667085
--cd-line         #e4e7ec     --cd-line-soft    #eef0f3
--cd-surface      #ffffff     --cd-surface-soft #f8fafc     --cd-surface-band #f6f8fb
--cd-cta-band     #f3f7fb     --cd-cta-orange   #ec6608
--cd-positive     #166534     --cd-positive-dot #16a34a
--cd-radius-panel 24px        --cd-radius-card  18px        --cd-radius-hero  22px
--cd-space-section 96px       --cd-space-section-small 64px
```

Look at the near-misses: `#0f4c81` vs `#002856` for the accent, `#101828` vs `#1F2933` for body
text, `#ec6608` vs `#f60` for orange. These are two designers solving the same problem twice.

**Careful with orange:** brand orange and link contrast have been reverted once before during an
accessibility pass because the change broke the brand. Treat orange as fixed unless Piers says
otherwise.

---

## Job 2: flagship redesign

`/data/uk-insolvency-statistics/` is the monthly headline dashboard, and the most valuable page in
the section. Piers's view is that it is not good. A full redesign is in scope: layout,
hierarchy, how the charts and KPI panels are presented.

Its current sections, in order:

1. Latest UK Company Insolvency Figures
2. Monthly Company Insolvencies by Procedure
3. Long-Run UK Company Insolvency Trends Since 2000
4. UK Company Insolvency Rate (May 2026)
5. UK Company Insolvencies by Procedure Type
6. UK Company Insolvencies by Sector
7. UK Company Insolvencies by Jurisdiction
8. Methodology
9. Source and Citation
10. Frequently Asked Questions
11. Related Guides

Content notes that should shape the design:

- The page's job is for a **worried company director**, not an analyst. It should answer "is this
  happening to everyone or just me?" quickly, then route them to the sector pages and to advice.
- It is also a **citation target**. Journalists and AI answer engines lift figures from it, so the
  numbers, the "as at" date and the source line must stay prominent and unambiguous.
- The section now has nine detailed sector pages under it. The flagship should route into them
  much more strongly than it does; currently it only links to the sector overview.

---

## Hard constraints (please read, these will bite)

1. **The page HTML is machine-generated by Python. Do not hand-edit it.**
   Every data page begins with a sentinel comment:
   `<!-- CD-NO-AUTOEDIT: data_reference page generated by scripts/datahub/pages/... -->`
   Anything you change in the HTML is overwritten at the next monthly data refresh.
   - Deliver **CSS as CSS**, which we can apply directly.
   - Deliver **markup/structure changes as a written spec**, and Claude Code will implement them
     in the generator so they survive the refresh.

2. **There is un-versioned CSS in the WordPress Customizer that beats everything.**
   Appearance → Customise → Additional CSS contains **~22.9KB**, with **105 `!important`
   declarations** and **148 `.cd-` rules**. It is not in the git repo, it is not in the theme, and
   it overrides both. On the flagship specifically, the type scale is governed from there.
   - If a change "does not apply", this is why. Check it first.
   - Reducing it is desirable. Say so if your design lets us delete chunks of it.

3. **No JavaScript.** Mobile performance is already poor (Lighthouse ~38 on mobile, desktop 98),
   and the cause is JavaScript. CSS-only solutions please. Inline scripts are stripped by
   WordPress KSES anyway and have to be loaded via an mu-plugin, so they are expensive in every
   sense.

4. **Accessibility is a hard gate.** The site holds a static 100 score. Keep visible focus states,
   do not rely on colour alone to convey meaning, and keep contrast ratios. A previous
   accessibility-driven change to link and orange contrast was reverted for brand reasons, so if
   you hit a brand-versus-contrast conflict, flag it rather than deciding.

5. **Tables must stay inside `.cd-tablewrap`**, which is the horizontal-scroll container. Sector
   pages have four tables each and they must not break the page width on a phone.

6. **Mobile matters and is currently unproven.** We have not been able to render these pages on a
   real sub-720px device. There are `@media (max-width: 720px)` rules covering the tables, KPI
   grid and chart panels. Please treat mobile as a first-class deliverable, not a checked box.

7. Do not put credentials in any URL.

---

## Deliverables

1. **A recommendation on the architecture:** does `/data/` adopt `cd-ttt-design`, or keep its own
   scope and match it visually? With reasoning. This decides the shape of everything else.
2. **CSS** implementing the alignment (fonts, hero band, spacing, tokens) across all 18 pages.
3. **A written spec** for any markup or structural changes, since we implement those in the
   Python generator rather than by hand.
4. **The flagship redesign**, as CSS plus a structural spec.
5. **A note on what can be deleted from the Customizer** once your CSS lands.

---

## Answers you will probably want

- **Are these live?** No. Staging only. There is no time pressure from a live deadline.
- **How many pages does the alignment touch?** 18 under `/data/`. They share one inline CSS block,
  so this is mostly one stylesheet, not 18.
- **Can we change the content?** Not in this job. The nine sector pages were rewritten in July 2026
  and are signed off pending review. Design only.
- **House style, if you write any UI copy:** British spelling, plain English, and no em dashes.
  Em dashes are treated as an AI tell and are banned across the site.
