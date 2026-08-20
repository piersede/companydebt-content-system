# Open Items

Running list of work that is finished except for a decision, a confirmation, or a
push that needs saying out loud. Started 2026-08-18. If you close an item, delete
it rather than marking it done, and keep the reason in the commit message.

There was no to-do convention in this repo before this file. Background tasks that
are genuinely separate pieces of work get spawned as their own session instead of
being listed here; those are noted at the bottom so nothing looks lost.

---

## Needs a human decision

**1. The referral-fee sentence in the commercial disclosure.** Page 65614,
`drafts/65614_closing-a-limited-company.html`, methodology block.

> "We may also receive a fee where you engage another practitioner through our network."

This contradicts the standing rule that Company Debt **is** a licensed insolvency
practice and does not introduce directors out to other practitioners. It sits on
the page that most directly sells the service. Either it is true, and the
positioning rule needs revisiting, or it is boilerplate that drifted in and should
be cut. Flagged by the trust-pass stage on 2026-08-18. Not resolved editorially,
because it is a compliance statement rather than prose.

**2. The Bounce Back Loan anecdote.** Same page. The original sentence was:

> "We have spoken to directors who paid thousands towards a Bounce Back Loan after
> the company failed, believing they had guaranteed it."

Cut on 2026-08-18 because it asserts first-hand casework that could not be
verified, and the standing rule bans invented case anecdotes. The misconception is
still stated on the page, without the claimed caseload. If someone confirms this
is real, it can go back as written, with the confirmation recorded.

**3. Named-IP sign-off on page 65614.** The prose was rewritten in full on
2026-08-17 and again on 2026-08-18. The methodology block currently reads
"This rewritten text is awaiting his review, and the date will be recorded here
once that is done." Chris Andersen needs to review the current text, and the date
goes in when he has. Every other page in the corpus carries the dated form.

**4. Live push of page 65614.** It is on staging and gating 34/34. It has never
been pushed to live and will not be without an explicit instruction naming the
page.

---

## Needs a human decision

**7. Live push of the insolvency data hub (10 pages).** Staging only, gating clean,
verified in-browser. Nine sector detail pages built and content-rewritten this
pass (furniture, recruitment agency, motor vehicle repair, cleaning company,
hotel, plus the four already live: restaurant, road haulage, temporary staffing
agency, estate agency) and five hub-family pages unified to the site's visual
language (flagship `uk-insolvency-statistics`, winding-up petition tracker,
dissolutions vs insolvencies, payment practices & late payment, and the `/data/`
hub landing page). None pushed live; will not be without an instruction naming
the page(s).

**8. Payment practices trend chart uses a Company Debt calculation, not a
published DBT figure.** `scripts/datahub/sources/payment_practices_trend.py`
buckets the raw report-level export into six-monthly periods (most recently
filed report per company per period, ≥30 companies to publish a period,
excludes any period inside its own 45-day filing window). The design handoff's
sample trend was fabricated (it included a period that had not happened yet),
so this replaces it with something real rather than something plausible-looking.
It is still our own aggregation of raw data, not a DBT-published series. Worth a
second pair of eyes on the method before this page is pushed live, given it is
a citation target.

---

## Deferred, small

**5. `cvl_all_in` is a misleading key name.** `data/statutory_fees.json` records
£4,000 to £5,000 under `cvl_all_in`, described as the fixed fee plus
disbursements. It excludes VAT. The page took that key at its word and published
"£4,000 to £5,000 all in", understating the real bill by roughly £800 until the
trust pass caught it. The page is fixed. The key name is not, and it will invite
the same error on the next page that reads it. Worth renaming to
`cvl_fee_plus_disbursements_ex_vat`, or adding an explicit `_excludes_vat: true`.

**9. The nine sector detail pages have not been through the site-alignment pass.**
Item 7's flagship/petition-tracker/dissolutions/payment-practices/hub group now
shares one visual system (Arial, the site's full-bleed hero band, one spacing
rhythm) via `cd_datahub_alignment_css()` in the mu-plugin. The sector pages
(furniture, hotel, etc., generated from `sic_group_stats.py`) run their own,
separate `DASHBOARD_CSS` with different token values and were not part of this
pass since they are a different generator entirely. Not urgent, since they were
never held up as unaligned, but worth knowing before assuming "the hub is
unified" covers all 18 `/data/` pages rather than the 5-page hub family.

**6. MVL link placement on page 65614.** The link to the canonical
`/liquidation/members-voluntary-liquidation/` guide sits in the last line of the
MVL section, after the reader has already been given the full answer. Trust pass
suggested moving it up to just after the relief-rate paragraph, so a reader who
wants the detail leaves before this page does the owner page's job. Soft flag, not
a failure.

