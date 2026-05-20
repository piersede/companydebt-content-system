"""Fetch a staging page by slug, run the canonical article audit, and write the
score into Monday's 'Score 1.5' column.

Usage:
  python scripts/audit_staging_page.py --slug liquidation --monday-item 11624425693 [--apply]

Touches ONLY the Score 1.5 column on Monday. No other column or property is changed.
The fetched HTML is saved to drafts/<post-id>_<slug>.html so the audit can run
unchanged against the canonical script's expected file format.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import sys
from pathlib import Path

import requests

# Ensure UTF-8 stdout on Windows
if sys.platform == "win32":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)
    except Exception:
        pass

# Reuse repo helpers
sys.path.insert(0, str(Path(__file__).resolve().parent))
from wp_publish import get_credentials, create_authenticated_session  # noqa: E402
from article_audit import audit_file, _square, print_report  # noqa: E402

from dotenv import load_dotenv  # noqa: E402

BOARD_ID = 18406273663
SCORE_15_COLUMN_ID = "text_mm2xqrt8"  # Score 1.5
MONDAY_URL = "https://api.monday.com/v2"


def gql(token: str, query: str, variables: dict | None = None) -> dict:
    r = requests.post(
        MONDAY_URL,
        headers={"Authorization": token, "Content-Type": "application/json", "API-Version": "2025-10"},
        json={"query": query, "variables": variables or {}},
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    if "errors" in data:
        raise RuntimeError(json.dumps(data["errors"], indent=2))
    return data["data"]


def fetch_page_raw(slug: str) -> dict:
    creds = get_credentials(prod=False)
    session, api_base = create_authenticated_session(creds)
    r = session.get(f"{api_base}/pages", params={"slug": slug, "context": "edit", "status": "any"}, timeout=30)
    r.raise_for_status()
    pages = r.json()
    if not pages:
        sys.exit(f"No page found with slug '{slug}' on staging")
    return pages[0]


def write_draft_file(page: dict, slug: str, drafts_dir: Path) -> Path:
    post_id = page["id"]
    title = page["title"]["raw"]
    author = page.get("author", "")
    fm = page.get("featured_media", "")
    template = page.get("template", "") or "templates/take-the-test-template.php"
    link = page.get("link", "")
    content = page["content"]["raw"]

    drafts_dir.mkdir(parents=True, exist_ok=True)
    out = drafts_dir / f"{post_id}_{slug}.html"
    header = (
        f"<!-- TITLE: {title} -->\n"
        f"<!-- POST ID: {post_id} / TYPE: pages / AUTHOR: {author} / FM: {fm} / TEMPLATE: {template} -->\n"
        f"<!-- LINK: {link} -->\n\n"
    )
    out.write_text(header + content, encoding="utf-8")
    return out


def write_score_to_monday(token: str, item_id: str, score: int, max_score: int) -> None:
    label = f"{_square(score, max_score)} {score}/{max_score}"
    mutation = """
    mutation ($board: ID!, $item: ID!, $col: String!, $val: String!) {
      change_simple_column_value(board_id: $board, item_id: $item, column_id: $col, value: $val) { id }
    }
    """
    gql(token, mutation, {
        "board": str(BOARD_ID),
        "item": str(item_id),
        "col": SCORE_15_COLUMN_ID,
        "val": label,
    })
    print(f"\nWrote to Monday Score 1.5: {label}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True, help="WordPress page slug (e.g. 'liquidation')")
    ap.add_argument("--monday-item", required=True, help="Monday item id to score")
    ap.add_argument("--apply", action="store_true", help="Write the score to Monday")
    args = ap.parse_args()

    # Load Monday token from .env (climb up to repo root)
    here = Path(__file__).resolve()
    for c in [here.parents[1] / ".env", here.parents[3] / ".env", here.parents[4] / ".env"]:
        if c.exists():
            load_dotenv(c); break
    monday_token = os.environ.get("MONDAY_API_KEY")
    if args.apply and not monday_token:
        sys.exit("MONDAY_API_KEY required for --apply")

    print(f"Fetching staging page slug='{args.slug}'...")
    page = fetch_page_raw(args.slug)
    print(f"  post_id={page['id']} title={page['title']['raw']!r}")

    drafts_dir = Path("drafts")
    out = write_draft_file(page, args.slug, drafts_dir)
    print(f"  saved draft: {out}")

    print("\nRunning canonical audit...")
    audit = audit_file(out)
    print_report(audit)

    if args.apply:
        if os.environ.get("AUDIT_WRITE_CONFIRM") != "yes":
            sys.exit("Refusing to write: set AUDIT_WRITE_CONFIRM=yes to proceed.")
        write_score_to_monday(monday_token, args.monday_item, audit.score, audit.max_score)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
