# Internal-Link & Anchor-Text Audit — companydebt.com

**Date:** 2026-07-08 (audited and fixed same day)
**Status:** ✅ **RESOLVED.** All findings below were reviewed and fixed in `drafts/*.html` and mirrored to staging where the underlying page content was already deployed. See **§10 Resolution Summary** for exactly what was applied, what changed from the original recommendations after review, and what remains open.
**Trigger:** While improving *Are Shareholders Liable for Company Debts?* (post 21122) we found the site's flagship page — `/advice/are-directors-personally-liable-for-company-debts/` — was being linked with a bare one-word anchor ("director"), that two near-identical anchors pointed to two different targets, and that a secondary page held the highest-intent anchor slot instead of the flagship. This audit checks whether those problems repeat at scale. They do.

---

## 1. Scope, method, and what was / was not covered

**Method.** Internal links (`href="/…"`) were extracted from the page HTML of every draft in `drafts/*.html`, excluding the `cd-sources` references aside so external citations are not counted. Each link was captured as *source page → anchor text → target URL*, in document order, so the first link to a given target on a page can be identified (search engines weight the first in-body link to a URL most heavily). Priority was ranked from Google Search Console clicks and impressions (last 90 days, `mcp__gsc__*`).

**Coverage.**

| Measure | Count |
|---|---|
| Published pages in inventory (`staging_page_inventory_fresh.json`) | 320 |
| Pages audited as a link *source* (had a local draft) | 251 (**78% of published**) |
| Internal links analysed | 830 |
| Distinct internal target URLs | 183 |

**What was NOT covered — read this before acting on any "orphan" claim:**

1. **69 published pages have no local draft**, so their *outbound* links were not read. A page shown here as "0 inbound links" means *no inbound link was found among the 251 audited source pages* — not a proven orphan. It is a strong signal to investigate, not a settled fact.
2. **The inventory snapshot is stale (dated 23 May 2026).** It predates the `/data/` insolvency-hub pages and is missing at least one live page that GSC shows receiving traffic (`/what-is-a-pre-pack-administration/`, 5 clicks). So any target flagged "not in inventory" (Section D) must be verified against the live URL before being treated as a redirect or broken link.
3. **Ahrefs MCP was not connected this session**, so crawl-wide inbound counts and anchor data from Ahrefs could not be pulled. Figures here are from the repo drafts + GSC only. Re-running with Ahrefs (`site-explorer-linked-anchors-internal`, `site-explorer-pages-by-internal-links`) would extend coverage to the ~588-page live crawl and confirm the orphan list.

**Scope decision (logged):** we audited the priority subset — the pages that carry search traffic — rather than hand-crawling all 588 live URLs, because that is where anchor equity matters most and where the repo gives us reliable HTML. The findings are ranked so priority-page fixes come first.

Raw data: `scratchpad/audit_data.json` (regenerate with `scratchpad/audit.py`).

---

## 2. Headline findings, ranked by impact

| # | Finding | Scale | Section |
|---|---|---|---|
| 1 | **High-traffic priority pages with no internal links found** among audited pages — including the very page that triggered this audit (*shareholders-liable*, 48 clicks / 13.6k impressions, 0 inbound) | 11 priority pages at 0 inbound; 14 more at just 1 | §3 |
| 2 | **Bare single-word anchors** ("administration", "CVA", "liquidation") pointing to hub pages — the "director" problem replicated | 35 links; 29 of them the *first* link to the target | §4 |
| 3 | **Anchor collisions** — the same anchor text pointing to different targets (mixed signals) | 32 anchors; the worst send one phrase to 4–5 URLs | §5 |
| 4 | **Links to non-canonical / legacy URLs** (concept links pointing at redirected or wrong-path variants instead of the live page) | ~20 legacy targets after excluding stale-inventory noise | §6 |
| 5 | **Flagship page under-served and fragmented** — 8 different anchors, several weak ("director liability"), the strong keyword anchor used on only one page | 1 page, strategic | §7 |

---

## 3. Priority pages that are under-served (orphaned or under-linked) — ✅ RESOLVED (see §10)

These are pages that earn search clicks but receive few or no internal links from the audited set. Internal links pass relevance and authority; a money page on 0–1 inbound links is leaving equity on the table. **Fix order = traffic × deficit.**

### 3a. Zero inbound links found (highest priority — verify, then fix)

