"""
Push specific _all/ files to staging WP.
Run this before insert_internal_links.py to ensure staging is current.
"""
import os, re, sys, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

URL      = os.getenv('WP_STAGING_URL', '').rstrip('/')
BA_USER  = os.getenv('WP_BASIC_AUTH_USER', '')
BA_PASS  = os.getenv('WP_BASIC_AUTH_PASS', '')
WP_USER  = os.getenv('WP_STAGING_USERNAME', '')
WP_PASS  = os.getenv('WP_STAGING_APP_PASSWORD', '')

ALL_DIR  = Path('internal-links/_all')

# slug -> (post_id, endpoint)
PENDING = {
    'voluntary-vs-compulsory-liquidation': (77916,  'pages'),
    'charity-non-profit-insolvency':       (77218,  'pages'),
    'debt-creditor-pressure-hub':          (77146,  'pages'),
    'director-protection-hub':             (77396,  'pages'),
    'funding-options-for-smes-in-the-uk':  (68183,  'pages'),
    'home-2022':                           (55052,  'pages'),
    'cant-pay-paye':                       (8324,   'pages'),
    'cant-pay-vat':                        (9443,   'pages'),
    'corporation-tax-penalties':           (28761,  'pages'),
}


def extract_content(path: Path) -> str:
    lines = path.read_text(encoding='utf-8').splitlines(keepends=True)
    start = 0
    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith('<!--') and not s.startswith('<!-- wp:'):
            start = i + 1
        elif s == '' and start == i:
            start = i + 1
        else:
            break
    return ''.join(lines[start:]).strip()


def auth_session():
    s = requests.Session()
    s.auth = (BA_USER, BA_PASS)
    s.headers['User-Agent'] = 'CompanyDebt-PushPending/1.0'
    # Load cookies
    s.get(f'{URL}/wp-login.php', timeout=15)
    s.post(f'{URL}/wp-login.php',
           headers={'Referer': f'{URL}/wp-login.php', 'Origin': URL},
           data={'log': WP_USER, 'pwd': WP_PASS, 'wp-submit': 'Log In',
                 'redirect_to': f'{URL}/wp-admin/', 'testcookie': '1'},
           allow_redirects=True, timeout=30)
    # Get nonce
    admin = s.get(f'{URL}/wp-admin/', timeout=15)
    m = re.search(r'wpApiSettings[^}]+"nonce":"([a-f0-9]+)"', admin.text)
    if not m:
        sys.exit('Could not extract nonce — login may have failed')
    nonce = m.group(1)
    s.headers['X-WP-Nonce'] = nonce
    print(f'  nonce: {nonce[:8]}...')
    return s


def main():
    print('Logging in...')
    session = auth_session()

    pushed = 0
    for slug, (post_id, endpoint) in PENDING.items():
        src = ALL_DIR / f'{slug}.txt'
        if not src.exists():
            print(f'  [SKIP] {slug} — file not found')
            continue
        content = extract_content(src)
        r = session.post(
            f'{URL}/wp-json/wp/v2/{endpoint}/{post_id}',
            json={'content': content},
            headers={'Content-Type': 'application/json'},
            timeout=30,
        )
        if r.status_code in (200, 201):
            print(f'  [OK]   {slug} (HTTP {r.status_code})')
            pushed += 1
        else:
            print(f'  [ERR]  {slug} — HTTP {r.status_code}: {r.text[:120]}')
        time.sleep(0.2)

    print(f'\nDone. {pushed}/{len(PENDING)} pages pushed.')


if __name__ == '__main__':
    main()
