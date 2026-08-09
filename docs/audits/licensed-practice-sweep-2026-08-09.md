# Licensed-practice wording sweep — everything outside `drafts/`

**Date:** 9 August 2026
**Scope:** everything the earlier drafts sweep (commit `d05d386`) could not reach — the live site, the
staging site, theme and plugin code, Gravity Forms, Yoast titles and descriptions, the WordPress
options table, reusable blocks, PDFs and cached schema data.

**Rule being enforced:** nothing on the site may say or imply that Company Debt refers, connects,
introduces or matches directors to insolvency practitioners, is an introducer / advisory firm /
referral network / panel / lead generator, does not itself act as an insolvency practitioner, or
receives a referral fee. Company Debt **is** a licensed UK insolvency practice.

---

## 1. Headline result

| Surface | Checked | Problems found | Status |
|---|---|---|---|
| Repo `drafts/` (residue the earlier sweep missed) | 305 files | 25 wording breaches + 85 files with broken grammar | **Fixed** |
| Staging site content | 338 pages + all post types, all statuses | 114 pages | **Fixed and verified** |
| Staging cached schema data | all pages | 1 page | **Fixed** |
| Live site content | 337 pages (whole sitemap) | 183 pages | **Listed below — needs your go-ahead** |
| Theme code (repo + live staging copy over file transfer) | full tree | 0 | Clean |
| Custom plugin code (repo + staging copy) | full tree | 0 | Clean |
| Gravity Forms (live) — descriptions, confirmations, notification emails | 10 forms | 0 | Clean |
| Yoast SEO titles and descriptions (staging database) | all rows | 0 | Clean |
| WordPress options table (CTA/footer copy) | all rows | 0 | Clean |
| Reusable blocks and patterns | all rows | 0 | Clean |
| PDFs and downloadable assets in the repo | 8 files | 0 | Clean |

Two things worth knowing up front:

- **Live is a long way behind staging.** 183 live pages still carry the old wording. Staging is now
  clean. Nothing has been written to live.
- **The earlier sweep left a grammar fault across 85 pages.** A blunt find-and-replace turned
  "our advisory referral network" into "the cases we handle" without fixing the rest of the
  sentence, producing lines like *"we draw on cases handled in the cases we handle"*. That text is
  in the repo, on staging and on live. It is fixed in the repo and on staging; it is part of the
  live list below.

---

## 2. Repo files fixed (`drafts/`)

### 2a. Wording breaches — 25 replacements across 21 files

