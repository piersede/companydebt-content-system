"""
Fix redundant / malformed anchor text in hub 'In this section' blocks.

Issues found:
  1. HMRC hub: anchors prefixed with "HMRC " making double-HMRC phrases
  2. Cash-flow hub: "cant" (missing apostrophe) throughout
  3. Other hubs: slug-derived fallback text that is awkward

Usage:
  python scripts/fix_hub_anchor_text.py            # dry run (shows diffs)
  python scripts/fix_hub_anchor_text.py --apply    # write to staging
"""
import os, re, sys, json
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

# ── Targeted replacements ─────────────────────────────────────────────────────
# Each entry: (exact_old_anchor_text, new_anchor_text)
# Applied only inside <a href="...">TEXT</a> patterns.

ANCHOR_FIXES = [
    # HMRC hub — redundant "HMRC" prefix (slug-derived with category prefix)
    ('HMRC pay hmrc or suppliers first',                    'Pay HMRC or suppliers first'),
    ('HMRC understanding hmrc debt collection',             'Understanding HMRC debt collection'),
    ('HMRC what happens if hmrc sends bailiffs to a business', 'What happens if HMRC sends bailiffs to a business'),
    ('HMRC what happens if you ignore hmrc letters',        'What happens if you ignore HMRC letters'),
    ('HMRC Time to Pay arrangement',                        'Time to Pay arrangement'),
    ('HMRC offices contact guide',                          'HMRC offices contact guide'),  # already fine — keep
    ('HMRC tax investigations',                             'HMRC tax investigations'),      # already fine — keep

    # Cash-flow hub — missing apostrophes in slug-derived text
    ("cant afford to pay suppliers what are the options",   "Can't afford to pay suppliers – what are the options"),
    ("cant afford to repay business loan",                  "Can't afford to repay business loan"),
    ("cant pay a commercial lease or rent",                 "Can't pay a commercial lease or rent"),
    ("cant pay staff wages",                                "Can't pay staff wages"),
    ("cant pay suppliers what are the options",             "Can't pay suppliers – what are the options"),
    # Generic catch for any remaining "cant " at start of anchor text (applied last)
    # Handled separately via regex below.

    # Bounce Back Loan hub — slug-derived fallbacks
    ('bounce back loan support hub',                        'Bounce Back Loan support hub'),

    # Insolvency hub
    ('business recovery services',                          'Business recovery services'),
    ('how to save a struggling business',                   'How to save a struggling business'),
    ('insolvent company investigations',                    'Insolvent company investigations'),
    ('rescue your business from insolvency',                'Rescue your business from insolvency'),

    # Liquidation hub
    ('closing a limited company',                           'Closing a limited company'),
    ('what is a pre pack administration',                   'What is a pre-pack administration'),

    # Sample letters hub — slug-derived
    ('sample letter template',                              'Sample letter template'),

    # Sector hub — slug-derived
    ('sector specific insolvency',                          'Sector-specific insolvency'),
]

# Build lookup for fast replacement (old → new)
_fix_map = {old: new for old, new in ANCHOR_FIXES if old != new}


def fix_anchor_text(raw: str) -> tuple[str, list[str]]:
    """
    Apply all anchor-text fixes to raw Gutenberg content.
    Returns (new_raw, list_of_changes).
    Only modifies text inside <a ...>TEXT</a> tags.
    """
    changes = []

    def replacer(m):
        full_open  = m.group(1)   # <a href="...">
        inner_text = m.group(2)   # anchor display text
        full_close = m.group(3)   # </a>

        # Direct lookup first
        if inner_text in _fix_map:
            new_text = _fix_map[inner_text]
            changes.append(f'  "{inner_text}"  →  "{new_text}"')
            return f'{full_open}{new_text}{full_close}'

        # Generic: fix "cant " at start (lowercase, no apostrophe)
        if re.match(r"^cant\s", inner_text):
            new_text = "Can't" + inner_text[4:]
            changes.append(f'  "{inner_text}"  →  "{new_text}"')
            return f'{full_open}{new_text}{full_close}'

        return m.group(0)

    pattern = re.compile(r'(<a\s[^>]*>)(.*?)(</a>)', re.DOTALL | re.IGNORECASE)
    new_raw = pattern.sub(replacer, raw)
    return new_raw, changes


def api_session():
    s = requests.Session()
    s.auth = (BA_USER, BA_PASS)
    s.headers['User-Agent'] = 'CompanyDebt-AnchorFixer/1.0'
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

    total_changes = 0
    total_pages   = 0

    for path, meta in sorted(cache.items()):
        raw = meta.get('raw', '')
        if not raw:
            continue

        new_raw, changes = fix_anchor_text(raw)
        if not changes:
            continue

        total_changes += len(changes)
        total_pages   += 1
        print(f'\n[{meta["slug"]}]  ({len(changes)} fix(es))')
        for c in changes:
            print(c)

        if not DRY_RUN:
            status = patch_content(session, meta['endpoint'], meta['id'], new_raw, nonce)
            print(f'  -> patched (HTTP {status})')

    print(f'\n{"="*60}')
    print(f'Pages to update: {total_pages}')
    print(f'Anchors to fix:  {total_changes}')
    if DRY_RUN:
        print('\nRe-run with --apply to write.')


if __name__ == '__main__':
    main()
