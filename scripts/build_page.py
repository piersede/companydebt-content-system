#!/usr/bin/env python3
"""Company Debt Credit Card Page Builder — CLI entry point.

Usage:
    python scripts/build_page.py --page low-apr
    python scripts/build_page.py --page low-apr --preview
    python scripts/build_page.py --page low-apr --publish
    python scripts/build_page.py --page low-apr --publish --id 70072
    python scripts/build_page.py --list

Research commands:
    python scripts/build_page.py --research-cards amex_business_gold,rbs
    python scripts/build_page.py --research-cards all
    python scripts/build_page.py --missing-cards
    python scripts/build_page.py --verify-freshness
"""

import argparse
import importlib
import json
import os
import sys
import tempfile
from pathlib import Path

# Add scripts/ to path so cc_builder is importable
SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))

from cc_builder.data.loader import load_cards_for_page, list_available_cards
from cc_builder.quality_checks import run_all_checks, print_report


# ── Page registry ──────────────────────────────────────────────────────
# Maps slug to module path in cc_builder.data.pages

PAGE_REGISTRY = {
    # Roundup pages (11)
    'low-apr': 'cc_builder.data.pages.low_apr',
    'best-business-credit-cards': 'cc_builder.data.pages.best_business_credit_cards',
    'sole-traders': 'cc_builder.data.pages.sole_traders',
    'cashback-reward': 'cc_builder.data.pages.cashback_reward',
    'start-ups': 'cc_builder.data.pages.start_ups',
    'poor-credit': 'cc_builder.data.pages.poor_credit',
    'interest-free': 'cc_builder.data.pages.interest_free',
    'travel': 'cc_builder.data.pages.travel',
    'air-miles-avios': 'cc_builder.data.pages.air_miles_avios',
    'instant-approval': 'cc_builder.data.pages.instant_approval',
    'charge-cards': 'cc_builder.data.pages.charge_cards',
    # Review pages (3)
    'capital-on-tap-review': 'cc_builder.data.pages.capital_on_tap_review',
    'funding-circle-review': 'cc_builder.data.pages.funding_circle_review',
    'flexipay-review': 'cc_builder.data.pages.flexipay_review',
    # Brand comparison pages (3)
    'compare-barclaycard': 'cc_builder.data.pages.compare_barclaycard',
    'compare-amex': 'cc_builder.data.pages.compare_amex',
    'capital-on-tap-vs-amex': 'cc_builder.data.pages.capital_on_tap_vs_amex',
    # Guide pages (3)
    'guide-to-business-credit-cards': 'cc_builder.data.pages.guide_to_business_credit_cards',
    'credit-cards-vs-charge-cards': 'cc_builder.data.pages.credit_cards_vs_charge_cards',
    'balance-transfer': 'cc_builder.data.pages.balance_transfer',
}


def load_page_config(slug: str) -> dict:
    """Import page module and return its PAGE_CONFIG dict."""
    if slug not in PAGE_REGISTRY:
        print(f"ERROR: Unknown page '{slug}'")
        print(f"Available pages: {', '.join(sorted(PAGE_REGISTRY.keys()))}")
        sys.exit(1)

    module = importlib.import_module(PAGE_REGISTRY[slug])
    return module.PAGE_CONFIG


def build_page(slug: str) -> tuple[str, dict]:
    """Build a single page and return (content, config)."""
    config = load_page_config(slug)
    page_type = config.get('page_type', 'roundup')

    # Load card data
    cards, separate_cards = load_cards_for_page(config)

    # Route to the correct assembler
    if page_type == 'roundup':
        from cc_builder.page_types.roundup import assemble
        content = assemble(config, cards, separate_cards)
    elif page_type == 'review':
        from cc_builder.page_types.review import assemble
        content = assemble(config, cards, separate_cards)
    elif page_type in ('brand_comparison', 'brand_compare'):
        from cc_builder.page_types.brand_compare import assemble
        content = assemble(config, cards, separate_cards)
    elif page_type == 'guide':
        from cc_builder.page_types.guide import assemble
        content = assemble(config, cards, separate_cards)
    else:
        print(f"ERROR: Unknown page type '{page_type}'")
        sys.exit(1)

    return content, config


