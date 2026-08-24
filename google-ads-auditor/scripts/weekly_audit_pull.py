#!/usr/bin/env python3
"""Weekly Google Ads audit pull for Company Debt. Read-only.

Pulls, for a primary week plus a prior week and a trailing tail:
  - campaign performance and impression share (totals and by day)
  - Performance Max split by network type
  - device and hour-of-day splits
  - every search term (Search campaigns) and every enabled keyword
  - Performance Max search *category* insights (not terms)
  - ad-level and asset-group-level policy status
  - current budgets, serving status, and account budget/balance if exposed

Everything lands in runs/<run-name>/raw/*.json. Nothing is written to the
account.

Usage:
    python scripts/weekly_audit_pull.py --run 2026-08-20-weekly-audit \
        --primary 2026-08-11 2026-08-17 --prior 2026-08-04 2026-08-10 \
        --tail 2026-08-18 2026-08-19
"""

import argparse
import json
import os
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from run_snapshot import MCPSession  # noqa: E402

EXE = (
    r"C:\Users\piers\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache"
    r"\Local\pipx\pipx\venvs\google-ads-mcp\Scripts\google-ads-mcp.exe"
)

PERF = [
    "metrics.cost_micros",
    "metrics.impressions",
    "metrics.clicks",
    "metrics.ctr",
    "metrics.average_cpc",
    "metrics.conversions",
    "metrics.all_conversions",
]

IS_FIELDS = [
    "metrics.search_impression_share",
    "metrics.search_budget_lost_impression_share",
    "metrics.search_rank_lost_impression_share",
    "metrics.search_top_impression_share",
    "metrics.search_absolute_top_impression_share",
]

CAMPAIGN_ID = ["campaign.id", "campaign.name"]


