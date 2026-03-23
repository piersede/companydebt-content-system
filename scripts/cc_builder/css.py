"""Shared CSS for credit card page components.

Each constant is a complete <style> block ready for raw_html() injection.
"""

# ── Hero zone (v4 design) ─────────────────────────────────────────────

CC_HERO_CSS = '''<style>
/* Hero Zone — v4 two-column grid layout, breaks out to full width */
.cc-hero-zone {
  width: 100vw;
  position: relative;
  left: 50%;
  transform: translateX(-50%);
  padding: 0 max(40px, calc((100vw - 1100px) / 2));
  box-sizing: border-box;
  margin: 0 0 32px 0;
}

/* ── Two-column hero grid ── */
.cc-hero-grid {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 60px;
  align-items: stretch;
  margin-bottom: 28px;
}
@media (max-width: 880px) {
  .cc-hero-grid { grid-template-columns: 1fr; gap: 32px; }
}
.cc-hero-left {
  display: flex;
  flex-direction: column;
}
.cc-hero-right {}

/* ── Verdict text (left column) ── */
.cc-hero-verdict {
  font-size: 16.5px;
  color: #4A4A5A;
  line-height: 1.65;
  margin: 48px 0 20px 0;
}

/* ── Verification notice (left column) ── */
.cc-hero-verify {
  font-size: 14.5px;
  font-weight: 600;
  color: #7B2D8E;
  font-style: italic;
  letter-spacing: -0.01em;
  line-height: 1.5;
  margin: 0 0 20px 0;
}

/* ── Top Pick Card (right column) v4.5 ──
   Hierarchy: eyebrow → product name → tagline → image → benefits → CTA.
   Type scale: 11px metadata | 14.5px body | 18px name. */
.cc-hero-tp {
  background: #fff;
  border: 1px solid #DDD6E5;
  border-radius: 14px;
  padding: 24px 28px 22px;
  margin-top: 48px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.10);
}

/* Eyebrow: small restrained label */
.cc-hero-tp__label {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #6E6E78;
  margin-bottom: 6px;
  text-align: center;
}

/* Product name: primary focal point */
.cc-hero-tp__name {
  font-size: 18px;
  font-weight: 700;
  line-height: 1.25;
  color: #2A2A2E;
  text-align: center;
  margin: 0 0 4px 0;
}

/* Tagline: one-line positioning, secondary */
.cc-hero-tp__tagline {
  font-size: 13px;
  color: #6E6E78;
  text-align: center;
  line-height: 1.4;
  margin-bottom: 0;
}

/* Product image: recognition support */
.cc-hero-tp__logo {
  width: 140px;
  height: 90px;
  margin: 18px auto 0;
  background: #FCFBFD;
  border: 1px solid #EEEAF2;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14.5px;
  color: #6E6E78;
  overflow: hidden;
}
.cc-hero-tp__logo img {
  max-width: 100%;
  max-height: 74px;
  object-fit: contain;
}

/* Benefits list: tight parallel proof points */
.cc-hero-tp__list {
  list-style: none;
  margin: 18px 0 20px 0;
  padding: 14px 0 0 0;
  border-top: 1px solid #EEEAF2;
}
.cc-hero-tp__list li {
  font-size: 13px;
  color: #2A2A2E;
  padding: 5px 0 5px 22px;
  position: relative;
  line-height: 1.45;
}
.cc-hero-tp__list li::before {
  content: '\\2713';
  position: absolute;
  left: 0;
  top: 5px;
  color: #6704A4;
  font-weight: 600;
  font-size: 12px;
}

/* CTA: clear action conclusion */
.cc-hero-tp__cta {
  display: block;
  width: 100%;
  padding: 12px;
  background: #6704A4;
  color: #fff !important;
  border: none;
  border-radius: 8px;
  font-size: 14.5px;
  font-weight: 700;
  cursor: pointer;
  text-align: center;
  text-decoration: none;
  transition: background 0.15s;
}
.cc-hero-tp__cta:hover {
  background: #4F0280;
}
.cc-hero-tp__cta:focus-visible {
  outline: 2px solid #6704A4;
  outline-offset: 2px;
}

/* ── Also Consider Strip v4.2 ──
   Clean editorial alternatives. Reading order: image → text → CTA.
   Palette: #6704A4 accent (button only), #DDD6E5 borders, dark neutrals. */
.cc-hero-also {
  padding: 0;
}
.cc-hero-also__label {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color: #6E6E78;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.cc-hero-also__label::before {
  content: '';
  width: 16px;
  height: 1.5px;
  background: #6704A4;
}
.cc-hero-also__list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
}
@media (max-width: 780px) {
  .cc-hero-also__list { grid-template-columns: 1fr; }
}

/* Card: single-row grid — image | text block (badge inside) | CTA */
.cc-hero-also__row {
  display: grid;
  grid-template-columns: 44px 1fr max-content;
  gap: 0 12px;
  align-items: center;
  background: #fff;
  border: 1px solid #DDD6E5;
  border-radius: 10px;
  padding: 22px 20px;
  transition: border-color 0.15s, box-shadow 0.15s;
}
.cc-hero-also__row:hover {
  border-color: #C5BCD2;
  box-shadow: 0 2px 10px rgba(103,4,164,0.05);
}

/* Logo: small, functional, left-anchored */
.cc-hero-also__thumb {
  width: 44px;
  height: 34px;
  border-radius: 6px;
  background: #FCFBFD;
  border: 1px solid #E8E2EF;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 11px;
  color: #6E6E78;
  overflow: hidden;
  flex-shrink: 0;
}
.cc-hero-also__thumb img {
  max-width: 100%;
  max-height: 28px;
  object-fit: contain;
}

/* Text block: badge (optional) → title → tagline */
.cc-hero-also__body {
  min-width: 0;
}
.cc-hero-also__tag {
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.3px;
  text-transform: uppercase;
  color: #6704A4;
  line-height: 1;
  margin-bottom: 3px;
}
.cc-hero-also__name {
  font-size: 14.5px;
  font-weight: 700;
  line-height: 1.25;
  color: #2A2A2E;
}
.cc-hero-also__desc {
  font-size: 12.5px;
  color: #4A4A52;
  line-height: 1.4;
  margin-top: 4px;
}

/* CTA: right-aligned, compact, clearly secondary */
.cc-hero-also__link {
  padding: 7px 14px;
  background: #6704A4;
  color: #fff !important;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  text-decoration: none;
  white-space: nowrap;
  transition: background 0.15s;
  cursor: pointer;
  flex-shrink: 0;
}
.cc-hero-also__link:hover {
  background: #4F0280;
}

/* ── Affiliate disclosure (tier 1, top of page) ── */
.cc-hero-disclosure {
  font-size: 12.5px;
  color: #888;
  line-height: 1.5;
  margin: 8px 0 0 0;
}
.cc-hero-disclosure a {
  color: #6704A4;
  text-decoration: underline;
}

/* ── FAQ native details/summary ── */
.cc-faq__details { border: none; }
.cc-faq__details summary { cursor: pointer; list-style: none; }
.cc-faq__details summary::-webkit-details-marker { display: none; }
.cc-faq__details[open] .cc-faq__icon { transform: rotate(90deg); }
.cc-faq__answer { padding: 0 0 12px 0; }

/* ── Mobile: collapse also-consider behind toggle ── */
@media (max-width: 640px) {
  .cc-hero-also__list { display: none; }
  .cc-hero-also__list.cc-hero-also--expanded { display: grid; grid-template-columns: 1fr; gap: 14px; }
  .cc-hero-also__toggle {
    display: block; width: 100%; padding: 10px; margin-top: 8px;
    background: #f5f0fa; border: 1px solid #DDD6E5; border-radius: 8px;
    font-size: 13px; font-weight: 600; color: #6704A4; cursor: pointer;
    text-align: center;
  }
}
@media (min-width: 641px) {
  .cc-hero-also__toggle { display: none; }
}

/* ── Align also-consider breakpoint with hero grid (880px) ── */
@media (max-width: 880px) and (min-width: 641px) {
  .cc-hero-also__list { grid-template-columns: 1fr 1fr; }
}

/* ── Medium-screen TOC (horizontal sticky bar, 768-1340px) ── */
@media (min-width: 768px) and (max-width: 1339px) {
  .cc-toc {
    position: sticky !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    display: flex !important;
    background: #fff;
    border-bottom: 1px solid #eee;
    padding: 10px 20px;
    z-index: 100;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  }
  .cc-toc__list {
    display: flex;
    gap: 18px;
    flex-wrap: nowrap;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    margin: 0; padding: 0; list-style: none;
  }
  .cc-toc__item { white-space: nowrap; }
  .cc-toc__link { font-size: 13px; padding: 4px 0; }
}
</style>'''

