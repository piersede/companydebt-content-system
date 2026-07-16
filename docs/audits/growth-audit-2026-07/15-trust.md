# Trust, Credibility, E-E-A-T and Persuasion Audit — companydebt.com

Audit date: 2026-07-10. Lens: brief section 6. Method: live read-only WebFetch of 8 URLs (homepage, /about-us/, CVL money page, /hmrc/cant-pay-vat/, /data/uk-insolvency-statistics/, Carillion article, /case-studies/chinese-takeaway/, plus 404 probes for /author/chris-andersen/ and /editorial-standards/), cross-referenced against the foundation brief (inventory, Ahrefs, GSC, business model, competitors, repo context). Verified facts are labelled; the rest is marked inference.

---

## 1. The headline finding

The site's trust architecture is **excellent at the page level and hollow at the entity level**. Money pages carry a disclosure most competitors would never publish, statutory-grade citations, fresh review dates and published pricing. But the person all of that hangs off — Chris Andersen — has **no author page on the site** (`/author/chris-andersen/` returns 404, verified 2026-07-10), the About page names no individuals, there is no published editorial-standards page (`/editorial-standards/` 404), the data hub built "for journalists" has no named analyst and a methodology still marked "Planned", and the review proof is 9 reviews on reviews.io against a homepage claim of "Trusted by Thousands of UK Directors".

The repo context confirms a genuinely rigorous internal system: editorial-os v2.3, a 14-check pre-publish gate, 10 YMYL prose gates, a mandatory named-IP human sign-off, and a hard rule against faked authorship. **None of that rigour is visible to a user, a journalist, or a Google quality rater.** The site is doing Which?-grade governance and presenting it like a generic lead-gen site. Closing that visibility gap is the cheapest trust work available because the substance already exists — it only needs publishing.

This matters commercially right now for two reasons grounded in the other workstreams:

- **GSC/Ahrefs**: the traffic collapse (clicks -89% Mar 2025→Jun 2026; DR 52→42 step-change Oct 2025 without refdomain loss) is consistent with a quality/trust reappraisal plus AI-Overview absorption. AI Overviews on the HMRC-debt SERPs cite Crunch, RBR and theinsolvencyexperts — never companydebt. Answer engines cite *entities* they can resolve and verify. An unresolvable author byline and an About page with no people weakens exactly the machine-readable entity graph that AEO selection runs on.
- **Business model**: revenue is high-trust phone/form conversion from stressed directors. Trust elements on the decision path (reviews, named people, disclosure clarity) are direct conversion levers, not SEO garnish.

---

## 2. What is genuinely strong (verified live)

These should be protected and extended, not reworked:

1. **Commercial-interest disclosure on money pages.** Verbatim from /liquidation/creditors-voluntary-liquidation/ and /hmrc/cant-pay-vat/: *"Company Debt is a commercial insolvency practice. We are not independent of the process described on this page. If you instruct us, we act as your insolvency practitioner and are paid from company assets or director funding."* Plus the disclosed network referral fee. Almost no competitor says this. It is a real differentiator with both stressed directors (reduces the "who's actually paying you?" suspicion) and quality raters.
2. **Published pricing with worked examples.** CVL £4,000–£6,000 +VAT with disbursement breakdown; MVL £3,000–£5,000 +VAT with a £17,750 tax-saving example. Sector-unusual transparency.
3. **Statutory-grade sources blocks.** CVL page cites Insolvency Act 1986 ss. 84, 123, 210, 214, 216, 235, 238, 239; Insolvency Rules 2016; CDDA 1986; ERA 1996; gov.uk pay caps and the IP register. Cant-pay-vat cites nine legislation.gov.uk/gov.uk references and carries current penalty rates (3%/6%/10%) attributed to HMRC guidance dated July 2026.
4. **Fresh, honest review dates on core pages.** "Reviewed on 09/07/2026" (CVL), 08/07/2026 (cant-pay-vat) — days before this audit; content includes the 6 April 2026 £751 statutory pay cap, i.e. the dates reflect real maintenance.
5. **Regulated-person anchoring in the footer.** Four named IPs with licence numbers (Andersen 16070, Newton 9732, Bradstock 5956, Meadows 9184), AABRS affiliation, IPA/ICAS/ICAEW routes, company number 06352368 and the Bank Street address, sitewide.
6. **User-first steering where it counts.** The TTP/VAT pages lead with HMRC's own Business Payment Support Service line (0300 200 3835) inside the content before pitching representation — a genuine best-interest signal (while the firm's 0800 number still owns the conversion furniture, which is fine).
7. **Accreditation and press logos** (IPA, ICAS, TMA; BBC, Guardian, FT, Telegraph, Fortune, Investopedia) — present but currently unlinked/unevidenced (see §3.8).

