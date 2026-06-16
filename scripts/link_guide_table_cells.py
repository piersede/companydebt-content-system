"""
Link unlinked "Related guide" table cells across staging pages.

Finds <td>XYZ guide</td> cells (no <a> tag) and wraps them with the correct href.

Usage:
  python scripts/link_guide_table_cells.py            # dry run
  python scripts/link_guide_table_cells.py --apply    # write to staging WP
"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

STAGING_URL = os.getenv('WP_STAGING_URL', '').rstrip('/')
BA_USER     = os.getenv('WP_BASIC_AUTH_USER', '')
BA_PASS     = os.getenv('WP_BASIC_AUTH_PASS', '')
WP_USER     = os.getenv('WP_STAGING_USERNAME', '')
WP_APP_PASS = os.getenv('WP_STAGING_APP_PASSWORD', '')

DRY_RUN = '--apply' not in sys.argv

# Guide cell text → staging-relative target URL
GUIDE_REMAP = {
    'CVL guide':                    '/liquidation/creditors-voluntary-liquidation/',
    'Compulsory liquidation guide': '/liquidation/compulsory-liquidation/',
    'Compulsory guide':             '/liquidation/compulsory-liquidation/',
    'MVL guide':                    '/liquidation/members-voluntary-liquidation/',
    'Administration guide':         '/company-administration/',
    'CVA guide':                    '/company-rescue-solutions/company-voluntary-arrangement/',
    'Strike-off guide':             '/liquidation/company-strike-off-and-dissolution/',
    'Pre-pack guide':               '/company-rescue-solutions/pre-packs/',
    'Creditor pressure guide':      '/debt-creditor-pressure-hub/',
    'Time to Pay guide':            '/hmrc/time-to-pay-hmrc/',
}

# Plain <td> cell containing a guide label (no existing <a> tag)
GUIDE_TD = re.compile(r'<td>([^<]{3,60} guide[^<]{0,30})</td>', re.IGNORECASE)

# Pages confirmed to have unlinked guide cells
TARGET_PAGES = [
    (78129, 'closing-a-limited-company',   'pages'),
    (79396, 'company-administration',       'pages'),
    # creditor-negotiations — check via scan; ID unknown from previous session
    # creditors-voluntary-liquidation — likewise
    # dealing-with-creditor-pressure — likewise
    # liquidation — likewise
]

# We'll scan all pages listed in staging_page_inventory.json rather than hard-coding IDs,
# so even the ones without confirmed IDs get covered.


def api_session():
    s = requests.Session()
    s.auth = (BA_USER, BA_PASS)
    s.headers['User-Agent'] = 'CompanyDebt-GuideLinker/1.0'
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
    raise RuntimeError('Could not extract WP nonce from wpApiSettings')


def get_raw(session, endpoint, post_id, nonce):
    r = session.get(
        f'{STAGING_URL}/wp-json/wp/v2/{endpoint}/{post_id}',
        params={'context': 'edit', '_fields': 'id,slug,content'},
        headers={'X-WP-Nonce': nonce},
        timeout=30,
    )
    r.raise_for_status()
    return r.json().get('content', {}).get('raw', '')


def patch_raw(session, endpoint, post_id, raw_content, nonce):
    r = session.post(
        f'{STAGING_URL}/wp-json/wp/v2/{endpoint}/{post_id}',
        json={'content': raw_content},
        headers={'X-WP-Nonce': nonce, 'Content-Type': 'application/json'},
        timeout=30,
    )
    r.raise_for_status()
    return r.status_code


def apply_guide_links(raw: str):
    """Replace unlinked guide cells with linked versions. Returns (new_raw, count)."""
    changed = 0

    def replacer(m):
        nonlocal changed
        text = m.group(1)
        if text in GUIDE_REMAP:
            changed += 1
            href = GUIDE_REMAP[text]
            return f'<td><a href="{href}">{text}</a></td>'
        # Guide text not in our map — leave untouched
        return m.group(0)

    new_raw = GUIDE_TD.sub(replacer, raw)
    return new_raw, changed


def load_inventory():
    import json
    with open('staging_page_inventory.json', encoding='utf-8') as f:
        inv = json.load(f)
    # Returns list of (id, slug, type) for all pages
    entries = []
    for path, meta in inv.items():
        entries.append((meta['id'], meta['slug'], meta['type']))
    return entries


def main():
    if DRY_RUN:
        print('DRY RUN — no changes written. Pass --apply to write.\n')

    session = api_session()
    nonce = None
    if not DRY_RUN:
        print('Logging in to staging...')
        wp_login(session)
        nonce = get_nonce(session)
        print(f'  nonce: {nonce[:8]}...\n')
    else:
        # Dry run still needs nonce to fetch raw content for preview
        wp_login(session)
        nonce = get_nonce(session)
        print(f'  nonce (read-only): {nonce[:8]}...\n')

    inventory = load_inventory()

    total_cells = 0
    total_pages = 0

    for (post_id, slug, post_type) in sorted(inventory, key=lambda x: x[1]):
        endpoint = 'posts' if post_type == 'post' else 'pages'
        try:
            raw = get_raw(session, endpoint, post_id, nonce)
        except Exception as e:
            print(f'[{slug}] SKIP — {e}')
            continue

        if not raw:
            continue

        # Quick pre-check: does this page have any guide cells at all?
        if not GUIDE_TD.search(raw):
            continue

        new_raw, count = apply_guide_links(raw)

        if count == 0:
            # All guide cells in this page had unknown labels
            matches = GUIDE_TD.findall(raw)
            print(f'[{slug}] {len(matches)} guide cell(s) found but none in REMAP:')
            for m in matches:
                print(f'    "{m}"')
            continue

        total_cells += count
        total_pages += 1

        print(f'[{slug}] {count} cell(s) to link')
        # Show what will change
        for m in GUIDE_TD.finditer(raw):
            text = m.group(1)
            if text in GUIDE_REMAP:
                print(f'    "{text}" → {GUIDE_REMAP[text]}')

        if not DRY_RUN:
            status = patch_raw(session, endpoint, post_id, new_raw, nonce)
            print(f'    -> patched (HTTP {status})')

    print(f'\nDone. {total_cells} cell(s) across {total_pages} page(s).')
    if DRY_RUN:
        print('Re-run with --apply to write changes.')


if __name__ == '__main__':
    main()
