# 22. Google Search Quality Evaluator Guidelines

Standalone audit system based on Google's Search Quality Evaluator Guidelines (September 2025 edition, 182 pages). This is a diagnostic tool, not part of the core editorial workflow. It runs only when manually invoked.

The file has two parts:
- **Part A (sections 22.1-22.10):** The 12-agent audit framework — how to run an audit
- **Part B (sections 22.11-22.30):** The QRG reference material — what the agents assess against

---

# Part A: Audit Framework

## 22.1 Purpose

Evaluate any page on the BusinessExpert website against the quality framework defined in the Google Search Quality Evaluator Guidelines. The audit produces a structured quality report with a final quality rating, specific failures, and actionable remediation steps.

This system exists because Google trains human raters using these guidelines to assess search result quality. Pages that would receive low ratings from a trained rater are pages that Google's algorithms are designed to demote. The audit catches problems that editorial governance alone cannot detect: page-level trust signals, site-wide reputation patterns, ad/content balance, deceptive design, and YMYL compliance gaps.

## 22.2 Separation from the core editorial system

This audit system is structurally independent from the default content workflow defined in the master methodology (sections 1.1-1.11) and governance files (09-18).

- The default workflow (reader-intent brief → draft → trust pass → pre-publish gate) runs on every article. This audit runs only when manually invoked.
- The pre-publish gate checks editorial quality before publication. This audit checks published page quality after the page exists in its final rendered form.
- The editorial governance files (09-18) are shared: the `editorial-voice` agent references them. But this audit does not modify them and does not add new rules to them.
- No existing workflow step triggers, requires, or is blocked by this audit. No audit triggers, requires, or blocks an existing workflow step.
- This system does not change how articles are written, reviewed, or published. It is a diagnostic tool, not a gatekeeping tool.

## 22.3 When to use it

- Before publishing a new YMYL page (financial advice, product recommendations with monetary stakes)
- After a major site redesign or template change
- When investigating unexplained ranking drops on specific pages
- During periodic quality reviews of the credit card section or other commercial content
- When adding a new content type or page template to the site

## 22.4 When not to use it

- During normal article drafting or editing (the default workflow handles editorial quality)
- For copy edits, typo fixes, or minor content updates
- As a replacement for the pre-publish gate or human-authorship self-audit
- On third-party pages or competitor sites (the agents assume access to the BusinessExpert codebase and CMS)

## 22.5 Execution modes

**Full audit**: All 12 agents run in sequence. Produces a complete quality report. Use for new YMYL pages or periodic reviews.

**Targeted audit**: Specify which agents to run. Use when investigating a specific quality dimension (e.g., run only `trust-eeat` and `reputation` when diagnosing an authority problem).

**Batch audit**: Run a full or targeted audit across multiple pages. Produces a summary matrix showing quality distribution across the section.

Invocation: `Run website quality audit on [URL or page slug]` or `Run [agent-name] audit on [URL or page slug]`.

## 22.6 The 12 audit agents

Twelve named agents, each responsible for one quality dimension. Agents run in dependency order: the orchestrator sequences them so that downstream agents can reference upstream findings.

**Agent 1 — orchestrator**
Receives the audit request. Loads the target page content, metadata, and surrounding site context. Sequences the remaining agents. Collects all findings into the final report.

**Agent 2 — page-classifier**
Determines the page purpose (informational, transactional, navigational, mixed) and whether the page qualifies as YMYL. Classification uses the QRG taxonomy (see §22.13). Flags pages where the purpose is ambiguous or where the stated purpose and actual content diverge.

**Agent 3 — harm-deception**
Checks for deceptive page design, misleading content, hidden intent, and potentially harmful advice. Covers: deceptive page purpose, misleading titles or headings, fake reviews or testimonials, hidden affiliate relationships, dark patterns in CTAs, content that could cause financial harm if followed. Any finding from this agent is a hard fail that blocks a passing score. Uses criteria from §22.17-22.18.

