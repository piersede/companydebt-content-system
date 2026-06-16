"""
Resolve the 404 links in links_404_needs_decision.csv.

For each broken link:
  - If the old target URL is in REMAP → update href to the new relative path
  - Otherwise → strip the <a> tag (keep anchor text)

Usage:
  python scripts/fix_404_links.py            # dry run
  python scripts/fix_404_links.py --apply    # write to staging WP
"""
import os, csv, sys, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from collections import defaultdict

import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

STAGING_URL = os.getenv('WP_STAGING_URL', '').rstrip('/')
BA_USER     = os.getenv('WP_BASIC_AUTH_USER', '')
BA_PASS     = os.getenv('WP_BASIC_AUTH_PASS', '')
WP_USER     = os.getenv('WP_STAGING_USERNAME', '')
WP_APP_PASS = os.getenv('WP_STAGING_APP_PASSWORD', '')

DECISIONS_CSV = 'links_404_needs_decision.csv'
DRY_RUN       = '--apply' not in sys.argv

# Old target URL → new staging-relative path.
# Covers: URL restructures, live-site links pointing to moved slugs,
# staging links with old parent paths.
REMAP = {
    # Pre-pack administration — canonical URL
    'https://comdebstage.wpengine.com/company-rescue-solutions/pre-pack-administration/':
        '/company-rescue-solutions/pre-packs/',

    # CVA vs liquidation — old slug/path variations
    'https://comdebstage.wpengine.com/company-rescue-solutions/company-voluntary-arrangement/cva-vs-liquidation/':
        '/company-rescue-solutions/company-voluntary-arrangement/vs-liquidation/',
    'https://comdebstage.wpengine.com/company-rescue-solutions/cva-vs-liquidation/':
        '/company-rescue-solutions/company-voluntary-arrangement/vs-liquidation/',
    'https://www.companydebt.com/company-rescue-solutions/company-voluntary-arrangement/cva-vs-liquidation/':
        '/company-rescue-solutions/company-voluntary-arrangement/vs-liquidation/',
    'https://www.companydebt.com/vs-liquidation/':
        '/company-rescue-solutions/company-voluntary-arrangement/vs-liquidation/',
    'https://comdebstage.wpengine.com/vs-liquidation/':
        '/company-rescue-solutions/company-voluntary-arrangement/vs-liquidation/',

    # CVA fails — slug renamed
    'https://www.companydebt.com/company-rescue-solutions/company-voluntary-arrangement/what-happens-when-a-cva-fails/':
        '/company-rescue-solutions/company-voluntary-arrangement/when-a-cva-fails/',

    # Company Voluntary Arrangement hub — old short path
    'https://www.companydebt.com/company-voluntary-arrangement/':
        '/company-rescue-solutions/company-voluntary-arrangement/',
    'https://comdebstage.wpengine.com/company-voluntary-arrangement/':
        '/company-rescue-solutions/company-voluntary-arrangement/',

    # Free advice → correct advice page
    '/free-advice/':
        '/advice/get-free-business-debt-advice/',

    # Company voluntary liquidation → CVL hub
    'https://www.companydebt.com/insolvency/company-voluntary-liquidation/':
        '/liquidation/creditors-voluntary-liquidation/',

    # What is insolvency → insolvency hub
    'https://www.companydebt.com/what-is-insolvency/':
        '/insolvency/',

    # HMRC debt collection — old slug, moved into /hmrc/ section
    'https://comdebstage.wpengine.com/hmrc-debt-collection/':
        '/hmrc/understanding-hmrc-debt-collection/',
    'https://www.companydebt.com/hmrc-debt-collection/':
        '/hmrc/understanding-hmrc-debt-collection/',

    # Director guarantees in a CVA — old root path
    'https://comdebstage.wpengine.com/director-guarantees-in-a-cva/':
        '/company-rescue-solutions/company-voluntary-arrangement/director-guarantees-in-a-cva/',
    'https://www.companydebt.com/director-guarantees-in-a-cva/':
        '/company-rescue-solutions/company-voluntary-arrangement/director-guarantees-in-a-cva/',

    # Personal guarantee risks — old live path
    'https://www.companydebt.com/the-risks-of-signing-a-personal-guarantee/':
        '/advice/the-risks-of-signing-a-personal-guarantee/',

    # Director guarantees (short slug) → personal guarantees page
    'https://comdebstage.wpengine.com/director-guarantees/':
        '/advice/directors-personal-guarantees/',

    # CVL old slug
    'https://www.companydebt.com/cvl-creditors-voluntary-liquidation/':
        '/liquidation/creditors-voluntary-liquidation/',
    'https://comdebstage.wpengine.com/cvl-creditors-voluntary-liquidation/':
        '/liquidation/creditors-voluntary-liquidation/',

    # CVL vs liquidation old path
    'https://comdebstage.wpengine.com/liquidation/creditors-voluntary-liquidation-vs-liquidation/':
        '/liquidation/creditors-voluntary-liquidation/',

    # Partnership voluntary arrangements — old live path
    'https://www.companydebt.com/partnership-voluntary-arrangements/':
        '/company-rescue-solutions/partnership-voluntary-arrangements/',

    # Business recovery services — old root path
    'https://comdebstage.wpengine.com/business-recovery-services/':
        '/insolvency/business-recovery-services/',

    # How to save struggling business — old live path
    'https://www.companydebt.com/how-to-save-a-struggling-business/':
        '/insolvency/how-to-save-a-struggling-business/',

    # Rescue business from insolvency — old root and live paths
    'https://www.companydebt.com/rescue-your-business-from-insolvency/':
        '/insolvency/rescue-your-business-from-insolvency/',
    'https://comdebstage.wpengine.com/rescue-your-business-from-insolvency/':
        '/insolvency/rescue-your-business-from-insolvency/',

    # Insolvent company investigations — old root and live paths
    'https://comdebstage.wpengine.com/insolvent-company-investigations/':
        '/insolvency/insolvent-company-investigations/',
    'https://www.companydebt.com/insolvent-company-investigations/':
        '/insolvency/insolvent-company-investigations/',

    # Administration — moved under /company-administration/
    'https://comdebstage.wpengine.com/company-rescue-solutions/administration/':
        '/company-administration/',

    # Personal guarantee old long slug — remap to risks page
    'https://comdebstage.wpengine.com/advice/what-if-i-have-a-personal-guarantee-and-my-business-goes-into-liquidation/':
        '/advice/the-risks-of-signing-a-personal-guarantee/',

    # CVA pros and cons — strip (no equivalent page exists)
    # directors-duties-when-insolvent — strip (no equivalent page exists)
}

