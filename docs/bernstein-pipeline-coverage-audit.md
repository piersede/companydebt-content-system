# How many pages were edited without a recorded pipeline run

Assessment written 2026-08-18. No pages were changed to produce it.

## The short answer

**285 of 311 drafts have no usable evidence that the Bernstein pipeline was run
against the prose they now carry.** Those pages take 94% of the site's search
traffic. Only 26 pages have any fresh evidence, and only one has the new tracked
attestation.

**All 26 pages in the invented-reader-scene sweep had their prose edited with no
pipeline run recorded. That is now settled, and the "worth checking" note in the
grandfather file can be closed.**

The grandfathering should be narrowed. The reason is not that 285 pages are bad.
It is that the grandfather file was built on the wrong day, and it froze the
*result* of recent unpipelined edits rather than the state of pages that predate
the rule.

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
3. `editorial-os/bernstein-runs/<slug>.json`, the new attestation. 1 page has one.

A page counts as having evidence only when the record is **fresh**: the pipeline
run or voice pass has to be dated at or after the last prose change, or its
recorded prose hash has to match the prose sitting in the file today. A pipeline
run that the prose has since outrun is not evidence about the prose that is now
published.

Traffic is Search Console clicks and impressions for the 90 days to 16 August
2026, matched to drafts by the last part of the address. 248 of 311 drafts
matched; the rest have no search traffic to report.

## What the numbers say

| | Pages | Clicks (90d) |
|---|---:|---:|
| Drafts in the corpus | 311 | 1,748 |
| Fresh evidence of a pipeline run or voice pass | 26 | 102 |
| **No fresh evidence** | **285** | **1,646** |
| Of those, prose edited on or after 1 July 2026 | 182 | 1,235 |
| Of those, prose edited on or after 1 August 2026 | 121 | 862 |
| Substantial rewrites (50+ prose words changed), no evidence | 86 | 321 |
| Near-total rewrites (300+ prose words changed), no evidence | 13 | 30 |

A second, smaller category matters as well. **Eight pages have a genuine local
pipeline record that the prose has since overtaken.** These are pages where the
work really was done and then quietly invalidated by a later correction:

| Page | Clicks | Last recorded run | Prose changed since | Words changed |
|---|---:|---|---|---:|
| `how-much-does-liquidation-cost` | 74 | (no dated stage) | 2026-07-15 | 70 |
| `cant-pay-vat` | 54 | (no dated stage) | 2026-07-30 | 2 |
| `uk-insolvency-statistics` | 47 | 2026-05-20 | 2026-08-14 | 27 |
| `pub-closures-in-the-uk` | 37 | 2026-07-22 | 2026-08-17 | 32 |
| `liquidation` | 22 | 2026-06-19 | 2026-08-09 | 91 |
| `members-voluntary-liquidation` | 10 | 2026-07-15 | 2026-07-30 | 16 |
| `winding-up-petitions` | 6 | (no dated stage) | 2026-07-29 | 496 |
| `creditors-voluntary-liquidation` | 4 | 2026-07-17 | 2026-08-12 | 263 |

## What actually caused the prose to change

The edits are not 285 separate acts of drafting outside the pipeline. They
cluster into a small number of corpus-wide sweeps. This is the most useful thing
the audit found, because it changes what the fix should be.

| Date | Pages | Clicks | Median words changed | The edit |
|---|---:|---:|---:|---|
| 2026-08-09 | 52 | 427 | 5 | Correcting the regulated status of Company Debt across the corpus |
| 2026-05-23 | 39 | 117 | 99 | Merge resolving draft conflicts |
| 2026-05-12 | 36 | 212 | 117 | Full rewrite batch, described in the message as via Bernstein |
| 2026-08-17 | 24 | 246 | 14 | The invented-reader-scene sweep |
| 2026-05-20 | 16 | 54 | 1,161 | 17 rewrite batches plus heading demotions |
| 2026-07-12 | 14 | 9 | 33 | Rewriting all 25 sector bodies |
| 2026-07-14 | 10 | 84 | 1 | Single source of truth for statutory fees |
| 2026-08-14 | 5 | 50 | 643 | Fixing confirmed errors on the data pages |

Two things follow.

**The May 2026 batches are ambiguous, not damning.** Their commit messages say
the work went through Bernstein. The pipeline state was gitignored and is long
gone, so it cannot be confirmed either way. These are best read as "the record
was never durable", not "the rule was skipped".

