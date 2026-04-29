# 28. UK Insolvency Semantic H-Tag Framework

**Source:** Theo Cristofari, *UK Insolvency, Liquidation and HMRC Semantic H-Tag Framework v3* (April 2026).

**Status:** Canonical governance for H-tag construction across the Company Debt UK insolvency, liquidation, HMRC, creditor and recovery library.

**Scope:** Every article in those families — new builds, rewrites, and migrations from earlier rubrics.

---

## Purpose

This framework exists to keep every article tightly aligned to its exact title tag and search intent. It stops generic insolvency headings from diluting keyword relevance or causing cannibalisation between similar articles.

The architecture (number and order of H2 sections) is fixed per page family. The semantics inside (the H3 wording) are variable and must be filled from the exact title.

---

## Non-negotiable rules

1. Every H1, H2 and H3 must be semantically relevant to the exact article title.
2. Do not reuse fixed H3s across a whole page family unless the wording is legally essential to that exact topic.
3. If a heading could appear unchanged on five unrelated insolvency articles, it is too generic and must be rewritten.
4. Use the primary keyword, a close semantic variant, a direct legal subtopic, or a direct next-step query in every H3.
5. Do not use body-copy prompts as headings.
6. Do not add broad insolvency sections unless they directly support the page intent.
7. Do not create sections that should be separate dedicated pages.
8. Every page must end with an FAQ section: `H2: Frequently Asked Questions About (Primary Keyword)`. **The FAQ H2 must be the FINAL H2 in the visible article.** No editorial H2 may appear after it.
9. Most pages should stop at H3.
10. Use British spelling and UK legal/business terminology.
11. **Heading cannibalisation rule.** Do not promote neighbouring topics into H3s when they have their own dedicated pages or when they pull the article into a different page intent. Supporting concepts should usually be handled as: (a) table rows, (b) checklist items, (c) bolded labels inside a paragraph, (d) short linked summaries, (e) internal-link cards. An H3 must directly support THIS article's title, not a sibling page's title.
12. **Methodology and Sources sit OUTSIDE the main H-tag flow.** They may exist as a footer module, sidebar, collapsible editorial note, source box, or styled labels (e.g. `<p class="methodology-label"><strong>Methodology and Disclosure</strong></p>` or inside an `<aside>` / `<footer>` / styled `<div>`), but **not as `<h2>` elements in the article body**. Their content (author, reviewer, statutory references, gov.uk links) is required by the pre-publish gate and must be present — only their wrapping element changes.
13. **Heading Promotion test (per-H3, not per-template).** Templates do not authorise an H3 just because the slot exists. Before creating any H3, run the four-question test below. The test is the binding rule; the templates are a starting structure that the test refines.

---

## The Heading Promotion test

Before creating any H3 in any article, ask:

1. Is this subtopic directly part of the article's primary search intent?
2. Is this subtopic specific enough to this article that it would not appear unchanged across several other pages?
3. Would this subtopic likely have its own standalone article elsewhere on the site?
4. Would promoting this subtopic to H3 make the page compete with another guide?

**Use an H3 only when:** yes to 1, yes to 2, no or acceptable to 3, no to 4.

If the subtopic is relevant but broad, adjacent, or cannibalising, demote it into:

- a table row,
- a short bullet,
- a bolded inline label,
- a checklist item,
- an internal-link card,
- or an H4 only if the section needs scanability and a table would be too cramped.

---

## The H3 Demotion list

The following topics each have their own dedicated page on the Company Debt site. Do **NOT** make any of them an H3 on a different article unless the article title is specifically about that topic, the topic is one of the main solutions promised by the title, or the page is explicitly a comparison or decision guide:

- Wrongful Trading
- Director Disqualification
- Preferences (Section 239 IA 1986)
- Transactions at Undervalue (Section 238 IA 1986)
- Personal Guarantees
- Personal Liability Notices (PLN)
- Company Voluntary Arrangement (CVA)
- Administration
- Pre-Pack Administration
- Creditors' Voluntary Liquidation (CVL)
- Members' Voluntary Liquidation (MVL)
- Time to Pay (TTP)
- Winding-Up Petitions
- Statutory Demands
- Validation Orders
- High Court Writs
- Controlled Goods Agreements
- HMRC Penalties
- HMRC Bailiffs
- Insolvency Act 1986
- Companies Act 2006

Otherwise, place them in a table, checklist, short linked summary, or internal-link block.

---

## When to use H3s, tables, H4s, or bolded labels

| Format | Use for |
|---|---|
| **H3** | Causes specific to the primary keyword; stages in the primary process; direct risks specific to the primary keyword; direct actions specific to the primary keyword; decision branches central to the article; FAQ questions |
| **Table** | Risk summaries; option comparisons; creditor-type comparisons; procedure comparisons; director-duty summaries; deadlines and response windows; documents needed; pros and cons; "what happens next" sequences where each row is not a full section |
| **H4** | Long H2 sections that need scanability where the subtopic is important but should not be promoted to H3 AND a table would be too cramped |
| **Bolded label** | Short explanatory items; examples; warning signs; mistakes; brief legal concepts; mini-definitions inside a section |
| **Internal-link card** | Related guides; neighbouring procedures; deeper legal topics; separate HMRC / enforcement pages; full guides on specific insolvency risks |

---

## The semantic slot model

The framework standardises the role of each section, not the exact wording of every heading. H2s may follow common patterns, but H3s should usually be **semantic slots** that are filled from the exact title.

### Bad pattern (too reusable)

```
H2: What Directors Should Do About (Business Debt Keyword)
  H3: Review Cashflow and Creditor Pressure
  H3: Check Whether the Company Is Insolvent
  H3: Stop the Problem Getting Worse
  H3: Get Business Debt Advice Early
```

These H3s could appear unchanged on many unrelated pages. They weaken topical relevance.

### Good pattern (variable, title-specific)

```
H2: What Directors Should Do About (Primary Keyword)
  H3: (First Specific Action Linked to Primary Keyword)
  H3: (Evidence, Document or Test Linked to Primary Keyword)
  H3: (Risk Control Linked to Primary Keyword)
  H3: (Relevant Advice, Application or Procedure Linked to Primary Keyword)
```

The H3s are now slots. Each slot must be replaced with the most precise heading for the exact page title before publish.

---

## Core Bracket Library

| Placeholder | Use when | Example fill |
|---|---|---|
| `(Primary Keyword)` | Exact page topic / title keyword | Validation Orders |
| `(Audience Modifier)` | Who the page is mainly for | UK Company Directors |
| `(Legal Rule Keyword)` | Act, rule, notice, order or duty | Insolvency Act 1986, Personal Liability Notice |
| `(Process Step Keyword)` | A real step in the topic process | Submit a Proof of Debt |
| `(Risk Keyword)` | Specific risk created by the topic | Wrongful Trading Risk |
| `(Director Risk Keyword)` | Director-specific risk | Director Disqualification Risk |
| `(Creditor Keyword)` | Creditor class or action | Secured Creditors, HMRC as a Creditor |
| `(Asset Keyword)` | Asset involved | Company Vehicles, Intellectual Property |
| `(Evidence Keyword)` | Documents or evidence needed | Statement of Affairs, Board Minutes |
| `(Option Keyword)` | Procedure or solution | CVA, Administration, Time to Pay Arrangement |
| `(Enforcement Keyword)` | Enforcement action | High Court Writ, Notice of Enforcement |
| `(HMRC Keyword)` | HMRC-specific topic | Security Bond, Follower Notice |
| `(Related Keyword)` | Closely related guide only | Winding-Up Petition, Proof of Debt |

