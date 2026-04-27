# Article Rewrite Runbook

**Purpose.** This runbook is the canonical workflow for rewriting articles in the Company Debt editorial system. It exists because prior sessions drifted — reconstructing a scoring framework from conversation memory instead of reading the governance files. That drift produced articles that "scored 20/20" against a miscalibrated rubric while failing the actual pre-publish gate.

**Rule zero.** Do not reconstruct a scoring framework from memory. The canonical framework lives in `editorial-os/` and is read by `scripts/article_audit.py`. If a session starts scoring articles without running that script, stop and run it.

---

## The workflow

### 1. Fetch current versions from WordPress staging

Staging URLs follow the pattern `https://comdebstage.wpengine.com/<path>/<slug>/`. Fetch via `scripts/wp_publish.py`'s cookie-auth session (dual-auth: nginx basic + WP login). Save each file to `drafts/<postid>_<slug>.html` with a 3-line metadata header:

```
<!-- TITLE: <title> -->
<!-- POST ID: <id> / TYPE: <pt> / AUTHOR: <author_id> / FM: <featured_media_id> / TEMPLATE: <template> -->
<!-- LINK: <live_url> -->
```

The header is read by the audit script. Do not omit it.

### 2. Audit against the canonical gate

```bash
python scripts/article_audit.py --drafts drafts --slug <postid>
```

That script reads the rules directly from:

- `editorial-os/16-pre-publish-gate.md` — the 16-check gate
- `editorial-os/13-readability-governance.md` — em dashes, paragraph length
- `editorial-os/09-voice-governance.md` — first-person rules, padded evaluation
- `editorial-os/14-failure-modes-and-recovery.md §16` — AI prose fingerprints

The score it produces (out of 20) IS the score. Do not modify.

### 3. Update Monday Pre Score

Monday board `18406273663` ("Content Rework Tracker"), column `text_mm1ypyg5` (Pre Score). Format: `<square> <n>/20` where squares are:

- ⬛ 0–4
- 🟥 5–9
- 🟧 10–14
- 🟨 15–19
- ✅ 20

