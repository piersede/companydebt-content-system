# How many pages were edited without a recorded pipeline run

Assessment written 2026-08-18, and the changes it recommends applied the same day.
No page prose was touched.

## The short answer

**285 of 311 drafts have no usable evidence that the Bernstein pipeline was run
against the prose they now carry.** Those pages take 94% of the site's search
clicks and 84% of its impressions. Only 26 pages have any fresh evidence, and
only one has the tracked attestation.

**All 26 pages in the invented-reader-scene sweep had their prose edited with no
pipeline run recorded.** That question is now settled and closed in the
grandfather file.

The grandfathering has been narrowed, from 311 exempt pages to 173. The reason is
not that the removed pages are bad. It is that the grandfather file was built on
the wrong day, and froze the *result* of recent edits made outside the pipeline
instead of exempting pages that predate the rule.

**What a removed page needs is a check, not a rewrite.** That distinction is the
whole point of the change, and the tooling now supports it. See "Check, don't
rewrite" below.

## How this was measured

For every file in `drafts/`, the prose hash from `scripts/voice_metrics.py`
(`prose_sha`) was recomputed at each commit that touched the file, walking
backwards until the hash changed. That gives the commit where the *current*
prose was introduced. Edits to tables, comments and attributes do not count,
which is the same rule the gate itself uses. File timestamps were not used.

Each page was then cross-referenced against three sources:

1. `editorial-os/bernstein-state/<slug>/state.json` in the main working copy.
   This is not tracked in git, so it exists on one machine only. 19 pages have it.
2. `editorial-os/voice-audits/<slug>.json`, which is tracked. 17 pages have one.
3. `editorial-os/bernstein-runs/<slug>.json`, the attestation. 1 page has one.

A page counts as having evidence only when the record is **fresh**: the pipeline
run or voice pass has to be dated at or after the last prose change, or its
recorded prose hash has to match the prose sitting in the file today. A pipeline
run that the prose has since outrun is not evidence about the prose that is now
published.

Traffic is Search Console clicks and impressions for the 90 days to 16 August
2026, matched to drafts by the last part of the address. 289 of 311 drafts
matched.

**Both clicks and impressions are reported, and impressions matter more here.**
Ranking on clicks alone buries pages that rank and are seen but convert poorly in
search, and those are often the commercially important ones. The clearest example
is `company-strike-off-and-dissolution`: 51 clicks, but 34,105 impressions, the
highest in the corpus.

## What the numbers say

| | Pages | Clicks (90d) | Impressions (90d) |
|---|---:|---:|---:|
| Drafts in the corpus | 311 | 1,758 | 624,843 |
| Fresh evidence of a pipeline run or voice pass | 26 | 102 | 96,990 |
| **No fresh evidence** | **285** | **1,656** | **527,853** |
| Of those, prose edited on or after 1 July 2026 | 182 | 1,235 | — |
| Of those, prose edited on or after 1 August 2026 | 121 | 862 | — |
| Substantial rewrites (50+ prose words changed), no evidence | 86 | 321 | — |
| Near-total rewrites (300+ prose words changed), no evidence | 13 | 30 | — |

A second, smaller category matters as well. **Eight pages have a genuine local
pipeline record that the prose has since overtaken.** These are pages where the
work really was done and then quietly invalidated by a later correction:

| Page | Clicks | Impressions | Last recorded run | Prose changed since | Words changed |
|---|---:|---:|---|---|---:|
| `how-much-does-liquidation-cost` | 74 | 23,041 | (no dated stage) | 2026-07-15 | 70 |
| `cant-pay-vat` | 54 | 9,180 | (no dated stage) | 2026-07-30 | 2 |
| `uk-insolvency-statistics` | 48 | 12,298 | 2026-05-20 | 2026-08-14 | 27 |
| `pub-closures-in-the-uk` | 38 | 10,600 | 2026-07-22 | 2026-08-17 | 32 |
| `liquidation` | 22 | 8,800 | 2026-06-19 | 2026-08-09 | 91 |
| `members-voluntary-liquidation` | 10 | 12,337 | 2026-07-15 | 2026-07-30 | 16 |
| `winding-up-petitions` | 6 | 17,280 | (no dated stage) | 2026-07-29 | 496 |
| `creditors-voluntary-liquidation` | 4 | 7,000 | 2026-07-17 | 2026-08-12 | 263 |

