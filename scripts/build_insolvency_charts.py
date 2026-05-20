"""Generate inline SVG charts for the UK Company Insolvency Statistics page.

Reads JSON produced by parse_insolvency_data.py and writes a dict of SVG
strings (and supporting metadata) keyed by chart id. Pre-rendered SVG avoids
any chart library dependency; native `<title>` elements provide tooltips.

Charts:
  - monthly_stacked_5y, monthly_stacked_since_2000, monthly_stacked_post_covid
  - longrun_total_line
  - rate_line
  - sector_bars

Usage from build_insolvency_dashboard.py:
    from build_insolvency_charts import build_all_charts
    charts = build_all_charts(json_dir)
    charts["monthly_stacked_5y"]   # -> "<svg ...>"
"""

from __future__ import annotations

import json
from pathlib import Path

# Restrained palette per the brief
COLOURS = {
    "cvls":          "#1d3557",   # dark blue
    "compulsory":    "#a04646",   # muted red
    "administrations": "#b87333", # amber/brown
    "cvas":          "#5a6373",   # slate
    "receiverships": "#b8bcc4",   # light grey
    "total":         "#0f172a",   # near-black, for line charts
    "rate":          "#0f172a",
    "grid":          "#e5e7eb",
    "axis":          "#9ca3af",
    "text":          "#374151",
    "accent":        "#0f172a",
    "marker":        "#94a3b8",
    "bar_primary":   "#1d3557",
}

PROCEDURE_LABELS = {
    "cvls":            "CVLs",
    "compulsory":      "Compulsory liquidations",
    "administrations": "Administrations",
    "cvas":            "CVAs",
    "receiverships":   "Receiverships",
}

# Stack order: largest at bottom for legibility
STACK_ORDER = ["cvls", "compulsory", "administrations", "cvas", "receiverships"]


# ─── helpers ──────────────────────────────────────────────────────────────

def nice_axis_max(value: float) -> float:
    """Round up to a friendly axis maximum."""
    if value <= 0:
        return 10
    import math
    magnitude = 10 ** math.floor(math.log10(value))
    fraction = value / magnitude
    if fraction <= 1.2:
        step = 1.5
    elif fraction <= 2:
        step = 2
    elif fraction <= 3:
        step = 3
    elif fraction <= 5:
        step = 5
    else:
        step = 10
    return step * magnitude


def axis_ticks(max_val: float, count: int = 5) -> list[float]:
    return [round(max_val * i / count, 1) for i in range(count + 1)]


def format_number(n: float | int | None) -> str:
    if n is None:
        return "n/a"
    if isinstance(n, float):
        if n == int(n):
            return f"{int(n):,}"
        return f"{n:,.1f}"
    return f"{int(n):,}"


def month_label(period: str) -> str:
    """'2026-04' -> 'Apr 2026'."""
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    try:
        y, m = period.split("-")
        return f"{months[int(m) - 1]} {y}"
    except (ValueError, IndexError):
        return period


# ─── stacked bar chart ────────────────────────────────────────────────────