**The recent sweeps are the real gap.** The August 2026 edits were correction
passes: fixing a regulated-status claim, fixing fee figures, removing invented
reader scenes. They were correct edits, made for good reasons. But the standing
rule is that a correction pass flattens voice and the page must be re-humanised
afterwards, and none of that was recorded. 121 pages carry August correction
edits with nothing behind them.

## The 26 pages: answered

The grandfather file flags commit `1429dc5` as a known gap and asks whether any
pipeline run happened for those pages. It did not.

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

That is not what it does. It exempts whatever the prose looked like on the day it
was built, including edits made hours earlier. The invented-reader-scene sweep
landed at 09:21 on 2026-08-17. The grandfather file captured the post-edit hash
of those pages the same day and blessed it permanently. The same applies to the
52 pages from the 9 August regulated-status sweep, and to everything else edited
in August.

The result is that the check cannot fire on the exact failure it was built to
catch, until somebody edits one of those pages again. 121 pages had prose changed
outside the pipeline in the four weeks before the file was written. Every one of
them was granted a permanent pass for that change.

## Recommendation

**Yes, narrow it. Cut the exemption at 1 August 2026.**

Remove from `editorial-os/bernstein-runs/_baseline.json` every page whose prose
last changed on or after 2026-08-01, and record why. That removes 121 of the 311
entries and leaves 190.

Three reasons this is the right cut, rather than a wider or a narrower one.

**It is nearly free.** There is no continuous integration in this repository, and
nothing runs `article_audit.py` across the corpus. The gate runs one page at a
time, on demand, when somebody works on that page. Removing an exemption
therefore breaks nothing today. It means one thing: the next time anyone touches
one of these pages, they must run the pipeline first. That is precisely the
wanted behaviour, and it costs nothing until the moment it is useful.

**It separates the two honest categories.** Pages last edited in May 2026 have
commit messages saying they went through Bernstein. The evidence was lost because
it was gitignored, not because the rule was skipped. Grandfathering them is what
grandfathering is for. Pages edited in August 2026 were edited after the rule was
well established, with nothing recorded. Those are not the same case, and they
should not get the same treatment.

**A wider cut is not worth it.** A cut at 1 July would remove 182 entries instead
of 121. The extra 61 pages are mostly the ambiguous May and early-July batches.
That buys little. It also makes the file look like a punishment list rather than
a record.

Three supporting changes are worth making at the same time.

1. **Close the known-gap note.** Replace the "worth checking" text with the
   finding: zero of the 26 had a run, so the 24 still exempt are dropped under
   this cut. An open question invites somebody to re-ask it.

2. **Re-baseline the eight overtaken pages properly.** These have real pipeline
   work behind them that a later small correction invalidated. They deserve a
   re-run rather than an exemption. `how-much-does-liquidation-cost` at 74 clicks
   is the highest-traffic page in the whole assessment.

3. **Make future baselines refuse to bless a same-day edit.** The mechanism
   failed because `--build-baseline` records the current hash with no regard for
   how recently that hash changed. A baseline build should skip any page whose
   prose changed in the previous month, or at least list those pages separately.

## Where to start the actual work

The grandfathering question is separate from the question of which pages to
re-run. If pages go back through the pipeline, traffic says start here. These are
the highest-traffic pages with no fresh evidence:

| Page | Clicks (90d) | Prose last changed | Words changed |
|---|---:|---|---:|
| `personal-guarantee-insurance` | 77 | 2026-08-09 | 5 |
| `how-much-does-liquidation-cost` | 74 | 2026-07-15 | 70 |
| `list-of-liquidation-documents` | 68 | 2026-08-09 | 5 |
| `shareholders-liable-company-debts` | 66 | 2026-08-17 | 19 |
| `cant-pay-vat` | 54 | 2026-07-30 | 2 |
| `company-vehicles-and-equipment-in-liquidation` | 53 | 2026-05-12 | first import |
| `company-strike-off-and-dissolution` | 51 | 2026-07-14 | 5 |
| `uk-insolvency-statistics` | 47 | 2026-08-14 | 27 |
| `personal-liability-spouses-business-debts` | 44 | 2026-08-17 | 11 |
| `pub-closures-in-the-uk` | 37 | 2026-08-17 | 32 |

Note how small most of those edits are. That is the point of the standing rule
about re-humanising after a correction. Five words changed by a fact-fix can
still leave a sentence that no longer sounds like the person who wrote it, and
nothing mechanical will catch that.

