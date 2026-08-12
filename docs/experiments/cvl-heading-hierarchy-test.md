# CVL page: heading-hierarchy test

**Page:** https://www.companydebt.com/liquidation/creditors-voluntary-liquidation/ (WP 7674)
**Change made:** 12 August 2026 (staging)
**Went live:** _not yet_
**Decision point:** 90 days after the change reaches production

---

## The hypothesis

The CVL page will not rank for its own head term (position ~26 to 28) while three
sibling pages in the same section rank 5.9, 6.5 and 14.7.

The CVL page was the only page in the section not built to the section's own template.
Three of four siblings open with a summary H2 ("... at a Glance") and then answer their
own head term directly ("What Is ...?"). The CVL page had neither. It reached the process
at H2 #3 and led with a decision framing instead of a definition.

The definition was present in the copy. It was not structurally primary.

Confidence is moderate. Search data cannot prove cause. This is the only difference that
tracks the outcome across four controlled internal comparisons and matches the structure
of what ranks on this SERP.

Everything else was ruled out first: site-wide quality collapse, cannibalisation, link
decay, lost redirect equity, weak internal anchoring, click-through, entity evidence,
time since rewrite, thinness, title, schema and technical faults. The page held position
7 to 9 until October 2023, so it is a demoted page, not one Google never trusted.

## What changed

Top-level H2 order only.

| Before | After |
| ------ | ----- |
| 1. Is CVL the Right Route for Your Company? | 1. Creditors' Voluntary Liquidation at a Glance |
| 2. When Directors Should Consider a CVL | 2. What Is a Creditors' Voluntary Liquidation? |
| 3. How the CVL Process Works | 3. How Does a Creditors' Voluntary Liquidation Work? |
| 4. What Directors Need to Prepare | 4. Is CVL the Right Route for Your Company? |
| 5+ unchanged | 5. When Directors Should Consider a CVL |
| | 6+ unchanged |

Detail:

- The existing key-facts panel already carried the summary content, but its title was a
  styled paragraph, not a heading. A real H2 (`id="cvl-at-a-glance"`) now sits above it,
  and the panel's own bar was shortened to "Key Facts" to avoid saying it twice.
- "What Is a Creditors' Voluntary Liquidation?" (`id="what-is-a-cvl"`) is genuinely new:
  five paragraphs at the legal-concept level, about 250 words.
- The process section was retitled and moved up. Its anchor id (`cvl-process`) was kept,
  so existing links to it still work.
- Two intro paragraphs (HMRC arrears / Time to Pay, and wrongful trading / timing) were
  moved verbatim out of the opening into "Is CVL the Right Route". Nothing was rewritten.

## Second change, same date: Related Guides

Made 12 August 2026, on Piers's instruction, after the heading work. It is a second
variable on the same date. Both changes go live together, so the test cannot separate
their effects. Judge them as one intervention.

Removed:

- Members' Voluntary Liquidation. It closes a *solvent* company. It has no business being
  offered as further reading to a director whose company cannot pay its debts.

Added:

- `/data/cvl-statistics/` and `/data/compulsory-liquidation-statistics/`
- `/data/uk-insolvency-statistics/`
- `/liquidation/how-much-does-liquidation-cost/`, which the page had never linked to
  anywhere despite carrying a costs section. Cost is the question directors ask first.

All four were confirmed live (200, no redirect) before linking. Note that
`/uk-insolvency-statistics/` now 301s to `/data/uk-insolvency-statistics/`, so the link
uses the destination directly.

The two Members' Voluntary Liquidation links in the *body* were kept. They sit in the
route-selection table and the alternatives section, where the job is to send a solvent
reader somewhere better. That is the opposite of a Related Guides entry.

## What deliberately did NOT change

Title tag, H1, URL, body copy below the opening sections, FAQs, schema, anchor ids, and
no link-building was started. If any of these change before the decision point, record
the date and what changed, because the test is then no longer clean.

## Open inconsistency, not fixed

The body calls the insolvency tool a "two-minute insolvency test" twice. Related Guides
calls it the "30-Second Insolvency Test", which matches the live page title. The tool was
rebuilt as a multi-step guided test in August 2026, so it is not obvious which duration is
now true. Left alone rather than guessed at. Somebody should time it and make the page
say one thing.

## Baseline: 90 days, 13 May to 10 August 2026, UK

Head-term family only. The URL's blended average is diluted by 646 peripheral queries and
must not be used. Search Console keeps the apostrophe variant as a separate query, so the
set is ten. Count only rows landing on `/liquidation/creditors-voluntary-liquidation/`;
drop anchor-fragment rows (`#cvl-process`, `#toc_0`) and sibling URLs.

| Query | Clicks | Impressions | Position |
| ----- | -----: | ----------: | -------: |
| creditors voluntary liquidation | 1 | 2,020 | 29.5 |
| cvl | 0 | 860 | 28.0 |
| creditor voluntary liquidation | 0 | 549 | 28.4 |
| voluntary creditors liquidation | 0 | 334 | 28.0 |
| creditors' voluntary liquidation | 0 | 222 | 28.3 |
| creditors voluntary liquidation uk | 0 | 205 | 22.1 |
| what is a cvl | 0 | 195 | 25.5 |
| creditors liquidation | 0 | 158 | 27.5 |
| cvl process | 0 | 120 | 32.0 |
| cvl liquidation | 0 | 76 | 24.5 |

**The three numbers to beat**

| Measure | Baseline |
| ------- | -------- |
| Median position across the ten | **28.0** |
| Bands 1-10 / 11-20 / 21-30 / 31+ | **0 / 0 / 9 / 1** |
| Total impressions across the set | **4,739** |

Supporting: mean 27.4, best 22.1, worst 32.0, total clicks 1.

28-day trend (14 Jul to 10 Aug 2026): median 24.1, 1,162 impressions, 0 clicks. The
28-day window reads 3 to 4 places better than the 90-day. On these volumes that is noise.
Use the 90-day figures as the decision baseline.

## How to re-measure

Search Console API, property `https://www.companydebt.com/`, country `GBR`, dimensions
`query,page`, filter operator `includingRegex`:

```
^(creditors? voluntary liquidation( uk)?|creditors'? voluntary liquidation|voluntary creditors liquidation|creditors liquidation|cvl|cvl liquidation|cvl process|what is a cvl)$
```

Compute the same three numbers the same way. Check weekly. Do not act on a single week.

**Success:** several of the ten queries move from the 21-30 band into 11-20 or better,
with nothing else altered.

**Failure:** the band stays at 20-30. The structural explanation is then spent. The honest
conclusion is a strong page on the deepest SERP in the sector, with eleven competing
licensed practices in the top 20, and the effort belongs where the cluster already wins.

## Notes from making the change

- The handover said the page had no summary block at all. It did: a `cd-key-facts-panel`
  headed "Creditors' Voluntary Liquidation in 30 Seconds". The problem was that its title
  was a paragraph, not a heading, so it was invisible to any structural read of the page.
- The handover reported a duplicated "Related Guides" H2 on live. There is only one. The
  apparent duplicate is a `<h2>Related Guides</h2>` string inside a comment in the theme's
  related-guides script. Nothing to fix.
- The voice-audit gate was overridden twice, with reasons recorded in
  `editorial-os/voice-audits/creditors-voluntary-liquidation.json`: the redraft-after-4-passes
  rule (a redraft would move many variables and destroy the test) and the outside-eye read
  (outstanding, not waived). An outside-eye read should be run before this goes to production.
- `article_audit.py`: 32/32 PASS. `check_statutory_fees.py`: clean.