---

## Running as separate sessions

- **Dead internal links across `drafts/`.** Two were found on page 65614 and fixed;
  no gate check resolves internal links, so others are likely. Spawned 2026-08-17.
- **Prose edited outside the Bernstein pipeline, corpus-wide.** Establishes how far
  the problem this session uncovered actually spreads, and whether the
  grandfathering in `editorial-os/bernstein-runs/_baseline.json` should be
  narrowed. Includes the 26 pages in commit 1429dc5, whose prose was edited with no
  recorded pipeline run and which are currently grandfathered on the basis that it
  is not established either way. Spawned 2026-08-18.

---

## Awaiting a human decision or action — Google Ads / lead pipeline review, 20 Aug 2026

Full report: `google-ads-auditor/runs/2026-08-20-weekly-audit/report.md` (gitignored;
holds real account data). Everything below was verified read-only. Nothing was changed
in Google Ads, in the CRM, or on the site.

**1. Quick Quote form has produced nothing since 31 July 15:22, while paid ads keep
sending traffic to it.** 88 paid clicks and £738.72 between 1 and 19 Aug; 182 clicks and
£1,584.05 since 15 Jul, making `/quick-quote/` the most expensive landing page on the
account. Ruled out: spam folder (1 entry, from 2023), bin (newest 2022), form disabled
(active, notification active), broken form scripts (they load and bind correctly once a
visitor interacts). Not ruled out, because it needs a real submission and this pass was
read-only: whether a completed submission actually saves. Last entry lands on the same
day as the 31 Jul conversion-forms work. Needs a live test submission, and paid traffic
paused off that page until it passes.

**2. Website form leads stopped reaching Zoho on 7 Aug 16:36.** Confirmed against
converted leads as well, so a converted record is not hiding them. The CRM kept taking
Facebook, live chat and email leads throughout. 12 real entries created 8–19 Aug are not
in the CRM and are named in `forms-to-zoho-reconciliation.csv`. Worth chasing by hand:
entry 8343 (Phil Cooper, 6 Aug), entry 8358 (Spencer Evans, 18 Aug), entry 8355
(17 Aug). The Zoho credentials in `.env` can read Leads but not Contacts or Deals, so
one gap remains open: a record created directly as a Contact would be invisible. Widen
the CRM access, or have someone check one of those names in the CRM.

**3. Ad lead quality is measurably poor, and the evidence is click-level, not
conversion-level.** Of 18 Contact Us entries in August: 4 are sales pitches aimed at
Company Debt, 10 share near-identical templated wording with no company/amount/deadline
named, 2 have no message, 2 are genuine specific director enquiries. Nine entries carry
a Google Ads click tag, and all nine are templated or no-message. Neither genuine
enquiry came from a paid click.

**4. Proposed Search exclusions, awaiting sign-off — not added.** £104.53 of Search's
£208.88 traceable spend in 11–17 Aug went on other firms' names, named individuals and a
postal address. One broad keyword, "licensed insolvency practitioner near me", took
£143.45 of £296.89 — 48% of Search — and £96.94 of that went to competitor-brand
searches. Candidate exclusions and the full term list are in the report. Also consider
narrowing that keyword from broad matching.

**5. Prepaid balance is £873.05,** about 16 days at the current £53.26/day. August spend
to the 19th is £2,646 against £5,425–£6,976 in each of the previous 12 months. No budget
increase recommended until items 1 and 2 are fixed.

**6. Policy restrictions, real but minor for Search, possibly structural for
Performance Max.** Three Search ads are limited under "government documents and official
services" — they took 19 showings and 1 click all week, so the cost is negligible. All
four live Performance Max asset groups are limited, under the same topic plus
"restricted personalised advertising, financial hardship". Performance Max lost 71% of
its available showings to rank rather than budget, and three of its four asset groups
are built around audience targeting that this rule blocks. Worth rewording headlines in
the same sweep; not ahead of items 1 and 2.

**7. The insolvency calculator is not broken — it is unvisited.** The served script is
current and complete; the stale-cache theory was tested and does not hold. Zero paid
clicks to `/insolvency-calculator/` in five weeks, and the Performance Max asset group
built around it is paused. All three real entries it has ever taken reached the CRM
correctly. If it should produce leads, something has to send traffic to it.

**8. Unreconciled, flagged rather than guessed.** Six website form entries carrying an ad
click tag arrived 11–17 Aug, but Google recorded only two conversions across both
campaigns. Either conversion tracking is under-counting form fills, or those tags did not
come from clicks Google billed. Not enough evidence to say which.
