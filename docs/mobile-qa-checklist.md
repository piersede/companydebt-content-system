# Mobile QA Checklist

Run this on every new page or significant redesign before considering it done — not on request, by default. Applies to the new page's own layout and content modules. Assume the site-wide header, menu, logo, footer and other existing global components already work unless this page has changed or broken them.

## Test sizes

Render at 320px, 360px, 390px, 430px, 768px, and resize gradually between them. Do not rely only on preset device emulation or assume existing breakpoints are correct.

## Overall mobile layout

- No horizontal page scrolling
- No text, image, card, table or control is clipped
- Desktop columns stack in the correct reading order
- The most important answer, data and primary CTA appear early
- Sections do not retain unsuitable desktop widths, heights or spacing
- No large blank areas from `min-height`, fixed heights or absolute positioning
- Page padding is consistent; content does not touch the screen edges
- Repeated cards/sections do not become excessively long or monotonous
- The page keeps clear hierarchy rather than becoming one continuous stack

Do not hide valuable content to make the layout fit — reformat it. Do not use `overflow-x: hidden` to conceal an overflow problem — find the element causing it.

## Hero and opening section

- H1 wraps naturally, not oversized
- Opening answer/proposition visible without excessive scrolling
- Supporting copy not too wide, too small or too long
- CTA buttons stack or wrap cleanly
- Statistics have clear labels, not unexplained numbers
- Imagery remains useful when cropped
- Decorative elements do not dominate the first screen
- Desktop height rules do not make the hero unnecessarily tall

## Typography and spacing

- Body and input text at least 16px
- Headings scale properly, no awkward breaks
- Line lengths and line heights stay readable
- Labels, captions and source notes stay legible
- Spacing clearly shows which heading belongs to which content
- Desktop + mobile margins do not combine into oversized gaps
- Cards do not retain excessive internal padding
- Content remains usable with increased browser text size

Do not shrink text to force a desktop component to fit.

## Cards, grids and content blocks

- Grids collapse at the point where content stops fitting
- Cards do not retain fixed desktop heights
- Headings, badges, prices and long names wrap properly
- Icons remain aligned with their text
- Buttons remain attached to the card/section they relate to
- Stacked cards remain easy to distinguish
- Alternating desktop layouts retain a logical mobile order
- No content depends on hover
- Accordions/tabs used only where they improve mobile usability

Use content-led breakpoints, not fixes for individual phone models.

## Tables and comparison sections

Do not squeeze tables until unreadable. Choose the most suitable treatment: contained horizontal scrolling, stacked comparison cards, a simplified mobile table, or fewer visible columns with secondary info still accessible.

- Column headings remain clear
- Values stay associated with the correct product/category
- Pricing, eligibility, warnings and key differences are not removed
- A scrollable table does not make the whole page scroll sideways
- Users can tell horizontal scrolling is available

## Forms and page-specific controls

Where the page has forms, calculators, filters, tabs, accordions or selectors, test with realistic content.

- Fields and controls fit the viewport
- Tap targets are large enough
- Labels remain visible
- Long options and error messages wrap properly
- Dropdowns and date controls work by touch

## Reporting

Report findings as: what's broken, at which breakpoint(s), why it matters, and the fix — not just a pass/fail. Fix real bugs found before calling the page done; note anything deferred and why.
