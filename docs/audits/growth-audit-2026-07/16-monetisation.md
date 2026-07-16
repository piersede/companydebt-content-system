# Monetisation & Revenue-per-Visitor Analysis — companydebt.com

Growth audit lens 7 (monetisation). Date: 2026-07-10. Author: monetisation subagent.
Sources: foundation brief (inventory / Ahrefs / GSC / business-model / competitor / repo digests), live spot-checks via WebFetch on 2026-07-10 (read-only, sanctioned): /insolvency-calculator/, /sample-letters/, /data/uk-insolvency-statistics/, /liquidation/members-voluntary-liquidation/, /winding-up-petitions/. Note: the upstream detail files (01–06) were not present on disk at run time (empty growth-audit directory except sitemaps/); this analysis grounds itself in the foundation-brief summaries plus fresh live fetches. Claims are marked verified vs inference throughout.

---

## 1. The existing model, restated precisely

**Verified on-page:** companydebt.com is first-party lead generation for licensed insolvency practitioner appointments. Two disclosed revenue streams:

1. **Direct appointments** via affiliated AABRS Limited IPs (four named, Chris Andersen IP 16070 fronting content), paid from company assets or director funding (commonly the statutory redundancy claim).
2. **Network referral fees** — "we may receive a fee where you engage another practitioner through our network."

Published pricing (verified live on the MVL page today): CVL £4,000–£6,000 +VAT (+£500–£1,000 disbursements); MVL £3,000–£5,000 +VAT, with a worked £17,750 tax-saving example. No ads, no affiliate links, no sponsorships anywhere (verified absence across 12 pages in the business-model pass).

