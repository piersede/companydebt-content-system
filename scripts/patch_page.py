"""
Patch a single staging page/post's content from a local file.
Used by the editorial internal-link pass: edit the raw content locally, then push.

Usage:
  python scripts/patch_page.py <page_id> <content_file> [post|page]

Credentials read from .env only.
"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')


def env(key):
    v = os.getenv(key)
    if not v:
        sys.exit(f'Missing required .env key: {key}')
    return v

STAGING_URL = env('WP_STAGING_URL').rstrip('/')
BA_USER     = env('WP_BASIC_AUTH_USER')
BA_PASS     = env('WP_BASIC_AUTH_PASS')
WP_USER     = env('WP_STAGING_USERNAME')
WP_APP_PASS = env('WP_STAGING_APP_PASSWORD')


def main():
    if len(sys.argv) < 3:
        sys.exit('Usage: python scripts/patch_page.py <page_id> <content_file> [post|page]')
    page_id      = sys.argv[1]
    content_file = sys.argv[2]
    post_type    = sys.argv[3] if len(sys.argv) > 3 else 'page'
    endpoint     = 'posts' if post_type == 'post' else 'pages'

    with open(content_file, encoding='utf-8') as f:
        content = f.read()

    s = requests.Session()
    s.auth = (BA_USER, BA_PASS)
    s.headers['User-Agent'] = 'CompanyDebt-PatchPage/1.0'

    login_url = f'{STAGING_URL}/wp-login.php'
    s.get(login_url, params={'wpe-login': 'true'})
    s.post(login_url, params={'wpe-login': 'true'}, data={
        'log': WP_USER, 'pwd': WP_APP_PASS,
        'wp-submit': 'Log In', 'testcookie': '1',
    }, allow_redirects=True)
    r = s.get(f'{STAGING_URL}/wp-admin/', timeout=30)
    nonce = None
    for pat in (r'wpApiSettings[^}]+"nonce":"([a-f0-9]+)"', r'"nonce":"([a-f0-9]+)"'):
        m = re.search(pat, r.text)
        if m:
            nonce = m.group(1)
            break
    if not nonce:
        sys.exit('Could not extract WP nonce')

    resp = s.post(f'{STAGING_URL}/wp-json/wp/v2/{endpoint}/{page_id}',
                  json={'content': content},
                  headers={'X-WP-Nonce': nonce, 'Content-Type': 'application/json'},
                  timeout=30)
    resp.raise_for_status()
    print(f'Patched {endpoint}/{page_id} (HTTP {resp.status_code}) from {content_file}')


if __name__ == '__main__':
    main()