| File | Offending text | Replacement |
|---|---|---|
| `20435_partnership-voluntary-arrangements.html` | "Company Debt connects directors and business owners with licensed insolvency practitioners. We are not insolvency practitioners ourselves…" | "Company Debt is a licensed UK insolvency practice. Our licensed insolvency practitioners take appointments where formal procedures are appropriate. Nothing on this page constitutes legal or insolvency advice." |
| `20435_partnership-voluntary-arrangements.html` | "We work with insolvency practitioners who deal with insolvent partnerships regularly…" | "In the insolvent-partnership cases we handle, the pattern is consistent:" |
| `24080_can-we-trade-out-of-insolvency.html` | "Company Debt is a commercial insolvency referral service… until a licensed IP is formally instructed." | "Company Debt is a commercial insolvency practice… until a licensed insolvency practitioner is formally instructed." |
| `53166_i-cannot-afford-to-repay-my-debt.html` | "Company Debt provides information and referrals to licensed insolvency practitioners." | "Company Debt is a licensed UK insolvency practice… our own appointments are corporate." |
| `53185_i-need-more-information-about-this-debt.html` | "Company Debt is a commercial insolvency and debt advisory service." | "Company Debt is a commercial insolvency practice." |
| `53243_tell-debt-collector-to-stop-contacting-you.html` | "…business rescue firm advising directors and creditors… we do not earn referral fees from FOS or ICO complaints." | "Company Debt is a licensed UK insolvency practice advising directors and creditors. We do not act for collection agencies." |
| `66786_what-is-wrongful-trading.html` | "We refer directors into our network for exactly this conversation." | "That is exactly the conversation our licensed insolvency practitioners have with directors every week." |
| `67535_pros-and-cons.html` | "Company Debt is an independent advisory service." | "Company Debt is a licensed UK insolvency practice… take appointments where formal procedures are appropriate." |
| `67535_pros-and-cons.html` | "We are not a firm of insolvency practitioners, we do not carry out CVA proposals directly…" | "We do not have a financial interest in any particular insolvency outcome. Where a CVA is the right route, our licensed insolvency practitioners can act as nominee and supervisor under separate engagement." |
| `67757_transactions-at-undervalue.html` | "Company Debt is a commercial insolvency referral service." | "Company Debt is a commercial insolvency practice." |
| `74390_when-a-cva-fails.html` | "Company Debt is a licensed insolvency referral service… We do not act as an insolvency practitioner ourselves…" | "Company Debt is a licensed UK insolvency practice. Our licensed insolvency practitioners take appointments where formal procedures are appropriate. We do not provide legal advice." |
| `74390_when-a-cva-fails.html` | "Company Debt **may receive a referral fee** when directors proceed with an insolvency practitioner or adviser introduced through our service." | **Removed entirely** |
| `7665_company-rescue-solutions.html` | "We do not earn a referral fee for the spoke pages linked above…" | "The spoke pages linked above are part of the same editorial library." |
| `77146_debt-creditor-pressure-hub.html` | "…we do not earn a referral fee for the spoke pages linked above…" | Referral-fee clause removed |
| `77175_professional-services-insolvency.html` | "Company Debt works with licensed insolvency practitioners and specialist professional services advisers across the UK." | "Company Debt is a licensed UK insolvency practice. Our licensed insolvency practitioners take appointments where formal procedures are appropriate." |
| `77175_professional-services-insolvency.html` | "Company Debt is a trading name providing business debt and insolvency information and referral services in the UK." | "Company Debt is a licensed UK insolvency practice." |
| `77181_energy-provider-insolvency.html` | "Company Debt is a UK-based business rescue and insolvency advisory service." | "Company Debt is a licensed UK insolvency practice." |
| `77207_manufacturing-insolvency.html` | "…and work alongside licensed insolvency practitioners and restructuring specialists." | "Company Debt is a licensed UK insolvency practice specialising in UK corporate insolvency and business rescue. Our licensed insolvency practitioners take appointments where formal procedures are appropriate." |
| `77372_company-rescue-recovery-hub.html` | "We do not earn a referral fee for the spoke pages linked above…" | Referral-fee clause removed |
| `77684_debt-charities-uk.html` | "…it acts as a referral service connecting directors with licensed Insolvency Practitioners…" | "Company Debt is a licensed UK insolvency practice. Where Company Debt is mentioned in this article, it is not a charity or a free debt advice service." |
| `77739_which-creditors-get-paid-first.html` | "Company Debt connects directors and creditors with licensed insolvency practitioners who can explain…" | "Company Debt is a licensed UK insolvency practice. Our licensed insolvency practitioners can explain…" |
| `78756_liquidating-a-limited-liability-partnership.html` | "Company Debt connects directors and LLP members with licensed, regulated insolvency practitioners." | "Company Debt is a licensed UK insolvency practice advising directors and LLP members." |
| `79387_use-a-cva-to-close-a-company.html` | "Company Debt is a UK-based information and referral service… **We receive fees when directors proceed with insolvency practitioners**…" | "Company Debt is a licensed UK insolvency practice advising directors facing insolvency. This page does not favour any particular outcome;" |

### 2b. Broken grammar left by the earlier sweep — 85 files, 88 replacements

- "we draw on cases handled **in the cases we handle**" → "we draw on **the cases we handle**"
- "a case we reviewed **through our the cases we handle**" → "a case **we handled**"
- "we're drawing on the cases handled in the cases we handle" → "we're drawing on the cases we handle"

---

## 3. Staging — fixed and verified

**114 pages updated, 126 individual replacements**, applied surgically to the page text (no whole-page
republish, so nothing else on those pages moved). Plus one cached-schema record.

Breakdown:

- **21 pages** — the wording breaches in section 2a above, applied to the live-on-staging copies.
- **86 pages** — the broken grammar in section 2b.
- **9 pages with no repo draft, fixed on staging only:**
  - `/hmrc/controlled-goods-agreement/` (12958), `/hmrc/tax-penalties/` (14775),
    `/insolvency/what-is-limited-liability/` (21011), `/company-cash-flow-problems/cant-pay-business-rates/` (26347),
    `/company-cash-flow-problems/cant-pay-business-energy/` (58601),
    `/company-cash-flow-problems/cant-afford-to-pay-suppliers-what-are-the-options/` (67960),
    `/company-cash-flow-problems/when-employers-cant-afford-redundancy-payments/` (74382) —
    all said *"Company Debt is an insolvency advisory firm."* → *"Company Debt is a licensed UK insolvency practice."*
  - `/winding-up-petitions/what-is-a-winding-up-order/` (67370) and the unpublished `pre-pack-or-cva` (13554) —
    *"Company Debt is a UK insolvency advisory firm."* → same replacement.
  - `/care-home-insolvency/` (77186) — *"an insolvency advisory firm regulated through our licensed insolvency
    practitioners"* and *"case files we triage through our insolvency-practitioner referral network"*.
  - `/sample-letters/request-a-reduced-monthly-payment/` (53174) — same referral-network sentence.
