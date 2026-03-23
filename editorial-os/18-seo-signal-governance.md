# 18. SEO Signal Governance

Derived from confirmed Google ranking signals exposed in the ContentWarehouse API (March 2024 leak). These rules reinforce existing editorial standards with specific, signal-aware requirements. Every rule here maps to a named signal in Google's internal scoring system.

---

## Signal 1: Site-level quality (NSR / chard / tofu)

Google assigns site-level quality scores that affect every page on the domain. These are not page-level — they are levied against the whole site. A single low-quality page drags the signal for all pages.

**Rules:**
- Every published page must meet the pre-publish gate. No exceptions for short-form, topical, or time-sensitive posts.
- Do not publish thin, filler, or promotional-only content. The chard and tofu classifiers identify pages that provide no informational value to the reader.
- Quantity does not offset quality. Five strong pages outperform twenty weak ones for site-level scoring.

---

## Signal 2: Product and service review quality

Google has dedicated promotion and demotion classifiers for review pages (`productReviewPUhqPage`, `productReviewPPromotePage`, `productReviewPDemotePage`). These operate at both page and site level. For BusinessExpert, this applies to any content comparing BusinessExpert against alternatives or reviewing practice management software.

**Rules:**
- **Comparison frameworks must be genuine.** Any comparison must include at least one dimension where BusinessExpert is not the strongest fit. See `11-comparison-governance.md`.
- **Evidence density matters.** Specific figures — response rate uplifts, time saved per week, client adoption rates, pricing — are extractable signals. Vague comparative claims are not.
- **Verification dates required.** Every capability claim about a competitor product must include a verification date or a `[VERIFY]` flag.

---

## Signal 3: YMYL classification

BusinessExpert's content touches accountancy practice operations, compliance workflows, and financial decision-making. This places it within YMYL-adjacent territory (`ymylNewsV2Score`). Content advising practices on workflow tools that handle client data, HMRC compliance, or financial document management carries higher evidential standards than general SaaS content.

**Rules:**
- Every claim about compliance, regulatory requirements, data handling, or client financial outcomes requires a named source or a `[HUMAN CONFIRMATION NEEDED]` flag.
- No casual assertions about what "most practices" do without a named basis.
- In YMYL-adjacent categories, unsupported claims carry heavier penalties than in non-YMYL content.

---

## Signal 4: Salient term coverage

Google identifies salient terms per document and scores topical coverage depth. Each term has a salience score, IDF, and virtual term frequency. For BusinessExpert's content, covering the full vocabulary of the topic — naturally, not by stuffing — is a quality signal.

**Core salient terms by topic area:**

- **Document collection and chasing:** document request, client portal, automated chasing, follow-up schedule, overdue documents, receipt collection, secure upload, multi-channel chasing (email, SMS, WhatsApp)
- **Practice management:** practice management software, Xero integration, client onboarding, workflow automation, team assignment, staff permissions, audit trail
- **AI receptionist:** AI receptionist, call handling, enquiry capture, call triage, meeting booking, call transcript, escalation, out-of-hours
- **Accountancy practice context:** accountancy practice, bookkeeper, sole practitioner, small firm, medium firm, client communication, admin bottleneck

**Rules:**
- Articles on document chasing must include the core terms naturally. A post on "reducing document delays" that never mentions client portals, automated chasing, or Xero integration is topically shallow.
- Do not force terms into places they do not fit. Topical coverage is scored on natural occurrence, not density.
- Avoid synonym drift. Use the established terms consistently within an article.

---

## Signal 5: Article structure signals

Google classifies pages as articles using structural signals (`articleScore`). Clear structure increases classification confidence and passage-level scoring accuracy.

**Rules:**
- Use H2 and H3 headings that reflect the real content of each section. Headings that describe what the section says rather than label a template slot.
- Include a visible byline with the author name.
- Include a publication date and last-reviewed date on decision-stage pages.
- Methodology or research basis notes must be present on comparison and review pages.

### Signal 5a: H2 semantic relevance guidance

H2s should be semantically connected to the page topic, but must read naturally as chapter titles. The page context already establishes the topic — don't force the full keyword phrase into every H2.

**Principle: keywords but natural.** Write H2s for readers first, then optimise gently. A sharp, contextual heading like "The Rate Problem" on a Capital on Tap review page is better than "The Capital on Tap Business Credit Card Rate Problem".

