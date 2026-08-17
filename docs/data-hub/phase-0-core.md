# Phase 0 Core: what exists, and how to run it on 18 August

**Status:** spine built and passing. Not yet wired into page generation.
**Built:** 15 August 2026

Phase 0 Core has one job: make one release object the source of truth, so the hub,
the dashboard and every sector page cannot disagree with each other or with
themselves.

## What is built

| Piece | File | State |
|---|---|---|
| Canonical taxonomy | `scripts/intelligence/taxonomy.py` | 22 sectors, validated |
| Metric engine | `scripts/intelligence/metrics.py` | deterministic, one definition each |
| Release object + pointer | `scripts/intelligence/build_release.py` | June 2026 built and promoted |
| Revision detection | `scripts/intelligence/revisions.py` | ready, needs a second release |
| Consistency assertions | `scripts/datahub/check_derived_values.py` | 20 sectors passing |
| Page reproduction test | `scripts/intelligence/verify_against_pages.py` | 70 of 70 figures |

## The success criterion is met

> Can the system reproduce every statistic currently shown on the existing pages?

Yes, for the sector layer. All 70 headline figures across 21 sector pages are
derivable from the release object: year to date, prior year to date and rolling
12 months for the 20 trade pages, and the full annual series for construction.

Two page shapes exist and the test knows the difference. The trade pages lead on
year to date and rolling; the whole-section pages publish an annual series and
never show a year-to-date figure. Testing the second shape for the first reports a
false failure, which it did on the first run.

## What is NOT built

- Pages still generate their own figures. Nothing reads from the release object yet. That is the next step and it is the one that actually removes the duplication.
- The national headline layer is captured but not verified against the dashboard.
- No importer from the raw workbook; the release is assembled from the already-parsed JSON. Fine for now, wrong long term.
- Bulk-event handling. The record-level file has the flag; this release model does not use it yet.

## Running it on 18 August

The July figures publish at 09:30. Run the normal refresh as usual. Alongside it,
in parallel and publishing nothing:

```bash
# 1. after the July data is parsed as normal
python scripts/intelligence/taxonomy.py --validate
python scripts/intelligence/build_release.py --month 2026-07

# 2. what did the source restate? This is the question the manual process cannot answer.
python scripts/intelligence/revisions.py --from 2026-06 --to 2026-07

# 3. do the regenerated pages still agree with the release object?
python scripts/intelligence/verify_against_pages.py --month 2026-07 --verbose
python scripts/datahub/check_derived_values.py

# 4. only if all of the above are clean
python scripts/intelligence/build_release.py --month 2026-07 --promote
```

### What to record

The point of the parallel run is a comparison, so write down:

1. Figures the automated path produced that the manual path missed, and the reverse.
2. Every stale hand-written value `check_derived_values.py` catches.
3. Anything a human spotted that no check caught. **This is the most valuable number.** It is the honest measure of how much of the QA framework is still missing.
4. How long each path took.

Item 3 decides whether Phase 0 proper is worth funding. If the checks catch
everything a careful human catches, the model works. If humans keep finding things
the code misses, the model needs more before anyone builds on it.

## Design notes worth keeping

**The pointer is the safety mechanism.** Building a release changes nothing. Only
`--promote` makes it live, and every page is meant to move together. In August the
hub sat on May while the dashboard was on June for weeks, and nothing detected it.

**The vintage hash matters more than it looks.** The source revises history, so a
published figure is only reproducible if you know which vintage produced it. A
chart regenerated from a later vintage will not match a screenshot taken earlier,
and that is not an error.

**The taxonomy holds facts, not prose.** Editorial copy stays in the builders.
Identity, SIC mapping, parent and tier live in one place, because the August
failures were all cases where a fact lived inside a sentence.