`winding-up-petitions` is the one to look at first in that group: 17,280
impressions and a 496-word rewrite that landed after the recorded work.

## Pages with no search data are in scope, not out of it

14 published pages returned no Search Console rows at all in the period. They
cannot be ranked by traffic, and that is a gap in the data, **not evidence that
they do not matter**. They are in scope on the same terms as everything else.

| Page | Words | Prose last changed | Words changed |
|---|---:|---|---:|
| `find-a-liquidator-near-me` | 1,813 | 2026-04-30 | 122 |
| `joint-and-several-liability-for-unpaid-vat` | 849 | 2026-05-23 | 105 |
| `hmrc-follower-notice` | 1,021 | 2026-05-12 | 100 |
| `voluntary-liquidation` | 1,819 | 2026-08-09 | 43 |
| `garden-centres` | 1,684 | 2026-07-12 | 33 |
| `sector-specific-insolvency` | 2,873 | 2026-08-17 | 16 |
| `company-voluntary-arrangement-vs-administration-which-to-choose` | 880 | 2026-08-09 | 5 |
| `pre-pack-advantages-and-disadvantages` | 2,162 | 2026-08-09 | 4 |
| `business-debt-advice` | 1,674 | 2026-07-08 | 4 |
| `creditors-guides-to-insolvency-practitioners-fees` | 3,393 | 2026-07-15 | 3 |
| `care-homes` | 1,632 | 2026-07-12 | 3 |
| `bounce-back-loan-hub` | 50 | 2026-05-26 | first import |
| `sample-letters-hub` | 41 | 2026-05-26 | first import |
| `advice-hub` | 57 | 2026-05-26 | first import |

Three further unmatched entries are not editorial pages: `audit-13554` and
`audit-67370` are audit artefacts, and `hub-page-template` is scaffolding.

A correction worth recording, because it nearly distorted the whole ranking. The
first version of this assessment reported 63 unmatched pages and treated them as
zero-traffic. That was an error in the measurement, not a fact about the pages:
the traffic pull was capped at 1,000 addresses, so the long tail was cut off.
Re-pulling without the cap matched 289 of 311. Among the pages wrongly shown as
having no traffic were `company-ccj-mortgage-lender-criteria` (a 1,754-word
rewrite) and all 25 sector pages.

## What actually caused the prose to change

The edits are not 285 separate acts of drafting outside the pipeline. They
cluster into a small number of corpus-wide sweeps. This is the most useful thing
the audit found, because it changes what the fix should be.

| Date | Pages | Median words changed | The edit |
|---|---:|---:|---|
| 2026-08-09 | 52 | 5 | Correcting the regulated status of Company Debt across the corpus |
| 2026-05-23 | 39 | 99 | Merge resolving draft conflicts |
| 2026-05-12 | 36 | 117 | Full rewrite batch, described in the message as via Bernstein |
| 2026-08-17 | 24 | 14 | The invented-reader-scene sweep |
| 2026-05-20 | 16 | 1,161 | 17 rewrite batches plus heading demotions |
| 2026-07-12 | 14 | 33 | Rewriting all 25 sector bodies |
| 2026-07-14 | 10 | 1 | Single source of truth for statutory fees |
| 2026-08-14 | 5 | 643 | Fixing confirmed errors on the data pages |

Two things follow.

**The May 2026 batches are ambiguous, not damning.** Their commit messages say
the work went through Bernstein. The pipeline state was gitignored and is long
gone, so it cannot be confirmed either way. These are best read as "the record
was never durable", not "the rule was skipped".

**The recent sweeps are the real gap.** The August 2026 edits were correction
passes: fixing a regulated-status claim, fixing fee figures, removing invented
reader scenes. They were correct edits, made for good reasons. But the standing
rule is that a correction pass flattens voice and the page must be re-humanised
afterwards, and none of that was recorded. Note the median change size: five
words, fourteen words, one word. These are not rewrites.

## The 26 pages: answered

The grandfather file flagged commit `1429dc5` as a known gap and asked whether
any pipeline run happened for those pages. It did not.

- **0 of 26** have a pipeline run recorded at or after the prose change.
- **1 of 26** has any local pipeline state at all, and that record predates the
  edit by nearly a month.
