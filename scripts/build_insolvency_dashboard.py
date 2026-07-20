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

# Logos for the masthead/source strip live in the active theme so they survive
# content rewrites (KSES leaves <img> alone; the files are deployed via SFTP).
THEME_ASSETS = "/wp-content/themes/company-debt-webpigment/assets/data-hub"

WP_TEMPLATE = "templates/take-the-test-template.php"
WP_POST_ID = 77399
WP_TITLE = "UK Company Insolvency Statistics 2026"
WP_SLUG = "uk-insolvency-statistics"
STAGING_LINK = "https://comdebstage.wpengine.com/data/uk-insolvency-statistics/"
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
    """Wide 2-col hero. Title block left, fixed-width KPI card right.
    Both sit inside the shared cd-w-hero container so they align with the
    breadcrumb/byline rendered by the PHP template."""
    return dedent(f"""\
    <section class="cd-w-hero">
      <a class="cd-back" href="/data/"><span aria-hidden="true">&larr;</span> UK Company Insolvency Data</a>
      <div class="cd-hero">
      <div class="cd-hero__copy">
        <h1><span class="cd-h1__line">UK Company Insolvency</span> <span class="cd-h1__line">Statistics 2026</span></h1>
        <p class="cd-lede">The Insolvency Service's {meta['latest_month_label']} release records {format_number(latest_total)} company insolvencies in England and Wales. That was 10% lower than April 2026 and 16% lower than May 2025. This page tracks the headline figures, the 12-month rolling rate and business insolvency statistics by sector, updated with each monthly release.</p>
        <dl class="cd-meta-grid">
          <div class="cd-meta-item"><span>Latest data</span><strong>{meta['latest_month_label']}</strong></div>
          <div class="cd-meta-item"><span>Published</span><strong>{meta['publication_date']}</strong></div>
          <div class="cd-meta-item"><span>Next release</span><strong>{meta['next_release_date']}</strong></div>
          <div class="cd-meta-item"><span>Source</span><strong>{meta['source_label']}</strong></div>
        </dl>
        <p class="cd-official-badge"><span aria-hidden="true"></span>{meta['status']}</p>
      </div>

      <aside class="cd-hero__panel" aria-label="Latest figures">
        <p class="cd-kpi-label">Latest figures · England and Wales</p>
        <div class="cd-main-kpi">
          <span class="cd-main-kpi__v">{format_number(latest_total)}</span>
          <span class="cd-main-kpi__k">company insolvencies, {meta['latest_month_label']}</span>
        </div>
        <div class="cd-change-row cd-change-row--down">
          <span><strong>-10%</strong> vs April 2026</span>
          <span><strong>-16%</strong> vs May 2025</span>
        </div>
        <div class="cd-kpi-divider" aria-hidden="true"></div>
        <div class="cd-mini-kpi-grid">
          <div class="cd-mini-kpi"><span class="cd-mini-kpi__v">1,423</span><span class="cd-mini-kpi__k">CVLs</span><span class="cd-mini-kpi__n">76% of total</span></div>
          <div class="cd-mini-kpi"><span class="cd-mini-kpi__v">285</span><span class="cd-mini-kpi__k">Compulsory</span><span class="cd-mini-kpi__n">-26% on April</span></div>
          <div class="cd-mini-kpi"><span class="cd-mini-kpi__v">135</span><span class="cd-mini-kpi__k">Administrations</span><span class="cd-mini-kpi__n">-24% on April</span></div>
          <div class="cd-mini-kpi"><span class="cd-mini-kpi__v">50.9</span><span class="cd-mini-kpi__k">Rate per 10,000</span><span class="cd-mini-kpi__n">1 in 196 companies</span></div>
        </div>
      </aside>
      </div>
    </section>
    """)


def secnav_block() -> str:
    """In-page section navigation. Sits below the source strip, above the
    first section, matching the design order: masthead, hero, sources, nav."""
    return dedent("""\
    <nav class="cd-secnav cd-w-wide" aria-label="Page sections">
      <a href="#figures">Latest figures</a>
      <a href="#monthly">Monthly trend</a>
      <a href="#longrun">Long-run</a>
      <a href="#rate">Insolvency rate</a>
      <a href="#sector">Sector</a>
      <a href="#sector-pages">Trade data</a>
      <a href="#nations">UK nations</a>
      <a href="#method">Method</a>
      <a href="#source">Source</a>
      <a href="#faq">FAQ</a>
    </nav>
    """)


def masthead_block() -> str:
    """Shared data-hub identity bar: CompanyDebt brand lockup + inter-page nav.
    The brand links back to the hub landing page; the nav is the shared data-hub
    menu (this is the Insolvency Statistics tab). Mirrors the masthead on the
    sibling data pages so the whole hub reads as one product with one menu."""
    return dedent("""\
    <div class="cd-masthead cd-w-wide">
      <a class="cd-brand" href="/data/">
        <span class="cd-brand__mark" aria-hidden="true">CD</span>
        <span class="cd-brand__name">CompanyDebt</span>
        <span class="cd-brand__sub">Insolvency Data Hub</span>
      </a>
      <nav class="cd-mastnav" aria-label="Data hub pages"><a href="/data/uk-insolvency-statistics/" aria-current="page">Insolvency Statistics</a><a href="/data/winding-up-petition-tracker/">Petition Tracker</a><a href="/data/dissolutions-vs-insolvencies/">Dissolutions</a><a href="/data/payment-practices-late-payment/">Late Payment</a></nav>
    </div>
    """)


def srcstrip_block() -> str:
    """Data-sources logo strip. Logos are served from the theme (THEME_ASSETS)
    so a content rewrite can never strip or relink them."""
    return dedent(f"""\
    <div class="cd-w-wide" style="margin-top:8px;margin-bottom:8px">
      <div class="cd-srcstrip">
        <span class="cd-srcstrip__label">Data sources</span>
        <div class="cd-srcstrip__logos">
          <figure class="cd-srclogo"><img src="{THEME_ASSETS}/logo-insolvency-service-trim.png" alt="The Insolvency Service logo"></figure>
          <figure class="cd-srclogo"><img src="{THEME_ASSETS}/logo-companies-house-trim.png" alt="Companies House logo"></figure>
        </div>
      </div>
    </div>
    """)


# ── Latest figures table ──────────────────────────────────────────────────

