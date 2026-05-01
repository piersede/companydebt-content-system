"""Register an insolvency page in the Bernstein page registry.

Given a slug, this script:
  1. Fetches the page metadata from staging WP REST API (wp_page_id, title).
  2. Writes a slim PAGE_CONFIG module to scripts/cc_builder/data/pages/<slug>.py.
  3. Adds the slug to PAGE_REGISTRY in scripts/build_page.py under the
     "Insolvency pages" block.

Insolvency configs are intentionally slim (~6 fields) compared to credit-card
configs (~360 lines of card data). Page-class routing comes from
scripts/page_runtime_metadata.py SLUG_PAGE_CLASS_OVERRIDES — confirm the slug
is in that map (or accept a default page-class) before running.

Usage:
    python scripts/register_insolvency_page.py --slug liquidation
    python scripts/register_insolvency_page.py --slug compulsory-liquidation --page-type definition
    python scripts/register_insolvency_page.py --slug liquidation --dry-run
"""

from __future__ import annotations

import argparse
import io
import os
import re
import sys
from datetime import date
from pathlib import Path

# UTF-8 stdout on Windows
if sys.platform == "win32":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from dotenv import load_dotenv

# Walk up to find a .env (worktree-local first, then parent repo)
for c in [ROOT / ".env.local", ROOT / ".env", ROOT.parents[2] / ".env"]:
    if c.exists():
        load_dotenv(c); break

from wp_publish import get_credentials, create_authenticated_session  # noqa: E402

PAGES_DIR = ROOT / "scripts" / "cc_builder" / "data" / "pages"
BUILD_PAGE_PATH = ROOT / "scripts" / "build_page.py"
RUNTIME_METADATA_PATH = ROOT / "scripts" / "page_runtime_metadata.py"


def slug_to_module_name(slug: str) -> str:
    """liquidation -> liquidation; compulsory-liquidation -> compulsory_liquidation"""
    return slug.replace("-", "_")


def fetch_page_meta(slug: str) -> dict:
    """Pull wp_page_id and title from staging WP REST API for the given slug."""
    creds = get_credentials(prod=False)
    session, api_base = create_authenticated_session(creds)
    r = session.get(f"{api_base}/pages", params={"slug": slug, "context": "edit", "status": "any"}, timeout=30)
    r.raise_for_status()
    pages = r.json()
    if not pages:
        sys.exit(f"No page found on staging with slug='{slug}'.")
    p = pages[0]
    return {
        "wp_page_id": p["id"],
        "title": p["title"]["raw"],
        "link": p.get("link", ""),
    }


def page_class_from_overrides(slug: str) -> str | None:
    """Read scripts/page_runtime_metadata.py SLUG_PAGE_CLASS_OVERRIDES and find slug."""
    text = RUNTIME_METADATA_PATH.read_text(encoding="utf-8")
    m = re.search(rf'"{re.escape(slug)}"\s*:\s*"([^"]+)"', text)
    return m.group(1) if m else None


def write_page_config(slug: str, meta: dict, page_type: str, verification_date: str, dry_run: bool) -> Path:
    module_name = slug_to_module_name(slug)
    out = PAGES_DIR / f"{module_name}.py"
    title = meta["title"]
    page_class = page_class_from_overrides(slug) or "(not in SLUG_PAGE_CLASS_OVERRIDES)"
    content = (
        f'"""Page config for: {title}\n'
        f"\n"
        f"Insolvency-page slim config — only the fields the Bernstein pipeline\n"
        f"and runtime-pack router actually read. Page-class routing for this\n"
        f'slug ({page_class}) sits in scripts/page_runtime_metadata.py.\n'
        f'"""\n'
        f"\n"
        f"PAGE_CONFIG = {{\n"
        f"    'slug': '{slug}',\n"
        f"    'page_type': '{page_type}',\n"
        f"    'wp_page_id': {meta['wp_page_id']},\n"
        f"    'title': {repr(title)},\n"
        f"    'verification_date': '{verification_date}',\n"
        f"}}\n"
    )
    if dry_run:
        print(f"\n--- WOULD WRITE: {out} ---\n{content}")
    else:
        out.write_text(content, encoding="utf-8")
        print(f"Wrote {out}")
    return out


def add_registry_entry(slug: str, dry_run: bool) -> None:
    module_name = slug_to_module_name(slug)
    text = BUILD_PAGE_PATH.read_text(encoding="utf-8")

    # If already registered, skip
    if f"'{slug}': 'cc_builder.data.pages.{module_name}'" in text:
        print(f"PAGE_REGISTRY already contains '{slug}' — skipping.")
        return

    # Insertion point: inside the "Insolvency pages" block, before the closing "}"
    if "# ── Insolvency pages" not in text:
        # Insert the section header + entry before the final "}" of PAGE_REGISTRY
        new_block = (
            "    # ── Insolvency pages ────────────────────────────────────────────────\n"
            "    # Slim configs (slug, title, page_type, wp_page_id, verification_date).\n"
            "    # Page-class routing for these slugs is in scripts/page_runtime_metadata.py\n"
            "    # SLUG_PAGE_CLASS_OVERRIDES.\n"
            f"    '{slug}': 'cc_builder.data.pages.{module_name}',\n"
            "}"
        )
        new_text = re.sub(r"^\}[ \t]*$", new_block, text, count=1, flags=re.MULTILINE)
    else:
        # Add the entry just before the closing "}"
        new_entry = f"    '{slug}': 'cc_builder.data.pages.{module_name}',\n}}"
        new_text = re.sub(r"^\}\s*$", new_entry, text, count=1, flags=re.MULTILINE)

    if dry_run:
        diff_start = new_text.find("Insolvency pages")
        if diff_start >= 0:
            print(f"\n--- WOULD UPDATE: {BUILD_PAGE_PATH} ---")
            print(new_text[diff_start - 8 : diff_start + 400])
    else:
        BUILD_PAGE_PATH.write_text(new_text, encoding="utf-8")
        print(f"Updated PAGE_REGISTRY in {BUILD_PAGE_PATH}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True, help="Page slug (e.g. 'liquidation')")
    ap.add_argument(
        "--page-type",
        default="definition",
        help="page_type for PAGE_CONFIG. Default: 'definition'. Common: definition, process, comparison, hub, decision, risk.",
    )
    today = date.today()
    # Cross-platform "%-d %B %Y" — Windows strftime doesn't support %-d.
    default_date = f"{today.day} {today.strftime('%B %Y')}"
    ap.add_argument(
        "--verification-date",
        default=default_date,
        help="Editorial verification date. Default: today as '<day> <Month> <Year>'.",
    )
    ap.add_argument("--dry-run", action="store_true", help="Print the would-be changes without writing.")
    args = ap.parse_args()

    print(f"Fetching staging metadata for slug='{args.slug}'...")
    meta = fetch_page_meta(args.slug)
    print(f"  wp_page_id={meta['wp_page_id']} title={meta['title']!r}")

    page_class = page_class_from_overrides(args.slug)
    if not page_class:
        print(f"  WARNING: '{args.slug}' is not in SLUG_PAGE_CLASS_OVERRIDES. Add it to scripts/page_runtime_metadata.py for runtime-pack routing.")

    write_page_config(args.slug, meta, args.page_type, args.verification_date, args.dry_run)
    add_registry_entry(args.slug, args.dry_run)

    if not args.dry_run:
        print("\nVerify the registration:")
        print(f"  node editorial-os/bernstein.js status {args.slug}")
        print(f"  PYTHONIOENCODING=utf-8 python scripts/editorial_task_entry.py --page {args.slug} --task humanise")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
