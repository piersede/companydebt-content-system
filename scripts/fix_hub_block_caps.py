"""
Two fixes in one pass:

1. Capitalise first letter of every anchor text in hub 'In this section' blocks
   (added by link_hubs_to_spokes.py — they used anchor-bank text verbatim which
   is often lowercase; in a list context the first letter should be uppercase).

2. Fix two missing-apostrophe anchor texts site-wide:
   "when employers cant afford redundancy payments"
   "whats the risk of being disqualified as a director"

Usage:
  python scripts/fix_hub_block_caps.py            # dry run
  python scripts/fix_hub_block_caps.py --apply    # write to staging
"""
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

STAGING_URL = os.getenv('WP_STAGING_URL', '').rstrip('/')
BA_USER     = os.getenv('WP_BASIC_AUTH_USER', '')
BA_PASS     = os.getenv('WP_BASIC_AUTH_PASS', '')
WP_USER     = os.getenv('WP_STAGING_USERNAME', '')
WP_APP_PASS = os.getenv('WP_STAGING_APP_PASSWORD', '')

DRY_RUN    = '--apply' not in sys.argv
CACHE_FILE = 'content_cache.json'

# Hub heading labels (match the strings written by link_hubs_to_spokes.py)
HUB_LABELS = {
    'HMRC guides in this section',
    'Director advice guides',
    'Cash flow problem guides',
    'Company administration guides',
    'Bounce Back Loan guides',
    'Insolvency guides',
    'Sample letter templates',
    'CVA guides in this section',
    'Company rescue guides',
    'Liquidation guides',
    'Sector insolvency guides',
    'Winding up petition guides',
    'Strike-off and dissolution guides',
    'Pre-pack administration guides',
}

# Build pattern that matches any hub block:
#   <!-- wp:heading ... --><h3 ...>LABEL</h3><!-- /wp:heading -->
#   <!-- wp:paragraph --><p>LINKS</p><!-- /wp:paragraph -->
labels_re = '|'.join(re.escape(l) for l in HUB_LABELS)
HUB_BLOCK_RE = re.compile(
    r'(<!-- wp:heading[^>]*-->\s*<h3[^>]*>(?:' + labels_re + r')</h3>\s*<!-- /wp:heading -->'
    r'\s*<!-- wp:paragraph -->\s*<p>)(.*?)(</p>\s*<!-- /wp:paragraph -->)',
    re.DOTALL | re.IGNORECASE,
)

# Global apostrophe fixes (slug-derived text, no apostrophe)
APOS_FIXES = {
    'when employers cant afford redundancy payments':
        "when employers can't afford redundancy payments",
    'whats the risk of being disqualified as a director':
        "what's the risk of being disqualified as a director",
}

LINK_RE = re.compile(r'(<a\s[^>]*>)(.*?)(</a>)', re.DOTALL | re.IGNORECASE)


def clean_anchor(text):
    """
    Apply all quality fixes to anchor display text (after initial capitalisation):
      - standalone lowercase 'i' → 'I'
      - missing apostrophes: whats, cant, dont, wont, havent, isnt, etc.
      - 'Hmrcs' → "HMRC's"
      - leading 'Vs ' → 'vs ' (more natural in list context)
    """
    # Leading "Vs " → "vs "
    text = re.sub(r'^Vs\s', 'vs ', text)
    # Standalone "i" pronoun → "I"
    text = re.sub(r'(?<!\w)i(?!\w)', 'I', text)
    # Missing apostrophes (case-insensitive, preserve case of rest)
    contractions = [
        (r'\bWhats\b', "What's"), (r'\bwhats\b', "what's"),
        (r'\bCant\b',  "Can't"),  (r'\bcant\b',  "can't"),
        (r'\bDont\b',  "Don't"),  (r'\bdont\b',  "don't"),
        (r'\bWont\b',  "Won't"),  (r'\bwont\b',  "won't"),
        (r'\bIsnt\b',  "Isn't"),  (r'\bisnt\b',  "isn't"),
        (r'\bHavent\b',"Haven't"),(r'\bhavent\b', "haven't"),
        (r'\bThats\b', "That's"), (r'\bthats\b',  "that's"),
    ]
    for pattern, replacement in contractions:
        text = re.sub(pattern, replacement, text)
    # "Hmrcs" → "HMRC's"
    text = re.sub(r'\bHmrcs\b', "HMRC's", text)
    text = re.sub(r'\bhmrcs\b', "HMRC's", text)
    return text


def fix_hub_block_links(paragraph_html):
    """Capitalise + clean each anchor text inside a hub block paragraph."""
    changes = []

    def replacer(m):
        open_tag, inner, close_tag = m.group(1), m.group(2), m.group(3)
        stripped = re.sub(r'<[^>]+>', '', inner).strip()
        if not stripped:
            return m.group(0)
        # Capitalise first letter
        new_text = stripped[0].upper() + stripped[1:] if stripped[0].islower() else stripped
        # Apply secondary quality fixes
        new_text = clean_anchor(new_text)
        if new_text != stripped:
            changes.append((stripped, new_text))
            return open_tag + new_text + close_tag
        return m.group(0)

    new_html = LINK_RE.sub(replacer, paragraph_html)
    return new_html, changes


def apply_fixes(raw):
    """Return (new_raw, list_of_change_descriptions)."""
    all_changes = []

    # 1. Hub block capitalisation + cleaning
    def block_replacer(m):
        prefix, para, suffix = m.group(1), m.group(2), m.group(3)
        new_para, changes = fix_hub_block_links(para)
        for old, new in changes:
            all_changes.append(f'  CAP  "{old}"  →  "{new}"')
        return prefix + new_para + suffix

    new_raw = HUB_BLOCK_RE.sub(block_replacer, raw)

    # 2. Global apostrophe fixes — also handles cases outside hub blocks
    def apos_replacer(m):
        open_tag, inner, close_tag = m.group(1), m.group(2), m.group(3)
        stripped = re.sub(r'<[^>]+>', '', inner).strip()
        if stripped in APOS_FIXES:
            new_text = APOS_FIXES[stripped]
            all_changes.append(f'  APOS "{stripped}"  →  "{new_text}"')
            return open_tag + new_text + close_tag
        return m.group(0)

    new_raw = LINK_RE.sub(apos_replacer, new_raw)

    return new_raw, all_changes


def api_session():
    s = requests.Session()
    s.auth = (BA_USER, BA_PASS)
    s.headers['User-Agent'] = 'CompanyDebt-HubCaps/1.0'
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

    session = api_session()
    nonce = None
    if not DRY_RUN:
        print('Logging in...')
        wp_login(session)
        nonce = get_nonce(session)
        print(f'  nonce: {nonce[:8]}...\n')

    total_pages   = 0
    total_changes = 0

    for path, meta in sorted(cache.items(), key=lambda x: x[1]['slug']):
        raw = meta.get('raw', '')
        if not raw:
            continue

        new_raw, changes = apply_fixes(raw)
        if not changes:
            continue

        total_pages   += 1
        total_changes += len(changes)
        print(f'\n[{meta["slug"]}]  ({len(changes)} change(s))')
        for c in changes:
            print(c)

        if not DRY_RUN:
            status = patch_content(session, meta['endpoint'], meta['id'], new_raw, nonce)
            print(f'  -> patched (HTTP {status})')

    print(f'\n{"="*60}')
    print(f'Pages to update: {total_pages}')
    print(f'Changes:         {total_changes}')
    if DRY_RUN:
        print('\nRe-run with --apply to write.')


if __name__ == '__main__':
    main()