- **3 of 26** have a tracked voice audit; only 2 of those match the current prose.
  Both were recorded as part of the clean-up in that same commit, not as a
  pipeline run.
- The edits themselves were small. The median is 14 prose words. The largest is
  75 words, leaving aside `closing-a-limited-company`, which has since been
  redrafted and properly attested.

So the honest description is: 24 pages carry a small, correct, voice-affecting
edit that nobody put back through the pipeline, and the grandfather file then
made that state permanent.

## The flaw in the grandfathering

The grandfather file was built on 2026-08-17 by recording the prose hash of
every page as it stood **that day**. Its stated purpose is to exempt pages that
predate the requirement.

That is not what it did. It exempted whatever the prose looked like on the day it
was built, including edits made hours earlier. The invented-reader-scene sweep
landed at 09:21 on 2026-08-17. The grandfather file captured the post-edit hash
of those pages the same day and blessed it permanently. The same applies to the
52 pages from the 9 August regulated-status sweep, and to everything else edited
in August.

The result was that the check could not fire on the exact failure it was built to
catch, until somebody edited one of those pages again.

## Check, don't rewrite

Before narrowing anything, the tooling had a gap that would have made the
narrowing harmful.

`bernstein_attest.py` could record only one thing: that the pipeline stages were
run. There was no way to record "I read this page against the stage criteria and
it holds up". So removing a page's exemption forced the expensive option, because
the cheap and usually correct one could not be written down. Given that the
median edit that cost a page its exemption was five words, that would have meant
a great deal of redrafting to reach the conclusion "it was fine" — and a check
that expensive is a check people route around.

So the attestation now records two kinds of thing, and says which:

- **`pipeline-run`** — the stages were run and the page was written or rewritten
  through them. What a new page or a real redraft produces.
- **`verification`** — somebody read an existing page against the stage criteria
  and fixed only what failed. No redraft.

```bash
python scripts/bernstein_attest.py --slug <slug> --verify --by <model> --checked review,humanise,gate --outcome pass --notes "..."
```

`--outcome` is `pass` if the page held up as written, or `fixed` if things were
corrected, and `--notes` is then required so the record says what was wrong. Both
kinds are hashed against the prose in the same way, so a later edit invalidates
either. The freshness discipline does not soften; only the cost of satisfying it
honestly comes down.

A verification is a weaker claim than a pipeline run and is stored as a distinct
kind, so the two can never be read as the same thing. `article_audit.py` check 34
accepts either, and its detail line reports which it saw.

## What was changed

1. **`scripts/bernstein_attest.py`** — added the `--verify` mode described above.
   It refuses to record unless `review`, `humanise` and `gate` were all checked,
   refuses without `--by`, and refuses an outcome of `fixed` with no notes.

2. **`scripts/article_audit.py`** — check 34 now accepts a verification record as
   well as a pipeline-run record, and names which one it found.

3. **`editorial-os/bernstein-runs/_baseline.json`** — narrowed from 311 exempt
   pages to 173. Removed: 134 pages whose prose last changed on or after
   2026-08-01, plus 4 whose real pipeline record a later edit had overtaken. The
   file now records why, and what a removed page is actually being asked for.

4. **The known-gap note** — replaced with the finding about the 26 pages, so the
   question is not re-asked.

5. **`--build-baseline` guard** — the mechanism failed because it recorded the
   current hash with no regard for how recently that hash changed. It now refuses
   to grandfather any page whose prose changed within the last 30 days, and lists
   those pages instead. `--baseline-recent-days` changes the window.

### Why the cut is at 1 August 2026

**It is nearly free.** There is no continuous integration in this repository, and
nothing runs `article_audit.py` across the corpus. The gate runs one page at a
time, on demand. Removing an exemption breaks nothing today. It means: the next
time anyone touches one of these pages, they check it first. That costs nothing
until the moment it is useful.

**It separates the two honest categories.** Pages last edited in May 2026 have
commit messages saying they went through Bernstein. The evidence was lost because
it was gitignored, not because the rule was skipped. Grandfathering them is what
grandfathering is for. Pages edited in August 2026 were edited after the rule was
well established, with nothing recorded. Those are not the same case.