# ── Table of Contents sidebar ──────────────────────────────────────────

CC_TOC_CSS = '''<style>
/* Table of Contents Sidebar — spacious, invisible-but-useful
   Matches page type scale: 14.5px body tier. Max 6 items. */
.cc-toc {
  display: none;
}

@media (min-width: 1340px) {
  .cc-toc {
    display: block;
    position: fixed;
    top: 140px;
    width: 220px;
    max-height: calc(100vh - 200px);
    overflow-y: auto;
    padding: 0;
    z-index: 50;
  }
  .cc-toc__list {
    list-style: none;
    margin: 0;
    padding: 0;
    border-right: 1px solid #E0DCE8;
  }
  .cc-toc__item {
    margin: 0;
    padding: 0;
  }
  .cc-toc__link {
    display: block;
    padding: 10px 16px;
    font-size: 14.5px;
    line-height: 1.45;
    color: #6E6E78;
    text-decoration: none;
    margin-right: -1px;
    border-right: 2px solid transparent;
    transition: color 0.2s, border-color 0.2s;
  }
  .cc-toc__link:hover {
    color: #2A2A2E;
  }
  .cc-toc__link--active {
    color: #6704A4;
    border-right-color: #6704A4;
    font-weight: 600;
  }
  .cc-toc::-webkit-scrollbar {
    width: 3px;
  }
  .cc-toc::-webkit-scrollbar-thumb {
    background: #DDD6E5;
    border-radius: 3px;
  }
}
</style>'''


# ── Credit card component v4 ──────────────────────────────────────────