def latest_figures_block(meta: dict) -> str:
    t = meta["latest_figures_table"]
    rows_html = "".join(latest_table_row(r) for r in t["rows"])
    return dedent(f"""\
    <section class="cd-section cd-w-standard" id="figures">
      <div class="cd-section-head">
        <p class="cd-eyebrow">Snapshot <span>· May 2026</span></p>
        <h2>Latest UK company insolvency figures</h2>
        <p class="cd-section-intro">The May 2026 total was made up mainly of creditors' voluntary liquidations, and fell back across every main procedure. Administrations were 24% lower than in April, when more than 70 connected real estate companies entered insolvency in a single cluster.</p>
      </div>
      <div class="cd-tablewrap">
        <table class="cd-table cd-table--latest">
          <caption class="cd-table__caption">Company insolvencies in England and Wales by procedure, May 2026 compared with April 2026 and May 2025. Seasonally adjusted where available. Source: Insolvency Service / Companies House.</caption>
          <thead>
            <tr>
              <th scope="col">Procedure</th>
              <th scope="col" class="cd-num">May 2026</th>
              <th scope="col" class="cd-num">April 2026</th>
              <th scope="col" class="cd-num">May 2025</th>
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
          <p class="cd-section-intro">CVLs remain the largest share of the total. Administrations dropped back in May after a connected real-estate cluster lifted the April figure.</p>
        </div>
        <div class="cd-chart-controls" role="tablist" aria-label="Time range">
          <span class="cd-chart-controls__label">View range</span>
          <button type="button" class="cd-chart-tab is-active" data-cd-view="post_covid" aria-pressed="true">Post-Covid</button>
          <button type="button" class="cd-chart-tab" data-cd-view="5y" aria-pressed="false">5 years</button>
          <button type="button" class="cd-chart-tab" data-cd-view="since_2000" aria-pressed="false">Since 2000</button>
        </div>
      </div>
      <figure class="cd-chart-figure">
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
        <figcaption class="cd-figcaption"><strong>Monthly UK company insolvencies by procedure, England and Wales.</strong> CVLs, compulsory liquidations and administrations are seasonally adjusted where available; CVAs and receivership appointments are not seasonally adjusted due to low volumes. Source: Insolvency Service / Companies House.</figcaption>
      </figure>
    </section>
    """)


# ── Long-run line chart panel with side notes ─────────────────────────────

def longrun_block(charts: dict) -> str:
    return dedent(f"""\
    <section class="cd-section cd-w-wide" id="longrun">
      <div class="cd-section-head">
        <p class="cd-eyebrow">Long-run</p>
        <h2>Long-run UK company insolvency trends since 2000</h2>
        <p class="cd-section-intro">Volumes are now close to levels last seen around the 2008–09 recession. The rate is lower than the recession peak because the active company register has more than doubled since then.</p>
      </div>
      <div class="cd-longrun-grid">
        <figure class="cd-chart-figure">
          <div class="cd-chart-panel cd-chart-panel--longrun">
            {charts['longrun_total_line']}
          </div>
          <figcaption class="cd-figcaption"><strong>Total monthly UK company insolvencies, England and Wales, 2000–2026.</strong> Seasonally adjusted. Vertical markers note the 2008–09 recession peak, the 2020–21 Covid support period and the post-Covid CVL peak. Source: Insolvency Service / Companies House.</figcaption>
        </figure>
        <aside class="cd-side-notes" aria-label="Key context">
          <h3 class="cd-side-notes__title">What this means</h3>
          <p class="cd-side-note__d">Current volumes are roughly equal to 2008–09 recession levels, but the insolvency rate is half that recession peak, because the active company register has more than doubled since.</p>
          <p class="cd-side-note__d">The 2020–21 dip is the Covid support effect, not a real improvement in trading conditions: government support suppressed formal procedures sharply, then volumes rebounded.</p>
          <p class="cd-side-note__d">The 2022–24 climb tracks the unwinding of Covid support, HMRC's return to active enforcement, and a wave of CVL filings catching up with companies that had stopped trading earlier.</p>
        </aside>
      </div>
    </section>
    """)


# ── Rate section: text + callout | chart (2-col, chart-dominant) ──────────

def rate_block(charts: dict, latest_rate: float) -> str:
    return dedent(f"""\
    <section class="cd-section cd-w-wide" id="rate">
      <div class="cd-section-head">
        <p class="cd-eyebrow">Rate <span>· 12-month rolling</span></p>
        <h2>UK company insolvency rate (May 2026)</h2>
      </div>
      <div class="cd-rate-grid">
        <div class="cd-rate-text">
          <p class="cd-section-intro">In the 12 months to 31 May 2026, the company insolvency rate in England and Wales was {latest_rate} per 10,000 companies on the effective register. That is equal to one in 196 companies entering insolvency.</p>
          <p>The rate was lower than the 53.0 per 10,000 recorded for the 12 months to May 2025, and has fallen from a post-pandemic peak of around 57.3 in late 2023.</p>
          <div class="cd-callout-card">
            <div class="cd-callout-card__row">
              <span class="cd-callout-card__k">May 2026</span>
              <span class="cd-callout-card__v">{latest_rate} <span class="cd-callout-card__u">per 10,000</span></span>
            </div>
            <div class="cd-callout-card__row">
              <span class="cd-callout-card__k">2008–09 peak</span>
              <span class="cd-callout-card__v">113.1 <span class="cd-callout-card__u">per 10,000</span></span>
            </div>
          </div>
          <p class="cd-rate-text__note">The rate is calculated on a 12-month rolling basis using company insolvencies and the average number of companies on the effective register.</p>
        </div>
        <figure class="cd-chart-figure">
          <div class="cd-chart-panel cd-chart-panel--rate">
            {charts['rate_line']}
          </div>
          <figcaption class="cd-figcaption"><strong>12-month rolling UK company insolvency rate per 10,000 active companies, England and Wales.</strong> Calculated using company insolvencies and the average number of companies on the effective register. Source: Insolvency Service / Companies House.</figcaption>
        </figure>
      </div>
    </section>
    """)


# Procedure card grid removed per the 2026-07 flagship redesign (see
# docs/data-hub/design-brief-2026-07.md): a statistics page's job is not to
# route readers off to procedure guides, and the KPI panel in the hero
# already carries CVL/compulsory/administration counts. Its figures were also
# hardcoded placeholders (1,423 CVLs, a fixed "May 2026" label) never wired to
# real data. CVL, compulsory liquidation and administration statistics remain
# linked from the /data/ hub's "Formal statistics" group, so no page is
# orphaned by this removal.


# ── Sector section: table + chart (2-col) + caveat ────────────────────────

def sector_block(sector: dict, charts: dict) -> str:
    return dedent(f"""\
    <section class="cd-section cd-w-wide" id="sector">
      <div class="cd-section-head">
        <p class="cd-eyebrow">Sector <span>· 12 months to May 2026</span></p>
        <h2>UK company insolvencies by sector</h2>
        <p class="cd-section-intro">The sector breakdown covers the 12 months to May 2026, ranked by volume. Construction remains the largest, ahead of wholesale and retail and accommodation and food. The full ranking and year-by-year trends are in the <a href="/data/company-insolvencies-by-sector/">company insolvencies by sector</a> data, including the <a href="/data/construction-insolvency-statistics/">construction insolvency statistics</a>.</p>
      </div>
      <figure class="cd-chart-figure">
        <div class="cd-chart-panel cd-chart-panel--sector">
          {charts['sector_bars']}
        </div>
        <figcaption class="cd-figcaption"><strong>UK company insolvencies by industry section, 12 months to May 2026, England and Wales.</strong> Ranked by volume. SIC code is self-reported and uses the first recorded code. Source: Insolvency Service / Companies House.</figcaption>
      </figure>
      <aside class="cd-caveat">
        <p><strong>About sector volumes.</strong> These are volumes, not sector failure rates. Larger sectors tend to have more insolvencies because they have more registered companies. SIC codes are self-reported, and the first recorded SIC code is used.</p>
      </aside>
    </section>
    """)