---

## 3. Trust gaps, in order of severity

### 3.1 The author entity does not resolve (highest severity)
- `https://www.companydebt.com/author/chris-andersen/` → **404 (verified)**. Every content page bylines Chris Andersen, yet the name has nowhere to go. No on-site bio, no photo in a profile context, no link to the IPA register entry for IP 16070, no LinkedIn/sameAs trail the site controls.
- Google's QRG and every answer engine's citation heuristics look for a discoverable, corroborable author. The current state is "a name and a claim of 20+ years' experience with no landing point" — the exact pattern content farms fake, presented by a firm that isn't faking it.
- Same problem for the other three IPs: named only in footer text, no profiles anywhere.

### 3.2 Author reviews his own work, on everything
- On the CVL page the byline and the "Reviewed by" credit are both Chris Andersen (verified). One person appears to author *and* review ~300 live URLs spanning statutory guides, news posts, case studies and statistics. Externally this reads as a rubber stamp, not a review chain — and it is factually misleading about the real process, which (per repo governance) includes a mechanical 25-point gate and a separate human sign-off.
- It also concentrates the entire site's E-E-A-T on one individual: a single-point-of-failure entity.

### 3.3 The internal editorial rigour is invisible
- `/editorial-standards/` → **404 (verified)**. The About page (verified) contains no editorial policy, no review-process description, no corrections policy, no complaints route, no conflicts-of-interest statement.
- Internally there is a documented ~30-file governance system, YMYL prose gates, an evidence hierarchy, a caveat library, and a hard "never fake authorship" gate. Publishing a 600-word honest description of this process is close to free and is the kind of thing Which?, MSE and NerdWallet all surface prominently.

### 3.4 The data hub fails its own audience test
- /data/uk-insolvency-statistics/ (verified): no named author or analyst, no press/media contact, no citation guidance, no visible downloads; methodology absent (repo confirms it is marked "Planned"). Update cadence is good (published 19 June 2026, next release 17 July 2026) and sources (Insolvency Service, Companies House) are named.
- The business-model workstream found the hub is explicitly "built for journalists, accountants, lenders and company directors", and an active citation-gap outreach programme is emailing journalists about it. **Journalists check for a named analyst and a methodology before citing.** Every outreach email sent before this is fixed converts below potential. This is the single highest-leverage trust fix for the link-earning strategy — and it should ship with the pending /data/ live push, not after.

### 3.5 Review proof is thin and self-contradicting
- Homepage (verified): "Excellent", "5 average", reviews.io widget, testimonials dated "2 years ago", and the unsourced claim **"Trusted by Thousands of UK Directors"**. CVL page (verified): "Read our 9 reviews".
- Nine reviews cannot carry a "thousands" claim; the contradiction is visible on a single browsing session from homepage to money page and actively undermines both signals. Testimonial sitemap last modified June 2022 (inventory workstream) confirms the programme is dormant.
- Competitor context: Begbies/RBR run hundreds of reviews on Trustpilot/Reviews.co.uk. For a distress-purchase, recent third-party reviews are among the few signals a panicking director actually checks.

### 3.6 First-hand experience (the first E) is the weakest letter
- Exactly one case study exists (/case-studies/chinese-takeaway/, verified): fully anonymised, no figures, no timeline, no client quote, no outcome numbers; it reads as a composite teaching example (it does disclose that details are altered — honest, but it deprives the page of evidentiary force).
- The voice rules (company-authored "we", lived-caseload texture) do inject experience signals into prose, but there is no *evidence layer*: no aggregate case numbers ("X CVLs completed in 2025"), no named-IP case commentary, no before/after specifics.

### 3.7 Blanket "Reviewed on" stamps on stale content poison the good dates
- The Carillion piece (2018 news, verified live) shows "Reviewed on 23/05/2026" with no archival notice and reads as current advice. Paradise Papers (2017) and other dated news are in the same state (inventory).
- A rater or reader who sees a 2018 news story "reviewed" in 2026 learns to distrust *every* review stamp on the site — including the genuinely fresh ones on money pages. Freshness signalling is only worth something if it is falsifiable and honest.

### 3.8 Unsupported claims and unlinked badges
- "Trusted by Thousands of UK Directors" — no source (verified homepage).
- Press logos (BBC, Guardian, FT…) with no links to the actual coverage. Unlinked press logos are indistinguishable from fabricated ones; the coverage exists, so link it or list it on a press page.
- Accreditation logos not linked to the registrable entries (IPA member search, ICAS directory).
- "20+ Years Experience" for Andersen — plausible, but nothing on site corroborates it (no career history anywhere).

