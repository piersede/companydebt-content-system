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

## Deferred, small

**5. `cvl_all_in` is a misleading key name.** `data/statutory_fees.json` records
£4,000 to £5,000 under `cvl_all_in`, described as the fixed fee plus
disbursements. It excludes VAT. The page took that key at its word and published
"£4,000 to £5,000 all in", understating the real bill by roughly £800 until the
trust pass caught it. The page is fixed. The key name is not, and it will invite
the same error on the next page that reads it. Worth renaming to
`cvl_fee_plus_disbursements_ex_vat`, or adding an explicit `_excludes_vat: true`.

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