def build_stacked_bar(monthly: dict, start_period: str, end_period: str, *, chart_id: str) -> str:
    """Stacked bar of monthly insolvencies by procedure for a window."""
    months = monthly["months"]
    series = monthly["series"]
    try:
        i0 = months.index(start_period)
    except ValueError:
        i0 = 0
    try:
        i1 = months.index(end_period) + 1
    except ValueError:
        i1 = len(months)
    window_months = months[i0:i1]
    n = len(window_months)
    if n == 0:
        return ""

    # Stack heights per month
    stacked = []
    for idx in range(i0, i1):
        per_month = {k: (series[k][idx] or 0) for k in STACK_ORDER}
        stacked.append(per_month)

    monthly_totals = [sum(v.values()) for v in stacked]
    ymax_raw = max(monthly_totals) if monthly_totals else 100
    ymax = nice_axis_max(ymax_raw)

    # SVG geometry:viewBox so it scales fluidly
    W, H = 900, 360
    pad_l, pad_r, pad_t, pad_b = 56, 16, 24, 56
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    bar_gap = 1
    bar_w = max(2, (plot_w / n) - bar_gap)

    parts = []
    parts.append(f'<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="{chart_id}-title {chart_id}-desc" class="cd-chart cd-chart--stacked" xmlns="http://www.w3.org/2000/svg">')
    parts.append(f'<title id="{chart_id}-title">Monthly company insolvencies by procedure, {month_label(window_months[0])} to {month_label(window_months[-1])}</title>')
    parts.append(f'<desc id="{chart_id}-desc">Stacked bars showing the monthly count of company insolvencies in England and Wales, broken down by procedure type.</desc>')

    # Y-axis gridlines + labels
    parts.append('<g class="cd-chart__grid">')
    for tick in axis_ticks(ymax, 5):
        y = pad_t + plot_h - (tick / ymax) * plot_h
        parts.append(f'<line x1="{pad_l}" x2="{W - pad_r}" y1="{y:.1f}" y2="{y:.1f}" stroke="{COLOURS["grid"]}" stroke-width="1"/>')
        parts.append(f'<text x="{pad_l - 8}" y="{y + 4:.1f}" text-anchor="end" font-size="11" fill="{COLOURS["text"]}" font-variant-numeric="tabular-nums">{format_number(int(tick))}</text>')
    parts.append('</g>')

    # Bars
    parts.append('<g class="cd-chart__bars">')
    for i, per_month in enumerate(stacked):
        x = pad_l + i * (bar_w + bar_gap)
        cumulative = 0
        # Build tooltip lines once per month
        tt_lines = [month_label(window_months[i])]
        total = monthly_totals[i]
        tt_lines.append(f"Total {format_number(total)}")
        for key in reversed(STACK_ORDER):  # show largest first in tooltip
            v = per_month[key]
            if v:
                tt_lines.append(f"{PROCEDURE_LABELS[key]} {format_number(v)}")
        title = "&#10;".join(tt_lines)
        for key in STACK_ORDER:
            v = per_month[key]
            if not v:
                continue
            h = (v / ymax) * plot_h
            y = pad_t + plot_h - cumulative - h
            parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{h:.2f}" fill="{COLOURS[key]}"><title>{title}</title></rect>')
            cumulative += h
    parts.append('</g>')

    # X-axis: show year labels at start of each calendar year only (avoids clutter)
    parts.append('<g class="cd-chart__xaxis">')
    seen_years = set()
    for i, period in enumerate(window_months):
        year = period.split("-")[0]
        if year not in seen_years and (period.endswith("-01") or i == 0):
            seen_years.add(year)
            x = pad_l + i * (bar_w + bar_gap) + bar_w / 2
            parts.append(f'<text x="{x:.1f}" y="{H - pad_b + 18}" text-anchor="middle" font-size="11" fill="{COLOURS["text"]}">{year}</text>')
    parts.append('</g>')

    # Axis line
    parts.append(f'<line x1="{pad_l}" x2="{W - pad_r}" y1="{pad_t + plot_h}" y2="{pad_t + plot_h}" stroke="{COLOURS["axis"]}" stroke-width="1"/>')

    parts.append('</svg>')
    return "".join(parts)


# ─── line chart ───────────────────────────────────────────────────────────