CC_CARD_CSS = '''<style>
/* Credit Card Comparison Component v4.5 — Company Debt
   Strip → horizontal header (image | text | CTA) → stats → notes → footer.
   Palette: #6704A4 accent (CTA only). Text: #2A2A2E / #4A4A52 / #6E6E78 / #8A8A94.
   Type scale (4 tiers): 18px title | 14.5px body | 13px secondary | 11px metadata. */

/* ── Card shell ── */
.cc-card {
  border: 1px solid #DDD6E5;
  border-radius: 14px;
  background: #fff;
  margin-top: 40px;
  margin-bottom: 36px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0,0,0,0.10);
}

/* ── Context strip: quiet positioning metadata ── */
.cc-card__summary-strip {
  background: #FCFBFD;
  border-bottom: 1px solid #EEEAF2;
  padding: 6px 32px;
  font-size: 11px;
  font-weight: 600;
  color: #6E6E78;
}

/* ── Header: 3-column — image | text | CTA ── */
.cc-card__header {
  display: grid;
  grid-template-columns: 100px 1fr auto;
  gap: 0 24px;
  align-items: center;
  padding: 22px 32px;
}
.cc-card__image {
  width: 100px;
  height: 72px;
  background: #FCFBFD;
  border-radius: 8px;
  border: 1px solid #EEEAF2;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6px;
}
.cc-card__image img {
  max-width: 100%;
  max-height: 60px;
  object-fit: contain;
  display: block;
}
.cc-card__identity {
  min-width: 0;
}
.cc-card__identity h3 {
  font-size: 18px;
  font-weight: 700;
  line-height: 1.25;
  color: #2A2A2E;
  margin-bottom: 5px;
}
.cc-card__verdict {
  font-size: 14.5px;
  line-height: 1.5;
  color: #4A4A52;
  max-width: 520px;
}

/* CTA: right-aligned, vertically centred */
.cc-card__header-cta {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}
.cc-card__cta {
  display: inline-block;
  padding: 11px 28px;
  background: #6704A4;
  color: #fff !important;
  font-size: 14.5px;
  font-weight: 700;
  border-radius: 8px;
  text-decoration: none;
  transition: background 0.15s;
  white-space: nowrap;
}
.cc-card__cta:hover {
  background: #4F0280;
}
.cc-card__cta:focus-visible {
  outline: 2px solid #6704A4;
  outline-offset: 2px;
}

/* Legacy: hide if still in markup */
.cc-card__fit-label { display: none; }

/* ── 2×2 facts grid ── */
.cc-card__facts {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0;
  margin: 0 32px;
  border-top: 1px solid #EEEAF2;
  border-bottom: 1px solid #EEEAF2;
}
.cc-card__fact {
  padding: 14px 18px 14px 0;
  border-bottom: 1px solid #EEEAF2;
}
.cc-card__fact:nth-child(even) {
  border-left: 1px solid #EEEAF2;
  padding-left: 18px;
}
.cc-card__fact:nth-child(odd) {
  padding-left: 0;
}
.cc-card__fact:nth-last-child(-n+2) {
  border-bottom: none;
}
.cc-card__fact-label {
  display: block;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #6E6E78;
  margin-bottom: 4px;
}
.cc-card__fact-value {
  display: block;
  font-size: 14.5px;
  font-weight: 700;
  color: #2A2A2E;
  line-height: 1.35;
}
/* APR value: same size as other facts, title stays largest */
.cc-card__fact-value--apr {
  font-size: 14.5px;
  font-weight: 700;
}
.cc-card__fact-qualifier {
  display: block;
  font-size: 11px;
  font-weight: 400;
  color: #8A8A94;
  line-height: 1.35;
  margin-top: 3px;
}
.cc-card__fact-value--required,
.cc-card__fact-value--none-required {
  font-size: 14.5px;
  font-weight: 700;
}

/* ── Notes: concise editorial labels ── */
.cc-card__notes {
  margin: 0 32px;
  padding: 14px 0 10px 0;
}
.cc-card__note {
  font-size: 13px;
  line-height: 1.5;
  color: #4A4A52;
  padding: 5px 0;
}
.cc-card__note strong {
  color: #2A2A2E;
  font-weight: 700;
}

/* ── Footer: quiet concluding line ── */
.cc-card__footer {
  display: flex;
  align-items: baseline;
  gap: 24px;
  margin: 0 32px;
  padding: 10px 0 18px 0;
  border-top: 1px solid #EEEAF2;
}
.cc-card__editorial-toggle {
  font-size: 13px;
  font-weight: 600;
  color: #6704A4 !important;
  text-decoration: none;
  transition: color 0.15s;
  white-space: nowrap;
}
.cc-card__editorial-toggle:hover {
  color: #4F0280 !important;
  text-decoration: underline;
}
.cc-card__trust {
  font-size: 11px;
  color: #8A8A94;
  line-height: 1.4;
}

/* ── Section divider ── */
.cc-section-divider {
  margin-top: 48px;
  padding-top: 48px;
  border-top: 1px solid #DDD6E5;
}
.cc-section-divider__label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #6704A4;
  margin-bottom: 8px;
}
.cc-section-divider__label::before {
  content: '';
  display: block;
  width: 18px;
  height: 1.5px;
  background: #6704A4;
}

/* ── Mobile ── */
@media (max-width: 640px) {
  .cc-card__summary-strip {
    padding: 6px 20px;
  }
  .cc-card__header {
    grid-template-columns: 72px 1fr;
    grid-template-rows: auto auto;
    gap: 0 14px;
    padding: 18px 20px 16px 20px;
  }
  .cc-card__image {
    width: 72px;
    height: 52px;
    padding: 5px;
    grid-row: 1 / 2;
  }
  .cc-card__image img {
    max-height: 42px;
  }
  .cc-card__header-cta {
    grid-column: 1 / -1;
    padding-top: 10px;
  }
  .cc-card__cta {
    display: block;
    width: 100%;
    text-align: center;
  }
  .cc-card__facts {
    grid-template-columns: 1fr;
    margin: 0 20px;
  }
  .cc-card__fact:nth-child(even) {
    border-left: none;
    padding-left: 0;
  }
  .cc-card__fact {
    border-bottom: 1px solid #EEEAF2;
    padding: 12px 0;
  }
  .cc-card__fact:last-child {
    border-bottom: none;
  }
  .cc-card__notes {
    margin: 0 20px;
  }
  .cc-card__footer {
    margin: 0 20px;
    flex-direction: column;
    gap: 6px;
  }
  .cc-card__trust {
    text-align: left;
  }
}
</style>'''


# ── Comparison Table (v4 — 6-column desktop, stacked mobile) ──────────

