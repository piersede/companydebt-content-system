"""
For each cluster hub page, find sub-pages not already linked from it
and append a Gutenberg 'In this section' block covering the gaps.

This gives each orphaned sub-page +1 inbound link from its own hub —
the most editorially natural internal link a sub-page can have.

Usage:
  python scripts/link_hubs_to_spokes.py            # dry run
  python scripts/link_hubs_to_spokes.py --apply    # write to staging
"""
import os, re, sys, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

STAGING_URL = os.getenv('WP_STAGING_URL', '').rstrip('/')
BA_USER     = os.getenv('WP_BASIC_AUTH_USER', '')
BA_PASS     = os.getenv('WP_BASIC_AUTH_PASS', '')
WP_USER     = os.getenv('WP_STAGING_USERNAME', '')
WP_APP_PASS = os.getenv('WP_STAGING_APP_PASSWORD', '')

DRY_RUN    = '--apply' not in sys.argv
CACHE_FILE  = 'content_cache.json'
ANCHOR_XLSX = r'C:\Users\piers\Downloads\companydebt_current_site_url_anchor_banks.xlsx'

# Load anchor bank: path → first anchor option (best display text)
def load_anchor_labels():
    df = pd.read_excel(ANCHOR_XLSX, sheet_name='URL Anchors')
    df.columns = ['url', 'anchors']
    labels = {}
    for _, row in df.iterrows():
        url = str(row['url']).strip()
        url = re.sub(r'^https?://(?:www\.)?companydebt\.com', '', url)
        if not url.startswith('/'): url = '/' + url
        if not url.endswith('/'): url += '/'
        anchors = [a.strip() for a in str(row['anchors']).split(',') if a.strip()]
        if anchors and 'no routine' not in anchors[0].lower():
            labels[url] = anchors[0]
    return labels

ANCHOR_LABELS = load_anchor_labels()

# Cluster hub path → display label for the "In this section" heading
HUBS = {
    '/hmrc/':                           'HMRC guides in this section',
    '/advice/':                         'Director advice guides',
    '/company-cash-flow-problems/':     'Cash flow problem guides',
    '/company-administration/':         'Company administration guides',
    '/bounce-back-loan-support-hub/':   'Bounce Back Loan guides',
    '/insolvency/':                     'Insolvency guides',
    '/sample-letters/':                 'Sample letter templates',
    '/company-rescue-solutions/company-voluntary-arrangement/':
                                        'CVA guides in this section',
    '/company-rescue-solutions/':       'Company rescue guides',
    '/liquidation/':                    'Liquidation guides',
    '/sector-specific-insolvency/':     'Sector insolvency guides',
    '/winding-up-petitions/':           'Winding up petition guides',
    '/liquidation/company-strike-off-and-dissolution/':
                                        'Strike-off and dissolution guides',
    '/company-rescue-solutions/pre-packs/':
                                        'Pre-pack administration guides',
}

# Pages to skip as spoke targets
SKIP_PATHS = {
    '/site-map/', '/meet-the-team/', '/about-us/', '/contact-us/',
    '/terms-conditions/', '/privacy-policy/', '/accessibility/',
    '/express-liquidation/', '/stressed-directors-guide/',
}

# Anchor text: derive from slug (title-case words, strip common suffixes)
def slug_to_anchor(path):
    slug = path.strip('/').split('/')[-1]
    words = slug.replace('-', ' ')
    return words.capitalize()


def build_gutenberg_block(label, links):
    """
    Build a Gutenberg paragraph block with comma-separated linked items,
    preceded by a heading.
    """
    items = ', '.join(f'<a href="{path}">{anchor}</a>' for path, anchor in links)
    block = (
        '\n\n<!-- wp:heading {"level":3} -->\n'
        f'<h3 class="wp-block-heading">{label}</h3>\n'
        '<!-- /wp:heading -->\n\n'
        '<!-- wp:paragraph -->\n'
        f'<p>{items}</p>\n'
        '<!-- /wp:paragraph -->'
    )
    return block


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


def main():
    if DRY_RUN:
        print('DRY RUN — pass --apply to write.\n')

    with open(CACHE_FILE, encoding='utf-8') as f:
        cache = json.load(f)

    all_paths = set(cache.keys())

    session = api_session()
    nonce = None
    if not DRY_RUN:
        print('Logging in...')
        wp_login(session)
        nonce = get_nonce(session)
        print(f'  nonce: {nonce[:8]}...\n')

    total_links = 0
    total_hubs  = 0

    # Process deepest hubs first (longer prefix wins for sub-sub-pages)
    for hub_path, label in sorted(HUBS.items(), key=lambda x: -len(x[0])):
        if hub_path not in cache:
            print(f'[SKIP] {hub_path} — not in cache')
            continue

        hub_meta = cache[hub_path]
        hub_raw  = hub_meta['raw']
        if not hub_raw:
            print(f'[SKIP] {hub_path} — empty raw content')
            continue

        # Find direct children only (one path segment deeper)
        hub_depth = hub_path.count('/')
        spokes = [
            p for p in all_paths
            if p.startswith(hub_path)
            and p != hub_path
            and p.count('/') == hub_depth + 1  # direct children only
            and p not in SKIP_PATHS
        ]

        # Filter to spokes not already linked in hub raw
        missing = []
        for spoke_path in sorted(spokes):
            if spoke_path not in hub_raw:
                # Use anchor bank label if available, else derive from slug
                anchor = ANCHOR_LABELS.get(spoke_path) or slug_to_anchor(spoke_path)
                missing.append((spoke_path, anchor))

        if not missing:
            print(f'[OK]   {hub_path} — all {len(spokes)} spokes already linked')
            continue

        print(f'\n[HUB]  {hub_path}')
        print(f'  Spokes total: {len(spokes)}  Missing: {len(missing)}')
        for path, anchor in missing:
            print(f'    + {path}  "{anchor}"')

        block = build_gutenberg_block(label, missing)
        new_raw = hub_raw + block

        total_links += len(missing)
        total_hubs  += 1

        if not DRY_RUN:
            endpoint = hub_meta['endpoint']
            post_id  = hub_meta['id']
            status = patch_content(session, endpoint, post_id, new_raw, nonce)
            print(f'  -> patched ({len(missing)} links, HTTP {status})')

    print(f'\n{"="*60}')
    print(f'Hub pages to update: {total_hubs}')
    print(f'Links to add:        {total_links}')
    if DRY_RUN:
        print('\nRe-run with --apply to write.')


if __name__ == '__main__':
    main()