# ── Trade data-page links: registry-driven table ───────────────────────────
# Per docs/data-hub/design-brief-2026-07-sector-nav.md and the Claude Design
# handoff's sector-trade-links-generator-spec.md. Reads scripts/datahub/pages/
# sic_group_stats.py's SECTORS registry (not a second hand-maintained list),
# so a new trade page appears here automatically on the next monthly rebuild.
# Registry moved to scripts/datahub/pages/sector_trade_links.py, shared with
# the hub landing page's "By sector" cards (company_insolvency_hub.py) - one
# list, not two that can drift apart. See that module's docstring.

def _trade_link_rows() -> list[dict]:
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).resolve().parent / "datahub" / "pages"))
    from sector_trade_links import rows as _rows  # noqa: E402
    return _rows()


def sector_pages_block() -> str:
    rows = _trade_link_rows()
    if not rows:
        # Sticky-nav coupling: an empty table must not ship an empty section
        # or a dead #sector-pages nav link (the class of bug that produced an
        # earlier dead #procedures link).
        return ""
    rows_html = "".join(
        f'<tr><th scope="row"><span class="cd-sectorlinks__name">{r["trade"]}</span>'
        f'<span class="cd-sectorlinks__desc">{r["blurb"].replace("&", "&amp;")}</span></th>'
        f'<td class="cd-sectorlinks__action">'
        f'<a class="cd-sectorlinks__btn" href="/data/{r["slug"]}/">View data'
        f'<span aria-hidden="true">&#8594;</span></a></td></tr>'
        for r in rows
    )
    return dedent(f"""\
    <section class="cd-section cd-w-wide" id="sector-pages">
      <div class="cd-section-head">
        <p class="cd-eyebrow">Detailed data</p>
        <h2>Get the insolvency data for your trade</h2>
        <p class="cd-section-intro">We publish a dedicated, monthly-updated data page for individual trades within the industry sections above. Find yours in the table and open its full time series.</p>
      </div>
      <div class="cd-tablewrap">
        <table class="cd-table cd-sectorlinks">
          <caption class="cd-table__caption">Detailed insolvency data pages by trade, grouped by SIC industry section.</caption>
          <thead>
            <tr><th scope="col">Trade or sub-sector</th><th scope="col" class="cd-sectorlinks__actionhead">Data page</th></tr>
          </thead>
          <tbody>{rows_html}</tbody>
        </table>
      </div>
      <p class="cd-sectorlinks__all"><a href="/data/company-insolvencies-by-sector/">See all sectors and the full SIC breakdown <span aria-hidden="true">&#8594;</span></a></p>
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
        <p class="cd-eyebrow">UK nations <span>· May 2026</span></p>
        <h2>UK company insolvencies by jurisdiction</h2>
        <p class="cd-section-intro">Figures are reported separately for England and Wales, Scotland and Northern Ireland.</p>
      </div>
      <div class="cd-nations-grid">
        <div class="cd-tablewrap">
          <table class="cd-table cd-table--nations">
            <caption class="cd-table__caption">Company insolvencies by UK jurisdiction, May 2026. Source: Insolvency Service / Companies House / Department for the Economy (NI).</caption>
            <thead>
              <tr>
                <th scope="col">Jurisdiction</th>
                <th scope="col" class="cd-num">May 2026</th>
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
          <h2>UK company insolvency statistics: methodology</h2>
        </div>
        <p class="cd-section-intro">Company insolvency data is sourced mainly from Companies House. Compulsory liquidation data for England and Wales comes from the Insolvency Service, and compulsory liquidation data for Northern Ireland comes from the Department for the Economy in Northern Ireland.</p>
        <p>The headline England and Wales figures use seasonally adjusted data where the Insolvency Service has identified seasonality. Scotland and Northern Ireland figures are shown on an unadjusted basis.</p>
        <p>The statistics count formal company insolvency procedures. They do not include members' voluntary liquidations, dissolutions or ordinary company closures.</p>
        <h3>Data limitations</h3>
        <ul class="cd-limits">
          <li>The latest month is provisional and can be revised.</li>
          <li>Table 1c industry totals by three-digit SIC are published monthly, through the latest headline month; the breakdown by insolvency procedure within each industry is published quarterly.</li>
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
        <h2>UK company insolvency data: source and citation</h2>
      </div>
      <div class="cd-cite-card">
        <div class="cd-cite-card__left">
          <dl>
            <dt>Primary source</dt><dd>Insolvency Service, Company Insolvency Statistics, May 2026.</dd>
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


# ── FAQ (FAQPage schema injected by mu-plugin) ────────────────────────────

def faq_block() -> str:
    qa = [
        (
            "How many UK company insolvencies were there in May 2026?",
            "There were 1,868 registered company insolvencies in England and Wales in May 2026, on a seasonally adjusted basis. That was 10% lower than April 2026 and 16% lower than May 2025. Scotland recorded 100 insolvencies and Northern Ireland 30 in the same month."
        ),
        (
            "What is the current UK company insolvency rate?",
            "The 12-month rolling company insolvency rate for England and Wales was 50.9 per 10,000 active companies in the year to May 2026, equal to one in 196 companies. The rate is lower than the 53.0 per 10,000 recorded a year earlier, and well below the 113.1 per 10,000 peak of the 2008–09 recession."
        ),
        (
            "Which procedure accounts for the most UK company insolvencies?",
            "Creditors' Voluntary Liquidations (CVLs) account for the largest share. There were 1,423 CVLs in May 2026, 76% of all company insolvencies for the month. Compulsory liquidations (285) and administrations (135) followed, with a small number of CVAs (25) and no receiverships."
        ),
        (
            "Which UK sectors have the most company insolvencies?",
            "Across the 12 months to May 2026, construction (3,803, 17%), wholesale and retail (3,527, 15%), and accommodation and food services (3,296, 14%) had the largest counts. Administrative services, professional services and manufacturing followed. These are volumes, not failure rates: larger sectors have more registered companies and so tend to have more insolvencies."
        ),
        (
            "When is the next UK insolvency statistics release?",
            "The Insolvency Service publishes monthly company insolvency statistics. The next scheduled release is 17 July 2026. This page is updated each month from the official release."
        ),
        (
            "Where does this UK insolvency data come from?",
            "Company insolvency data is published by the Insolvency Service as accredited official statistics, sourced mainly from Companies House. Compulsory liquidations for England and Wales come from the Insolvency Service directly; Northern Ireland compulsory liquidation data comes from the Department for the Economy. CompanyDebt presents the published figures. We do not produce them."
        ),
    ]
    items_html = "".join(
        f'<details class="cd-faq__item"><summary class="cd-faq__q">{q}</summary><div class="cd-faq__a"><p>{a}</p></div></details>'
        for q, a in qa
    )
    return dedent(f"""\
    <section class="cd-section cd-w-standard" id="faq">
      <div class="cd-section-head">
        <p class="cd-eyebrow">FAQ</p>
        <h2>UK company insolvency statistics: frequently asked questions</h2>
      </div>
      <div class="cd-faq">{items_html}</div>
    </section>
    """)


# ── Final CTA (full-bleed soft band) ──────────────────────────────────────

def final_cta_block() -> str:
    return dedent("""\
    <div class="cd-bleed cd-final-cta">
      <div class="cd-final-cta__inner">
        <div class="cd-final-cta__copy">
          <p class="cd-final-cta__head">Worried your company is at risk?</p>
          <p class="cd-final-cta__body">Our licensed insolvency practitioners offer free, confidential advice. The sooner you call, the more options you have.</p>
        </div>
        <div class="cd-final-cta__actions">
          <a class="cd-final-cta__btn" href="https://companydebt.com/contact-us/">Speak to an adviser</a>
          <a class="cd-final-cta__phone" href="tel:08000746757">0800 074 6757 <span>· free, no obligation</span></a>
        </div>
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
  /* Contains the intentional full-bleed sections below (.cd-w-wide, .cd-bleed
     use width:100vw to escape the WP container). 100vw resolves to the
     viewport width INCLUDING the scrollbar gutter, so on any page tall
     enough to scroll it overshoots the true visible width by the scrollbar's
     width (~15-17px) and creates a real, swipeable horizontal scroll. This
     is not masking an unknown overflow — the cause is the 100vw pattern
     above, which has no scrollbar-safe CSS-only fix; contain the resulting
     15px here rather than letting it leak into the page/site chrome. */
  overflow-x: hidden;
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
  --cd-figure: #0a1f44;
  --cd-positive: #166534;
  --cd-positive-dot: #16a34a;
  --cd-cta-orange: #ec6608;

  --cd-shadow-panel: 0 16px 45px rgba(16, 24, 40, 0.06);
  --cd-shadow-hero: 0 18px 50px rgba(16, 24, 40, 0.08);

  --cd-space-section: 96px;
  --cd-space-section-small: 64px;

  --cd-radius-panel: 24px;
  --cd-radius-card: 18px;
  --cd-radius-hero: 22px;

  color: var(--cd-text);
  /* The system-UI sans stack, identical to the sibling data pages. Without this
     the page inherited the theme's Arial, which is wider/heavier than Segoe UI
     (Windows) or San Francisco (macOS) — that, NOT font-smoothing, is what made
     this page's nav and breadcrumb read "bolder" than the others. Headings still
     override to the serif via --cd-serif. */
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-feature-settings: "tnum" 1, "ss01" 1;
  font-size: 14px;
  line-height: 1.65;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.cd-data-hub *, .cd-data-hub *::before, .cd-data-hub *::after { box-sizing: border-box; }
.cd-data-hub img, .cd-data-hub svg { max-width: 100%; }

/* ── Shared data-hub identity ─────────────────────────────────
   Serif display face on headings, the brand masthead and the data-sources
   logo strip. These match the new data pages so the hub reads as one product.
   The serif uses !important so it wins over the WordPress Customizer "Additional
   CSS" type scale (which sets sizes, not family) regardless of source order. */
.cd-data-hub { --cd-serif: "Source Serif 4", Georgia, "Times New Roman", serif; }
.cd-data-hub h1,
.cd-data-hub .cd-hero h1,
.cd-data-hub .cd-section-head h2,
.cd-data-hub .cd-cta h2 { font-family: var(--cd-serif) !important; }

/* padding 24/24 + margin-bottom:0 match the sibling pages' masthead exactly, so
   the menu bar is the same height on every page and the hero's own padding-top
   sets the gap below it (see .cd-w-hero). */
.cd-data-hub .cd-masthead { display:flex; align-items:center; justify-content:space-between; gap:24px; padding-top:24px; padding-bottom:24px; margin-bottom:0; border-bottom:1px solid var(--cd-line); flex-wrap:wrap; }
.cd-data-hub .cd-brand { display:inline-flex; align-items:center; gap:12px; color:var(--cd-text); text-decoration:none; }
.cd-data-hub .cd-brand:hover { text-decoration:none; }
.cd-data-hub .cd-brand__mark { display:inline-grid; place-items:center; width:38px; height:38px; border-radius:9px; background:var(--cd-figure); color:#fff; font-family:var(--cd-serif); font-weight:700; font-size:16px; letter-spacing:0.02em; }
.cd-data-hub .cd-brand__name { font-family:var(--cd-serif); font-weight:700; font-size:18px; letter-spacing:-0.01em; line-height:1; color:var(--cd-text); }
.cd-data-hub .cd-brand__sub { font-size:12px; letter-spacing:0.07em; text-transform:uppercase; color:var(--cd-muted); border-left:1px solid var(--cd-line); padding-left:12px; }
.cd-data-hub .cd-masthead__meta { display:inline-flex; align-items:center; gap:24px; font-size:12px; letter-spacing:0.05em; text-transform:uppercase; font-weight:600; color:var(--cd-muted); margin:0; }
.cd-data-hub .cd-verified { display:inline-flex; align-items:center; gap:7px; color:var(--cd-positive); }
.cd-data-hub .cd-verified svg { width:14px; height:14px; }
@media (max-width:560px){ .cd-data-hub .cd-brand__sub, .cd-data-hub .cd-masthead__meta { display:none; } }
.cd-data-hub .cd-mastnav { display:flex; align-items:center; gap:2px; flex-wrap:wrap; }
.cd-data-hub .cd-mastnav a { font-size:13px; font-weight:600; letter-spacing:.01em; color:var(--cd-text-soft); padding:7px 12px; border-radius:8px; white-space:nowrap; text-decoration:none; }
.cd-data-hub .cd-mastnav a:hover { background:var(--cd-surface-soft); color:var(--cd-accent); text-decoration:none; }
.cd-data-hub .cd-mastnav a[aria-current="page"] { color:var(--cd-accent); background:var(--cd-accent-soft); }
@media (max-width:640px){ .cd-data-hub .cd-mastnav a { font-size:12px; padding:6px 9px; } }

.cd-data-hub .cd-srcstrip { display:flex; align-items:center; gap:40px; flex-wrap:wrap; padding:28px 0; border-top:1px solid var(--cd-line); border-bottom:1px solid var(--cd-line); }
.cd-data-hub .cd-srcstrip__label { font-size:12px; text-transform:uppercase; letter-spacing:0.08em; font-weight:700; color:var(--cd-muted); flex:none; }
.cd-data-hub .cd-srcstrip__logos { display:flex; align-items:center; gap:30px; flex-wrap:wrap; }
.cd-data-hub .cd-srclogo { display:flex; flex-direction:column; gap:9px; margin:0; }
.cd-data-hub .cd-srclogo img { height:74px; width:auto; max-width:240px; display:block; object-fit:contain; }
.cd-data-hub .cd-srclogo figcaption { font-size:12px; color:var(--cd-muted); font-weight:600; letter-spacing:0.02em; }
@media (max-width:560px){ .cd-data-hub .cd-srclogo img { height:56px; } .cd-data-hub .cd-srcstrip { gap:20px; } }

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
   1280px on wide viewports. max-width:none beats inherited theme caps. */
.cd-data-hub .cd-w-wide {
  width: 100vw;
  max-width: 100vw;
  margin-left: calc(50% - 50vw);
  margin-right: calc(50% - 50vw);
  padding-left: max(24px, calc(50vw - 640px));
  padding-right: max(24px, calc(50vw - 640px));
}
/* Full-bleed band that escapes the parent .container. Inner content
   re-aligns to a 1280px max-width. */
.cd-data-hub .cd-bleed {
  width: 100vw;
  max-width: 100vw;
  margin-left: calc(50% - 50vw);
  margin-right: calc(50% - 50vw);
  padding-left: max(24px, calc(50vw - 640px));
  padding-right: max(24px, calc(50vw - 640px));
}

/* ── Spacing rhythm ───────────────────────────────────────── */
.cd-data-hub .cd-section { margin-top: var(--cd-space-section); }
.cd-data-hub .cd-section-small { margin-top: var(--cd-space-section-small); }
.cd-data-hub > .cd-section:first-child { margin-top: 24px; }

/* ── Typography (5-size scale on 8px grid) ────────────────── */
.cd-data-hub h1 {
  font-size: clamp(40px, 5vw, 56px);
  line-height: 1.02;
  letter-spacing: -0.04em;
  font-weight: 700;
  margin: 0 0 32px;
  max-width: 680px;
  color: var(--cd-text);
}
.cd-data-hub h2 {
  font-size: 32px;
  line-height: 1.12;
  letter-spacing: -0.025em;
  font-weight: 700;
  margin: 0;
  color: var(--cd-text);
}
.cd-data-hub h3 {
  font-size: 20px;
  line-height: 1.3;
  font-weight: 650;
  margin: 40px 0 16px;
  letter-spacing: -0.01em;
  color: var(--cd-text);
}
.cd-data-hub p { margin: 0 0 16px; color: var(--cd-text-soft); font-size: 14px; line-height: 1.65; }
.cd-data-hub a { color: var(--cd-accent); text-decoration: none; }
.cd-data-hub a:hover { text-decoration: underline; text-underline-offset: 3px; }

.cd-data-hub .cd-lede {
  font-size: 18px;
  line-height: 1.55;
  color: var(--cd-text-soft);
  max-width: 660px;
  margin: 0 0 32px;
}

/* Optional subtitle line directly under the H1, e.g. a geographic-scope
   clarifier ("Latest detailed figures for England and Wales"). */
.cd-data-hub .cd-hero__subtitle {
  font-size: 15px;
  font-weight: 500;
  color: var(--cd-muted);
  margin: 6px 0 20px;
}
/* Optional scope-definition line (e.g. clarifying which SIC groups are and
   are not included) — sits between the subtitle and the lede, slightly
   heavier than the subtitle since it carries a real caveat, not just a
   geography tag. */
.cd-data-hub .cd-hero__scope {
  font-size: 15px;
  font-weight: 600;
  color: var(--cd-text-soft);
  background: var(--cd-surface-soft);
  border-left: 3px solid var(--cd-accent);
  border-radius: 8px;
  padding: 10px 14px;
  margin: 0 0 20px;
  max-width: 640px;
}

.cd-data-hub .cd-eyebrow {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--cd-accent);
  margin: 0 0 16px;
  line-height: 1.2;
  display: inline-flex;
  align-items: center;
}
/* Date/context suffix inside an eyebrow — muted grey, kept in same line. */
.cd-data-hub .cd-eyebrow span:not(.cd-eyebrow__pulse) {
  color: #6b7280;
  font-weight: 600;
  margin-left: 4px;
}
.cd-data-hub .cd-eyebrow__pulse {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--cd-positive-dot);
  margin-right: 10px;
  box-shadow: 0 0 0 0 rgba(22, 163, 74, 0.6);
  animation: cd-pulse 2.2s ease-out infinite;
}
@keyframes cd-pulse {
  0%   { box-shadow: 0 0 0 0 rgba(22, 163, 74, 0.6); }
  70%  { box-shadow: 0 0 0 7px rgba(22, 163, 74, 0); }
  100% { box-shadow: 0 0 0 0 rgba(22, 163, 74, 0); }
}
@media (prefers-reduced-motion: reduce) {
  .cd-data-hub .cd-eyebrow__pulse { animation: none; }
}