CC_COMPARISON_TABLE_CSS = '''<style>
/* Comparison Table v4 */
.cc-ct {
  margin: 32px 0;
  font-family: inherit;
}

/* ── Desktop: 6-column table ── */
.cc-ct__table {
  width: 100%;
  border-collapse: collapse;
  border-spacing: 0;
  table-layout: auto;
  font-size: 14px;
  line-height: 1.45;
}
.cc-ct__table thead th {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #555;
  background: #f8f8fa;
  padding: 12px 14px;
  border-bottom: 2px solid #e0e0e5;
  text-align: left;
  white-space: nowrap;
}
/* Column widths: Card 22%, Fee 12%, APR/Type 14%, Best for 22%, Features 18%, Action 12% */
.cc-ct__table thead th:nth-child(1) { width: 22%; }
.cc-ct__table thead th:nth-child(2) { width: 12%; }
.cc-ct__table thead th:nth-child(3) { width: 14%; }
.cc-ct__table thead th:nth-child(4) { width: 22%; }
.cc-ct__table thead th:nth-child(5) { width: 18%; }
.cc-ct__table thead th:nth-child(6) { width: 12%; }

.cc-ct__table tbody tr {
  border-bottom: 1px solid #ebebeb;
  transition: background 0.1s;
}
.cc-ct__table tbody tr:hover {
  background: #fafafa;
}
.cc-ct__table tbody td {
  padding: 14px 14px;
  vertical-align: top;
  color: #1a1a1a;
}
.cc-ct__table tbody td:first-child {
  position: relative;
  padding-bottom: 32px;
}

/* Card name cell */
.cc-ct__card-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}
.cc-ct__card-logo {
  width: 40px;
  height: 28px;
  border-radius: 4px;
  background: #f5f5f6;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  overflow: hidden;
}
.cc-ct__card-logo img {
  max-width: 100%;
  max-height: 24px;
  object-fit: contain;
}
.cc-ct__card-name {
  font-weight: 700;
  font-size: 14px;
  color: #1a1a1a;
  line-height: 1.3;
}

/* Badge in card cell */
.cc-ct__badge {
  display: inline-block;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  padding: 2px 8px;
  border-radius: 3px;
  margin-top: 3px;
  white-space: nowrap;
}
.cc-ct__badge--top { background: #6b3fa0; color: #fff; }
.cc-ct__badge--gold { background: #fef3cd; color: #856404; }
.cc-ct__badge--teal { background: #d1ecf1; color: #0c5460; }
.cc-ct__badge--pink { background: #f8d7da; color: #721c24; }

/* APR/type cell */
.cc-ct__apr {
  font-weight: 700;
  font-size: 15px;
  color: #1a1a1a;
}
.cc-ct__type {
  font-size: 12px;
  color: #666;
  margin-top: 2px;
}

/* Features cell — compact list */
.cc-ct__features {
  list-style: none;
  padding: 0;
  margin: 0;
}
.cc-ct__features li {
  font-size: 13px;
  color: #333;
  line-height: 1.4;
  padding: 2px 0 2px 14px;
  position: relative;
}
.cc-ct__features li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: #2e7d32;
  font-size: 12px;
  font-weight: 700;
}

/* Action cell */
.cc-ct__action-link {
  display: inline-block;
  padding: 7px 12px;
  min-width: 120px;
  max-width: 160px;
  box-sizing: border-box;
  text-align: center;
  background: #6b3fa0;
  color: #fff !important;
  font-size: 12px;
  font-weight: 600;
  border-radius: 5px;
  text-decoration: none;
  white-space: normal;
  line-height: 1.3;
  transition: background 0.15s;
}
.cc-ct__action-link:hover {
  background: #5a3488;
}

/* Expandable detail row */
.cc-ct__detail-toggle {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #6b3fa0;
  cursor: pointer;
  background: none;
  border: none;
  padding: 0;
  position: absolute;
  bottom: 14px;
  left: 14px;
  font-weight: 600;
}
.cc-ct__detail-toggle:hover {
  text-decoration: underline;
}
.cc-ct__detail-toggle:focus-visible {
  outline: 2px solid #6704A4;
  outline-offset: 2px;
  border-radius: 3px;
}
.cc-ct__detail-row {
  display: none;
}
.cc-ct__detail-row.cc-ct--open {
  display: table-row;
}
.cc-ct__detail-row td {
  padding: 0 14px 16px 14px;
  background: #fafafa;
  border-bottom: 1px solid #ebebeb;
}
.cc-ct__detail-inner {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px 24px;
  font-size: 13px !important;
  line-height: 1.5;
  color: #333;
  padding: 14px 0;
}
.cc-ct__detail-label {
  font-size: 11px !important;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #777;
  margin: 0 0 4px 0;
  line-height: 1.3;
}
.cc-ct__detail-block p {
  margin: 0;
  font-size: 13px !important;
  line-height: 1.5;
}

/* Verification footer */
.cc-ct__footer {
  font-size: 12.5px;
  color: #666;
  line-height: 1.4;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid #ebebeb;
}

/* ── Mobile: stacked cards ── */
@media (max-width: 768px) {
  .cc-ct__table,
  .cc-ct__table thead,
  .cc-ct__table tbody,
  .cc-ct__table tr,
  .cc-ct__table td,
  .cc-ct__table th {
    display: block;
    width: 100%;
  }
  .cc-ct__table thead {
    display: none;
  }
  .cc-ct__table tbody tr {
    background: #fff;
    border: 1px solid #e0e0e5;
    border-radius: 10px;
    margin-bottom: 16px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .cc-ct__table tbody tr:hover {
    background: #fff;
  }
  .cc-ct__table tbody td {
    padding: 0;
  }
  /* Show labels on mobile */
  .cc-ct__table tbody td::before {
    content: attr(data-label);
    display: block;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #777;
    margin-bottom: 2px;
  }
  /* Card cell: no label needed (logo + name is self-describing) */
  .cc-ct__table tbody td:first-child::before {
    display: none;
  }
  .cc-ct__card-cell {
    gap: 12px;
  }
  .cc-ct__card-logo {
    width: 48px;
    height: 34px;
  }
  /* Action: full width button */
  .cc-ct__action-link {
    display: block;
    text-align: center;
    padding: 10px 16px;
    width: 100%;
    box-sizing: border-box;
  }
  /* Detail panel: single column on mobile */
  .cc-ct__detail-row {
    display: none;
    border: none;
    background: none;
    padding: 0;
  }
  .cc-ct__detail-row.cc-ct--open {
    display: flex;
    margin-top: 4px;
  }
  .cc-ct__detail-row td {
    padding: 12px 0 0 0;
    background: transparent;
    border: none;
  }
  .cc-ct__detail-inner {
    grid-template-columns: 1fr;
    gap: 10px;
  }
}
</style>'''


# ── Editorial layout CSS generator ─────────────────────────────────────
# Generates page-scoped CSS for the spacious editorial design.
# Validated on compare_amex (page-id-54934), now parameterised for all pages.

