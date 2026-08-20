#!/usr/bin/env python3
"""Turn a weekly_audit_pull raw dump into the full search-term CSV plus a
flagged summary. Read-only; reads runs/<run>/raw and writes into runs/<run>/.

Flagging has three layers:
  1. agreed exclusions from accounts/company-debt.yml (irrelevant_topics)
  2. personal-insolvency / consumer intent, matched on word boundaries
  3. navigational: another firm's name, a person's name, or a street address

Usage:
    python scripts/weekly_search_terms.py --run 2026-08-20-weekly-audit \
        --label search_terms_primary --out search-terms-2026-08-11_to_2026-08-17.csv
"""

import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

# Personal-debt / consumer intent. Matched as whole words, so "iva" does not
# fire inside "private" or "receivables".
PERSONAL = [
    "iva", "ivas", "individual voluntary arrangement", "personal bankruptcy",
    "debt relief order", "dro", "payday", "payday loan", "consumer credit",
    "personal loan", "personal loans", "credit card debt", "stepchange",
    "citizens advice", "national debtline", "sole trader", "self employed",
    "bailiff", "bailiffs", "council tax", "student loan", "car finance",
    "mortgage arrears", "free debt advice", "debt management plan",
    "personal debt", "declare myself bankrupt", "am i bankrupt",
    "bankruptcy uk", "going bankrupt", "my debts", "my debt",
]

# Signals that the searcher wanted a specific other business or a location,
# not a service. Postcode / street-address shapes and legal-entity suffixes.
POSTCODE = re.compile(r"\b[a-z]{1,2}\d{1,2}[a-z]?\s*\d[a-z]{2}\b", re.I)
ADDRESSY = re.compile(r"\b(unit|suite|road|street|avenue|lane|floor)\b", re.I)
COHOUSE = re.compile(r"\b(compan(y|ies|ys)\s*house|companieshouse)\b", re.I)
FIRMY = re.compile(r"\b(llp|ltd|limited|solicitors|law|legal|recoveries|associates|partners|& co)\b", re.I)


def word_hit(term, phrase):
    return re.search(r"\b" + re.escape(phrase) + r"\b", term) is not None


def classify(term, config_terms, brand_terms):
    t = term.lower().strip()
    flags = []
    for k in config_terms:
        if k in t:
            flags.append(f"agreed exclusion ({k})")
    for k in PERSONAL:
        if word_hit(t, k):
            flags.append(f"personal debt ({k})")
    if any(b in t for b in brand_terms):
        return "brand"
    if COHOUSE.search(t):
        flags.append("Companies House navigational search")
    if POSTCODE.search(t) or ADDRESSY.search(t):
        flags.append("address / location lookup")
    words = t.split()
    # two or three words, no service vocabulary at all: probably a person or firm
    SERVICE = {
        "company", "companies", "business", "businesses", "debt", "debts",
        "liquidation", "liquidate", "insolvency", "insolvent", "close",
        "closing", "closure", "dissolve", "dissolution", "strike", "off",
        "winding", "petition", "hmrc", "vat", "paye", "tax", "administration",
        "cva", "creditor", "creditors", "director", "directors", "ltd",
        "limited", "how", "what", "can", "i", "my", "a", "the", "to", "do",
        "does", "uk", "practitioner", "practitioners", "advice", "help",
        "cost", "costs", "process", "bankrupt", "bankruptcy", "bankruptcies",
    }
    has_service = bool(set(words) & SERVICE)
    if 1 <= len(words) <= 4 and not has_service:
        flags.append("looks like another firm or a person's name")
    elif FIRMY.search(t) and not has_service:
        flags.append("looks like another firm or a person's name")
    return "; ".join(dict.fromkeys(flags))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--label", default="search_terms_primary")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    cfg = yaml.safe_load((ROOT / "accounts" / "company-debt.yml").read_text(encoding="utf-8"))
    config_terms = [str(t).lower() for t in cfg["irrelevant_topics"]]
    brand_terms = [str(t).lower() for t in cfg["brand_terms"]]

    run_dir = ROOT / "runs" / args.run
    rows = json.loads((run_dir / "raw" / f"{args.label}.json").read_text(encoding="utf-8"))

    agg = defaultdict(lambda: {"imp": 0, "clk": 0, "cost": 0, "conv": 0.0, "all": 0.0})
    for r in rows:
        k = (
            r["search_term_view.search_term"],
            r.get("segments.search_term_match_type"),
            r["campaign.name"],
            r["ad_group.name"],
            r.get("search_term_view.status"),
        )
        a = agg[k]
        a["imp"] += r["metrics.impressions"]
        a["clk"] += r["metrics.clicks"]
        a["cost"] += r["metrics.cost_micros"]
        a["conv"] += r["metrics.conversions"]
        a["all"] += r["metrics.all_conversions"]

    out = run_dir / args.out
    with out.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow([
            "search_term", "match_type", "campaign", "ad_group", "term_status",
            "impressions", "clicks", "cost_gbp", "conversions", "all_conversions", "flag",
        ])
        for k, v in sorted(agg.items(), key=lambda x: (-x[1]["cost"], -x[1]["imp"])):
            w.writerow([
                k[0], k[1], k[2], k[3], k[4], v["imp"], v["clk"],
                round(v["cost"] / 1e6, 2), v["conv"], v["all"],
                classify(k[0], config_terms, brand_terms),
            ])

    flagged = [(k, v) for k, v in agg.items() if classify(k[0], config_terms, brand_terms) not in ("", "brand")]
    print(f"{len(agg)} unique terms -> {out}")
    print(f"total captured: GBP{sum(v['cost'] for v in agg.values())/1e6:.2f}, "
          f"{sum(v['clk'] for v in agg.values())} clicks, "
          f"{sum(v['imp'] for v in agg.values())} impressions")
    print(f"flagged: {len(flagged)} terms, GBP{sum(v['cost'] for _, v in flagged)/1e6:.2f}, "
          f"{sum(v['clk'] for _, v in flagged)} clicks")
    print("\n-- flagged terms that cost money --")
    for k, v in sorted(flagged, key=lambda x: -x[1]["cost"]):
        if v["cost"] == 0:
            continue
        print(f"GBP{v['cost']/1e6:>7.2f} clk={v['clk']:>2} imp={v['imp']:>3} "
              f"{k[3][:24]:<25} [{str(k[1])[:10]:<10}] {k[0][:52]:<53} "
              f"{classify(k[0], config_terms, brand_terms)}")


if __name__ == "__main__":
    main()