.cd-data-hub .cd-sr-only {
  position: absolute; width: 1px; height: 1px; padding: 0;
  margin: -1px; overflow: hidden; clip: rect(0,0,0,0); border: 0;
}

/* ── Section header ───────────────────────────────────────── */
.cd-data-hub .cd-section-head { margin-bottom: 32px; }
.cd-data-hub .cd-section-head h2 { margin: 0; }
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

/* ── Hero — spans the heading rail (left) to the wide rail (right) ── */
.cd-data-hub .cd-w-hero {
  /* The hero straddles the page's two rails so it stays consistent with both:
       LEFT  edge = the 1040 heading rail's content edge (= the brand logo and the
                    section headings), so the H1 lines up under the logo.
       RIGHT edge = the 1280 wide-content rail (= the chart/data sections below),
                    so the hero's KPI panel lines up with those blocks.
     Left inset  = 50vw - 520 + 24 (centre a 1040 rail, then its 24px padding).
     Right inset = 50vw - 640 (identical to .cd-w-wide, the wide rail).
     This keeps the H1 aligned with the logo AND gives the two-column grid room
     to breathe (a centred 1040 rail left only ~470px for the text column once the
     440px panel + 88px gap are taken out). */
  width: 100vw;
  max-width: 100vw;
  margin-left: calc(50% - 50vw);
  margin-right: calc(50% - 50vw);
  padding-left: max(24px, calc(50vw - 496px));
  padding-right: max(24px, calc(50vw - 640px));
  /* 64px matches the sibling wrapper (.cd-hub-header) so the back-link sits the
     same distance below the masthead on every page. */
  padding-top: 64px;
  box-sizing: border-box;
}
.cd-data-hub .cd-hero {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 440px;
  gap: 88px;
  align-items: start;
  padding-bottom: 48px;
  margin-top: 0;
}
/* Back-link to the hub — matches the sibling data pages (.cd-back). It sits in
   the .cd-w-hero wrapper ABOVE the .cd-hero grid (not inside it), so the grid's
   column gap can't push it off the H1; its own 24px bottom margin sets the gap.
   This mirrors the siblings' .cd-hub-header > .cd-back structure. */
