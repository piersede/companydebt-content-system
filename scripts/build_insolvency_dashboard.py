"""Assemble the UK Company Insolvency Statistics data hub draft.

Reads parsed JSON + chart SVGs and writes a WordPress block HTML draft to
drafts/77399_uk-insolvency-statistics.html. Re-runnable: re-parse the source
files then re-run this to refresh the page for a new monthly release.
"""

from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent

from build_insolvency_charts import build_all_charts, format_number, month_label

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "insolvency-statistics"
DRAFT_PATH = ROOT / "drafts" / "77399_uk-insolvency-statistics.html"

WP_TEMPLATE = "templates/take-the-test-template.php"
WP_POST_ID = 77399
WP_TITLE = "UK Company Insolvency Statistics 2026"
WP_SLUG = "uk-insolvency-statistics"
STAGING_LINK = "https://comdebstage.wpengine.com/uk-insolvency-statistics/"
META_DESCRIPTION = (
    "Monthly UK company insolvency statistics using Insolvency Service and Companies House "
    "data. Track CVLs, compulsory liquidations, administrations, insolvency rates and sector trends."
)


def load_data() -> dict:
    return {
        "metadata":  json.loads((DATA_DIR / "release_metadata.json").read_text(encoding="utf-8")),
        "monthly":   json.loads((DATA_DIR / "monthly_series.json").read_text(encoding="utf-8")),
        "rate":      json.loads((DATA_DIR / "rate_series.json").read_text(encoding="utf-8")),
        "sector":    json.loads((DATA_DIR / "sector_breakdown.json").read_text(encoding="utf-8")),
        "nations":   json.loads((DATA_DIR / "uk_nations.json").read_text(encoding="utf-8")),
    }


def fmt_pct(value):
    if value is None:
        return "n/a"
    sign = "+" if value > 0 else ""
    return f"{sign}{value}%"


def latest_table_row(row: dict) -> str:
    return (
        f'<tr>'
        f'<th scope="row">{row["procedure"]}</th>'
        f'<td class="cd-num">{format_number(row["latest"])}</td>'
        f'<td class="cd-num">{format_number(row["prior_month"])}</td>'
        f'<td class="cd-num">{format_number(row["prior_year"])}</td>'
        f'<td class="cd-num">{fmt_pct(row["month_change_pct"])}</td>'
        f'<td class="cd-num">{fmt_pct(row["year_change_pct"])}</td>'
        f'</tr>'
    )


# ── Hero ──────────────────────────────────────────────────────────────────

def hero_block(meta: dict, latest_total: int) -> str:
    """Wide 2-col hero. 60/40 split with confident H1 and large KPI panel."""
    return dedent(f"""\
    <section class="cd-section cd-w-wide cd-hero">
      <div class="cd-hero__copy">
        <p class="cd-eyebrow">Company insolvency statistics</p>
        <h1>UK Company Insolvency Statistics 2026</h1>
        <p class="cd-lede">There were {format_number(latest_total)} registered company insolvencies in England and Wales in {meta['latest_month_label']} — 2% higher than March 2026 and 3% higher than April 2025. The Insolvency Service publishes new figures monthly.</p>
        <dl class="cd-meta-row">
          <div><dt>Latest data</dt><dd>{meta['latest_month_label']}</dd></div>
          <div><dt>Published</dt><dd>{meta['publication_date']}</dd></div>
          <div><dt>Next release</dt><dd>{meta['next_release_date']}</dd></div>
          <div><dt>Source</dt><dd>{meta['source_label']}</dd></div>
        </dl>
        <p class="cd-status"><span class="cd-status__dot" aria-hidden="true"></span>{meta['status']}</p>
      </div>

      <aside class="cd-hero__panel" aria-label="Latest figures">
        <p class="cd-eyebrow">Latest figures · England and Wales</p>
        <div class="cd-primary-kpi">
          <div class="cd-primary-kpi__num">{format_number(latest_total)}</div>
          <div class="cd-primary-kpi__cap">company insolvencies, {meta['latest_month_label']}</div>
          <div class="cd-primary-kpi__delta">
            <span><span class="cd-delta-v">+2%</span> vs March 2026</span>
            <span><span class="cd-delta-v">+3%</span> vs April 2025</span>
          </div>
        </div>
        <div class="cd-mini-kpi-grid">
          <div class="cd-mini-kpi"><div class="cd-mini-kpi__v">1,510</div><div class="cd-mini-kpi__k">CVLs <span>72% of total</span></div></div>
          <div class="cd-mini-kpi"><div class="cd-mini-kpi__v">371</div><div class="cd-mini-kpi__k">Compulsory <span>+19% on March</span></div></div>
          <div class="cd-mini-kpi"><div class="cd-mini-kpi__v">183</div><div class="cd-mini-kpi__k">Administrations <span>incl. real-estate cluster</span></div></div>
          <div class="cd-mini-kpi"><div class="cd-mini-kpi__v">51.8</div><div class="cd-mini-kpi__k">Rate per 10,000 <span>1 in 193 companies</span></div></div>
        </div>
      </aside>
    </section>

    <nav class="cd-secnav cd-w-wide" aria-label="Page sections">
      <a href="#figures">Latest figures</a>
      <a href="#monthly">Monthly trend</a>
      <a href="#longrun">Long-run</a>
      <a href="#rate">Insolvency rate</a>
      <a href="#procedures">By procedure</a>
      <a href="#sector">Sector</a>
      <a href="#nations">UK nations</a>
      <a href="#method">Method</a>
      <a href="#source">Source</a>
    </nav>
    """)


# ── Latest figures table ──────────────────────────────────────────────────