def build_line_chart(months: list[str], values: list[float | None], *, chart_id: str,
                     title: str, desc: str, y_label: str = "",
                     value_format=lambda v: format_number(v),
                     reference_lines: list[dict] | None = None) -> str:
    """Generic line chart with optional reference annotations.

    reference_lines: list of {period: 'YYYY-MM', label: str} to draw vertical markers.
    """
    n = len(months)
    pairs = [(i, v) for i, v in enumerate(values) if v is not None]
    if not pairs:
        return ""
    series_vals = [v for _, v in pairs]
    ymin_raw = min(series_vals)
    ymax_raw = max(series_vals)
    ymax = nice_axis_max(ymax_raw * 1.05)
    ymin = 0 if ymin_raw >= 0 else -nice_axis_max(-ymin_raw)

    W, H = 900, 360
    pad_l, pad_r, pad_t, pad_b = 60, 16, 28, 48
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b

    def x_of(i: int) -> float:
        return pad_l + (i / max(n - 1, 1)) * plot_w

    def y_of(v: float) -> float:
        return pad_t + plot_h - ((v - ymin) / (ymax - ymin)) * plot_h

    parts = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="{chart_id}-title {chart_id}-desc" class="cd-chart cd-chart--line" xmlns="http://www.w3.org/2000/svg">']
    parts.append(f'<title id="{chart_id}-title">{title}</title>')
    parts.append(f'<desc id="{chart_id}-desc">{desc}</desc>')

    # Y gridlines
    parts.append('<g class="cd-chart__grid">')
    for tick in axis_ticks(ymax, 5):
        y = y_of(tick)
        parts.append(f'<line x1="{pad_l}" x2="{W - pad_r}" y1="{y:.1f}" y2="{y:.1f}" stroke="{COLOURS["grid"]}" stroke-width="1"/>')
        parts.append(f'<text x="{pad_l - 8}" y="{y + 4:.1f}" text-anchor="end" font-size="11" fill="{COLOURS["text"]}" font-variant-numeric="tabular-nums">{value_format(tick)}</text>')
    parts.append('</g>')

    # Reference markers
    if reference_lines:
        parts.append('<g class="cd-chart__markers">')
        for ref in reference_lines:
            try:
                i = months.index(ref["period"])
            except ValueError:
                continue
            x = x_of(i)
            parts.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{pad_t}" y2="{pad_t + plot_h}" stroke="{COLOURS["marker"]}" stroke-width="1" stroke-dasharray="3 3"/>')
            parts.append(f'<text x="{x:.1f}" y="{pad_t - 6}" text-anchor="middle" font-size="10" fill="{COLOURS["text"]}">{ref["label"]}</text>')
        parts.append('</g>')

    # Line path
    points = " ".join(f"{x_of(i):.1f},{y_of(v):.2f}" for i, v in pairs)
    parts.append(f'<polyline points="{points}" fill="none" stroke="{COLOURS["accent"]}" stroke-width="1.6"/>')

    # Invisible hover points with <title> tooltips
    parts.append('<g class="cd-chart__points">')
    for i, v in pairs:
        # Only every Nth point to avoid SVG bloat
        step = max(1, n // 60)
        if i % step != 0 and i != pairs[-1][0]:
            continue
        cx, cy = x_of(i), y_of(v)
        tt = f"{month_label(months[i])}:{value_format(v)}"
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.2f}" r="3.5" fill="transparent" stroke="transparent"><title>{tt}</title></circle>')
    parts.append('</g>')

    # X-axis year labels
    parts.append('<g class="cd-chart__xaxis">')
    seen_years = set()
    for i, period in enumerate(months):
        year = period.split("-")[0]
        if year not in seen_years and period.endswith("-01"):
            seen_years.add(year)
            # Show every other year to avoid crowding on long ranges
            yr_int = int(year)
            if n > 100 and yr_int % 2 != 0:
                continue
            if n > 200 and yr_int % 5 != 0:
                continue
            x = x_of(i)
            parts.append(f'<text x="{x:.1f}" y="{H - pad_b + 18}" text-anchor="middle" font-size="11" fill="{COLOURS["text"]}">{year}</text>')
    parts.append('</g>')

    parts.append(f'<line x1="{pad_l}" x2="{W - pad_r}" y1="{pad_t + plot_h}" y2="{pad_t + plot_h}" stroke="{COLOURS["axis"]}" stroke-width="1"/>')

    if y_label:
        parts.append(f'<text x="14" y="{pad_t + plot_h / 2}" transform="rotate(-90, 14, {pad_t + plot_h / 2})" text-anchor="middle" font-size="11" fill="{COLOURS["text"]}">{y_label}</text>')

    parts.append('</svg>')
    return "".join(parts)


# ─── sector horizontal bar chart ──────────────────────────────────────────