**A wider cut is not worth it.** A cut at 1 July would remove roughly 60 more
pages, mostly the ambiguous May and early-July batches. That buys little, and
makes the file read as a punishment list rather than a record.

## Where to start the actual work

Narrowing the exemption does not schedule the work. If pages are to be checked,
reach says start here. Ranked by impressions, since that is the better measure of
what is at stake:

| Page | Clicks | Impressions | Prose last changed | Words changed |
|---|---:|---:|---|---:|
| `company-strike-off-and-dissolution` | 51 | 34,105 | 2026-07-14 | 5 |
| `how-much-does-liquidation-cost` | 74 | 23,041 | 2026-07-15 | 70 |
| `company-voluntary-arrangement` | 4 | 17,606 | 2026-08-09 | 6 |
| `winding-up-petitions` | 6 | 17,280 | 2026-07-29 | 496 |
| `company-administration` | 1 | 14,992 | 2026-08-08 | 1 |
| `what-is-an-individual-voluntary-arrangement` | 2 | 14,196 | 2026-05-20 | 1,250 |
| `members-voluntary-liquidation` | 10 | 12,337 | 2026-07-30 | 16 |
| `uk-insolvency-statistics` | 48 | 12,298 | 2026-08-14 | 27 |
| `hmrc-tax-investigations` | 11 | 12,022 | 2026-08-17 | 6 |
| `shareholders-liable-company-debts` | 67 | 11,553 | 2026-08-17 | 19 |

Two of those deserve singling out, because they are the cases where a check is
most likely to find something real: `winding-up-petitions` (496 words rewritten,
17,280 impressions) and `what-is-an-individual-voluntary-arrangement` (1,250
words rewritten, 14,196 impressions).

Most of the rest changed by a handful of words. Those should be quick, and most
will come out as `--outcome pass`. That is a fine result. The point of the check
is to know, not to find fault.

A full ranked list of the top 60 is in the appendix below.

## Appendix: top 60 by risk

Risk here is search reach — clicks and impressions combined — weighted up for a
larger prose change and a more recent one. It is a sorting aid, not a score with
a meaning of its own. Pages with no search data are excluded from this table and
listed in their own section above; they are in scope regardless of their absence
here.

