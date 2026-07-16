# SEO Strategy, Topic Selection and Topical Authority — companydebt.com
Growth audit lens 4a–c. Date: 2026-07-10. Author: senior growth strategist (subagent).

**Evidence note:** the foundation brief referenced full-detail files (01–06) in the scratchpad growth-audit directory; at the time of this analysis that directory contained only an empty `sitemaps/` folder, so this lens works from the brief digests plus fresh primary verification: live-page fetches of https://www.companydebt.com/liquidation/, /liquidation/creditors-voluntary-liquidation/, /liquidation/members-voluntary-liquidation/ (2026-07-10), an Ahrefs GB SERP pull for "creditors voluntary liquidation" (2026-07-01 index), and two Ahrefs organic-keyword pulls against companydebt.com (GB, 2026-07-01). Everything sourced from the brief is marked (brief); everything I verified directly is marked (verified).

---

## 1. Is the site targeting commercially valuable topics, or over-invested in unmonetisable traffic?

**Verdict: the portfolio is inverted.** 60% of the sitemap is informational vs 24% money (brief: 190 vs 76 of 317 URLs), which would be fine if the informational layer fed the money layer. It largely does not:

- The site's top organic pages by clicks are liability long-tail and newsjack: /insolvency/shareholders-liable-company-debts/ is the #1 page at just 904 clicks/year, and 6 of the top 30 GSC pages are celebrity/news articles (cruise industry, Orla Kiely, Bobby Davro, Jamie Oliver) with no conversion path (brief, GSC).
- The definitional informational corpus is being eaten by AI Overviews, not by ranking loss: misfeasance 40,053 impressions at position 8.5 with 0.01% CTR; Insolvency Act 1986 27,209 impr at 10.0 with 0.06%; "administration" 13,027 at 8.3 with 0.02% (brief, GSC). These pages now generate impressions Google answers itself. Writing more of this class of content is producing training data for competitors' AI citations, not traffic.
- Meanwhile the content that survived the Sep–Oct 2025 collapse is precisely the high-intent distress cluster: can't pay PAYE #2, can't pay VAT #2, can't pay corporation tax #5, liquidation cost #4, all KD 0–4 (brief, Ahrefs). Traffic value fell only -31% while volume fell -63% (brief) — the market is telling the site exactly what it is valued for: urgent, monetisable, HMRC-pressure and closure-cost queries.

**Strategic conclusion:** stop allocating editorial capacity to definitional explainers and newsjacking. Every new informational page should pass one test: "does a stressed director with a real deadline (Gazette notice, HMRC letter, petition) search this?" If not, the page belongs in the data hub (citation asset) or nowhere.

The dated news posts still live (/articles/paradise-papers 2017, Carillion 2018 — with a typo slug "effect") are pure dead weight for topical focus; the celebrity insolvency posts earn clicks but zero journey value. Keep the few that earn links, prune or noindex the rest, and redirect that production capacity to the two clusters below.

## 2. Missing high-intent topics with a realistic right to win