def latest_figures_block(meta: dict) -> str:
    t = meta["latest_figures_table"]
    rows_html = "".join(latest_table_row(r) for r in t["rows"])
    return dedent(f"""\
    <section class="cd-section cd-w-standard" id="figures">
      <div class="cd-section-head">
        <p class="cd-eyebrow">Snapshot</p>
        <h2>Latest company insolvency figures</h2>
        <p class="cd-section-intro">The April 2026 total was made up mainly of creditors' voluntary liquidations. Administrations were higher than usual in March and April because around 200 connected real estate companies entered administration across those two months.</p>
      </div>
      <div class="cd-tablewrap">
        <table class="cd-table cd-table--latest">
          <caption class="cd-sr-only">Company insolvencies in England and Wales by procedure, {t['latest_month_label']} compared with March 2026 and April 2025. Seasonally adjusted where available.</caption>
          <thead>
            <tr>
              <th scope="col">Procedure</th>
              <th scope="col" class="cd-num">April 2026</th>
              <th scope="col" class="cd-num">March 2026</th>
              <th scope="col" class="cd-num">April 2025</th>
              <th scope="col" class="cd-num">Monthly change</th>
              <th scope="col" class="cd-num">Annual change</th>
            </tr>
          </thead>
          <tbody>
            {rows_html}
          </tbody>
        </table>
      </div>
      <p class="cd-source-note">Seasonally adjusted, England and Wales. Percentage changes not shown where both values are below five. Source: Insolvency Service / Companies House.</p>
    </section>
    """)


# ── Monthly chart panel ───────────────────────────────────────────────────

def monthly_chart_block(charts: dict) -> str:
    return dedent(f"""\
    <section class="cd-section cd-w-wide" id="monthly">
      <div class="cd-section-head cd-section-head--inline">
        <div>
          <p class="cd-eyebrow">Trend</p>
          <h2>Monthly company insolvencies by procedure</h2>
          <p class="cd-section-intro">CVLs remain the largest share of the total. Administrations were distorted by connected real-estate cases in March and April 2026.</p>
        </div>
        <div class="cd-chart-controls" role="tablist" aria-label="Time range">
          <span class="cd-chart-controls__label">View range</span>
          <button type="button" class="cd-chart-tab is-active" data-cd-view="post_covid" aria-pressed="true">Post-Covid</button>
          <button type="button" class="cd-chart-tab" data-cd-view="5y" aria-pressed="false">5 years</button>
          <button type="button" class="cd-chart-tab" data-cd-view="since_2000" aria-pressed="false">Since 2000</button>
        </div>
      </div>
      <div class="cd-chart-panel cd-chart-panel--hero">
        <div class="cd-chart-view is-active" data-cd-view-pane="post_covid">{charts['monthly_stacked_post_covid']}</div>
        <div class="cd-chart-view" data-cd-view-pane="5y" hidden>{charts['monthly_stacked_5y']}</div>
        <div class="cd-chart-view" data-cd-view-pane="since_2000" hidden>{charts['monthly_stacked_since_2000']}</div>
        <ul class="cd-legend" aria-label="Procedure colour legend">
          <li><span class="cd-legend__sw" style="background:#1d3557"></span>CVLs</li>
          <li><span class="cd-legend__sw" style="background:#a04646"></span>Compulsory liquidations</li>
          <li><span class="cd-legend__sw" style="background:#b87333"></span>Administrations</li>
          <li><span class="cd-legend__sw" style="background:#5a6373"></span>CVAs</li>
          <li><span class="cd-legend__sw" style="background:#b8bcc4"></span>Receiverships</li>
        </ul>
      </div>
      <p class="cd-source-note">England and Wales. CVLs, compulsory liquidations and administrations are seasonally adjusted where available. CVAs and receivership appointments are not seasonally adjusted due to low volumes. Source: Insolvency Service / Companies House.</p>
    </section>
    """)


# ── Long-run line chart panel with side notes ─────────────────────────────

def longrun_block(charts: dict) -> str:
    return dedent(f"""\
    <section class="cd-section cd-w-wide" id="longrun">
      <div class="cd-section-head">
        <p class="cd-eyebrow">Long-run</p>
        <h2>How company insolvencies have changed since 2000</h2>
        <p class="cd-section-intro">Volumes are now close to levels last seen around the 2008–09 recession. The rate is lower than the recession peak because the active company register has more than doubled since then.</p>
      </div>
      <div class="cd-longrun-grid">
        <div class="cd-chart-panel cd-chart-panel--longrun">
          {charts['longrun_total_line']}
        </div>
        <aside class="cd-side-notes" aria-label="Long-run key points">
          <div class="cd-side-note">
            <p class="cd-side-note__k">Peak</p>
            <p class="cd-side-note__v">2008–09 recession</p>
            <p class="cd-side-note__d">Highest monthly volumes in the modern series.</p>
          </div>
          <div class="cd-side-note">
            <p class="cd-side-note__k">Low point</p>
            <p class="cd-side-note__v">2020–21 Covid support</p>
            <p class="cd-side-note__d">Government support suppressed formal insolvencies sharply.</p>
          </div>
          <div class="cd-side-note">
            <p class="cd-side-note__k">Recent level</p>
            <p class="cd-side-note__v">Close to 2008–09 volumes</p>
            <p class="cd-side-note__d">But lower by rate — the company register has more than doubled.</p>
          </div>
        </aside>
      </div>
      <p class="cd-source-note">England and Wales, seasonally adjusted. Source: Insolvency Service / Companies House.</p>
    </section>
    """)


# ── Rate section: text + callout | chart (2-col, chart-dominant) ──────────

def rate_block(charts: dict, latest_rate: float) -> str:
    return dedent(f"""\
    <section class="cd-section cd-w-wide" id="rate">
      <div class="cd-section-head">
        <p class="cd-eyebrow">Rate</p>
        <h2>Company insolvency rate</h2>
      </div>
      <div class="cd-rate-grid">
        <div class="cd-rate-text">
          <p>In the 12 months to 30 April 2026, the company insolvency rate in England and Wales was {latest_rate} per 10,000 companies on the effective register. That is equal to one in 193 companies entering insolvency.</p>
          <p>The rate was slightly lower than the 52.5 per 10,000 recorded for the 12 months to April 2025, and has fallen from a post-pandemic peak of around 57.3 in late 2023.</p>
          <div class="cd-callout-card">
            <div class="cd-callout-card__row">
              <span class="cd-callout-card__k">April 2026</span>
              <span class="cd-callout-card__v">{latest_rate} <span class="cd-callout-card__u">per 10,000</span></span>
            </div>
            <div class="cd-callout-card__row">
              <span class="cd-callout-card__k">2008–09 peak</span>
              <span class="cd-callout-card__v">113.1 <span class="cd-callout-card__u">per 10,000</span></span>
            </div>
          </div>
          <p class="cd-rate-text__note">The rate is calculated on a 12-month rolling basis using company insolvencies and the average number of companies on the effective register.</p>
        </div>
        <div class="cd-chart-panel cd-chart-panel--rate">
          {charts['rate_line']}
        </div>
      </div>
      <p class="cd-source-note">Source: Insolvency Service / Companies House.</p>
    </section>
    """)