# URLs not in REMAP get stripped (link removed, text kept).
STRIP_URLS = {
    'https://comdebstage.wpengine.com/company-rescue-solutions/cva-pros-and-cons/',
    'https://www.companydebt.com/insolvency/directors-duties-when-insolvent/',
}


def api_session():
    s = requests.Session()
    s.auth = (BA_USER, BA_PASS)
    s.headers['User-Agent'] = 'CompanyDebt-Fix404/1.0'
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


def get_raw_content(session, endpoint, post_id, nonce):
    r = session.get(
        f'{STAGING_URL}/wp-json/wp/v2/{endpoint}/{post_id}',
        params={'context': 'edit', '_fields': 'id,slug,content'},
        headers={'X-WP-Nonce': nonce},
        timeout=30,
    )
    r.raise_for_status()
    return r.json().get('content', {}).get('raw', '')


def patch_content(session, endpoint, post_id, raw_content, nonce):
    r = session.post(
        f'{STAGING_URL}/wp-json/wp/v2/{endpoint}/{post_id}',
        json={'content': raw_content},
        headers={'X-WP-Nonce': nonce, 'Content-Type': 'application/json'},
        timeout=30,
    )
    r.raise_for_status()
    return r.status_code


def replace_href(content, old_href, new_href):
    """Swap href value in <a> tags matching old_href."""
    old_esc = re.escape(old_href)
    # Double-quoted
    content, n1 = re.subn(
        rf'(<a\s[^>]*href="){old_esc}"',
        rf'\g<1>{new_href}"',
        content, flags=re.IGNORECASE,
    )
    # Single-quoted
    content, n2 = re.subn(
        rf"(<a\s[^>]*href='){old_esc}'",
        rf"\g<1>{new_href}'",
        content, flags=re.IGNORECASE,
    )
    return content, n1 + n2


