# /liquidation/ — search baseline before the correction pass

Captured 8 August 2026, immediately before the factual corrections were pushed.
Source: Search Console, property `https://www.companydebt.com/`, page filter
`https://www.companydebt.com/liquidation/`.

## Head term: "company liquidation"

90 days to 8 Aug 2026: **8 clicks, 2,038 impressions, 0.39% CTR, average position 14.4.**

The 90-day average hides a step change. Daily position for the head term:

| Period | Position |
|---|---|
| 9 Jun – 2 Jul | 17 to 27 (page 2 to 3) |
| 3 Jul – 13 Jul | 7 to 9 |
| 14 Jul – 6 Aug | 5.3 to 6.6, stable |

The page moved onto page one around **3 July 2026** and has held positions 5 to 6
for five weeks. The owner's "first page" description is correct and current; the
90-day average position of 14.4 is a lagging artefact of the pre-July period.
That confirms the preservation-first mandate.

## The finding the brief did not have

At position 5 to 6 with roughly 30 impressions a day, this page earns close to
zero clicks. Across the whole 90 days: **8 clicks from 2,038 impressions.**
There were 0 clicks on 24 of the last 30 days despite holding position 6.

A normal CTR at position 5 to 6 is in the 4 to 8% band. This page is at 0.4%,
so it is underperforming its own ranking by roughly an order of magnitude.
Ranking is not the constraint here. The click is.

The most likely cause is what the result looks like in the SERP. As at this
baseline:

- Title tag: `Company Liquidation: What UK Directors Need to Know`
- Meta description: `Understand company liquidation and how to wind up your UK business legally, efficiently, and with confidence.`

Neither carries a number, a route, a cost or a next step, and both read as
generic against GOV.UK and the practitioner firms sitting around them.

This is deliberately **not** acted on in this pass. The master brief bars
title/meta changes in phase one, and correctly: the corrections should be
allowed to settle first so any movement can be attributed. But the brief's
reason for leaving title/meta alone was "do not change it simply because a
competitor uses different wording". That reasoning does not cover this. A 0.4%
CTR at position 6 is first-party evidence, not competitor mimicry, and it is
the single largest gap between what this page ranks for and what it earns.

Recommended as the next lever once the corrections have settled, ahead of the
optional route selector.

## Other queries the page holds (90 days)

| Query | Clicks | Impressions | Position |
|---|---:|---:|---:|
| company liquidation | 8 | 2,038 | 14.4 |
| liquidation of a company | 1 | 279 | 16.1 |
| liquidate a company | 1 | 263 | 18.4 |
| business liquidation | 0 | 255 | 25.5 |
| business liquidation process | 0 | 103 | 26.7 |
| business in liquidation | 0 | 51 | 26.9 |

## Page state at baseline

Snapshot of the live HTML and the page metadata are alongside this file:
`baseline-live-7669-2026-08-08.html`, `baseline-draft-7669-2026-08-08.html`,
`baseline-metadata.json`. H1, canonical and section order are recorded there
and were all preserved through the correction pass.

## What to watch after deployment

Compare against the numbers above. Position for the head term should hold at
5 to 6. If it weakens materially, the cause is more likely the added cost
table than any of the factual corrections; revert the table before touching
the corrections, which should not go back to stale figures under any
circumstances.