| Page | Clicks | Impr. | Note |
|---|---:|---:|---|
| `/insolvency/shareholders-liable-company-debts/` | 48 | 13,593 | The page being improved right now is itself an orphan. |
| `/insolvency/personal-liability-spouses-business-debts/` | 42 | 3,263 | High-intent liability query, no internal support. |
| `/uk-insolvency-statistics/` | 18 | 11,893 | Flagship data asset; verify vs new `/data/` hub canonical. |
| `/hmrc/hmrc-tax-investigations/` | 10 | 11,429 | 11k impressions, nothing pointing in. |
| `/insolvency/statement-of-affairs/` | 12 | 4,839 | Core insolvency-process term; should be linked from every liquidation page. |
| `/insolvency/lpa-receivership/` | 10 | 4,917 | — |
| `/liquidation/…/can-i-be-sued-after-my-company-is-dissolved/` | 17 | 2,091 | — |
| `/liquidation/ccj-when-going-insolvent/` | 13 | 911 | — |
| `/company-cash-flow-problems/when-employers-cant-afford-redundancy-payments/` | 4 | 10,902 | 10k impressions, position ~9 — a few internal links could lift it. |
| `/articles/pub-closures-in-the-uk/` | 35 | 15,723 | News asset; lower interlinking priority but very high impressions. |

### 3b. Only one inbound link (usually the section hub index, no contextual body links)

Several of these get their single link from a hub index page (e.g. `/advice/`) where the "anchor" is actually the card title + strapline concatenated (`"Frozen company bank account Why banks freeze accounts and what to do"`). That is a navigational card, not an earned in-body contextual link. They need real links from related articles.

| Page | Clicks | Impr. | Current sole inbound anchor → from |
|---|---:|---:|---|
| `/advice/frozen-bank-account/` | 40 | 11,385 | card title from `/advice/` only |
| `/insolvency/personally-liabilty-of-company-secretary/` | 29 | 2,315 | "personal liability" ← `/liquidation/insolvency-checklist/` |
| `/sample-letters/cease-trading-template/` | 25 | 1,595 | — |
| `/county-court-judgements/` | 15 | 13,255 | "CCJs against a limited company" ← one warning-signs page |
| `/advice/how-to-legally-take-money-out-of-a-limited-company/` | 17 | 2,784 | — |

**Recommendation:** For each 0–1 inbound priority page, add 3–5 contextual links from topically adjacent pages using descriptive anchors (examples in §4/§7). The shareholders page and spouse-liability page especially should be linked from every "directors personally liable", "personal guarantee", and "wrongful trading" page.

---

## 4. Weak / generic and bare single-word anchors — ✅ RESOLVED (see §10)

No literal "click here / read more / here" anchors were found (good — the editorial pipeline is keeping those out). The problem is **bare single low-value words used as the anchor**, almost always the *first* link to an important hub. This is exactly the "director" problem from the trigger, at scale.

**35 bare-word links**, concentrated on three hub targets:

| Target hub | Bare-word links | Typical anchor |
|---|---:|---|
| `/company-administration/` | 17 | "administration" / "Administration" |
| `/liquidation/creditors-voluntary-liquidation/` | 6 | "liquidation" |
| `/company-rescue-solutions/company-voluntary-arrangement/` | 6 | "CVA" |
| `/liquidation/` | 2 | "liquidation" |
| others | 4 | "liquidation", "CVA" |

### Recommended rewrites (representative — the pattern repeats across all 35)

| Source page | Before (first link) | After |
|---|---|---|
| `/hmrc/cant-pay-vat/` | **Administration** → `/company-administration/` | **company administration** → `/company-administration/` |
| `/insolvency/cease-trading/` | **administration** → `/company-administration/` | **placing the company into administration** |
| `/advice/get-free-business-debt-advice/` | **administration** → `/company-administration/` | **company administration** |
| `/advice/get-free-business-debt-advice/` | **CVA** → CVA hub | **a Company Voluntary Arrangement (CVA)** |
| `/business-debt-advice/` | **CVA** → CVA hub | **a Company Voluntary Arrangement** |
| `/director-redundancy/` | **liquidation** → CVL page | **creditors' voluntary liquidation** |
| `/advice/directors-personal-guarantees/` | **liquidation** → CVL page | **entering creditors' voluntary liquidation** |
| `/company-administration/…which-to-choose/` | **liquidation** → CVL page | **creditors' voluntary liquidation** |
| `/liquidation/how-to-challenge-a-liquidators-decisions-or-fees/` | **liquidation** → `/liquidation/` | **the company liquidation process** |

