"""
Strip all 404/broken internal links from staging WP content.
Removes the <a> tag but keeps the anchor text. Dry-run by default.

Usage:
  python scripts/strip_broken_links.py            # dry run
  python scripts/strip_broken_links.py --apply    # write to staging
"""
import os, csv, sys, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from collections import defaultdict

import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

STAGING_URL = os.getenv('WP_STAGING_URL', '').rstrip('/')
BA_USER     = os.getenv('WP_BASIC_AUTH_USER', '')
BA_PASS     = os.getenv('WP_BASIC_AUTH_PASS', '')
WP_USER     = os.getenv('WP_STAGING_USERNAME', '')
WP_APP_PASS = os.getenv('WP_STAGING_APP_PASSWORD', '')

PROBLEMS_CSV = 'internal_links_problems.csv'
DRY_RUN      = '--apply' not in sys.argv


def api_session():
    s = requests.Session()
    s.auth = (BA_USER, BA_PASS)
    s.headers['User-Agent'] = 'CompanyDebt-LinkStrip/1.0'
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
    return r.json().get('content', {}).get('raw', '')


def patch_content(session, post_type, post_id, raw_content, nonce):
    r = session.post(
        f'{STAGING_URL}/wp-json/wp/v2/{post_type}/{post_id}',
        json={'content': raw_content},
        headers={'X-WP-Nonce': nonce, 'Content-Type': 'application/json'},
        timeout=30,
    )
    r.raise_for_status()
    return r.status_code


def strip_link(content, href):
    """Remove <a href="...">...</a> wrapping the given href, leaving inner text."""
    # Match <a ...href="href"...>content</a> — handles attributes in any order
    # Escape special regex chars in href
    href_esc = re.escape(href)
    # Double-quoted href
    pattern = rf'<a\s[^>]*href="{href_esc}"[^>]*>(.*?)</a>'
    content, n1 = re.subn(pattern, r'\1', content, flags=re.DOTALL | re.IGNORECASE)
    # Single-quoted href
    pattern = rf"<a\s[^>]*href='{href_esc}'[^>]*>(.*?)</a>"
    content, n2 = re.subn(pattern, r'\1', content, flags=re.DOTALL | re.IGNORECASE)
    return content, n1 + n2


def type_to_endpoint(source_type):
    return 'posts' if source_type == 'post' else 'pages'


def main():
    if DRY_RUN:
        print('DRY RUN — no changes will be written. Pass --apply to write.\n')

    with open(PROBLEMS_CSV, encoding='utf-8', newline='') as f:
        problems = list(csv.DictReader(f))

    # Only handle broken links (404/410/0) — skip 301/302
    broken = [r for r in problems if int(r.get('target_status') or 0) not in (200, 301, 302)]
    print(f'Broken links to strip: {len(broken)} instances across '
          f'{len({r["source_id"] for r in broken})} pages\n')

    # Group by source page
    by_source = defaultdict(list)
    for row in broken:
        key = (row['source_id'], row['source_slug'], row['source_type'])
        by_source[key].append(row)

    session = api_session()
    nonce = None
    if not DRY_RUN:
        print('Logging in to staging...')
        wp_login(session)
        nonce = get_nonce(session)
        print(f'  nonce: {nonce[:8]}...\n')

    total_stripped = 0
    total_pages = 0

    for (source_id, source_slug, source_type), rows in sorted(by_source.items(), key=lambda x: x[0][1]):
        endpoint = type_to_endpoint(source_type)
        print(f'[{source_slug}] — {len(rows)} broken link(s) to strip')

        if not DRY_RUN:
            raw = get_raw_content(session, endpoint, source_id, nonce)
        else:
            raw = None

        # Deduplicate hrefs for this page (same target may appear multiple times)
        unique_hrefs = list(dict.fromkeys(r['target_url'] for r in rows))
        page_stripped = 0

        for href in unique_hrefs:
            anchor_examples = [r['anchor'] for r in rows if r['target_url'] == href]
            print(f'  STRIP: {href}')
            for a in anchor_examples[:2]:
                print(f'    text: "{a}"')

            if not DRY_RUN:
                raw, count = strip_link(raw, href)
                if count:
                    page_stripped += count
                    print(f'    removed {count} instance(s)')
                else:
                    print(f'    (not found in raw content)')

        if not DRY_RUN and page_stripped:
            status = patch_content(session, endpoint, source_id, raw, nonce)
            print(f'  PATCHED (HTTP {status}) — {page_stripped} link(s) stripped')
            total_stripped += page_stripped
            total_pages += 1
        print()

    if DRY_RUN:
        print(f'Dry run complete. Would strip links from {len(by_source)} pages.')
        print('Run with --apply to write changes.')
    else:
        print(f'Done. Stripped {total_stripped} broken links across {total_pages} pages.')


if __name__ == '__main__':
    main()
