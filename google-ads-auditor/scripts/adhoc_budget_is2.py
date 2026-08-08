#!/usr/bin/env python3
"""Second read-only pull for the budget / impression-share review:
campaign settings + experiment status, budget pools, and daily spend."""

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


def main():
    config = yaml.safe_load((ROOT / "accounts" / "company-debt.yml").read_text(encoding="utf-8"))
    cid = config["customer_id"]
    end = date.today() - timedelta(days=1)
    w30 = end - timedelta(days=29)

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
            rows = session.call_tool("search_search", {
                "customer_id": cid, "fields": fields, "resource": resource,
                "conditions": conditions, "orderings": orderings or [],
            })
        except Exception as e:
            print(f"   FAILED: {e}")
            results[label] = {"error": str(e)}
            return
        print(f"   {len(rows)} rows")
        results[label] = rows

    run("campaign_settings", [
        "campaign.id", "campaign.name", "campaign.status", "campaign.serving_status",
        "campaign.experiment_type", "campaign.start_date", "campaign.end_date",
        "campaign.advertising_channel_type", "campaign.bidding_strategy_type",
        "campaign.maximize_conversions.target_cpa_micros",
        "campaign.target_cpa.target_cpa_micros",
        "campaign_budget.id", "campaign_budget.name", "campaign_budget.amount_micros",
        "campaign_budget.explicitly_shared", "campaign_budget.status",
        "campaign.network_settings.target_search_network",
        "campaign.network_settings.target_content_network",
        "campaign.network_settings.target_partner_search_network",
    ], "campaign", ["campaign.status = 'ENABLED'"])

    run("budgets", [
        "campaign_budget.id", "campaign_budget.name", "campaign_budget.amount_micros",
        "campaign_budget.explicitly_shared", "campaign_budget.status",
        "campaign_budget.reference_count", "campaign_budget.has_recommended_budget",
        "campaign_budget.recommended_budget_amount_micros",
    ], "campaign_budget", ["campaign_budget.status = 'ENABLED'"])

    run("daily_30d", [
        "campaign.id", "campaign.name", "segments.date",
        "metrics.cost_micros", "metrics.clicks", "metrics.conversions",
        "metrics.search_budget_lost_impression_share",
    ], "campaign", [
        f"segments.date BETWEEN '{w30.isoformat()}' AND '{end.isoformat()}'",
        "metrics.impressions > 0",
    ], ["segments.date ASC"])

    session.close()
    (out_dir / "raw2.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nsaved {out_dir / 'raw2.json'}")


if __name__ == "__main__":
    main()
