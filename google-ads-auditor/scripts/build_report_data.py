#!/usr/bin/env python3
"""Compute the mechanical, non-judgement parts of the weekly audit report
(headline numbers with a real previous-period comparison, ranked priority
actions, per-category finding groups) so the orchestrator has no reason to
hand-calculate or invent a figure when writing the narrative sections.

Usage:
    python scripts/build_report_data.py <run-folder>

Writes <run-folder>/report-data.json. Requires reconciled-findings.json
(run scripts/merge-findings.py first) and the raw snapshot files.
"""

import json
import sys
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")


def load(path):
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def pct_change(current, previous):
    if previous == 0:
        return None  # can't express a meaningful percent change from zero
    return (current - previous) / previous


def main():
    if len(sys.argv) != 2:
        print("Usage: python build_report_data.py <run-folder>", file=sys.stderr)
        sys.exit(2)

    run_dir = Path(sys.argv[1])
    raw_dir = run_dir / "raw"

    manifest = load(run_dir / "manifest.json")
    reconciled = load(run_dir / "reconciled-findings.json")
    campaigns = load(raw_dir / "campaigns.json")
    daily = load(raw_dir / "daily-performance.json")
    config = yaml.safe_load((run_dir / "account-config.yml").read_text(encoding="utf-8"))

    if manifest is None or campaigns is None:
        print("ERROR: manifest.json and raw/campaigns.json are required", file=sys.stderr)
        sys.exit(2)
    if reconciled is None:
        print("ERROR: reconciled-findings.json not found - run scripts/merge-findings.py first", file=sys.stderr)
        sys.exit(2)

    # --- Headline numbers: audit period from campaigns.json (authoritative,
    # its own query is scoped to audit_start/audit_end directly) ---
    audit_cost = sum(c.get("metrics.cost_micros", 0) for c in campaigns) / 1_000_000
    audit_impr = sum(c.get("metrics.impressions", 0) for c in campaigns)
    audit_clicks = sum(c.get("metrics.clicks", 0) for c in campaigns)
    audit_conv = sum(c.get("metrics.conversions", 0) for c in campaigns)
    audit_conv_value = sum(c.get("metrics.conversions_value", 0) for c in campaigns)

    # --- Previous period: filter daily-performance.json to comparison_start/end ---
    data_completeness_notes = []
    prev_cost = prev_impr = prev_clicks = prev_conv = prev_conv_value = None
    previous_period_complete = False
    if daily is not None:
        comp_start, comp_end = manifest["comparison_start"], manifest["comparison_end"]
        prev_rows = [r for r in daily if comp_start <= r["segments.date"] <= comp_end]
        daily_dates = sorted(set(r["segments.date"] for r in daily))
        expected_days = (
            __import__("datetime").date.fromisoformat(manifest["context_end"])
            - __import__("datetime").date.fromisoformat(manifest["context_start"])
        ).days + 1
        if daily_dates and len(daily_dates) < expected_days:
            data_completeness_notes.append(
                f"daily-performance.json covers {daily_dates[0]} to {daily_dates[-1]} "
                f"({len(daily_dates)} of {expected_days} expected context days) - the most recent 1-2 days are "
                "commonly incomplete in Google Ads reporting at generation time, not a query failure."
            )
        expected_comp_days = (
            __import__("datetime").date.fromisoformat(comp_end)
            - __import__("datetime").date.fromisoformat(comp_start)
        ).days + 1
        covered_comp_dates = sorted(set(r["segments.date"] for r in prev_rows))
        previous_period_complete = len(covered_comp_dates) == expected_comp_days
        if covered_comp_dates and not previous_period_complete:
            data_completeness_notes.append(
                f"Previous-period comparison ({comp_start} to {comp_end}, {expected_comp_days} days) is only "
                f"partially covered by daily-performance.json (actual coverage: {covered_comp_dates[0]} to "
                f"{covered_comp_dates[-1]}, {len(covered_comp_dates)} days) - percent-change figures are "
                "suppressed rather than computed from a mismatched day count, which would understate the "
                "audit period's real change."
            )
        if prev_rows:
            prev_cost = sum(r.get("metrics.cost_micros", 0) for r in prev_rows) / 1_000_000
            prev_impr = sum(r.get("metrics.impressions", 0) for r in prev_rows)
            prev_clicks = sum(r.get("metrics.clicks", 0) for r in prev_rows)
            prev_conv = sum(r.get("metrics.conversions", 0) for r in prev_rows)
            prev_conv_value = sum(r.get("metrics.conversions_value", 0) for r in prev_rows)
    else:
        data_completeness_notes.append("daily-performance.json not found - no previous-period comparison available.")

    def change_or_none(current, previous):
        if not previous_period_complete or previous is None:
            return None
        return pct_change(current, previous)

    headline = {
        "previous_period_complete": previous_period_complete,
        "spend_gbp": {"audit": round(audit_cost, 2), "previous": round(prev_cost, 2) if prev_cost is not None else None,
                       "change_pct": change_or_none(audit_cost, prev_cost)},
        "impressions": {"audit": audit_impr, "previous": prev_impr, "change_pct": change_or_none(audit_impr, prev_impr)},
        "clicks": {"audit": audit_clicks, "previous": prev_clicks, "change_pct": change_or_none(audit_clicks, prev_clicks)},
        "primary_conversions": {"audit": audit_conv, "previous": prev_conv, "change_pct": change_or_none(audit_conv, prev_conv)},
        "cpa_gbp": {"audit": round(audit_cost / audit_conv, 2) if audit_conv else None,
                     "previous": round(prev_cost / prev_conv, 2) if prev_conv else None},
        "conversion_value_gbp": {"audit": round(audit_conv_value, 2), "previous": round(prev_conv_value, 2) if prev_conv_value is not None else None} if audit_conv_value or (prev_conv_value or 0) else None,
        "roas": None,  # conversions_value is 0 across this account - no ROAS to report, per template's "only show metrics that apply"
    }

    # --- Priority actions: top N by severity/confidence rank, already sorted by merge-findings.py ---
    max_actions = config.get("reporting", {}).get("maximum_priority_actions", 10)
    include_low_conf = config.get("reporting", {}).get("include_low_confidence_findings", True)
    findings = reconciled["findings"]
    eligible = findings if include_low_conf else [f for f in findings if f.get("confidence") != "low"]
    priority_actions = eligible[:max_actions]

    # --- Group by source skill / category for the report's section-by-section tables ---
    by_skill = {}
    for f in findings:
        by_skill.setdefault(f.get("source_skill", "unknown"), []).append(f)

    # --- Dormant-campaign budget summary: distinct budget pools, not summed per-campaign
    # (a budget shared by N dormant campaigns must count once, not N times) ---
    dormant = [f for f in findings if f.get("category") == "dormant-campaign"]
    distinct_budgets = {}
    for f in dormant:
        bid = f.get("evidence", {}).get("campaign_budget_id")
        amt = f.get("evidence", {}).get("daily_budget_gbp")
        if bid is not None and amt is not None:
            distinct_budgets[bid] = amt
    unexplained_dormant = [f for f in dormant if f.get("confidence") == "low"]
    dormant_campaign_summary = {
        "dormant_campaign_count": len(dormant),
        "distinct_budget_pool_count": len(distinct_budgets),
        "distinct_daily_budget_gbp": round(sum(distinct_budgets.values()), 2),
        "unexplained_dormant_count": len(unexplained_dormant),
        "unexplained_dormant_campaigns": [
            {"campaign": f["campaign"], "daily_budget_gbp": f["evidence"]["daily_budget_gbp"], "finding_id": f["finding_id"]}
            for f in unexplained_dormant
        ],
    }

    report_data = {
        "account_name": manifest["account_name"],
        "customer_id": manifest["customer_id"],
        "currency": manifest["currency"],
        "audit_start": manifest["audit_start"],
        "audit_end": manifest["audit_end"],
        "comparison_start": manifest["comparison_start"],
        "comparison_end": manifest["comparison_end"],
        "generated_at": manifest["generated_at"],
        "data_complete": manifest["data_complete"],
        "failed_queries": manifest.get("failed_queries", []),
        "manifest_warnings": manifest.get("warnings", []),
        "reconciliation": manifest.get("reconciliation"),
        "headline_numbers": headline,
        "data_completeness_notes": data_completeness_notes,
        "total_findings": reconciled["total_findings"],
        "duplicates_removed": reconciled["duplicates_removed"],
        "conflicting_groups": reconciled["conflicting_groups"],
        "priority_actions": priority_actions,
        "dormant_campaign_summary": dormant_campaign_summary,
        "findings_by_skill": {
            "negative-keyword-miner": by_skill.get("negative-keyword-miner", []),
            "search-terms-analyzer": by_skill.get("search-terms-analyzer", []),
            "ad-performance-diagnostic": by_skill.get("ad-performance-diagnostic", []),
            "performance-max-auditor": by_skill.get("performance-max-auditor", []),
        },
    }

    out_path = run_dir / "report-data.json"
    out_path.write_text(json.dumps(report_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {out_path}")
    print(f"  {len(priority_actions)} priority action(s) selected (max {max_actions}, include_low_confidence={include_low_conf})")
    if data_completeness_notes:
        print(f"  {len(data_completeness_notes)} data-completeness note(s) recorded")


if __name__ == "__main__":
    main()
