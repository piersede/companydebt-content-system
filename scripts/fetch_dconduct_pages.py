"""
One-off: fetch the two director-conduct-report pages from staging for comparison.
Dumps raw + rendered content and key metadata to dconduct_pages.json.
"""
import os, re, json, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

STAGING_URL = os.getenv('WP_STAGING_URL', '').rstrip('/')
BA_USER     = os.getenv('WP_BASIC_AUTH_USER', '')
BA_PASS     = os.getenv('WP_BASIC_AUTH_PASS', '')
WP_USER     = os.getenv('WP_STAGING_USERNAME', '')
WP_APP_PASS = os.getenv('WP_STAGING_APP_PASSWORD', '')

PAGE_IDS = [79396, 78129]


def api_session():
    s = requests.Session()
    s.auth = (BA_USER, BA_PASS)
    s.headers['User-Agent'] = 'CompanyDebt-Compare/1.0'
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


def fetch_page(session, nonce, page_id):
    r = session.get(
        f'{STAGING_URL}/wp-json/wp/v2/pages/{page_id}',
        params={'context': 'edit'},
        headers={'X-WP-Nonce': nonce},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def main():
    session = api_session()
    print('Logging in to staging...')
    wp_login(session)
    nonce = get_nonce(session)
    print(f'  nonce: {nonce[:8]}...\n')

    out = {}
    for pid in PAGE_IDS:
        data = fetch_page(session, nonce, pid)
        rendered = data.get('content', {}).get('rendered', '')
        raw = data.get('content', {}).get('raw', '')
        words = len(re.sub(r'<[^>]+>', ' ', rendered).split())
        out[pid] = {
            'id': pid,
            'slug': data.get('slug'),
            'status': data.get('status'),
            'link': data.get('link'),
            'title': data.get('title', {}).get('rendered', ''),
            'date': data.get('date'),
            'modified': data.get('modified'),
            'word_count': words,
            'excerpt': data.get('excerpt', {}).get('rendered', ''),
            'parent': data.get('parent'),
            'menu_order': data.get('menu_order'),
            'template': data.get('template'),
            'meta': data.get('meta', {}),
            'yoast_head_json': data.get('yoast_head_json', {}),
            'content_raw': raw,
            'content_rendered': rendered,
        }
        print(f'  {pid}: {data.get("slug")} — {words} words, status={data.get("status")}')

    with open('dconduct_pages.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print('\nWrote dconduct_pages.json')


if __name__ == '__main__':
    main()