.cd-data-hub .cd-w-hero > .cd-back {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--cd-muted);
  margin: 0 0 24px;
}
.cd-data-hub .cd-w-hero > .cd-back:hover { color: var(--cd-accent); text-decoration: none; }
.cd-data-hub .cd-hero__copy {
  max-width: 680px;
  padding-right: 0;
}

/* Eyebrow with live pulse dot — overrides the global cd-eyebrow */
.cd-data-hub .cd-hero__copy .cd-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  margin: 0 0 16px;
  font-size: 12px;
  font-weight: 750;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--cd-accent);
}

/* H1 with manual line break via <span>. Both lines wrapped in spans with
   nowrap so the title forms a clean two-line block. */
.cd-data-hub .cd-hero h1 {
  max-width: 650px;
  margin: 0 0 32px;
  font-size: clamp(40px, 5vw, 56px);
  line-height: 1.02;
  letter-spacing: -0.04em;
  font-weight: 700;
}
.cd-data-hub .cd-hero h1 .cd-h1__line { display: block; white-space: nowrap; }

/* Lede */
.cd-data-hub .cd-hero .cd-lede {
  max-width: 640px;
  margin: 0 0 32px;
  font-size: 18px;
  line-height: 1.6;
  color: #263244;
}

/* Metadata 2x2 grid */
.cd-data-hub .cd-meta-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px 32px;
  margin: 32px 0 0;
  padding: 0;
  max-width: 560px;
}
.cd-data-hub .cd-meta-item { margin: 0; }
.cd-data-hub .cd-meta-item span {
  display: block;
  font-size: 11px;
  font-weight: 750;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--cd-muted);
  margin-bottom: 6px;
}
.cd-data-hub .cd-meta-item strong {
  display: block;
  font-size: 15px;
  font-weight: 550;
  color: var(--cd-text);
}