def generate_editorial_css(wp_page_id: int, include_comparison_table: bool = True) -> str:
    """Generate editorial layout CSS scoped to a specific WP page ID.

    Args:
        wp_page_id: WordPress page ID (used for .page-id-XXXXX scoping).
        include_comparison_table: Include comparison table refinements
            (False for review/guide pages that don't use tables).

    Returns:
        Complete <style> block string.
    """
    p = f'.page-id-{wp_page_id}'

    # Section 5: Comparison table refinements (conditional)
    comparison_table_css = ''
    if include_comparison_table:
        comparison_table_css = f"""
/* ── 5. COMPARISON TABLE — calm, scannable, spacious rows ── */
{p} .cc-ct {{
  margin: 48px 0 56px 0;
}}
{p} .cc-ct__table {{
  font-size: 14px;
}}
{p} .cc-ct__table thead th:nth-child(1) {{ width: 19%; }}
{p} .cc-ct__table thead th:nth-child(2) {{ width: 11%; }}
{p} .cc-ct__table thead th:nth-child(3) {{ width: 12%; }}
{p} .cc-ct__table thead th:nth-child(4) {{ width: 25%; }}
{p} .cc-ct__table thead th:nth-child(5) {{ width: 20%; }}
{p} .cc-ct__table thead th:nth-child(6) {{ width: 13%; }}
{p} .cc-ct__table thead th {{
  padding: 14px 16px;
  background: #FAFAFA;
  border-bottom: 1px solid #E8E2EF;
  color: #8A8A94;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.07em;
}}
{p} .cc-ct__table tbody td {{
  padding: 22px 16px;
  vertical-align: middle;
  color: #2A2A2E;
  line-height: 1.5;
}}
{p} .cc-ct__table tbody tr {{
  border-bottom: 1px solid #F0ECF4;
}}
{p} .cc-ct__table tbody tr:last-child {{
  border-bottom: none;
}}
{p} .cc-ct__table tbody tr:hover {{
  background: #FDFCFE;
}}
{p} .cc-ct__table tbody td:first-child {{
  padding-bottom: 38px;
}}
{p} .cc-ct__card-cell {{
  gap: 12px;
}}
{p} .cc-ct__card-logo {{
  width: 42px;
  height: 30px;
  border-radius: 5px;
  background: #FAFAFA;
  border: 1px solid #F0ECF4;
}}
{p} .cc-ct__card-name {{
  font-size: 13.5px;
  font-weight: 700;
  line-height: 1.35;
}}
{p} .cc-ct__badge {{
  font-size: 9px;
  padding: 2px 7px;
  margin-top: 4px;
}}
{p} .cc-ct__apr {{
  font-size: 14px;
  font-weight: 600;
}}
{p} .cc-ct__type {{
  font-size: 12px;
  color: #8A8A94;
  margin-top: 3px;
}}
{p} .cc-ct__table tbody td:nth-child(4) {{
  font-size: 13.5px;
  line-height: 1.55;
  color: #4A4A52;
}}
{p} .cc-ct__features li {{
  font-size: 13px;
  padding: 3px 0 3px 16px;
  line-height: 1.45;
  color: #4A4A52;
}}
{p} .cc-ct__features li::before {{
  color: #6704A4;
  font-size: 11px;
}}
{p} .cc-ct__action-link {{
  padding: 8px 14px;
  min-width: 110px;
  font-size: 12px;
  border-radius: 6px;
  background: #6704A4;
}}
{p} .cc-ct__action-link:hover {{
  background: #4F0280;
}}
{p} .cc-ct__detail-toggle {{
  font-size: 11px;
  color: #8A8A94;
  font-weight: 500;
}}
{p} .cc-ct__detail-toggle:hover {{
  color: #6704A4;
}}
{p} .cc-ct__detail-row td {{
  padding: 0 16px 20px 16px;
  background: #FDFCFE;
  border-bottom: 1px solid #F0ECF4;
}}
{p} .cc-ct__detail-inner {{
  padding: 18px 0;
  gap: 16px 28px;
}}
{p} .cc-ct__footer {{
  font-size: 12px;
  color: #8A8A94;
  margin-top: 14px;
  padding-top: 14px;
  border-top: 1px solid #F0ECF4;
}}"""

    css = f"""<style>
/* ══ Spacious Editorial Layout — auto-generated for page {wp_page_id} ══ */

/* ── 0. PAGE HEADER ── */
{p} .section-breadcrumbs {{
  margin-bottom: 0;
  padding-bottom: 20px;
  position: relative;
}}
{p} .section-breadcrumbs::before {{
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  left: calc(-50vw + 50%);
  right: calc(-50vw + 50%);
  background: #F9F8FC;
  z-index: -1;
}}
{p} #breadcrumbs,
{p} #breadcrumbs a,
{p} #breadcrumbs span {{
  font-size: 12px;
  color: #7A7584;
  font-weight: 400;
  letter-spacing: 0.01em;
}}
{p} #breadcrumbs a:hover {{
  color: #4A4654;
}}
{p} #breadcrumbs img {{
  opacity: 0.55;
  width: 12px;
  height: 12px;
}}
{p} .hero-section {{
  padding-top: 8px;
  padding-bottom: 20px;
  position: relative;
}}
{p} .hero-section::before {{
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  left: calc(-50vw + 50%);
  right: calc(-50vw + 50%);
  background: #F9F8FC;
  z-index: -1;
}}
{p} .hero-section .container > .row > .col-12:first-child > .row:first-child {{
  display: none !important;
}}
{p} .cc-meta-strip {{
  display: flex;
  align-items: center;
  gap: 0;
  font-size: 13px;
  line-height: 1.4;
  width: 100%;
  padding: 10px 0 6px;
}}
{p} .cc-meta-avatar {{
  width: 44px;
  height: 44px;
  border-radius: 50%;
  margin-right: 12px;
  flex-shrink: 0;
}}
{p} .cc-meta-author {{
  color: #4A4654;
  font-weight: 500;
  white-space: nowrap;
}}
{p} .cc-meta-author .cc-meta-label {{
  color: #7A7584;
  font-weight: 400;
}}
{p} .cc-meta-divider {{
  width: 1px;
  height: 14px;
  background: #D0CDD6;
  margin: 0 8px;
  flex-shrink: 0;
}}
{p} .cc-readtime-inline {{
  display: flex;
  align-items: center;
  gap: 4px;
  color: #6E6E78;
  font-weight: 400;
  white-space: nowrap;
}}
{p} .cc-readtime-icon {{
  color: #9A95A3;
  flex-shrink: 0;
}}
{p} .cc-meta-date {{
  color: #7A7584;
  font-weight: 400;
  white-space: nowrap;
  margin-left: auto;
}}
{p} .cc-disclosure-aligned {{
  display: flex;
  align-items: flex-start;
  justify-content: flex-end;
  padding-top: 8px;
}}
{p} .hero-section h1 {{
  font-size: 38px;
  line-height: 1.18;
  letter-spacing: -0.02em;
  color: #1a1a1e;
  margin-top: 2px;
  margin-bottom: 8px;
  max-width: 620px;
}}
{p} .ad-disclaimer-tooltip {{
  font-size: 11px;
  opacity: 0.9;
}}
{p} .ad-disclaimer-tooltip img {{
  opacity: 0.5;
  filter: grayscale(100%);
  width: 13px;
  height: 13px;
}}
{p} .ad-tooltip-title {{
  font-size: 11px;
  color: #7A7584;
  font-weight: 400;
}}
{p} .date-time-section {{
  display: none !important;
}}

/* ── 1. GLOBAL RHYTHM ── */
{p} .entry-content p {{
  font-size: 17px;
  line-height: 1.75;
  color: #2A2A2E;
  margin-bottom: 1.6em;
}}
{p} .entry-content h2.wp-block-heading {{
  margin-top: 64px;
  margin-bottom: 22px;
  font-size: 26px;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: #1a1a1e;
}}
{p} .entry-content h3.wp-block-heading {{
  margin-top: 44px;
  margin-bottom: 16px;
  font-size: 20px;
  font-weight: 700;
  color: #2A2A2E;
}}

/* ── 2. HERO ZONE ── */
{p} .cc-hero-zone {{
  margin-bottom: 40px;
  padding-bottom: 20px;
  position: relative;
}}
{p} .cc-hero-zone::before {{
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  left: calc(-50vw + 50%);
  right: calc(-50vw + 50%);
  background: #F9F8FC;
  z-index: -1;
}}
{p} .cc-hero-grid {{
  gap: 48px;
  margin-bottom: 24px;
  align-items: start;
}}
{p} .cc-hero-verdict {{
  font-size: 17px;
  line-height: 1.75;
  margin-top: 20px;
  color: #1E1E22;
}}
{p} .cc-hero-verify {{
  font-size: 17px !important;
  line-height: 1.75 !important;
  color: #2A2A2E !important;
  font-weight: 400 !important;
  font-style: italic !important;
  letter-spacing: -0.01em !important;
  margin-bottom: 1.6em !important;
}}
{p} .cc-hero-tp {{
  border-color: #E8E2EF;
  box-shadow: 0 2px 12px rgba(0,0,0,0.10);
  padding: 24px;
  margin-top: 20px;
}}
{p} .cc-hero-tp__label {{
  color: #8A8A94;
  font-size: 10px;
  letter-spacing: 0.08em;
  margin-bottom: 6px;
  text-align: left;
}}
{p} .cc-hero-tp__name {{
  font-size: 18px;
  margin-bottom: 4px;
  text-align: left;
}}
{p} .cc-hero-tp__tagline {{
  text-align: left;
}}
{p} .cc-hero-tp__logo {{
  margin: 16px 0 0 0;
}}
{p} .cc-hero-tp__list {{
  margin: 16px 0 20px 0;
  padding-top: 16px;
}}
{p} .cc-hero-tp__list li {{
  padding: 5px 0 5px 24px;
  font-size: 14px;
  line-height: 1.5;
}}
{p} .cc-hero-tp__cta {{
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 14px;
  display: inline-block;
  width: auto;
  text-align: center;
}}

/* ── 4. BRIDGE PARAGRAPH ── */
{p} .cc-hero-zone + .wp-block-html + .wp-block-paragraph,
{p} .cc-hero-zone ~ .wp-block-paragraph:first-of-type {{
  margin-top: 8px;
  margin-bottom: 2.2em;
}}
{comparison_table_css}

/* ── 6. SECTION DIVIDERS ── */
{p} .cc-section-divider {{
  margin-top: 64px;
  padding-top: 64px;
  border-top: 1px solid #F0ECF4;
}}

/* ── 7. CARD BLOCKS ── */
{p} .cc-card {{
  margin-top: 48px;
  margin-bottom: 48px;
  border-color: #E8E2EF;
  box-shadow: 0 2px 12px rgba(0,0,0,0.10);
}}
{p} .cc-card__summary-strip {{
  padding: 7px 32px;
  background: #FDFCFE;
  border-bottom-color: #F0ECF4;
}}
{p} .cc-card__header {{
  padding: 26px 32px;
  gap: 0 28px;
}}
{p} .cc-card__identity h3 {{
  font-size: 19px;
  margin-bottom: 6px;
}}
{p} .cc-card__verdict {{
  font-size: 15px;
  line-height: 1.6;
}}
{p} .cc-card__facts {{
  margin: 0 32px;
}}
{p} .cc-card__fact {{
  padding: 16px 18px 16px 0;
}}
{p} .cc-card__fact:nth-child(even) {{
  padding-left: 20px;
}}
{p} .cc-card__notes {{
  padding: 16px 0 12px 0;
}}
{p} .cc-card__note {{
  padding: 6px 0;
  font-size: 14px;
  line-height: 1.55;
}}
{p} .cc-card__footer {{
  padding: 12px 0 20px 0;
}}

/* ── 8. WP DECISION TABLE ── */
{p} .wp-block-table.is-style-stripes table {{
  border-collapse: collapse;
}}
{p} .wp-block-table.is-style-stripes table th {{
  font-size: 12px;
  font-weight: 600;
  padding: 14px 18px;
  background: #FAFAFA;
  color: #6E6E78;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}}
{p} .wp-block-table.is-style-stripes table td {{
  font-size: 15px;
  padding: 16px 18px;
  line-height: 1.55;
}}
{p} .wp-block-table.is-style-stripes tbody tr:nth-child(odd) {{
  background: #FDFCFE;
}}
{p} .wp-block-table.is-style-stripes tbody tr:nth-child(even) {{
  background: #fff;
}}

/* ── 9. METHODOLOGY ── */
{p} .wp-block-group.methodology {{
  border-color: #F0ECF4 !important;
  background: #FDFCFE !important;
  border-radius: 12px !important;
  padding: 24px 28px 32px !important;
  margin-top: 64px !important;
}}

/* ── 10. METADATA ── */
{p} .cc-hero-meta {{
  font-size: 14px;
  color: #8A8A94;
  letter-spacing: 0;
}}
{p} .cc-hero-meta strong {{
  color: #6E6E78;
  font-weight: 600;
}}

/* ── 12. FAQ ACCORDION ── */
{p} .cc-faq {{
  margin-top: 56px;
}}
{p} .cc-faq__list {{
  list-style: none;
  margin: 12px 0 0 0;
  padding: 0;
}}
{p} .cc-faq__item {{
  border-bottom: 1px solid #EEEAF2;
}}
{p} .cc-faq__question {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  width: 100%;
  padding: 20px 8px 20px 0;
  background: none;
  border: none;
  cursor: pointer;
  text-align: left;
  font-size: 16px;
  font-weight: 600;
  line-height: 1.45;
  color: #2A2A2E;
  transition: color 0.15s;
}}
{p} .cc-faq__question:hover {{
  color: #6704A4;
}}
{p} .cc-faq__question:focus-visible {{
  outline: 2px solid #6704A4;
  outline-offset: -2px;
  border-radius: 4px;
}}
{p} .cc-faq__item--open .cc-faq__question {{
  color: #6704A4;
  padding-bottom: 4px;
}}
{p} .cc-faq__icon {{
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6E6E78;
  transition: transform 0.25s ease, color 0.15s;
}}
{p} .cc-faq__icon svg {{
  width: 15px;
  height: 15px;
  stroke-width: 2;
}}
{p} .cc-faq__item--open .cc-faq__icon {{
  transform: rotate(90deg);
  color: #6704A4;
}}
{p} .cc-faq__answer {{
  display: none;
  padding: 8px 0 28px;
  font-size: 15.5px;
  line-height: 1.7;
  color: #4A4A52;
  max-width: 780px;
}}
{p} .cc-faq__answer p {{
  margin: 0 0 14px 0;
}}
{p} .cc-faq__answer p:last-child {{
  margin-bottom: 0;
}}
{p} .cc-faq__item--open .cc-faq__answer {{
  display: block;
}}

@media (max-width: 640px) {{
  {p} .cc-faq__question {{
    font-size: 15px;
    padding: 18px 0;
  }}
  {p} .cc-faq__item--open .cc-faq__question {{
    padding-bottom: 4px;
  }}
  {p} .cc-faq__answer {{
    padding: 0 0 18px;
    font-size: 14.5px;
  }}
}}
</style>"""

    return css


