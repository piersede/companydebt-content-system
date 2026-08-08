#!/usr/bin/env python3
"""Ad-hoc pull for the budget / impression-share reallocation review.

Read-only. Pulls campaign performance + impression share for a 30-day and a
90-day window, plus budget structure and a conversion-action breakdown, and
writes them to runs/<date>-budget-is-review/.

Usage:
    python scripts/adhoc_budget_is.py
"""

import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from run_snapshot import MCPSession  # noqa: E402

EXE = (
    r"C:\Users\piers\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache"
    r"\Local\pipx\pipx\venvs\google-ads-mcp\Scripts\google-ads-mcp.exe"
)

CAMPAIGN_FIELDS = [
    "campaign.id",
    "campaign.name",
    "campaign.status",
    "campaign.advertising_channel_type",
    "campaign.bidding_strategy_type",
    "campaign_budget.id",
    "campaign_budget.amount_micros",
    "campaign_budget.explicitly_shared",
    "metrics.cost_micros",
    "metrics.impressions",
    "metrics.clicks",
    "metrics.ctr",
    "metrics.average_cpc",
    "metrics.conversions",
    "metrics.conversions_value",
    "metrics.all_conversions",
    "metrics.search_impression_share",
    "metrics.search_budget_lost_impression_share",
    "metrics.search_rank_lost_impression_share",
    "metrics.search_top_impression_share",
    "metrics.search_absolute_top_impression_share",
]

CONV_FIELDS = [
    "campaign.id",
    "campaign.name",
    "campaign.advertising_channel_type",
    "segments.conversion_action_name",
    "segments.conversion_action_category",
    "metrics.conversions",
    "metrics.all_conversions",
]

CONV_ACTION_FIELDS = [
    "conversion_action.id",
    "conversion_action.name",
    "conversion_action.status",
    "conversion_action.type",
    "conversion_action.category",
    "conversion_action.primary_for_goal",
    "conversion_action.counting_type",
    "conversion_action.include_in_conversions_metric",
]


def main():
    config = yaml.safe_load((ROOT / "accounts" / "company-debt.yml").read_text(encoding="utf-8"))
    cid = config["customer_id"]

    end = date.today() - timedelta(days=1)
    w30 = end - timedelta(days=29)
    w90 = end - timedelta(days=89)

    env = os.environ.copy()
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()

    out_dir = ROOT / "runs" / f"{date.today().isoformat()}-budget-is-review"
    out_dir.mkdir(parents=True, exist_ok=True)

    session = MCPSession(EXE, env)
    results = {}

    def run(label, fields, resource, conditions, orderings=None):
        print(f"-> {label}")
        try:
            rows = session.call_tool(
                "search_search",
                {
                    "customer_id": cid,
                    "fields": fields,
                    "resource": resource,
                    "conditions": conditions,
                    "orderings": orderings or [],
                },
            )
        except Exception as e:
            print(f"   FAILED: {e}")
            results[label] = {"error": str(e)}
            return
        print(f"   {len(rows)} rows")
        results[label] = rows

    for label, start in (("campaigns_30d", w30), ("campaigns_90d", w90)):
        run(
            label,
            CAMPAIGN_FIELDS,
            "campaign",
            [
                f"segments.date BETWEEN '{start.isoformat()}' AND '{end.isoformat()}'",
                "campaign.status != 'REMOVED'",
                "metrics.impressions > 0",
            ],
            ["metrics.cost_micros DESC"],
        )

    run(
        "conversion_breakdown_90d",
        CONV_FIELDS,
        "campaign",
        [
            f"segments.date BETWEEN '{w90.isoformat()}' AND '{end.isoformat()}'",
            "campaign.status != 'REMOVED'",
        ],
        ["metrics.conversions DESC"],
    )

    run(
        "conversion_actions",
        CONV_ACTION_FIELDS,
        "conversion_action",
        ["conversion_action.status != 'REMOVED'"],
    )

    session.close()

    payload = {
        "customer_id": cid,
        "window_30d": [w30.isoformat(), end.isoformat()],
        "window_90d": [w90.isoformat(), end.isoformat()],
        "data": results,
    }
    (out_dir / "raw.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nsaved {out_dir / 'raw.json'}")


if __name__ == "__main__":
    main()