### 3.9 Entity fuzziness: Company Debt vs AABRS vs "our network"
- The disclosure honestly says appointments run through affiliated AABRS IPs and that referral fees may arise from "our network", but nowhere is the relationship explained in plain English: who signs the engagement letter, who holds the licence, when a case goes to the network and why. For users this is a residual "so who am I actually hiring?" doubt at the decision point; for search engines it splits the entity graph across two brands (aabrs.com is a separate DR-33 site under the same owner).

### 3.10 Homepage carries the least disclosure of any key page
- Verified: no update dates, no monetisation disclosure, no named people on the homepage itself (IPs are footer-only). The page users trust-check first has the thinnest trust layer.

---

## 4. Would greater commercial transparency help or hurt?

**Help — the evidence points one way.** The site's two most differentiated trust assets are already transparency plays (the non-independence disclosure and published pricing), and the pages carrying them are the site's best performers (cant-pay-vat/paye at #2; liquidation-cost holding a PAA slot on the CVL SERP per the competitor workstream). Distress-purchase buyers are suspicious by default; competitors mostly hide fees and independence status; every increment of verifiable transparency is differentiation the Begbies brands cannot cheaply copy at their scale. The one boundary: transparency about *process and money* helps; manufactured intimacy (fake founder stories, inflated case counts) would hurt. Extend the disclosure pattern upward to a site-level "How we make money" page and outward to the AABRS relationship. There is no plausible mechanism by which this reduces conversions among directors who were going to call; it removes a hesitation reason for those on the fence.

---

## 5. Recommendations (ranked)

1. **Build the author entity layer** (high impact / low effort). Create /team/chris-andersen/ (and pages for Newton, Bradstock, Meadows): photo, career history substantiating "20+ years", IP licence number linked to the IPA register entry, LinkedIn sameAs, Person schema, list of authored/reviewed pages. Point every byline at it. Fix the /author/ 404 (redirect to the profile). This is the prerequisite for AI-Overview citation and the cheapest QRG win available.
2. **Ship the data-hub trust layer with the /data/ live push** (high impact / medium effort). Named analyst + reviewing IP, completed methodology page (the internal architecture doc already contains the substance: source hierarchy, release ledgers, caveat library), press contact (a real person + email), "cite this page" guidance, CSV downloads. Do this *before* more outreach emails go out.
3. **Publish the editorial standards** (high impact / low effort). One page: how content is produced, the review gate, IP sign-off, evidence rules, corrections policy, and a "How we make money" section that elevates the existing money-page disclosure to site level. Link it from the About page, footer, and byline block. The content already exists in editorial-os/ — this is a condensation job, not a creation job.
4. **Split author from reviewer** (medium-high impact / low effort). Use the four named IPs as topic-area reviewers (e.g. Andersen authors, Newton reviews liquidation; Meadows reviews HMRC pages) so the "Reviewed by" credit reflects the real two-person process. Kills the self-review optic and de-concentrates the entity risk. Requires governance change in the byline template, not rewriting content.
5. **Restart the review engine and retire the "thousands" claim** (high impact / medium effort, ops-dependent). Systematic post-case review request (reviews.io or Trustpilot), target 50+ reviews in 12 months; until the count supports it, replace "Trusted by Thousands of UK Directors" with something verifiable (e.g. years operating, cases completed if internally sourced). Fix the homepage-vs-money-page contradiction now by showing count + recency, not just stars.
6. **Date-honesty pass on legacy content** (medium impact / low effort). Archival banner on dated news (Carillion, Paradise Papers, Orla Kiely etc.) or prune them; stop applying "Reviewed on" stamps to pages that received no substantive review. Protects the credibility of the review dates on the pages that earn money.
7. **Build 5–8 evidence-bearing case studies** (medium impact / medium effort). Anonymised but concrete: debt figures, timeline, fees charged, outcome, handling IP named, standard verification note ("details altered; case file held"). One per money cluster (CVL, MVL, TTP, WUP, strike-off) and interlink from the money pages at the decision point. This is the only scalable fix for the Experience signal and doubles as conversion proof.
8. **Publish the entity map** (medium impact / low effort). A plain-English page: Company Debt Ltd ↔ AABRS Limited ↔ "our network" — who holds the licence, who takes the appointment, when and why a referral happens and what the fee is. Link it from every disclosure block. Also link the press logos to the actual coverage and the accreditation logos to the register entries.

**Sequencing note:** items 1, 3, 4 and 8 are essentially one sprint of publishing work using material that already exists internally; item 2 must land before further data-hub outreach; item 5 is the only one needing new operational muscle.