# ── Also-consider vertical list (brand_compare pages) ──────────────────

CC_ALSO_CONSIDER_VERTICAL_CSS = '''<style>
/* Also-consider: vertical list layout (brand comparison pages) */
.cc-hero-also {
  margin-top: 8px;
  padding-top: 0;
}
.cc-hero-also__label {
  margin-bottom: 16px;
  font-size: 10px;
  color: #B0ABB8;
  font-weight: 500;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}
.cc-hero-also__label::before {
  background: #D8D3DE;
}
.cc-hero-also__list {
  display: flex;
  flex-direction: column;
  gap: 0;
}
.cc-hero-also__row {
  display: grid;
  grid-template-columns: 56px 1fr auto auto;
  gap: 0 20px;
  align-items: center;
  padding: 18px 0;
  border-bottom: 1px solid #F0ECF4;
}
.cc-hero-also__row:last-child {
  border-bottom: none;
}
.cc-hero-also__thumb {
  width: 56px;
  height: 40px;
  border-radius: 6px;
  border: 1px solid #EEEAF2;
  background: #FCFBFD;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4px;
  flex-shrink: 0;
}
.cc-hero-also__thumb img {
  max-width: 100%;
  max-height: 32px;
  object-fit: contain;
}
.cc-hero-also__name {
  font-size: 15px;
  font-weight: 700;
  color: #2A2A2E;
  line-height: 1.25;
  margin-bottom: 2px;
}
.cc-hero-also__desc {
  font-size: 13px;
  color: #8A8A94;
  line-height: 1.35;
}
.cc-hero-also__tag {
  font-size: 11px;
  font-weight: 500;
  color: #8A8A94;
  background: #F5F3F7;
  padding: 3px 10px;
  border-radius: 4px;
  white-space: nowrap;
  flex-shrink: 0;
}
.cc-hero-also__link {
  font-size: 13px;
  font-weight: 600;
  color: #6704A4;
  text-decoration: none;
  white-space: nowrap;
  flex-shrink: 0;
}
.cc-hero-also__link:hover {
  color: #4F0280;
  text-decoration: underline;
}
@media (max-width: 640px) {
  .cc-hero-also__row {
    grid-template-columns: 48px 1fr;
    grid-template-rows: auto auto;
    gap: 4px 14px;
    padding: 14px 0;
  }
  .cc-hero-also__thumb {
    width: 48px;
    height: 34px;
    grid-row: 1 / 3;
  }
  .cc-hero-also__tag {
    grid-column: 2;
    justify-self: start;
    margin-top: 4px;
  }
  .cc-hero-also__link {
    grid-column: 2;
    justify-self: start;
    margin-top: 6px;
  }
}
</style>'''


