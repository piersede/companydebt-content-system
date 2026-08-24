#!/usr/bin/env python3
"""Find negative keywords that block business the account actually wants.

Negative keyword lists accumulate for years and nobody prunes them. This script
takes a corpus of searches the business DOES want, replays Google's own negative
matching rules against every live exclusion, and reports which wanted searches
are blocked and by which entry in which list.

Read-only. It proposes removals; it never changes the account.

Matching rules implemented (Google's, for negatives):
  EXACT   blocks only the identical query. No close variants, no plurals.
  PHRASE  blocks any query containing that exact run of words.
  BROAD   blocks any query containing all those words, in any order.

Usage:
    python scripts/audit_negative_overblock.py --run 2026-08-20-weekly-audit \
        --queries wanted-queries.json --out overblocking
"""

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Lists that are actually attached to a serving campaign, plus the account-level
# list, which applies everywhere by definition.
# Only lists whose campaign_shared_set link is ENABLED are actually in force.
# Five older lists (Negatives, Old Negatives, Negatives #2, n-grams, Irrelevant)
# still exist but were detached from the campaigns, so they block nothing. The
# account-level list needs no link: it applies to every campaign by definition,
# which is exactly why it gets forgotten.
ATTACHED = {
    "Master 2026",
    "Master Negatives List 2",
    "account-level negative keywords list",
}

TOKEN = re.compile(r"[a-z0-9&']+")


def words(s):
    return TOKEN.findall((s or "").lower())


def blocks(neg_text, match_type, query_words):
    n = words(neg_text)
    if not n:
        return False
    if match_type == "EXACT":
        return query_words == n
    if match_type == "PHRASE":
        span = len(n)
        return any(query_words[i:i + span] == n for i in range(len(query_words) - span + 1))
    return set(n).issubset(set(query_words))  # BROAD


def load_negatives(run_dir):
    raw = json.loads((run_dir / "raw" / "shared_criterion_all.json").read_text(encoding="utf-8"))
    live = [
        {
            "text": r.get("shared_criterion.keyword.text") or "",
            "match": r.get("shared_criterion.keyword.match_type") or "",
            "list": r["shared_set.name"],
        }
        for r in raw
        if r["shared_set.name"] in ATTACHED and r["shared_set.status"] == "ENABLED"
    ]
    campaign_file = run_dir / "raw" / "campaign_negatives.json"
    if campaign_file.exists():
        for r in json.loads(campaign_file.read_text(encoding="utf-8")):
            live.append({
                "text": r.get("campaign_criterion.keyword.text") or "",
                "match": r.get("campaign_criterion.keyword.match_type") or "",
                "list": f"campaign: {r['campaign.name']}",
            })
    return live


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--queries", required=True, help="JSON: {area: [query, ...]} or a flat list")
    ap.add_argument("--out", default="overblocking")
    args = ap.parse_args()

    run_dir = ROOT / "runs" / args.run
    live = load_negatives(run_dir)

    payload = json.loads(Path(args.queries).read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        corpus = [(area, q) for area, qs in payload.items() for q in qs]
    else:
        corpus = [("(unsorted)", q) for q in payload]
    # dedupe, keeping the first area a query appeared under
    seen, deduped = set(), []
    for area, q in corpus:
        key = " ".join(words(q))
        if key and key not in seen:
            seen.add(key)
            deduped.append((area, q))

    print(f"{len(live)} live exclusions vs {len(deduped)} wanted searches\n")

    # Index BROAD/PHRASE negatives by their rarest word so we do not do 15k x 300.
    by_word = defaultdict(list)
    exacts = defaultdict(list)
    for n in live:
        w = words(n["text"])
        if not w:
            continue
        if n["match"] == "EXACT":
            exacts[" ".join(w)].append(n)
        else:
            by_word[w[0]].append(n)
            for extra in w[1:]:
                by_word[extra].append(n)

    blocked, per_area = [], Counter()
    culprits = Counter()
    for area, q in deduped:
        qw = words(q)
        candidates = {id(n): n for w in set(qw) for n in by_word.get(w, [])}
        hits = [n for n in candidates.values() if blocks(n["text"], n["match"], qw)]
        hits += [n for n in exacts.get(" ".join(qw), [])]
        if hits:
            blocked.append({"area": area, "query": q, "blocked_by": hits})
            per_area[area] += 1
            for h in hits:
                culprits[(h["text"], h["match"], h["list"])] += 1

    total_by_area = Counter(a for a, _ in deduped)
    print("=== wanted searches blocked, by service area ===")
    print(f"{'area':<26}{'wanted':>8}{'blocked':>9}{'%':>7}")
    for area in sorted(total_by_area, key=lambda a: -per_area[a] / max(total_by_area[a], 1)):
        t, b = total_by_area[area], per_area[area]
        print(f"{area:<26}{t:>8}{b:>9}{(b / t * 100 if t else 0):>6.0f}%")
    print(f"\nTOTAL: {len(blocked)} of {len(deduped)} wanted searches are blocked "
          f"({len(blocked) / len(deduped) * 100:.0f}%)")

    print("\n=== the exclusions doing the most damage ===")
    print(f"{'kills':>6}  {'match':<8}{'list':<38}entry")
    for (text, match, lst), n in culprits.most_common(40):
        print(f"{n:>6}  {match:<8}{lst[:37]:<38}{text}")

    out_dir = run_dir / args.out
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "blocked-wanted-searches.json").write_text(
        json.dumps(blocked, indent=2), encoding="utf-8")

    import csv
    with (out_dir / "exclusions-to-remove.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["exclusion", "match_type", "in_list", "wanted_searches_it_blocks", "examples"])
        for (text, match, lst), n in culprits.most_common():
            ex = [b["query"] for b in blocked
                  if any(h["text"] == text and h["match"] == match and h["list"] == lst
                         for h in b["blocked_by"])][:4]
            w.writerow([text, match, lst, n, " | ".join(ex)])
    with (out_dir / "blocked-searches.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["area", "wanted_search", "blocked_by", "match_type", "in_list"])
        for b in blocked:
            for h in b["blocked_by"]:
                w.writerow([b["area"], b["query"], h["text"], h["match"], h["list"]])
    print(f"\nwrote {out_dir}")


if __name__ == "__main__":
    main()
