"""
Remove an injected hub-spoke block from a staging page.

Usage:
  python scripts/remove_hub_block.py --page /liquidation/           # dry run
  python scripts/remove_hub_block.py --page /liquidation/ --apply   # write to staging
"""
import os, re, sys, json, argparse
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

BLOCK_SENTINEL = '\n\n<!-- wp:heading {"level":3} -->\n<h3 class="wp-block-heading">'


def api_session():
    s = requests.Session()
    s.auth = (BA_USER, BA_PASS)
    s.headers['User-Agent'] = 'CompanyDebt-HubLinker/1.0'
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



def patch_content(session, endpoint, post_id, raw_content, nonce):
    r = session.post(
        f'{STAGING_URL}/wp-json/wp/v2/{endpoint}/{post_id}',
        json={'content': raw_content},
        headers={'X-WP-Nonce': nonce, 'Content-Type': 'application/json'},
        timeout=30,
    )
    r.raise_for_status()
    return r.status_code


def strip_block(raw, label):
    """Remove the first hub-spoke block with the given heading label."""
    sentinel = BLOCK_SENTINEL + label
    idx = raw.find(sentinel)
    if idx == -1:
        return None, raw  # nothing to remove
    return raw[idx:], raw[:idx]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--page', required=True, help='Hub path, e.g. /liquidation/')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()

    path = args.page
    if not path.endswith('/'):
        path += '/'

    with open(CACHE_FILE, encoding='utf-8') as f:
        cache = json.load(f)

    if path not in cache:
        print(f'ERROR: {path} not in cache')
        sys.exit(1)

    meta = cache[path]
    post_id  = meta['id']
    endpoint = meta['endpoint']

    session = api_session()

    # Use cached raw as source (same pattern as link_hubs_to_spokes.py)
    live_raw = meta['raw']

    if args.apply:
        print('Logging in...')
        wp_login(session)
        nonce = get_nonce(session)
        print(f'  nonce: {nonce[:8]}...\n')

    # The appended hub-spoke block starts at the last occurrence of the heading sentinel
    # and runs to the very end of the raw content. Split on the last sentinel.
    sentinel_re = re.compile(
        r'\n\n<!-- wp:heading \{"level":3\} -->\n'
        r'<h3 class="wp-block-heading">([^<]+)</h3>\n'
        r'<!-- /wp:heading -->\n\n'
        r'<!-- wp:paragraph -->\n<p>'
    )
    matches = list(sentinel_re.finditer(live_raw))
    if not matches:
        print(f'No hub-spoke block found on {path}')
        sys.exit(0)

    # Take the last match — that is the appended block
    last = matches[-1]
    label = last.group(1)
    removed_block = live_raw[last.start():]
    cleaned = live_raw[:last.start()]

    print(f'Page:    {path}  (ID {post_id})')
    print(f'Block:   "{label}"')
    print(f'Removed: {len(removed_block)} chars')
    print(f'Clean length: {len(cleaned)} chars')
    print(f'Clean tail (120 chars): ...{repr(cleaned[-120:])}')

    if not args.apply:
        print('\nDRY RUN — re-run with --apply to write to staging.')
        return

    status = patch_content(session, endpoint, post_id, cleaned, nonce)
    print(f'\nPatched staging (HTTP {status})')

    # Update cache
    cache[path]['raw'] = cleaned
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)
    print('Cache updated.')


if __name__ == '__main__':
    main()