# ── Procedure card grid ───────────────────────────────────────────────────

def procedure_cards_block() -> str:
    rows = [
        ("CVLs", "1,510", "Main procedure. 72% of all insolvencies."),
        ("Compulsory liquidations", "371", "Up 19% on March 2026. HMRC-led petitions."),
        ("Administrations", "183", "Elevated by a real-estate cluster in March and April."),
        ("CVAs", "20", "Low by historical standards."),
        ("Receiverships", "1", "Now a rare procedure."),
    ]
    rows_html = "".join(
        f'<article class="cd-procard"><p class="cd-procard__name">{name}</p><p class="cd-procard__value">{count}</p><p class="cd-procard__note">{note}</p></article>'
        for name, count, note in rows
    )
    return dedent(f"""\
    <section class="cd-section cd-w-wide" id="procedures">
      <div class="cd-section-head">
        <p class="cd-eyebrow">By procedure</p>
        <h2>What's driving the total</h2>
      </div>
      <div class="cd-procard-grid">{rows_html}</div>
      <p class="cd-linkrow">
        <a href="https://companydebt.com/cvl-creditors-voluntary-liquidation/">About CVLs</a>
        <span aria-hidden="true">·</span>
        <a href="https://companydebt.com/administration/">About administration</a>
        <span aria-hidden="true">·</span>
        <a href="https://companydebt.com/compulsory-liquidation/">About compulsory liquidation</a>
      </p>
    </section>
    """)


# ── Sector section: table + chart (2-col) + caveat ────────────────────────

def sector_block(sector: dict, charts: dict) -> str:
    rows_data = [
        ("Construction", 3827, 16),
        ("Wholesale and retail trade; repair of motor vehicles and motorcycles", 3642, 16),
        ("Accommodation and food service activities", 3295, 14),
        ("Administrative and support service activities", 2374, 10),
        ("Professional, scientific and technical activities", 2002, 9),
        ("Manufacturing", 1876, 8),
    ]
    rows_html = "".join(
        f'<tr><th scope="row">{label}</th><td class="cd-num">{format_number(count)}</td><td class="cd-num">{share}%</td></tr>'
        for label, count, share in rows_data
    )
    return dedent(f"""\
    <section class="cd-section cd-w-wide" id="sector">
      <div class="cd-section-head">
        <p class="cd-eyebrow">Sector</p>
        <h2>Company insolvencies by industry</h2>
        <p class="cd-section-intro">Industry data is published one month behind the headline figures. The latest sector figures cover the 12 months to March 2026.</p>
      </div>
      <div class="cd-sector-grid">
        <div class="cd-tablewrap">
          <table class="cd-table cd-table--sector">
            <caption class="cd-sr-only">Company insolvencies by industry section, England and Wales, 12 months to March 2026.</caption>
            <thead>
              <tr>
                <th scope="col">Industry</th>
                <th scope="col" class="cd-num">12 months to March 2026</th>
                <th scope="col" class="cd-num">Share</th>
              </tr>
            </thead>
            <tbody>{rows_html}</tbody>
          </table>
        </div>
        <div class="cd-chart-panel cd-chart-panel--sector">
          {charts['sector_bars']}
        </div>
      </div>
      <aside class="cd-caveat">
        <p><strong>About sector volumes.</strong> These are volumes, not sector failure rates. Larger sectors tend to have more insolvencies because they have more registered companies. SIC codes are self-reported, and the first recorded SIC code is used.</p>
      </aside>
    </section>
    """)


# ── UK nations: standard container + side note card ───────────────────────

def nations_block(nations: dict) -> str:
    ew = nations["england_and_wales"]
    sc = nations["scotland"]
    ni = nations["northern_ireland"]
    rows = [
        ("England and Wales", ew["total"], ew["rate_per_10k"], "Seasonally adjusted headline count"),
        ("Scotland", sc["total"], sc["rate_per_10k"], "Not seasonally adjusted"),
        ("Northern Ireland", ni["total"], ni["rate_per_10k"], "Not seasonally adjusted"),
    ]
    rows_html = "".join(
        f'<tr><th scope="row">{name}</th><td class="cd-num">{format_number(total)}</td><td class="cd-num">{rate}</td><td>{note}</td></tr>'
        for name, total, rate, note in rows
    )
    return dedent(f"""\
    <section class="cd-section cd-w-standard" id="nations">
      <div class="cd-section-head">
        <p class="cd-eyebrow">UK nations</p>
        <h2>Company insolvencies across the UK</h2>
        <p class="cd-section-intro">Figures are reported separately for England and Wales, Scotland and Northern Ireland.</p>
      </div>
      <div class="cd-nations-grid">
        <div class="cd-tablewrap">
          <table class="cd-table cd-table--nations">
            <caption class="cd-sr-only">Company insolvencies by UK jurisdiction, April 2026.</caption>
            <thead>
              <tr>
                <th scope="col">Jurisdiction</th>
                <th scope="col" class="cd-num">April 2026</th>
                <th scope="col" class="cd-num">Rate per 10,000</th>
                <th scope="col">Notes</th>
              </tr>
            </thead>
            <tbody>{rows_html}</tbody>
          </table>
        </div>
        <aside class="cd-side-note cd-side-note--single">
          <p class="cd-side-note__k">Important note</p>
          <p class="cd-side-note__d">Scotland and Northern Ireland figures are not seasonally adjusted. Direct comparisons with England and Wales should account for this.</p>
        </aside>
      </div>
    </section>
    """)


