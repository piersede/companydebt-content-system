"""Read-only audit + reorder helper for Monday board 18406273663, group "Live".

Two modes:
  --dry-run   : pull Live items, match against GA CSV, print proposed order + ambiguities.
                Writes nothing to Monday.
  --apply     : after dry-run is approved, repositions items in the Live group only.
                Touches NO column values, NO names, NO URLs. Reorder only.

Usage:
  python scripts/monday_live_reorder.py --dry-run --csv "<path-to-ga-csv>"
  python scripts/monday_live_reorder.py --apply  --csv "<path-to-ga-csv>"
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

# Force UTF-8 stdout on Windows so bullet/dash chars don't break.
if sys.platform == "win32":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)
    except Exception:
        pass

import requests
from dotenv import load_dotenv

BOARD_ID = 18406273663
LIVE_GROUP_TITLE = "Live"
MONDAY_URL = "https://api.monday.com/v2"


def load_env() -> str:
    # Walk up from this file to find the repo .env (parent repo, not worktree).
    here = Path(__file__).resolve()
    for candidate in [
        here.parents[1] / ".env",
        here.parents[3] / ".env",
        here.parents[4] / ".env",
    ]:
        if candidate.exists():
            load_dotenv(candidate)
            break
    key = os.environ.get("MONDAY_API_KEY")
    if not key:
        sys.exit("MONDAY_API_KEY not set in .env")
    return key


def gql(token: str, query: str, variables: dict[str, Any] | None = None, api_version: str = "2024-10") -> dict[str, Any]:
    import time
    for attempt in range(5):
        r = requests.post(
            MONDAY_URL,
            headers={"Authorization": token, "Content-Type": "application/json", "API-Version": api_version},
            json={"query": query, "variables": variables or {}},
            timeout=30,
        )
        if r.status_code == 429:
            wait = int(r.headers.get("Retry-After", "10"))
            print(f"  rate-limited; sleeping {wait}s")
            time.sleep(wait)
            continue
        r.raise_for_status()
        data = r.json()
        if "errors" in data:
            # Rate-limit errors sometimes show up in the body
            err_text = json.dumps(data["errors"])
            if "ComplexityException" in err_text or "rate limit" in err_text.lower():
                print(f"  complexity/rate limit; sleeping 10s")
                time.sleep(10)
                continue
            raise RuntimeError(json.dumps(data["errors"], indent=2))
        return data["data"]
    raise RuntimeError("gql: exhausted retries")


def fetch_live_items(token: str) -> tuple[str, list[dict[str, Any]]]:
    """Fetch all items in the Live group via items_page pagination."""
    # Step 1: find the Live group id
    q = """
    query ($board_id: [ID!]) {
      boards(ids: $board_id) {
        groups { id title }
      }
    }
    """
    data = gql(token, q, {"board_id": [str(BOARD_ID)]})
    groups = data["boards"][0]["groups"]
    live = next((g for g in groups if g["title"].strip().lower() == LIVE_GROUP_TITLE.lower()), None)
    if not live:
        sys.exit(f"No group titled '{LIVE_GROUP_TITLE}' on board {BOARD_ID}. Found: {[g['title'] for g in groups]}")
    group_id = live["id"]

    # Step 2: paginate items_page within the group
    items: list[dict[str, Any]] = []
    cursor: str | None = None
    page_q = """
    query ($board_id: ID!, $group_id: String!, $cursor: String) {
      boards(ids: [$board_id]) {
        groups(ids: [$group_id]) {
          items_page(limit: 100, cursor: $cursor) {
            cursor
            items {
              id
              name
              column_values { id text value column { title } }
            }
          }
        }
      }
    }
    """
    while True:
        data = gql(token, page_q, {"board_id": str(BOARD_ID), "group_id": group_id, "cursor": cursor})
        page = data["boards"][0]["groups"][0]["items_page"]
        items.extend(page["items"])
        cursor = page.get("cursor")
        if not cursor:
            break
    return group_id, items


# ---------- Title matching -----------------------------------------------------

# Generic words that appear too often to discriminate.
_STOPWORDS = {
    "a", "an", "the", "and", "or", "of", "in", "on", "to", "for", "is", "are", "be",
    "what", "how", "why", "when", "who", "which", "do", "does", "can", "your", "you",
    "my", "i", "it", "its", "as", "at", "by", "with", "from", "into", "than",
    "uk", "ltd",
    "company", "companies", "debt", "debts",
    "guide", "guides", "explained", "explain", "explainer", "overview",
    "limited", "directors", "director", "businesses", "business",
    "2024", "2025", "2026", "2027",
    "hub", "key", "complete", "full", "step", "steps",
}
_PUNCT_RE = re.compile(r"[^\w\s]", re.UNICODE)


def normalise(title: str) -> str:
    t = title.lower()
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    t = _PUNCT_RE.sub(" ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def token_set(text: str) -> set[str]:
    """Extract content tokens, dropping stopwords and very short tokens."""
    out = set()
    for tok in normalise(text).split():
        if not tok or len(tok) <= 2:
            continue
        if tok in _STOPWORDS:
            continue
        out.add(tok)
    return out


def slug_from_url(url_text: str | None) -> str:
    """Extract URL slug from the 'Staging URL' field (which may contain '/path/ - https://...').
    We grab the trailing path segments."""
    if not url_text:
        return ""
    # Format observed: "/liquidation/am-i-solvent/ - https://...". Take the first space-separated piece.
    first = url_text.split(" - ")[0].strip().strip("/")
    return first.replace("/", " ").replace("-", " ")


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, normalise(a), normalise(b)).ratio()


def parse_csv(path: Path) -> list[tuple[str, int]]:
    """Parse a GA4 Pages and screens CSV. Works with title-based or path-based exports —
    the first column is whatever dimension was selected; we treat it as the key."""
    rows: list[tuple[str, int]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        lines = [ln for ln in fh if not ln.lstrip().startswith("#")]
    reader = csv.reader(lines)
    next(reader, None)  # header
    for row in reader:
        if len(row) < 2:
            continue
        key = row[0].strip()
        try:
            views = int(row[1])
        except ValueError:
            continue
        if key:
            rows.append((key, views))
    return rows


def normalise_path(p: str) -> str:
    """Canonicalise a path for matching: lowercase, strip whitespace, ensure single trailing slash."""
    if not p:
        return ""
    p = p.strip().lower()
    # Strip query/fragment
    p = p.split("?", 1)[0].split("#", 1)[0]
    # Drop scheme + host if a full URL slipped in
    if "://" in p:
        try:
            p = "/" + p.split("://", 1)[1].split("/", 1)[1]
        except IndexError:
            pass
    if not p.startswith("/"):
        p = "/" + p
    if not p.endswith("/"):
        p = p + "/"
    return p


def extract_monday_path(item: dict[str, Any]) -> str:
    """Extract the canonical path from Monday's Staging URL (or Live URL) column.

    Staging URL format observed: '/liquidation/am-i-solvent/ - https://comdebstage.wpengine.com/...'
    """
    for col_title in ("Staging URL", "Live URL"):
        for cv in item.get("column_values", []):
            if cv.get("column", {}).get("title") == col_title and cv.get("text"):
                text = cv["text"].strip()
                # Take the part before ' - ' if present (the bare path), else parse the URL
                first = text.split(" - ", 1)[0].strip()
                if first.startswith("/"):
                    return normalise_path(first)
                # Fallback: pull path from the URL
                if "://" in text:
                    return normalise_path(text)
    return ""


def strip_brand_suffix(title: str) -> str:
    # Remove trailing "- Company Debt", "| Company Debt", etc.
    return re.sub(r"\s*[-–|]+\s*Company\s*Debt(\s*Ltd)?\s*$", "", title, flags=re.IGNORECASE).strip()


def get_url_text(item: dict[str, Any]) -> str:
    for cv in item.get("column_values", []):
        if cv.get("column", {}).get("title") in ("Staging URL", "Live URL") and cv.get("text"):
            return cv["text"]
    return ""


def build_item_tokens(item: dict[str, Any]) -> set[str]:
    """Combine item name + URL slug tokens for richer matching."""
    name = item["name"]
    url = get_url_text(item)
    slug_text = slug_from_url(url)
    return token_set(strip_brand_suffix(name)) | token_set(slug_text)


def match_score(item_tokens: set[str], ga_tokens: set[str]) -> float:
    """Asymmetric containment: how much of the (shorter) Monday key is in the GA title."""
    if not item_tokens or not ga_tokens:
        return 0.0
    overlap = len(item_tokens & ga_tokens)
    # Containment of Monday tokens in GA title tokens (Monday is the shorter key).
    monday_containment = overlap / len(item_tokens)
    # Mutual coverage to avoid generic short Monday names matching everything.
    ga_containment = overlap / len(ga_tokens)
    # Combined: prefer high Monday containment but require some GA discrimination.
    return monday_containment * (0.6 + 0.4 * ga_containment)


def match_items_by_path(
    monday_items: list[dict[str, Any]],
    ga_rows: list[tuple[str, int]],
) -> tuple[list[dict[str, Any]], list[tuple[str, int]], list[dict[str, Any]], list[str]]:
    """Direct path-based match. GA rows are (path, views).

    Returns:
      ranked              : Monday items sorted by views desc
      orphan_ga           : (path, views) GA rows with no Monday item
      duplicate_paths     : Monday items sharing the same canonical path (we'd merge views into one)
      missing_url_items   : Monday items with no parseable Staging URL
    """
    # Index GA by path
    ga_by_path: dict[str, int] = {}
    for raw_path, views in ga_rows:
        np = normalise_path(raw_path)
        ga_by_path[np] = ga_by_path.get(np, 0) + views

    # Index Monday by path
    monday_by_path: dict[str, list[dict[str, Any]]] = {}
    missing_url_items: list[str] = []
    for item in monday_items:
        path = extract_monday_path(item)
        if not path:
            missing_url_items.append(f"{item['name']} (id {item['id']})")
            continue
        monday_by_path.setdefault(path, []).append(item)

    # Identify duplicates: same path on multiple Monday items
    duplicates: list[dict[str, Any]] = []
    for path, items in monday_by_path.items():
        if len(items) > 1:
            duplicates.append({
                "path": path,
                "views": ga_by_path.get(path, 0),
                "items": [{"id": it["id"], "name": it["name"]} for it in items],
            })

    # Build per-item view counts. For duplicate paths, all items get the same view count
    # (we surface the duplicate to the user — we do NOT pick a winner silently).
    results: list[dict[str, Any]] = []
    matched_paths: set[str] = set()
    for item in monday_items:
        path = extract_monday_path(item)
        views = ga_by_path.get(path, 0) if path else 0
        if path and path in ga_by_path:
            matched_paths.add(path)
        results.append({
            "item_id": item["id"],
            "item_name": item["name"],
            "path": path,
            "views": views,
            "matched_titles": [(path, views, "path", 1.0)] if views else [],
            "match_type": "path" if views else "none",
        })

    orphan_ga = [(p, v) for p, v in ga_by_path.items() if p not in matched_paths]
    orphan_ga.sort(key=lambda x: -x[1])

    results.sort(key=lambda r: (-r["views"], r["item_name"].lower()))
    return results, orphan_ga, duplicates, missing_url_items


# Legacy fuzzy matcher kept below for fallback (unused when paths available)
def match_items_to_ga(
    monday_items: list[dict[str, Any]],
    ga_rows: list[tuple[str, int]],
    min_overlap_tokens: int = 2,
    min_score: float = 0.55,
) -> tuple[list[dict[str, Any]], list[tuple[str, int]], list[dict[str, Any]], list[dict[str, Any]]]:
    """For each Monday item, find GA title(s) that map to it.

    Returns:
      ranked       : list of {item, views, matched_titles, match_type} sorted desc by views
      orphan_ga    : GA titles not matched to any Monday item (informational)
      ambiguous    : Monday items where multiple plausible GA titles were merged (likely renames)
      contested_ga : GA titles that plausibly matched multiple Monday items (need user choice)
    """
    # Pre-tokenise GA rows
    ga_pool: list[tuple[str, int, set[str]]] = []
    for title, views in ga_rows:
        clean = strip_brand_suffix(title)
        ga_pool.append((title, views, token_set(clean)))

    # Pre-tokenise Monday items
    monday_tokens = [(it, build_item_tokens(it)) for it in monday_items]

    # First pass: for every (item, GA) pair that scores high enough, record candidate.
    candidates: dict[int, list[tuple[int, float, str, int]]] = {}  # ga_idx -> [(item_idx, score, name, views)]
    item_candidates: dict[int, list[tuple[int, float, str, int]]] = {}  # item_idx -> [(ga_idx, score, title, views)]

    for it_idx, (item, it_tokens) in enumerate(monday_tokens):
        if not it_tokens:
            continue
        for ga_idx, (title, views, ga_tokens) in enumerate(ga_pool):
            if not ga_tokens:
                continue
            overlap = len(it_tokens & ga_tokens)
            if overlap < min_overlap_tokens:
                # Allow single-token overlap only if Monday side has only 1 token total
                if not (len(it_tokens) == 1 and overlap == 1):
                    continue
            score = match_score(it_tokens, ga_tokens)
            if score < min_score:
                continue
            candidates.setdefault(ga_idx, []).append((it_idx, score, item["name"], views))
            item_candidates.setdefault(it_idx, []).append((ga_idx, score, title, views))

    # Resolve contested GA: each GA row is assigned to its best item.
    contested_ga_records: list[dict[str, Any]] = []
    ga_assignment: dict[int, int] = {}  # ga_idx -> chosen item_idx
    for ga_idx, cand_list in candidates.items():
        cand_list.sort(key=lambda x: -x[1])  # by score desc
        best = cand_list[0]
        ga_assignment[ga_idx] = best[0]
        # If 2+ items had a high score, surface as contested
        runners = [c for c in cand_list[1:] if c[1] >= best[1] - 0.10 and c[1] >= 0.65]
        if runners:
            title, views, _ = ga_pool[ga_idx]
            contested_ga_records.append({
                "ga_title": title,
                "views": views,
                "winner": {"item_id": monday_items[best[0]]["id"], "item_name": best[2], "score": round(best[1], 3)},
                "runners_up": [
                    {"item_id": monday_items[r[0]]["id"], "item_name": r[2], "score": round(r[1], 3)}
                    for r in runners
                ],
            })

    # Build per-item match list from assignments
    item_matches: dict[int, list[tuple[int, str, int, float]]] = {}  # item_idx -> [(ga_idx, title, views, score)]
    for ga_idx, item_idx in ga_assignment.items():
        title, views, _ = ga_pool[ga_idx]
        # Find score from item_candidates
        score = next((s for (gi, s, _, _) in item_candidates[item_idx] if gi == ga_idx), 0.0)
        item_matches.setdefault(item_idx, []).append((ga_idx, title, views, score))

    # Build results
    results: list[dict[str, Any]] = []
    ambiguous: list[dict[str, Any]] = []
    for it_idx, item in enumerate(monday_items):
        matches = item_matches.get(it_idx, [])
        # Sort matches by views desc
        matches.sort(key=lambda m: -m[2])
        total_views = sum(m[2] for m in matches)
        if not matches:
            match_type = "none"
        elif len(matches) == 1:
            # Was the score very high?
            match_type = "exact" if matches[0][3] >= 0.95 else "fuzzy"
        else:
            match_type = "merged"

        record = {
            "item_id": item["id"],
            "item_name": item["name"],
            "url": get_url_text(item),
            "views": total_views,
            "matched_titles": [(m[1], m[2], "match", round(m[3], 3)) for m in matches],
            "match_type": match_type,
        }
        results.append(record)
        if len(matches) >= 2:
            ambiguous.append(record)

    orphan_ga = [(ga_pool[i][0], ga_pool[i][1]) for i in range(len(ga_pool)) if i not in ga_assignment]
    results.sort(key=lambda r: (-r["views"], r["item_name"].lower()))
    return results, orphan_ga, ambiguous, contested_ga_records


# ---------- Output -------------------------------------------------------------

def print_dry_run_paths(
    ranked: list[dict[str, Any]],
    orphan_ga: list[tuple[str, int]],
    duplicates: list[dict[str, Any]],
    missing_url_items: list[str],
) -> None:
    print(f"\n=== Proposed new order for 'Live' group ({len(ranked)} items) ===\n")
    print(f"{'Rank':>4}  {'Views':>6}  Item name  -->  /path/")
    print("-" * 110)
    for i, r in enumerate(ranked, 1):
        path_disp = r["path"] or "(no URL)"
        print(f"{i:>4}  {r['views']:>6}  {r['item_name'][:60]:<60}  -->  {path_disp}")

    no_match = [r for r in ranked if r["views"] == 0]
    if no_match:
        print(f"\n--- Monday items with 0 views in GA window ({len(no_match)}) — pushed to bottom ---")
        for r in no_match:
            path_disp = r["path"] or "(NO URL on Monday)"
            print(f"  - {r['item_name']:<55}  {path_disp}")

    if duplicates:
        print(f"\n--- Monday items sharing the SAME path ({len(duplicates)}) — NEED YOUR DECISION ---")
        for d in duplicates:
            print(f"  - {d['path']}  ({d['views']} views)")
            for it in d["items"]:
                print(f"      id {it['id']}  {it['name']}")

    if missing_url_items:
        print(f"\n--- Monday items with NO Staging URL ({len(missing_url_items)}) — placed at bottom alphabetically ---")
        for line in missing_url_items:
            print(f"  - {line}")

    if orphan_ga:
        print(f"\n--- GA paths with NO Monday item ({len(orphan_ga)}) — informational only, NOT added ---")
        for path, views in orphan_ga:
            print(f"  {views:>4}  {path}")


def write_snapshot(ranked: list[dict[str, Any]], path: Path) -> None:
    path.write_text(json.dumps(ranked, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSnapshot written to {path}")


# ---------- Apply (reorder only — no other writes) -----------------------------

def apply_reorder(token: str, ranked: list[dict[str, Any]], group_id: str) -> None:
    """Move items into the desired order using change_item_position (API 2025-10).

    Strategy: place item[0] at group_top, then each subsequent item after_at the previous one.
    No other mutation is performed — only position is touched.
    """
    print("\n=== APPLYING reorder (positions only) ===")
    if not ranked:
        return

    api_version = "2025-10"

    # Step 1: lift item[0] to the top of the group
    top_mutation = """
    mutation ($item_id: ID!, $group_id: ID!) {
      change_item_position(item_id: $item_id, group_id: $group_id, group_top: true) { id }
    }
    """
    gql(token, top_mutation, {"item_id": str(ranked[0]["item_id"]), "group_id": group_id}, api_version=api_version)
    print(f"  positioned 1/{len(ranked)} (top): {ranked[0]['item_name'][:60]}")

    # Step 2: each remaining item goes after_at its predecessor in the new order
    after_mutation = """
    mutation ($item_id: ID!, $relative_to: ID!) {
      change_item_position(item_id: $item_id, relative_to: $relative_to, position_relative_method: after_at) { id }
    }
    """
    for i in range(1, len(ranked)):
        prev_id = ranked[i - 1]["item_id"]
        cur_id = ranked[i]["item_id"]
        gql(token, after_mutation, {"item_id": str(cur_id), "relative_to": str(prev_id)}, api_version=api_version)
        if (i + 1) % 25 == 0:
            print(f"  positioned {i + 1}/{len(ranked)}")
    print(f"\nDone. Repositioned {len(ranked)} items in 'Live' group.")


# ---------- main ---------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True, help="Path to GA4 Pages and screens CSV")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--snapshot", default="data/monday-live-reorder-plan.json")
    ap.add_argument("--fuzzy-threshold", type=float, default=0.78)
    args = ap.parse_args()

    if args.apply == args.dry_run:
        sys.exit("Pick exactly one of --dry-run or --apply.")

    token = load_env()
    csv_path = Path(args.csv)
    if not csv_path.exists():
        sys.exit(f"CSV not found: {csv_path}")

    print(f"Loading GA CSV: {csv_path}")
    ga_rows = parse_csv(csv_path)
    print(f"  parsed {len(ga_rows)} GA rows")

    print(f"Fetching 'Live' group from Monday board {BOARD_ID}...")
    group_id, items = fetch_live_items(token)
    print(f"  fetched {len(items)} Live items")

    # Detect path-based vs title-based CSV: paths start with '/'
    is_path_csv = bool(ga_rows) and ga_rows[0][0].startswith("/")
    if is_path_csv:
        print("Detected path-based CSV — using direct URL matching")
        ranked, orphan_ga, duplicates, missing_url = match_items_by_path(items, ga_rows)
        print_dry_run_paths(ranked, orphan_ga, duplicates, missing_url)
    else:
        sys.exit("Title-based CSV detected. Please re-export with 'Page path and screen class' dimension.")

    snap_path = Path(args.snapshot)
    snap_path.parent.mkdir(parents=True, exist_ok=True)
    write_snapshot(ranked, snap_path)

    if args.apply:
        confirm = os.environ.get("MONDAY_REORDER_CONFIRM")
        if confirm != "yes":
            sys.exit("Refusing to apply: set env MONDAY_REORDER_CONFIRM=yes to proceed.")
        apply_reorder(token, ranked, group_id)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
