# Sector Statistics Overlay

Sub-class of the Data Reference overlay: a single-SIC-sector insolvency data
page (`scripts/datahub/pages/sic_group_stats.py`), e.g. furniture, pubs,
haulage. Audience is analytical (journalists, lenders, accountants,
directors researching a sector), not a stressed director working through a
procedure — do not import the full guide-page humanise treatment wholesale.

Everything in `overlays/statistics.md` applies. In addition:

- **Sourced sector-context fact, not an asserted one.** Every page must carry
  at least one comparison computed from the actual data (e.g. share of the
  parent SIC section, a trough-year divergence) — never a plausible-sounding
  claim invented for colour. `sic_group_stats.py`'s `sector_fact()` computes
  this generically from `sector_series.json`; do not hand-write a stat that
  bypasses it.
- **Practitioner-voice insight, calibrated down from the full guide bar.**
  Apply `runtime-packs/stages/humanise.md` Part C items 2 and 4 only (earned
  practitioner "we", one asymmetrical evaluative line) — skip item 1
  (concrete scenes) and item 3 (reader-stress warmth); those assume a
  director mid-crisis reading a procedural page, which is the wrong register
  here. The insight must read as informed sector judgement ("in the cases we
  handle..."), not a restatement of the numbers already on the page.
- **No invented specifics.** Do not assert named companies, dates, or figures
  that are not in `data/insolvency-statistics/`. General, well-established
  sector economics (cost structure, demand sensitivity) are fine as editorial
  judgement; specific claims are not, unless sourced.
- **Gate is real, not a printed claim.** `scripts/sector_data_audit.py` runs
  automatically inside `build_page.py --publish` for this page_class and
  blocks the push on a hard-fail. It checks structurally for the insight and
  sector-fact blocks (`.cd-side-note__insight`, `.cd-sector-fact`), not their
  quality — a human re-read against the two points above is still required
  before publish, same as Tier 3 on the guide-page gate.