def load_env():
    env = os.environ.copy()
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
    return env


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--primary", nargs=2, required=True)
    ap.add_argument("--prior", nargs=2, required=True)
    ap.add_argument("--tail", nargs=2, required=True)
    args = ap.parse_args()

    cfg = yaml.safe_load((ROOT / "accounts" / "company-debt.yml").read_text(encoding="utf-8"))
    cid = cfg["customer_id"]

    p0, p1 = args.primary
    q0, q1 = args.prior
    t0, t1 = args.tail
    span0, span1 = q0, t1  # whole stretch, prior week through tail

    out_dir = ROOT / "runs" / args.run / "raw"
    out_dir.mkdir(parents=True, exist_ok=True)

    session = MCPSession(EXE, load_env())
    results = {}

    def run(label, fields, resource, conditions, orderings=None, limit=None):
        payload = {
            "customer_id": cid,
            "fields": fields,
            "resource": resource,
            "conditions": conditions,
            "orderings": orderings or [],
        }
        if limit:
            payload["limit"] = limit
        try:
            rows = session.call_tool("search_search", payload)
        except Exception as e:
            print(f"[FAIL] {label}: {e}")
            results[label] = {"error": str(e)}
            return []
        print(f"[ok]   {label}: {len(rows)} rows")
        results[label] = rows
        return rows

    def between(a, b):
        return f"segments.date BETWEEN '{a}' AND '{b}'"

    # ---- structure: budgets and serving status (no date segment) ----
    run(
        "campaign_structure",
        CAMPAIGN_ID + [
            "campaign.status",
            "campaign.serving_status",
            "campaign.advertising_channel_type",
            "campaign.bidding_strategy_type",
            "campaign.experiment_type",
            "campaign_budget.id",
            "campaign_budget.name",
            "campaign_budget.amount_micros",
            "campaign_budget.explicitly_shared",
            "campaign_budget.delivery_method",
        ],
        "campaign",
        ["campaign.status != 'REMOVED'"],
    )

    run(
        "account_budget",
        [
            "account_budget.id",
            "account_budget.name",
            "account_budget.status",
            "account_budget.approved_spending_limit_micros",
            "account_budget.amount_served_micros",
            "account_budget.total_adjustments_micros",
        ],
        "account_budget",
        [],
    )

    run(
        "billing_setup",
        ["billing_setup.id", "billing_setup.status", "billing_setup.payments_account_info.payments_account_name"],
        "billing_setup",
        [],
    )

    # ---- campaign performance, three windows ----
    for label, (a, b) in (
        ("campaign_primary", (p0, p1)),
        ("campaign_prior", (q0, q1)),
        ("campaign_tail", (t0, t1)),
    ):
        run(
            label,
            CAMPAIGN_ID + ["campaign.advertising_channel_type", "campaign.serving_status"] + PERF + IS_FIELDS,
            "campaign",
            [between(a, b), "campaign.status != 'REMOVED'", "metrics.impressions > 0"],
            ["metrics.cost_micros DESC"],
        )

    run(
        "campaign_by_day",
        CAMPAIGN_ID + ["segments.date", "campaign.advertising_channel_type"] + PERF + IS_FIELDS,
        "campaign",
        [between(span0, span1), "campaign.status != 'REMOVED'", "metrics.impressions > 0"],
        ["segments.date ASC"],
    )

    run(
        "campaign_by_network",
        CAMPAIGN_ID + ["segments.ad_network_type"] + PERF,
        "campaign",
        [between(p0, p1), "campaign.status != 'REMOVED'", "metrics.impressions > 0"],
        ["metrics.cost_micros DESC"],
    )

    run(
        "campaign_by_network_prior",
        CAMPAIGN_ID + ["segments.ad_network_type"] + PERF,
        "campaign",
        [between(q0, q1), "campaign.status != 'REMOVED'", "metrics.impressions > 0"],
        ["metrics.cost_micros DESC"],
    )

    run(
        "campaign_by_device",
        CAMPAIGN_ID + ["segments.device"] + PERF,
        "campaign",
        [between(p0, p1), "campaign.status != 'REMOVED'", "metrics.impressions > 0"],
        ["metrics.cost_micros DESC"],
    )

    run(
        "campaign_by_hour",
        CAMPAIGN_ID + ["segments.hour", "segments.day_of_week"] + PERF,
        "campaign",
        [between(p0, p1), "campaign.status != 'REMOVED'", "metrics.impressions > 0"],
        ["segments.hour ASC"],
    )

    # ---- conversions by action ----
    for label, (a, b) in (("conv_primary", (p0, p1)), ("conv_prior", (q0, q1))):
        run(
            label,
            CAMPAIGN_ID + [
                "segments.conversion_action_name",
                "segments.conversion_action_category",
                "metrics.conversions",
                "metrics.all_conversions",
            ],
            "campaign",
            [between(a, b), "campaign.status != 'REMOVED'"],
            ["metrics.all_conversions DESC"],
        )

    # ---- search terms ----
    for label, (a, b) in (("search_terms_primary", (p0, p1)), ("search_terms_prior", (q0, q1))):
        run(
            label,
            [
                "search_term_view.search_term",
                "search_term_view.status",
                "segments.search_term_match_type",
                "campaign.id",
                "campaign.name",
                "ad_group.id",
                "ad_group.name",
                "metrics.impressions",
                "metrics.clicks",
                "metrics.cost_micros",
                "metrics.conversions",
                "metrics.all_conversions",
            ],
            "search_term_view",
            [between(a, b)],
            ["metrics.impressions DESC"],
        )

    # ---- keywords: structure and performance ----
    run(
        "keywords_structure",
        [
            "campaign.id",
            "campaign.name",
            "campaign.serving_status",
            "ad_group.id",
            "ad_group.name",
            "ad_group.status",
            "ad_group_criterion.criterion_id",
            "ad_group_criterion.keyword.text",
            "ad_group_criterion.keyword.match_type",
            "ad_group_criterion.status",
            "ad_group_criterion.negative",
            "ad_group_criterion.system_serving_status",
            "ad_group_criterion.approval_status",
            "ad_group_criterion.quality_info.quality_score",
        ],
        "ad_group_criterion",
        [
            "ad_group_criterion.type = 'KEYWORD'",
            "ad_group_criterion.status != 'REMOVED'",
            "campaign.status = 'ENABLED'",
        ],
    )

    run(
        "keyword_performance",
        [
            "campaign.name",
            "ad_group.name",
            "ad_group_criterion.keyword.text",
            "ad_group_criterion.keyword.match_type",
            "metrics.impressions",
            "metrics.clicks",
            "metrics.cost_micros",
            "metrics.conversions",
            "metrics.all_conversions",
            "metrics.search_impression_share",
            "metrics.search_budget_lost_impression_share",
            "metrics.search_rank_lost_impression_share",
        ],
        "keyword_view",
        [between(p0, p1), "metrics.impressions > 0"],
        ["metrics.cost_micros DESC"],
    )

    run(
        "ad_groups",
        [
            "campaign.id",
            "campaign.name",
            "ad_group.id",
            "ad_group.name",
            "ad_group.status",
            "ad_group.type",
        ],
        "ad_group",
        ["ad_group.status != 'REMOVED'", "campaign.status = 'ENABLED'"],
    )

    # ---- Performance Max: category insights, asset groups, listings ----
    run(
        "pmax_search_categories",
        [
            "campaign_search_term_insight.category_label",
            "campaign_search_term_insight.id",
            "metrics.impressions",
            "metrics.clicks",
            "metrics.conversions",
            "metrics.all_conversions",
        ],
        "campaign_search_term_insight",
        [between(p0, p1), "campaign_search_term_insight.campaign_id = 21268756208"],
        ["metrics.impressions DESC"],
    )

    run(
        "asset_groups",
        [
            "campaign.id",
            "campaign.name",
            "asset_group.id",
            "asset_group.name",
            "asset_group.status",
            "asset_group.primary_status",
            "asset_group.primary_status_reasons",
            "asset_group.ad_strength",
        ],
        "asset_group",
        ["campaign.status = 'ENABLED'"],
    )

    run(
        "asset_group_perf",
        [
            "campaign.name",
            "asset_group.name",
            "metrics.impressions",
            "metrics.clicks",
            "metrics.cost_micros",
            "metrics.conversions",
        ],
        "asset_group",
        [between(p0, p1), "campaign.status = 'ENABLED'"],
        ["metrics.cost_micros DESC"],
    )

    # ---- policy status ----
    run(
        "ad_policy",
        [
            "campaign.id",
            "campaign.name",
            "ad_group.name",
            "ad_group_ad.ad.id",
            "ad_group_ad.ad.type",
            "ad_group_ad.status",
            "ad_group_ad.policy_summary.approval_status",
            "ad_group_ad.policy_summary.review_status",
            "ad_group_ad.policy_summary.policy_topic_entries",
        ],
        "ad_group_ad",
        ["ad_group_ad.status != 'REMOVED'", "campaign.status = 'ENABLED'"],
    )

    run(
        "ad_performance",
        [
            "campaign.name",
            "ad_group.name",
            "ad_group_ad.ad.id",
            "ad_group_ad.policy_summary.approval_status",
            "metrics.impressions",
            "metrics.clicks",
            "metrics.cost_micros",
            "metrics.conversions",
        ],
        "ad_group_ad",
        [between(p0, p1), "campaign.status = 'ENABLED'"],
        ["metrics.impressions DESC"],
    )

    run(
        "asset_policy",
        [
            "campaign.name",
            "asset_group.name",
            "asset_group_asset.field_type",
            "asset_group_asset.status",
            "asset_group_asset.policy_summary.approval_status",
            "asset_group_asset.policy_summary.review_status",
            "asset_group_asset.policy_summary.policy_topic_entries",
            "asset.id",
            "asset.type",
            "asset.name",
        ],
        "asset_group_asset",
        ["campaign.status = 'ENABLED'"],
    )

    # ---- landing pages ----
    run(
        "landing_pages",
        [
            "campaign.name",
            "landing_page_view.unexpanded_final_url",
            "metrics.impressions",
            "metrics.clicks",
            "metrics.cost_micros",
            "metrics.conversions",
        ],
        "landing_page_view",
        [between(p0, p1), "metrics.impressions > 0"],
        ["metrics.clicks DESC"],
    )

    # ---- recent change history ----
    run(
        "change_events",
        [
            "change_event.change_date_time",
            "change_event.change_resource_type",
            "change_event.resource_change_operation",
            "change_event.user_email",
            "change_event.changed_fields",
            "change_event.campaign",
            "change_event.old_resource",
            "change_event.new_resource",
        ],
        "change_event",
        [
            "change_event.change_date_time DURING LAST_30_DAYS",
            "change_event.change_resource_type IN ('CAMPAIGN_BUDGET','CAMPAIGN','AD_GROUP','AD_GROUP_AD','AD_GROUP_CRITERION','CAMPAIGN_CRITERION')",
        ],
        ["change_event.change_date_time DESC"],
        limit=500,
    )

    session.close()

    for label, rows in results.items():
        (out_dir / f"{label}.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    (out_dir / "_index.json").write_text(
        json.dumps(
            {
                "customer_id": cid,
                "primary": [p0, p1],
                "prior": [q0, q1],
                "tail": [t0, t1],
                "labels": {k: (len(v) if isinstance(v, list) else "ERROR") for k, v in results.items()},
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"\nsaved to {out_dir}")


if __name__ == "__main__":
    main()