/* Accredited-statistics pill — credibility mark, tighter and brighter */
.cd-data-hub .cd-official-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin: 24px 0 0;
  padding: 4px 12px;
  border-radius: 100px;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #166534;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.01em;
}
.cd-data-hub .cd-official-badge span {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 999px;
  background: #16a34a;
}

/* KPI card — fixed 440px width, top-aligned with margin to match H1 */
.cd-data-hub .cd-hero__panel {
  width: 100%;
  margin-top: 38px;
  padding: 34px;
  background: var(--cd-surface);
  border: 1px solid var(--cd-line);
  border-radius: 24px;
  box-shadow: 0 22px 60px rgba(16, 24, 40, 0.08);
}
.cd-data-hub .cd-kpi-label {
  max-width: 280px;
  margin: 0 0 22px;
  font-size: 13px;
  font-weight: 750;
  letter-spacing: 0.12em;
  line-height: 1.35;
  text-transform: uppercase;
  color: var(--cd-muted);
}
.cd-data-hub .cd-main-kpi { display: block; }
.cd-data-hub .cd-main-kpi__v {
  display: block;
  font-size: 48px;
  line-height: 1;
  font-weight: 750;
  letter-spacing: -0.04em;
  color: var(--cd-text);
  font-variant-numeric: tabular-nums;
}
.cd-data-hub .cd-main-kpi__k {
  display: block;
  margin-top: 12px;
  font-size: 14px;
  color: #263244;
}
.cd-data-hub .cd-change-row {
  display: flex;
  gap: 24px;
  margin-top: 22px;
  font-size: 11px;
  color: #9ca3af;
  font-weight: 400;
  align-items: baseline;
}
.cd-data-hub .cd-change-row > span { display: inline-flex; align-items: baseline; gap: 6px; }
.cd-data-hub .cd-change-row strong {
  color: #dc2626;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  font-size: 14px;
  margin: 0;
}
.cd-data-hub .cd-change-row.cd-change-row--down strong { color: #16a34a; }
.cd-data-hub .cd-kpi-divider {
  height: 1px;
  background: #e5e7eb;
  margin: 24px 0;
}
.cd-data-hub .cd-mini-kpi-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 24px;
}
.cd-data-hub .cd-mini-kpi { display: block; }
.cd-data-hub .cd-mini-kpi__v {
  display: block;
  font-size: 32px;
  line-height: 1;
  font-weight: 700;
  letter-spacing: -0.025em;
  color: #0a1f44;
  font-variant-numeric: tabular-nums;
}
.cd-data-hub .cd-mini-kpi__k {
  display: block;
  margin-top: 6px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: #6b7280;
}
.cd-data-hub .cd-mini-kpi__n {
  display: block;
  margin-top: 4px;
  font-size: 12px;
  color: #9ca3af;
  font-weight: 400;
}

/* Subtle divider line right after the hero — same rails as .cd-w-hero so the
   line starts under the logo/H1 and ends at the wide-content right edge. */
.cd-data-hub .cd-hero-divider {
  width: 100vw;
  max-width: 100vw;
  margin-left: calc(50% - 50vw);
  margin-right: calc(50% - 50vw);
  padding-left: max(24px, calc(50vw - 496px));
  padding-right: max(24px, calc(50vw - 640px));
  box-sizing: border-box;
}
.cd-data-hub .cd-hero-divider::after {
  content: "";
  display: block;
  height: 1px;
  background: #edf0f3;
}

/* ── Sticky section nav — wayfinding bar ──────────────────── */
.cd-data-hub .cd-secnav {
  position: sticky;
  top: 0;
  z-index: 20;
  background: #f0f2f5;
  border-top: 1px solid var(--cd-line);
  border-bottom: 1px solid var(--cd-line);
  margin-top: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  font-size: 14px;
  padding-top: 8px;
  padding-bottom: 8px;
}
.cd-data-hub .cd-secnav a {
  color: #555;
  padding: 6px 14px;
  border-radius: 4px;
  line-height: 1.3;
  font-weight: 500;
  text-decoration: none;
  border: 1px solid transparent;
  transition: background 0.12s ease, color 0.12s ease;
}
.cd-data-hub .cd-secnav a:hover { color: var(--cd-text); background: rgba(255,255,255,0.6); text-decoration: none; }
.cd-data-hub .cd-secnav a.is-active {
  color: #0a1f44;
  background: #ffffff;
  border-color: #d0d5dd;
  font-weight: 600;
}
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
.cd-data-hub .cd-table { width: 100%; border-collapse: collapse; font-size: 14px; }
.cd-data-hub .cd-table th,
.cd-data-hub .cd-table td { padding: 12px 16px; text-align: left; vertical-align: top; }
.cd-data-hub .cd-table thead th {
  background: #f7f8fa;
  font-weight: 650;
  color: var(--cd-text);
  font-size: 12px;
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
  white-space: nowrap;
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

/* Chart figure + visible figcaption — semantic image grouping for SEO. */
.cd-data-hub .cd-chart-figure { margin: 0; padding: 0; }
.cd-data-hub .cd-figcaption {
  font-size: 12px;
  line-height: 1.55;
  color: var(--cd-muted);
  margin: 12px 4px 0;
  max-width: 920px;
}
.cd-data-hub .cd-figcaption strong {
  color: var(--cd-text-soft);
  font-weight: 600;
}

/* Visible table caption — replaces the prior screen-reader-only treatment so
   search engines and users both see the table's purpose. */
.cd-data-hub .cd-tablewrap .cd-table__caption {
  caption-side: top;
  text-align: left;
  font-size: 12px;
  color: var(--cd-muted);
  line-height: 1.55;
  padding: 14px 18px;
  border-bottom: 1px solid var(--cd-line-soft);
  background: #fcfcfd;
  font-weight: 400;
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
  padding: 24px 24px 22px;
  background: var(--cd-surface-soft);
  border-radius: 14px;
  border-left: 3px solid var(--cd-accent);
}
.cd-data-hub .cd-side-notes__title {
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--cd-accent);
  font-weight: 700;
  margin: 0 0 16px;
  line-height: 1.2;
}
.cd-data-hub .cd-side-note__d {
  font-size: 14px;
  color: var(--cd-text-soft);
  margin: 0 0 14px;
  line-height: 1.6;
}
.cd-data-hub .cd-side-note__d:last-child { margin-bottom: 0; }
/* Grouped sub-items inside a .cd-side-notes box, each with its own h3 (e.g.
   the "why <sector> is under pressure" list on single-SIC-sector pages). */
