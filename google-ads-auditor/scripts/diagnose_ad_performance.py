#!/usr/bin/env python3
"""Reference implementation of the ad-performance-diagnostic skill
(.claude/skills/ad-performance-diagnostic/SKILL.md). Deterministic — same
snapshot always produces the same findings.

Usage:
    python scripts/diagnose_ad_performance.py <run-or-fixture-folder>

<run-or-fixture-folder> must contain campaigns.json, account-baseline.json,
and impression-share.json, plus account-config.yml (either a
runs/YYYY-MM-DD-<slug>/ folder or a tests/fixtures/<scenario>/ folder — same
shape). ads.json and keywords.json are optional — if present, they sharpen
the dormant-campaign diagnosis; if absent, Check 1 states plainly that
ads/keywords couldn't be checked.

MICRO_MIN_BUDGET is deliberately generous ("near-zero") rather than
literally zero — a shared or trivial budget still technically has
amount_micros > 0.
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

NEAR_ZERO_BUDGET_GBP = 1.0


def load(folder, name):
    path = folder / name
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def severity_for_budget(daily_gbp):
    if daily_gbp >= 50:
        return "high"
    if daily_gbp >= 10:
        return "medium"
    return "low"


def main():
    if len(sys.argv) != 2:
        print("Usage: python diagnose_ad_performance.py <run-or-fixture-folder>", file=sys.stderr)
        sys.exit(2)

    folder = Path(sys.argv[1])
    raw = folder / "raw" if (folder / "raw").exists() else folder

    campaigns = load(raw, "campaigns.json")
    baseline = load(raw, "account-baseline.json")
    impression_share = load(raw, "impression-share.json")
    ads = load(raw, "ads.json")  # optional
    keywords = load(raw, "keywords.json")  # optional
    config = yaml.safe_load((folder / "account-config.yml").read_text(encoding="utf-8"))

    if campaigns is None or baseline is None or impression_share is None:
        print("ERROR: campaigns.json, account-baseline.json, and impression-share.json are all required", file=sys.stderr)
        sys.exit(2)

    manifest = load(folder, "manifest.json")
    if manifest:
        period = {"start": manifest["audit_start"], "end": manifest["audit_end"]}
    else:
        period = config.get("_period", {"start": "UNKNOWN", "end": "UNKNOWN"})

    enabled_ids = {c["campaign.id"] for c in campaigns if c["campaign.status"] == "ENABLED"}
    campaign_by_id = {c["campaign.id"]: c for c in campaigns}

    baseline_by_id = {b["campaign.id"]: b for b in baseline if b["campaign.id"] in enabled_ids}
    is_by_id = {i["campaign.id"]: i for i in impression_share if i["campaign.id"] in enabled_ids}

    # --- Check 2 first: shared-budget clusters (Check 1 references this) ---
    by_budget_id = defaultdict(list)
    for cid, b in baseline_by_id.items():
        by_budget_id[b["campaign_budget.id"]].append(cid)
    shared_clusters = {bid: cids for bid, cids in by_budget_id.items() if len(cids) > 1}
    cluster_of_campaign = {}
    for bid, cids in shared_clusters.items():
        for cid in cids:
            cluster_of_campaign[cid] = bid

    findings = []
    counter = 1

    # --- Check 1: dormant ENABLED campaigns ---
    dormant_count = 0
    for cid in enabled_ids:
        b = baseline_by_id.get(cid)
        i = is_by_id.get(cid)
        if b is None or i is None:
            continue  # not a Search campaign, or missing baseline — out of scope for this check
        budget_gbp = b["campaign_budget.amount_micros"] / 1_000_000
        if budget_gbp <= 0:
            continue  # genuinely £0 budget is a different, more obvious problem
        if i.get("metrics.search_impression_share", 0) > 0:
            continue  # it's delivering — not dormant

        dormant_count += 1
        campaign_name = campaign_by_id[cid]["campaign.name"]

        explanations = []
        checked = []

        if cid in cluster_of_campaign:
            cluster_size = len(shared_clusters[cluster_of_campaign[cid]])
            explanations.append(
                f"shares campaign_budget.id {cluster_of_campaign[cid]} (£{budget_gbp:.2f}/day) with "
                f"{cluster_size - 1} other ENABLED campaign(s) — whichever wins auctions first may be "
                "exhausting the shared budget before this one gets a look-in."
            )
        elif budget_gbp < NEAR_ZERO_BUDGET_GBP:
            explanations.append(f"budget is £{budget_gbp:.2f}/day — near-zero, likely too small to win any auction.")
        checked.append("budget-sharing/near-zero")

        if ads is not None:
            campaign_ads = [a for a in ads if a.get("campaign.id") == cid]
            if campaign_ads:
                statuses = {a["ad_group_ad.status"] for a in campaign_ads}
                if statuses <= {"PAUSED", "REMOVED"}:
                    explanations.append(f"every ad in this campaign is {'/'.join(sorted(statuses))} — nothing eligible to serve.")
                checked.append("ad status")

        if keywords is not None:
            campaign_kws = [k for k in keywords if k.get("campaign.id") == cid]
            if campaign_kws:
                active_kws = [k for k in campaign_kws if k["ad_group_criterion.status"] == "ENABLED" and not k.get("ad_group_criterion.negative")]
                if not active_kws:
                    explanations.append("every keyword in this campaign is paused or negative — nothing eligible to trigger.")
                checked.append("keyword status")

        checked_str = ", ".join(checked) if checked else "none available in this snapshot"
        if explanations:
            interpretation = (
                f"Checked: {checked_str}. Likely explanation(s): " + " ".join(explanations)
            )
            confidence = "high"
        else:
            interpretation = (
                f"Checked: {checked_str} — none of these explain it; budget, ads, and keywords all appear "
                "active for this campaign, but it shows zero delivery. The cause isn't visible in this data "
                "(could be ad schedule, geo/language targeting, a policy or billing hold, or campaign "
                "start/end dates, none of which the current query library captures)."
            )
            confidence = "low"

        finding_id = f"ADP-{counter:03d}"
        counter += 1
        findings.append({
            "finding_id": finding_id,
            "source_skill": "ad-performance-diagnostic",
            "category": "dormant-campaign",
            "severity": severity_for_budget(budget_gbp),
            "confidence": confidence,
            "account": config.get("account_name", "UNKNOWN"),
            "campaign_id": str(cid),
            "campaign": campaign_name,
            "period": period,
            "evidence": {
                "daily_budget_gbp": round(budget_gbp, 2),
                "campaign_budget_id": str(b["campaign_budget.id"]),
                "search_impression_share": i.get("metrics.search_impression_share", 0),
                "bidding_strategy_type": b.get("campaign.bidding_strategy_type"),
                "target_cpa_gbp": round(b.get("campaign.maximize_conversions.target_cpa_micros", 0) / 1_000_000, 2),
            },
            "observation": (
                f"'{campaign_name}' is ENABLED with a £{budget_gbp:.2f}/day budget but shows 0% search "
                f"impression share in the {period.get('start')}-{period.get('end')} period — it received no "
                "impressions at all."
            ),
            "interpretation": interpretation,
            "recommendation": "Investigate and either fix delivery or pause/remove this campaign — an enabled, budgeted campaign that can't deliver is doing nothing but sitting in the account.",
            "estimated_impact": "Unknown until investigated — this skill cannot estimate the value of fixing a problem whose cause isn't confirmed.",
            "effort": "medium",
            "caveats": [
                "The three explanations this skill checks (budget-sharing/near-zero, ad status, keyword status) "
                "are not exhaustive — ad schedule, geo/language targeting, policy holds, and campaign dates are "
                "not captured by the current query library.",
            ],
        })

    # --- Check 2: shared-budget clusters, as their own findings ---
    for bid, cids in shared_clusters.items():
        names = [campaign_by_id[c]["campaign.name"] for c in cids]
        amt = baseline_by_id[cids[0]]["campaign_budget.amount_micros"] / 1_000_000
        dormant_in_cluster = sum(1 for c in cids if is_by_id.get(c, {}).get("metrics.search_impression_share", 0) == 0)

        finding_id = f"ADP-{counter:03d}"
        counter += 1
        findings.append({
            "finding_id": finding_id,
            "source_skill": "ad-performance-diagnostic",
            "category": "shared-budget-cluster",
            "severity": "high" if (amt * len(cids) >= 50 or dormant_in_cluster >= len(cids) - 1) else "medium",
            "confidence": "high",
            "account": config.get("account_name", "UNKNOWN"),
            "period": period,
            "evidence": {
                "campaign_budget_id": str(bid),
                "daily_budget_gbp": round(amt, 2),
                "campaign_count": len(cids),
                "campaigns": names,
                "dormant_count_in_cluster": dormant_in_cluster,
            },
            "observation": (
                f"{len(cids)} ENABLED campaigns share campaign_budget.id {bid} (£{amt:.2f}/day): "
                + "; ".join(names) + f". {dormant_in_cluster} of them show 0% impression share this period."
            ),
            "interpretation": (
                "A shared budget across this many campaigns can be a deliberate strategy, but with "
                f"{dormant_in_cluster} of {len(cids)} showing zero delivery, it's at least worth confirming "
                "this is intentional rather than an accidental leftover from campaign duplication/testing."
            ),
            "recommendation": "Review whether this is intentional; if not, give each campaign its own budget so they don't compete with each other for the same spend.",
            "estimated_impact": "Unknown — depends on whether splitting the budget would let currently-dormant campaigns in the cluster actually deliver.",
            "effort": "low",
            "caveats": [
                "campaign_budget.explicitly_shared read false for these campaigns despite sharing an ID — "
                "the shared ID itself is treated as the evidence here, not that flag.",
            ],
        })

    # --- Check 3: impression-share constraint on genuinely-delivering campaigns ---
    for cid, i in is_by_id.items():
        share = i.get("metrics.search_impression_share", 0)
        if share <= 0:
            continue  # caught by Check 1
        budget_lost = i.get("metrics.search_budget_lost_impression_share", 0)
        rank_lost = i.get("metrics.search_rank_lost_impression_share", 0)
        if budget_lost <= 0 and rank_lost <= 0:
            continue  # nothing constraining it

        campaign_name = campaign_by_id[cid]["campaign.name"]
        camp_perf = next((c for c in campaigns if c["campaign.id"] == cid), {})
        cost = camp_perf.get("metrics.cost_micros", 0) / 1_000_000
        conversions = camp_perf.get("metrics.conversions", 0)

        finding_id = f"ADP-{counter:03d}"
        counter += 1

        if budget_lost >= rank_lost and budget_lost > share:
            interp = (
                f"Losing more impression share to budget ({budget_lost:.0%}) than it's currently winning "
                f"({share:.0%}) — budget looks like the binding constraint here, not bid/quality."
            )
            recommendation = "Worth testing a higher budget — no specific figure recommended, this data doesn't support estimating the right one."
            category_note = "budget-constrained"
        elif rank_lost > budget_lost:
            interp = (
                f"Rank loss ({rank_lost:.0%}) exceeds budget loss ({budget_lost:.0%}) — a budget increase "
                "alone won't help here; the constraint looks like bid/Quality Score/ad relevance, which this "
                "skill doesn't have the ad-level evidence to fully diagnose."
            )
            recommendation = "Budget increase won't help here — investigate bids/Quality Score/ad relevance instead."
            category_note = "rank-constrained"
        else:
            interp = (
                f"Some impression share lost to both budget ({budget_lost:.0%}) and rank ({rank_lost:.0%}), "
                "roughly evenly — no single clear lever here."
            )
            recommendation = "Mixed constraint — review both budget headroom and bid/quality before acting on either alone."
            category_note = "mixed-constraint"

        findings.append({
            "finding_id": finding_id,
            "source_skill": "ad-performance-diagnostic",
            "category": "impression-share-constraint",
            "severity": "high" if cost * budget_lost >= 50 else "medium",
            "confidence": "high",
            "account": config.get("account_name", "UNKNOWN"),
            "campaign_id": str(cid),
            "campaign": campaign_name,
            "period": period,
            "evidence": {
                "search_impression_share": share,
                "search_budget_lost_impression_share": budget_lost,
                "search_rank_lost_impression_share": rank_lost,
                "period_cost_gbp": round(cost, 2),
                "period_conversions": conversions,
                "constraint_type": category_note,
            },
            "observation": (
                f"'{campaign_name}' won {share:.1%} of available search impression share in the "
                f"{period.get('start')}-{period.get('end')} period, losing {budget_lost:.1%} to budget and "
                f"{rank_lost:.1%} to rank."
            ),
            "interpretation": interp,
            "recommendation": recommendation,
            "estimated_impact": "Directional only — this data shows a constraint exists, not the precise volume a fix would unlock.",
            "effort": "low",
            "caveats": [
                "No specific new budget figure is being recommended — only that current budget is or isn't a binding constraint.",
                "Conversion counts for this account carry a standing low-confidence flag (see accounts/company-debt.yml) — weigh cost/impression-share evidence more heavily than the conversion figure here.",
            ],
        })

    print(json.dumps(findings, indent=2, ensure_ascii=False))
    print(
        f"\n# Summary: {len(findings)} finding(s) ({dormant_count} dormant-campaign, "
        f"{len(shared_clusters)} shared-budget-cluster, {len(findings) - dormant_count - len(shared_clusters)} "
        f"impression-share-constraint) across {len(enabled_ids)} ENABLED campaigns.",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