**Guidelines:**
- H2s should work as a table of contents. Each one should clearly describe what that section covers.
- Include a topic keyword where it reads naturally, not where it feels forced. One or two anchored H2s per page is enough for search engines to understand the structure.
- Avoid bare generic labels that could appear on any page: "Overview", "Summary", "Details". But contextual headings like "The Key Differences" or "How to Improve Your Chances" are fine when the page title provides the context.
- FAQ headings should include a short topic label: "Sole Trader FAQs", not bare "Frequently Asked Questions". Keep it short — don't repeat the full page title.
- **Heading hierarchy:** No level skips (h2→h4). Labels inside components (e.g. "Our take", "Watch out") must use styled divs, not heading tags.

**Exemptions:** "Related Pages" and "Methodology and Disclosure" are structural headings exempt from topic-anchoring.

**Enforcement:** The build script runs `validate_h2_relevance()` as an advisory check (WARN only). Heading hierarchy violations (level skips) remain FAIL-level.

---

## Signal 6: Freshness signals (Last Significant Update)

Google tracks the Last Significant Update (LSU) of each page using passage timestamps, content age analysis, and crawler changerate. The update must be substantively meaningful — cosmetic edits do not reset LSU.

**Rules:**
- When updating an article, make substantive changes. Adding new pricing data, a new section, correcting outdated competitor claims, or adding a new use case counts. Rewording an introduction does not.
- Date-stamp significant updates visibly: "Last reviewed: [Month Year]" near the top.
- Do not fake freshness with cosmetic-only edits. Google detects change significance (`averageChangeSignificance`, `lastChangeSignificance`).

---

## Signal 7: Page clutter penalty

Google penalises pages with distracting or annoying elements (`clutterScore`). This is a design and CMS concern, but editorial choices can introduce clutter.

**Rules:**
- Do not embed promotional banners mid-article that break reading flow.
- Do not stack multiple BusinessExpert CTAs inside a single article — one natural CTA per article is the limit.
- Avoid decorative visual inserts that add no information value.

---

## Signal 8: Click satisfaction signals (NavBoost)

Google tracks user click behaviour: good clicks, bad clicks, last-longest clicks (the click that was both the last and longest in a search session). These cannot be manipulated directly, but editorial choices either support or undermine them.

**Rules:**
- **Title promise must match content.** A title like "How to stop chasing clients for documents" must deliver a practical answer, not redirect the reader to BusinessExpert without substance.
- **No bait-and-switch.** If the title frames a problem, the article must solve it — not pivot immediately to BusinessExpert as the answer.
- **Answer the question early.** Readers who find their answer in paragraph 2 are more likely to be last-longest clicks. Delayed answers produce bad clicks.
- **Every article must have a clear ending.** A reader who reaches the end and finds a useful conclusion is more likely to be satisfied.

---

## Signal 9: Passage-level scoring

Google scores individual passages independently (`passageScore`, `subqueryRelevance`). A page with a strong introduction but weak body sections is penalised at passage level even if the overall page appears comprehensive.

**Rules:**
- Every major section must stand on its own. A section that only makes sense in context of the previous section is a passage-level weakness.
- **Minimum information density per passage.** Vague generalities, filler sentences, and incomplete explanations score poorly even if the surrounding content is strong.
- **Avoid thin transitions.** Transition paragraphs that repeat what was just said and preview what comes next without adding information are a passage-level liability.

---

## Signal 10: Anchor text quality (anchorMismatch)

Google uses anchor text of inbound and internal links as a content quality signal. `anchorMismatch` is an explicit attribute — mismatched or generic anchor text is a negative signal.

**Rules:**
- **No generic anchor text.** Banned phrases as link anchors: "click here", "read more", "find out more", "this article", "here", "learn more", "this guide", "more information".
- **Descriptive, destination-accurate anchors.** Use the target topic as the anchor: "how BusinessExpert's document chasing works", "Xero integration setup guide", "automated client portal walkthrough".
- **Internal link anchors must match the target page's primary topic.**
- **Varied anchors for repeated links.** If the same page is linked multiple times, vary the anchor text rather than repeating the same phrase.

---

## Signal 11: Commercial and promotional link density (SpamBrain)

SpamBrain and thin-content classifiers are sensitive to the ratio of promotional links to editorial content. A page where the majority of links are CTAs or BusinessExpert product links is a negative quality signal.

**Rules:**
- The balance of links must favour editorial and informational destinations.
- No paragraph where the only link is to BusinessExpert's pricing page, demo request, or signup without accompanying substantive editorial content.
- Every BusinessExpert link should sit within genuine editorial context, not act as a standalone CTA in otherwise thin content.

