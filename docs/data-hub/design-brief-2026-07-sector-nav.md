# Brief 2 for Claude Design: sector navigation on the flagship

Company Debt (companydebt.com). Prepared 17 July 2026. Staging only.
Read alongside Brief 1 (visual alignment + flagship redesign). Same constraints apply.

---

## The problem, in one line

From the main statistics page you cannot get to any of the nine new sector pages.

## What is actually there now

`/data/uk-insolvency-statistics/`, the section with `id="sector"`, headed
**"UK Company Insolvencies by Sector"**:

- A horizontal bar chart ranking all 21 SIC industry sections by volume over the last 12 months.
  Construction leads on 3,803 (17% of known-sector cases), then wholesale and retail, then
  accommodation and food.
- Below it, one line of prose.
- **It carries exactly two links:** the sector overview, and construction.

We now have **ten** detailed sector pages sitting underneath this page. Nine of them are invisible
from it. A reader looks at a bar labelled "Accommodation and food service activities: 3,296" and
has no way to reach our hotel page or our restaurant page.

Piers's words: "I don't see any links or filters for the new sectors from the main page."

## What we want

A way to get from the main statistics page into a specific trade.

Piers's own suggestion, in his words: a dropdown where you select the relevant sector and the whole
page refreshes into it. That is a good instinct and it is the brief. How it should look and behave
is your call, within the constraints below.

---

## The design problem you have to solve

**The chart is SIC sections. The detail pages are SIC groups, one level down. It is not
one-to-one.** This is the thing that makes it harder than it looks.

| SIC section | Section total, 12 mths | Detail pages we have |
|---|---|---|
| F Construction | 3,803 | Construction (whole section) |
| G Wholesale and retail trade; repair of motor vehicles | 3,527 | Motor vehicle repair (SIC 452) |
| I Accommodation and food service | 3,296 | Hotels (SIC 551); Restaurants (SIC 561) |
| N Administrative and support services | 2,221 | Cleaning contractors (SIC 812); Recruitment agencies (SIC 781); Temporary staffing agencies (SIC 782) |
| C Manufacturing | 1,872 | Furniture manufacturing (SIC 310) |
| L Real estate activities | 924 | Estate agencies (SIC 683) |
| H Transportation and storage | 713 | Road haulage (SIC 494) |

Consequences you need to design around:

- **7 sections out of 21 have a detail page. 14 have none** (A, B, D, E, J, K, M, O, P, Q, R, S, T, U).
  So "make the bars clickable" fails: two thirds of them would go nowhere, and a chart where some
  bars are links and most are not is worse than a chart where none are.
- **One section holds three pages** (admin and support: cleaning, recruitment, temp staffing), so
  the relationship is one-to-many, not a simple lookup.
- **Construction is the odd one out**: it is a whole-section page, while the other nine are a
  single trade within a section.
- The set grows. More sector pages are coming, so whatever you design should not need
  hand-editing each time one is added.

## The ten pages

| Trade | URL |
|---|---|
| Construction | https://comdebstage.wpengine.com/data/construction-insolvency-statistics/ |
| Motor vehicle repair | https://comdebstage.wpengine.com/data/motor-vehicle-repair-insolvency-statistics/ |
| Hotels | https://comdebstage.wpengine.com/data/hotel-insolvency-statistics/ |
| Restaurants | https://comdebstage.wpengine.com/data/restaurant-insolvency-statistics/ |
| Cleaning contractors | https://comdebstage.wpengine.com/data/cleaning-company-insolvency-statistics/ |
| Recruitment agencies | https://comdebstage.wpengine.com/data/recruitment-agency-insolvency-statistics/ |
| Temporary staffing agencies | https://comdebstage.wpengine.com/data/temporary-staffing-agency-insolvency-statistics/ |
| Furniture manufacturing | https://comdebstage.wpengine.com/data/furniture-insolvency-statistics/ |
| Estate agencies | https://comdebstage.wpengine.com/data/estate-agency-insolvency-statistics/ |
| Road haulage | https://comdebstage.wpengine.com/data/road-haulage-insolvency-statistics/ |

## Already built, for reference

`/data/company-insolvencies-by-sector/` now has a working version of this: a plain link block
grouped by SIC section, sections ordered by size. Look at it before designing. Piers's steer there
was "just links is fine", so do not over-build. The flagship needs the same job doing with more
care, because it is the most valuable page in the section.

---

## Options, with our view

**1. A visible link block, grouped by section.** What the by-sector page does now. Safest, best for
search (visible crawlable links), no interaction cost. Least exciting.

**2. A dropdown.** What Piers asked for. Important technical note: **it must not require
JavaScript** (see constraints). Two ways:

   - **`<details>` / `<summary>` disclosure containing real links.** Looks and behaves like a
     dropdown, needs no JavaScript, is keyboard accessible natively, and the links stay real `<a
     href>` elements so they remain crawlable. **This is our suggestion** if you want the dropdown
     feel.
   - **A `<select>` that jumps on change.** Needs JavaScript, and it is an accessibility
     anti-pattern: a keyboard user arrowing through the options fires navigation on every one. If
     you want a `<select>`, it needs a separate "Go" button. We would rather avoid it.

**3. Clickable bars in the chart.** We think no, for the 14-of-21 reason above. Say so if you
disagree and can solve it.

A hybrid is fine: for example a compact dropdown for people who know the trade they want, plus the
grouped links visible for people who are browsing and for search engines.

---

## Constraints

All of Brief 1's constraints apply. The ones that bite hardest here:

1. **No JavaScript.** Mobile Lighthouse is already ~38 and JavaScript is the cause. This is why the
   `<details>` route is attractive.
2. **Links must be real `<a href>` elements.** These pages earn their traffic in search. A control
   that changes what is displayed without producing a link is worth much less to us, and Piers has
   already considered and rejected an in-place filter that swaps numbers without changing the URL.
3. **The HTML is generated by Python. Do not hand-edit it.** The flagship is generated by
   `scripts/build_insolvency_dashboard.py` into page 77399. Hand edits are lost at the next monthly
   data refresh. Send markup as a **spec** and Claude Code will build it into the generator, where
   it can be driven off the sector registry so new pages appear automatically.
4. **The bar chart is a generated SVG.** If your design touches it, that is a generator change, not
   a CSS change. Flag it clearly.
5. **Accessibility is a hard gate** (static 100 across the site). Whatever the control is, it must
   work by keyboard and be announced sensibly.
6. **Mobile is unproven and matters.** A dropdown on a phone is a different problem to a dropdown on
   a desktop. Please design both.

## Deliverables

1. The design for the sector navigation on the flagship: what the control is, where it sits in the
   page, and what it looks like on desktop and mobile.
2. A recommendation between the options above, with reasoning.
3. Markup as a **spec** (not HTML we paste), plus the CSS.
4. A note on whether the same pattern should replace the plain link block now live on
   `/data/company-insolvencies-by-sector/`, so the two pages behave consistently.

## Decisions already made, so you do not reopen them

- **Rejected:** a filter that swaps the numbers in place without changing the URL. No web address
  means nothing for search to send people to, it can only ever show shallow data, and it adds
  JavaScript to a page with a known mobile speed problem.
- **Accepted:** plain grouped links on `/data/company-insolvencies-by-sector/`. Already live.
- **Open:** whether the flagship gets the same plain links or something better. That is this brief.
