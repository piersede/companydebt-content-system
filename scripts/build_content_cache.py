"""
Fetch raw content for all pages/posts in staging_page_inventory.json
and save to content_cache.json for use by link-gap scripts.

Usage:
  python scripts/build_content_cache.py
"""
import os, re, sys, json, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

STAGING_URL = os.getenv('WP_STAGING_URL', '').rstrip('/')
BA_USER     = os.getenv('WP_BASIC_AUTH_USER', '')
BA_PASS     = os.getenv('WP_BASIC_AUTH_PASS', '')
WP_USER     = os.getenv('WP_STAGING_USERNAME', '')
WP_APP_PASS = os.getenv('WP_STAGING_APP_PASSWORD', '')
CACHE_FILE  = 'content_cache.json'


def api_session():
    s = requests.Session()
    s.auth = (BA_USER, BA_PASS)
    s.headers['User-Agent'] = 'CompanyDebt-CacheBuilder/1.0'
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
    m = re.search(r'wpApiSettings[^}]+"nonce":"([a-f0-9]+)"', r.text)
    if m:
        return m.group(1)
    raise RuntimeError('Could not extract nonce')


def main():
    with open('staging_page_inventory.json', encoding='utf-8') as f:
        inv = json.load(f)

    session = api_session()
    print('Logging in...')
    wp_login(session)
    nonce = get_nonce(session)
    print(f'  nonce: {nonce[:8]}...')
    print(f'  fetching {len(inv)} pages...\n')

    cache = {}
    errors = []
    for i, (path, meta) in enumerate(inv.items(), 1):
        post_id  = meta['id']
        slug     = meta['slug']
        endpoint = 'posts' if meta['type'] == 'post' else 'pages'
        try:
            r = session.get(
                f'{STAGING_URL}/wp-json/wp/v2/{endpoint}/{post_id}',
                params={'context': 'edit', '_fields': 'id,slug,content'},
                headers={'X-WP-Nonce': nonce},
                timeout=30,
            )
            r.raise_for_status()
            raw = r.json().get('content', {}).get('raw', '')
            cache[path] = {
                'id':       post_id,
                'slug':     slug,
                'type':     meta['type'],
                'endpoint': endpoint,
                'raw':      raw,
            }
            if i % 50 == 0:
                print(f'  {i}/{len(inv)} fetched...')
        except Exception as e:
            errors.append((path, str(e)))
            print(f'  ERROR [{slug}]: {e}')

    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False)

    print(f'\nCached {len(cache)} pages to {CACHE_FILE}')
    if errors:
        print(f'Errors ({len(errors)}):')
        for path, err in errors:
            print(f'  {path}: {err}')


if __name__ == '__main__':
    main()
