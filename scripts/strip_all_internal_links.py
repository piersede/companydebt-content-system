"""
Strip ALL editorial internal links from every published post and page on staging.
Removes <a> tags pointing to companydebt.com or relative paths, keeping anchor text.
External links (other domains) are untouched. Headers/footers/nav are not in content.

Usage:
  python scripts/strip_all_internal_links.py            # dry run
  python scripts/strip_all_internal_links.py --apply    # write to staging
"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

STAGING_URL = os.getenv('WP_STAGING_URL', '').rstrip('/')
BA_USER     = os.getenv('WP_BASIC_AUTH_USER', '')
BA_PASS     = os.getenv('WP_BASIC_AUTH_PASS', '')
WP_USER     = os.getenv('WP_STAGING_USERNAME', '')
WP_APP_PASS = os.getenv('WP_STAGING_APP_PASSWORD', '')

STAGING_HOST = urlparse(STAGING_URL).netloc
LIVE_HOST    = 'www.companydebt.com'

DRY_RUN = '--apply' not in sys.argv


def api_session():
    s = requests.Session()
    s.auth = (BA_USER, BA_PASS)
    s.headers['User-Agent'] = 'CompanyDebt-StripLinks/1.0'
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


def fetch_all(session, nonce):
    items = []
    for post_type in ('posts', 'pages'):
        page = 1
        while True:
            r = session.get(
                f'{STAGING_URL}/wp-json/wp/v2/{post_type}',
                params={'per_page': 100, 'page': page, 'status': 'publish',
                        'context': 'edit', '_fields': 'id,slug,type,content'},
                headers={'X-WP-Nonce': nonce},
                timeout=30,
            )
            if r.status_code == 400:
                break
            r.raise_for_status()
            batch = r.json()
            if not batch:
                break
            items.extend(batch)
            if len(batch) < 100:
                break
            page += 1
        count = sum(1 for i in items if i.get('type') == post_type.rstrip('s'))
        print(f'  {post_type}: {count} items')
    return items


def is_internal(href):
    """True if href points to companydebt.com or is a relative path."""
    if not href or href.startswith('#') or href.startswith('mailto:') or href.startswith('tel:'):
        return False
    parsed = urlparse(href)
    if parsed.netloc in (LIVE_HOST, STAGING_HOST, ''):
        return True
    return False


def strip_internal_links(raw):
    """Remove all internal <a> tags from raw Gutenberg content, keeping inner text."""
    def replacer(m):
        href = m.group(1) or m.group(2)  # double or single quoted
        if is_internal(href):
            return m.group(3)  # inner content only
        return m.group(0)  # leave external links untouched

    pattern = r'<a\s[^>]*href="([^"]*)"[^>]*>(.*?)</a>|<a\s[^>]*href=\'([^\']*)\'[^>]*>(.*?)</a>'

    def replacer(m):
        href = m.group(1) if m.group(1) is not None else m.group(3)
        inner = m.group(2) if m.group(2) is not None else m.group(4)
        if is_internal(href):
            return inner
        return m.group(0)

    return re.sub(pattern, replacer, raw, flags=re.DOTALL | re.IGNORECASE)


def patch_content(session, post_type, post_id, raw_content, nonce):
    r = session.post(
        f'{STAGING_URL}/wp-json/wp/v2/{post_type}/{post_id}',
        json={'content': raw_content},
        headers={'X-WP-Nonce': nonce, 'Content-Type': 'application/json'},
        timeout=30,
    )
    r.raise_for_status()
    return r.status_code


def main():
    if DRY_RUN:
        print('DRY RUN — no changes will be written. Pass --apply to write.\n')

    session = api_session()

    print('Logging in to staging...')
    wp_login(session)
    nonce = get_nonce(session)
    print(f'  nonce: {nonce[:8]}...\n')

    print('Fetching all published content...')
    items = fetch_all(session, nonce)
    print(f'Total: {len(items)} posts/pages\n')

    total_links = 0
    total_pages = 0

    for item in items:
        raw = item.get('content', {}).get('raw', '')
        if not raw:
            continue

        stripped = strip_internal_links(raw)

        # Count how many links were removed
        original_count = len(re.findall(r'<a\s', raw, re.IGNORECASE))
        new_count = len(re.findall(r'<a\s', stripped, re.IGNORECASE))
        removed = original_count - new_count

        if removed == 0:
            continue

        slug = item.get('slug', item.get('id'))
        post_type = item.get('type', 'page')
        endpoint = 'posts' if post_type == 'post' else 'pages'

        print(f'  [{slug}] — {removed} internal link(s) stripped')
        total_links += removed

        if not DRY_RUN:
            patch_content(session, endpoint, item['id'], stripped, nonce)
            total_pages += 1
        else:
            total_pages += 1

    print(f'\n{"Would strip" if DRY_RUN else "Stripped"} {total_links} internal links '
          f'across {total_pages} pages.')
    if DRY_RUN:
        print('Run with --apply to write changes.')


if __name__ == '__main__':
    main()
