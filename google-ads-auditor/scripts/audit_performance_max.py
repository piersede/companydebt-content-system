#!/usr/bin/env python3
"""Reference implementation of the performance-max-auditor skill
(.claude/skills/performance-max-auditor/SKILL.md). Deterministic — same
snapshot always produces the same findings.

Usage:
    python scripts/audit_performance_max.py <run-or-fixture-folder>

<run-or-fixture-folder> must contain pmax.json (with search_terms,
asset_groups, campaigns sub-keys; placements/products optional/may be
empty), plus account-config.yml.
"""

import json
import sys
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")


def load(folder, name):
    path = folder / name
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def contains_any(text, phrases):
    text = (text or "").lower()
    return [p for p in phrases if p and p.lower() in text]


def severity_for_clicks(clicks):
    if clicks >= 50:
        return "high"
    if clicks >= 10:
        return "medium"
    return "low"


def main():
    if len(sys.argv) != 2:
        print("Usage: python audit_performance_max.py <run-or-fixture-folder>", file=sys.stderr)
        sys.exit(2)

    folder = Path(sys.argv[1])
    raw = folder / "raw" if (folder / "raw").exists() else folder

    pmax = load(raw, "pmax.json")
    config = yaml.safe_load((folder / "account-config.yml").read_text(encoding="utf-8"))

    if pmax is None:
        print("ERROR: pmax.json is required", file=sys.stderr)
        sys.exit(2)

    search_terms = pmax.get("search_terms", [])
    asset_groups = pmax.get("asset_groups", [])
    campaigns = pmax.get("campaigns", [])
    placements = pmax.get("placements", [])
    products = pmax.get("products", [])

    irrelevant_topics = config.get("irrelevant_topics") or []

    manifest = load(folder, "manifest.json")
    if manifest:
        period = {"start": manifest["audit_start"], "end": manifest["audit_end"]}
    else:
        period = config.get("_period", {"start": "UNKNOWN", "end": "UNKNOWN"})

    account_name = config.get("account_name", "UNKNOWN")
    findings = []
    counter = 1

    # --- Check 1: off-target category-level search insights ---
    off_target_count = 0
    for row in search_terms:
        label = row.get("campaign_search_term_insight.category_label", "")
        matched = contains_any(label, irrelevant_topics)
        if not matched:
            continue
        off_target_count += 1
        clicks = row.get("metrics.clicks", 0)
        impressions = row.get("metrics.impressions", 0)

        finding_id = f"PMX-{counter:03d}"
        counter += 1
        findings.append({
            "finding_id": finding_id,
            "source_skill": "performance-max-auditor",
            "category": "pmax-off-target-category",
            "severity": severity_for_clicks(clicks),
            "confidence": "high",
            "evidence_label": "observed",
            "account": account_name,
            "campaign_id": str(row["campaign.id"]),
            "campaign": row["campaign.name"],
            "period": period,
            "evidence": {
                "category_label": label,
                "matched_irrelevant_topic": ", ".join(matched),
                "impressions": impressions,
                "clicks": clicks,
            },
            "observation": (
                f"The PMax search-category insight '{label}' received {impressions} impression(s) and "
                f"{clicks} click(s) in the {period.get('start')}-{period.get('end')} period, and matches the "
                f"configured irrelevant-topic categor{'y' if len(matched)==1 else 'ies'} '{', '.join(matched)}'."
            ),
            "interpretation": (
                "This category label reads as outside the account's target audience. Cost impact cannot be "
                "stated — PMax search-category insights have no cost field, unlike Search's search_term_view."
            ),
            "recommendation": (
                f"Add '{label}' to the account-level Performance Max negative keyword list (Settings > "
                "Account-level negative keywords), or a brand exclusion list if this is a competitor/brand "
                "name — PMax does not support ad-group or campaign-level EXACT-match negatives the way Search does."
            ),
            "estimated_impact": "Not measurable — no cost data exists at this granularity for PMax search-category insights.",
            "effort": "low",
            "caveats": [
                "PMax search-category insights are category-level labels, not literal search queries, and have "
                "no cost field — this finding states a topical concern, not a £ impact.",
                "Categories not matching the configured irrelevant_topics list were not evaluated — an "
                "unmatched category that looks off-target is a configuration gap for human review, not "
                "something this skill classifies unilaterally.",
            ],
        })

    # --- Check 2: asset-group coverage ---
    enabled_campaign_ids = {c["campaign.id"] for c in campaigns if c.get("campaign.status") == "ENABLED"}
    live_weak_count = 0
    live_asset_group_count = 0
    for ag in asset_groups:
        if ag.get("asset_group.status") != "ENABLED":
            continue
        if ag.get("campaign.id") not in enabled_campaign_ids:
            continue
        live_asset_group_count += 1
        strength = ag.get("asset_group.ad_strength")
        if strength not in ("POOR", "AVERAGE"):
            continue
        live_weak_count += 1

        finding_id = f"PMX-{counter:03d}"
        counter += 1
        findings.append({
            "finding_id": finding_id,
            "source_skill": "performance-max-auditor",
            "category": "pmax-asset-strength",
            "severity": "medium" if strength == "POOR" else "low",
            "confidence": "high",
            "evidence_label": "inferred",
            "account": account_name,
            "campaign_id": str(ag["campaign.id"]),
            "campaign": ag["campaign.name"],
            "period": period,
            "evidence": {
                "asset_group": ag.get("asset_group.name"),
                "ad_strength": strength,
                "impressions": ag.get("metrics.impressions", 0),
                "clicks": ag.get("metrics.clicks", 0),
                "cost_gbp": round(ag.get("metrics.cost_micros", 0) / 1_000_000, 2),
            },
            "observation": (
                f"Asset group '{ag.get('asset_group.name')}' in '{ag['campaign.name']}' is ENABLED, in an "
                f"ENABLED campaign, with ad_strength = {strength}."
            ),
            "interpretation": (
                "Ad strength is Google's own coverage/completeness heuristic (more headline/description "
                "variety, better asset-type coverage), not a measure of commercial performance — this asset "
                "group could be converting fine despite the label, or an EXCELLENT one could be "
                "underperforming. This finding is about asset coverage, not proven results."
            ),
            "recommendation": f"Add more headline/description/image variety to '{ag.get('asset_group.name')}' to improve Google's coverage assessment.",
            "estimated_impact": "Not measurable as a commercial outcome — asset strength does not equate to conversion performance.",
            "effort": "low",
            "caveats": [
                "asset_group.ad_strength is an inferred coverage label from Google, not proof of commercial "
                "performance, per CLAUDE.md's Performance Max rules.",
            ],
        })

    # --- Check 3: dormant ENABLED PMax campaigns ---
    dormant_count = 0
    for c in campaigns:
        if c.get("campaign.status") != "ENABLED":
            continue
        budget_gbp = c.get("campaign_budget.amount_micros", 0) / 1_000_000
        if budget_gbp <= 0:
            continue
        if c.get("metrics.impressions", 0) > 0:
            continue
        dormant_count += 1

        finding_id = f"PMX-{counter:03d}"
        counter += 1
        findings.append({
            "finding_id": finding_id,
            "source_skill": "performance-max-auditor",
            "category": "pmax-dormant-campaign",
            "severity": "high" if budget_gbp >= 50 else ("medium" if budget_gbp >= 10 else "low"),
            "confidence": "high",
            "evidence_label": "observed",
            "account": account_name,
            "campaign_id": str(c["campaign.id"]),
            "campaign": c["campaign.name"],
            "period": period,
            "evidence": {
                "daily_budget_gbp": round(budget_gbp, 2),
                "impressions": c.get("metrics.impressions", 0),
            },
            "observation": (
                f"'{c['campaign.name']}' is ENABLED with a £{budget_gbp:.2f}/day budget but received 0 "
                f"impressions in the {period.get('start')}-{period.get('end')} period."
            ),
            "interpretation": (
                "This skill doesn't cross-reference PMax asset-group/policy status the way "
                "ad-performance-diagnostic does for Search ads/keywords — the cause isn't diagnosed here, "
                "only observed."
            ),
            "recommendation": "Investigate and either fix delivery or pause/remove this campaign.",
            "estimated_impact": "Unknown until investigated.",
            "effort": "medium",
            "caveats": [
                "No deeper diagnosis (asset-group status, policy holds) was performed for this campaign — "
                "this check only observes zero delivery against an active budget.",
            ],
        })

    print(json.dumps(findings, indent=2, ensure_ascii=False))
    print(
        f"\n# Summary: {len(findings)} finding(s) ({off_target_count} off-target-category, "
        f"{live_weak_count} weak-asset-strength of {live_asset_group_count} live asset groups, "
        f"{dormant_count} dormant-campaign). Placements: {len(placements)} row(s) "
        f"({'not applicable — no data this period' if not placements else 'present'}). "
        f"Products: {len(products)} row(s) ({'not applicable — no Shopping feed' if not products else 'present'}).",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