.cd-data-hub .cd-side-notes .cd-note-item { margin: 0 0 20px; }
.cd-data-hub .cd-side-notes .cd-note-item:last-child { margin-bottom: 0; }
.cd-data-hub .cd-side-notes .cd-note-item h3 {
  font-size: 15px;
  font-weight: 700;
  color: var(--cd-text);
  margin: 0 0 8px;
  line-height: 1.3;
}
/* Single-note variant used in the UK nations section. */
.cd-data-hub .cd-side-note--single {
  padding: 20px 22px;
  background: var(--cd-surface-band);
  border-left: 3px solid var(--cd-accent);
  border-radius: 12px;
}
.cd-data-hub .cd-side-note--single .cd-side-note__k {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--cd-accent);
  font-weight: 700;
  margin: 0 0 8px;
}

/* ── Rate section (text + callout / chart) ────────────────── */
.cd-data-hub .cd-rate-grid {
  display: grid;
  grid-template-columns: minmax(360px, 0.85fr) minmax(560px, 1.15fr);
  gap: 48px;
  align-items: start;
}
/* NOTE: live type scale is governed by the Customizer "Additional CSS"
   (#wp-custom-css), which sets .cd-data-hub p { 14px !important } and
   .cd-section-intro { 18px } and overrides the sizes below. Section lead
   paragraphs MUST carry class="cd-section-intro" to read at 18px like every
   other section; the rate + methodology leads do. Do not rely on the 17px
   rule here for the deployed page. */
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
  font-size: 32px;
  font-weight: 700;
  color: var(--cd-text);
  font-variant-numeric: tabular-nums;
  letter-spacing: -0.02em;
  line-height: 1.05;
}
.cd-data-hub .cd-callout-card__u { font-size: 13px; color: var(--cd-muted); font-weight: 500; margin-left: 4px; }
@media (max-width: 1020px) {
  .cd-data-hub .cd-rate-grid { grid-template-columns: 1fr; gap: 28px; }
  .cd-data-hub .cd-chart-panel--rate { min-height: 320px; }
}

/* ── Sector data-page links table ("Get the insolvency data for your
   trade") — always-visible table pairing each trade with a View data
   button, replacing the earlier procedure-card grid. Per
   docs/data-hub/design-brief-2026-07-sector-nav.md and the Claude Design
   handoff's sector-trade-links-generator-spec.md. ──────────────────── */