def build_sector_bars(sector: dict, *, chart_id: str, top_n: int = 10) -> str:
    sections = sector["sections"][:top_n]
    if not sections:
        return ""
    n = len(sections)
    max_val = max(s["count"] for s in sections)
    xmax = nice_axis_max(max_val)

    W = 900
    row_h = 30
    pad_l, pad_r, pad_t, pad_b = 200, 60, 16, 36
    plot_w = W - pad_l - pad_r
    H = pad_t + n * row_h + pad_b

    parts = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="{chart_id}-title {chart_id}-desc" class="cd-chart cd-chart--sector" xmlns="http://www.w3.org/2000/svg">']
    parts.append(f'<title id="{chart_id}-title">Company insolvencies by industry, 12 months to {sector["window_end"]}</title>')
    parts.append(f'<desc id="{chart_id}-desc">Horizontal bar chart of company insolvencies by SIC industry section, sorted from highest to lowest count.</desc>')

    # X gridlines
    parts.append('<g class="cd-chart__grid">')
    for tick in axis_ticks(xmax, 4):
        x = pad_l + (tick / xmax) * plot_w
        parts.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{pad_t}" y2="{H - pad_b}" stroke="{COLOURS["grid"]}" stroke-width="1"/>')
        parts.append(f'<text x="{x:.1f}" y="{H - pad_b + 18}" text-anchor="middle" font-size="11" fill="{COLOURS["text"]}" font-variant-numeric="tabular-nums">{format_number(int(tick))}</text>')
    parts.append('</g>')

    parts.append('<g class="cd-chart__bars">')
    for i, sec in enumerate(sections):
        y = pad_t + i * row_h + 4
        w = (sec["count"] / xmax) * plot_w
        # Label (truncate gracefully)
        label = sec["label_short"]
        if len(label) > 28:
            label = label[:27] + "…"
        parts.append(f'<text x="{pad_l - 10}" y="{y + row_h / 2}" text-anchor="end" font-size="12" fill="{COLOURS["text"]}" dominant-baseline="middle">{label}</text>')
        parts.append(f'<rect x="{pad_l}" y="{y:.1f}" width="{w:.1f}" height="{row_h - 10}" fill="{COLOURS["bar_primary"]}"><title>{sec["label_full"]}:{format_number(sec["count"])} ({sec["share_pct"]}% of known-sector cases)</title></rect>')
        # Value at end of bar
        parts.append(f'<text x="{pad_l + w + 6:.1f}" y="{y + row_h / 2}" font-size="12" fill="{COLOURS["text"]}" dominant-baseline="middle" font-variant-numeric="tabular-nums">{format_number(sec["count"])} ({sec["share_pct"]}%)</text>')
    parts.append('</g>')

    parts.append(f'<line x1="{pad_l}" x2="{W - pad_r}" y1="{H - pad_b}" y2="{H - pad_b}" stroke="{COLOURS["axis"]}" stroke-width="1"/>')

    parts.append('</svg>')
    return "".join(parts)


# ─── orchestration ────────────────────────────────────────────────────────

def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_all_charts(json_dir: Path) -> dict[str, str]:
    """Build all chart SVGs for the data hub page."""
    monthly = _load_json(json_dir / "monthly_series.json")
    rate    = _load_json(json_dir / "rate_series.json")
    sector  = _load_json(json_dir / "sector_breakdown.json")

    months = monthly["months"]
    latest = months[-1]

    # Default view: post-COVID era (Jan 2020 onwards)
    five_years_start = months[max(0, len(months) - 60)]  # 60 months = 5 years
    since_2020 = "2020-01"
    since_2000 = "2000-01"

    charts = {
        "monthly_stacked_post_covid": build_stacked_bar(monthly, since_2020, latest, chart_id="chart-stack-pc"),
        "monthly_stacked_5y":         build_stacked_bar(monthly, five_years_start, latest, chart_id="chart-stack-5y"),
        "monthly_stacked_since_2000": build_stacked_bar(monthly, since_2000, latest, chart_id="chart-stack-all"),

        "longrun_total_line": build_line_chart(
            months, monthly["series"]["total"],
            chart_id="chart-longrun",
            title=f"Total monthly company insolvencies, England and Wales, {month_label(months[0])} to {month_label(latest)}",
            desc="Long-run line chart of total monthly company insolvencies in England and Wales, seasonally adjusted.",
            y_label="Monthly insolvencies",
            reference_lines=[
                {"period": "2009-02", "label": "2008–09 recession peak"},
                {"period": "2020-04", "label": "Covid support"},
                {"period": "2023-09", "label": "Post-Covid CVL peak"},
            ],
        ),

        "rate_line": build_line_chart(
            rate["months"], rate["rate_per_10k"],
            chart_id="chart-rate",
            title=f"12-month rolling company insolvency rate per 10,000 active companies, England and Wales",
            desc="Line chart of the 12-month rolling company insolvency rate per 10,000 active companies in England and Wales.",
            y_label="Per 10,000 companies",
            value_format=lambda v: f"{v:.1f}" if v is not None else "n/a",
        ),

        "sector_bars": build_sector_bars(sector, chart_id="chart-sector", top_n=6),
    }
    return charts


if __name__ == "__main__":
    import sys
    here = Path(__file__).resolve().parent.parent / "data" / "insolvency-statistics"
    charts = build_all_charts(here)
    out = here / "charts"
    out.mkdir(exist_ok=True)
    for name, svg in charts.items():
        (out / f"{name}.svg").write_text(svg, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    for name, svg in charts.items():
        print(f"  {name}: {len(svg):,} chars")
    print(f"\nWrote {len(charts)} SVGs to {out}")