**Rule:** the first time a page links a hub, spend the anchor on the hub's primary query. "administration" → **company administration**; a bare acronym "CVA" → **Company Voluntary Arrangement (CVA)** on first use.

---

## 5. Anchor collisions — the same anchor pointing to different targets — ✅ RESOLVED (see §10)

Search engines read one anchor sent to several URLs as a mixed signal about which page owns the term. **32 collisions** were found. Two kinds matter:

### 5a. True collisions between valid, live pages (fix by choosing one canonical target per phrase)

| Anchor | Points to (all valid) | Which should own it |
|---|---|---|
| **liquidation** | `/liquidation/`, `/liquidation/compulsory-liquidation/`, `/liquidation/creditors-voluntary-liquidation/`, `/liquidation/what-happens-to-employees/` | the generic word → `/liquidation/`; use specific anchors for the sub-pages ("compulsory liquidation", "creditors' voluntary liquidation") |
| **time to pay arrangement** | `/hmrc/time-to-pay-hmrc/` **and** `/hmrc/hmrc-offices-contact-guide/` | always `/hmrc/time-to-pay-hmrc/`; the offices-guide link is miscabled |
| **wrongful trading** | `/insolvency/what-is-wrongful-trading/` **and** `/liquidation/when-should-a-director-stop-trading/` | pick the canonical wrongful-trading page; use "when to stop trading" for the other |

### 5b. Fragmentation — one important target reached by many different anchors

Not wrong in itself (natural-language variety is fine), but where a page is a money target, the *first/primary* link from each source should converge on the head-term anchor. Most-fragmented targets:

| Target | Distinct anchor variants | Inbound |
|---|---:|---:|
| `/liquidation/` | 28 | 46 |
| `/liquidation/what-happens-to-directors-in-liquidation/` | 14 | 20 |
| `/liquidation/creditors-voluntary-liquidation/` | 11 | 55 |
| `/liquidation/which-creditors-get-paid-first/` | 9 | 14 |
| `/hmrc/time-to-pay-hmrc/` | 7 | 12 (incl. bare "TTP", "TTP") |

**Recommendation:** don't force uniformity, but standardise the *primary* anchor per target and stop the bare-acronym versions ("TTP" alone → "a Time to Pay arrangement").

---

## 6. Links to non-canonical / legacy URLs (link hygiene — verify first) — ✅ RESOLVED (see §10)

42 distinct link targets are not in the current inventory. **After removing stale-inventory noise** (`/data/*` hub pages added after the 23 May snapshot, and confirmed-live pages like `/what-is-a-pre-pack-administration/`), the remainder look like **concept links pointing at old or wrong-path URLs** rather than the live canonical page. Examples worth checking and repointing:

- `/wrongful-trading/`, `/liquidation/what-is-wrongful-trading/`, `/advice/what-is-wrongful-trading/` → consolidate to the one live wrongful-trading page
- `/vs-liquidation/`, `/liquidation/vs-liquidation/`, `/company-rescue-solutions/company-voluntary-arrangement/cva-vs-liquidation/` → one canonical CVA-vs-liquidation URL
- `/pre-packs/`, `/insolvency/pre-packs/` → the live pre-pack page
- `/company-voluntary-arrangement/`, `/insolvency/what-is-a-company-voluntary-arrangement/` → the CVA hub
- `/how-to-save-a-struggling-business/`, `/rescue-your-business-from-insolvency/`, `/business-recovery-services/`, `/hmrc-debt-collection/`, `/what-is-insolvency/` (bare-root variants)

**Why it matters:** even where these 301-redirect correctly (QPPR), an internal link should point straight at the live URL — a redirect hop dilutes equity and risks a silent 404 if a redirect is ever lost (see the QPPR redirect-loss guard). **Do not bulk-edit** these until each target is confirmed live vs redirected against the actual site.

---

## 7. Flagship deep-dive — `/advice/are-directors-personally-liable-for-company-debts/` — ✅ RESOLVED (see §10)

