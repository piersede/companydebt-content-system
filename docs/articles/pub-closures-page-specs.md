# Pub Closures - page build spec (design handoff)

Build-ready blueprint for refreshing **/articles/pub-closures-in-the-uk/** (WP post
id **24589**, post_type `post`). The data is already prepared in
`data/pub-closures/datasets.json` (figures) and `data/pub-closures/sources.json`
(attribution). This spec fixes structure, exact figures, caveats and the visual
list so the design step is purely visual.

**This is a `post`, not a data-hub `page`.** It does NOT sit inside `.cd-data-hub`,
so the Customizer 14px type-scale governance does not apply. Namespace the visuals
under a fresh wrapper class (e.g. `.cd-article-data`) so nothing collides with the
hub CSS.

## House rules (carried from the editorial brief)

- British English. Plain, factual copy ("There were...", "The rate was...", "This is not the same as...").
- **No em dashes anywhere** (hard AI signal on this site). Use commas, full stops or brackets.
- Company-authored insolvency-practice voice, not a single founder's first-person narrative. `we` sparingly.
- Every figure carries **definition + geography + period** inline. "Number of pubs", "pub closures" and "hospitality insolvencies" are different measures. Never merge them into one number.
- Every chart and table carries a visible **source line**.
- Volumes are not rates. A count of insolvencies is not an insolvency rate.
- Wider containers for data than for prose.
- One final advice CTA only. No generic related-content grid.
- Keep the existing internal links (they are the page's commercial value): liquidation, CVL, MVL, strike-off/dissolution, closing a limited company, winding-up petitions, CVA, administration, pre-pack, time-to-pay, insolvency, insolvency-calculator (30-second test). Weave them into the relevant new sections, not a footer dump.

## Rendering constraints (critical - so the build survives WordPress)

- Charts = **static inline `<svg>`**. Tables = **semantic `<table>`** (`<th scope>`, `<td class="cd-num">`). Both survive KSES with zero JavaScript. Follow the approach in `scripts/build_insolvency_charts.py`: hand-built SVG, restrained palette, `<title>` elements for tooltips, **no chart library, no pie charts**.
- Wrap the whole visual layer in a single `<!-- wp:html --> ... <!-- /wp:html -->` block with a scoped inline `<style>` under `.cd-article-data`.
- Put a `<!-- CD-NO-AUTOEDIT -->` sentinel as the first line of the draft so the internal-link and rewrite pipelines skip the file.
- **No inline `<script>` in content** (KSES strips it). If chart tabs / copy-citation / Dataset JSON-LD are wanted, they go in a slug-gated mu-plugin cloning `mu-plugins/cd-insolvency-data-hub.php` (gate on `post_name === 'pub-closures-in-the-uk'`). For a purely static build, skip this entirely.
- Deploy the assembled block with `scripts/wp_push.py --id 24589 --file drafts/24589_pub-closures-in-the-uk.html` (admin `wp_update_post`, KSES-bypassed) so the SVG + `<style>` persist. Do NOT push chart content through the REST/`staging_edit.py` path.

## Latest headline figures (as prepared)

- UK pub stock: ~45,000 (2024), down from 60,800 (2000) and 55,400 (2010). UK. HoC Library citing BBPA.
- Permanent losses: 366 pubs lost for good in England & Wales in 2025 (stock 38,989 -> 38,623). Ryan rating-list analysis.
- Recent closures: BBPA counted 161 closures across Britain in Q1 2026 (vs 128 in Q1 2025); 289 across E&W in 2024.
- Distress: 3,296 accommodation & food insolvencies in the 12 months to May 2026; sector insolvency rate 268 per 10,000 in 2025 (peak 314 in 2023), the highest of any sector every year since 2015.
- Cost pressure (ONS BICS, June 2026): 83% of accom & food firms report a turnover challenge; materials 48%, labour 48%, uncertainty 43%.

---

## Page structure (8 H2s)

**H1: Pub Closures in the UK** (keep the current title's intent; the "What's Behind the Decline" framing can stay as a subtitle if wanted).
Byline: Chris Andersen, Licensed Insolvency Practitioner. Reviewed date: set at publish.

### H2 1 - How many pubs have closed in the UK
Short answer first, then the definitions box. Lead sentence pairs both agreed framings:
the UK had around **45,000 pubs in 2024, down from 60,800 in 2000**, and recent data
shows the pressure has not eased, with **366 pubs permanently lost in England & Wales in 2025**
and **161 closures across Britain in Q1 2026**.
- Callout: three different measures explained in one line each (stock / permanent premise loss / company insolvency).
- Date stamp + link to the methodology box at the foot.

### H2 2 - UK pub numbers over time
- **Visual A: UK pubs over time** (line, `uk_pub_stock_over_time`). Points 2000 / 2010 / 2024. Source line: HoC Library citing BBPA.
- Supporting **table**: the same three values.
- Copy: one paragraph on the long-run structural decline. No cultural commentary here.

### H2 3 - Permanent pub closures in England and Wales
- **Visual B: Permanent pub losses, E&W** (bar, `permanent_losses_ew`) with an explicit definition note: "permanent loss = demolition or conversion; the stock total includes vacant and to-let pubs".
- **Visual C: Q1 comparison** (paired columns / stat box, `quarterly_closures_britain`): 128 (Q1 2025) -> 161 (Q1 2026), Britain.
- **Visual D: Closures by region 2025** (`regional_hotspots_2025`) - DATA GAP: only named regions are available (East Midlands, North West, Yorkshire & Humber). Render as a labelled list/callout, NOT a fabricated numeric chart, unless exact regional counts are sourced first.
- Method note: this is rating-list based, England & Wales only, and differs from UK stock and from insolvency counts.

### H2 4 - Pub insolvency and financial distress
- **Visual E: Hospitality insolvencies vs pub closures** (side-by-side small multiples, `hospitality_insolvencies` + a closures series) - the point of the visual is to show they are DIFFERENT systems.
- **Visual F: Births vs deaths** (clustered columns, `business_demography`): 30,360 births vs 26,195 deaths, 12.9% death rate, accom & food, 2024, UK.
- Stat line: sector insolvency rate 268 per 10,000 (2025), peak 314 (2023), highest of any sector since 2015.
- This is the natural home for the insolvency internal links (liquidation, CVL, administration, CVA, winding-up petitions, time-to-pay) and the 30-second insolvency test CTA.

### H2 5 - Why pubs are closing
Short subheads on measurable drivers only (demote Netflix / smoking ban / smartphones):
- **Labour** - NLW £12.71 (Apr 2026), employer NIC 15% from a £5,000 threshold (Apr 2025).
- **Business rates** - pub rateable values up 30% (70% with lodge) at the 2026 revaluation vs ~19.4% all-property; RHL multipliers 38.2p / 43p; 15% pub relief. England.
- **Tax / duty** - alcohol duty up 3.66% (Feb 2026); draught relief rate £19.45/litre vs £22.58 main beer.
- **Energy** - note non-domestic energy prices as a pressure (DESNZ quarterly; data extraction needed if charted).
- **Weaker drinking frequency** - one line pointing to H2 6.
- **Visual G: Cost-pressure survey** (horizontal bars, `cost_pressure_survey`): 83% / materials 48% / labour 48% / uncertainty 43%, ONS BICS June 2026.
- **Visual H: 2026 rates pressure** (comparison bars, `rates_revaluation_2026`): 30% / 70% / 19.4%.
- Optional **Visual I: cost-stack explainer** (annotated, `cost_stack_policy`) if design wants one consolidated graphic.

### H2 6 - Are pubs closing because people drink less
- **Visual J: Adults and drinking** (slope, `drinking_demand`): abstention 19% (2022) -> 24% (2024); 16-24 weekly drinking 30% (lowest group). NHS England, England only.
- **Visual K: Average pint price** (line, `pint_price_over_time`): 200p (2000) -> 477p (2024), ONS RPI.
- Copy: carefully separate demand (people drinking less) from affordability (price) and from off-trade vs on-trade. Do NOT overclaim the off-trade/on-trade split - the open evidence is weak (flag as a known limitation).
- The old "2014 supermarkets overtook pubs" and "beer duty 14x Germany" lines are removed unless a current, defensible source is added.

### H2 7 - What pub closures mean for communities
- Jobs and local impact (BBPA job-loss estimates, clearly labelled trade analysis).
- **Visual L: Community pubs** (stat cards / small table, `community_pubs`): 217 community-owned + 28 community-run (Apr 2025); 210+ trading (Jan 2026).
- Keep the "Friends on Tap" / Dunbar wellbeing material here, de-weighted, clearly older and not about closure counts.
- Conversions subsection: the Fleurets 34%-change-of-use stat lives here, framed as property transactions, not closures.

### H2 8 - Methodology and definitions
Sticky or expandable box:
- The page uses different primary sources for different metrics (list them: BBPA via HoC for stock; Ryan rating-list for permanent E&W loss; Insolvency Service + ONS for distress; GOV.UK/HMRC/VOA for the cost stack; NHS England for demand).
- Definitions of stock vs permanent loss vs insolvency; geography notes (UK vs GB vs E&W).
- Refresh cadence: closures & insolvency at least quarterly; policy figures on change.
- "How to cite" line.

---

## SEO / schema

- Keep the strong existing slug and internal-link equity. Title: keep "Pub Closures" intent; meta description should carry the headline stock + permanent-loss figures with year stamps.
- Schema (optional, via the slug-gated mu-plugin if used): Article + optionally Dataset for the chart data + FAQPage if an FAQ accordion is added (article_audit rewards a methodology + FAQ). BreadcrumbList.

## Open items to resolve before publish (do not fabricate)

1. **Source URLs**: `data/pub-closures/sources.json` marks most exact deep-links `verify`. Run a citation pass (WebFetch each publisher) to pin real URLs before the prose links go live.
2. **Regional 2025 counts**: not in the research pack. Source exact figures or keep Visual D as a named-region list.
3. **Pint price intermediate points**: only 2000 and 2024 endpoints are prepared; pull the ONS series if a fuller line is wanted.
4. **Energy prices**: DESNZ quarterly series needs extraction if Visual (energy) is charted.
5. **Human-authorship gate**: this is a hard pre-publish stop. Staging only until the named IP (Chris Andersen or reviewer) signs off.
