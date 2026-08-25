# Open Items

Running list of work that is finished except for a decision, a confirmation, or a
push that needs saying out loud. Started 2026-08-18. If you close an item, delete
it rather than marking it done, and keep the reason in the commit message.

There was no to-do convention in this repo before this file. Background tasks that
are genuinely separate pieces of work get spawned as their own session instead of
being listed here; those are noted at the bottom so nothing looks lost.

---

## Needs a human decision

**0. The live WordPress application password stopped authenticating after the
2026-08-22 Custom push.** Scripted admin access to production is gone. The site,
the forms, the leads and the Gravity Forms API key are all unaffected.

Diagnosed, not guessed. Three requests to `/wp-json/wp/v2/users/me`:

| credential | response |
| --- | --- |
| the real one | `rest_not_logged_in` |
| deliberately wrong password | `rest_not_logged_in` |
| a username that does not exist | `rest_not_logged_in` |

All identical. WordPress is not checking the password at all, so the stored
password is almost certainly still valid. The header does reach WordPress: the
Gravity Forms key uses the same `Authorization` header and returns 200. The
site still advertises application-password support at
`/wp-json/` → `authentication`.

So application-password auth specifically has been turned off on production.
Most likely `wp_options` carried a security-plugin setting over from staging in
the push; the `wp_itsec_*` tables show a security plugin is installed. It broke
at exactly the moment of the push and nothing else changed.

Not damage, a setting. To resolve: in wp-admin check the security plugin for
anything covering the REST API, XML-RPC or application passwords, and compare
with what production had before. Regenerating the application password is the
fallback.

**Check at the same time:** whether the user list on production still looks
right. `wp_users` and `wp_usermeta` were deselected in the push and verified at
the time, but not re-verified at the end after the search filter was changed
several times. If they travelled anyway, any account created on production since
the last clone is gone. Clearing the cache did not help, which is already ruled
out.

Blocks: future scripted pushes to live via `publish_to_live.py` and
`push_site_content_live.py`. Does not block anything currently running.

**1. "practical experience from cases handled by licensed practitioners in our
network."** Roughly ten pages carry this in their sources-of-fact block, for
example `drafts/26298_misfeasance.html` and
`drafts/31199_business-restructuring.html`.

Same positioning problem as the referral-fee sentence removed on 2026-08-21: it
implies Company Debt draws on practitioners outside itself, when the standing
rule is that Company Debt IS the practice. It makes no fee claim, so it is
milder, and it may simply be accurate if associates are involved. Left
deliberately unchanged pending a decision rather than swept up with the fee
sentence. If it should go, the fix is "our practitioners" or "the cases we
handle".

Separately and NOT a problem: "They provide free, impartial guidance and can
refer you to an IP if needed" describes what debt charities do, not what
Company Debt does. Leave it.

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
holds real account data). Updated the same day with the Moneypenny call log. Everything below was verified read-only. Nothing was changed
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

**3. Ad lead quality is measurably poor on the WEBSITE FORMS ONLY. The phone is fine.**
Of 18 Contact Us entries in August: 4 are sales pitches aimed at Company Debt, 10 share
near-identical templated wording with no company/amount/deadline named, 2 have no
message, 2 are genuine specific director enquiries. Nine entries carry a Google Ads click
tag, and all nine are templated or no-message. Neither genuine enquiry came from a paid
click. Against that, the Moneypenny call log (22 May - 19 Aug, 35 calls) shows August at
4 of 6 calls graded A or B - 67%, the best of the four months, better than June. So the
quality complaint is real and is specific to the forms, not to demand.

**3b. Company Debt phone calls stopped reaching the CRM on 13 July** - three weeks before
the website forms did. The "Phone - CD" lead source holds 8 records between 22 May and
20 Aug (1, 5, 11, 23, 24 Jun; 13 Jul x2; then a test record on 28 Jul). Four match a
Moneypenny call by name exactly, so the process did work. Since 13 Jul, Moneypenny has
logged 8 calls including two graded A, and only one reached the CRM - Anoma Radkevitch,
6 Aug, filed as a live chat rather than a call and with her email missing. Over the same
window "Phone - AABRS" recorded 18 leads, newest 17 Aug. Call logging is alive on the
sister firm and dead on Company Debt, which points at a process or setting on the CD side.
Even in the working period the gap was wide: 19 Moneypenny calls in June against 5 CRM
phone leads.

**3c. Six callers are waiting for a call back and are not in any system.** Oldest is
6 Jul. Three are grade A. Full detail in the report; the short list is Dean Morris
(18 Aug, A, hot), Anthony Wallox / Metro Real Estate (17 Aug, B), Johnny Chicaiza /
El Escorial (14 Aug, B - ask for the owner Juan), Anoma Radkevitch / Flowerdot Limited
(6 Aug, A - EMAIL anomarad@hotmail.com, she will not answer an unknown number), Shaily
Shah (22 Jul, B, call 07721 648556), Simon Dubock / Dubock Ltd (6 Jul, A, hot). This
costs nothing and should go first.

**3d. Call volume fell in JULY, a month before the budget cut, so the cut cannot be its
cause.** June 19 calls (0.63/day), July 6 (0.19/day), August 6 in 19 days (0.32/day).
Treat this as suggestive only: Moneypenny answers overflow, not every call, so a fall can
mean fewer calls or better in-house answering, and 35 calls over 90 days is a small
sample. Settling it needs the total call count from the phone system, not the overflow
log.

**3e. Six of the ten out-of-scope calls were sole traders or individuals with personal
debt** - exactly what the agreed exclusion list is meant to keep out, and they still
reached the phone. A second, independent reason to tighten the Search exclusions in
item 4.

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

---

## WebP Express can hide the header logo again (25 Aug 2026)

The site logo disappeared from every page on 25 Aug. The image file was fine. WebP
Express answered the logo's URL with a redirect that pointed back at itself, and the
edge cache stored that answer for a year. A cache purge on the live install brought the
logo straight back, and the logo now loads on desktop and mobile.

Nothing in the repo changed, because nothing in the repo was wrong.

**The decision needed.** WebP Express can do the same thing to any theme image that a
script or a stylesheet calls by its plain URL. Two ways to stop it:

1. Exclude `wp-content/themes/` from WebP Express.
2. Turn off its redirect-to-itself mode.

Both are settings in the live WordPress admin, so a human has to make the change. Until
one of them is done, the outage can repeat without warning.

**If it repeats**, purge the live caches through the WP Engine interface, or run the
three purges recorded in the session notes. Full write-up:
`~/.claude/projects/*/memory/reference_webp_express_logo_redirect_loop.md`.