**Conversion assets (all verified):**
- Freephone 0800 074 6757, one number sitewide, 4–8+ instances per page.
- 4-field unqualified contact form (name/email/phone/message) on nearly every page; "same day" response.
- 30-Second Insolvency Test (/insolvency-calculator/): debt sliders (Bank/HMRC/Creditors), asset value, personal-guarantee toggle, then mandatory name/company/email/phone + best-time-to-contact before results. Verified today: hidden fields carry the slider data through; **no newsletter opt-in, no marketing-consent checkbox, results delivered by phone call, not on screen**.
- /quick-quote/ page (linked from the MVL page's "Get a Quote" button — generic, not MVL-specific).
- LiveChat (working hours), info@companydebt.com, ungated Stressed Directors Guide PDF.

## 2. The revenue-per-visitor arithmetic that frames everything

- GSC: ~12,818 clicks in the last 12 months, of which only ~8,080 are UK — **~22 commercially relevant UK visitors per day**, falling (576 clicks in Jun 2026 vs 5,232 in Mar 2025).
- One CVL appointment ≈ £4,000–£6,000; one MVL ≈ £3,000–£5,000 (verified pricing). So **a single incremental appointment per month is worth roughly £48k–£72k/year** — several multiples of the entire Ahrefs "traffic value" ($2,349/mo) of the site's rankings.
- Inference (no analytics/lead-volume access): at typical distress-lead-gen enquiry rates of 2–5% on high-intent pages, current UK organic supports perhaps 15–35 enquiries/month across phone+form+test. Unverified; the point is the base is small enough that **conversion-rate and lead-value work beats traffic work pound-for-pound at current volumes**, and every leak matters.

This is the single most important monetisation fact: the site's economics are appointment-shaped, not RPM-shaped. Everything below is judged against "does it produce or protect appointments (or disclosed referral fees) without eroding the trust stack that makes a stressed director hand over a £5k engagement."

## 3. Lead qualification, routing and attribution (existing stream — biggest lever)

**Problems, all verified:**
1. The default form is 4 fields with zero qualification. The only qualified capture is the 30-Second Test. So most leads arrive unscored: no debt band, no HMRC-involvement flag, no personal-guarantee flag, no solvency signal. That forces triage onto the phone team and makes routing (direct IP vs network referral — the two revenue streams) slower and lossier.
2. The phone number — the dominant CTA at 4–8+ instances/page — is a single untracked freephone as rendered. The colleague's Gravity Forms lead-source attribution (cta_origin_url etc.) is on staging and covers **forms only**; call revenue is invisible to content decisions. (Repo memory: gform attribution deployed to staging 2026-07-10, not live.)
3. No callback scheduling. "Same day" response vs a director reading the winding-up-petition page at 11pm with a 7-day court clock is a mismatch; the test's "best time to contact" dropdown is the only concession.
4. Mobile is the clicking audience (55% of clicks, 0.41% CTR vs desktop 0.21%) and mobile Lighthouse is ~38. Every mobile performance point lost is lost on the highest-converting device. This is already an in-flight project; from the monetisation lens it is revenue work, not tech debt.

**Recommendations (existing stream, high confidence):**
- Add 2–3 optional qualifiers to the standard form (approximate debt band dropdown, "Is HMRC one of the creditors?", "Have you signed a personal guarantee?"). Optional keeps friction near-zero; even 50% fill-rate transforms triage and lets the same day promise become "priority callback" for high-band leads. This is a template change, not a rebuild.
- Get call attribution live: at minimum, distinct numbers for (a) money pages, (b) data/PR pages, (c) everything else; ideally dynamic number insertion keyed to landing page. Trade-off: fragments the memorable single freephone; mitigate by keeping 0800 074 6757 as the printed/branded number and swapping only on-page display numbers. Without this, all content ROI claims about the phone-first funnel are guesses.
- Offer a scheduled-callback slot picker on the money pages (evening/weekend slots explicit). Distress does not keep office hours; LiveChat is working-hours only (verified).
- Land the mobile performance remediation before any new funnel work — it multiplies everything else.

**Upside estimate:** if qualification+attribution+callback lift enquiry-to-appointment yield by even 10–20% on the existing base, that is plausibly 1–3 extra appointments/month = £50k–£200k/yr. Highest confidence, lowest regulatory risk of anything in this file.

## 4. Segments the current model wastes

### 4a. Solvent closures (MVL) — served but under-productised
Verified today: the MVL page's conversion paths are generic — a /quick-quote/ link, the **insolvency** test widget ("Is Your Company Insolvent?" — actively wrong for a solvent MVL prospect), and the standard form. No MVL-specific calculator despite the page itself doing the £17,750 worked example in prose. No contractor/IR35/retirement targeting language.
- **Fix:** an MVL tax-savings calculator (distributable reserves in → CGT-with-BADR vs dividend-tax comparison out, instant on-screen result, optional "email me this estimate" capture) plus an MVL-specific quote form (reserves band, number of shareholders, assets to distribute). This is the price-shopped, non-distressed segment: it comparison-shops (Clarke Bell ranks #4 for MVL at DR 22), tolerates email, and converts on transparent numbers — which CD already publishes. Serving the insolvency test to these visitors is a verified mis-fit.
- **Upside:** medium-high. MVL fee is £3k–£5k with far less casework variance; "members voluntary liquidation" (994/mo, KD 1) is winnable — CD is currently absent from the GB top-100.

### 4b. Micro companies too small for an IP
The striking-distance cluster GSC already shows — "cheapest way to close a limited company" (pos 14.2), "close a ltd company that never traded" (pos 9.8), "close a company with bounce back loan" (pos 9.6) — is exactly Begbies' best single asset ("how to close a company with no money", ~$8.3k/mo value). Many of these searchers have companies with no assets and no funds for a £4k CVL.
- Options, in ascending trust-risk order: (i) content that routes honestly to the director-redundancy-funded CVL (already the disclosed model — redundancy claim commonly funds the fee, which IS the answer for "no money" cases and is under-sold); (ii) a productised low-cost strike-off/dissolution support service where strike-off is genuinely appropriate; (iii) referral to a cheap dissolution provider for a fee.
- **Constraint:** the IP-voice rule (no DIY steer) is a house rule, not just taste. Option (i) is fully compatible and mostly a content/framing job: lead with "you may not need to fund this personally" on the no-money pages. Option (iii) risks the brand looking like a lead-flipper for £13 strike-offs; skip it. Option (ii) is credible only if AABRS actually wants that work.
- **Upside:** medium via (i) — it converts an existing striking-distance impression pool rather than opening a new stream.

### 4c. Creditors — verified unserved
The winding-up-petitions page is written exclusively for recipient directors (verified today: "no actionable guidance for creditors"; the only creditor mention is the £750 threshold). Creditors owed money by insolvent companies are the mirror-image audience on the same SERPs.
- A small creditor-services cluster ("how to issue a winding-up petition", "statutory demand", "recover a debt from a limited company") monetised by disclosed referral to debt-recovery solicitors/collection agencies (or to AABRS if it takes creditor instructions) is a genuine new stream.
- **Trade-off:** conflict-of-interest optics — the brand promises confidential rescue to directors; visibly arming their creditors on the same domain needs careful separation (own section, own disclosure, arguably its own nav silo). Also the /data/winding-up-petition-tracker/ is a natural creditor magnet, so the audience is arriving anyway once /data/ goes live.
- **Upside:** low-medium revenue (referral fees, thinner than IP fees) but real SERP-coverage value on the winding-up cluster where CD is pos 19 with a 3-page silo.

### 4d. Personal-debt spillover
Directors whose personal guarantees crystallise become personal-insolvency prospects (IVA/bankruptcy). CD already owns the relevant queries ("if my ltd company goes bust will i lose my house" 2,798 impr @ pos 6.0; "personal guarantee loopholes" 3,129 @ 9.2).
- A disclosed referral partnership with an FCA-regulated personal-debt/IVA firm converts traffic the current model answers but never monetises.
- **Constraints:** debt counselling/adjusting for individuals is FCA-regulated activity — the referral must go to an authorised firm and the arrangement disclosed exactly like the existing network-fee disclosure; and personal-debt lead-gen is a reputationally scummy sector, so partner choice is the whole game. MoneyHelper signposting alongside keeps the YMYL trust posture.
- **Upside:** low-medium; genuinely incremental, but the trust downside of a bad partner exceeds the fee income. Do it only with a named, vetted partner and the same "we are not independent" candour the site already models.

### 4e. Accountants and advisors — the cheapest missing channel
No partner/referrer page exists in the nav (verified absence in business-model pass). Accountant referral is the standard deal-flow channel for every competitor at Begbies' tier, and the /data/ hub is explicitly aimed at accountants already.
- A "For accountants & advisors" page (how referrals work, what happens to their client, response SLAs, optionally a disclosed commission or a strict no-commission trust stance — pick one and say it) plus the data-hub monthly briefing (below) as the retention mechanism.
- **Upside:** medium and compounding; near-zero build cost; zero regulatory issues; also the only channel that is insulated from Google/AI-Overview volatility, which the GSC collapse (-89% clicks) makes strategic, not nice-to-have.

## 5. Email, newsletter and first-party data capture

**Current state (verified): zero.** No newsletter, no opt-in checkbox on the test or forms, ungated PDF guide, ungated sample letters (confirmed today: letters are inline pages, no email wall).

The obvious move — gate everything — is wrong for this site:
- Distressed directors are a **days-to-weeks** audience; a monthly newsletter to them is worthless, and gating the letters/PDF would damage rankings, AEO citability, and the generosity signal that differentiates CD's disclosure-led brand.

What actually works, per audience:
1. **Distressed directors:** a short opt-in "what happens next" sequence (5–7 emails over 10 days: what an IP call involves, redundancy funding, what not to do before the hearing) offered at the moment of capture (test completion, form submission) and as an optional "email me this letter as a document" button on each sample-letter page — value exchange without gating the page itself. Purpose is enquiry recovery (people who tested but didn't answer the callback), not nurture. Needs explicit PECR/GDPR marketing consent — currently there is no consent language at all on the test (verified), which is a compliance gap worth fixing regardless.
2. **Accountants + journalists:** a **monthly UK insolvency statistics briefing email** built off the already-scripted monthly data-hub update. This is the one genuinely durable list this brand can own; it feeds the outreach conductor with warm recipients, compounds the PR asset, and creates the referrer-retention loop for 4e. Low effort: the data and the update cadence already exist in the repo workflow.
- **Upside:** direct revenue low-medium (enquiry recovery is real but small at ~22 UK visitors/day); strategic value high (first-party channel immune to SERP volatility). Cost: an ESP, consent plumbing, and two sequences.

## 6. Data licensing / API from the statistics asset

**Assessment: near-zero direct revenue; do not build a paid product.** The underlying data (Insolvency Service, Companies House, Gazette, ONS) is public and OGL-licensed — CD cannot sell what gov.uk gives away; the value CD adds is assembly, timeliness and interpretation. The payment-practices dataset (6,882 companies, avg 34.5 days to pay) is also statutory public data. A paid API would have a market of approximately nobody and a maintenance bill.

The data asset's real monetisation is **indirect and already the house strategy** (links, E-E-A-T, AI-citation surface; the outreach conductor is active; "insolvency statistics" already pos ~9.4 at 6.8% CTR — the only new winning query in recent GSC data). What's missing, verified on the live stats page today, is the packaging that converts a page into a citable source:
- methodology anchor exists but content is thin/"Planned"; **no press contact, no CSV/embed downloads, no citation instructions, no named analyst author, no email signup.**
- Ship: named author + finished methodology, a press-contact route, one-click chart embeds and CSV downloads carrying a "must credit Company Debt" line, and the monthly briefing signup (5.2). Offer journalists free bespoke cuts (e.g. petitions by region/sector from the tracker) — that is PR spend purchasing DR-70+ links of the kind the site verifiably lost in 2026 (equifax.co.uk DR80, business-money.com DR71, economicjournal.co.uk DR70).
- **Upside as "revenue": ~£0 direct. Upside as link equity:** the site's deep-link deficit (~90% of 879 referring domains hit the homepage; money pages have 0–21 RDs; /liquidation/ needs ~21→50 to move five pos-12–15 head terms) is the binding constraint on the whole organic P&L, and this asset is the only credible way to earn those links. Fund it as marketing, not as a product line.

## 7. Ads and affiliate — the evidence says no

**Verdict: net-negative, with numbers.**
- Scale: ~12.8k clicks/year total. At generous UK finance display RPMs (£20–£40), AdSense-style ads yield **£250–£500/year** — less than one-tenth of one CVL appointment — while introducing third-party ad JS to a site already failing mobile performance (Lighthouse ~38, TBT/third-party-JS-bound) on the device that produces 55% of clicks.
- Trust: the entire competitive moat at DR 42 is the disclosure/E-E-A-T stack (named IPs, "we are not independent" candour, published fees). Ads for debt consolidation or loans next to YMYL insolvency advice is precisely the pattern Google's QRG punishes and precisely what none of the ranked competitors do (verified: Begbies/RBR/theinsolvencyexperts run no display ads).
- Affiliate: marginally less bad, but the only high-relevance affiliate categories (personal-guarantee insurance — a striking-distance query cluster; business banking; credit insurance) either conflict with advice neutrality or belong as **disclosed referral partnerships** (same mechanism as the existing network-fee stream, same disclosure language) rather than tracked affiliate links. PGI specifically: a vetted partner + disclosed introducer fee on /advice/personal-guarantee-* pages is defensible and on-model; a generic affiliate link is not.

## 8. Entity clarity as a conversion issue

Company Debt Ltd vs AABRS Limited vs "our network" (part practice, part marketplace) is not just a schema/SEO nicety — it is a checkout-page problem. A director deciding whom to trust with a £5k engagement meets three identities. One paragraph on money pages ("Who will actually handle my case?") naming the AABRS relationship and when a case goes to network, mirrored in Organization schema, costs nothing and removes a late-funnel wobble. (Also relevant: the AABRS sister-site project must not create duplicate-content or self-competition on money SERPs — flagged, existing originality gate covers it.)

## 9. Priority stack (relative upside × effort × trust risk)

| # | Move | Stream | Upside | Effort | Trust/reg risk |
|---|------|--------|--------|--------|----------------|
| 1 | Qualify the form + call attribution + callback scheduling | Existing | High (£50k–£200k/yr plausible) | Low | None |
| 2 | MVL calculator + MVL-specific quote funnel | Existing (under-served) | Med-high | Medium | None |
| 3 | Accountant/advisor referrer page + monthly stats briefing email | New channel | Medium, compounding | Low | None |
| 4 | Data-hub packaging (methodology, press contact, embeds/CSV, named author) | Indirect (links) | High strategic, £0 direct | Low-med | None |
| 5 | Post-enquiry email sequence + consent plumbing | Existing (recovery) | Low-med | Low-med | GDPR care (also fixes current consent gap) |
| 6 | "No money to liquidate" framing: redundancy-funded CVL front and centre on the cheap-closure cluster | Existing | Medium | Low | None (on-model) |
| 7 | PGI / personal-debt disclosed referral partnerships | New | Low-med | Medium | Real — partner-dependent |
| 8 | Creditor-services cluster + referral | New | Low-med | Medium | Optics — needs separation |
| 9 | Paid data API / licensing | — | ~£0 | High | — skip |
| 10 | Display ads / generic affiliate | — | Negative | Low | High — do not |

**Unverified items to close before acting:** actual monthly lead volumes and phone/form split (needs GA/GF data, not available to this audit); whether AABRS wants creditor or micro-company work; partner appetite for PGI/personal-debt referrals; legal review of introducer-fee disclosures for regulated referrals.
