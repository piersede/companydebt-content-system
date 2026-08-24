#!/usr/bin/env python3
"""Second-pass pulls for the weekly audit: the queries the API rejected on the
first pass, plus negatives, geo and audience context. Read-only.

Usage:
    python scripts/weekly_audit_pull2.py --run 2026-08-20-weekly-audit \
        --primary 2026-08-11 2026-08-17
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
from weekly_audit_pull import EXE, load_env  # noqa: E402

SERVING = ("21716142426", "21268756208")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--primary", nargs=2, required=True)
    args = ap.parse_args()

    cfg = yaml.safe_load((ROOT / "accounts" / "company-debt.yml").read_text(encoding="utf-8"))
    cid = cfg["customer_id"]
    p0, p1 = args.primary
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
            return
        print(f"[ok]   {label}: {len(rows)} rows")
        results[label] = rows

    between = f"segments.date BETWEEN '{p0}' AND '{p1}'"

    run(
        "keyword_performance",
        [
            "campaign.name",
            "ad_group.name",
            "ad_group_criterion.keyword.text",
            "ad_group_criterion.keyword.match_type",
            "ad_group_criterion.status",
            "metrics.impressions",
            "metrics.clicks",
            "metrics.cost_micros",
            "metrics.conversions",
            "metrics.all_conversions",
            "metrics.average_cpc",
        ],
        "keyword_view",
        [between, "metrics.impressions > 0"],
        ["metrics.cost_micros DESC"],
    )

    run(
        "pmax_search_categories",
        [
            "campaign_search_term_insight.category_label",
            "campaign_search_term_insight.id",
            "metrics.impressions",
            "metrics.clicks",
            "metrics.conversions",
        ],
        "campaign_search_term_insight",
        [between, "campaign_search_term_insight.campaign_id = 21268756208"],
        ["metrics.impressions DESC"],
    )

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
            "change_event.change_date_time DURING LAST_14_DAYS",
            "change_event.change_resource_type IN ('CAMPAIGN_BUDGET','CAMPAIGN','AD_GROUP','AD_GROUP_AD','AD_GROUP_CRITERION','CAMPAIGN_CRITERION')",
        ],
        ["change_event.change_date_time DESC"],
        limit=500,
    )

    run(
        "campaign_negatives",
        [
            "campaign.id",
            "campaign.name",
            "campaign_criterion.criterion_id",
            "campaign_criterion.type",
            "campaign_criterion.negative",
            "campaign_criterion.keyword.text",
            "campaign_criterion.keyword.match_type",
        ],
        "campaign_criterion",
        [
            "campaign_criterion.negative = TRUE",
            "campaign_criterion.type = 'KEYWORD'",
            f"campaign.id IN ({','.join(SERVING)})",
        ],
    )

    run(
        "shared_negative_lists",
        [
            "shared_set.id",
            "shared_set.name",
            "shared_set.type",
            "shared_set.status",
            "shared_set.member_count",
        ],
        "shared_set",
        ["shared_set.status = 'ENABLED'"],
    )

    run(
        "shared_negative_members",
        [
            "shared_set.name",
            "shared_criterion.criterion_id",
            "shared_criterion.type",
            "shared_criterion.keyword.text",
            "shared_criterion.keyword.match_type",
        ],
        "shared_criterion",
        ["shared_criterion.type = 'KEYWORD'"],
    )

    run(
        "campaign_shared_sets",
        ["campaign.id", "campaign.name", "shared_set.name", "campaign_shared_set.status"],
        "campaign_shared_set",
        [f"campaign.id IN ({','.join(SERVING)})"],
    )

    run(
        "geo_performance",
        [
            "campaign.name",
            "geographic_view.country_criterion_id",
            "geographic_view.location_type",
            "metrics.impressions",
            "metrics.clicks",
            "metrics.cost_micros",
            "metrics.conversions",
        ],
        "geographic_view",
        [between, "metrics.impressions > 0"],
        ["metrics.impressions DESC"],
    )

    run(
        "ad_schedule",
        [
            "campaign.id",
            "campaign.name",
            "campaign_criterion.type",
            "campaign_criterion.ad_schedule.day_of_week",
            "campaign_criterion.ad_schedule.start_hour",
            "campaign_criterion.ad_schedule.end_hour",
        ],
        "campaign_criterion",
        [
            "campaign_criterion.type = 'AD_SCHEDULE'",
            f"campaign.id IN ({','.join(SERVING)})",
        ],
    )

    run(
        "campaign_settings",
        [
            "campaign.id",
            "campaign.name",
            "campaign.url_expansion_opt_out",
            "campaign.optimization_score",
            "campaign.network_settings.target_google_search",
            "campaign.network_settings.target_search_network",
            "campaign.network_settings.target_content_network",
            "campaign.network_settings.target_partner_search_network",
            "campaign.target_cpa.target_cpa_micros",
            "campaign.maximize_conversions.target_cpa_micros",
        ],
        "campaign",
        [f"campaign.id IN ({','.join(SERVING)})"],
    )

    session.close()
    for label, rows in results.items():
        (out_dir / f"{label}.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(f"\nsaved to {out_dir}")


if __name__ == "__main__":
    main()