def strip_link(content, href):
    """Remove <a href="href">...</a>, keeping inner text."""
    href_esc = re.escape(href)
    content, n1 = re.subn(
        rf'<a\s[^>]*href="{href_esc}"[^>]*>(.*?)</a>',
        r'\1', content, flags=re.DOTALL | re.IGNORECASE,
    )
    content, n2 = re.subn(
        rf"<a\s[^>]*href='{href_esc}'[^>]*>(.*?)</a>",
        r'\1', content, flags=re.DOTALL | re.IGNORECASE,
    )
    return content, n1 + n2


def type_to_endpoint(source_type):
    return 'posts' if source_type == 'post' else 'pages'


def main():
    if DRY_RUN:
        print('DRY RUN — no changes written. Pass --apply to write.\n')

    with open(DECISIONS_CSV, encoding='utf-8', newline='') as f:
        rows = list(csv.DictReader(f))

    remapped = [(r, REMAP[r['target_url']]) for r in rows if r['target_url'] in REMAP]
    stripped = [r for r in rows if r['target_url'] not in REMAP]
    unknown  = [r for r in stripped if r['target_url'] not in STRIP_URLS]

    print(f'Total 404 links:  {len(rows)}')
    print(f'  To remap:       {len(remapped)}')
    print(f'  To strip:       {len(stripped)}')
    if unknown:
        print(f'\nWARNING: {len(unknown)} links not in REMAP or STRIP_URLS — will be stripped:')
        for r in unknown:
            print(f'  [{r["source_slug"]}] {r["target_url"]}')
    print()

    # Group all actions by source page
    by_source = defaultdict(list)
    for row, new_path in remapped:
        by_source[(row['source_id'], row['source_slug'], row['source_type'])].append(
            ('remap', row['target_url'], new_path)
        )
    for row in stripped:
        by_source[(row['source_id'], row['source_slug'], row['source_type'])].append(
            ('strip', row['target_url'], None)
        )

    session = api_session()
    nonce = None
    if not DRY_RUN:
        print('Logging in to staging...')
        wp_login(session)
        nonce = get_nonce(session)
        print(f'  nonce: {nonce[:8]}...\n')

    total_remapped = 0
    total_stripped = 0

    for (source_id, source_slug, source_type), actions in sorted(by_source.items(), key=lambda x: x[0][1]):
        endpoint = type_to_endpoint(source_type)
        remaps = [(old, new) for action, old, new in actions if action == 'remap']
        strips = [old for action, old, _ in actions if action == 'strip']
        print(f'[{source_slug}] remap={len(remaps)} strip={len(strips)}')
        for old, new in remaps:
            print(f'  REMAP  {old}')
            print(f'      -> {new}')
        for old in strips:
            print(f'  STRIP  {old}')

        if not DRY_RUN:
            raw = get_raw_content(session, endpoint, source_id, nonce)
            changed = 0
            for old, new in remaps:
                raw, n = replace_href(raw, old, new)
                changed += n
            for old in strips:
                raw, n = strip_link(raw, old)
                changed += n
            if changed:
                patch_content(session, endpoint, source_id, raw, nonce)
                print(f'  -> {changed} substitution(s) applied')
            else:
                print(f'  -> no matches found in raw content (may already be fixed)')

        total_remapped += len(remaps)
        total_stripped += len(strips)

    print(f'\nDone. Remapped: {total_remapped}, Stripped: {total_stripped}')
    if DRY_RUN:
        print('Re-run with --apply to write changes.')


if __name__ == '__main__':
    main()
