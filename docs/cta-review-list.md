# CTA Placement Review List — how to use it

The list itself is `cta-review-list.csv` (230 rows, opens in Excel or Sheets). Columns are
the ones set out in section 12 of `cta-insolvency-test-wording-plan.md`; row order is the
review order from section 13.

Regenerate after the manifest changes: `python scripts/build_cta_review_list.py`
(this overwrites the file, so export your working copy elsewhere once you start filling
it in).

## State of play

The theme's automatic three-CTA injector has been removed. **No page on staging currently
carries an in-content CTA**, including the 54 that used to. Nothing goes back until the
rows below say where it goes, so an unreviewed page shows nothing rather than something
wrong.

## What is already filled in, and what is not

Only two groups have decisions pre-filled, because only two are conclusive from the page
name alone:

| Group | Rows | What is filled | Confidence |
|---|---|---|---|
| Solvent-closure cluster | 8 | Variant `none`, solvent-closure CTA instead | high |
| Page names a formal creditor action | 14 | `urgent_action`, test secondary, direct advice as primary | medium |
| Everything else | 208 | Nothing | low |

The 208 are blank on purpose. The plan says clusters and URLs are not decisions, and the
earlier automated pass proved the point by classing a directors' loan account page as an
enforcement page because "writ" appears inside "writing".

Even the 14 medium rows want a check: a page named after a winding-up petition may be read
by a director who has one, or by a director trying to work out whether one is coming. Only
the first is urgent.

## Filling a row

Work through the questions in plan section 8, in order:

1. **Primary audience** — director, employee, creditor, mixed. Anything but director or
   mixed usually means `Test fit: none`.
2. **Assumed state** — uncertain, serious distress, solvent, already in process.
3. **Formal action** — none, possible, active. Only "active" earns `urgent_action`.
4. **Personal-risk context** — yes or no. Yes means `personal_risk_secondary`, compact.
5. **Test fit** — primary, secondary, none.
6. **Variant** — `early_check`, `serious_position`, `personal_risk_secondary` or `none`.
7. **Block size** — large, compact, none. No page gets two dominant blocks.
8. **Alternative primary CTA** — where the test is not the right primary action: direct
   advice, solvent closure, creditor guidance.

Notes column: say why, especially where the answer was not obvious. That is what makes the
decision reviewable later rather than re-litigated.

## Feeding decisions back

Reviewed rows go into the page map in `mu-plugins/cd-cta-insolvency-test.php`
(`cd_test_cta_page_map()`), keyed by slug. Only reviewed pages belong there; anything
absent falls to the safe default.

## The 54

54 rows are marked "carried the old injected CTA set" in Notes. They lost a CTA when the
injector came out, so they are the ones currently converting worse than they were. Worth
doing first within each phase.