.cd-data-hub .cd-sectorlinks th[scope="row"] { font-weight: 650; color: var(--cd-text); }
.cd-data-hub .cd-sectorlinks__name { display: block; font-size: 16px; font-weight: 650; color: var(--cd-text); }
.cd-data-hub .cd-sectorlinks__desc { display: block; margin-top: 3px; font-size: 13px; font-weight: 400; line-height: 1.45; color: var(--cd-muted); max-width: 52ch; }
.cd-data-hub .cd-sectorlinks td { color: var(--cd-text-soft); }
.cd-data-hub .cd-sectorlinks__actionhead { text-align: left; }
.cd-data-hub .cd-sectorlinks__action { text-align: left; white-space: nowrap; vertical-align: middle; width: 1%; }
.cd-data-hub .cd-sectorlinks__btn {
  /* The WP theme forces `a { display: inline }`, which would collapse the
     44px min-height tap target to a text baseline. Beat it explicitly. */
  display: inline-flex !important;
  align-items: center;
  gap: 8px;
  padding: 11px 16px;
  min-height: 44px;
  box-sizing: border-box;
  background: var(--cd-accent);
  color: #fff !important;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 650;
  text-decoration: none;
  white-space: nowrap;
  transition: background .15s ease;
}
.cd-data-hub .cd-sectorlinks__btn span { font-size: 15px; line-height: 1; transition: transform .15s ease; }
.cd-data-hub .cd-sectorlinks__btn::after, .cd-data-hub .cd-sectorlinks__btn::before { content: none !important; display: none !important; }
.cd-data-hub .cd-sectorlinks .cd-table-arrow { display: none !important; }
.cd-data-hub .cd-sectorlinks__btn:hover { background: #0c3c66; color: #fff !important; text-decoration: none; }
.cd-data-hub .cd-sectorlinks__btn:hover span { transform: translateX(3px); }
.cd-data-hub .cd-sectorlinks__btn:focus-visible { outline: 2px solid var(--cd-accent); outline-offset: 2px; }
.cd-data-hub .cd-sectorlinks tbody tr:hover { background: var(--cd-surface-soft); }
.cd-data-hub .cd-sectorlinks__all { margin: 18px 0 0 !important; font-size: 15px; }
.cd-data-hub .cd-sectorlinks__all a { font-weight: 700; color: var(--cd-accent); text-decoration: none; }
.cd-data-hub .cd-sectorlinks__all a:hover { text-decoration: underline; }
@media (max-width: 700px) {
  .cd-data-hub .cd-sectorlinks { min-width: 0; }
  .cd-data-hub .cd-sectorlinks thead { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
  .cd-data-hub .cd-sectorlinks tbody tr { display: block; padding: 16px 4px; }
  .cd-data-hub .cd-sectorlinks tbody tr + tr { border-top: 1px solid var(--cd-line-soft); }
  .cd-data-hub .cd-sectorlinks tbody tr + tr td, .cd-data-hub .cd-sectorlinks tbody tr + tr th { border-top: 0; }
  .cd-data-hub .cd-sectorlinks th[scope="row"] { display: block; padding: 0 0 12px; }
  .cd-data-hub .cd-sectorlinks__action { display: block; padding: 0; width: auto; }
}

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

/* ── FAQ ──────────────────────────────────────────────────── */
.cd-data-hub .cd-faq {
  border: 1px solid var(--cd-line);
  border-radius: var(--cd-radius-panel);
  background: var(--cd-surface);
  overflow: hidden;
  box-shadow: var(--cd-shadow-panel);
}
.cd-data-hub .cd-faq__item { border-bottom: 1px solid var(--cd-line-soft); }
.cd-data-hub .cd-faq__item:last-child { border-bottom: 0; }
.cd-data-hub .cd-faq__q {
  list-style: none;
  cursor: pointer;
  padding: 20px 24px;
  font-size: 14px;
  font-weight: 600;
  color: var(--cd-text);
  line-height: 1.45;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}
.cd-data-hub .cd-faq__q::-webkit-details-marker { display: none; }
.cd-data-hub .cd-faq__q::after {
  content: "";
  width: 14px;
  height: 14px;
  flex-shrink: 0;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23667085' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: center;
  transition: transform 0.2s ease;
  transform: rotate(-90deg);
}
.cd-data-hub .cd-faq__item[open] > .cd-faq__q::after { transform: rotate(0deg); }
.cd-data-hub .cd-faq__q:hover { color: var(--cd-accent); }
.cd-data-hub .cd-faq__a { padding: 0 24px 20px; }
.cd-data-hub .cd-faq__a p { font-size: 14px; line-height: 1.65; color: var(--cd-text-soft); margin: 0; }
@media (max-width: 720px) {
  .cd-data-hub .cd-faq__q { padding: 18px 20px; font-size: 16px; }
  .cd-data-hub .cd-faq__a { padding: 0 20px 20px; }
}

/* ── Final CTA (full-bleed soft band) ─────────────────────── */
.cd-data-hub .cd-final-cta {
  margin-top: 96px;
  padding-top: 56px;
  padding-bottom: 56px;
  background: #0a1f44;
  border-top: 0;
  color: #fff;
}
.cd-data-hub .cd-final-cta__inner {
  max-width: 1040px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: minmax(0, 1.5fr) auto;
  gap: 40px;
  align-items: center;
}
.cd-data-hub .cd-final-cta__head {
  font-size: 26px;
  color: #fff;
  font-weight: 700;
  margin: 0 0 10px;
  letter-spacing: -0.015em;
  line-height: 1.2;
}
.cd-data-hub .cd-final-cta__body {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.85);
  margin: 0;
  line-height: 1.55;
  font-weight: 400;
  max-width: 560px;
}
.cd-data-hub .cd-final-cta__actions {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 10px;
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
  box-shadow: 0 6px 16px rgba(236, 102, 8, 0.22);
}
.cd-data-hub .cd-final-cta__btn:hover { background: #d65906; text-decoration: none; color: #fff; }
.cd-data-hub .cd-final-cta__phone {
  display: inline-block;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
}
.cd-data-hub .cd-final-cta__phone:hover { text-decoration: underline; color: #fff; }
.cd-data-hub .cd-final-cta__phone span {
  color: rgba(255, 255, 255, 0.65);
  font-weight: 400;
  margin-left: 2px;
}
@media (max-width: 760px) {
  .cd-data-hub .cd-final-cta__inner { grid-template-columns: 1fr; gap: 24px; }
  .cd-data-hub .cd-final-cta__head { font-size: 22px; }
}

/* ── Mobile layout adjustments ───────────────────────────── */
@media (max-width: 980px) {
  /* On mobile, the hero becomes a single column. Use display:contents on the
     copy block and order properties so the KPI card sits immediately after
     the H1/intro and before the metadata grid and badge. */
  .cd-data-hub .cd-hero {
    display: flex;
    flex-direction: column;
    gap: 32px;
    padding-bottom: 32px;
  }
  .cd-data-hub .cd-hero__copy {
    display: contents;
    max-width: none;
    padding-right: 0;
  }
  .cd-data-hub .cd-hero__copy .cd-eyebrow { order: 1; }
  .cd-data-hub .cd-hero h1 { order: 2; }
  .cd-data-hub .cd-hero .cd-lede { order: 3; }
  .cd-data-hub .cd-hero__panel { order: 4; margin-top: 0; max-width: none; }
  .cd-data-hub .cd-meta-grid { order: 5; }
  .cd-data-hub .cd-official-badge { order: 6; }
  .cd-data-hub .cd-section { margin-top: 72px; }
  .cd-data-hub .cd-method-band { padding-top: 64px; padding-bottom: 64px; }
  .cd-data-hub .cd-final-cta { padding-top: 40px; padding-bottom: 40px; margin-top: 64px; }
}
@media (max-width: 720px) {
  .cd-data-hub .cd-meta-grid { grid-template-columns: 1fr; gap: 16px; max-width: none; }
  .cd-data-hub .cd-secnav { overflow-x: auto; flex-wrap: nowrap; padding-left: 16px; padding-right: 16px; }
  .cd-data-hub .cd-secnav a { white-space: nowrap; }
  .cd-data-hub .cd-tablewrap,
  body.page-template-data-hub-template .main-content .cd-data-hub .cd-tablewrap {
    overflow-x: auto !important;
    -webkit-overflow-scrolling: touch;
  }
  .cd-data-hub .cd-table { min-width: 560px; font-size: 16px; }
  .cd-data-hub .cd-table th, .cd-data-hub .cd-table td { padding: 14px 16px; }
  /* Body copy stays at a compact 14-15px on desktop, but mobile has no room
     for a smaller-than-16px paragraph without forcing pinch-zoom or an iOS
     input-focus zoom (on any field that shares this size). The high-specificity
     selector duplicates an un-versioned theme-template override
     (body.page-template-data-hub-template .main-content .cd-data-hub ...,
     deployed straight to the live template outside this file) that otherwise
     wins over a plain .cd-data-hub rule regardless of media query. */
  .cd-data-hub .cd-side-note__d,
  .cd-data-hub .cd-final-cta__body,
  .cd-data-hub .cd-table td,
  body.page-template-data-hub-template .main-content .cd-data-hub .cd-side-note__d,
  body.page-template-data-hub-template .main-content .cd-data-hub td,
  body.page-template-data-hub-template .main-content .cd-data-hub .cd-table tbody td {
    font-size: 16px !important;
  }
  .cd-data-hub .cd-chart-panel { padding: 20px 18px 16px; }
  .cd-data-hub .cd-cite-card dl { grid-template-columns: 1fr; gap: 4px 0; }
  .cd-data-hub .cd-cite-card dl dd { margin-bottom: 12px; }
  /* Chart controls scroll horizontally on narrow viewports so all view-range
     buttons stay on one row. */
  .cd-data-hub .cd-chart-controls { display: flex; flex-wrap: nowrap; max-width: 100%; overflow-x: auto; }
  .cd-data-hub .cd-chart-controls__label { padding: 0 8px 0 10px; }
  .cd-data-hub .cd-chart-tab { padding: 8px 12px; font-size: 13px; }
}
@media (max-width: 700px) {
  .cd-data-hub .cd-w-hero,
  .cd-data-hub .cd-hero-divider { padding-inline: 20px; }
  .cd-data-hub .cd-hero { gap: 36px; padding-bottom: 56px; }
  .cd-data-hub .cd-hero h1 {
    font-size: clamp(30px, 8vw, 40px);
    letter-spacing: -0.03em;
    margin: 0 0 24px;
    overflow-wrap: break-word;
  }
  /* On mobile, the H1 lines must wrap if needed. The HTML contains a real
     space between the two spans so the browser has a break opportunity. */
  .cd-data-hub .cd-hero h1 .cd-h1__line { white-space: normal; display: inline; }
  .cd-data-hub .cd-hero__panel { padding: 22px; border-radius: 18px; }
  .cd-data-hub .cd-main-kpi__v { font-size: 40px; }
  .cd-data-hub .cd-change-row { flex-direction: column; gap: 8px; }
}
@media (max-width: 520px) {
  .cd-data-hub .cd-w-narrow, .cd-data-hub .cd-w-standard { padding-left: 16px; padding-right: 16px; }
  .cd-data-hub .cd-w-wide, .cd-data-hub .cd-bleed { padding-left: 16px; padding-right: 16px; }
  .cd-data-hub .cd-mini-kpi-grid { grid-template-columns: 1fr; }
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
        masthead_block(),
        hero_block(meta, latest_total),
        srcstrip_block(),
        secnav_block(),
        latest_figures_block(meta),
        monthly_chart_block(charts),
        longrun_block(charts),
        rate_block(charts, latest_rate),
        sector_block(d["sector"], charts),
        sector_pages_block(),
        nations_block(d["nations"]),
        methodology_block(),
        source_citation_block(meta),
        faq_block(),
        final_cta_block(),
        '</div>',
    ])

    metadata_comments = (
        f"<!-- CD-NO-AUTOEDIT: data_reference page generated by build_insolvency_dashboard.py."
        f" Internal-link and article-rewrite pipelines must skip this file. -->\n"
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
