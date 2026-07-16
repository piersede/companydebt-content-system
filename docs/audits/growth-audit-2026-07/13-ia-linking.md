# Information Architecture & Internal Linking Audit — companydebt.com

Growth-audit lens 4d/f. Date: 2026-07-10. Sources: Ahrefs API v3 (pages-by-internal-links, linked-anchors-internal, pages-by-backlinks, all pulled live during this audit), live-page fetches (read-only), and the foundation briefs (inventory/Ahrefs/GSC/business/competitors). Facts are labelled VERIFIED (measured in this session) or INFERENCE.

---

## 1. Executive summary

The site runs a **two-tier internal-link economy**. Roughly 36 URLs — the nav, footer and template slots — each receive ~155–206 internal links; everything else falls off a cliff to ≤69, and most of the ~190 informational pages sit at 1–5 internal links, fed only by "Related Guides" blocks and breadcrumbs. There is almost **no contextual in-content linking layer**: the flagship CVL money page's 202 internal links are 194 copies of the identical nav anchor, 7 empty image links, and exactly 1 unique in-content anchor (VERIFIED). Internal linking currently does one job (navigation chrome) and neither of the two jobs the brief asks about — moving users to the next journey stage is done patchily by hand on refreshed pages, and consolidating authority onto priority commercial pages is essentially not done at all.

Three structural failures matter most:

1. **The /liquidation/ "hub" is a hub in URL only.** It links to the 6 nav service pages and nothing else — not to its own cost page and not to any of its ~61 long-tail children (VERIFIED). Its 242k GSC impressions and 22 referring domains (the best-linked real deep page on the site) push equity nowhere.
2. **The new /data/ section is floating.** Every /data/ page has 1–5 internal links, while the *superseded* /uk-insolvency-statistics/ URL holds the sitewide footer slot worth 192 internal links (VERIFIED). The one asset built to earn links has no internal plumbing to receive or distribute them.
3. **External equity leaks and pools in the wrong places.** Live external links still point at 404s (veterans page: 17 refdomains; hmrc-office-locations: 8) and at 301'd legacy linkbait (/features/124-pints/ 16 RDs, /coronavirus-business-help/ 12 RDs, dead http CVL paths 12+9 RDs), while the current CVL URL doesn't even make the top-30 pages by referring domains (VERIFIED).

---

## 2. Navigation and the sitewide template tier

### 2.1 What the nav actually contains (VERIFIED, live fetch of homepage)

Five menus, 23 destination items:

- **Company Closure**: /liquidation/, CVL, MVL, strike-off, /closing-a-limited-company/, /winding-up-petitions/, compulsory
- **Company Rescue**: CVA, /company-administration/, /what-is-a-pre-pack-administration/
- **Tax Debt**: /hmrc/time-to-pay-hmrc/, cant-pay-vat, problems-paying-corporation-tax-hmrc, cant-pay-paye
- **Advice**: /insolvency/, are-directors-personally-liable, what-happens-to-directors-in-liquidation, /bounce-back-loan-support-hub/what-happens-if-i-default/, cant-afford-to-pay-suppliers, limited-company-bankruptcy, get-free-business-debt-advice
- **About Us**: meet-the-team, contact-us

The footer mirrors the nav service links and adds legal pages plus **"UK Insolvency Statistics" → /uk-insolvency-statistics/** (the legacy URL, not /data/).

### 2.2 The measured template tier (VERIFIED, Ahrefs pages-by-internal-links)

Top of the distribution (links_to_target, all dofollow):

| URL | Internal links |
|---|---|
| /winding-up-petitions/ | 206 |
| / (homepage) | 205 |
| /liquidation/creditors-voluntary-liquidation/ | 201 |
| /insolvency/ | 201 |
| /company-administration/ | 201 |
| /hmrc/time-to-pay-hmrc/ | 199 |
| /about-us/ | 199 |
| CVA page | 198 |
| /hmrc/problems-paying-corporation-tax-hmrc/ | 197 |
| /liquidation/ | 197 |
| /hmrc/cant-pay-vat/ | 196 |
| /liquidation/members-voluntary-liquidation/ | 196 |
| ... ~20 more nav/footer/template URLs ... | 155–196 |
| **/uk-insolvency-statistics/ (legacy)** | **192** |
| /stressed-directors-guide/ | 159 |
| /insolvency-calculator/ | 157 |
| /author/chrisandersen/ | 156 |
| — cliff — | |
| /company-rescue-solutions/pre-packs/pre-pack-faq/ | 69 |
| /hmrc/ | 31 |
| /advice/ | 21 |
| /sectors/ | 20 |
| /liquidation-hub/ | 18 |
| /quick-quote/ | 16 |
| /liquidation/how-much-does-liquidation-cost/ | **11** |
| /data/uk-insolvency-statistics/ | **5** |
| /data/ | **4** |