# ── Tabbed product card CSS (brand_compare pages) ──────────────────────

CC_TABBED_CARD_CSS = '''<style>
/* Tabbed product card — editorial recommendation module with tabs */
.cc-tab-card {
  border: 1px solid #E8E2EF;
  border-radius: 14px;
  background: #fff;
  margin-top: 48px;
  margin-bottom: 48px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0,0,0,0.10);
}
.cc-tab-card__strip {
  background: #FDFCFE;
  border-bottom: 1px solid #F0ECF4;
  padding: 7px 32px;
  font-size: 11px;
  font-weight: 600;
  color: #6E6E78;
}
.cc-tab-card__header {
  display: grid;
  grid-template-columns: 100px 1fr auto;
  gap: 0 28px;
  align-items: center;
  padding: 26px 32px 18px;
}
.cc-tab-card__image {
  width: 100px;
  height: 72px;
  background: #FCFBFD;
  border-radius: 8px;
  border: 1px solid #EEEAF2;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6px;
}
.cc-tab-card__image img {
  max-width: 100%;
  max-height: 60px;
  object-fit: contain;
}
.cc-tab-card__identity h3 {
  font-size: 19px;
  font-weight: 700;
  line-height: 1.25;
  color: #2A2A2E;
  margin: 0 0 6px 0;
}
.cc-tab-card__summary {
  font-size: 15px;
  line-height: 1.55;
  color: #4A4A52;
  max-width: 480px;
}
.cc-tab-card__header-cta {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}
.cc-tab-card__cta {
  display: inline-block;
  padding: 9px 22px;
  background: #6704A4;
  color: #fff !important;
  font-size: 13px;
  font-weight: 600;
  border-radius: 7px;
  text-decoration: none;
  transition: background 0.15s;
  white-space: nowrap;
}
.cc-tab-card__cta:hover {
  background: #4F0280;
}
.cc-tab-card__stats {
  display: flex;
  gap: 0;
  margin: 0 32px;
  padding: 10px 0 14px 0;
  border-top: 1px solid #F0ECF4;
  border-bottom: 1px solid #F0ECF4;
}
.cc-tab-card__stat {
  flex: 1;
  padding: 0 14px 0 0;
}
.cc-tab-card__stat + .cc-tab-card__stat {
  border-left: 1px solid #F0ECF4;
  padding-left: 14px;
}
.cc-tab-card__stat-label {
  display: block;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #8A8A94;
  margin-bottom: 2px;
}
.cc-tab-card__stat-value {
  display: block;
  font-size: 13.5px;
  font-weight: 700;
  color: #2A2A2E;
  line-height: 1.35;
}
.cc-tab-card__tabs {
  display: flex;
  gap: 0;
  margin: 0 32px;
  padding-top: 6px;
  border-bottom: 1px solid #F0ECF4;
}
.cc-tab-card__tab {
  padding: 10px 20px;
  font-size: 13px;
  font-weight: 600;
  color: #8A8A94;
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  transition: color 0.15s, border-color 0.15s;
  white-space: nowrap;
}
.cc-tab-card__tab:hover {
  color: #4A4A52;
}
.cc-tab-card__tab:first-child {
  padding-left: 0;
}
.cc-tab-card__tab--active {
  color: #6704A4;
  border-bottom-color: #6704A4;
}
.cc-tab-card__tab:focus-visible {
  outline: 2px solid #6704A4;
  outline-offset: -2px;
  border-radius: 4px;
}
.cc-tab-card__panel {
  display: none;
  padding: 20px 32px 24px;
}
.cc-tab-card__panel--active {
  display: block;
}
.cc-tab-card__item {
  font-size: 14px;
  line-height: 1.55;
  color: #4A4A52;
  padding: 7px 0;
}
.cc-tab-card__item strong {
  color: #2A2A2E;
  font-weight: 700;
}
.cc-tab-card__detail-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  padding: 10px 0;
  border-bottom: 1px solid #F8F6FA;
}
.cc-tab-card__detail-row:last-child {
  border-bottom: none;
}
.cc-tab-card__detail-label {
  font-size: 13px;
  font-weight: 600;
  color: #6E6E78;
  flex-shrink: 0;
  width: 160px;
}
.cc-tab-card__detail-value {
  font-size: 14px;
  font-weight: 600;
  color: #2A2A2E;
  text-align: right;
  line-height: 1.45;
}
.cc-tab-card__qual {
  font-size: 11px;
  font-weight: 400;
  color: #8A8A94;
  display: block;
}
.cc-tab-card__footer {
  margin: 0 32px;
  padding: 10px 0 18px;
  border-top: 1px solid #F0ECF4;
}
.cc-tab-card__trust {
  font-size: 11px;
  color: #8A8A94;
  line-height: 1.4;
}
@media (max-width: 640px) {
  .cc-tab-card__header {
    grid-template-columns: 72px 1fr;
    grid-template-rows: auto auto;
    gap: 0 14px;
    padding: 18px 20px 14px;
  }
  .cc-tab-card__image {
    width: 72px;
    height: 52px;
    padding: 5px;
  }
  .cc-tab-card__header-cta {
    grid-column: 1 / -1;
    padding-top: 10px;
  }
  .cc-tab-card__cta {
    display: block;
    width: 100%;
    text-align: center;
  }
  .cc-tab-card__stats {
    flex-direction: column;
    margin: 0 20px;
  }
  .cc-tab-card__stat + .cc-tab-card__stat {
    border-left: none;
    border-top: 1px solid #F0ECF4;
    padding-left: 0;
    padding-top: 10px;
    margin-top: 10px;
  }
  .cc-tab-card__tabs {
    margin: 0 20px;
    overflow-x: auto;
  }
  .cc-tab-card__tab {
    padding: 10px 16px;
    font-size: 12px;
  }
  .cc-tab-card__panel {
    padding: 16px 20px 20px;
  }
  .cc-tab-card__detail-row {
    flex-direction: column;
    gap: 2px;
  }
  .cc-tab-card__detail-label {
    width: auto;
  }
  .cc-tab-card__detail-value {
    text-align: left;
  }
  .cc-tab-card__footer {
    margin: 0 20px;
  }
  .cc-tab-card__strip {
    padding: 6px 20px;
  }
}
</style>'''