# ── Methodology (full-bleed band) ─────────────────────────────────────────

def methodology_block() -> str:
    return dedent("""\
    <div class="cd-bleed cd-method-band">
      <section class="cd-method-inner" id="method">
        <div class="cd-section-head">
          <p class="cd-eyebrow">Method</p>
          <h2>How this data is measured</h2>
        </div>
        <p>Company insolvency data is sourced mainly from Companies House. Compulsory liquidation data for England and Wales comes from the Insolvency Service, and compulsory liquidation data for Northern Ireland comes from the Department for the Economy in Northern Ireland.</p>
        <p>The headline England and Wales figures use seasonally adjusted data where the Insolvency Service has identified seasonality. Scotland and Northern Ireland figures are shown on an unadjusted basis.</p>
        <p>The statistics count formal company insolvency procedures. They do not include members' voluntary liquidations, dissolutions or ordinary company closures.</p>
        <h3>Data limitations</h3>
        <ul class="cd-limits">
          <li>The latest month is provisional and can be revised.</li>
          <li>Sector data is published one month behind the headline figures.</li>
          <li>Industry is based on self-reported SIC codes.</li>
          <li>Registered office addresses are not a reliable guide to where a company traded.</li>
          <li>Solvent company closures are not included.</li>
        </ul>
      </section>
    </div>
    """)


# ── Source + citation (2-col card) ────────────────────────────────────────

def source_citation_block(meta: dict) -> str:
    citation = (
        "CompanyDebt. (2026). UK Company Insolvency Statistics 2026. CompanyDebt.com. "
        "Data sourced from the Insolvency Service and Companies House company insolvency statistics."
    )
    return dedent(f"""\
    <section class="cd-section cd-w-standard" id="source">
      <div class="cd-section-head">
        <p class="cd-eyebrow">Source</p>
        <h2>Source and citation</h2>
      </div>
      <div class="cd-cite-card">
        <div class="cd-cite-card__left">
          <dl>
            <dt>Primary source</dt><dd>Insolvency Service, Company Insolvency Statistics, April 2026.</dd>
            <dt>Supporting source</dt><dd>Companies House company register data.</dd>
            <dt>Publication date</dt><dd>{meta['publication_date']}</dd>
            <dt>Next scheduled release</dt><dd>{meta['next_release_date']}</dd>
            <dt>Status</dt><dd>{meta['status']}</dd>
          </dl>
        </div>
        <div class="cd-cite-card__right">
          <p class="cd-eyebrow">How to cite this page</p>
          <p class="cd-cite-text" id="cd-citation-text">{citation}</p>
          <button type="button" class="cd-cite-copy" aria-label="Copy citation to clipboard" data-cd-copy="#cd-citation-text">Copy citation</button>
        </div>
      </div>
    </section>
    """)


# ── Final CTA (full-bleed soft band) ──────────────────────────────────────

def final_cta_block() -> str:
    return dedent("""\
    <div class="cd-bleed cd-final-cta">
      <div class="cd-final-cta__inner">
        <div class="cd-final-cta__copy">
          <p class="cd-final-cta__head">Need company debt advice?</p>
          <p class="cd-final-cta__body">If your company is under creditor pressure, speak to a licensed insolvency adviser before the position worsens.</p>
        </div>
        <a class="cd-final-cta__btn" href="https://companydebt.com/contact-us/">Speak to an adviser</a>
      </div>
    </div>
    """)


# ── CSS ──────────────────────────────────────────────────────────────────