| Page | Clicks | Impressions | Prose last changed | Words changed |
|---|---:|---:|---|---:|
| `how-much-does-liquidation-cost` | 74 | 23,041 | 2026-07-15 | 70 |
| `personal-guarantee-insurance` | 77 | 10,692 | 2026-08-09 | 5 |
| `shareholders-liable-company-debts` | 67 | 11,553 | 2026-08-17 | 19 |
| `list-of-liquidation-documents` | 68 | 3,644 | 2026-08-09 | 5 |
| `uk-insolvency-statistics` | 48 | 12,298 | 2026-08-14 | 27 |
| `personal-liability-spouses-business-debts` | 44 | 2,890 | 2026-08-17 | 11 |
| `company-strike-off-and-dissolution` | 51 | 34,105 | 2026-07-14 | 5 |
| `pub-closures-in-the-uk` | 38 | 10,600 | 2026-08-17 | 32 |
| `cant-pay-vat` | 54 | 9,196 | 2026-07-30 | 2 |
| `ccj-when-going-insolvent` | 36 | 1,309 | 2026-08-09 | 5 |
| `what-happens-if-a-director-resigns-before-liquidation` | 34 | 1,123 | 2026-08-09 | 5 |
| `personally-liabilty-of-company-secretary` | 33 | 2,018 | 2026-08-09 | 4 |
| `can-personal-assets-of-directors-be-seized-from-a-ltd-company` | 29 | 2,014 | 2026-08-09 | 8 |
| `statement-of-affairs` | 27 | 5,059 | 2026-08-08 | 7 |
| `winding-up-petitions` | 6 | 17,280 | 2026-07-29 | 496 |
| `redundancy-payments-for-directors-in-an-mvl` | 28 | 920 | 2026-08-09 | 11 |
| `cease-trading` | 32 | 11,114 | 2026-07-08 | 1 |
| `what-happens-to-employees` | 19 | 4,511 | 2026-08-08 | 1 |
| `paying-staff-but-not-hmrc-before-liquidation` | 20 | 1,181 | 2026-08-09 | 7 |
| `request-a-reduced-monthly-payment` | 27 | 4,882 | 2026-05-23 | 202 |
| `can-director-criminal-record` | 18 | 2,866 | 2026-08-09 | 5 |
| `cease-trading-template` | 18 | 1,683 | 2026-08-17 | 13 |
| `company-vehicles-and-equipment-in-liquidation` | 54 | 2,774 | 2026-05-12 | first import |
| `liquidation-deadlines-and-time-limits` | 17 | 2,241 | 2026-08-17 | 8 |
| `hmrc-tax-investigations` | 11 | 12,022 | 2026-08-17 | 6 |
| `how-to-legally-take-money-out-of-a-limited-company` | 14 | 2,823 | 2026-08-09 | 10 |
| `what-are-phoenix-companies` | 21 | 3,936 | 2026-07-15 | 1 |
| `intellectual-property-and-trading-assets-in-liquidation` | 14 | 779 | 2026-05-20 | 1510 |
| `liquidating-a-group-company-or-holding-company-in-the-uk` | 14 | 469 | 2026-08-09 | 5 |
| `can-directors-pay-themselves-before-liquidation` | 10 | 430 | 2026-07-14 | 101 |
| `can-i-be-sued-after-my-company-is-dissolved` | 13 | 879 | 2026-08-17 | 10 |
| `which-creditors-get-paid-first` | 12 | 2,684 | 2026-08-09 | 7 |
| `construction-insolvency-statistics` | 6 | 1,054 | 2026-08-07 | 289 |
| `company-voluntary-arrangement` | 4 | 17,606 | 2026-08-09 | 6 |
| `making-employees-redundant-cva` | 18 | 1,672 | 2026-05-20 | 167 |
| `can-directors-go-to-prison-for-company-debt` | 12 | 616 | 2026-08-09 | 5 |
| `notice-of-intention-to-appoint-administrators` | 11 | 2,172 | 2026-08-09 | 6 |
| `when-a-cva-fails` | 11 | 1,605 | 2026-08-17 | 18 |
| `can-i-liquidate-a-dormant-company` | 8 | 980 | 2026-07-15 | 114 |
| `members-voluntary-liquidation` | 10 | 12,337 | 2026-07-30 | 16 |
| `losing-house-if-company-goes-bust` | 15 | 2,174 | 2026-07-08 | 28 |
| `tell-debt-collector-to-stop-contacting-you` | 10 | 888 | 2026-08-09 | 17 |
| `lpa-receivership` | 14 | 3,328 | 2026-05-12 | 138 |
| `what-happens-if-i-default` | 14 | 2,840 | 2026-05-23 | 164 |
| `frozen-bank-account` | 26 | 9,670 | 2026-05-12 | first import |
| `vs-administrative-receivership` | 9 | 1,886 | 2026-08-09 | 5 |
| `time-to-pay-hmrc` | 7 | 5,257 | 2026-08-09 | 5 |
| `cant-afford-to-liquidate` | 13 | 1,656 | 2026-07-15 | 6 |
| `what-is-an-individual-voluntary-arrangement` | 2 | 14,196 | 2026-05-20 | 1250 |
| `liquidating-a-charity-or-non-profit` | 13 | 1,006 | 2026-07-15 | 6 |
| `company-administration` | 1 | 14,992 | 2026-08-08 | 1 |
| `insolvent-company-owes-me-money` | 7 | 2,862 | 2026-08-17 | 5 |
| `cant-pay-staff-wages` | 11 | 2,778 | 2026-05-23 | 106 |
| `dissolving-a-company-with-bounce-back-loan` | 11 | 1,767 | 2026-07-14 | 1 |
| `unenforceable-personal-guarantee` | 10 | 3,163 | 2026-05-23 | 288 |
| `overdrawn-directors-loan-accounts` | 6 | 3,387 | 2026-08-08 | 1 |
| `cant-pay-paye` | 6 | 3,152 | 2026-08-09 | 5 |
| `hmrcs-ir35-investigations-different` | 7 | 1,144 | 2026-08-09 | 5 |
| `how-to-challenge-a-liquidators-decisions-or-fees` | 22 | 1,173 | 2026-05-12 | first import |
| `transport-haulage-insolvency` | 7 | 746 | 2026-08-17 | 16 |