**Agent 4 — mc-quality**
Evaluates Main Content quality across four dimensions: effort, originality, talent, and accuracy (see §22.14). Effort: does the content show meaningful research and synthesis, or is it thin/templated? Originality: does it add information value beyond what exists elsewhere? Talent: does the writing demonstrate subject expertise and editorial judgement? Accuracy: are factual claims correct, are sources current, are prices/rates/dates verified?

**Agent 5 — trust-eeat**
Assesses Experience, Expertise, Authoritativeness, and Trustworthiness at three levels: content creator, content itself, and website (see §22.16). For YMYL content, trust requirements are elevated: anonymous or unqualified authorship on financial advice is a hard fail.

**Agent 6 — reputation**
Evaluates the website's external reputation using the research methods in §22.15. Notes where reputation evidence is absent (not the same as negative reputation). For YMYL pages, absent reputation evidence is a warning.

**Agent 7 — ads-sc-interference**
Assesses whether ads, supplementary content, or interstitials interfere with the main content experience. Checks: ad density relative to content, interstitial timing and dismissibility, affiliate link density per section, whether ads are clearly distinguished from editorial content, mobile ad experience.

**Agent 8 — search-intent**
Evaluates how well the page satisfies the likely search intent behind its target queries using the Needs Met scale (see §22.25-22.30). Checks: does the content answer the core question, does it address follow-up questions, is the information current, does the page require unnecessary effort to extract the answer?

**Agent 9 — editorial-voice**
Cross-references the page against the Editorial OS governance files (09-voice, 10-evidence, 11-comparison, 12-structure, 13-readability, 14-failure-modes). This agent bridges the audit system with the existing editorial system. It checks whether the published page still passes the rules it was built against (content can drift after CMS edits, template changes, or plugin updates).

**Agent 10 — ux-layout**
Evaluates page layout, readability, and user experience. Checks: heading hierarchy, content scanability, mobile responsiveness, font size and contrast, link clarity, table readability, image alt text, page load indicators. Does not require browser testing; evaluates from the HTML/CSS output.

**Agent 11 — site-patterns**
Looks at site-wide patterns that affect individual page quality. Checks: internal linking to and from the audited page, orphan page status, breadcrumb accuracy, category structure coherence, cross-linking between related content, navigation accessibility, sitemap inclusion.

**Agent 12 — final-scorer**
Receives findings from all preceding agents. Produces the final quality rating on the QRG scale (see §22.19-22.22). Applies hard-fail logic: any finding from `harm-deception` caps the score at Low. Any YMYL page without adequate E-E-A-T caps at Medium.

## 22.7 Operating principles

1. **Assess what is published, not what was intended.** The audit evaluates the live or staged page as a reader and rater would encounter it, not the source files or editorial intent behind it.

2. **Use the QRG rating scale, not invented scales.** Ratings map to Lowest / Low / Low+ / Medium / Medium+ / High / High+ / Highest. No numeric scores, no percentage grades, no letter grades.

3. **Hard fails are absolute.** Deceptive content, harmful advice, or missing YMYL trust signals cannot be offset by high quality in other dimensions.

4. **Absence of evidence is not evidence of absence.** If reputation data cannot be found, report "reputation evidence not found" rather than "no reputation." If author credentials are missing, report the gap rather than inferring expertise from content quality.

5. **Separate observation from judgement.** Each agent finding states what was observed, then states the quality implication. Findings do not use padded evaluative language.

6. **Do not invent rater consensus.** The audit produces one assessment. It does not simulate multiple raters or claim statistical confidence.

7. **Actionable over comprehensive.** Each finding that identifies a quality gap must include a specific remediation step. General advice ("improve E-E-A-T") is not acceptable output.

## 22.8 Inputs