---

## Signal 12: Title and meta description match (titleMatchScore)

Google explicitly scores the alignment between title, meta description, and content delivered. This is a named signal.

**Rules:**
- The title must reflect the actual content of the article, not a keyword target that the article only partially addresses.
- Meta descriptions must describe what the article actually delivers, not generic "learn more" language.
- The H1 and title tag should align. Avoid situations where the title tag promises something the H1 frames differently.
- If the title targets a buyer question ("how to automate document chasing"), the article must answer it directly, not pivot to an BusinessExpert promotion.

---

## Signal 13: Content originality (cross-article differentiation)

Google's duplicate content detection operates at sub-document level. On a site with multiple posts covering similar practice management topics, repeated passages score poorly independently of the page's other quality signals.

**Rules:**
- Each article must have a distinct angle. Two articles on "document chasing" cannot cover the same points in the same order.
- Do not re-use boilerplate product descriptions across articles. Every BusinessExpert product description in a new article must be written for that article's specific framing.
- Where topics overlap, differentiate by buyer segment, workflow stage, or decision lens — not just by adding a different introduction.

---

## Signal 14: Author entity recognition (authorEntityId)

Google attempts to identify the real author behind content and scores it against known author entities. Author pages, consistent bylines, and author profiles improve entity recognition and EAT signalling.

**Rules:**
- Every article must have a named author byline. Anonymous content does not feed author entity recognition.
- Authors should have a consistent, linked author profile on the site.
- Author profiles should include relevant credentials: role, area of expertise, relevant background.
- Do not imply author credentials that are not real. See `09-voice-governance.md` for authorship rules.

---

## Signal 15: Image relevance scoring

Google scores images for topical relevance to surrounding content. An image with no relationship to the surrounding passage is neutral-to-negative, not positive.

**Rules:**
- Every image must be directly relevant to the section it appears in. A generic office stock photo in a document-chasing article does not serve image relevance scoring.
- Alt text must describe the specific content of the image, not a keyword.
- Screenshots of BusinessExpert's interface should be placed in the section that discusses the feature shown — not grouped at the end or used decoratively.
- No decorative imagery that has no relationship to the surrounding content.

---

## Signal 16: Content comprehensiveness (thin-content classifier)

Google operates a thin-content classifier distinct from and independent of the low-quality classifiers. A page can pass general quality checks while still triggering thin-content classification.

**Rules:**
- Every article must contain at least three specific, verifiable claims that the reader could not find in a product homepage alone.
- Vague language ("one of the most popular tools", "widely trusted by practices") with no figure or source is a thin-content signal. Name the basis or remove the claim.
- FAQ answers must be self-contained and substantive. One-sentence answers that refer the reader elsewhere ("see above") are thin at passage level.

---

## Signal 17: Inauthentic content signals

Google's quality systems flag content that does not originate from genuine expertise or direct engagement with the subject. These signals apply to human-written filler as much as to AI-generated text.

**Rules:**
- **No generic filler sentences.** Sentences that could have been written without product familiarity are authenticity signals: "BusinessExpert is a powerful tool that helps practices work more efficiently."
- **Verdicts must have immediate evidence.** "BusinessExpert reduces document-chasing time" must be followed immediately by its evidence basis (named source, customer data, or a clearly labelled editorial judgement).
- **Uneven specificity is itself a signal.** A mix of highly specific sections and vague filler passages flags the vague passages, even if the rest of the article is strong.
- **AI prose fingerprints are an authenticity signal.** See `14-failure-modes-and-recovery.md` §16 for the 13 patterns to check.

---

## Signal 18: Internal linking and article-level PageRank

Google scores internal linking as part of page-level authority distribution. An article with no internal links from other pages on the site is treated as isolated and lower-authority.

**Rules:**
- Every new article must be linked from at least one existing article on the site shortly after publication.
- Related articles section must be present on decision-stage pages (comparison, review, buyer guide) with 3–5 internal links using descriptive anchor text.
- Prioritise internal links from high-traffic, high-authority pages rather than only from recent posts.
- Internal link anchors must follow the same descriptor-accurate, non-generic rules as external anchors (see Signal 10 above).

---

## Pre-publish SEO signal checklist

Run this after the main pre-publish gate. All items must pass.