A full ranked list of the top 60 by risk is in the appendix below.

## Appendix: top 60 by risk

Risk here is clicks, weighted up for a larger prose change and for a more recent
one. It is a sorting aid, not a score with a meaning of its own.

| Page | Clicks (90d) | Prose last changed | Words changed | Edit that did it |
|---|---:|---|---:|---|
| `how-much-does-liquidation-cost` | 74 | 2026-07-15 | 70 | fix(fees): CVL and MVL repriced to flat Â£3,500 + VA |
| `personal-guarantee-insurance` | 77 | 2026-08-09 | 5 | Correct Company Debt's regulated status across the c |
| `list-of-liquidation-documents` | 68 | 2026-08-09 | 5 | Correct Company Debt's regulated status across the c |
| `shareholders-liable-company-debts` | 66 | 2026-08-17 | 19 | Twenty-six pages: drop the invented reader scene, an |
| `uk-insolvency-statistics` | 47 | 2026-08-14 | 27 | Fix the publication audit's confirmed errors across  |
| `personal-liability-spouses-business-debts` | 44 | 2026-08-17 | 11 | Twenty-six pages: drop the invented reader scene, an |
| `pub-closures-in-the-uk` | 37 | 2026-08-17 | 32 | Twenty-six pages: drop the invented reader scene, an |
| `ccj-when-going-insolvent` | 36 | 2026-08-09 | 5 | Correct Company Debt's regulated status across the c |
| `cant-pay-vat` | 54 | 2026-07-30 | 2 | fix(cant-pay-vat): Related Guides as final H2 to sat |
| `company-strike-off-and-dissolution` | 51 | 2026-07-14 | 5 | fix(fees): single source of truth for statutory fees |
| `personally-liabilty-of-company-secretary` | 33 | 2026-08-09 | 4 | Correct Company Debt's regulated status across the c |
| `what-happens-if-a-director-resigns-before-liquidation` | 33 | 2026-08-09 | 5 | Correct Company Debt's regulated status across the c |
| `can-personal-assets-of-directors-be-seized-from-a-ltd-company` | 28 | 2026-08-09 | 8 | Correct Company Debt's regulated status across the c |
| `redundancy-payments-for-directors-in-an-mvl` | 28 | 2026-08-09 | 11 | Teach the fee checker the drift patterns it was miss |
| `statement-of-affairs` | 26 | 2026-08-08 | 7 | Correct the stale law and fees on the liquidation cl |
| `cease-trading` | 32 | 2026-07-08 | 1 | fix(links): resolve internal-link/anchor audit findi |
| `paying-staff-but-not-hmrc-before-liquidation` | 20 | 2026-08-09 | 7 | Correct Company Debt's regulated status across the c |
| `what-happens-to-employees` | 19 | 2026-08-08 | 1 | Pull back the overreach on the liquidation page |
| `cease-trading-template` | 18 | 2026-08-17 | 13 | Twenty-six pages: drop the invented reader scene, an |
| `can-director-criminal-record` | 18 | 2026-08-09 | 5 | Correct Company Debt's regulated status across the c |
| `request-a-reduced-monthly-payment` | 27 | 2026-05-23 | 202 | merge: resolve draft conflicts â€” accept remote Ber |
| `company-vehicles-and-equipment-in-liquidation` | 53 | 2026-05-12 | first import | Drafts: full rewrite batch via Bernstein wp_post mod |
| `liquidation-deadlines-and-time-limits` | 17 | 2026-08-17 | 8 | Twenty-six pages: drop the invented reader scene, an |
| `how-to-legally-take-money-out-of-a-limited-company` | 14 | 2026-08-09 | 10 | Correct stale tax rates and fees across the liquidat |
| `liquidating-a-group-company-or-holding-company-in-the-uk` | 14 | 2026-08-09 | 5 | Correct Company Debt's regulated status across the c |
| `what-are-phoenix-companies` | 21 | 2026-07-15 | 1 | fix(mvl): correct MVL/BADR/fee facts across cluster, |
| `intellectual-property-and-trading-assets-in-liquidation` | 14 | 2026-05-20 | 1510 | Drafts: 17 Bernstein wp_post batches + 9 legacy H2 d |
| `can-directors-pay-themselves-before-liquidation` | 10 | 2026-07-14 | 101 | fix(fees): single source of truth for statutory fees |
| `can-i-be-sued-after-my-company-is-dissolved` | 13 | 2026-08-17 | 10 | Twenty-six pages: drop the invented reader scene, an |
| `can-directors-go-to-prison-for-company-debt` | 12 | 2026-08-09 | 5 | Correct Company Debt's regulated status across the c |
| `construction-insolvency-statistics` | 6 | 2026-08-07 | 289 | Fix task-entry crash on Windows and chart/prose span |
| `winding-up-petitions` | 6 | 2026-07-29 | 496 | Plain-English pass: explain the vocabulary before us |
| `making-employees-redundant-cva` | 18 | 2026-05-20 | 167 | Drafts: 17 Bernstein wp_post batches + 9 legacy H2 d |
| `hmrc-tax-investigations` | 11 | 2026-08-17 | 6 | Twenty-six pages: drop the invented reader scene, an |
| `when-a-cva-fails` | 11 | 2026-08-17 | 18 | Twenty-six pages: drop the invented reader scene, an |
| `notice-of-intention-to-appoint-administrators` | 11 | 2026-08-09 | 6 | Correct Company Debt's regulated status across the c |
| `which-creditors-get-paid-first` | 11 | 2026-08-09 | 7 | Finish the licensed-practice sweep beyond drafts |
| `can-i-liquidate-a-dormant-company` | 8 | 2026-07-15 | 114 | fix(mvl): correct MVL/BADR/fee facts across cluster, |
| `tell-debt-collector-to-stop-contacting-you` | 10 | 2026-08-09 | 17 | Finish the licensed-practice sweep beyond drafts |
| `losing-house-if-company-goes-bust` | 15 | 2026-07-08 | 28 | fix(links): resolve internal-link/anchor audit findi |
| `lpa-receivership` | 14 | 2026-05-12 | 138 | Drafts: full rewrite batch via Bernstein wp_post mod |
| `vs-administrative-receivership` | 9 | 2026-08-09 | 5 | Correct Company Debt's regulated status across the c |
| `cant-afford-to-liquidate` | 13 | 2026-07-15 | 6 | fix(fees): CVL and MVL repriced to flat Â£3,500 + VA |
| `liquidating-a-charity-or-non-profit` | 13 | 2026-07-15 | 6 | fix(mvl): correct MVL/BADR/fee facts across cluster, |
| `what-happens-if-i-default` | 13 | 2026-05-23 | 164 | merge: resolve draft conflicts â€” accept remote Ber |
| `frozen-bank-account` | 26 | 2026-05-12 | first import | Drafts: full rewrite batch via Bernstein wp_post mod |
| `dissolving-a-company-with-bounce-back-loan` | 11 | 2026-07-14 | 1 | fix(fees): single source of truth for statutory fees |
| `cant-pay-staff-wages` | 11 | 2026-05-23 | 106 | merge: resolve draft conflicts â€” accept remote Ber |
| `how-to-challenge-a-liquidators-decisions-or-fees` | 22 | 2026-05-12 | first import | Drafts: full rewrite batch via Bernstein wp_post mod |
| `insolvent-company-owes-me-money` | 7 | 2026-08-17 | 5 | Twenty-six pages: drop the invented reader scene, an |
| `transport-haulage-insolvency` | 7 | 2026-08-17 | 16 | Twenty-six pages: drop the invented reader scene, an |
| `hmrcs-ir35-investigations-different` | 7 | 2026-08-09 | 5 | Correct Company Debt's regulated status across the c |
| `time-to-pay-hmrc` | 7 | 2026-08-09 | 5 | Correct Company Debt's regulated status across the c |
| `members-voluntary-liquidation` | 10 | 2026-07-30 | 16 | Fix remaining 11 body-prose citation errors across 7 |
| `unenforceable-personal-guarantee` | 10 | 2026-05-23 | 288 | merge: resolve draft conflicts â€” accept remote Ber |
| `business-bank-account-in-liquidation` | 6 | 2026-08-17 | 14 | Twenty-six pages: drop the invented reader scene, an |
| `administration-statistics` | 2 | 2026-08-14 | 682 | Fix the publication audit's confirmed errors across  |
| `cant-pay-paye` | 6 | 2026-08-09 | 5 | Correct Company Debt's regulated status across the c |
| `overdrawn-directors-loan-accounts` | 6 | 2026-08-08 | 1 | Pull back the overreach on the liquidation page |
| `i-cannot-afford-to-repay-my-debt` | 9 | 2026-05-12 | 243 | Drafts: full rewrite batch via Bernstein wp_post mod |