- **Required**: A page URL (staging or production) or a page slug that can be resolved to built HTML content
- **Optional**: Target search queries (improves the `search-intent` agent's assessment)
- **Optional**: Agent selection for targeted audits
- **Automatic**: The audit system reads the Editorial OS governance files, the cc_builder output, and site-level metadata as needed

## 22.9 Outputs

A structured quality report containing:

1. **Page classification**: Purpose, YMYL status, page type
2. **Per-agent findings**: Each agent produces a list of observations, each tagged as pass / warning / fail, with remediation steps for warnings and fails
3. **Final quality rating**: QRG scale rating with justification
4. **Hard-fail summary**: Any absolute failures that cap the rating, listed first
5. **Remediation priority list**: Ordered by impact on the final rating, most impactful first

The report is plain text (Markdown). It does not modify any files or push any changes. Remediation is a separate step performed through the normal editorial workflow.

## 22.10 Extension path

- **New agents** can be added by defining a new numbered agent in §22.6 and registering it with the orchestrator. Existing agents are not modified.
- **Custom scoring profiles** can be created for different content types (e.g., stricter YMYL thresholds for credit card pages, relaxed thresholds for opinion posts) by extending the `final-scorer` agent's configuration.
- **Automated scheduling** can be layered on top: a cron job or Monday automation that triggers batch audits on a section and surfaces results.
- **Benchmark tracking** can compare audit scores over time to detect quality drift.

---

# Part B: QRG Reference Material

Source: Google Search Quality Evaluator Guidelines, September 11, 2025 (182 pages). This reference captures the rules, criteria, and definitions that the audit agents assess against.

---

## 22.11 Document structure

The QRG has three parts:

| Part | Sections | Covers |
|---|---|---|
| Part 1: Page Quality Rating | §1.0-11.0 | How to assess the quality of a single webpage |
| Part 2: Understanding Search User Needs | §12.0 | How to interpret queries, user intent, and locale |
| Part 3: Needs Met Rating | §13.0-24.0 | How to rate whether a search result satisfies the user |

Page Quality and Needs Met are two independent rating dimensions. PQ is assessed based on the landing page alone (independent of any query). Needs Met depends on both the query and the result.

---

## 22.12 Webpage anatomy

Every webpage has three content zones:

| Zone | Definition | Examples |
|---|---|---|
| Main Content (MC) | Content that directly helps the page achieve its purpose | Article text, product descriptions, videos, calculators, user reviews, forum posts |
| Supplementary Content (SC) | Content that supports the user experience but is not the primary purpose | Navigation, related links, sidebars, "about the author" blocks |
| Ads/Monetisation | Content displayed for revenue generation | Display ads, affiliate links, sponsored content blocks |

**Page purpose:** Every legitimate page has a purpose. Raters must determine what that purpose is before assessing quality. Common purposes: inform, entertain, sell, facilitate transactions, allow sharing, provide tools/downloads.

**Website context:** Raters research who owns the website and who created the content. They look for About pages, Contact pages, customer service information, editorial policies, and authorship attribution.

## 22.13 Your Money or Your Life (YMYL)

YMYL topics are those where inaccurate, untrustworthy, or low-quality content could cause real harm to people's health, financial stability, safety, or welfare.

### YMYL categories

| Category | Scope |
|---|---|
| Health or Safety | Physical, mental, and emotional health; any form of safety including online safety |
| Financial Security | Topics that could damage a person's ability to support themselves or their family |
| Government, Civics and Society | Elections, voting, civic participation, trust in public institutions |
| Other | Any other topic where low-quality content could hurt people or negatively impact societal welfare |

### YMYL is a spectrum

| Level | Definition | Examples |
|---|---|---|
| Clear YMYL | Inaccurate content could cause direct harm | Tsunami evacuation routes, emergency medical advice, purchasing prescription drugs, voter eligibility rules |
| May be YMYL | A careful person would want reliable sources | Weather forecasts, car reviews, how often to replace a toothbrush |
| Not YMYL | Low-quality content causes no real harm | Music award winners, rock band opinions, jean-washing frequency |

### Decision test for ambiguous topics

1. Would a careful person seek experts or highly trusted sources to avoid harm? → Likely YMYL.
2. Would most people be comfortable consulting friends casually? → Probably not YMYL.

### YMYL consequence for quality standards

Pages on clear YMYL topics are held to the highest Page Quality standards. Low-quality content on YMYL topics is rated more severely than equivalent quality on non-YMYL topics.

**BusinessExpert relevance:** All credit card comparison pages, financial product reviews, and business finance guides are clear YMYL (Financial Security). This elevates the E-E-A-T, accuracy, and disclosure requirements for every page in the credit card section.

## 22.14 Main Content quality assessment

MC quality is assessed across four dimensions:

### Effort
The degree to which a human being actively worked to produce satisfying content. Effort includes direct creation (writing, filming), designing page functionality, or building systems that serve users. Mass-generating pages from freely available content with no oversight does not count. For forums and social media, cumulative participation depth counts as effort.

### Originality
Whether the content is unique and adds value beyond what exists elsewhere. If similar content exists on other sites, determine whether the page being assessed is the original source or a derivative.

### Talent or skill
Whether the content is created with enough craft to provide a satisfying experience. Applies to writing quality, video production, how-to instruction clarity, artistic ability. The standard varies by content type — a social media post has different expectations than a professional documentary.

### Accuracy
For informational pages, factual correctness matters. For YMYL topics, accuracy must be consistent with well-established expert consensus — not just technically defensible but aligned with what experts in the relevant field agree upon.

### Assessment method
Spend genuine time engaging with the MC — read the article, watch the video, test the calculator. Assess whether a person genuinely interested in the topic would be satisfied.

## 22.15 Reputation research

Content may appear high quality on the surface, but reputation research can expose scams, fraud, harmful intent, or persistent unreliability.

### What counts as reputation evidence

- Independent reviews and expert references
- News articles about the site or creator
- Wikipedia articles
- Ratings from independent organisations
- Awards or recognitions (e.g., journalistic awards for news sites)
- Forum discussions and blog posts about the site

### What does not count

- Traffic statistics (Similarweb, etc.) — irrelevant to quality
- What the website says about itself — a starting point only, not definitive
- Social media pages maintained by the website/company itself

### How to research reputation

Recommended search patterns (using IBM as example):
- `[ibm -site:ibm.com]` — exclude the site's own pages
- `["ibm.com" -site:ibm.com]` — search for the domain name
- `[ibm reviews -site:ibm.com]` — search for reviews
- `[ibm site:en.wikipedia.org]` — check Wikipedia

### Reputation of content creators

- For journalists, scientists, academics: educational degrees, peer-reviewed publications, citations, professional employment
- For influencers and bloggers: biographical information, news articles, comments by others in their field
- For ordinary individuals: comments from others on the same page. Absence of reputation information for non-professional creators is neither positive nor negative

### When no reputation information exists

For large websites and professional creators, absence of reputation information is itself a signal. For small local businesses, community organisations, and individuals, it is normal and does not indicate low quality. On YMYL topics, pay extra attention to other quality criteria when reputation evidence is absent.

## 22.16 Experience, Expertise, Authoritativeness, and Trust (E-E-A-T)

### Trust is the most important component

An untrustworthy page has low E-E-A-T regardless of how experienced or expert the creator appears. A financial scammer can be highly experienced at scamming — that does not make the page trustworthy.

### The four components

| Component | Definition | How to assess |
|---|---|---|
| Experience | First-hand or life experience with the topic | A product review from someone who actually used the product; a patient describing their treatment journey |
| Expertise | Knowledge or skill in the subject | Formal qualifications (doctor, electrician) or informal expertise visible in the content (lifelong knitter explaining techniques) |
| Authoritativeness | Whether the site/creator is a recognised go-to source | A government site for passport renewal; the IRS for tax forms; a local business for its own promotions |
| Trust | Whether the page is accurate, honest, safe, and reliable | Secure payment systems for stores; honest reviews not written to sell; accuracy on YMYL informational pages |

### E-E-A-T assessment sources

1. What the website or content creator says about themselves (About pages, profiles) — starting point, not definitive
2. What independent sources say — reviews, references, news articles, expert commentary
3. What is visible in the MC itself — expertise evident from content quality, depth, and reader response

### Conflict of interest

A content creator with a clear financial or personal stake in a topic is less trustworthy for that topic. Manufacturer reviews of their own products, or paid influencer endorsements, are not neutral.

### YMYL and E-E-A-T

On YMYL topics, both experience and expertise can be appropriate depending on purpose:
- If the page provides advice or information: expert-level expertise is typically required
- If the page shares personal lived experience (coping with treatment, describing pregnancy): first-hand experience can be sufficient, provided the content is safe and consistent with expert consensus

| Content type | Required E-E-A-T |
|---|---|
| Prescription drug safety during pregnancy | Medical expert knowledge |
| Sleep tips during pregnancy from other pregnant people | Lived experience sufficient |
| Retirement investment advice | Expert financial knowledge |
| Why a citizen finds voting important | Personal experience sufficient |
| Voter eligibility rules | Authoritative official sources |

## 22.17 Lowest Quality Pages

Lowest is the most severe rating. It applies when a page is untrustworthy, deceptive, harmful, or has deeply undesirable characteristics.

### Screening process

1. Does the page have a harmful purpose or deceive users about its purpose? → Lowest
2. Could the page cause harm to individuals, groups, or society? → Lowest
3. Only if neither applies: assess on standard PQ criteria

### Harm categories

**Harmful to self or individuals (§4.2)**
Pages that encourage, depict, incite, or cause physical, mental, emotional, or financial harm. Includes: incitement of violence, doxxing, how-to guides for violent acts, glorifying atrocities, suicide promotion, pro-anorexia content, health advice contradicting expert consensus that could prevent life-saving treatment, encouraging dangerous behaviour.

Does NOT include: violence in fiction/film, news about violent events, educational content involving gross imagery, explanations of scams designed to warn people, depictions of dangerous activities that clearly communicate risks.

**Harmful to specified groups (§4.3)**
Pages that promote, condone, or incite hatred against people defined by age, caste, disability, ethnicity, gender identity, immigration status, nationality, race, religion, sex/gender, sexual orientation, veteran status, or victims of violent events.

The tone must be serious or mean-spirited (not satirical or critical of ideas/doctrines). Criticism of philosophies is not the same as targeting the people who hold them.

**Harmfully misleading information (§4.4)**
Three types:
1. Harmful and clearly inaccurate information (false election dates, false claims a leader died)
2. Harmful claims contradicting expert consensus (claiming lemons cure cancer, lottery tickets are investments)
3. Harmful unsubstantiated conspiracy theories that erode trust in institutions

Does NOT include: entertainment content, satire, fiction, astrology, personal opinion reviews, reasonably debatable topics, trivial inaccuracies on inconsequential topics.

### Deceptive and untrustworthy pages (§4.5)

| Type | What it looks like |
|---|---|
| Deceptive purpose | Appearing to offer one thing, actually doing another |
| Deceptive creator information | Fake credentials, impersonation, fake author profiles with AI-generated images, false physical addresses |
| Deceptive design | Ads disguised as navigation, misleading buttons, titles unrelated to content, ads covering MC |
| Obstructed MC | Pop-ups that cannot be closed, white-on-white text, ads pushing MC below the fold |
| Malicious behaviour | Scams, phishing, malicious downloads |
| Missing responsible party | Complete absence of who is responsible on YMYL pages |

Paywalls and login requirements on otherwise trustworthy sites are NOT deceptive.

### Spam types (§4.6)

| Type | Description |
|---|---|
| No MC / gibberish | Purpose cannot be determined; MC is incomprehensible or adds nothing |
| Hacked/defaced pages | Modified without owner's permission; comment sections filled with bot spam |
| Expired domain abuse | Purchasing a formerly reputable domain and repurposing it for low-value content |
| Site reputation abuse | Third-party content on an established host site to exploit the host's ranking signals (e.g., payday loan affiliate content on an educational site) |
| Scaled content abuse | Mass-producing content with minimal effort or originality — including using generative AI to create pages that provide no value over existing pages |
| Low effort/originality MC | All or almost all MC is copied, paraphrased, embedded, or reposted with no meaningful original contribution |

The Lowest threshold for copied/derivative content is "all or almost all." The Low threshold (§22.18) is "much of" — a meaningful distinction.

## 22.18 Low Quality Pages

Pages with a beneficial or non-harmful purpose that fail to achieve it well.

**Any one of these justifies a Low rating:**

| Signal | Description |
|---|---|
| Low effort MC | Content created without adequate effort, originality, talent, or skill for the purpose |
| Misleading title | Page title that is slightly misleading, shocking, or exaggerated relative to the actual content |
| Distracting ads/SC | Ads or supplementary content that significantly distract from or interrupt use of the MC |
| Insufficient creator info | Unsatisfying amount of information about who is responsible, on pages where trust is required |
| Mildly negative reputation | Pattern of negative customer experiences or documented problems |
| Inadequate E-E-A-T | Level of experience, expertise, authoritativeness, or trust is insufficient for the topic |

### Low effort, low originality, low added value

The Low rating applies when much (but not all) of the MC is copied, paraphrased, embedded, or reposted with minimal original contribution. Examples: social media reposts with no added comment, "best of" lists based entirely on other sources, pages of embedded videos with no curation.

### Filler content

Content that inflates the page without supporting its purpose. Helpful MC should be placed prominently. Filler that forces users to scroll past irrelevant content to reach what they came for is a Low quality characteristic.

### Exaggerated creator claims

Claims of personal experience or expertise that appear overstated or included merely to impress. E-E-A-T should be assessed from actual content and independently verifiable credentials, not self-reported "I'm an expert" statements.

## 22.19 Medium Quality Pages

Pages that have a beneficial purpose and achieve it. Nothing wrong, but nothing distinguished.

**Medium quality criteria:**
- MC created with adequate (not exceptional) effort, originality, talent, or skill
- Reputation that is not notably positive or notably negative
- Adequate level of E-E-A-T for the purpose
- Ads and SC do not block or significantly interfere with the MC
- Page titles summarise the page accurately
- Adequate website information is present

### Two types of Medium pages

1. **Nothing wrong, nothing special:** All Medium criteria apply. The page works but does not demonstrate characteristics that would justify High.
2. **Mixed with redeeming qualities:** Shows some High quality signs (E-E-A-T, content, reputation) alongside some Low quality signs. The positive and negative balance out.

Medium is the rating for many pages in practice. Most pages are neither exceptional nor problematic.

## 22.20 High Quality Pages

Pages that serve a beneficial purpose and achieve it well. To qualify as High, a page must demonstrate at least one of:

- MC created with a high level of effort, originality, talent, or skill
- Positive reputation of the website for the topic
- High level of E-E-A-T for the purpose

All base criteria must also be met: non-harmful purpose, accurate title, non-intrusive ads/SC, adequate website information.

### High vs Medium MC

| High quality | Low quality |
|---|---|
| Well-organised, edited, curated | Filler mixed with helpful content |
| Meaningful forum discussion with depth | Superficial or minimal participation |
| Clear how-to instructions that enable success | Instructions buried under unhelpful preamble |
| Unique, original photos or footage | Stock or scraped images |
| First-person perspective based on real experience | Summary of others' perspectives |
| Creator showcases genuine talent or skill | Lack of skill prevents page achieving its purpose |

### High E-E-A-T signals

- **Experience:** First-hand experience in social media posts and forums can justify High quality
- **Expertise:** Informal expertise visible in the MC itself counts (not just formal qualifications)
- **Authoritativeness:** Government sites for official forms; local businesses as the authoritative source for their own information; niche community forums as go-to sources
- **Trust:** Especially important for financial transaction pages and YMYL topics

## 22.21 Highest Quality Pages

Pages that serve a beneficial purpose and achieve it very well. The distinction from High is the degree of excellence.

**To qualify as Highest, at least one of:**
- MC created with a very high level of effort, originality, talent, or skill
- Very positive reputation of the website or content creator for the topic
- Very high level of E-E-A-T for the purpose

### Very high quality MC by content type

- **News:** Original investigative reporting, accuracy, depth, described primary sources, professional journalistic standards
- **Artistic content:** Unique original work from highly skilled creators
- **Informational content:** Original, accurate, comprehensive, clearly communicated, reflecting expert consensus

### Very high E-E-A-T

The question: for this specific topic, who is the most trusted source on the internet? If the page being assessed is that source, very high E-E-A-T is justified.

Examples: the IRS website for US tax forms; the National Park Service website for Yosemite; a hospital ranked in the top four nationally; a recipe blogger who has documented years of personal experimentation.

## 22.22 Special page types

### Encyclopedia pages

Quality varies by site. High and Highest only for encyclopedias with very good reputations for accuracy. Wikipedia specifically: generally good reputation, but evaluate each article individually. Well-sourced Wikipedia article on a non-YMYL topic: High range. Thin Wikipedia article: lower than Medium. Factual inaccuracy: Low or Lowest regardless of site reputation.

### Error pages and pages with no MC

- Custom 404 page that helps users navigate: typically Medium (can be higher if genuinely clever and helpful)
- Broken page where other site pages load normally: Low (temporarily broken)
- No MC across many pages on the same site: Lowest (systemic neglect or spam)
- Paywalls and login requirements on trustworthy sites: NOT evidence of untrustworthiness

### Forum and Q&A pages

Rate from the perspective of a reader visiting from search, not a participant. MC includes the original question, all answers, and the resulting discussion.

E-E-A-T assessment: for some topics Experience matters most; for others Expertise visible in the posts. YMYL forum topics require especially careful E-E-A-T assessment.

| Quality level | Forum characteristics |
|---|---|
| Highest | Extremely satisfying conversations with genuine effort, depth, unique insights |
| High | Satisfying discussion with meaningful effort and relevant experience/expertise |
| Medium | Nothing wrong but nothing special, or mixed characteristics |
| Low | Little effort, superficial discussion, lacking experience/expertise, mild inaccuracies |
| Lowest | Harmfully misleading information, advice contradicting expert consensus |

---

## 22.23 Understanding queries and user intent

### Query interpretation types

| Type | Definition |
|---|---|
| Dominant interpretation | What most users mean; usually clear with minimal research |
| Common interpretation | What many or some users mean; a query can have multiple |
| Reasonable minor interpretation | Less common but still helpful to include in results |
| Unlikely minor interpretation | Theoretically possible but very few users intend it |
| No chance interpretation | So unlikely that almost no user would intend it |

### User intent types

| Intent type | Definition | Examples |
|---|---|---|
| Know | Find information or explore a topic | [how does gravity work], [barack obama] |
| Know Simple | Find a specific, short, correct fact (1-2 sentences) | [barack obama height], [weather], [what is starbucks stock price] |
| Do | Accomplish a goal, buy something, interact with a site | [get my GED online], [watch stranger things], [pay parking ticket] |
| Website | Find a specific website or webpage | [reddit login], [walmart.com], [ibm.com] |
| Visit-in-Person | Find a physical place to visit | [car repair shop], [gas stations near me], [dentists] |

Many queries have multiple intents. Err on the side of treating interpretations and intents as reasonable.

### Know Simple test

If most people would agree on a correct answer and it fits in 1-2 sentences, it is Know Simple. Queries that are NOT Know Simple: broad/complex topics, ambiguous queries, controversial topics, queries with no definitive answer, queries where users want to browse or explore.

## 22.24 Locale and freshness

### Locale

Locale (language + region) is always assigned to a query. For location-sensitive queries like [coffee shops near me], user location is critical. For universal queries like [how does gravity work], location is irrelevant.

### Freshness requirements

Some queries demand current information. Stale results should receive low Needs Met ratings.

| Query type | Examples | Freshness requirement |
|---|---|---|
| Breaking news | [tornado], [tsunami] | Information needed immediately; yesterday's news is useless |
| Recurring events | [olympics], [elections], [redsox schedule] | Assume users want the most recent/current event |
| Current information | [population of paris], [airfare from ny to sfo] | Users want the most up-to-date figures |
| Product queries | [iphone], [toyota camry] | Users want the current model/version |

Freshness is generally less critical for Page Quality ratings. A "stale" page can have high PQ if it is an authoritative archival source. But unmaintained websites with outdated/misleading content are a reason for low PQ.

---

## 22.25 The Needs Met scale

Five levels, from best to worst:

| Rating | Definition |
|---|---|
| **Fully Meets (FullyM)** | Special, conservative rating. Only applies when the query has a clear, specific intent and the result completely satisfies all or almost all users |
| **Highly Meets (HM)** | Very helpful result for any dominant, common, or reasonable minor interpretation/intent |
| **Moderately Meets (MM)** | Helpful result but less satisfying than HM |
| **Slightly Meets (SM)** | Less helpful result for a reasonable interpretation, OR helpful for an unlikely minor interpretation |
| **Fails to Meet (FailsM)** | Completely fails to meet the needs of all or almost all users |

## 22.26 Fully Meets criteria

All three conditions must be true:
1. The query interpretation and user intent is specific, clear, and unambiguous
2. There is one specific website, webpage, or fact that all or almost all users are looking for
3. All or almost all users would be completely satisfied by the result

**When appropriate:** User clearly wants a specific webpage (e.g., [amazon] → amazon.com), or a specific fact with a single correct answer that is provided accurately from a trustworthy source.

**Queries that cannot have Fully Meets results:**
- Broad queries ([knitting], [credit cards])
- Famous names with multiple intents ([barack obama])
- Ambiguous queries ([ada] — could be Americans with Disabilities Act, American Dental Association, etc.)

Be conservative: when in doubt, use a lower rating.

## 22.27 Highly Meets criteria

Very helpful results for any dominant, common, or reasonable minor interpretation.

Characteristics:
- Entertaining or enjoyable for entertainment queries
- Representative of real opinions and perspectives for open-ended queries
- Easy to understand, with helpful images/video, in-depth content, expert analysis for informational queries
- Fresh where the query demands it
- Accurate — especially for informational results. YMYL medical/scientific content must reflect expert consensus

No length requirement. A query can have many HM results from diverse sources and perspectives. HM is the highest possible rating for most queries.

## 22.28 Moderately Meets criteria

Helpful but less satisfying results. Nothing inherently wrong — generally average to good. MM results "fit" the query but have fewer valuable attributes than HM. May be slightly harder to understand, slightly out of date, or lack depth.

Also appropriate when a result has some HM aspects but also some SM aspects.

## 22.29 Slightly Meets criteria

Results that are less helpful for a reasonable interpretation, OR helpful for an unlikely interpretation.

Common causes: outdated information, misleading/exaggerated titles that don't match the landing page, content that partially addresses the query but misses a key aspect, results for unlikely minor interpretations.

A result with a very misleading or exaggerated title should be rated SM or lower even if the landing page has quality content.

## 22.30 Fails to Meet criteria

Results that completely fail to meet the needs of all or almost all users.

Causes: off-topic for any reasonable interpretation, addresses a "no chance" interpretation, incorrect/factually wrong information, very outdated for freshness-critical queries, wrong locale, missing a critical aspect, harmful/misleading/untrustworthy content.

**Always rate FailsM** (regardless of other qualities) for:
- Content harmful to self or others
- Content harmful to specified groups
- Harmfully misleading information
- Untrustworthy content
- Spam
- Porn (when user is not looking for it)

### Relationship between Page Quality and Needs Met

These are independent dimensions:
- **Needs Met:** Based on both the query and the result
- **Page Quality:** Based on the landing page alone, independent of any query

Key interaction rules:
1. A result that fails to help the user is always FailsM regardless of how high the Page Quality is. A great page that answers the wrong question is useless.
2. HM requires trustworthiness. The HM rating is not appropriate if the page is untrustworthy, outdated, or inaccurate.
3. Very low PQ can override helpfulness. A page so low quality that it is unhelpful or harmful should be rated FailsM.
4. Exception for website intent: even a very low quality target website should be rated FullyM when the user has clear website intent.

---

## 22.31 Product queries

Product queries do not always have a single clear intent. Three main sub-types: Know (researching), Do (purchasing), Website (navigating to a specific store).

Key principle: many users enjoy browsing and visually exploring products online. Give high Needs Met ratings to results that allow users to research, browse, and make purchase decisions — even when the user may not actually buy online.

Pre-purchase activities that deserve support:
- Researching via reviews and technical specifications
- Understanding available options (brands, models, pricing)
- Viewing and visually browsing options

**BusinessExpert relevance:** Credit card comparison pages serve the product research intent. Pages should support browsing, comparison, and informed decision-making — not just push conversions.