Everything below the cliff is fed by breadcrumbs (section hubs /hmrc/ 31, /advice/ 21 ≈ their child counts) and Related Guides blocks (long-tail pages at 2–5).

### 2.3 Judgement on the tier allocation

The nav is commercially sane at the top (all four HMRC money pages, all liquidation routes, WUP) — the survival of the cant-pay-* cluster at #2 is partly this tier's doing. But three slots are misallocated:

- **/bounce-back-loan-support-hub/what-happens-if-i-default/** holds a full sitewide Advice slot (195 links) for a fading Covid-era query, while **/liquidation/how-much-does-liquidation-cost/** — pos 10.9–14.7 on "how much does liquidation cost" (GSC striking-distance cluster, CPC ~$10), holder of the PAA slot on the CVL SERP — gets 11 internal links.
- The footer statistics slot (192 links) props up the superseded /uk-insolvency-statistics/ instead of the /data/ hub.
- /author/chrisandersen/ at 156 links is defensible for E-E-A-T; the other three author pages get 1 link each (fine).

---

## 3. Section structure: /advice/ vs /articles/ vs /insolvency/ vs service paths

The taxonomy is **historical, not thematic** (INFERENCE from inventory + spot checks). Director-liability content lives in at least three sections (/advice/are-directors-personally-liable…, /insolvency/shareholders-liable…, /liquidation/what-happens-to-directors…); HMRC enforcement is split between /hmrc/ and /company-cash-flow-problems/; "closing a company" splits across /closing-a-limited-company/ (root), /liquidation/*, and /liquidation/company-strike-off-and-dissolution/*. Users never see this (nav flattens it), but it produces four consequences:

1. **Breadcrumbs are the only section glue.** E.g. cant-pay-vat: `Home › Help with HMRC Pressure › Can't Pay VAT…` (VERIFIED). Section hubs exist as breadcrumb targets but are not in the nav and hold no equity (31/21/16/12 links).
2. **Hub proliferation without inbound links**: /liquidation-hub/ (18), /liquidation/liquidation-hub/ (6), /guides-resources-hub/ (1), /debt-creditor-pressure-hub/ (8), /hmrc/hmrc-debt-enforcement-hub/ (5), /business-insolvency/articles-insights-hub/ (2), /sector-insolvency-hub/, /case-studies-hub/ (VERIFIED counts). These are index-bloat: near-zero internal links, near-zero external links, competing with the real section pages.
3. **Four competing sector layers, all starved**: /sectors/ archive 20 links; legacy posts (carehomes 5, leisure/automotive/charity/energy/travel/taxi/fish-chip 3 each); new root landing pages /construction-insolvency/ 3, /manufacturing-insolvency/ 3; plus two sector hub pages. Nothing in nav or footer points at any sector layer (VERIFIED for homepage). The 25-page sector rewrite programme is underway in the repo — the IA decision (which layer is canonical) should land **before** more rewritten pages are published into a structure where they get 3 internal links.
4. **Duplicate statistics location**: /uk-insolvency-statistics/ (192 internal links, live, current data, no visible pointer to having moved) coexists with /data/uk-insolvency-statistics/ (5 links). Both are in the sitemap. This splits internal equity, external citations from the active outreach programme, and crawl signals for exactly the asset class the whole data-layer strategy depends on. GSC shows "insolvency statistics" ranking ~9.4 — the ranking URL is almost certainly the legacy one given the link disparity (INFERENCE; check GSC page-level before acting).

### Depth

Max 3 path segments (inventory, VERIFIED); nothing is deep in URL terms. Real depth is *link* depth: any page not in nav/related-guides chains is 2 clicks from home via section hub breadcrumb at best, but with 1–4 inlinks its crawl priority is weak regardless.

---

## 4. Hub pages: the /liquidation/ hub failure (VERIFIED, two live fetches)

/liquidation/ — the page holding 5 head terms at pos 12–15, 242k impressions at 0.06% CTR, and 22 referring domains — links to:

- the same 10 nav service pages everyone gets,
- the insolvency calculator,
- a Related Guides block repeating CVL/compulsory/MVL/strike-off/CVA/WUP/insolvency.

It does **not** link to /liquidation/how-much-does-liquidation-cost/ (it quotes "Typical CVL fee: £4,000 to £6,000 + VAT" without linking the dedicated page), not to /liquidation-hub/, and not to a single one of its ~61 long-tail children (what-happens-to-employees, cant-afford-to-liquidate, can-i-liquidate-my-company-with-a-bounce-back-loan, etc.).

Consequences:
- **Journey failure**: a director on the hub with cost anxiety (the #1 commercial follow-up per GSC) has no click path to the cost page.
- **Consolidation failure**: the best-externally-linked deep page passes its 22-RD equity only to pages that already have 200 internal links.
- **Discovery failure**: the 61 children are crawl-findable only via each other's Related Guides blocks (2–5 links each).

The same pattern will hold for /hmrc/ and /insolvency/ hubs (INFERENCE — not individually fetched, but their link counts and the shared template make it near-certain).

## 5. The anchor monoculture (VERIFIED, linked-anchors-internal)

Internal anchors pointing at /liquidation/creditors-voluntary-liquidation/:

| Anchor | Links |
|---|---|
| "Creditors' Voluntary Liquidation (CVL)" (nav/footer) | 194 |
| "" (empty — image links) | 7 |
| "Creditors' Voluntary Liquidation (CVL): A Practical Guide for UK Directors" | 1 |

One unique contextual anchor site-wide, to the page targeting a 1,500/mo head term where the site ranks #39. Competitors ranking top-5 for CVL/MVL do so with <16 referring domains (competitor brief) — page-level relevance signals, which internal contextual anchors are the cheapest source of, are the plausible missing input (INFERENCE, consistent with "coverage not authority is the binding constraint").

Counter-example proving the capability exists: /hmrc/cant-pay-vat/ carries 10 varied in-content internal links (time-to-pay, CVA, WUP, statutory demand, corporation tax, creditor order, CVL, administration, alternatives-to-liquidation) — the recent Bernstein-refreshed pages do this well. The gap is the old estate and, critically, *inbound* links to money pages, not outbound from them.

## 6. Where external equity sits vs where internal links point (VERIFIED, pages-by-backlinks, live links only)

| URL | RDs | Status | Note |
|---|---|---|---|
| companydebt.com/ variants (4 URLs) | 409+348+45+13 | 301/200 | ~90% of all equity, homepage-bound |
| /hmrc-tax-problems/hmrc-redundancy-payments-directors/ | 91 | gone | 100% nofollow scraper spam — ignore |
| /liquidation/ | 22 | 200 | best genuine deep page |
| /what-support-is-available-for-military-veterans-starting-a-business/ | 17 | **404** | reclaim via redirect |
| /articles/124-pints-to-save-the-pub/ (+ /features/ 301 twin) | 16+16 | 200/301 | linkbait equity, passes nothing onward (2 internal outlinks measured to it; body links unaudited) |
| /bounce-back-loan-support-hub/ | 15 | 200 | 15 RDs sitting on a Covid hub |
| /articles/ | 13 | 200 | archive |
| /coronavirus-business-help/ | 12 | 301 | |
| http://…/liquidation/creditors-voluntary-liquidation(+/directors-guide) | 12+9 | 301/429 | CVL's real equity stranded on dead http paths (429 = bot-block noise, known Ahrefs artefact) |
| /articles/covid-19-effects-on-cruise-industry/ | 11 | 301 | |
| /winding-up-petitions/ | 10 | 200 | |
| /hmrc/hmrc-office-locations-uk/ | 8 | **404** | reclaim |
| /hmrc/time-to-pay-hmrc/ (+ /hmrc-tax-problems/ 301 twin) | 8+8 | 200/301 | |

Pattern: the pages that earn links (linkbait, data, news) have no designed onward path, and two 404s are leaking ~25 RDs that a Quick Redirects rule recovers in minutes.

## 7. /data/ wiring (VERIFIED)

- Inbound: /data/ 4 links; children 1–5 each (petition tracker 5, dissolutions 5, uk-insolvency-statistics 5, payment-practices 5, cvl-stats 3, by-sector 3, compulsory 2, administration 1, construction 1). Sole non-template source found: one homepage body line ("We maintain a UK insolvency data hub").
- Outbound: excellent. The /data/ hub links all 9 children AND the full service stack, with "Talk to our insolvency team" CTAs (VERIFIED live fetch). The section gives; it does not receive.
- The legacy /uk-insolvency-statistics/ page carries current May-2026 data, no relocation note, and holds the 192-link footer slot.

This is exactly backwards for the strategy: the /data/ section exists to earn journalist links whose equity should flow to money pages — which requires (a) crawlers finding/valuing the data pages (inbound links) and (b) the money pages citing them (they don't yet: cant-pay-vat's 10 body links include zero /data/ links).

## 8. Journey vs consolidation — kept separate, as briefed

**Journey linking (user's next step)** — grade B on refreshed pages, F at hubs:
- Good: money↔money cross-links (cant-pay-vat → TTP/CVL/administration), info→money funnels (shareholders-liable → CVL/liquidation/calculator, VERIFIED), universal phone/calculator CTAs.
- Broken: hub pages answer questions inline instead of routing (cost example); long-tail Q&A pages rely on generic Related Guides; dead ends at /testimonials/ pagination, author archives, /case-studies/ (2 inlinks), /site-map/.

**Consolidation linking (equity to priority pages)** — grade F:
- No contextual inbound layer to CVL/MVL/cost (Section 5).
- Equity-rich legacy pages (124-pints, BBL hub, /articles/ archive) don't push to matched commercial targets.
- The one sitewide slot pointing at statistics props the wrong URL.
- Linked 404s unredirected.

These need different mechanisms: journey links belong in page templates and hub design (blocks, decision paths); consolidation links belong in body prose with descriptive anchors, placed on the ~30 pages that actually have external equity or traffic.

---

## 9. Concrete link plan (from → to, anchor, rationale)

**Template/nav changes (one edit, sitewide effect):**

1. Footer "UK Insolvency Statistics" → change target /uk-insolvency-statistics/ ⇒ **/data/**, anchor "UK Insolvency Data & Statistics". Then (separate decision, after confirming /data/ visual QA + live push) 301 the legacy URL into /data/uk-insolvency-statistics/ via Quick Redirects and update the outreach conductor's target. Rationale: stop splitting the site's flagship link-earning asset; 192-link slot moves to the section built to receive citations.
2. Nav "Company Closure" — add "Liquidation Costs" ⇒ **/liquidation/how-much-does-liquidation-cost/**. Rationale: 11 → ~200 internal links for the striking-distance high-CPC cluster (pos 10.9–14.7); it already owns the PAA slot on the CVL SERP.
3. Nav "Advice" — swap /bounce-back-loan-support-hub/what-happens-if-i-default/ out for the cost page or /advice/directors-personal-guarantees/ if (2) is done another way. Rationale: reclaim a decaying Covid slot.

**Hub repair (journey):**

4. /liquidation/ fee section: link the sentence quoting "£4,000 to £6,000 + VAT" ⇒ /liquidation/how-much-does-liquidation-cost/, anchor "full breakdown of liquidation costs".
5. /liquidation/ — add 3 themed child blocks (Costs & affordability: how-much-does-liquidation-cost, cant-afford-to-liquidate, cheapest framing; People: what-happens-to-directors-in-liquidation, what-happens-to-employees, director-redundancy; Special cases: can-i-liquidate-my-company-with-a-bounce-back-loan, liquidating-an-llp, group companies). Rationale: routes the hub's 242k impressions and 22 RDs; makes 61 children crawl-reachable from their parent.
6. Same pattern for /hmrc/ and /insolvency/ hubs (breadcrumb-only today at 31/21 links).

**Consolidation (equity to money pages):**

7. /articles/124-pints-to-save-the-pub/ (16 RDs) ⇒ body links to /articles/pub-closures-in-the-uk/ (anchor "UK pub closures data") and /liquidation/ (anchor "options when a pub company can't pay its debts").
8. /bounce-back-loan-support-hub/ (15 RDs) ⇒ /liquidation/can-i-liquidate-my-company-with-a-bounce-back-loan/ (anchor "liquidate a company with an outstanding bounce back loan" — GSC pos 9.6, currently 3 internal links) and /liquidation/creditors-voluntary-liquidation/.
9. Top-10 GSC informational pages each get 1 varied-anchor body link into CVL and/or cost: e.g. /liquidation/what-happens-to-directors-in-liquidation/ ⇒ CVL ("entering a creditors' voluntary liquidation"); /closing-a-limited-company/ ⇒ cost page ("what liquidation costs in 2026"); /insolvency/limited-company-bankruptcy/ ⇒ CVL ("the formal CVL process"). Target: ≥8 unique contextual anchors into CVL within a quarter (from today's 1).
10. Redirect reclamation (Quick Redirects only, per infra rules): /what-support-is-available-for-military-veterans-starting-a-business/ (404, 17 RDs) ⇒ /advice/funding-options-for-smes-in-the-uk/; /hmrc/hmrc-office-locations-uk/ (404, 8 RDs) ⇒ /hmrc/ (or resurrect as HMRC-utility content — competitor brief shows RBR farms this exact long-tail).

**Data section wiring (both directions):**

11. Reciprocal pairs, body-level: /liquidation/creditors-voluntary-liquidation/ ⇄ /data/cvl-statistics/ ("latest CVL statistics"); /winding-up-petitions/ ⇄ /data/winding-up-petition-tracker/ ("live winding-up petition tracker" — also a differentiated SERP feature vs competitors); /company-administration/ ⇄ /data/administration-statistics/; /liquidation/company-strike-off-and-dissolution/ ⇄ /data/dissolutions-vs-insolvencies/; /construction-insolvency/ ⇄ /data/construction-insolvency-statistics/; /liquidation/compulsory-liquidation/ ⇄ /data/compulsory-liquidation-statistics/. Rationale: journalists arriving at data pages get a route to expertise pages; data pages get crawlable inbound links; sector/service pages get fresh-data E-E-A-T signals. (Data-page side must respect the CD-NO-AUTOEDIT sentinel — route through the data-hub build scripts, not link-injection.)

**Structural consolidation:**

12. Retire vestigial hubs: 301 /liquidation-hub/ and /liquidation/liquidation-hub/ ⇒ /liquidation/; /guides-resources-hub/ and /business-insolvency/articles-insights-hub/ ⇒ /articles/; fold /debt-creditor-pressure-hub/ into /company-cash-flow-problems/ or keep one, linked from the relevant section hub.
13. Sector layer decision before the rewrite programme publishes further: canonical = root-level /X-insolvency/ pages (matches the 8 newer landing pages and the rewrite direction); 301 the 8 direct legacy duplicates (/sectors/carehomes/ ⇒ /care-home-insolvency/, /sectors/construction/ ⇒ /construction-insolvency/, etc.); keep one sector index linked from the footer; retire /sector-insolvency-hub/ and /sector-specific-insolvency/.

---

## 10. What NOT to do

- Don't blanket-inject links into the 190 informational pages; the Bernstein/humanise pipeline already produces good outbound linking — the deficit is *inbound to money pages* and *hub design*, both fixable with ~40 targeted edits on the pages listed above.
- Don't nofollow or strip the legal/author template links; the tier-1 set is not the problem, its composition is.
- Don't add a fifth sector layer or a new "resources" hub; consolidate to one of each.
- Redirects only via Quick Redirects (repo hard rule); remember qppr rules vanish if a page is trashed — run the sentinel checker after the hub retirements.

## 11. Measurement

- Re-pull pages-by-internal-links after changes: cost page 11 ⇒ ~200; /data/ hub 4 ⇒ ~200; CVL unique contextual anchors 1 ⇒ 8+.
- GSC 8-week watch: "how much does liquidation cost" cluster (10.9–14.7 ⇒ top 8), CVL head term (39 ⇒ top 20), "insolvency statistics" URL swap-over, /liquidation/ hub CTR (0.06% baseline).
- Ahrefs: /data/ children entering top-100 pages by internal links; 404-reclaimed RDs reappearing on 200 targets.