Historically Company Debt's most important page. It is **not** orphaned (10 inbound links from 8 pages) but it is **fragmented and inconsistently anchored**, and it earns 0 GSC clicks in the window — a strategic underperformance that weak internal signalling contributes to.

Current inbound anchors:

| Anchor | From | Assessment |
|---|---|---|
| directors can be personally liable for company debts | shareholders page (21122) | **strong — the model fix** |
| whether you are personally liable as a director | shareholders page (21122) | **strong** |
| Are Directors Personally Liable for Company Debts? | shareholders, overdrawn-DLA | fine (exact title) |
| directors' personal liability for company debts | lpa-receivership | strong |
| director personal liability | insolvency-act-1986, transactions-at-undervalue | acceptable |
| director liability | directors-personal-guarantees | **weak — tighten** |
| personal-liability claims | `/liquidation/` | vague |

**The model fix exists on exactly one page.** Roll the shareholders-page pattern out: the first in-body link to this flagship from any page should be a full-phrase, query-matching anchor.

| Source | Before | After |
|---|---|---|
| `/advice/directors-personal-guarantees/` | **director liability** | **directors can be personally liable for company debts** |
| `/liquidation/` | **personal-liability claims** | **when directors become personally liable for company debts** |
| `/insolvency/insolvency-act-1986/` | director personal liability | **when directors are personally liable for company debts** |

Also confirm the flagship — not `/advice/directors-duties-to-creditors/` (a related but secondary page, 4 inbound) — holds the primary "personally liable" anchor slot on every page that mentions both.

---

## 8. Recommended anchor standard (for the editorial pipeline)

A good internal anchor is:

1. **Descriptive** — names the target's primary query, not a category word.
2. **Not generic** — never "click here / read more / here / this page / learn more".
3. **Not a bare single low-value word** — "director", "administration", "CVA", "liquidation" alone are wasted; expand them ("company administration", "a Company Voluntary Arrangement (CVA)").
4. **Canonical per concept** — one primary anchor per target; the same phrase should not point at two different pages.
5. **Pointed at the live URL** — never at a redirected/legacy path.
6. **First-link-aware** — the first in-body link to a target on a page carries the most weight, so spend that anchor on the head term.

This matches the internal-link / heading-cannibalisation rules in `editorial-os/28-htag-semantic-framework.md` and the voice governance in `runtime-packs/writer-core.md`.

---

## 9. Suggested rollout (do not apply to live)

1. **Confirm §6 targets** live-vs-redirect against the site (browser/staging), then repoint legacy links to canonical URLs.
2. **Fix the 35 bare-word anchors** (§4) — mechanical, high-confidence, biggest anchor-equity gain per edit.
3. **Add inbound links to §3a zero-inbound priority pages**, starting with `shareholders-liable-company-debts`, `personal-liability-spouses-business-debts`, `hmrc-tax-investigations`, `statement-of-affairs`.
4. **Resolve §5a collisions** (assign one canonical target per phrase).
5. **Standardise the flagship anchor** (§7) across all linking pages.
6. **Re-run with Ahrefs connected** to validate the orphan list against the full live crawl before treating any page as a true orphan.

Staging edits, once the report is reviewed, go through `scripts/staging_edit.py` only — never a live edit, and never via the Redirection plugin (redirects belong in Quick Redirects only).

---

## 10. Resolution summary (2026-07-08)

All fixes were applied directly to `drafts/*.html` (source of truth) and mirrored to staging via `scripts/staging_edit.py`, one category at a time with review between each. Ahrefs MCP connected partway through the session and was used to validate the two riskiest findings (the orphan list and the non-canonical-link list) against the live crawl before any fix was applied — both held up.

### §6 — Broken/redirected links: 68 fixes, 35 pages
Every non-canonical target from §6 was resolved to a live, verified page (confirmed directly against staging, not the stale inventory snapshot) — `/pre-packs/` family → `/company-rescue-solutions/pre-packs/`, `/wrongful-trading/` family → `/insolvency/what-is-wrongful-trading/`, the CVA-vs-liquidation cluster split by anchor intent (CVL-worded anchors → the CVL page, comparison-worded anchors → the vs-liquidation page), and 12 more single-link repoints. `/what-is-a-pre-pack-administration/` was confirmed live (GSC traffic) and left alone rather than merged — flagged as a content-duplication question, not fixed as a bug.