DASHBOARD_CSS = """
/* ============================================================
   COMPANY DEBT — UK INSOLVENCY DATA HUB
   Scoped under .cd-data-hub. Multi-width layout, panel-wrapped
   charts, restrained financial-report styling. Final-polish pass.
   ============================================================ */

.cd-data-hub {
  /* tokens */
  --cd-text: #101828;
  --cd-text-soft: #1f2937;
  --cd-muted: #667085;
  --cd-line: #e4e7ec;
  --cd-line-soft: #eef0f3;
  --cd-surface: #ffffff;
  --cd-surface-soft: #f8fafc;
  --cd-surface-band: #f6f8fb;
  --cd-cta-band: #f3f7fb;
  --cd-accent: #0f4c81;
  --cd-accent-soft: #e8f1f8;
  --cd-positive: #166534;
  --cd-positive-dot: #16a34a;
  --cd-cta-orange: #ec6608;

  --cd-shadow-panel: 0 16px 45px rgba(16, 24, 40, 0.06);
  --cd-shadow-hero: 0 18px 50px rgba(16, 24, 40, 0.08);

  --cd-space-section: 104px;
  --cd-space-section-small: 72px;

  --cd-radius-panel: 24px;
  --cd-radius-card: 18px;
  --cd-radius-hero: 22px;

  color: var(--cd-text);
  font-feature-settings: "tnum" 1, "ss01" 1;
  font-size: 17px;
  line-height: 1.65;
}

.cd-data-hub *, .cd-data-hub *::before, .cd-data-hub *::after { box-sizing: border-box; }
.cd-data-hub img, .cd-data-hub svg { max-width: 100%; }

/* ── Width containers ─────────────────────────────────────── */
.cd-data-hub .cd-w-narrow,
.cd-data-hub .cd-w-standard {
  margin-left: auto;
  margin-right: auto;
  padding-left: 24px;
  padding-right: 24px;
}
.cd-data-hub .cd-w-narrow   { max-width: 760px; }
.cd-data-hub .cd-w-standard { max-width: 1040px; }
/* Wide sections bleed out of the WP container so they can actually reach
   1280px on wide viewports. */
.cd-data-hub .cd-w-wide {
  width: 100vw;
  margin-left: calc(50% - 50vw);
  margin-right: calc(50% - 50vw);
  padding-left: max(24px, calc(50vw - 640px));
  padding-right: max(24px, calc(50vw - 640px));
}
/* Full-bleed band that escapes the parent .container. Inner content
   re-aligns to a 1280px max-width. */
.cd-data-hub .cd-bleed {
  width: 100vw;
  margin-left: calc(50% - 50vw);
  margin-right: calc(50% - 50vw);
  padding-left: max(24px, calc(50vw - 640px));
  padding-right: max(24px, calc(50vw - 640px));
}

/* ── Spacing rhythm ───────────────────────────────────────── */
.cd-data-hub .cd-section { margin-top: var(--cd-space-section); }
.cd-data-hub .cd-section-small { margin-top: var(--cd-space-section-small); }
.cd-data-hub > .cd-section:first-child,
.cd-data-hub > section.cd-hero { margin-top: 24px; }

/* ── Typography ───────────────────────────────────────────── */
.cd-data-hub h1 {
  font-size: clamp(44px, 5vw, 68px);
  line-height: 0.98;
  letter-spacing: -0.04em;
  font-weight: 700;
  margin: 0 0 1.25rem;
  max-width: 680px;
  color: var(--cd-text);
}
.cd-data-hub h2 {
  font-size: clamp(32px, 3.4vw, 44px);
  line-height: 1.08;
  letter-spacing: -0.025em;
  font-weight: 700;
  margin: 0;
  color: var(--cd-text);
}
.cd-data-hub h3 {
  font-size: 22px;
  line-height: 1.25;
  font-weight: 650;
  margin: 1.5em 0 0.6em;
  letter-spacing: -0.01em;
  color: var(--cd-text);
}
.cd-data-hub p { margin: 0 0 18px; color: var(--cd-text-soft); }
.cd-data-hub a { color: var(--cd-accent); text-decoration: none; }
.cd-data-hub a:hover { text-decoration: underline; text-underline-offset: 3px; }

.cd-data-hub .cd-lede {
  font-size: 20px;
  line-height: 1.55;
  color: var(--cd-text-soft);
  max-width: 660px;
  margin: 0 0 1.75rem;
}

.cd-data-hub .cd-eyebrow {
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  color: var(--cd-accent);
  margin: 0 0 14px;
  line-height: 1.2;
}

.cd-data-hub .cd-sr-only {
  position: absolute; width: 1px; height: 1px; padding: 0;
  margin: -1px; overflow: hidden; clip: rect(0,0,0,0); border: 0;
}

/* ── Section header ───────────────────────────────────────── */
.cd-data-hub .cd-section-head { margin-bottom: 32px; }
.cd-data-hub .cd-section-intro {
  font-size: 18px;
  line-height: 1.6;
  color: var(--cd-muted);
  max-width: 720px;
  margin: 16px 0 0;
}
.cd-data-hub .cd-section-head--inline {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 32px;
  align-items: end;
  margin-bottom: 28px;
}
@media (max-width: 880px) {
  .cd-data-hub .cd-section-head--inline { grid-template-columns: 1fr; align-items: start; }
}

/* ── Hero ─────────────────────────────────────────────────── */
.cd-data-hub .cd-hero {
  display: grid;
  grid-template-columns: minmax(0, 1.25fr) minmax(360px, 0.75fr);
  gap: 64px;
  align-items: start;
  padding-top: 56px;
  padding-bottom: 72px;
  border-bottom: 1px solid var(--cd-line);
  margin-top: 32px;
}
.cd-data-hub .cd-hero__copy { padding-right: 8px; }
.cd-data-hub .cd-meta-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 18px 32px;
  margin: 32px 0 16px;
  padding: 0;
}
.cd-data-hub .cd-meta-row > div { margin: 0; }
.cd-data-hub .cd-meta-row dt {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--cd-muted);
  font-weight: 600;
  margin: 0 0 5px;
}
.cd-data-hub .cd-meta-row dd { margin: 0; font-size: 15px; color: var(--cd-text); font-weight: 500; }
.cd-data-hub .cd-status {
  font-size: 14px;
  color: var(--cd-positive);
  margin: 0;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}
.cd-data-hub .cd-status__dot {
  display: inline-block; width: 8px; height: 8px;
  border-radius: 50%; background: var(--cd-positive-dot);
}

/* Hero KPI panel — primary number + 2x2 mini grid */
.cd-data-hub .cd-hero__panel {
  padding: 32px;
  background: var(--cd-surface);
  border: 1px solid var(--cd-line);
  border-radius: var(--cd-radius-hero);
  box-shadow: var(--cd-shadow-hero);
}
.cd-data-hub .cd-hero__panel .cd-eyebrow { color: var(--cd-muted); margin-bottom: 18px; }
.cd-data-hub .cd-primary-kpi {
  padding-bottom: 26px;
  margin-bottom: 26px;
  border-bottom: 1px solid var(--cd-line-soft);
}
.cd-data-hub .cd-primary-kpi__num {
  font-size: 56px;
  font-weight: 700;
  line-height: 1;
  letter-spacing: -0.03em;
  color: var(--cd-text);
  font-variant-numeric: tabular-nums;
}
.cd-data-hub .cd-primary-kpi__cap {
  font-size: 16px;
  color: var(--cd-text-soft);
  margin-top: 10px;
}
.cd-data-hub .cd-primary-kpi__delta {
  margin-top: 16px;
  font-size: 14px;
  color: var(--cd-muted);
  display: flex;
  flex-wrap: wrap;
  gap: 4px 20px;
}
.cd-data-hub .cd-delta-v { color: var(--cd-text); font-weight: 600; font-variant-numeric: tabular-nums; margin-right: 4px; }

.cd-data-hub .cd-mini-kpi-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 22px 28px;
}
.cd-data-hub .cd-mini-kpi { display: flex; flex-direction: column; gap: 4px; }
.cd-data-hub .cd-mini-kpi__v {
  font-size: 28px;
  font-weight: 650;
  line-height: 1.05;
  color: var(--cd-text);
  font-variant-numeric: tabular-nums;
  letter-spacing: -0.015em;
}
.cd-data-hub .cd-mini-kpi__k {
  font-size: 14px;
  color: var(--cd-text-soft);
  display: flex;
  flex-direction: column;
  gap: 2px;
  line-height: 1.35;
}
.cd-data-hub .cd-mini-kpi__k span {
  font-size: 12px;
  color: var(--cd-muted);
}

/* ── Sticky section nav ───────────────────────────────────── */
.cd-data-hub .cd-secnav {
  position: sticky;
  top: 0;
  z-index: 20;
  background: rgba(255, 255, 255, 0.94);
  backdrop-filter: saturate(180%) blur(8px);
  -webkit-backdrop-filter: saturate(180%) blur(8px);
  border-bottom: 1px solid var(--cd-line);
  margin-top: 24px;
  display: flex;
  flex-wrap: wrap;
  gap: 2px;
  font-size: 14px;
  padding-top: 10px;
  padding-bottom: 10px;
}
.cd-data-hub .cd-secnav a {
  color: var(--cd-muted);
  padding: 9px 16px;
  border-radius: 7px;
  line-height: 1.2;
  font-weight: 500;
  text-decoration: none;
}
.cd-data-hub .cd-secnav a:hover { color: var(--cd-text); background: var(--cd-surface-soft); text-decoration: none; }
.cd-data-hub .cd-secnav a.is-active { color: var(--cd-text); background: var(--cd-accent-soft); }
.cd-data-hub [id] { scroll-margin-top: 76px; }

/* ── Tables ───────────────────────────────────────────────── */
.cd-data-hub .cd-tablewrap {
  margin: 0;
  border: 1px solid var(--cd-line);
  border-radius: 20px;
  overflow: hidden;
  background: var(--cd-surface);
  box-shadow: var(--cd-shadow-panel);
}
.cd-data-hub .cd-table { width: 100%; border-collapse: collapse; font-size: 16px; }
.cd-data-hub .cd-table th,
.cd-data-hub .cd-table td { padding: 18px 22px; text-align: left; vertical-align: top; }
.cd-data-hub .cd-table thead th {
  background: #f7f8fa;
  font-weight: 650;
  color: var(--cd-text);
  font-size: 13px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  border-bottom: 1px solid var(--cd-line);
  white-space: nowrap;
}
.cd-data-hub .cd-table tbody tr + tr td,
.cd-data-hub .cd-table tbody tr + tr th { border-top: 1px solid var(--cd-line-soft); }
.cd-data-hub .cd-table th[scope="row"] { font-weight: 500; color: var(--cd-text); }
.cd-data-hub .cd-table .cd-num { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }

/* ── Chart panels ─────────────────────────────────────────── */
.cd-data-hub .cd-chart-panel {
  background: var(--cd-surface);
  border: 1px solid var(--cd-line);
  border-radius: var(--cd-radius-panel);
  padding: 36px 40px 30px;
  box-shadow: var(--cd-shadow-panel);
}
.cd-data-hub .cd-chart-panel--hero  { min-height: 480px; padding-bottom: 24px; }
.cd-data-hub .cd-chart-panel--longrun { min-height: 440px; }
.cd-data-hub .cd-chart-panel--rate { min-height: 380px; padding: 28px 32px 22px; }
.cd-data-hub .cd-chart-panel--sector { min-height: 360px; padding: 28px 28px 22px; }
.cd-data-hub .cd-chart-panel .cd-chart { width: 100%; height: auto; display: block; }

/* Chart controls (tab group) */
.cd-data-hub .cd-chart-controls {
  display: inline-flex;
  gap: 4px;
  align-items: center;
  padding: 4px;
  background: var(--cd-surface-soft);
  border: 1px solid var(--cd-line);
  border-radius: 12px;
}
.cd-data-hub .cd-chart-controls__label {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--cd-muted);
  padding: 0 12px 0 14px;
  font-weight: 700;
}
.cd-data-hub .cd-chart-tab {
  background: transparent;
  border: 1px solid transparent;
  padding: 8px 16px;
  font-size: 14px;
  border-radius: 8px;
  cursor: pointer;
  color: var(--cd-text);
  font-weight: 500;
  line-height: 1.2;
}
.cd-data-hub .cd-chart-tab:hover { background: rgba(15, 23, 42, 0.05); }
.cd-data-hub .cd-chart-tab.is-active {
  background: var(--cd-surface);
  color: var(--cd-text);
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.08), 0 0 0 1px var(--cd-line);
}

/* Legend */
.cd-data-hub .cd-legend {
  list-style: none;
  padding: 16px 0 0;
  margin: 18px 0 0;
  border-top: 1px solid var(--cd-line-soft);
  display: flex;
  flex-wrap: wrap;
  gap: 12px 26px;
  font-size: 14px;
  color: var(--cd-text-soft);
}
.cd-data-hub .cd-legend li { display: flex; align-items: center; gap: 8px; }
.cd-data-hub .cd-legend__sw { display: inline-block; width: 11px; height: 11px; border-radius: 3px; }

/* Source note */
.cd-data-hub .cd-source-note {
  font-size: 13px;
  color: var(--cd-muted);
  margin: 14px 0 0;
  line-height: 1.55;
}

/* ── Long-run section (75/25 chart + side notes) ──────────── */
.cd-data-hub .cd-longrun-grid {
  display: grid;
  grid-template-columns: minmax(0, 3fr) minmax(240px, 1fr);
  gap: 32px;
  align-items: start;
}
@media (max-width: 1020px) {
  .cd-data-hub .cd-longrun-grid { grid-template-columns: 1fr; }
}
.cd-data-hub .cd-side-notes {
  display: flex;
  flex-direction: column;
  gap: 22px;
  padding: 8px 0;
}
.cd-data-hub .cd-side-note {
  border-left: 3px solid var(--cd-accent);
  padding-left: 18px;
}
.cd-data-hub .cd-side-note__k {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.09em;
  color: var(--cd-accent);
  font-weight: 700;
  margin: 0 0 6px;
}
.cd-data-hub .cd-side-note__v {
  font-size: 17px;
  font-weight: 650;
  color: var(--cd-text);
  margin: 0 0 6px;
  line-height: 1.3;
  letter-spacing: -0.005em;
}
.cd-data-hub .cd-side-note__d {
  font-size: 14px;
  color: var(--cd-muted);
  margin: 0;
  line-height: 1.55;
}

/* ── Rate section (text + callout / chart) ────────────────── */
.cd-data-hub .cd-rate-grid {
  display: grid;
  grid-template-columns: minmax(360px, 0.85fr) minmax(560px, 1.15fr);
  gap: 48px;
  align-items: start;
}
.cd-data-hub .cd-rate-text p { font-size: 17px; line-height: 1.65; }
.cd-data-hub .cd-rate-text__note {
  font-size: 13px;
  color: var(--cd-muted);
  margin-top: 16px;
}
.cd-data-hub .cd-callout-card {
  margin: 24px 0 16px;
  background: var(--cd-accent-soft);
  border-radius: var(--cd-radius-card);
  padding: 24px 26px;
  display: grid;
  gap: 18px;
}
.cd-data-hub .cd-callout-card__row { display: grid; grid-template-columns: 1fr auto; align-items: baseline; gap: 18px; }
.cd-data-hub .cd-callout-card__k {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.09em;
  color: var(--cd-accent);
  font-weight: 700;
}
.cd-data-hub .cd-callout-card__v {
  font-size: 34px;
  font-weight: 700;
  color: var(--cd-text);
  font-variant-numeric: tabular-nums;
  letter-spacing: -0.015em;
  line-height: 1.05;
}
.cd-data-hub .cd-callout-card__u { font-size: 13px; color: var(--cd-muted); font-weight: 500; margin-left: 4px; }
@media (max-width: 1020px) {
  .cd-data-hub .cd-rate-grid { grid-template-columns: 1fr; gap: 28px; }
  .cd-data-hub .cd-chart-panel--rate { min-height: 320px; }
}

/* ── Procedure card grid ──────────────────────────────────── */
.cd-data-hub .cd-procard-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 18px;
}
.cd-data-hub .cd-procard {
  padding: 24px;
  border-radius: 18px;
  background: var(--cd-surface);
  border: 1px solid var(--cd-line);
  box-shadow: 0 4px 14px rgba(16, 24, 40, 0.03);
}
.cd-data-hub .cd-procard__name {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--cd-muted);
  font-weight: 700;
  margin: 0 0 8px;
  line-height: 1.3;
}
.cd-data-hub .cd-procard__value {
  font-size: 32px;
  font-weight: 700;
  line-height: 1.05;
  color: var(--cd-text);
  font-variant-numeric: tabular-nums;
  letter-spacing: -0.02em;
  margin: 0 0 10px;
}
.cd-data-hub .cd-procard__note {
  font-size: 14px;
  color: var(--cd-muted);
  margin: 0;
  line-height: 1.5;
}
.cd-data-hub .cd-linkrow {
  margin: 24px 0 0;
  font-size: 14px;
  color: var(--cd-muted);
}
.cd-data-hub .cd-linkrow a { color: var(--cd-accent); }
.cd-data-hub .cd-linkrow span { margin: 0 8px; }
@media (max-width: 980px) { .cd-data-hub .cd-procard-grid { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 720px) { .cd-data-hub .cd-procard-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 480px) { .cd-data-hub .cd-procard-grid { grid-template-columns: 1fr; } }

/* ── Sector grid ──────────────────────────────────────────── */
.cd-data-hub .cd-sector-grid {
  display: grid;
  grid-template-columns: minmax(520px, 0.95fr) minmax(480px, 1.05fr);
  gap: 48px;
  align-items: start;
}
@media (max-width: 1100px) {
  .cd-data-hub .cd-sector-grid { grid-template-columns: 1fr; gap: 28px; }
}
.cd-data-hub .cd-caveat {
  margin-top: 32px;
  background: var(--cd-surface-band);
  border-left: 3px solid var(--cd-accent);
  border-radius: 12px;
  padding: 20px 24px;
}
.cd-data-hub .cd-caveat p { margin: 0; font-size: 15px; color: var(--cd-text-soft); line-height: 1.6; }

/* ── UK nations grid (table + side note) ──────────────────── */
.cd-data-hub .cd-nations-grid {
  display: grid;
  grid-template-columns: minmax(0, 2.4fr) minmax(240px, 1fr);
  gap: 32px;
  align-items: start;
}
@media (max-width: 880px) {
  .cd-data-hub .cd-nations-grid { grid-template-columns: 1fr; }
}
.cd-data-hub .cd-side-note--single {
  padding: 20px 22px;
  background: var(--cd-surface-band);
  border-left: 3px solid var(--cd-accent);
  border-radius: 12px;
}

/* ── Methodology band ─────────────────────────────────────── */
.cd-data-hub .cd-method-band {
  margin-top: var(--cd-space-section);
  padding-top: 96px;
  padding-bottom: 96px;
  background: var(--cd-surface-band);
  border-top: 1px solid var(--cd-line);
  border-bottom: 1px solid var(--cd-line);
}
.cd-data-hub .cd-method-inner { max-width: 760px; margin: 0 auto; }
.cd-data-hub .cd-method-inner p { color: var(--cd-text-soft); font-size: 17px; }
.cd-data-hub .cd-limits { padding-left: 1.25em; margin: 8px 0 0; }
.cd-data-hub .cd-limits li { margin: 10px 0; color: var(--cd-text-soft); font-size: 16px; }

/* ── Citation card ────────────────────────────────────────── */
.cd-data-hub .cd-cite-card {
  display: grid;
  grid-template-columns: 1fr 1fr;
  border: 1px solid var(--cd-line);
  border-radius: var(--cd-radius-panel);
  overflow: hidden;
  background: var(--cd-surface);
  box-shadow: var(--cd-shadow-panel);
}
.cd-data-hub .cd-cite-card > div { padding: 36px; }
.cd-data-hub .cd-cite-card > div + div {
  border-left: 1px solid var(--cd-line);
  background: var(--cd-surface-soft);
}
.cd-data-hub .cd-cite-card dl { margin: 0; display: grid; grid-template-columns: auto 1fr; gap: 12px 24px; font-size: 15px; }
.cd-data-hub .cd-cite-card dt { color: var(--cd-muted); font-weight: 600; }
.cd-data-hub .cd-cite-card dd { margin: 0; color: var(--cd-text); }
.cd-data-hub .cd-cite-card__right .cd-eyebrow { margin-bottom: 16px; color: var(--cd-accent); }
.cd-data-hub .cd-cite-text { font-size: 15px; line-height: 1.6; color: var(--cd-text-soft); margin-bottom: 20px; }
.cd-data-hub .cd-cite-copy {
  background: var(--cd-text);
  border: 1px solid var(--cd-text);
  color: var(--cd-surface);
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
}
.cd-data-hub .cd-cite-copy:hover { background: #000; }
.cd-data-hub .cd-cite-copy.is-copied { background: var(--cd-accent); border-color: var(--cd-accent); }
@media (max-width: 820px) {
  .cd-data-hub .cd-cite-card { grid-template-columns: 1fr; }
  .cd-data-hub .cd-cite-card > div + div { border-left: 0; border-top: 1px solid var(--cd-line); }
}

/* ── Final CTA (full-bleed soft band) ─────────────────────── */
.cd-data-hub .cd-final-cta {
  margin-top: 96px;
  padding-top: 56px;
  padding-bottom: 56px;
  background: var(--cd-cta-band);
  border-top: 1px solid #e4ecf3;
}
.cd-data-hub .cd-final-cta__inner {
  max-width: 1040px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: minmax(0, 1.5fr) auto;
  gap: 32px;
  align-items: center;
}
.cd-data-hub .cd-final-cta__head {
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--cd-muted);
  font-weight: 700;
  margin: 0 0 8px;
}
.cd-data-hub .cd-final-cta__body {
  font-size: 19px;
  color: var(--cd-text);
  margin: 0;
  line-height: 1.5;
  font-weight: 500;
  max-width: 620px;
}
.cd-data-hub .cd-final-cta__btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 14px 28px;
  background: var(--cd-cta-orange);
  color: #fff;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  white-space: nowrap;
  text-decoration: none;
  box-shadow: 0 6px 16px rgba(236, 102, 8, 0.18);
}
.cd-data-hub .cd-final-cta__btn:hover { background: #d65906; text-decoration: none; color: #fff; }
@media (max-width: 760px) {
  .cd-data-hub .cd-final-cta__inner { grid-template-columns: 1fr; gap: 20px; }
}

/* ── Mobile layout adjustments ───────────────────────────── */
@media (max-width: 980px) {
  .cd-data-hub .cd-hero { grid-template-columns: 1fr; gap: 40px; padding-top: 32px; padding-bottom: 48px; }
  .cd-data-hub .cd-hero__copy { padding-right: 0; }
  .cd-data-hub h1 { font-size: clamp(36px, 7vw, 48px); }
  .cd-data-hub .cd-section { margin-top: 72px; }
  .cd-data-hub .cd-method-band { padding-top: 64px; padding-bottom: 64px; }
  .cd-data-hub .cd-final-cta { padding-top: 40px; padding-bottom: 40px; margin-top: 64px; }
}
@media (max-width: 720px) {
  .cd-data-hub .cd-mini-kpi-grid { grid-template-columns: 1fr 1fr; }
  .cd-data-hub .cd-meta-row { grid-template-columns: 1fr 1fr; }
  .cd-data-hub .cd-secnav { overflow-x: auto; flex-wrap: nowrap; padding-left: 16px; padding-right: 16px; }
  .cd-data-hub .cd-secnav a { white-space: nowrap; }
  .cd-data-hub .cd-tablewrap { overflow-x: auto; }
  .cd-data-hub .cd-table { min-width: 560px; }
  .cd-data-hub .cd-table th, .cd-data-hub .cd-table td { padding: 14px 16px; }
  .cd-data-hub .cd-chart-panel { padding: 20px 18px 16px; }
  .cd-data-hub .cd-cite-card dl { grid-template-columns: 1fr; gap: 4px 0; }
  .cd-data-hub .cd-cite-card dl dd { margin-bottom: 12px; }
}
@media (max-width: 520px) {
  .cd-data-hub .cd-w-narrow, .cd-data-hub .cd-w-standard { padding-left: 16px; padding-right: 16px; }
  .cd-data-hub .cd-w-wide, .cd-data-hub .cd-bleed { padding-left: 16px; padding-right: 16px; }
  .cd-data-hub .cd-mini-kpi-grid { grid-template-columns: 1fr; }
  .cd-data-hub .cd-hero__panel { padding: 24px; }
  .cd-data-hub .cd-primary-kpi__num { font-size: 44px; }
}
"""