Right-to-win logic: at DR 42 with 863 referring domains, CD out-guns most page-level requirements on these SERPs — competitor pages rank with 0–16 referring domains (verified on the CVL SERP: Begbies #3 with 3 RDs, RBR #4 with 16, Antony Batty DR 25 #9 with 2 RDs). Coverage and page format are the binding constraints, not authority (brief, competitors — corroborated by my SERP pull).

**Gap A — cost-anxiety closure cluster (highest value, verified absent).** Ahrefs GB shows companydebt.com ranks for ZERO keywords containing "cheapest", "no money" or "afford" (verified, phrase-match pull, 2026-07-01), and https://www.companydebt.com/liquidation/cant-afford-liquidation/ 404s (verified). Begbies Traynor's single best content asset is "how to close a company with no money": ~1,343 visits/mo, ~$8,306/mo value, 157 keywords including "cheapest way to liquidate a company" #2 (brief, competitors). GSC shows CD already surfaces at position ~14.2 for "cheapest way to close a limited company" with no dedicated page (brief, GSC) — i.e. Google already wants to rank CD here. This is also the cluster where CD has a genuine differentiator competitors soft-pedal: the director-redundancy-funding route to a funded CVL is already disclosed on money pages as the firm's funding model (brief, business).

**Gap B — strike-off / Gazette-notice urgency cluster (verified zero coverage).** Ahrefs GB shows no companydebt.com ranking for any keyword containing "gazette" or "strike off" (verified pull), despite /liquidation/company-strike-off-and-dissolution/* pages existing in the sitemap (brief, inventory). "First gazette notice for compulsory strike-off" alone is 2,400/mo (brief, competitors) and is a panic query — a director discovers their company is being struck off, often with a bounce-back loan or HMRC debt attached, which converts directly to CVL/advice. RBR farms this cluster (brief).

**Gap C — winding-up petition cluster (thin but already striking distance).** The /winding-up-petitions/ cluster is 3 pages (brief, inventory), yet the single hub page holds "winding up petition" (2,200/mo, KD 3) at position 13 and "what is a winding up petition" (1,000/mo, KD 4) at 22, and is also the ranking URL for "winding up order" (900/mo, KD 5) at position 44 (verified pull). The petition SERP has DR 3–22 incumbents (brief, competitors). One page is carrying three distinct intents; splitting the post-order intent out and strengthening the hub is the cheapest head-term win on the site, and it pairs with the already-built /data/winding-up-petition-tracker/ for freshness and internal links.

**Gap D — HMRC Time to Pay (open SERP, currently squandered).** "hmrc time to pay" (600/mo, KD 14) has no national insolvency firm in the top 10 (brief, competitors); CD's /hmrc/time-to-pay-hmrc/ sits at 39–45 for the head terms while ranking 7–10 for the long-tail "time to pay arrangement(s)" variants (verified pull). This is not a new-page gap but an optimisation gap: the page already exists, already ranks top-10 on variants, and needs internal-link concentration from the cant-pay-VAT/PAYE/CT trio (all #2–#5) plus a title/H1 aligned to the head term. Respect the IP-voice rule (no DIY steer) — the page can lead with representation value while still being the best TTP resource.

**Gap E — MVL/CVL service SERPs (format problem, not coverage problem).** See section 3.

## 3. Intent match of money pages vs their target SERPs

This is the site's most fixable strategic error. Verified live on 2026-07-10:

- **/liquidation/creditors-voluntary-liquidation/**: H1 "Creditors' Voluntary Liquidation (CVL): Practical Guide for UK Directors", ~5,500–6,000 words, 11 H2s, fees stated (verified). It ranks position 39 for "creditors voluntary liquidation" (1,500/mo) (brief, Ahrefs). The pages that actually rank (verified SERP pull): Begbies #3 and ukliquidators #10 with plain service-entity titles ("Creditors' Voluntary Liquidation (CVL)"), RBR #4 with a definitional title — all substantially shorter, service-shaped pages, ranking with 2–16 referring domains. gov.uk is #2. The SERP rewards a tight service/entity page, and CD is serving a 6,000-word practitioner guide titled as a "Practical Guide". Note also CD's own /liquidation/how-much-does-liquidation-cost/ holds a PAA/question slot on this SERP (verified) — proof Google trusts the domain on this entity.
- **/liquidation/members-voluntary-liquidation/**: H1 "Members' Voluntary Liquidation (MVL) Explained", meta title "Members Voluntary Liquidation (MVL) | Company Debt", ~4,500–5,000 words (verified). MVL is absent from the GB top 100 (brief, Ahrefs) while Clarke Bell ranks #4 at DR 22 with 10 refdomains (brief, competitors). MVL searchers are price-shopping solvent directors — a quote-led service page intent — and CD's page is framed as an explainer ("Explained") despite containing the strongest commercial assets on the SERP (published £3,000–£5,000 fee band and the £17,750 tax-saving worked example).
- **/liquidation/**: H1 "Company Liquidation: Process, Costs and Director Advice", ~5,500-word guide, holds 5 head terms at 12–15 with only 21 referring domains (brief, Ahrefs; page verified). "Company liquidation" (KD 42, gov.uk ×2 + Wikipedia) is the one genuinely outgunned SERP (brief, competitors); the hub's realistic job is to feed and rank the sub-terms, which it structurally does.

**Diagnosis:** the Bernstein pipeline produces excellent long-form practitioner guides, and that format wins on informational and long-tail SERPs (it is exactly why the cant-pay-HMRC cluster holds #2). But on the service-entity SERPs (CVL, MVL), Google's chosen format is a shorter, conversion-shaped service page. CD is bringing a textbook to a shop-window contest. The fix is not to gut the guides but to re-shape the top of these two pages to service intent: entity-first titles/H1s (drop "Practical Guide"/"Explained"), fees + timeline + eligibility + engage-CTA in the first viewport, guide depth retained below, plus a handful of targeted internal links with exact-entity anchors from the strongest pages (the hub, cost page, cant-pay trio). Given page-level link requirements of 3–16 RDs, even 5–10 relevant internal/external links to each should be decisive. If after re-shaping the CVL page still stalls, the fallback is a Begbies-style split (service page + guide) — but try re-shaping first; a split carries cannibalisation risk the current single-URL approach avoids.

## 4. Topical authority: depth, breadth, and dilution

**Where authority is real:** the HMRC-arrears entity (34 URLs, #2 rankings that survived the collapse) and increasingly the insolvency-statistics entity ("insolvency statistics" position ~9.4, 6.8% CTR — the only new query among recent top earners) (brief). The liquidation cluster is deep (70 URLs) and the internal hub structure is genuinely good (verified: /liquidation/ links CVL/MVL/compulsory/strike-off/administration).

**Where authority is diluted:**
- Four competing sector layers (25 legacy /sectors/ posts + 8 root-level sector pages + /sector-insolvency-hub/ + /sector-specific-insolvency/) with 8 direct topical duplicates, e.g. /sectors/carehomes/ vs /care-home-insolvency/ (brief, inventory). This is straightforward cannibalisation and crawl-signal splitting on a topic family the site is actively rewriting (the 25-page sector rewrite programme is already underway per repo memory). Consolidation should precede or accompany the rewrites — rewriting a page whose duplicate still competes with it wastes the rewrite.
- Near-duplicate money-adjacent pairs: /hmrc/security-bonds/ vs /hmrc/security-bond-notices/; /liquidation/director-conduct-review/ vs /liquidation/directors-conduct-report-2/ (a live "-2" collision slug) (brief, inventory).
- Hub proliferation (10+ hubs, including /liquidation/liquidation-hub/ nested inside /liquidation/) fragments the very entities the site needs Google to consolidate (brief, inventory).
- ~90% of link equity points at the homepage; the deep links that exist point at legacy linkbait and dead http:// CVL paths (10+9 RDs) rather than money pages (brief, Ahrefs). Reclaiming the dead-path equity via Quick Redirects to the current CVL URL is a free transfer of exactly the equity the CVL SERP needs.

**Update cadence:** money pages are freshly reviewed (CVL "Reviewed on 09/07/2026", verified) and the data hub has a scripted monthly workflow (brief, repo) — cadence on the core is good. The stale edge (2017–2018 news, testimonial sitemap lastmod 2022) sends the opposite signal and should be pruned.

## 5. The data-hub / original-research moat

This is the right strategic bet and it is already showing signal ("insolvency statistics" pos 9.4, 6.8% CTR within a quarter of launch). Three sharpenings:

1. **It is the AI-citation counter-move.** AI Overviews on CD's own money SERPs cite Crunch, RBR and theinsolvencyexperts — never companydebt.com (brief, competitors). Unique, monthly-updated, citable numbers (petition tracker, payment practices' 6,882-company dataset) are the most credible route to becoming the cited source rather than the absorbed one. The active citation-gap outreach conductor should point at these pages hard.
2. **Ship what is built before building more.** /data/ hub + petition tracker + dissolutions pages are finished on staging awaiting visual QA (brief, repo); every week not live is a week of lost freshness signal on a topic where CD already ranks. The 6 registered-but-unbuilt statistics pages (CVL/compulsory/administration statistics, insolvencies-by-sector, construction-insolvency, payment-practices) are correctly scoped in docs/data-hub/page-specs.md (verified read) with low-KD targets ("prompt payment code" 500/mo KD 1).
3. **Close the credibility gaps the business audit found:** methodology marked "Planned", no named author, no press contact on a hub explicitly built for journalists (brief, business). For a citation asset these are not polish, they are the product.

## 6. Proposed new pages (distinct intent, journey role, low cannibalisation)

Deliberately short list — the site's bigger problems are format and consolidation, not missing URLs.

| # | Proposed page | Target query (GB vol) | Role in journey | Cannibalisation control |
|---|---|---|---|---|
| 1 | /liquidation/close-a-company-with-no-money/ | "close a company with no money" + "cheapest way to close a limited company" (Begbies' version: 157 kws, ~$8.3k/mo value) | MONEY-adjacent: affordability objection → redundancy-funded CVL (the firm's own funding model) | Distinct from /liquidation/how-much-does-liquidation-cost/ (price fact) — this answers "I can't fund it"; cross-link both ways, keep cost figures canonical on the cost page. GSC already shows CD at ~14.2 for "cheapest…" with no dedicated page, so Google is asking for it. |
| 2 | /liquidation/first-gazette-notice-compulsory-strike-off/ (under the existing strike-off section) | "first gazette notice for compulsory strike-off" (2,400/mo) + suspension/objection variants | URGENT INFO → strike-off objection / funded CVL / BBL pages | Verified zero current CD rankings for any gazette/strike-off term, so nothing to cannibalise; links up to the strike-off guide, which targets the process entity not the notice event. |
| 3 | /winding-up-petitions/winding-up-order/ | "winding up order" (900/mo, KD 5; hub currently ranks 44 for it) | URGENT INFO → compulsory-liquidation advice; consequences intent post-order | Splits a distinct post-order intent OFF the hub, letting the hub focus on "winding up petition" (2,200/mo, pos 13). Add tracker cross-links. |
| 4 | /data/business-payment-practices/ (already fully specced) | "payment practices reporting" (700, KD 3), "prompt payment code" (500, KD 1) | DATA/citation asset + internal-link glue to cash-flow and cant-pay-suppliers pages | Spec already isolates it from insolvency data (enrichment-only hard rule); unique dataset = no SERP overlap with own pages. |
| 5 | The 3 route-statistics pages already registered (CVL/compulsory/administration statistics) | "cvl statistics", "compulsory liquidation statistics" etc. (low vol, near-zero KD) | DATA: freshness + entity reinforcement for the matching money pages; AI-citation surface | Statistics intent is cleanly separate from the service/guide pages; each links to its money twin. |

**Explicitly not proposed as new pages:** an MVL-costs page (fix the MVL page's intent instead — a costs page would cannibalise its strongest section); TTP variants (concentrate on the existing /hmrc/time-to-pay-hmrc/); more definitional explainers (AI-Overview-absorbed class); HMRC helpline-number utility pages (RBR's playbook, but it collides with the IP-voice rule and earns unmonetisable zero-click traffic).

## 7. Priority order (this lens only)

1. Re-shape CVL and MVL pages to service intent (titles, H1s, first viewport, internal anchors) — highest value per hour on the site.
2. Ship /data/ live + methodology/author/press-contact; keep the outreach conductor pointed at it.
3. Build page #1 (close-with-no-money) — the single largest proven content gap.
4. Winding-up-petition cluster build-out (#3 + hub strengthening + tracker links).
5. Strike-off/Gazette page (#2) and redirect the dead http:// CVL backlink paths.
6. Sector-layer consolidation folded into the existing 25-page rewrite programme; kill the duplicate pairs and hub-in-hub.
7. Payment-practices + route-statistics data pages on the monthly data cadence.
8. Prune/noindex the newsjack tail; hard stop on new definitional content.
