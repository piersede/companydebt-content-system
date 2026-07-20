#!/usr/bin/env python3
"""Reference implementation of the search-terms-analyzer skill
(.claude/skills/search-terms-analyzer/SKILL.md). Deterministic — same
snapshot always produces the same findings.

Usage:
    python scripts/analyze_search_terms.py <run-or-fixture-folder>

<run-or-fixture-folder> must contain search-terms.json, keywords.json, and
account-config.yml (either a runs/YYYY-MM-DD-<slug>/ folder or a
tests/fixtures/<scenario>/ folder — same shape).
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
    text = text.lower()
    return [p for p in phrases if p.lower() in text]


def main():
    if len(sys.argv) != 2:
        print("Usage: python analyze_search_terms.py <run-or-fixture-folder>", file=sys.stderr)
        sys.exit(2)

    folder = Path(sys.argv[1])
    raw = folder / "raw" if (folder / "raw").exists() else folder

    search_terms = load(raw, "search-terms.json")
    keywords = load(raw, "keywords.json")
    config = yaml.safe_load((folder / "account-config.yml").read_text(encoding="utf-8"))

    if search_terms is None or keywords is None:
        print("ERROR: search-terms.json and keywords.json are both required", file=sys.stderr)
        sys.exit(2)

    irrelevant_topics = config.get("irrelevant_topics") or []
    brand_terms = config.get("brand_terms") or []
    targets = config.get("targets", {})
    min_clicks = targets.get("minimum_clicks_before_judgement", 12)

    manifest = load(folder, "manifest.json")
    if manifest:
        period = {"start": manifest["audit_start"], "end": manifest["audit_end"]}
    else:
        period = config.get("_period", {"start": "UNKNOWN", "end": "UNKNOWN"})

    # existing dedicated (non-negative, enabled) keywords, keyed by campaign_id -> set of lowercased texts
    existing_keywords = {}
    for row in keywords:
        if not row.get("ad_group_criterion.negative") and row.get("ad_group_criterion.status") == "ENABLED":
            cid = str(row.get("campaign.id"))
            existing_keywords.setdefault(cid, set()).add(row["ad_group_criterion.keyword.text"].lower())

    findings = []
    counter = 1
    already_targeted_skipped = 0
    irrelevant_skipped = 0
    no_signal_skipped = 0
    excluded_skipped = 0

    for row in search_terms:
        term = row["search_term_view.search_term"]
        campaign_id = str(row.get("campaign.id"))

        if row.get("search_term_view.status") == "EXCLUDED":
            excluded_skipped += 1
            continue

        if term.lower() in existing_keywords.get(campaign_id, set()):
            already_targeted_skipped += 1
            continue

        if contains_any(term, irrelevant_topics):
            irrelevant_skipped += 1
            continue

        clicks = row.get("metrics.clicks", 0)
        conversions = row.get("metrics.conversions", 0)
        cost = row.get("metrics.cost_micros", 0) / 1_000_000
        impressions = row.get("metrics.impressions", 0)

        if conversions <= 0:
            no_signal_skipped += 1
            continue

        strong = clicks >= min_clicks
        is_brand = bool(contains_any(term, brand_terms))

        finding_id = f"OPP-{counter:03d}"
        counter += 1

        matched_kw = row.get("segments.keyword.info.text", "UNKNOWN")
        matched_kw_type = row.get("segments.keyword.info.match_type", "UNKNOWN")

        base_caveats = [
            "search-terms.gaql has no context-window equivalent at search-term granularity — this reflects the "
            "audit period only, and cannot be checked against prior weeks the way campaign-level findings can.",
            "Conversion counts for this account carry a standing low-confidence flag (see accounts/company-debt.yml) "
            "— only phone/email/chat conversions are trusted, and volume has been scant recently.",
        ]
        if clicks > impressions:
            base_caveats.append(
                f"This row reports {clicks} click(s) but only {impressions} impression(s) — clicks exceeding "
                "impressions is a known Google Ads search-terms reporting quirk at low volumes (asynchronous "
                "click/impression attribution), not a data error introduced here. Treat these figures as "
                "approximate rather than exact."
            )

        if strong:
            severity = "high" if (conversions >= 2 or clicks >= min_clicks * 2) else "medium"
            confidence = "high"
            recommendation = (
                f"Add '{term}' as an EXACT match keyword in the ad group '{row['ad_group.name']}' "
                f"(campaign {campaign_id}), so it can be bid and tracked independently of the "
                f"{matched_kw_type} keyword '{matched_kw}' that incidentally triggered it."
            )
            interpretation = (
                f"This term is being picked up incidentally by the {matched_kw_type} match keyword "
                f"'{matched_kw}' rather than deliberately targeted, and has enough volume and a conversion "
                "signal to justify dedicated targeting and bid control."
            )
        else:
            severity = "low"
            confidence = "low"
            recommendation = (
                f"Monitor '{term}' for another audit period before adding as a keyword — {clicks} click(s) "
                f"with {conversions} conversion(s) is below the account's minimum_clicks_before_judgement "
                f"threshold ({min_clicks}), so this is too little evidence to act on yet."
            )
            interpretation = (
                "A single low-volume conversion is exactly the kind of thin signal the account's "
                "conversion-data caveat warns about — worth watching, not yet worth a confident recommendation."
            )

        caveats = list(base_caveats)
        if is_brand:
            caveats.append(
                "This term matches the account's brand_terms — brand and non-brand performance should never "
                "be compared or read the same way; brand terms typically convert very differently."
            )

        findings.append({
            "finding_id": finding_id,
            "source_skill": "search-terms-analyzer",
            "category": "untargeted-opportunity",
            "severity": severity,
            "confidence": confidence,
            "account": config.get("account_name", "UNKNOWN"),
            "campaign_id": campaign_id,
            "campaign": row["campaign.name"],
            "ad_group_id": str(row["ad_group.id"]),
            "ad_group": row["ad_group.name"],
            "period": period,
            "evidence": {
                "search_term": term,
                "triggering_keyword": matched_kw,
                "triggering_match_type": matched_kw_type,
                "cost_gbp": round(cost, 2),
                "clicks": clicks,
                "impressions": impressions,
                "conversions": conversions,
                "is_brand_term": is_brand,
            },
            "observation": (
                f"The search term '{term}' received {clicks} click(s) and £{cost:.2f} spend via the "
                f"{matched_kw_type} match keyword '{matched_kw}' in the {period.get('start')}-{period.get('end')} "
                f"period, with {conversions} conversion(s)."
            ),
            "interpretation": interpretation,
            "recommendation": recommendation,
            "estimated_impact": (
                "Dedicated EXACT-match targeting typically gives better bid control and a cleaner Quality "
                "Score signal than an incidental broad/phrase match, but no specific £ uplift is claimed — "
                "the evidence here doesn't support estimating one."
            ),
            "effort": "low",
            "caveats": caveats,
        })

    print(json.dumps(findings, indent=2, ensure_ascii=False))
    print(
        f"\n# Summary: {len(findings)} finding(s). Skipped: {excluded_skipped} already-excluded, "
        f"{already_targeted_skipped} already-own-keyword, {irrelevant_skipped} irrelevant-topic "
        f"(negative-keyword-miner's territory), {no_signal_skipped} zero-conversion (no signal either way).",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