- **6 B2B partner pages** (`/services-to/accountants/`, `/solicitors/`, `/banks/`,
  `/asset-based-and-other-lenders/`, `/creditors/`, plus an unpublished duplicate of the accountants page) —
  *"Our referral services and professional partnerships are updated regularly"* → *"Our professional
  partnerships are updated regularly"*. These pages are about professionals sending work **to** Company
  Debt, which is legitimate; only the phrase describing Company Debt as running "referral services" changed.
- **1 cached schema record** — `/bounce-back-loan-support-hub/what-happens-if-i-default/` (43675). The page
  text was already correct but the search-result data the site publishes for that page was a stale copy
  still saying "insolvency advisory firm". Corrected.

**Verification:** a fresh database scan afterwards returns zero breaches, and 14 representative pages were
re-fetched from staging with the cache bypassed — all render the corrected wording, all at full length
(no truncation).

---

## 4. Live — 183 pages, awaiting your instruction

Nothing was written to live. The full machine-readable list with the exact offending sentence for each
page is at `docs/audits/licensed-practice-sweep-2026-08-09-live-list.json`.

What is on live, by phrase:

| Live pages | Phrase |
|---|---|
| 73 | "Company Debt is a UK insolvency advisory firm" |
| 73 | "our advisory referral network" |
| 60 | "we refer directors to licensed insolvency practitioners" |
| 59 | "Company Debt connects directors…" |
| 51 | "Company Debt is an insolvency advisory firm" |
| 18 | "our insolvency-practitioner referral network" |
| 6 | "our referral network" |
| 4 | "we do not earn a referral fee" |
| 4 | "we do not act as insolvency practitioners" |
| 2 | "Company Debt is an introducer to licensed insolvency practitioners" |
| 2 | "oversees referrals to our panel of licensed insolvency practitioners" |
| 1 each | "we receive a referral fee from some advisers in our network"; "Company Debt may receive a referral fee"; "we are not a firm of insolvency practitioners"; "we are not insolvency practitioners ourselves"; "we do not act as insolvency practitioners directly; we work alongside them"; "Company Debt is a business debt advice service"; "acts as a referral service"; "earns fees when directors instruct one of our regulated insolvency practitioners"; and the rest |

The worst individual pages:

- `/sample-letters/i-have-no-knowledge-of-this-debt/` — *"Company Debt is an introducer to licensed
  insolvency practitioners and specialist debt advisers across the UK. We do not provide legal services
  directly… **we receive a referral fee from some advisers in our network**."* See the open question in
  section 6.
- `/company-rescue-solutions/company-voluntary-arrangement/director-guarantees-in-a-cva/` —
  *"Company Debt is an introducer to licensed insolvency practitioners. We do not act as insolvency
  practitioners ourselves."* plus *"we… can introduce you to the right specialist for your situation."*
- `/company-rescue-solutions/company-voluntary-arrangement/when-a-cva-fails/` — *"Company Debt may receive
  a referral fee…"* and *"Company Debt is a licensed insolvency referral service."*
- `/company-rescue-solutions/company-voluntary-arrangement/pros-and-cons/` — *"We are not a firm of
  insolvency practitioners, we do not carry out CVA proposals directly."*
- `/insolvency-news-commentary/` — *"Company Debt is a business debt advice service. We refer directors to
  regulated insolvency practitioners… We do not act as insolvency practitioners ourselves."*
- `/energy-provider-insolvency/` — *"We do not act as insolvency practitioners directly; we work alongside them."*
- `/insolvency/can-we-trade-out-of-insolvency/` and `/insolvency/transactions-at-undervalue/` — *"reviewed by
  Chris Andersen, who oversees referrals to our panel of licensed insolvency practitioners."*
- `/insolvency/what-happens-if-a-company-cannot-pay-its-debts/` — *"Company Debt is a UK insolvency advisory
  firm that earns fees when directors instruct one of our regulated insolvency practitioners."*

**Every one of these 183 pages except one already has a corrected version in the repo**, so the fix is a
push rather than new writing. The exception is `/winding-up-petitions/what-is-a-winding-up-order/`, which
has no repo draft and was corrected directly on staging.