---

## How to build each page

1. Identify the primary search intent from the article title.
2. Choose the closest page family from the 14 templates below.
3. Replace every bracketed slot with title-specific wording.
4. **Run the Heading Promotion test on every H3 the template suggests.** Demote any H3 that fails the test using the §"When to use H3s, tables, H4s, or bolded labels" matrix.
5. Apply the cross-family section-type patterns below where the section type is one of: Risks, Options, Related Guides, What Directors Should Do.
6. Remove any section that would pull the article into a different page intent.
7. Add only related guides that are one click away from the current query, not broad category links.
8. End with FAQs about the exact primary keyword.

---

## Cross-family section-type patterns

These four patterns override the generic family-template structure for the named section types. They apply to all 14 page families.

### A. Risks section pattern

**Default for broad / overview pages.** Use a single H2 + a risk table. Do **NOT** use H3s for individual risk topics if those risks (wrongful trading, preferences, personal guarantees, PLN, director disqualification, misfeasance, etc.) have their own dedicated pages.

```
H2: What Risks Should Directors Watch With (Primary Keyword)?

[Table with three columns:]
| Risk | Why it matters for (Primary Keyword) | What to do |
|---|---|---|
| **Wrongful trading** | (one sentence) | (one sentence) |
| **Preference payments** | (one sentence) | (one sentence) |
| **Transactions at undervalue** | (one sentence) | (one sentence) |
| **Personal guarantees** | (one sentence) | (one sentence) |
| **HMRC personal liability** | (one sentence) | (one sentence) |
| **Director disqualification** | (one sentence) | (one sentence) |
```

**Promote a single risk to H3 only if** the entire article is about that risk (e.g. on a dedicated wrongful-trading page, "Wrongful Trading Tests" can be an H3; on a creditor-pressure page, it is a row).

### B. Options section pattern

**Default for broad / overview pages.** Use category-level H3s + a procedure comparison table. Do **NOT** make TTP, CVA, Administration, Pre-Pack, CVL, MVL, or Strike-Off into H3s on a broad page.

```
H2: What Options Are Available for (Primary Keyword)?

H3: Informal Agreement or Repayment Plan
H3: Rescue or Restructuring Procedure
H3: Sale, Closure or Insolvency Procedure

[Table with five columns:]
| Option | When it fits | What it does | Main director risk | Related guide |
|---|---|---|---|---|
| **Time to Pay** | (one phrase) | (one phrase) | (one phrase) | [link] |
| **Forbearance** | ... | ... | ... | [link] |
| **CVA** | ... | ... | ... | [link] |
| **Administration** | ... | ... | ... | [link] |
| **Pre-Pack Sale** | ... | ... | ... | [link] |
| **CVL** | ... | ... | ... | [link] |
| **MVL** | ... | ... | ... | [link] |
| **Strike off** | ... | ... | ... | [link] |
```

**Promote a single procedure to H3 only when** the article title is about that procedure or the procedure is one of the article's main search-intent solutions.

### C. Related Guides section pattern

**Default for non-hub articles.** Short link block. No H3 subsections.

```
H2: Related Guides

[3–6 link cards or bullets, descriptive anchors, each pointing to a directly connected sibling page.]
```

Do not turn this section into a second hub. Each related guide must be directly connected to the current article and must not introduce a new branch of intent.

**Recommended link counts:**
- Normal articles: 3–6 links
- Hub pages: 8–12 links (page family 14 only)

### D. What Directors Should Do section pattern

This is the section that bites worst on cannibalisation when written generically. **The H3s must be article-specific actions**, not generic insolvency advice.

```
H2: What Directors Should Do About (Primary Keyword)
  H3: (Immediate Action Specific to Primary Keyword)
  H3: (Document, Evidence or Test Specific to Primary Keyword)
  H3: (Risk-Control Action Specific to Primary Keyword)
  H3: (Relevant Adviser, Regulator or Procedure Specific to Primary Keyword)
```

**Banned generic H3s** (these appear on too many unrelated pages):
- Review Cashflow
- Speak to Creditors
- Get Advice
- Check Solvency
- Consider Insolvency Options

