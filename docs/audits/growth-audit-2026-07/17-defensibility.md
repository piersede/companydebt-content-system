# Long-Term Defensibility Audit — companydebt.com

Lens: Google volatility, AI search, brand (objective 8). Date: 2026-07-10.
Analyst basis: foundation briefs (inventory, Ahrefs, GSC, business model, competitors, repo), fresh Ahrefs AI-citation and Brand Radar pulls made for this report, repo inspection (AEO pipeline, outreach conductor), and live fetches of the stats hub and llms.txt. Verified facts are labelled; inference is flagged.

---

## 1. How exposed is the current traffic base?

### 1.1 The portfolio is structurally long AI-absorbable information

- 60% of the 317 sitemap URLs are informational; ~97 of the top-100 GB keywords are informational intent (Ahrefs). Verified.
- GSC shows the signature of zero-click absorption already complete on the definitional layer: misfeasance 40,053 impressions at position 8.5 with 0.01% CTR; insolvency act 1986 27,209 impr at 10.0 with 0.06%; "administration" 13,027 impr at 8.3 with 0.02%. These pages rank fine and earn nothing. Verified (GSC brief).
- Site-wide: clicks -89% (5,232/mo Mar 2025 -> 576/mo Jun 2026) while average position improved 22.8 -> ~18. Impressions -66%. That combination is not a ranking collapse; it is the SERP paying out less per ranking. The Sep-Oct 2025 cliff coincides with the DR step-down and (inference) a core update plus AI Overview expansion in the UK.
- What survived is instructive: the HMRC-arrears distress cluster (cant-pay-PAYE #2, cant-pay-VAT #2, cant-pay-CT #5, liquidation-cost #4) and the urgent personal-consequence queries (will I lose my house 0.39% CTR at pos 6, personal guarantee loopholes 0.45% at 9.2). Distress + personal stakes + need-a-human = the defensible end of informational search. Verified.

**Conclusion (judgement):** roughly the bottom two-thirds of the informational portfolio ("what is X", definitional, celebrity/news) is already economically dead or dying and will not come back. Defensibility spend should not try to resurrect it. The defensible organic core is ~15-20 pages: HMRC arrears, cost/fees, personal-liability outcomes, urgency (winding-up petition, strike-off notices), plus the data hub.

### 1.2 Concentration risk

Top 3 pages = 39% of Ahrefs-visible traffic; UK-relevant clicks are ~22/day (GSC). One algorithmic knock on the /hmrc/ cluster would remove most remaining commercial traffic. There is no meaningful non-Google demand channel today: brand search ~137 clicks/year, no email list (the Stressed Directors Guide is ungated), no referrer programme. Verified facts; risk framing is judgement.

---

## 2. AI-search position: measured, not guessed

Fresh Ahrefs AI-citation counts pulled 2026-07-10 (site-explorer-ai-responses-count, mode=subdomains). Citations = links in AI answers; AIO keywords = keywords where the domain is cited in a Google AI Overview.

| Domain | ChatGPT | Google AI Overviews (citations) | AIO keywords | AI Mode | Gemini | Perplexity | Copilot | Grok |
|---|---|---|---|---|---|---|---|---|
| **companydebt.com** | **17 (11 pages)** | **0** | **30 (20 pages)** | **0** | 6 | 6 | 15 | 18 |
| realbusinessrescue.co.uk | 16 (6 pages) | 27 | **746 (140 pages)** | 28 | 11 | 7 | 13 | 40 |
| begbies-traynorgroup.com | 22 (11 pages) | 18 | **692 (102 pages)** | 12 | 13 | 12 | 15 | 42 |
| theinsolvencyexperts.co.uk | 1 | 2 | 108 (32 pages) | 1 | 0 | 2 | 0 | 3 |

Three verified findings from this table:

1. **The AI-search gap is a Google gap, not an LLM gap.** On ChatGPT, companydebt is at parity with Begbies (17 vs 22 citations) and ahead of RBR on page diversity (11 pages vs 6). On Google AI Overviews — the channel actually suppressing its clicks — it is cited on 30 keywords vs RBR's 746 and Begbies' 692: a 23-25x deficit. Even DR-25 theinsolvencyexperts has 3.6x more AIO keyword citations.
2. Google AI Overview / AI Mode citation counts for CD are literally zero in the direct-citation columns. Combined with the competitors brief (AI Overviews on cant-pay-corporation-tax cite Crunch, RBR, theinsolvencyexperts — never companydebt), the site is being written out of the answer layer on SERPs where it ranks top-5 organically.
3. RBR's 140 AIO-cited pages vs CD's 20 is a concrete gap list, the AI-era equivalent of the 1,503 exclusive-keyword gap.

### 2.1 Brand Radar: monitoring exists but is empty (verified)

- An Ahrefs Brand Radar report exists (report_id 019eb316-81ca-7d5c-b00e-014547d21771, created 2026-06-10, ChatGPT daily; Copilot/Gemini/Perplexity/Claude/Grok/AIO all off).
- Tracked brands are configured (Company Debt, AABRS, Begbies Traynor Group, Company Rescue, Real Business Rescue, Wilson Field) but **the prompt list is empty** (`management-brand-radar-prompts` returns `[]`), so every mention metric returns zero and `ai_responses` is an empty set. The report has collected nothing in the month since creation.
- Operationally: the org decided to monitor AI visibility, paid for the seat, and never loaded the questions. This is a one-afternoon fix.

### 2.2 What the existing AEO work covers vs misses (repo-verified)

`scripts/answer_engine_audit/AUTOMATION_SPEC.md` confirms a genuinely mature pipeline: sitemap-driven (~588 live pages auditable), capture (OpenAI + Gemini), extract fact-deltas, verify against primary sources with cache, recommend render-aware edits; human applies. Facts already applied to the 5 liquidation-route guides (June 2026). llms.txt is live (verified fetch) — a full site directory, though with no emphasis on the data hub and no crawler guidance.

**Covers well:**
- Content completeness vs what AI engines say (nugget deltas), with verification discipline most competitors will never match.
- OpenAI + Gemini answer surfaces.
- Page-level structured data (JSON-LD read from rendered HTML in the already-covered guard).

**Misses — and the misses map exactly onto the measured gap:**
1. **No Google AI Overview / AI Mode capture.** The pipeline audits OpenAI and Gemini — the two surfaces where CD is already at or near parity — and does not observe the surface with the 25x deficit and the direct click suppression. This is the single biggest blind spot in the whole defensibility programme.
2. **No citation/mention outcome tracking.** The audit improves inputs (page content) but nothing measures whether CD gets cited afterwards. Brand Radar was the intended instrument and is empty (2.1).
3. **Excluded page types** (`/sectors/`, `/articles/`, landing pages are filtered out in sitemap.py). The excluded set includes the site's best PR/citation assets (pub-closures) and the 25-page sector layer being rewritten.
4. **Machine-readability of the data assets** — see section 3. Content audits cannot fix a missing CSV.
5. **Entity/brand-level signals** (section 4) are outside its scope entirely.

---

## 3. The data hub as a citation asset: right strategy, half-built artefact

The strategy is correct and already producing the only genuinely new positive signal on the site: "insolvency statistics" at position ~9.4 with 6.8% CTR (GSC, last quarter) — a CTR ~30x the site average, on a query class (fresh numbers) that AI engines must cite rather than absorb, because stale answers are visibly wrong.

The outreach conductor (outreach/README.md, verified) is well-designed: citation-gap framing ("you cite X's figure, ours is fresher for that exact point"), fail-closed guardrails, auto-draft human-send, daily cap of 5, Monday board. Phase 1 is STATS_HUB_ONLY; Ahrefs sourcing is still manual CSV; no reply tracking.

But a live fetch of https://www.companydebt.com/data/uk-insolvency-statistics/ (2026-07-10) shows the asset itself is not yet citation-grade for machines or journalists:

| Citation affordance | Status (verified live) |
|---|---|
| Methodology section | Absent (only "seasonally adjusted where available") |
| Named author / expert reviewer | None — no byline at all, on a site whose entire E-E-A-T stack is named IPs |
| Press/media contact | None — only the sales helpline |
| Downloadable data (CSV/API) | None — charts and HTML tables only |
| Last-updated + next-release date | Present and good ("Latest data: May 2026, Published 19 June 2026, Next release: 17 July 2026") |
| Cite-this-page block | Absent (the pub-closures article has one; the flagship hub does not) |
| Dataset JSON-LD (schema.org/Dataset) | Not observed (inference from fetch; verify in source) |
| Uniqueness | Repackaged official data + rolling-rate calc — modest value-add |

The genuinely unique data is still unshipped: the payment-practices page (6,882-company statutory dataset, avg 34.5 days to pay, manufacturing 47.4 days — fully specced in docs/data-hub/page-specs.md) is the only dataset in the pipeline no competitor can trivially copy, and the winding-up-petition tracker (weekly Gazette cadence) is the only asset with a recurring news hook faster than the monthly Insolvency Service release everyone shares.

**Judgement:** every month the hub runs without methodology, a named analyst, a press route and a CSV, the outreach conductor is pitching journalists a page that fails their own citation checklist. The fix costs days, not weeks.

---

## 4. Brand: the moat that does not exist yet

Fresh GB keyword volumes (Ahrefs keywords-explorer, 2026-07-10):

| Brand query | GB volume/mo | Notes |
|---|---|---|
| begbies traynor | 3,932 | sitelinks, PLC, ~29x CD's brand demand |
| insolvency practitioner near me | 273 | local pack — CD has no local play |
| **company debt** | **260** | SERP has paid_top, **ai_overview**, paid_bottom — Google treats it as a GENERIC query, not a brand |
| aabrs | 189 | sitelinks + paid_top: the sister brand has cleaner navigational demand than Company Debt itself |
| company rescue | 183 | knowledge_panel |
| uk liquidators | 177 | knowledge_panel |
| real business rescue | 150 | sitelinks |
| company debt ltd | 10 | the only unambiguous CD brand query |
| companydebt | 0 | |

Verified structural problems:

1. **The brand name is a generic phrase and Google now answers it.** "company debt" carries an AI Overview and four ad slots; GSC shows the homepage at position ~30 on "debt company"/"company debt advice" with 0 clicks. CD cannot win a navigational SERP that Google doesn't consider navigational. Competitors' brand SERPs (Begbies, Company Rescue, UK Liquidators) show sitelinks/knowledge panels; "company debt" shows neither.
2. **Brand demand ~137 clicks/year and falling** ("company debt" position 6.6 -> 10.9 over the last 3 months, GSC). Begbies' brand demand alone exceeds CD's entire monthly organic traffic.
3. **Entity fuzziness compounds it**: Company Debt Ltd vs AABRS Limited vs "our network" (business brief). For knowledge-graph and LLM entity recognition, two half-entities are worse than one whole one. AABRS out-polls Company Debt on navigational search — the group's brand equity sits on the other domain. (Inference on LLM effects; volumes verified.)
4. In LLM answers, brand mentions (unlinked) matter as much as citations, and there is currently zero measurement of either (Brand Radar empty).

**Judgement:** CD will not out-brand Begbies. The realistic brand play is *named-expert + named-dataset* branding: "Company Debt insolvency statistics", Chris Andersen and the other three licensed IPs quoted in national/trade press via the data assets, Wikidata/schema entity cleanup, and winning the tiny navigational SERPs it can own ("company debt ltd", "companydebt reviews"). Brand is built here as a by-product of data PR, not ad spend.

---

## 5. What actually makes this site defensible when "what is a CVL" evaporates

Ranked by durability (judgement, grounded in the above):

1. **Regulated human service + published prices.** Four licensed IPs, transparent CVL/MVL fees, disclosure honesty. AI answers end at "speak to a licensed insolvency practitioner" — CD is one. No AI Overview liquidates a company. This is the terminal conversion moat; everything else funnels to it.
2. **Fresh, hooked, owned data.** Monthly stats cadence + weekly petition tracker + unique payment-practices dataset. AI engines and journalists must cite current numbers from somewhere; freshness is the one content attribute LLM training data cannot absorb.
3. **The distress-query cluster.** Urgent, personal, YMYL-heavy queries where clickthrough survives (0.2-0.7% CTR vs 0.01% definitional) because the searcher needs confidential human help, not information.
4. **Operational verification infrastructure.** The AEO pipeline's verify-against-primary-source discipline is a real asymmetry: CD can keep hundreds of pages factually current at low marginal cost while competitors' pages drift stale — exactly what answer engines select for.
5. **Direct-demand channels that don't exist yet** (email nurture, accountant-referrer programme, brand search). Currently zero; every point built here is a point Google cannot take away.

What is NOT defensible: the 190-page informational long tail, the celebrity/news articles, the four redundant sector layers, definitional pages. Maintain the money-adjacent ones, stop investing in the rest.

---

## 6. Recommendations in priority order

### P1. Point the AEO programme at Google AI Overviews (the measured 25x gap)
The pipeline audits the two surfaces where CD is already competitive and ignores the one where it is absent. Actions: (a) pull RBR's 140 and Begbies' 102 AIO-cited pages from Ahrefs as the target list and map to CD equivalents; (b) add an AIO/AI-Mode capture leg to `answer_engine_audit` (Ahrefs API or SERP capture) so the recommend stage optimises for what Google's answer layer actually quotes; (c) prioritise the pages that rank top-5 organically but get zero AIO citations (cant-pay-CT, liquidation-cost, cant-pay-VAT/PAYE) — Google already trusts them organically, so citation absence is a format/extractability problem, the cheapest kind to fix. Impact: high — this is the channel suppressing the surviving money cluster. Effort: medium.

### P2. Finish the stats hub as a citation-grade asset before scaling outreach (days of work)
Add to /data/uk-insolvency-statistics/ and siblings: full methodology section, named analyst/IP reviewer byline, press contact (press@ + a person), CSV download per chart, cite-this-page block (exists on pub-closures already — port it), schema.org/Dataset JSON-LD, and llms.txt emphasis on /data/. Every outreach email currently points journalists at a page missing their checklist items. Impact: high (multiplies the already-running outreach). Effort: low.

### P3. Load the empty Brand Radar report this week
Zero prompts configured since 2026-06-10; it measures nothing. Load 50-100 prompts across the money intents (can't pay VAT/PAYE/CT, liquidate my company, liquidation cost, wind up petition received, close company with BBL, MVL tax) plus brand prompts; switch on AIO, Perplexity, Gemini sources alongside ChatGPT. This is the KPI instrument for P1/P2 and costs an afternoon. Impact: medium (measurement, not traffic — but nothing above can be steered without it). Effort: low.

### P4. Ship the two unique-data assets and hang the PR programme on their cadence
Payment-practices page (6,882-company dataset — the only truly proprietary asset in the pipeline) and the winding-up-petition tracker to live. Then: monthly stats-release comment note quoting a named IP (rebuilds the lost equifax/business-money-tier links), weekly petition-tracker snippets for trade press. Widen the conductor to Phase 2 assets and automate Ahrefs sourcing. Impact: high (links + brand + AI citations compound). Effort: medium (pages are specced/built; the programme is the work).

### P5. Entity and micro-brand cleanup
One clear entity story: Company Debt (trading brand) -> AABRS Limited (regulated firm), consistent Organization JSON-LD with sameAs, Wikidata entry, reviews consolidation (9 reviews on money pages vs 5-star homepage widget), and ownership of the navigational SERPs it can win ("company debt ltd", "companydebt"). Goal: knowledge panel + unambiguous LLM entity recognition, so mentions accrue to one brand instead of leaking between two. Impact: medium, slow-burn. Effort: low-medium.

### P6. Build the non-Google demand channels from existing traffic
Gate or follow up the Stressed Directors Guide (it is currently ungated with zero capture), add a monthly stats-digest email for accountants/advisors, and stand up an accountant-referrer page (unserved segment per business brief; referrals are the industry's actual lead engine). At ~22 UK clicks/day, organic is near its floor — each captured relationship is defensible in a way rankings are not. Impact: medium-high over 12 months. Effort: medium.

### P7. Stop-loss on the absorbable tail
Consolidate the four sector layers, prune/noindex dead definitional and celebrity pages or fold them into decision assets. Not a growth play — a maintenance-cost and crawl-focus play that concentrates freshness effort on the ~80 pages that can still pay. Impact: low-medium. Effort: medium.

---

## Appendix: data provenance

- AI citation counts: Ahrefs `site-explorer-ai-responses-count`, 2026-07-10, mode=subdomains, targets companydebt.com / realbusinessrescue.co.uk / begbies-traynorgroup.com / theinsolvencyexperts.co.uk.
- Brand Radar: `management-brand-radar-reports` + `management-brand-radar-prompts` (report 019eb316-81ca-7d5c-b00e-014547d21771; prompts = []); mentions-overview all zeros.
- Brand volumes: Ahrefs `keywords-explorer-overview`, GB, 2026-07-10. CPC values are USD cents.
- Live fetches: https://www.companydebt.com/llms.txt and https://www.companydebt.com/data/uk-insolvency-statistics/ (read-only, sanctioned).
- Repo: scripts/answer_engine_audit/AUTOMATION_SPEC.md; outreach/README.md + directory listing.
- All other figures: foundation briefs (inventory / Ahrefs / GSC / business model / competitors / repo) supplied by the audit orchestrator. Note: the other agents' full detail files were not present on disk in this session's scratchpad; where cited, figures come from the brief summaries.