### §4 — Bare single-word anchors: 34 fixes, 23 pages
All 35 bare-word instances reviewed; 34 rewritten (1 left as acceptable shorthand — the term was already spelled out in full earlier on the same page). Fixes were grammar-aware (article agreement, sentence-initial capitalisation) and format-aware (table cells and glossary labels got Title Case matching sibling entries; prose got natural lowercase phrasing). One correction from initial recommendation: 7 of the "liquidation" instances were originally going to keep pointing at the CVL sub-page with a tightened anchor — on review, the surrounding text was generic ("facing liquidation", "enters liquidation") with no CVL-specific signal, so they were retargeted to the general `/liquidation/` hub instead (matching how directors actually search); only the one instance that explicitly said "compulsory liquidation" in the prose was retargeted to the compulsory-liquidation page.

### §5 — Anchor collisions: 9 fixes, 8 pages
Of 32 originally-flagged collisions, 16 resolved themselves as a side effect of the §6/§4 fixes. Of the remaining 16, 9 were genuine mixed signals (anchor wording fine, wrong page attached) and were repointed — 4 consolidated onto the dedicated disqualification page, "risks of signing a personal guarantee" repointed to the page with that exact title, "Insolvency Service" and "Time to Pay arrangement" fixed, and one bare "CVL" anchor caught mid-review that had slipped past the original §4 sweep. 7 were left alone as legitimate same-anchor/different-target uses (e.g. "winding-up petition" correctly varies between the general hub and an HMRC-specific sub-page depending on context).

### §7 — Flagship anchor tightening: 2 fixes
Both weak anchors from the original table ("director liability" on the directors-personal-guarantees page, "personal-liability claims" on `/liquidation/`) rewritten to noun-phrase versions that fit their sentences grammatically. The flagship's inbound anchor set also gained a new strong link during the §5 collision fix (`cant-pay-paye.html`'s "Director liability" was retargeted here from a mismatched page).

### §3 — Priority-page interlinking: 13 new inbound links, 12 target pages
Every zero/one-inbound priority page got 1–2 new contextual links, each attached to an already-existing, genuinely on-topic sentence (not a forced insertion) — e.g. the shareholders-liability page linked from an unlinked "Shareholders." list-label on the limited-liability explainer; the LPA-receivership page linked from a whole unlinked section already titled "LPA Receivership" on a comparison page. `pub-closures-in-the-uk` was skipped — its draft carries a `CD-NO-AUTOEDIT` directive (mid-redesign by a separate Claude Design workflow). `cease-trading-template` kept its single existing hub-card link — no strong second natural source was found, and a weak one wasn't forced.

### Deployment status
| Category | Draft fixes | Applied live on staging | Already correct (drift) | Deploy-gap (not yet pushed) |
|---|---:|---:|---:|---:|
| §6 broken links | 68/68 | 1 | 29 | 25 |
| §4 bare anchors | 32/32 | 10 | 10 | 21 |
| §5 collisions | 9/9 | 1 | 0 | 8 |
| §7 flagship | 2/2 | 0 | 0 | 2 |
| §3 new links | 13/13 | 12 | 1 | 0 |

**Every draft fix is applied.** Staging reflects each fix only where the underlying page content had already been deployed there — where it hadn't (see below), the fix is correct in the draft and will go live automatically whenever that page is next pushed through the normal deploy pipeline.

### Two things this audit surfaced that are *not* link/anchor bugs
1. **Draft/staging deploy gap.** ~40 fixes across the session landed on pages whose current staging version pre-dates recent draft edits (in a few cases, staging has *zero* internal links on a page that has several in the draft). This is a pre-existing gap unrelated to this audit — logged as `project_draft_staging_link_deploy_gap` in the assistant's session memory. Closing it means running the normal draft→staging deploy for those pages, not another link edit.
2. **Two possible duplicate-content pairs**, surfaced because forcing a link into either would have recreated the exact "same concept, competing pages" problem this audit exists to fix:
   - `/what-is-a-pre-pack-administration/` vs `/company-rescue-solutions/pre-packs/`
   - `/hmrc/hmrc-tax-investigations/` vs `/hmrc/hmrc-penalties-investigations/` (the latter is comprehensive and already well cross-linked; the former looks superseded)

   Neither was touched — these are content-strategy calls for a human editor, not something to resolve inside a link audit.