**Banned cannibalising H3s** on broad pages (use the Demotion list):
- Wrongful Trading (unless that's the article)
- Preferences (unless that's the article)
- CVA (unless that's the article)
- Administration (unless that's the article)

**Example — creditor-pressure page (correct):**
```
H3: Build a Creditor Clock List
H3: Record Board Decisions and Cashflow Assumptions
H3: Stop Selective or Connected-Party Payments
H3: Take Advice Before Making Written Offers
```

These H3s only fit a creditor-pressure article. They would not appear unchanged on a wrongful-trading article or a CVA article. That is the test.

---

## Template 1: Specific legal concept, statute or insolvency rule

**Use for:**
- What Is Wrongful Trading?
- What Are Preferential Payments?
- What Are Transactions at Undervalue?
- What Is the Insolvency Act 1986?
- Antecedent Transactions in Corporate Insolvency
- The Companies Act 2006: A Guide

**H-tag structure:**

```
H1: (Primary Keyword): UK Guide for (Audience Modifier)
H2: (Primary Keyword) at a Glance
  H3: Quick Answer: (Primary Keyword)
  H3: Who (Primary Keyword) Applies To
  H3: Main Legal Risk in (Primary Keyword)
  H3: What to Do Next About (Primary Keyword)
H2: What Is (Primary Keyword)?
  H3: (Primary Keyword) Meaning
  H3: (Legal Rule Keyword) Behind (Primary Keyword)
  H3: When (Primary Keyword) Usually Applies
H2: How (Primary Keyword) Works
  H3: (Process Step Keyword)
  H3: (Relevant Time Period or Threshold Keyword)
  H3: (Evidence or Document Keyword)
H2: Examples of (Primary Keyword)
  H3: (Example Keyword Linked to Primary Keyword)
  H3: (Example Keyword Linked to Primary Keyword)
  H3: (Example Keyword Linked to Primary Keyword)
H2: Consequences of (Primary Keyword)
  H3: (Director Risk Keyword)
  H3: (Company Risk Keyword)
  H3: (Creditor or Liquidator Claim Keyword)
H2: How to Reduce Risk Around (Primary Keyword)
  H3: (Risk Control Keyword)
  H3: (Evidence or Record-Keeping Keyword)
  H3: (Advice or Defence Keyword)
H2: Related (Primary Keyword) Guides
  H3: (Directly Related Keyword)
  H3: (Directly Related Keyword)
H2: Frequently Asked Questions About (Primary Keyword)
```

**Notes:** Use fixed H3 wording only where it names the legal concept itself, such as Wrongful Trading, Preferential Payments or Transactions at Undervalue.

---

## Template 2: Director duties, conduct, disqualification and investigations

**Use for:**
- Director Disqualification
- Directors' Duties & Responsibilities
- Director Conduct Review
- Insolvency Investigations Explained
- Directors' Duties to Creditors
- Directors' Duties to Avoid and Disclose Conflicts of Interest

**H-tag structure:**

```
H1: (Director Conduct Keyword): What UK Company Directors Need to Know
H2: (Director Conduct Keyword) at a Glance
  H3: Quick Answer: (Director Conduct Keyword)
  H3: Who (Director Conduct Keyword) Applies To
  H3: Main Director Risk Linked to (Director Conduct Keyword)
  H3: What Directors Should Do About (Director Conduct Keyword)
H2: What Is (Director Conduct Keyword)?
  H3: (Director Conduct Keyword) Meaning
  H3: (Legal Duty or Investigation Keyword)
  H3: When (Director Conduct Keyword) Becomes Relevant
H2: Legal Rules Behind (Director Conduct Keyword)
  H3: (Relevant Act or Legal Duty Keyword)
  H3: (Board Decision or Conduct Keyword)
  H3: (Creditor Duty or Insolvency Trigger Keyword)
H2: Risks Linked to (Director Conduct Keyword)
  H3: (Disqualification Risk Keyword)
  H3: (Personal Liability Risk Keyword)
  H3: (Liquidator or Insolvency Service Keyword)
H2: What Directors Should Do About (Director Conduct Keyword)
  H3: (Specific Action Keyword)
  H3: (Evidence or Board Record Keyword)
  H3: (Advice or Response Keyword)
H2: Mistakes to Avoid With (Director Conduct Keyword)
  H3: (Mistake Keyword)
  H3: (Mistake Keyword)
  H3: (Mistake Keyword)
H2: Related (Director Conduct Keyword) Guides
  H3: (Directly Related Director Duty Keyword)
  H3: (Directly Related Insolvency Risk Keyword)
H2: Frequently Asked Questions About (Director Conduct Keyword)
```

**Notes:** Do not let every director-duties page become a Companies Act overview. Only include statutory sections that match the title.

**Patch v3.2 — H3 promotion controls for director-conduct pages:**

- The conduct topic in the title (e.g. wrongful trading, disqualification, conduct review) may be promoted heavily — H3s for triggers, evidence, defences, court / Insolvency Service interactions tied directly to that conduct topic.
- **Other director liability or conduct topics** must be table rows in a "Risks" or "Related Conduct" table, not H3s.
- **"Related Guides"** — short link card block, not H3-led.

---

## Template 3: Personal liability and personal exposure

**Use for:**
- Can a Director Be Sued Personally by Creditors?
- Can Directors Go to Prison for Company Debt?
- Are Shareholders Liable for Company Debts?
- Can a Company Secretary be Held Personally Liable for Debts?
- Am I Liable for My Spouse's Business Debts?
- Personal Liability Notices
- Overdrawn Directors' Loan Accounts
- Risks of Signing a Personal Guarantee

**H-tag structure:**

```
H1: (Personal Liability Keyword): What UK (Audience Modifier) Need to Know
H2: (Personal Liability Keyword) at a Glance
  H3: Quick Answer: (Personal Liability Keyword)
  H3: When (Personal Liability Keyword) Applies
  H3: Main Personal Risk in (Personal Liability Keyword)
  H3: What to Do About (Personal Liability Keyword)
H2: What Is (Personal Liability Keyword)?
  H3: (Personal Liability Keyword) Meaning
  H3: (Debt, Tax or Claim Keyword)
  H3: Difference Between (Company Liability Keyword) and (Personal Liability Keyword)
H2: When Personal Liability Can Arise From (Primary Keyword)
  H3: (Trigger Keyword)
  H3: (Document, Guarantee or Notice Keyword)
  H3: (Misconduct or Exception Keyword)
H2: What Assets or Income Are at Risk in (Personal Liability Keyword)?
  H3: (Asset Keyword)
  H3: (Income or Credit Keyword)
  H3: (Enforcement or Court Action Keyword)
H2: How (Personal Liability Keyword) Is Enforced
  H3: (Creditor Action Keyword)
  H3: (Court or HMRC Action Keyword)
  H3: (Settlement or Defence Keyword)
H2: How to Reduce Risk From (Personal Liability Keyword)
  H3: (Agreement Review Keyword)
  H3: (Evidence or Conduct Keyword)
  H3: (Professional Advice Keyword)
H2: Related (Personal Liability Keyword) Guides
  H3: (Directly Related Liability Keyword)
  H3: (Directly Related Insolvency Keyword)
H2: Frequently Asked Questions About (Personal Liability Keyword)
```

**Notes:** Avoid generic "limited liability" sections unless the title specifically requires explaining where limited liability stops.

**Patch v3.2 — H3 promotion controls for personal liability pages:**

- The liability named in the title (e.g. PLN, PG, overdrawn DLA) may be promoted heavily — H3s for triggers, mechanism, defences specific to that liability.
- **Neighbouring liability types** (e.g. wrongful trading on a PLN page) must be table rows, not H3s.
- **"What Risks Should Directors Watch With (Liability Keyword)?"** — risk table; H3s only where directly specific to the named liability.
- **"Options"** — H3s only for direct options (settlement, appeal, defence). Use a table for related insolvency or personal-debt routes (IVA, bankruptcy, DRO).

---

## Template 4: HMRC debt, penalties, notices, investigations and enforcement

**Use for:**
- HMRC Criminal Investigations
- HMRC Debt & Enforcement Hub
- HMRC Enforcement Action
- HMRC Follower Notices
- HMRC Fraud Investigations
- HMRC Notice of Enforcement
- HMRC Penalties & Investigations
- HMRC Security Bonds
- HMRC Tax Investigations
- HMRC Tax Penalties
- HMRC Threatening Letters
- HMRC's Debt Collection Process
- Time to Pay Arrangements
- VAT Penalties
- Corporation Tax Penalties

**H-tag structure:**

```
H1: (HMRC Keyword): UK Guide for (Audience Modifier)
H2: (HMRC Keyword) at a Glance
  H3: Quick Answer: (HMRC Keyword)
  H3: Why HMRC Uses (HMRC Keyword)
  H3: Main Risk in (HMRC Keyword)
  H3: What to Do Next About (HMRC Keyword)
H2: What Is (HMRC Keyword)?
  H3: (HMRC Keyword) Meaning
  H3: Taxes or Debts Covered by (HMRC Keyword)
  H3: When HMRC Can Use (HMRC Keyword)
H2: How (HMRC Keyword) Works
  H3: (HMRC Process Step Keyword)
  H3: (Notice, Letter or Deadline Keyword)
  H3: (Payment, Appeal or Compliance Keyword)
H2: Risks Linked to (HMRC Keyword)
  H3: (Financial Penalty Keyword)
  H3: (Enforcement Action Keyword)
  H3: (Director or Personal Liability Keyword)
H2: What to Do if You Receive (HMRC Keyword)
  H3: (First Response Keyword)
  H3: (Evidence or Document Keyword)
  H3: (Appeal, Negotiation or Advice Keyword)
H2: Options for Dealing With (HMRC Keyword)
  H3: (Payment Option Keyword)
  H3: (Dispute or Appeal Keyword)
  H3: (Insolvency or Rescue Option Keyword)
H2: Related (HMRC Keyword) Guides
  H3: (Directly Related HMRC Keyword)
  H3: (Directly Related Tax Debt Keyword)
H2: Frequently Asked Questions About (HMRC Keyword)
```

**Notes:** HMRC pages must keep HMRC as the semantic centre. Do not turn them into broad creditor-pressure pages unless HMRC enforcement is the title intent.

**Patch v3.2 — H3 promotion controls for HMRC pages:**

- Use H3s for: the specific HMRC notice / penalty / investigation / enforcement action in the title; the deadlines or response windows tied to that action; the direct taxpayer or director response; the direct challenge / appeal / negotiation route.
- Use **tables** for: penalties; deadlines; HMRC powers; escalation routes; director risks; payment options; related HMRC notices.
- The "Risks" section: apply the cross-family **Risks pattern (A)** — single H2 + risk table. Promote a risk to H3 only if the article is about that specific risk.
- The "Options" section: apply the cross-family **Options pattern (B)** — three category H3s + a comparison table covering Time to Pay, appeal / review, CVA, Administration, liquidation, PLN, and winding-up where they are options for resolving the named HMRC action. Do not give each route its own H3.
- The "What to Do" section: apply the cross-family **What Directors Should Do pattern (D)** — every H3 must be a specific action tied to the named HMRC action (e.g. "Reply to the s.36 Discovery Assessment Within 30 Days"), not a generic insolvency H3.

---

## Template 5: Enforcement, bailiffs, High Court writs, freezing orders and validation orders

**Use for:**
- Bailiffs & High Court Enforcement Officers
- High Court Writs Explained
- Freezing Orders & Injunctions Explained
- Validation Orders Explained
- What Happens If HMRC Sends Bailiffs to a Business?
- What Happens If HMRC Freezes Your Business Bank Account?
- What Is a Controlled Goods Agreement Letter From HMRC?

**H-tag structure:**

```
H1: (Enforcement Keyword): UK Business Guide to Rights, Risks and Next Steps
H2: (Enforcement Keyword) at a Glance
  H3: Quick Answer: (Enforcement Keyword)
  H3: Why (Enforcement Keyword) Happens
  H3: Main Business Risk in (Enforcement Keyword)
  H3: What to Do Next About (Enforcement Keyword)
H2: What Is (Enforcement Keyword)?
  H3: (Enforcement Keyword) Meaning
  H3: Who Can Use (Enforcement Keyword)
  H3: What (Enforcement Keyword) Allows or Restricts
H2: How (Enforcement Keyword) Works
  H3: (Notice or Court Step Keyword)
  H3: (Premises, Goods or Bank Account Keyword)
  H3: (Deadline or Response Keyword)
H2: Rights and Restrictions in (Enforcement Keyword)
  H3: (Business Rights Keyword)
  H3: (Enforcement Officer Limit Keyword)
  H3: (Court or Application Keyword)
H2: What Directors Should Do About (Enforcement Keyword)
  H3: (First Action Keyword)
  H3: (Document or Evidence Keyword)
  H3: (Payment, Suspension or Challenge Keyword)
H2: Risks of Ignoring (Enforcement Keyword)
  H3: (Asset or Account Risk Keyword)
  H3: (Trading Disruption Keyword)
  H3: (Insolvency Risk Keyword)
H2: Related (Enforcement Keyword) Guides
  H3: (Directly Related Enforcement Keyword)
  H3: (Directly Related HMRC or Creditor Keyword)
H2: Frequently Asked Questions About (Enforcement Keyword)
```

**Notes:** Do not mix all enforcement mechanisms together. A High Court writ page, freezing-order page and validation-order page need different H3s.

---

## Template 6: Solvency, insolvency tests, warning signs and early risk

**Use for:**
- Am I Solvent?
- How to Check If a Company Is Insolvent?
- What Are the Warning Signs of an Insolvent Company?
- What Is the Corporate Insolvency Test?
- Checklist: What to Do When Insolvency Is Likely
- How to Reduce Insolvency Risk

**H-tag structure:**

```
H1: (Solvency Keyword): UK Guide for Company Directors
H2: (Solvency Keyword) at a Glance
  H3: Quick Answer: (Solvency Keyword)
  H3: Who Needs to Check (Solvency Keyword)
  H3: Main Director Risk in (Solvency Keyword)
  H3: What to Do Next About (Solvency Keyword)
H2: What Does (Solvency Keyword) Mean?
  H3: (Solvency Keyword) Meaning
  H3: (Balance Sheet Test Keyword)
  H3: (Cashflow Test Keyword)
H2: How to Assess (Solvency Keyword)
  H3: (Specific Test or Evidence Keyword)
  H3: (Debt Due or Creditor Pressure Keyword)
  H3: (Forecast or Record Keyword)
H2: Warning Signs Linked to (Solvency Keyword)
  H3: (Warning Sign Keyword)
  H3: (Warning Sign Keyword)
  H3: (Warning Sign Keyword)
H2: Director Duties When (Solvency Keyword) Is in Doubt
  H3: (Creditor Duty Keyword)
  H3: (Trading Decision Keyword)
  H3: (Board Record Keyword)
H2: Options After (Solvency Keyword)
  H3: (Rescue Option Keyword)
  H3: (Creditor Negotiation Keyword)
  H3: (Formal Insolvency Option Keyword)
H2: Related (Solvency Keyword) Guides
  H3: (Directly Related Insolvency Test Keyword)
  H3: (Directly Related Director Duty Keyword)
H2: Frequently Asked Questions About (Solvency Keyword)
```

**Notes:** This family can use solvency tests as fixed subtopics only when the page is actually about solvency, not every rescue or debt article.

---

## Template 7: Company liquidation overview, process, costs and timelines

**Use for:**
- What Is Company Liquidation?
- Company Bankruptcy Explained
- How Long Does It Take to Liquidate a Company?
- How Much Does Company Liquidation Cost?
- How to Prepare for Company Liquidation
- List of Documents You'll Need for Liquidation
- Liquidation Deadlines and Time Limits

**H-tag structure:**

```
H1: (Liquidation Keyword): UK Guide for Company Directors
H2: (Liquidation Keyword) at a Glance
  H3: Quick Answer: (Liquidation Keyword)
  H3: Who (Liquidation Keyword) Applies To
  H3: Main Cost, Time or Process Issue in (Liquidation Keyword)
  H3: What to Do Next About (Liquidation Keyword)
H2: What Is (Liquidation Keyword)?
  H3: (Liquidation Keyword) Meaning
  H3: When (Liquidation Keyword) Is Used
  H3: Difference Between (Liquidation Keyword) and (Related Closure Keyword)
H2: How (Liquidation Keyword) Works
  H3: (Liquidation Step Keyword)
  H3: (Liquidator or Meeting Keyword)
  H3: (Creditor or Asset Keyword)
H2: Director Responsibilities During (Liquidation Keyword)
  H3: (Director Action Keyword)
  H3: (Document or Statement Keyword)
  H3: (Conduct Review or Cooperation Keyword)
H2: Costs, Timelines or Documents for (Liquidation Keyword)
  H3: (Cost, Fee or Funding Keyword)
  H3: (Timeline or Deadline Keyword)
  H3: (Required Document Keyword)
H2: What Happens After (Liquidation Keyword)?
  H3: (Company Closure Keyword)
  H3: (Creditor Outcome Keyword)
  H3: (Director Outcome Keyword)
H2: Related (Liquidation Keyword) Guides
  H3: (Directly Related Liquidation Keyword)
  H3: (Directly Related Insolvency Procedure Keyword)
H2: Frequently Asked Questions About (Liquidation Keyword)
```

**Notes:** Cost, timeline and document pages should use those exact concepts heavily. Do not give every liquidation page the same process H3s.

**Patch v3.2 — H3 promotion controls for liquidation / closure pages:**

- Promote procedure-specific steps to H3 only when the article title is about that procedure.
- The "Costs, Assets and Creditor Outcomes" section: prefer a **table** unless costs / assets / outcomes are central to the article title. Only use H3s where each one is title-specific.
- The "Risks" section: apply the cross-family **Risks pattern (A)** — risk table. Do not promote wrongful trading, preferences, misfeasance, or director disqualification to H3 unless the article is about that risk.
- The "Alternatives" section: use broad H3 categories (Rescue / Sale / Closure) plus a comparison table for CVA, Administration, MVL, CVL, Strike-Off. Do not create mini-guides to those routes unless the title is a comparison page.

---

## Template 8: Liquidation assets, contracts, property, pensions and trading assets

**Use for:**
- Company Pensions and Liquidation
- Company Property and Real Estate in Liquidation
- Company Vehicles and Equipment in Liquidation
- Intellectual Property and Trading Assets in Liquidation
- Leases and Contracts in Liquidation

**H-tag structure:**

```
H1: (Asset or Contract Keyword) in Liquidation: UK Guide for (Audience Modifier)
H2: (Asset or Contract Keyword) in Liquidation at a Glance
  H3: Quick Answer: (Asset or Contract Keyword) in Liquidation
  H3: Who Is Affected by (Asset or Contract Keyword) in Liquidation
  H3: Main Risk for (Asset or Contract Keyword) in Liquidation
  H3: What to Do Next About (Asset or Contract Keyword)
H2: What Happens to (Asset or Contract Keyword) in Liquidation?
  H3: (Asset or Contract Keyword) Meaning in Liquidation
  H3: Liquidator Control Over (Asset or Contract Keyword)
  H3: Ownership, Security or Contract Rights in (Asset or Contract Keyword)
H2: How (Asset or Contract Keyword) Is Valued, Sold or Dealt With
  H3: (Valuation Keyword)
  H3: (Sale, Assignment or Termination Keyword)
  H3: (Creditor or Employee Right Keyword)
H2: Director Duties for (Asset or Contract Keyword) in Liquidation
  H3: (Disclosure or Document Keyword)
  H3: (Preservation or Access Keyword)
  H3: (Risk of Misuse or Disposal Keyword)
H2: Common Problems With (Asset or Contract Keyword) in Liquidation
  H3: (Problem Keyword)
  H3: (Problem Keyword)
  H3: (Problem Keyword)
H2: Related (Asset or Contract Keyword) Liquidation Guides
  H3: (Directly Related Asset Keyword)
  H3: (Directly Related Liquidation Process Keyword)
H2: Frequently Asked Questions About (Asset or Contract Keyword) in Liquidation
```

**Notes:** Asset pages should not become generic liquidation guides. Keep the asset, contract or pension term in most headings.

---

## Template 9: Specific closure route or insolvency procedure

**Use for:**
- Creditors' Voluntary Liquidation
- Members' Voluntary Liquidation
- Compulsory Liquidation
- Company Strike Off and Dissolution
- Company Restoration After Liquidation
- CVA vs Strike-Off vs Liquidation
- Liquidation vs Dissolution
- Liquidating a Dormant Company
- Liquidating a Company with No Assets or Bank Account
- Liquidating an LLP
- Liquidating a Charity or Non-Profit
- Liquidating a Group Company or Holding Company

**H-tag structure:**

```
H1: (Procedure Keyword): UK Guide for (Audience Modifier)
H2: (Procedure Keyword) at a Glance
  H3: Quick Answer: (Procedure Keyword)
  H3: Who (Procedure Keyword) Is For
  H3: Main Risk or Requirement in (Procedure Keyword)
  H3: What to Do Next About (Procedure Keyword)
H2: What Is (Procedure Keyword)?
  H3: (Procedure Keyword) Meaning
  H3: When (Procedure Keyword) Is Suitable
  H3: When (Procedure Keyword) Is Not Suitable
H2: How (Procedure Keyword) Works
  H3: (Procedure Step Keyword)
  H3: (Approval, Meeting or Application Keyword)
  H3: (Liquidator, Court or Registrar Keyword)
H2: Requirements for (Procedure Keyword)
  H3: (Eligibility Keyword)
  H3: (Document or Filing Keyword)
  H3: (Debt, Asset or Solvency Requirement Keyword)
H2: Costs, Timescales and Outcomes of (Procedure Keyword)
  H3: (Cost Keyword)
  H3: (Timeline Keyword)
  H3: (Outcome Keyword)
H2: Alternatives to (Procedure Keyword)
  H3: (Alternative Procedure Keyword)
  H3: (Alternative Rescue or Closure Keyword)
  H3: (When to Choose Alternative Keyword)
H2: Related (Procedure Keyword) Guides
  H3: (Directly Related Procedure Keyword)
  H3: (Directly Related Director or Creditor Keyword)
H2: Frequently Asked Questions About (Procedure Keyword)
```

**Notes:** Comparison pages such as *CVA vs Strike-Off vs Liquidation* should keep comparison wording throughout the headings.

**Patch v3.2 — H3 promotion controls for specific closure-route pages:**

- The procedure named in the title may be promoted heavily — its process steps, requirements, costs, and timescales can each be H3.
- Other procedures referenced in the article (e.g. CVA on a CVL page) must be table rows in an "Alternatives" comparison table, not H3s.
- The "Risks" section: apply the cross-family **Risks pattern (A)** — risk table.
- The "Alternatives" section: apply the cross-family **Options pattern (B)** — three category H3s plus a comparison table.

---

## Template 10: Creditor rights, creditor guides and debt recovery in insolvency

**Use for:**
- How to Prove Your Debt in Company Liquidation
- What to Do When an Insolvent Company Owes You Money
- Customer Insolvency in the UK
- Secured vs Unsecured Creditors
- Understanding Creditors in UK Insolvency
- What Is a Preferential and Non-Preferential Creditor?
- Creditor Meetings in Liquidation
- Guide to Creditors' Meetings in Insolvency
- HMRC as a Creditor in Liquidation

**H-tag structure:**

```
H1: (Creditor Keyword): UK Guide for (Audience Modifier)
H2: (Creditor Keyword) at a Glance
  H3: Quick Answer: (Creditor Keyword)
  H3: Who (Creditor Keyword) Applies To
  H3: Main Right or Risk in (Creditor Keyword)
  H3: What to Do Next About (Creditor Keyword)
H2: What Is (Creditor Keyword)?
  H3: (Creditor Keyword) Meaning
  H3: (Creditor Class or Debt Type Keyword)
  H3: How (Creditor Keyword) Fits Into Insolvency
H2: Creditor Rights in (Primary Keyword)
  H3: (Voting, Meeting or Proof of Debt Keyword)
  H3: (Payment Priority Keyword)
  H3: (Information or Challenge Right Keyword)
H2: What Creditors Should Do About (Primary Keyword)
  H3: (First Creditor Action Keyword)
  H3: (Evidence or Invoice Keyword)
  H3: (Claim, Vote or Challenge Keyword)
H2: Risks and Limits for Creditors in (Primary Keyword)
  H3: (Recovery Risk Keyword)
  H3: (Security or Priority Risk Keyword)
  H3: (Deadline or Exclusion Risk Keyword)
H2: Related (Creditor Keyword) Guides
  H3: (Directly Related Creditor Keyword)
  H3: (Directly Related Insolvency Procedure Keyword)
H2: Frequently Asked Questions About (Creditor Keyword)
```

**Notes:** Creditor pages must be written from the creditor viewpoint unless the title is explicitly for directors.

---

## Template 11: Business rescue, recovery, trading, sale and insolvency avoidance

**Use for:**
- Business Recovery Services
- Can We Trade Out of Insolvency?
- Can You Rescue a Business from Insolvency?
- Can You Sell Your Insolvent Business?
- How Can I Stop or Avoid Insolvency?
- How to Save a Struggling Business?
- Creditor Negotiations
- Creditor Pressure
- Alternatives to Company Liquidation
- Funding Options for SMEs
- How to Manage Business Debt

**H-tag structure:**

```
H1: (Recovery Keyword): UK Guide for Company Directors
H2: (Recovery Keyword) at a Glance
  H3: Quick Answer: (Recovery Keyword)
  H3: When (Recovery Keyword) Is Realistic
  H3: Main Risk in (Recovery Keyword)
  H3: What to Do Next About (Recovery Keyword)
H2: What Does (Recovery Keyword) Mean?
  H3: (Recovery Keyword) Meaning
  H3: Difference Between (Recovery Keyword) and (Related Insolvency Keyword)
  H3: When (Recovery Keyword) May Not Be Suitable
H2: How to Assess Whether (Recovery Keyword) Is Possible
  H3: (Viability Test Keyword)
  H3: (Cashflow, Sale or Funding Evidence Keyword)
  H3: (Creditor Outcome Keyword)
H2: Options for (Recovery Keyword)
  H3: (Specific Recovery Option Keyword)
  H3: (Specific Creditor or Funding Option Keyword)
  H3: (Specific Formal Procedure Keyword)
H2: Director Risks During (Recovery Keyword)
  H3: (Wrongful Trading or Loss Increase Keyword)
  H3: (Preference or Undervalue Risk Keyword)
  H3: (Board Evidence or Advice Keyword)
H2: What Directors Should Do About (Recovery Keyword)
  H3: (First Specific Action Linked to Recovery Keyword)
  H3: (Evidence or Forecast Linked to Recovery Keyword)
  H3: (Advice or Procedure Linked to Recovery Keyword)
H2: Related (Recovery Keyword) Guides
  H3: (Directly Related Recovery Keyword)
  H3: (Directly Related Insolvency Option Keyword)
H2: Frequently Asked Questions About (Recovery Keyword)
```

**Notes:** This is the page family that needs the most variable H3s. Do not reuse generic cashflow, creditor pressure or solvency H3s unless the title is about those things.

**Patch v3.2 — H3 promotion controls for business rescue / recovery pages:**

These are broad pages. The defaults below override the generic Template 11 H-tag tree where the section type is one of: Risks, Options, Related Guides, What Directors Should Do.

- **"What Risks Should Directors Watch With (Recovery Keyword)?"** — apply cross-family **Risks pattern (A)**. Risk table. Standard director-liability topics are rows, not H3s, unless the article is about them.
- **"What Options Are Available for (Recovery Keyword)?"** — apply cross-family **Options pattern (B)**. 2–3 category H3s only (Informal Agreement / Rescue or Restructuring / Sale, Closure or Insolvency). TTP, CVA, Administration, Pre-Pack, CVL, MVL, Strike-Off go in the comparison table.
- **"What Directors Should Do About (Recovery Keyword)"** — apply cross-family **What Directors Should Do pattern (D)**. Every H3 must be specific to the title. No generic "Review Cashflow" / "Speak to Creditors" / "Get Advice" H3s.
- **"Related Guides"** — short link card block. No H3 subsections.

---

## Template 12: Insolvency practitioner, liquidator, regulator, fees and meetings

**Use for:**
- Insolvency Practitioner Explained
- Find an Insolvency Practitioner Near Me
- Liquidator's Powers and Duties
- How to Choose the Right Insolvency Procedure
- Can I Choose My Liquidator or Does HMRC Appoint One?
- How to Challenge a Liquidator's Decisions or Fees
- Creditors' Guides to Insolvency Practitioners' Fees
- Creditor Meetings in Liquidation

**H-tag structure:**

```
H1: (Practitioner or Meeting Keyword): UK Guide for (Audience Modifier)
H2: (Practitioner or Meeting Keyword) at a Glance
  H3: Quick Answer: (Practitioner or Meeting Keyword)
  H3: Who Is Involved in (Practitioner or Meeting Keyword)
  H3: Main Right or Risk in (Practitioner or Meeting Keyword)
  H3: What to Do Next About (Practitioner or Meeting Keyword)
H2: What Is (Practitioner or Meeting Keyword)?
  H3: (Practitioner or Meeting Keyword) Meaning
  H3: Role of (Practitioner, Liquidator or Creditor Keyword)
  H3: When (Practitioner or Meeting Keyword) Happens
H2: Powers, Duties or Rights in (Primary Keyword)
  H3: (Power, Duty or Right Keyword)
  H3: (Fee, Vote or Approval Keyword)
  H3: (Challenge or Complaint Keyword)
H2: How (Primary Keyword) Works in Practice
  H3: (Process Step Keyword)
  H3: (Document or Notice Keyword)
  H3: (Decision or Outcome Keyword)
H2: What Directors or Creditors Should Do About (Primary Keyword)
  H3: (Specific Action Keyword)
  H3: (Evidence or Question Keyword)
  H3: (Advice or Challenge Keyword)
H2: Related (Practitioner or Meeting Keyword) Guides
  H3: (Directly Related Liquidator Keyword)
  H3: (Directly Related Creditor Keyword)
H2: Frequently Asked Questions About (Practitioner or Meeting Keyword)
```

**Notes:** Separate "what is an insolvency practitioner" from "find an insolvency practitioner near me"; local-intent pages need location, suitability and selection headings.

---

## Template 13: Specific problem or "Can I" query

**Use for:**
- Can a Supplier Force My Company Into Liquidation?
- Can Directors Pay Themselves Before Liquidation?
- Can I Liquidate My Company with a Bounce Back Loan?
- Can I Start a New Company After Liquidating My Old One?
- Can You Liquidate to Avoid Paying Suppliers?
- Can't Afford to Liquidate
- Can I Be Sued After My Company Is Dissolved?
- Should I Pay HMRC or Suppliers First?
- What Happens If You Ignore HMRC Letters?
- What Happens If HMRC Rejects Your Time to Pay Arrangement?
- What Happens if I Can't Pay the VAT?

**H-tag structure:**

```
H1: (Specific Question Keyword): UK Guide for (Audience Modifier)
H2: (Specific Question Keyword) at a Glance
  H3: Quick Answer: (Specific Question Keyword)
  H3: When (Specific Question Keyword) Applies
  H3: Main Risk in (Specific Question Keyword)
  H3: What to Do Next About (Specific Question Keyword)
H2: Can You (Specific Action Keyword)?
  H3: Legal Position on (Specific Action Keyword)
  H3: When (Specific Action Keyword) May Be Allowed
  H3: When (Specific Action Keyword) Creates Risk
H2: Risks Linked to (Specific Question Keyword)
  H3: (Director Risk Keyword)
  H3: (Creditor or HMRC Risk Keyword)
  H3: (Personal Liability or Enforcement Keyword)
H2: What to Do Before (Specific Action Keyword)
  H3: (First Specific Check Keyword)
  H3: (Evidence or Advice Keyword)
  H3: (Safer Alternative Keyword)
H2: Options if (Specific Question Keyword) Is a Problem
  H3: (Option Keyword)
  H3: (Option Keyword)
  H3: (Option Keyword)
H2: Related (Specific Question Keyword) Guides
  H3: (Directly Related Question Keyword)
  H3: (Directly Related Risk Keyword)
H2: Frequently Asked Questions About (Specific Question Keyword)
```

**Notes:** For question pages, keep the question language. Do not convert them into broad explainers.

**Patch v3.2 — H3 promotion controls for "Specific Problem / Can-I" pages, including creditor-pressure pages:**

- **Triage section** ("Which X Should You Deal With First?") — use H3s only for pressure / problem categories if the article title is about triage. Otherwise use a priority table.
- **"What Risks Should Directors Watch With (Question Keyword)?"** — apply cross-family **Risks pattern (A)**. Risk table. Do not use H3s for wrongful trading, preferences, personal guarantees, PLNs, or disqualification unless the article is specifically about that risk.
- **"What Options Are Left if (Question Keyword) Escalates?"** — apply cross-family **Options pattern (B)**. Use H3s for broad option categories only (Informal / Formal Moratorium or Rescue / Closure). Use a table for TTP, CVA, Administration, CVL, injunctions, validation orders, or other standalone procedures.
- **"What to Do Before Responding"** — apply cross-family **What Directors Should Do pattern (D)**. Every H3 must be a specific action tied to the question, not a generic insolvency H3.
- **"Related Guides"** — short link card block.

---

## Template 14: Hubs, glossaries and section index pages

**Use for:**
- Insolvency & Liquidation Hub
- HMRC Debt & Enforcement Hub
- Glossary of UK Insolvency Terms

**H-tag structure:**

```
H1: (Hub or Glossary Keyword): UK Guide
H2: (Hub or Glossary Keyword) at a Glance
  H3: What This (Hub or Glossary Keyword) Covers
  H3: Who This (Hub or Glossary Keyword) Is For
  H3: How to Use This (Hub or Glossary Keyword)
H2: Key (Hub Topic Keyword) Guides
  H3: (Guide Cluster Keyword)
  H3: (Guide Cluster Keyword)
  H3: (Guide Cluster Keyword)
H2: (Hub Topic Keyword) by Situation
  H3: (Situation Keyword)
  H3: (Situation Keyword)
  H3: (Situation Keyword)
H2: (Hub Topic Keyword) by Risk or Procedure
  H3: (Risk or Procedure Keyword)
  H3: (Risk or Procedure Keyword)
  H3: (Risk or Procedure Keyword)
H2: Frequently Asked Questions About (Hub or Glossary Keyword)
```

**Notes:** Hub pages can use clusters, but each cluster heading must describe a real group and avoid duplicating article H1s unless used as internal navigation.

---

## Worked examples: correct semantic fill

### Can You Sell Your Insolvent Business?

```
H1: Can You Sell Your Insolvent Business? UK Guide for Company Directors
H2: Selling an Insolvent Business at a Glance
  H3: Quick Answer: Can You Sell Your Insolvent Business?
  H3: When Selling an Insolvent Business May Be Possible
  H3: Main Risk in Selling an Insolvent Business
  H3: What Directors Should Do Before Selling an Insolvent Business
H2: How to Assess Whether an Insolvent Business Can Be Sold
  H3: Get an Independent Valuation of the Business
  H3: Check Whether the Sale Could Be a Transaction at Undervalue
  H3: Record Why the Sale Is in Creditors' Interests
H2: Director Risks When Selling an Insolvent Business
  H3: Transactions at Undervalue Risk
  H3: Preference Risk if Connected Parties Benefit
  H3: Misfeasance Risk After Liquidation
H2: Frequently Asked Questions About Selling an Insolvent Business
```

### High Court Writs Explained

```
H1: High Court Writs Explained: UK Business Guide to Enforcement, Risks and Next Steps
H2: High Court Writs at a Glance
  H3: Quick Answer: High Court Writs
  H3: Why a Business May Receive a High Court Writ
  H3: Main Business Risk in a High Court Writ
  H3: What to Do Next About a High Court Writ
H2: What Directors Should Do About a High Court Writ
  H3: Check the Details of the High Court Writ
  H3: Confirm Whether Enforcement Officers Can Attend the Premises
  H3: Review Options to Pay, Set Aside or Suspend the Writ
  H3: Get Advice Before Goods Are Removed
H2: Frequently Asked Questions About High Court Writs
```

### What Happens if a Company Cannot Pay Its Debts?

```
H1: What Happens if a Company Cannot Pay Its Debts? UK Insolvency Guide for Directors
H2: Companies That Cannot Pay Their Debts at a Glance
  H3: Quick Answer: What Happens if a Company Cannot Pay Its Debts?
  H3: When a Company Fails the Cashflow Insolvency Test
  H3: Main Director Risk When Debts Cannot Be Paid
  H3: What Directors Should Do When a Company Cannot Pay Its Debts
H2: What Directors Should Do if a Company Cannot Pay Its Debts
  H3: Identify Which Debts Are Due Now
  H3: Check Whether the Company Has Failed a Solvency Test
  H3: Avoid Taking New Credit Without a Repayment Plan
  H3: Record Decisions Made in Creditors' Interests
H2: Frequently Asked Questions About Companies That Cannot Pay Their Debts
```

### Personal Liability Notices

```
H1: Personal Liability Notices: Understanding Your Personal Risk
H2: Personal Liability Notices at a Glance
  H3: Quick Answer: Personal Liability Notices
  H3: When HMRC Can Issue a Personal Liability Notice
  H3: Taxes Covered by a Personal Liability Notice
  H3: What to Do if You Receive a Personal Liability Notice
H2: How Personal Liability Notices Work
  H3: HMRC Conditions for Issuing a PLN
  H3: Evidence HMRC Uses in a PLN Case
  H3: How to Appeal a Personal Liability Notice
H2: Frequently Asked Questions About Personal Liability Notices
```

---

## Coverage checklist

The titles below are covered by the page families above. Use the assigned family as the starting point, then rewrite H3s so they match the exact title.

**Director duties, conduct and liability — Templates 2 and 3.**
Director Disqualification; Director Liability for CBILS Loans; Directors' Duties & Responsibilities; What are a Company Director's Duties to Avoid and Disclose Conflicts of Interest; What are Directors' Duties to Creditors in the UK; Can a Director Be Sued Personally by Creditors?; Can Directors Go to Prison for Company Debt?; Director Conduct Review; Insolvency Investigations Explained; Are Shareholders Liable for Company Debts?; Can a Company Secretary be Held Personally Liable for Debts?; Am I Liable for My Spouse's Business Debts?

**HMRC debt, penalties and enforcement — Template 4 (with Template 5 overlap for bailiff/seizure pages).**
HMRC Criminal Investigations; HMRC Debt & Enforcement Hub; HMRC Enforcement Action; HMRC Follower Notices; HMRC Fraud Investigations; HMRC Notice of Enforcement; HMRC Penalties & Investigations; HMRC Security Bonds; HMRC Tax Investigations; HMRC Tax Penalties; HMRC Threatening Letters; HMRC's Debt Collection Process; Joint and Several Liability for Unpaid VAT; Time to Pay Arrangements; VAT Penalties; Corporation Tax Penalties; Personal Liability Notices; What Happens If HMRC Rejects Your Time to Pay Arrangement?; What Happens If You Ignore HMRC Letters?; What Happens if I Can't Pay the VAT?

**Enforcement and urgent creditor action — Template 5.**
Bailiffs & High Court Enforcement Officers; High Court Writs Explained; Freezing Orders & Injunctions Explained; Validation Orders Explained; What Happens If HMRC Freezes Your Business Bank Account?; What Happens If HMRC Sends Bailiffs to a Business?; What is a Controlled Goods Agreement Letter From HMRC?; My Company Bank Account is Frozen.

**Solvency, warning signs and tests — Template 6.**
Am I Solvent?; How to Check If a Company is Insolvent?; What Are the Warning Signs of an Insolvent Company?; What Is the Corporate Insolvency Test?; Checklist: What to Do When Insolvency Is Likely; How to Reduce Insolvency Risk; What Happens if a Company Cannot Pay Its Debts?; What Does It Mean When a Company Has Ceased Trading?

**Liquidation overview, routes and closure — Templates 7 and 9.**
What is Company Liquidation?; Creditors' Voluntary Liquidation; Members' Voluntary Liquidation; Compulsory Liquidation; Company Strike Off and Dissolution; Company Restoration After Liquidation; Liquidation vs Dissolution; CVA vs Strike-Off vs Liquidation; Can I Liquidate a Dormant Company?; Can I Liquidate My Company with a Bounce Back Loan?; Can't Afford to Liquidate; Liquidating a Company with No Assets or Bank Account; Liquidating a Group Company or Holding Company; Liquidating an LLP; Liquidating a Charity or Non-Profit; Company Bankruptcy Explained.

**Liquidation assets, contracts and documents — Template 8.**
Company Pensions and Liquidation; Company Property and Real Estate in Liquidation; Company Vehicles and Equipment in Liquidation; Intellectual Property and Trading Assets in Liquidation; Leases and Contracts in Liquidation; List of Documents You'll Need for Liquidation; Statement of Affairs; Liquidation Deadlines and Time Limits.

**Creditor pages — Template 10.**
How to Prove Your Debt in Company Liquidation; What to Do When an Insolvent Company Owes You Money; Customer Insolvency in the UK; Secured vs Unsecured Creditors; Understanding Creditors in UK Insolvency; Preferential and Non-Preferential Creditors; Creditor Meetings in Liquidation; Guide to Creditors' Meetings in Insolvency; HMRC as a Creditor in Liquidation; Creditors' Guides to Insolvency Practitioners' Fees; Can a Supplier Force My Company Into Liquidation?

**Business rescue, recovery and debt management — Template 11.**
Alternatives to Company Liquidation; Business Recovery Services; Can We Trade Out of Insolvency?; Can You Rescue a Business from Insolvency?; Can You Sell Your Insolvent Business?; Creditor Negotiations; Creditor Pressure; Funding Options for SMEs; How to Manage Business Debt; How Can I Stop or Avoid Insolvency?; How to Save a Struggling Business?; Should I Pay HMRC or Suppliers First?

**Practitioners, fees, meetings and regulators — Template 12.**
Insolvency Practitioner Explained; Find an Insolvency Practitioner Near Me; Insolvency Service Explained; Liquidator's Powers and Duties; How to Choose the Right Insolvency Procedure; Can I Choose My Liquidator or Does HMRC Appoint One?; How to Challenge a Liquidator's Decisions or Fees; Creditor Meetings in Liquidation; Creditors' Guides to Insolvency Practitioners' Fees.

**Hubs and reference pages — Template 14.**
Insolvency & Liquidation Hub; HMRC Debt & Enforcement Hub; Glossary of UK Insolvency Terms; Limited Liability Explained; Fixed and Floating Charges Explained; Personal Guarantee Insurance; The Companies Act 2006; Insolvency Act 1986.

---

## Final QA checklist (run on every rewrite)

The 8-question test below is the binding QA. Every standardised template and every rewrite must pass it.

1. **Are H3s reserved for article-specific subtopics?** (Run the 4-question Heading Promotion test on every H3.)
2. **Are neighbouring standalone topics demoted into tables, bullets, H4s, or link cards?** (Check against the H3 Demotion list.)
3. **Are Risk sections using tables** where the risks would otherwise cannibalise other pages? (Cross-family Risks pattern A.)
4. **Are Option sections using comparison tables** where the procedures would otherwise cannibalise other pages? (Cross-family Options pattern B.)
5. **Are Related Guides link blocks** rather than H3-led mini-hubs? (Cross-family Related Guides pattern C.)
6. **Are Methodology and Sources outside the article H-tag flow?** (Styled labels in a footer / aside / div, not `<h2>` elements.)
7. **Are FAQs the final H2?** (No editorial H2 may follow.)
8. **Does the page still satisfy the article title without becoming a hub?** (Hub framing is reserved for Template 14 and titles that explicitly are hubs / decision guides.)

**Plus the original semantic-relevance checks:**

- [ ] Does the H1 match the title-tag intent closely?
- [ ] Does every H2 contain the primary keyword, a close variant, or a necessary legal/commercial subtopic?
- [ ] Could any H3 be reused unchanged on five unrelated pages? If yes, rewrite it.
- [ ] Has the article avoided drifting into a broader insolvency guide?
- [ ] Does the FAQ heading include the primary keyword?

## Heading cannibalisation diagnostic

For each H3 you have written, ask:

1. **Does this H3 belong to a sibling page?** Wrongful trading, preferences, personal guarantees, PLNs, director disqualification, CVA, Administration, CVL, TTP — these all have their own dedicated pages. If your article's H3 is one of these and the article's title is *not* the H3 topic, demote.
2. **Could a reader land on this article and feel they got a half-version of another article?** If yes, you have promoted a neighbouring topic into your hierarchy. Demote the H3 to a table row or short linked summary.
3. **Is the H3 wording specific to this title or generic to the sector?** "Wrongful Trading Risk" is generic. "Wrongful Trading Risk Under Live Creditor Pressure" is title-specific (still likely a demote candidate, because the dedicated page owns the concept).

**Default demotion patterns when a topic should not be an H3:**

- **Risk lists**: convert to a comparison table with columns *Risk / Why it matters in this context / What directors should do*. Each risk is one row, not one H3.
- **Procedure mentions** (TTP, CVA, Administration, CVL, IVA, etc.): use a comparison table with columns *Option / When it fits / When it does not* and link to the dedicated page from each row.
- **Creditor types / sector lists**: bullet list with bolded labels and one-line summaries, each pointing to the spoke article.
- **Statute lists**: inline parenthetical references (e.g. "section 214 of the Insolvency Act 1986 — wrongful trading") rather than dedicated H3s per statute.
- **Long related-guides sections**: a single short H2 *Related Guides* with a flat link list or link cards. No H3 subsections inside it.

The discipline this enforces: every H3 directly serves the article's own title intent. Topics that orbit the title sit in tables, lists, and links — not in the heading hierarchy.

---

## Relationship to other governance

| Governance area | What stays here | What stays elsewhere |
|---|---|---|
| H-tag architecture and slot model | This file | — |
| H-tag QA checklist | This file | — |
| General H2 semantic-relevance principle | Cross-referenced from `18-seo-signal-governance.md` §5a | `18-seo-signal-governance.md` §5a |
| Pre-publish gate enforcement | Cross-referenced from `16-pre-publish-gate.md` Check 14 | `16-pre-publish-gate.md` |
| Article opening formulas, paragraph payoff | — | `12-structure-governance.md`, `24-payoff-intent-first.md` |
| Voice, evaluative discipline, Rules A–J | — | `09-voice-governance.md`, `docs/human-authorship-voice-engine.md` |
| FAQ accordion implementation (Ultimate Blocks) | — | `REWRITE-RUNBOOK.md` step 4 |

The H-tag framework defines **architecture** (where the section sits) and **semantics** (what the section is about). Voice, evidence, paragraph rhythm and pre-publish enforcement remain owned by their existing governance files.

---

## Backfill on existing rewrites

Articles already rewritten under earlier H-tag rubrics will be reassessed against this framework on the user's instruction. The audit will check:

1. Whether each H2 satisfies the architecture for its assigned page family.
2. Whether H3s are slot-specific to the title, not generic.
3. Whether the FAQ H2 is final and keyword-bearing.
4. Whether the page has drifted into a sibling family's intent.

Articles failing any of those will be re-flagged for an H-tag-only rework rather than a full rewrite.

---

*Source document: `UK_Insolvency_Semantic_H_Tag_Framework_v3.docx` — Theo Cristofari, April 2026.*
