"""
Fix broken/redirect internal links found by audit_staging_links.py.

Reads internal_links_problems.csv and:
  - 301/302: updates href to the redirect destination in WP raw content
  - 404/410: copies rows to links_404_needs_decision.csv for manual review
  - 0 (error): skipped with a warning

Usage:
  python scripts/fix_internal_links.py            # dry run (no writes)
  python scripts/fix_internal_links.py --apply    # write changes to staging WP
"""
import os, csv, sys, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from collections import defaultdict
from urllib.parse import urlparse, urlunparse

import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

STAGING_URL  = os.getenv('WP_STAGING_URL', '').rstrip('/')
BA_USER      = os.getenv('WP_BASIC_AUTH_USER', '')
BA_PASS      = os.getenv('WP_BASIC_AUTH_PASS', '')
WP_USER      = os.getenv('WP_STAGING_USERNAME', '')
WP_APP_PASS  = os.getenv('WP_STAGING_APP_PASSWORD', '')

STAGING_HOST = urlparse(STAGING_URL).netloc
LIVE_HOST    = 'www.companydebt.com'

PROBLEMS_CSV  = 'internal_links_problems.csv'
DECISIONS_CSV = 'links_404_needs_decision.csv'

DRY_RUN = '--apply' not in sys.argv


def api_session():
    s = requests.Session()
    s.auth = (BA_USER, BA_PASS)
    s.headers['User-Agent'] = 'CompanyDebt-LinkFix/1.0'
    return s


def wp_login(session):
    login_url = f'{STAGING_URL}/wp-login.php'
    session.get(login_url, params={'wpe-login': 'true'})
    session.post(login_url, params={'wpe-login': 'true'}, data={
        'log': WP_USER, 'pwd': WP_APP_PASS,
        'wp-submit': 'Log In', 'testcookie': '1',
    }, allow_redirects=True)


def get_nonce(session):
    r = session.get(f'{STAGING_URL}/wp-admin/', timeout=30)
    for pattern in (r'wpApiSettings[^}]+"nonce":"([a-f0-9]+)"', r'"nonce":"([a-f0-9]+)"'):
        m = re.search(pattern, r.text)
        if m:
            return m.group(1)
    raise RuntimeError('Could not extract WP nonce')


def get_raw_content(session, post_type, post_id, nonce):
    r = session.get(
        f'{STAGING_URL}/wp-json/wp/v2/{post_type}/{post_id}',
        params={'context': 'edit', '_fields': 'id,slug,content'},
        headers={'X-WP-Nonce': nonce},
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    return data.get('content', {}).get('raw', '')


def patch_content(session, post_type, post_id, raw_content, nonce):
    r = session.post(
        f'{STAGING_URL}/wp-json/wp/v2/{post_type}/{post_id}',
        json={'content': raw_content},
        headers={'X-WP-Nonce': nonce, 'Content-Type': 'application/json'},
        timeout=30,
    )
    r.raise_for_status()
    return r.status_code


def normalise_redirect_to_live(location):
    """Convert a staging redirect Location to a live URL for storage in content."""
    parsed = urlparse(location)
    if parsed.netloc == STAGING_HOST:
        parsed = parsed._replace(netloc=LIVE_HOST, scheme='https')
    return urlunparse(parsed)


def type_to_endpoint(source_type):
    return 'posts' if source_type == 'post' else 'pages'


def main():
    if DRY_RUN:
        print('DRY RUN — no changes will be written. Pass --apply to write.\n')

    with open(PROBLEMS_CSV, encoding='utf-8', newline='') as f:
        problems = list(csv.DictReader(f))

    # Group by source post (to batch content edits per page)
    by_source = defaultdict(list)
    for row in problems:
        by_source[(row['source_id'], row['source_slug'], row['source_type'])].append(row)

    redirects_to_fix = []
    needs_decision   = []

    for row in problems:
        code = int(row['target_status'] or 0)
        if code in (301, 302):
            redirects_to_fix.append(row)
        elif code in (404, 410):
            needs_decision.append(row)
        # code 0 (error) or 200 (shouldn't be here) — skip silently

    print(f'Problems loaded: {len(problems)} rows')
    print(f'  Redirects (301/302): {len(redirects_to_fix)} — will auto-fix')
    print(f'  Broken (404/410):    {len(needs_decision)} — flagged for manual review')
    print()

    # Write 404/410 decisions file
    if needs_decision:
        with open(DECISIONS_CSV, 'w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, fieldnames=[
                'source_id', 'source_slug', 'source_type', 'source_url',
                'target_url', 'target_status', 'redirect_to', 'anchor'])
            w.writeheader()
            for row in needs_decision:
                w.writerow(row)
        print(f'Flagged {len(needs_decision)} broken links -> {DECISIONS_CSV}\n')

    if not redirects_to_fix:
        print('No redirect links to fix.')
        return

    # Group redirect fixes by source post
    fixes_by_source = defaultdict(list)
    for row in redirects_to_fix:
        key = (row['source_id'], row['source_slug'], row['source_type'])
        fixes_by_source[key].append(row)

    session = api_session()
    nonce = None
    if not DRY_RUN:
        print('Logging in to staging...')
        wp_login(session)
        nonce = get_nonce(session)
        print(f'  nonce: {nonce[:8]}...\n')

    total_fixed = 0
    total_pages = 0

    for (source_id, source_slug, source_type), rows in sorted(fixes_by_source.items()):
        endpoint = type_to_endpoint(source_type)
        print(f'[{source_slug}] — {len(rows)} redirect(s) to fix')

        if not DRY_RUN:
            raw = get_raw_content(session, endpoint, source_id, nonce)
            modified = raw
        else:
            raw = None
            modified = None

        changed = False
        for row in rows:
            old_href = row['target_url']
            new_href = row['redirect_to']
            if not new_href:
                print(f'  SKIP (no redirect_to): {old_href}')
                continue
            # Don't auto-fix if redirect leads to a media file
            MEDIA_EXTS = ('.jpg', '.jpeg', '.png', '.gif', '.pdf', '.svg', '.webp')
            if any(new_href.lower().rstrip('/').endswith(ext) for ext in MEDIA_EXTS):
                print(f'  SKIP (redirect points to media file): {old_href} -> {new_href}')
                needs_decision.append(row)
                continue
            # Convert staging destination back to live URL for content storage
            if STAGING_HOST in new_href:
                new_href = normalise_redirect_to_live(new_href)
            print(f'  {old_href}')
            print(f'    → {new_href}')
            print(f'    anchor: "{row["anchor"]}"')
            if not DRY_RUN:
                count_before = modified.count(f'href="{old_href}"') + modified.count(f"href='{old_href}'")
                modified = modified.replace(f'href="{old_href}"', f'href="{new_href}"')
                modified = modified.replace(f"href='{old_href}'", f"href='{new_href}'")
                count_after = modified.count(f'href="{new_href}"') + modified.count(f"href='{new_href}'")
                if count_before > 0:
                    changed = True
                    total_fixed += 1

        if not DRY_RUN and changed:
            if modified != raw:
                status = patch_content(session, endpoint, source_id, modified, nonce)
                print(f'  PATCHED (HTTP {status})')
                total_pages += 1
            else:
                print(f'  No change (href not found in raw content)')
        print()

    if DRY_RUN:
        print(f'Dry run complete. {len(redirects_to_fix)} redirect fixes proposed across {len(fixes_by_source)} pages.')
        print('Run with --apply to write changes to staging.')
    else:
        print(f'Fixed {total_fixed} redirect links across {total_pages} pages.')


if __name__ == '__main__':
    main()