| # | Check | Pass condition |
|---|-------|----------------|
| S1 | Title–content match | Title promise fully delivered in article body |
| S2 | No generic anchor text | Zero instances of "click here", "here", "read more", "learn more", "this guide" as link anchors |
| S3 | Authenticity phrases | Zero banned authenticity phrases (see `14-failure-modes-and-recovery.md` for the banned list) |
| S4 | Verdict evidence | Every verdict sentence followed by its evidence basis within 3 lines |
| S5 | FAQ depth | No one-sentence FAQ answers; no "see above" cross-references |
| S6 | Salient term coverage | Core topic vocabulary present naturally (not forced) |
| S7 | Author byline | Named author present on every published article |
| S8 | Internal links out | Article links to at least 2 other BusinessExpert site pages with descriptive anchors |
| S9 | Internal links in | Article linked from at least one existing page (or scheduled for linking post-publication) |
| S10 | Image alt text | Every image has specific, descriptive alt text — not generic or keyword-stuffed |
| S11 | Freshness date | Last-reviewed date visible on decision-stage pages |
| S12 | CTA density | No more than one BusinessExpert CTA per article; CTAs sit within editorial context |

---

## Full on-site SEO audit checklist

Run this on every article before publication. The quick checklist (S1–S12) above covers the highest-priority items. This extended audit covers all on-site, content-controllable ranking factors. Nothing speculative has been removed — if it is plausibly a factor, it is checked.

### Title and meta

| # | Factor | Pass condition |
|---|--------|----------------|
| F1 | Title tag keyword usage | Title clearly reflects the main topic and includes the primary keyword naturally |
| F2 | Title tag keyword position | Primary keyword appears early in the title |
| F3 | Meta description keyword usage | Meta description summarises the page and includes the primary keyword |
| F4 | Keyword in H1 | H1 clearly reflects the topic and aligns with the primary keyword |
| F5 | Semantic terms in title and description | Title and description include supporting terms that clarify intent |

### Keyword and topical coverage

| # | Factor | Pass condition |
|---|--------|----------------|
| F6 | Keyword prominence | Primary keyword appears early in the first section of content |
| F7 | Keyword usage in H2 and H3 | Subheadings reinforce the topic with relevant keyword variations where natural |
| F8 | Term frequency relevance (TF-IDF style) | Important terms appear frequently enough to establish topical relevance |
| F9 | Semantic keyword coverage (LSI-style) | Page includes related terms and concepts that broaden topical understanding |
| F10 | Entity match | Content clearly aligns with the real-world topic or product being searched |

### Content depth and quality

| # | Factor | Pass condition |
|---|--------|----------------|
| F11 | Content length | Page is long enough to compete with other pages targeting the same query |
| F12 | Topic depth | Page covers the topic comprehensively rather than superficially |
| F13 | Content breadth | Multiple angles of the topic are covered, not just a single perspective |
| F14 | Content completeness | All major user questions related to the query are answered |
| F15 | Content usefulness | Content solves a real user problem |
| F16 | Unique insights | Page provides original analysis or perspective |
| F17 | Supplementary content usefulness | Supporting elements (tables, summaries, FAQs) add real value |

### Freshness and originality

| # | Factor | Pass condition |
|---|--------|----------------|
| F18 | Content recency | Page signals freshness where relevant (review dates, updated pricing) |
| F19 | Magnitude of content updates | Updates materially improve the page, not just minor edits |
| F20 | Historical update frequency | Content is periodically reviewed and improved |
| F21 | No duplicate content | All content is unique within the site |
| F22 | Original content | Page is not syndicated or copied from other sources |
| F23 | Canonical tag correctness | Canonical signals are correct where duplication risk exists |

### Formatting and readability

| # | Factor | Pass condition |
|---|--------|----------------|
| F24 | Reading level | Writing is easy to understand for the intended audience |
| F25 | Grammar and spelling | Content is clean and professionally written |
| F26 | Bullets and numbered lists | Lists used where appropriate to improve clarity and scanability |
| F27 | Formatting for scanability | Short paragraphs, clear sections, visual breaks |
| F28 | User-friendly layout | Main content immediately visible and easy to follow |
| F29 | Table of contents usefulness | Page structure allows clear navigation and section understanding |
| F30 | Content visibility | Key content is directly visible, not hidden behind tabs or interactions |
| F31 | Mobile content visibility | Important content is not hidden or reduced on mobile |

### Media

