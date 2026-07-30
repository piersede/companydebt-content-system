#!/usr/bin/env python3
"""Company Debt page builder — CLI entry point.

Insolvency / editorial pages: content is authored in drafts/{wp_id}_{slug}.html
and this builder assembles the WordPress block payload from it. (The original
Business Expert credit-card rendering engine has been removed; it had no place
on an insolvency site.)

Usage:
    python scripts/build_page.py --page liquidation
    python scripts/build_page.py --page liquidation --preview
    python scripts/build_page.py --page liquidation --publish
    python scripts/build_page.py --page liquidation --publish --id 7669
    python scripts/build_page.py --list
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

from page_runtime_metadata import resolve_page_runtime_metadata
from runtime_pack_router import resolve_runtime_context


# ── Page registry ──────────────────────────────────────────────────────
# Maps slug to module path in cc_builder.data.pages

PAGE_REGISTRY = {
    # ── Insolvency pages ────────────────────────────────────────────────
    # Slim configs (slug, title, page_type, wp_page_id, verification_date).
    # Page-class routing for these slugs is in scripts/page_runtime_metadata.py
    # SLUG_PAGE_CLASS_OVERRIDES.
    'liquidation': 'cc_builder.data.pages.liquidation',
    'members-voluntary-liquidation': 'cc_builder.data.pages.members_voluntary_liquidation',
    'creditors-voluntary-liquidation': 'cc_builder.data.pages.creditors_voluntary_liquidation',
    'uk-insolvency-statistics': 'cc_builder.data.pages.uk_insolvency_statistics',
    'cant-pay-vat': 'cc_builder.data.pages.cant_pay_vat',
    'winding-up-petitions': 'cc_builder.data.pages.winding_up_petitions',
    'problems-paying-corporation-tax-hmrc': 'cc_builder.data.pages.problems_paying_corporation_tax_hmrc',
    # The insolvency data hub: lives at /data/ (page 79845, slug 'data').
    # Module file keeps its company_insolvency.py name; the page slug is 'data'.
    'data': 'cc_builder.data.pages.company_insolvency',
    'winding-up-petition-tracker': 'cc_builder.data.pages.winding_up_petition_tracker',
    'dissolutions-vs-insolvencies': 'cc_builder.data.pages.company_dissolutions_vs_insolvencies',
    'payment-practices-late-payment': 'cc_builder.data.pages.payment_practices_late_payment',
    'cvl-statistics': 'cc_builder.data.pages.cvl_statistics',
    'compulsory-liquidation-statistics': 'cc_builder.data.pages.compulsory_liquidation_statistics',
    'administration-statistics': 'cc_builder.data.pages.administration_statistics',
    'company-insolvencies-by-sector': 'cc_builder.data.pages.company_insolvencies_by_sector',
    'construction-insolvency-statistics': 'cc_builder.data.pages.construction_insolvency_statistics',
    'furniture-insolvency-statistics': 'cc_builder.data.pages.furniture_insolvency_statistics',
    'restaurant-insolvency-statistics': 'cc_builder.data.pages.restaurant_insolvency_statistics',
    'road-haulage-insolvency-statistics': 'cc_builder.data.pages.road_haulage_insolvency_statistics',
    'recruitment-agency-insolvency-statistics': 'cc_builder.data.pages.recruitment_agency_insolvency_statistics',
    'temporary-staffing-agency-insolvency-statistics': 'cc_builder.data.pages.temporary_staffing_agency_insolvency_statistics',
    'motor-vehicle-repair-insolvency-statistics': 'cc_builder.data.pages.motor_vehicle_repair_insolvency_statistics',
    'cleaning-company-insolvency-statistics': 'cc_builder.data.pages.cleaning_company_insolvency_statistics',
    'hotel-insolvency-statistics': 'cc_builder.data.pages.hotel_insolvency_statistics',
    'estate-agency-insolvency-statistics': 'cc_builder.data.pages.estate_agency_insolvency_statistics',
    'it-consultancy-insolvency-statistics': 'cc_builder.data.pages.it_consultancy_insolvency_statistics',
    'management-consultancy-insolvency-statistics': 'cc_builder.data.pages.management_consultancy_insolvency_statistics',
    'architectural-engineering-insolvency-statistics': 'cc_builder.data.pages.architectural_engineering_insolvency_statistics',
    'personal-care-services-insolvency-statistics': 'cc_builder.data.pages.personal_care_services_insolvency_statistics',
    'sports-facility-insolvency-statistics': 'cc_builder.data.pages.sports_facility_insolvency_statistics',
    'medical-dental-practice-insolvency-statistics': 'cc_builder.data.pages.medical_dental_practice_insolvency_statistics',
    'creative-arts-entertainment-insolvency-statistics': 'cc_builder.data.pages.creative_arts_entertainment_insolvency_statistics',
    'amusement-recreation-insolvency-statistics': 'cc_builder.data.pages.amusement_recreation_insolvency_statistics',
    'real-estate-letting-investment-insolvency-statistics': 'cc_builder.data.pages.real_estate_letting_investment_insolvency_statistics',
    'freight-forwarding-logistics-insolvency-statistics': 'cc_builder.data.pages.freight_forwarding_logistics_insolvency_statistics',
    'retail-insolvency-statistics': 'cc_builder.data.pages.retail_insolvency_statistics',
    'are-directors-personally-liable-for-company-debts': 'cc_builder.data.pages.are_directors_personally_liable_for_company_debts',
    'construction-insolvency': 'cc_builder.data.pages.construction_insolvency',
    # ── Sector pages (/sectors/*) — clean-rebuild programme, posts not pages ──
    'construction': 'cc_builder.data.pages.construction_sector',
    'garden-centres': 'cc_builder.data.pages.garden_centres_sector',
    'hotels': 'cc_builder.data.pages.hotels_sector',
    'care-homes': 'cc_builder.data.pages.care_homes_sector',
    'automotive': 'cc_builder.data.pages.automotive_sector',
    'retail': 'cc_builder.data.pages.retail_sector',
    'restaurants': 'cc_builder.data.pages.restaurants_sector',
    'recruitment': 'cc_builder.data.pages.recruitment_sector',
    'gyms': 'cc_builder.data.pages.gyms_sector',
    'leisure': 'cc_builder.data.pages.leisure_sector',
    'childcare': 'cc_builder.data.pages.childcare_sector',
    'charity': 'cc_builder.data.pages.charity_sector',
    'professional-services': 'cc_builder.data.pages.professional_services_sector',
    'events': 'cc_builder.data.pages.events_sector',
    'taxi-companies': 'cc_builder.data.pages.taxi_companies_sector',
    'cleaning-contractors': 'cc_builder.data.pages.cleaning_contractors_sector',
    'haulage': 'cc_builder.data.pages.haulage_sector',
    'dry-cleaning-laundry': 'cc_builder.data.pages.dry_cleaning_laundry_sector',
    'property': 'cc_builder.data.pages.property_sector',
    'entertainment': 'cc_builder.data.pages.entertainment_sector',
    'fish-chip': 'cc_builder.data.pages.fish_chip_sector',
    'schools': 'cc_builder.data.pages.schools_sector',
    'travel': 'cc_builder.data.pages.travel_sector',
    'manufacturing': 'cc_builder.data.pages.manufacturing_sector',
    'energy': 'cc_builder.data.pages.energy_sector',
    # ── Data-led article rebuilds (posts, not pages) ────────────────────
    'pub-closures-in-the-uk': 'cc_builder.data.pages.pub_closures_in_the_uk',
    'how-much-does-liquidation-cost': 'cc_builder.data.pages.how_much_does_liquidation_cost',
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
    page_type = config.get('page_type', '')

    if page_type in ('data_reference', 'definition', 'process_guide', 'hub'):
        # Insolvency and editorial pages: read content directly from the draft file.
        # Draft files live at drafts/{wp_page_id}_{slug}.html and contain WordPress
        # block content preceded by metadata comment lines (<!-- TITLE: ... --> etc.).
        wp_id = config.get('wp_page_id', '')
        slug = config.get('slug', '')
        draft_path = SCRIPTS_DIR.parent / 'drafts' / f'{wp_id}_{slug}.html'
        if not draft_path.exists():
            print(f"ERROR: Draft file not found: {draft_path}")
            sys.exit(1)
        raw = draft_path.read_text(encoding='utf-8')
        # Strip leading metadata comment lines and blank lines
        lines = raw.splitlines()
        content_lines = []
        past_header = False
        for line in lines:
            if not past_header:
                stripped = line.strip()
                if stripped.startswith('<!-- TITLE:') or stripped.startswith('<!-- POST ID:') or stripped.startswith('<!-- LINK:'):
                    continue
                if stripped == '' and not content_lines:
                    continue
                past_header = True
            content_lines.append(line)
        content = '\n'.join(content_lines).strip()
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
        '--show-runtime-packs', action='store_true',
        help='Show the system-decided runtime context for the requested page and task'
    )
    parser.add_argument(
        '--task', type=str, default='build',
        help='Task name for runtime context inspection (default: build)'
    )
    parser.add_argument(
        '--page-class', type=str, default=None,
        help='Optional Company Debt page class for runtime context inspection'
    )
    parser.add_argument(
        '--freshness-tier', type=str, default=None,
        help='Optional freshness tier for runtime context inspection'
    )
    args = parser.parse_args()

    if args.list:
        print('Registered pages:')
        for slug in sorted(PAGE_REGISTRY.keys()):
            config = load_page_config(slug)
            runtime_metadata = resolve_page_runtime_metadata(config, slug=config.get('slug', slug))
            wp_id = config.get('wp_page_id', '?')
            print(
                f'  {slug}  (WP ID: {wp_id}, type: {config.get("page_type", "?")}, '
                f'page_class: {runtime_metadata.page_class or "?"}, '
                f'freshness: {runtime_metadata.freshness_tier or "?"})'
            )
        return

    if not args.page:
        parser.print_help()
        sys.exit(1)

    config = load_page_config(args.page)
    runtime_metadata = resolve_page_runtime_metadata(config, slug=config.get('slug', args.page))

    if args.show_runtime_packs:
        runtime = resolve_runtime_context(
            args.task,
            page_type=config.get('page_type'),
            page_class=args.page_class or runtime_metadata.page_class,
            freshness_tier=args.freshness_tier or runtime_metadata.freshness_tier,
            slug=config.get('slug', args.page),
        )
        print('System-decided runtime context:')
        print(json.dumps(runtime, indent=2))

    # Build
    print(f'Building page: {args.page}')
    content, config = build_page(args.page)

    block_count = content.count('<!-- wp:')
    print(f'Generated {block_count} blocks, {len(content):,} chars')

    # Editorial / insolvency pages go through the Bernstein pipeline gate, not a
    # build-time assembler check.
    print(f'  (editorial page type: {config.get("page_type")}; quality gating via Bernstein)')

    # sector_statistics pages (the SIC-sector data family, e.g. furniture,
    # construction) carry a REAL automated gate — not just this printed claim.
    # Run it here and block --publish on a hard-fail, same discipline as the
    # bernstein.js gate for guide pages, calibrated for this page shape.
    gate_passed = True
    if runtime_metadata.page_class == 'sector_statistics':
        from sector_data_audit import audit_file, print_report
        draft_path = SCRIPTS_DIR.parent / 'drafts' / f"{config.get('wp_page_id')}_{config.get('slug')}.html"
        audit = audit_file(draft_path)
        print_report(audit)
        gate_passed = audit.gate_passed
        if not gate_passed:
            print(f'  SECTOR DATA GATE: FAIL ({audit.score}/{audit.max_score}) — see failures above.')
        else:
            print(f'  SECTOR DATA GATE: PASS ({audit.score}/{audit.max_score})')

    if args.publish and not gate_passed:
        print('ERROR: sector_statistics gate failed — publish blocked. Fix the flagged checks and rebuild.')
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
        verify_date = config.get('verification_date', '')
        excerpt = f'Last reviewed {verify_date}' if verify_date else ''

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