def assemble_draft() -> str:
    d = load_data()
    charts = build_all_charts(DATA_DIR)
    meta = d["metadata"]
    monthly = d["monthly"]
    latest_total = monthly["series"]["total"][-1]
    latest_rate  = d["rate"]["rate_per_10k"][-1]

    # NB: dashboard JS is injected by the mu-plugin.
    # Related guidance block intentionally removed — this is a stats page,
    # not an advice hub.
    body = "\n".join([
        f'<style>{DASHBOARD_CSS}</style>',
        '<div class="cd-data-hub">',
        hero_block(meta, latest_total),
        latest_figures_block(meta),
        monthly_chart_block(charts),
        longrun_block(charts),
        rate_block(charts, latest_rate),
        procedure_cards_block(),
        sector_block(d["sector"], charts),
        nations_block(d["nations"]),
        methodology_block(),
        source_citation_block(meta),
        final_cta_block(),
        '</div>',
    ])

    metadata_comments = (
        f"<!-- TITLE: {WP_TITLE} -->\n"
        f"<!-- POST ID: {WP_POST_ID} / TYPE: pages / AUTHOR: 34 / FM: 0 / TEMPLATE: {WP_TEMPLATE} -->\n"
        f"<!-- LINK: {STAGING_LINK} -->\n"
        f"<!-- META_DESC: {META_DESCRIPTION} -->\n\n"
    )
    return metadata_comments + "<!-- wp:html -->\n" + body + "\n<!-- /wp:html -->\n"


def main() -> int:
    DRAFT_PATH.parent.mkdir(parents=True, exist_ok=True)
    DRAFT_PATH.write_text(assemble_draft(), encoding="utf-8")
    size = DRAFT_PATH.stat().st_size
    print(f"Wrote draft: {DRAFT_PATH}")
    print(f"Size: {size:,} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
