"""
Fix the remaining zero-inbound pages:
1. Sector hub: add links to charity, hospitality, transport sector pages
2. BBL hub: add links from pages mentioning Bounce Back Loan

Applies directly to staging.
"""
import os, re, sys, json, time
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

CACHE_FILE = Path('content_cache.json')
cache = json.loads(CACHE_FILE.read_text(encoding='utf-8'))

# slug -> cache entry
by_slug = {m['slug']: (p, m) for p, m in cache.items()}


def auth_session():
    s = requests.Session()
    s.auth = (BA_USER, BA_PASS)
    s.headers['User-Agent'] = 'CompanyDebt-PatchFinalGaps/1.0'
    s.get(f'{URL}/wp-login.php', timeout=15)
    s.post(f'{URL}/wp-login.php',
           headers={'Referer': f'{URL}/wp-login.php', 'Origin': URL},
           data={'log': WP_USER, 'pwd': WP_PASS, 'wp-submit': 'Log In',
                 'redirect_to': f'{URL}/wp-admin/', 'testcookie': '1'},
           allow_redirects=True, timeout=30)
    admin = s.get(f'{URL}/wp-admin/', timeout=15)
    m = re.search(r'wpApiSettings[^}]+"nonce":"([a-f0-9]+)"', admin.text)
    if not m:
        sys.exit('Could not extract nonce')
    s.headers['X-WP-Nonce'] = m.group(1)
    print(f'  nonce: {m.group(1)[:8]}...')
    return s


def patch(session, post_id, endpoint, new_raw):
    r = session.post(
        f'{URL}/wp-json/wp/v2/{endpoint}/{post_id}',
        json={'content': new_raw},
        headers={'Content-Type': 'application/json'},
        timeout=30,
    )
    r.raise_for_status()
    return r.status_code


def wrap_first(raw, search_text, dest, anchor):
    """Wrap first occurrence of search_text (not already in a link) with <a href=dest>anchor</a>."""
    if dest in raw:
        return raw, False  # already linked
    idx = raw.find(search_text)
    if idx == -1:
        return raw, False
    # Check not already inside <a>
    before = raw[:idx]
    if before.count('<a ') > before.count('</a>'):
        return raw, False
    end = idx + len(search_text)
    new = raw[:idx] + f'<a href="{dest}">{anchor}</a>' + raw[end:]
    return new, True


# ── 1. Sector hub: add charity, hospitality, transport links ──────────────────

SECTOR_PATH, SECTOR_META = by_slug['sector-specific-insolvency']
SECTOR_ID = SECTOR_META['id']
raw = SECTOR_META['raw']

sector_fixes = [
    # (text to find in content, dest, anchor text)
    ('charity and non-profit insolvency',
     '/charity-non-profit-insolvency/',
     'charity and non-profit insolvency'),
    ('hospitality and restaurant insolvency',
     '/hospitality-restaurant-insolvency/',
     'hospitality and restaurant insolvency'),
    ('transport and haulage insolvency',
     '/transport-haulage-insolvency/',
     'transport and haulage insolvency'),
]

sector_changed = False
for search, dest, anchor in sector_fixes:
    raw, changed = wrap_first(raw, search, dest, anchor)
    if changed:
        print(f'  [sector-hub] wrapped "{anchor}" -> {dest}')
        sector_changed = True
    else:
        print(f'  [sector-hub] SKIP "{search}" (already linked or not found)')

# ── 2. BBL hub: add links from pages mentioning Bounce Back Loan ──────────────

BBL_HUB = '/bounce-back-loan-support-hub/'
BBL_PATTERNS = [
    'Bounce Back Loan',
    'bounce back loan',
    'bounce-back loan',
]
BBL_ANCHOR = 'Bounce Back Loan'
BBL_MAX_SOURCES = 5

bbl_sources = []
for src_path, meta in cache.items():
    if src_path == BBL_HUB or src_path.startswith(BBL_HUB):
        continue  # skip hub and its children as sources
    raw_src = meta.get('raw', '')
    if not raw_src:
        continue
    if BBL_HUB in raw_src:
        continue  # already links to hub
    # Check if mentions BBL
    for pat in BBL_PATTERNS:
        if pat in raw_src:
            bbl_sources.append((src_path, meta))
            break

print(f'\nPages mentioning BBL without hub link: {len(bbl_sources)}')
for p, m in bbl_sources[:5]:
    print(f'  {m["slug"]}')

# Patch up to BBL_MAX_SOURCES pages to add the hub link
bbl_patches = []
for src_path, meta in bbl_sources[:BBL_MAX_SOURCES]:
    raw_src = meta['raw']
    for pat in BBL_PATTERNS:
        new_raw, changed = wrap_first(raw_src, pat, BBL_HUB, BBL_ANCHOR)
        if changed:
            bbl_patches.append((meta['id'], meta['endpoint'], meta['slug'], new_raw))
            print(f'  [bbl] wrap "{pat}" in [{meta["slug"]}] -> {BBL_HUB}')
            break

# ── Apply all patches ─────────────────────────────────────────────────────────

print('\nLogging in...')
session = auth_session()

if sector_changed:
    status = patch(session, SECTOR_ID, SECTOR_META['endpoint'], raw)
    print(f'  [sector-specific-insolvency] HTTP {status}')
    time.sleep(0.2)

for post_id, endpoint, slug, new_raw in bbl_patches:
    status = patch(session, post_id, endpoint, new_raw)
    print(f'  [{slug}] HTTP {status}')
    time.sleep(0.2)

total = (3 if sector_changed else 0) + len(bbl_patches)
print(f'\nDone. {total} links added.')