**Recommended route:** push staging → live per page (or in batches) with `publish_to_live.py`, following
the live-push procedure. Say the word and I will prepare the batch; I will not touch live otherwise.

---

## 5. Things checked and found clean

- **Theme code** — repo `theme/`, `theme-mu-plugins/`, and the live theme tree on the server. No entity
  claims in footers, CTA blocks, sidebars or popups.
- **Custom plugin code** — repo `mu-plugins/` and the server's plugin directory. The only match is a spam
  filter that blocks inbound "lead generation service" emails, which is correct and unrelated.
- **Gravity Forms on live** — all 10 forms: titles, descriptions, field labels, confirmation messages and
  notification emails. Nothing. (The staging forms could not be read directly — the forms API key in
  `.env` is a live key and staging rejects it — but the staging forms render clean on the page and are a
  copy of live.)
- **Yoast SEO titles and meta descriptions** — read straight from the database table Yoast serves them
  from, not from the page. Zero matches.
- **WordPress options table** — where stray CTA copy sometimes hides. Zero matches.
- **Reusable blocks and patterns** — covered by the all-post-types database scan. Zero matches.
- **PDFs** — all 8 in the repo, text extracted and searched. Zero matches.
- **Unpublished and draft content on staging** — included in the scan; three drafts matched and were
  triaged as legitimate (see below).

### Deliberately left alone (legitimate, per your instruction)

- `/insolvency/what-is-an-insolvency-practitioner/` — the warning that *lead-generation firms take a
  substantial referral fee from the IP they introduce you to*. This is criticism of the market and correct.
- `/advice/insolvency-advice-for-directors/` — *"unregulated firms sell 'rescue plans' that turn out to be
  a relabelled introducer fee"*. Same reasoning.
- `whats-the-cheapest-way-to-liquidate-a-company` (unpublished) — warning about unlicensed companies that
  *"refer you to a licensed insolvency practitioner to carry out the actual process"*. Same reasoning.
- References to StepChange, Business Debtline, Citizens Advice and other free debt advice services, and
  referrals to solicitors, tax specialists and personal-guarantee specialists. All real and kept.
- `/insolvency/what-is-the-insolvency-service/` — *"The Insolvency Service is not your insolvency
  practitioner"*. True and about a government body.
- `/insolvency/lpa-receivership/` — *"the receiver does not need to be a licensed insolvency
  practitioner"*. A statement of law.
- MoneyHelper's "Pensions Advisory Service", and job-sector references to "financial advisory services".

---

## 6. Open compliance question — for you, not for me

`drafts/53159_i-have-no-knowledge-of-this-debt.html` previously carried:

> "Any referral we make is based on the nature of your enquiry; **we receive a referral fee from some
> advisers in our network.** This does not affect the editorial content on this page."

That sentence has been removed from the repo draft, **but it is still live** at
`/sample-letters/i-have-no-knowledge-of-this-debt/`, and two related pages still carry variants of it
(`/company-rescue-solutions/company-voluntary-arrangement/when-a-cva-fails/` says "Company Debt **may
receive** a referral fee"; `/insolvency/what-happens-if-a-company-cannot-pay-its-debts/` says the firm
"earns fees when directors instruct one of our regulated insolvency practitioners").

If Company Debt genuinely receives a fee from any third party it refers work to — solicitors, tax
counsel, personal-guarantee specialists, anyone — then removing the disclosure without replacing it may
be the wrong answer legally, and a corrected disclosure may be required. **This is your call, not a
decision the sweep should make silently.** Three possible positions:

1. No such fee exists → the sentences are simply wrong and deletion is right. Nothing further to do.
2. A fee exists for some third-party referrals → we need approved disclosure wording that discloses the
   fee **without** implying Company Debt introduces directors to insolvency practitioners.
3. Uncertain → hold the three pages off the live push until compliance confirms.

I have not touched those sentences on live.

---

## 7. Leftover script on staging — removed

There was a leftover one-shot script on the staging server from an earlier session that day:
`wp-content/mu-plugins/mu-cd-push-f9cf70c59dbf.php`. It was a page-updating script that failed to
delete itself after running; its data file was already gone, so it could not have changed anything, but
it ran on every page request and was guarded only by a fixed token.

Removed on 9 August 2026, with a copy archived to
`docs/archive/mu-plugin-leftovers/mu-cd-push-f9cf70c59dbf.php`. The folder was re-listed afterwards
(nothing of that kind left), five staging pages were re-fetched and render normally with no errors, and
the old trigger address now does nothing.

Every file this sweep itself created was removed and verified gone.
