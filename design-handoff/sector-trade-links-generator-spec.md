# Spec: "Get the insolvency data for your trade" — registry-driven table

Applies to the flagship `uk-insolvency-statistics.html` (section `#sector-pages`) and,
by the same pattern, to `/data/company-insolvencies-by-sector/`.

## Goal
The trade table must be generated from the page registry, so that when a new
per-trade data page is published it appears in the table automatically — no manual
HTML edit. Editors add a page; the flagship picks it up on next build.

## Registry shape
Each detailed trade page is a registry entry. The generator needs these fields:

| field        | example                                             | notes |
|--------------|-----------------------------------------------------|-------|
| `slug`       | `construction-insolvency-statistics`                | page URL segment |
| `trade`      | `Construction`                                       | display name (col 1) |
| `sic_section`| `Construction`                                       | SIC industry section (used for ordering only, not shown) |
| `sic_rank`   | `1`                                                  | rank of that SIC section by insolvency volume (largest = 1) |
| `blurb`      | `The single largest sector by insolvency volume …`   | one-line scope note (≤ ~120 chars) |
| `published`  | `true`                                               | only `true` rows render |

`sic_section` / `sic_rank` drive sort order; the section column itself was removed
from the rendered table (user decision) — trades now sort by their section's volume
rank, then alphabetically within a section.

## Ordering
1. `sic_rank` ascending (Construction first, etc.)
2. `trade` alphabetical within the same section.

## Row template (per published entry)
```html
<tr>
  <th scope="row">
    <span class="cd-sectorlinks__name">{{trade}}</span>
    <span class="cd-sectorlinks__desc">{{blurb}}</span>
  </th>
  <td class="cd-sectorlinks__action">
    <a class="cd-sectorlinks__btn" href="/data/{{slug}}/">View data<span aria-hidden="true">&#8594;</span></a>
  </td>
</tr>
```

## Section wrapper (unchanged, emitted once)
```html
<section class="cd-section cd-w-wide" id="sector-pages">
  <div class="cd-section-head">
    <p class="cd-eyebrow">Detailed data</p>
    <h2>Get the insolvency data for your trade</h2>
    <p class="cd-section-intro">We publish a dedicated, monthly-updated data page for
      individual trades within the industry sections above. Find yours in the table and
      open its full time series.</p>
  </div>
  <div class="cd-tablewrap">
    <table class="cd-table cd-sectorlinks">
      <caption class="cd-table__caption">Detailed insolvency data pages by trade,
        grouped by SIC industry section.</caption>
      <thead>
        <tr><th scope="col">Trade or sub-sector</th>
            <th scope="col" class="cd-sectorlinks__actionhead">Data page</th></tr>
      </thead>
      <tbody>
        {{#each published_entries_sorted}} …row template… {{/each}}
      </tbody>
    </table>
  </div>
  <p class="cd-sectorlinks__all">
    <a href="/data/company-insolvencies-by-sector/">See all sectors and the full SIC
      breakdown <span aria-hidden="true">&#8594;</span></a>
  </p>
</section>
```

## Sticky-nav coupling
The wayfinding bar (`.cd-secnav`) must only list rendered sections. If the registry
yields zero published trade pages, omit BOTH the `#sector-pages` section and its
`<a href="#sector-pages">Trade data</a>` nav entry. Generate the nav from the list of
sections actually emitted — never hard-code links to sections that may be absent.
(This is the class of bug that produced the earlier dead `#procedures` link.)

## Notes
- `blurb` describes coverage, not figures — keep it out of the stats pipeline so it
  doesn't need a monthly data refresh.
- Escape `&` as `&amp;` in generated blurbs.
- The `<span aria-hidden="true">&#8594;</span>` is the only arrow; do not let the theme
  append its own link arrow (the page pins `.cd-sectorlinks__btn::after{content:none}`).
