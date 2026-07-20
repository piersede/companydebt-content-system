#!/usr/bin/env python3
"""Reference implementation of the negative-keyword-miner skill
(.claude/skills/negative-keyword-miner/SKILL.md). Deterministic — same
snapshot always produces the same findings.

Usage:
    python scripts/mine_negative_keywords.py <run-or-fixture-folder>

<run-or-fixture-folder> must contain search-terms.json, keywords.json, and
account-config.yml (either a runs/YYYY-MM-DD-<slug>/ folder or a
tests/fixtures/<scenario>/ folder — same shape).
"""

import json
import sys
from pathlib import Path

import yaml

# Windows defaults stdout to the console codepage (e.g. cp1252), which can't
# encode £ and silently corrupts redirected output instead of erroring at
# write time — force UTF-8 so this is correct regardless of caller/console.
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ZERO_CONV_SEVERITY_MULTIPLIER = 3  # medium up to 3x zero_conversion_spend_threshold, high above


def load(folder, name):
    path = folder / name
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def contains_any(text, phrases):
    text = text.lower()
    return [p for p in phrases if p.lower() in text]


def main():
    if len(sys.argv) != 2:
        print("Usage: python mine_negative_keywords.py <run-or-fixture-folder>", file=sys.stderr)
        sys.exit(2)

    folder = Path(sys.argv[1])
    raw = folder / "raw" if (folder / "raw").exists() else folder  # runs/ nests under raw/, fixtures don't

    search_terms = load(raw, "search-terms.json")
    keywords = load(raw, "keywords.json")
    config = yaml.safe_load((folder / "account-config.yml").read_text(encoding="utf-8"))

    if search_terms is None or keywords is None:
        print("ERROR: search-terms.json and keywords.json are both required", file=sys.stderr)
        sys.exit(2)

    protected_terms = config.get("protected_terms") or []
    irrelevant_topics = config.get("irrelevant_topics") or []
    brand_terms = config.get("brand_terms") or []
    targets = config.get("targets", {})
    min_clicks = targets.get("minimum_clicks_before_judgement", 12)
    zero_conv_threshold = targets.get("zero_conversion_spend_threshold", 75)

    manifest = load(folder, "manifest.json")  # real runs/ have this; fixtures fall back to account-config.yml's _period
    if manifest:
        period = {"start": manifest["audit_start"], "end": manifest["audit_end"]}
    else:
        period = config.get("_period", {"start": "UNKNOWN", "end": "UNKNOWN"})

    # existing negatives, keyed by campaign_id -> set of lowercased keyword texts
    existing_negatives = {}
    for row in keywords:
        if row.get("ad_group_criterion.negative"):
            cid = str(row.get("campaign.id"))
            existing_negatives.setdefault(cid, set()).add(row["ad_group_criterion.keyword.text"].lower())

    def already_negated(term, campaign_id):
        term_l = term.lower()
        for neg in existing_negatives.get(campaign_id, set()):
            if neg in term_l:
                return True
        return False

    # group rows by search term text
    grouped = {}
    protected_skipped = 0
    excluded_skipped = 0
    deduped_skipped = 0
    for row in search_terms:
        term = row["search_term_view.search_term"]

        if row.get("search_term_view.status") == "EXCLUDED":
            excluded_skipped += 1
            continue

        if contains_any(term, protected_terms):
            protected_skipped += 1
            continue

        campaign_id = str(row.get("campaign.id"))
        if already_negated(term, campaign_id):
            deduped_skipped += 1
            continue

        grouped.setdefault(term, []).append(row)

    findings = []
    counter = 1
    relevant_zero_conv_skipped = 0
    low_volume_skipped = 0

    for term, rows in grouped.items():
        matched_topics = contains_any(term, irrelevant_topics)
        total_cost = sum(r.get("metrics.cost_micros", 0) for r in rows) / 1_000_000
        total_clicks = sum(r.get("metrics.clicks", 0) for r in rows)
        total_impressions = sum(r.get("metrics.impressions", 0) for r in rows)
        total_conversions = sum(r.get("metrics.conversions", 0) for r in rows)

        if not matched_topics:
            # topically relevant zero-conversion spend is not this skill's job
            if total_conversions == 0 and total_cost > 0:
                relevant_zero_conv_skipped += 1
            continue

        low_volume = total_clicks < min_clicks
        if low_volume:
            low_volume_skipped += 0  # still eligible per SKILL.md — irrelevance is topical, not volume-based

        if total_cost <= zero_conv_threshold:
            severity = "low"
        elif total_cost <= zero_conv_threshold * ZERO_CONV_SEVERITY_MULTIPLIER:
            severity = "medium"
        else:
            severity = "high"

        confidence = "low" if low_volume else "high"

        core_phrases = [t.lower() for t in brand_terms] + ["insolvency", "liquidation", "company debt", "creditors", "debt"]
        shares_core_word = any(cp in term.lower() for cp in core_phrases)
        blocking_risk = "medium" if shares_core_word else "low"

        breakdown = [
            {
                "campaign": r["campaign.name"],
                "campaign_id": str(r["campaign.id"]),
                "ad_group": r["ad_group.name"],
                "ad_group_id": str(r["ad_group.id"]),
                "cost_gbp": round(r.get("metrics.cost_micros", 0) / 1_000_000, 2),
                "clicks": r.get("metrics.clicks", 0),
                "impressions": r.get("metrics.impressions", 0),
            }
            for r in rows
        ]

        finding_id = f"NEG-{counter:03d}"
        counter += 1

        finding = {
            "finding_id": finding_id,
            "source_skill": "negative-keyword-miner",
            "category": "irrelevant-topic-negative",
            "severity": severity,
            "confidence": confidence,
            "account": config.get("account_name", "UNKNOWN"),
            "period": period,
            "evidence": {
                "search_term": term,
                "matched_irrelevant_topic": ", ".join(matched_topics),
                ("total_cost_gbp" if len(rows) > 1 else "cost_gbp"): round(total_cost, 2),
                ("total_clicks" if len(rows) > 1 else "clicks"): total_clicks,
                ("total_impressions" if len(rows) > 1 else "impressions"): total_impressions,
                ("total_conversions" if len(rows) > 1 else "conversions"): total_conversions,
            },
            "observation": (
                f"The search term '{term}' received {total_clicks} clicks and £{total_cost:.2f} spend "
                f"across {len(rows)} campaign(s) in the {period.get('start')}-{period.get('end')} period, "
                f"with {total_conversions} conversions, and matches the configured irrelevant-topic "
                f"categor{'y' if len(matched_topics) == 1 else 'ies'} '{', '.join(matched_topics)}'."
            ),
            "interpretation": "This traffic reads as outside the account's target audience for insolvency/company-debt services.",
            "recommendation": (
                f"Add '{term}' as an EXACT match negative keyword at ad-group level in "
                + "; ".join(f"'{b['ad_group']}' (campaign {b['campaign_id']})" for b in breakdown) + "."
            ),
            "estimated_impact": (
                f"Would prevent further spend on this exact query going forward. Historical spend of "
                f"£{total_cost:.2f} has already occurred and is not recovered by adding a negative."
            ),
            "effort": "low",
            "blocking_risk": blocking_risk,
            "caveats": [
                "Existing negative-keyword coverage was only checked at ad-group/campaign level via keyword_view; "
                "shared negative-keyword lists are not visible in the current query library, so this term could "
                "already be excluded via a shared list not captured here.",
            ],
        }

        if low_volume:
            finding["caveats"].append(
                f"Volume is low ({total_clicks} clicks total) — confidence is low because the sample is thin, "
                "even though the topic match itself is unambiguous."
            )
        if shares_core_word:
            finding["caveats"].append(
                "The term overlaps with the account's core commercial vocabulary — blocking risk rated medium, "
                "not low, on that basis."
            )

        if len(rows) == 1:
            finding["campaign_id"] = breakdown[0]["campaign_id"]
            finding["campaign"] = breakdown[0]["campaign"]
            finding["ad_group_id"] = breakdown[0]["ad_group_id"]
            finding["ad_group"] = breakdown[0]["ad_group"]
        else:
            finding["evidence"]["breakdown"] = breakdown

        findings.append(finding)

    print(json.dumps(findings, indent=2, ensure_ascii=False))
    print(
        f"\n# Summary: {len(findings)} finding(s). Skipped: {protected_skipped} protected, "
        f"{excluded_skipped} already-excluded, {deduped_skipped} already-negated, "
        f"{relevant_zero_conv_skipped} topically-relevant-zero-conversion (out of scope for this skill).",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