def main():
    parser = argparse.ArgumentParser(
        description='Company Debt Credit Card Page Builder'
    )
    parser.add_argument(
        '--page', type=str,
        help='Page slug to build (e.g. low-apr, cashback)'
    )
    parser.add_argument(
        '--list', action='store_true',
        help='List all registered pages'
    )
    parser.add_argument(
        '--preview', action='store_true',
        help='Also generate a preview HTML file'
    )
    parser.add_argument(
        '--publish', action='store_true',
        help='Push to WordPress staging after building'
    )
    parser.add_argument(
        '--id', type=int, default=None,
        help='WP page/post ID to update (overrides config wp_page_id)'
    )
    parser.add_argument(
        '--cards', action='store_true',
        help='List all available card data files'
    )
    # Research commands
    parser.add_argument(
        '--research-cards', type=str, default=None,
        help='Research cards via Gemini Deep Research (comma-separated IDs, or "all" for missing)'
    )
    parser.add_argument(
        '--missing-cards', action='store_true',
        help='List card IDs that need JSON files'
    )
    parser.add_argument(
        '--verify-freshness', action='store_true',
        help='Check all card data for stale verify_dates'
    )
    parser.add_argument(
        '--force', action='store_true',
        help='Force re-research even if card JSON exists'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Show research prompt without calling API'
    )
    args = parser.parse_args()

    if args.list:
        print('Registered pages:')
        for slug in sorted(PAGE_REGISTRY.keys()):
            config = load_page_config(slug)
            wp_id = config.get('wp_page_id', '?')
            print(f'  {slug}  (WP ID: {wp_id}, type: {config.get("page_type", "?")})')
        return

    if args.cards:
        cards = list_available_cards()
        print(f'Available cards ({len(cards)}):')
        for c in cards:
            print(f'  {c}')
        return

    # ── Research commands ─────────────────────────────────────────────
    if args.missing_cards:
        from cc_builder.research import list_missing_cards, CARD_REGISTRY
        missing = list_missing_cards()
        print(f'Missing card JSON files ({len(missing)}/{len(CARD_REGISTRY)}):')
        for cid in missing:
            meta = CARD_REGISTRY[cid]
            print(f'  {cid:30s}  {meta["name"]}')
        return

    if args.verify_freshness:
        from cc_builder.research import verify_card_freshness
        stale = verify_card_freshness()
        if not stale:
            print('All card data is fresh (< 30 days old)')
        else:
            print(f'Stale card data ({len(stale)} cards):')
            for s in stale:
                age = f"{s['age_days']} days" if s['age_days'] >= 0 else "unparseable date"
                print(f'  {s["card_id"]:30s}  verified: {s["verify_date"]}  ({age})')
        return

    if args.research_cards:
        from cc_builder.research import research_and_create_cards, list_missing_cards, CARD_REGISTRY

        if args.research_cards == 'all':
            card_ids = list_missing_cards()
            if not card_ids:
                print('All cards have JSON files. Use --force to re-research.')
                if args.force:
                    card_ids = list(CARD_REGISTRY.keys())
                else:
                    return
        else:
            card_ids = [c.strip() for c in args.research_cards.split(',')]

        print(f'Researching {len(card_ids)} cards: {", ".join(card_ids)}')
        saved = research_and_create_cards(card_ids, dry_run=args.dry_run)
        if saved:
            print(f'\nCreated {len(saved)} card draft JSONs.')
            print('Review each file and fill in [VERIFY] / [NEEDS_IMAGE] placeholders.')
        return

    if not args.page:
        parser.print_help()
        sys.exit(1)

    # Build
    print(f'Building page: {args.page}')
    content, config = build_page(args.page)

    block_count = content.count('<!-- wp:')
    print(f'Generated {block_count} blocks, {len(content):,} chars')

    # Quality checks (always run, block publish on FAIL)
    passed, violations = run_all_checks(config, content)
    print_report(violations, args.page)
    if not passed and args.publish:
        print('\nERROR: Quality checks failed. Fix FAIL issues before publishing.',
              file=sys.stderr)
        sys.exit(1)

    # Write JSON output
    out_path = os.path.join(tempfile.gettempdir(), f'wp_push_{args.page}.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({'content': content}, f, ensure_ascii=False)
    print(f'Written to {out_path}')

    # Preview
    if args.preview:
        preview_dir = SCRIPTS_DIR.parent / 'preview'
        preview_dir.mkdir(exist_ok=True)
        preview_path = preview_dir / f'{config["slug"]}.html'
        # Minimal preview wrapper
        preview_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{config["title"]}</title>
<meta name="description" content="{config.get("meta_description", "")}">
</head>
<body data-slug="{config["slug"]}">
<article class="entry-content container">
{content}
</article>
</body>
</html>'''
        with open(preview_path, 'w', encoding='utf-8') as f:
            f.write(preview_html)
        print(f'Preview: {preview_path}')

    # Publish
    if args.publish:
        from wp_publish import get_credentials, push_to_wordpress, create_authenticated_session
        creds = get_credentials(prod=False)

        wp_id = args.id or config.get('wp_page_id')
        if not wp_id:
            print('ERROR: No WP page ID. Use --id or set wp_page_id in page config.')
            sys.exit(1)

        # Build metadata excerpt to replace the theme deck/subtitle
        card_count = len(config.get('card_ids', [])) + len(config.get('separate_card_ids', []))
        verify_date = config.get('verification_date', 'March 2026')
        excerpt = (
            f'{card_count} cards reviewed · Independently assessed'
            f' · Rates verified {verify_date}'
        )

        article = {
            'title': config['title'],
            'slug': config['slug'],
            'content': content,
            'meta_description': config.get('meta_description', ''),
            'category_name': '',
            'excerpt': excerpt,
        }

        push_to_wordpress(article, creds, status='publish', post_id=wp_id, post_type='pages')


if __name__ == '__main__':
    main()