Use GraphQL variables, not inline strings (Monday's parser rejects surrogate-pair emojis in inline GraphQL).

### 4. Rewrite to 20/20

Write to the canonical gate AND the Tier 3 editorial rules. Target structure:

1. Metadata header (preserve exactly)
2. Opening (2–3 paragraphs). Concrete scene, reader-addressed, no meta-commentary. No banned opening patterns ("this page explains", "in this guide", etc.)
3. **H-tag architecture per `editorial-os/28-htag-semantic-framework.md`.** Identify the article's page family (1–14), then build the H2/H3 structure from the matching template. H2 architecture is fixed by family; H3 wording must be slot-filled from the exact title (no generic, reusable H3s).
4. "Your Next Step" H2 — the Rule J verdict (sits between the family-specific H2s and the Methodology/Sources/FAQ closure)
5. FAQ accordion (`wp:ub/content-toggle-block` from Ultimate Blocks) with 5–7 panels. The FAQ H2 must be the final H2, formatted "Frequently Asked Questions About (Primary Keyword)". This emits FAQPage schema on the frontend.
6. Methodology & Disclosure H2 — who wrote / reviewed, statutory basis, Company Debt disclosure
7. Sources & References H2 — bulleted list with `legislation.gov.uk` links

**H-tag QA before re-audit:** run the 8-question checklist at the foot of `28-htag-semantic-framework.md`. Any H3 that could appear unchanged on five unrelated pages must be rewritten.

### 5. Mechanical gate requirements

The script enforces these. You can fail any one and the gate blocks.

| Check | Rule |
|---|---|
| Em dashes | ≤ 1 in body (Sources block exempt). Use commas, full stops, colons. |
| `you` density | ≥ 8 per 1,000 words |
| `we/our/us` density | ≥ 5 per 1,000 words |
| First-person I/me | < 5 per 1,000 words (ceiling) |
| AI fingerprints | < 3 distinct ("that said", "in summary", "moving on to", "stands out", etc.) |
| Padded evaluation | ≤ 1 stand-alone instance ("genuinely good", "robust", "seamless" without consequence) |
| Generic anchor text | zero ("click here", "read more", "learn more") |
| Banned openings | zero |
| Internal links | ≥ 3 to `companydebt.com` / staging |
| Structural | Methodology, Sources, FAQ accordion, featured image, template, author (ID 34 = Chris Andersen), no body hero image in first 2k chars, word count ≥ 800 |

### 6. Tier 3 editorial rules (Rules A–J)

Source of truth: `editorial-os/docs/human-authorship-voice-engine.md`

The ones that bite most on insolvency content:

- **Rule B — evaluative phrases must be cashed out.** No "useful", "important", "effective", "robust" standing alone. Every evaluation followed by a concrete behaviour, user consequence, or trade-off.
- **Rule C — every H2 section must contain a lived-reality anchor.** For insolvency: the liquidator's letter on the desk, the Friday payroll BACS bounce, the bailiff at the door, the management accounts open on the kitchen table, the Barclays app showing £0.
- **Rule E — praise and criticism include friction.** No neat positives. "An IVA avoids bankruptcy, but pins your cash flow for five years."
- **Rule F — 1–3 asymmetrical editorial lines per article.** Compression that reframes. Examples from this backlog: "The dangerous payment is the quiet one to a spouse's company, not the noisy one." "A liquidator does not read minutes to find what was decided; they read them to find what was not."
- **Rule H — institutional "we" must imply method, labour, or direct observation.** Every "we" passes the two-part first-person test: (a) removing "we" changes meaning, (b) claim is verifiable or human-confirmed. Bad: "In our experience, directors waste time." Good: "Where we audit case files against our referral network, the ones that close cleanest are where the director rang a specialist inside 48 hours."
- **Rule J — verdict must be compressed and reality-based.** The "Your Next Step" section names the true problem, splits the audience (who should act vs who can wait), ends with a real decision frame. Never neutral equilibrium.

Hard fails from Check 1a (`16-pre-publish-gate.md`):
- Fewer than 3 concrete scenes in articles of 1,000+ words
- Fewer than 2 lines of genuine evaluative bite
- 3+ consecutive same-pattern paragraphs (monotone rhythm)
- 3+ sections lacking lived-reality anchors

### 7. Fact-check discipline (hard constraint)

**Do not fabricate statutes, section numbers, case citations, court fees, interest rates, or figures.** If unsure, use a qualitative description ("the petition deposit", "the statutory cap") rather than invent.

**Verified UK figures** (confirmed against `gov.uk` and `legislation.gov.uk` as at April 2026):

- £343 winding-up petition court fee
- £2,600 Official Receiver deposit for creditor WUP
- £750 statutory demand minimum for company
- £800 preferential wages cap (Sch 6 IA 1986)
- £800,000 prescribed part cap (floating charges post-6 April 2020; £600,000 for older)
- £1,350 tools-of-trade exemption (TCG Regs 2013)
- £94 County Court warrant of control
- £313 application on notice / £123 by consent (EX50)
- £377 Part 8 claim (non-money) in County Court
- £680 bankruptcy via adjudicator (£130 admin fee + £550 deposit)
- £751 weekly statutory pay cap from 6 April 2026 (was £719 for 2025/26)
- HMRC late-payment interest: Bank of England base rate + 4% (since 6 April 2025)
- 33.75% s.455 CTA 2010 charge on director loans to participators
- 39.35% additional-rate dividend tax
- 6 months / 2 years preference lookback (s.239 IA 1986)
- 75% CVA voting threshold
- Schedule 24 FA 2007: up to 30% careless, 70% deliberate, 100% deliberate-and-concealed
- Crown preference reinstated 1 December 2020 (Finance Act 2020) for VAT, PAYE, employee NIC, CIS, student loan deductions

**Real statutes/cases that can be cited by name** (subset — check legislation.gov.uk for specific section references):

- Insolvency Act 1986 — ss. 123, 127, 175, 212, 213, 214, 238, 239, 245, Schedule 6
- Companies Act 2006 — ss. 172, 197, 830, 847
- Company Directors Disqualification Act 1986 — ss. 6, 7, 7A, 15A–B
- Law of Property Act 1925 — ss. 101–109 (LPA receivership)
- Insolvency (England and Wales) Rules 2016
- Finance Act 2020 (Crown preference reinstatement)
- Fraud Act 2006
- Proceeds of Crime Act 2002
- *BNY Corporate Trustee Services v Eurosail* [2013] UKSC 28
- *BTI 2014 LLC v Sequana SA* [2022] UKSC 25
- *Re M.C. Bacon Ltd* [1990] BCC 78
- *Salomon v A Salomon & Co Ltd* [1897] AC 22
- *Royal Bank of Scotland v Etridge (No 2)* [2001] UKHL 44
- *Mann v Goldstein* [1968] 1 WLR 1091
- *Re Bayoil SA* [1999] 1 WLR 147

If citing anything else, verify against `legislation.gov.uk` first. When in doubt, omit.

### 8. Re-audit to confirm 20/20

```bash
python scripts/article_audit.py --drafts drafts --slug <postid> --quiet
```

Target: `✅ 20/20 PASS` or at worst `🟨 19/20 PASS` (soft paragraph-length flag).

The two non-editorial reasons for 19/20 FAIL that are acceptable:
- FM=0 (featured image not set in WP admin — flag for WP admin action)
- Author metadata wrong (not 34/Chris Andersen — flag for WP admin action)

Any other failure means iterate the rewrite.

### 9. Push to WP staging

```bash
python scripts/wp_publish.py --file drafts/<postid>_<slug>.html
```

Cookie-auth session handles the dual-auth (nginx basic + WP login). Pushes content only — does not alter status, author, template, or featured media.

### 10. Update Monday Post Score

Column `text_mm29x9z` (Post Score). Same format as Pre Score. GraphQL variables (not inline).

**Never move items between Monday groups.** Status column is managed by the human operator. Only update the score columns.

---

## Tier 3 verification (for larger batches)

After a batch of rewrites, read a random 3–5 articles end-to-end yourself. Do not rely only on the script. The script catches mechanical failures; only a human-quality read catches:

- "we" lines that passed density but fail Rule H (vague without method)
- Padded evaluation the regex missed
- Synthetic rhythm (monotone consecutive paragraphs)
- Authored lines that are filler-dressed-up

---

## Common failure patterns observed on this backlog (avoid)

- **Floating `useful move` / `sensible call`** in CTA openers (Rule B fail)
- **Vague `In our experience…`** without the specific observed detail after (Rule H fail)
- **Neutral verdicts** in "Your Next Step" (Rule J fail)
- **Missing asymmetrical editorial lines** on hub/overview pages (Rule F fail)
- **Over-long paragraphs** (>400 chars) — soft fail but fix
- **`&mdash;` HTML entity** in Sources block — exempt; do not confuse with em dash count
- **Inherited body hero `<figure class="wp-block-image">`** near top of content — rule is featured image theme-level only; strip from body

---

## Monday board reference

- Board: `18406273663` ("Content Rework Tracker")
- Groups: `topics` (Working on it), `group_mm1yh941` (To Rewrite), `group_mm1ybs4p` (Reworked on Staging), `group_mm292vk9` (Pushed Live)
- Columns: `text_mm1ypyg5` (Pre Score), `text_mm29x9z` (Post Score), `color_mm1ye6cd` (Status), `link_mm1ywn7s` (Staging URL)

---

## When this runbook is wrong

If a user correction contradicts this runbook, the correction wins. Update this runbook at the same time, in the same PR. A runbook that drifts from the actual operating standard is worse than no runbook.