| # | Factor | Pass condition |
|---|--------|----------------|
| F32 | Image optimisation | Images use descriptive filenames, alt text, and contextual placement |
| F33 | Multimedia usage | Page includes relevant visual elements to support understanding |

### Internal linking

| # | Factor | Pass condition |
|---|--------|----------------|
| F34 | Internal linking quantity | Page links to other relevant pages on the site |
| F35 | Internal linking quality | Links are contextually relevant and placed within content |
| F36 | Internal link anchor text | Anchor text reflects the linked page topic |
| F37 | Internal link authority flow | Important pages receive links from relevant sections |
| F38 | Broken links | No internal links are broken |

### URL and structure

| # | Factor | Pass condition |
|---|--------|----------------|
| F39 | URL length | URL is concise and readable |
| F40 | Keyword in URL | URL reflects the topic |
| F40a | No year in URL | URL must not contain a year (e.g. /best-cards-2026/). Years in URLs force redirects on annual updates. Put the year in the title and H1, not the slug. |
| F41 | URL structure clarity | URL path clearly indicates the page's place in the site |
| F42 | URL depth | Page is not buried unnecessarily deep |
| F43 | Page category relevance | Page sits in a relevant topical category |
| F44 | Breadcrumb clarity | Breadcrumbs accurately reflect site structure |
| F45 | Site architecture alignment | Page fits logically within the site's content hierarchy |

### Technical quality

| # | Factor | Pass condition |
|---|--------|----------------|
| F46 | HTML quality | Clean semantic structure for search engines |
| F47 | Duplicate meta information | Titles and descriptions are unique across pages |
| F48 | Schema / structured data | Appropriate schema applied to help interpretation |
| F49 | Mobile usability | Layout and interaction smooth on mobile |
| F50 | Mobile friendliness | Page designed for mobile-first rendering |
| F51 | Core Web Vitals alignment | Fast load, stable layout, responsive interaction |
| F52 | Page speed perception | Page loads quickly from a user perspective |
| F53 | Site usability | Page is easy to navigate and interact with |

### Engagement and snippet optimisation

| # | Factor | Pass condition |
|---|--------|----------------|
| F54 | Dwell-time support | Structure encourages continued reading |
| F55 | CTR optimisation | Title and description encourage clicks |
| F56 | Featured snippet formatting | Content includes concise, structured answers for extraction |
| F57 | Definition clarity | Key questions answered directly and clearly |
| F58 | List-style answer blocks | Some answers formatted as lists for snippet potential |
| F59 | FAQ clarity | FAQs directly answer real user questions |

### Trust and E-E-A-T

| # | Factor | Pass condition |
|---|--------|----------------|
| F60 | References and sources | Claims are supported or clearly grounded |
| F61 | Trust signals | Authorship and credibility clearly presented |
| F62 | E-E-A-T alignment | Experience, expertise, authority, and trust demonstrated |
| F63 | Contact / editorial transparency | Page signals who is behind the content |
| F64 | Content authenticity | Content reads as human, not templated or generic |

### Anti-patterns

| # | Factor | Pass condition |
|---|--------|----------------|
| F65 | No over-optimisation | No keyword stuffing or forced SEO patterns |
| F66 | No gibberish or autogenerated content | All content is coherent and purposeful |
| F67 | No excessive ads or distractions | Main content not pushed down or obscured |
| F68 | No intrusive elements | Nothing interrupts reading flow |
| F69 | Page layout clarity | Structure highlights the main content clearly |

### Usage note

Not every factor applies to every article. Technical factors (F46–F53) are CMS/theme concerns and only need re-checking when the template changes. Content factors (F1–F17, F24–F31, F54–F66) must be checked on every article. Internal linking (F34–F38) and URL/structure (F39–F45) are checked on new articles and after URL changes.

When auditing: run content factors first, then linking, then trust/E-E-A-T. Flag any factor that does not pass. Fix content-level failures before publication. Flag technical failures for theme-level resolution.

---

## Relationship to other governance files

- Signal 17 (authenticity) overlaps with `14-failure-modes-and-recovery.md` §16. The failure modes file governs prose quality; this file governs the SEO consequence of the same failures.
- Signal 3 (YMYL) overlaps with `10-evidence-governance.md`. Evidence governance governs claim treatment; this file governs the SEO consequence.
- Signal 11 (link density) overlaps with `11-comparison-governance.md` §BusinessExpert mentions. Comparison governance governs fairness; this file governs the SEO consequence.

When a rule appears in both files, the stricter interpretation applies.
