> **SUPERSEDED AND WRONG.** The 183,000-character figure below is an artefact
> of two bugs in the measurement, not a property of the site. See
> `2026-08-09-custom-push-cleared.md`. Kept for the record of how the error was
> made: a non-greedy `<main>` match that truncated pages, and comparing the two
> sides with different normalisation rules.

# Custom push staging → production, 2026-08-09: BLOCKED, do not run

**Verdict: do not select `wp_posts` in a Custom push today.** Staging is behind
production on roughly a third of the site. The push would replace live's
`wp_posts` with staging's and destroy content that exists only on live.

The Gravity Forms exclusion in the agreed method protects the *leads*. It does
nothing to protect *content*, and content is what is at risk here.

## Evidence

Random sample of 70 of the 331 live URLs, comparing the rendered `<main>` region
of live against staging.

| Measure | Result |
|---|---|
| Pages sampled | 70 |
| Pages where staging is >300 chars shorter than live | 26 (37%) |
| Of those, shortfall fully explained by the referral-wording fix | **0** |
| Pages losing a heading anchor | 6 |
| Unexplained live-only text in the sample | 38,789 characters |
| Projected across 331 live pages | ~183,000 characters |

"Unexplained" means live-only lines that contain none of the referral wording
this batch changed, so they are not my edit. They are content live has and
staging does not.

Worst affected in the sample:

| Live-only chars | Page |
|---:|---|
| 3,472 | /case-studies/chinese-takeaway/ |
| 3,395 | /advice/writing-off-a-directors-loan-account/ |
| 2,537 | /liquidation/seek-insolvency-advice-before-missing-payments/ |
| 2,460 | /liquidation/what-happens-if-a-director-transfers-assets-before-insolvency/ |
| 2,284 | /professional-services-insolvency/ |
| 2,178 | /liquidation/when-should-a-director-stop-trading/ |
| 2,151 | /liquidation/insolvency-checklist/ |
| 2,083 | /liquidation/liquidators-powers-and-duties/ |

Worked example, `/advice/writing-off-a-directors-loan-account/`. Live carries an
FAQ section headed "Writing Off an Overdrawn Director's Loan Account: FAQs",
positioned before the next-step section. Staging has a differently worded FAQ
heading in a different position, and lacks 24 lines of live text including the
section 455 comparison and the misfeasance warning. That is editorial work that
exists only on production.

## What is NOT the problem

Two risks from the 2026-08-07 incident have since been fixed and are clean:

- **Heading anchors:** parity on 64 of 70 pages.
- **`cd-cta` blocks:** parity on 70 of 70. Zero pages lose a CTA.

So the CTA rollout is safe. The problem is different: live has newer editorial
content than both staging *and* `drafts/`.

## Why `drafts/` cannot simply be pushed instead

The repo is stale too. `push_damage_check.json`, written 2026-08-09 18:06 before
this batch, already showed 202 pages queued with live-only content. Staging was
behind live before this batch was pushed to it, so pushing the drafts did not
cause the gap and re-pushing them will not close it.

## The safe sequence

1. **Pull production → staging.** `python scripts/sync_staging_from_live.py --confirm`
   This overwrites staging with live, so the referral fix and the liquidation
   voice work currently on staging are lost from staging (they survive in
   `drafts/` and in git).
2. **Refresh `drafts/` from the new staging state**, so the repo matches live.
   Otherwise step 3 re-applies corrections to stale copies.
3. **Re-apply the referral sweep** to the refreshed content. It is fully
   scripted and reproducible: see commit d05d386.
4. **Re-apply the liquidation page work** from `drafts/7669_liquidation.html`.
5. Re-gate, push to staging, verify.
6. **Then** run the Custom push with the `gf_` tables and `wp_options` excluded.

## The alternative, if the referral fix is urgent

The referral wording is a regulated-status error and is currently live. If it
needs correcting before the sync can be scheduled, the surgical route is the
right one for a wording-only change, exactly as the deployment doc says: replace
only the affected sentences on each live page and leave the rest alone. That is
per-page, which is slower, but it is the only route that fixes the wording
without taking live-only content with it.

## Still true regardless

- Files half of the copy is destructive with no exclusions. Any media uploaded
  on production since the last clone is lost. Run `python scripts/audit_mu_plugins.py`
  before any files copy.
- Push `wp_posts` without the Yoast indexable table and SEO titles drift.
- After any push: purge caches, re-render a sample, run
  `python scripts/check_live_form_entries.py`, and confirm Gravity Forms is
  still active.
