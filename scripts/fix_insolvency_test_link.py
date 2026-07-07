"""
Site-wide fix: repoint the body-content CTA link that wrongly points at
  /insolvency/insolvency-test/   (a non-existent nested path)
to the correct destination
  /insolvency-calculator/        (same target the sidebar CTA uses)

Crawls ALL published pages + posts on staging (context=edit RAW content),
finds any that contain the bad path in an href, and rewrites it.

The replacement operates on the substring 'insolvency/insolvency-test' ->
'insolvency-calculator', which cleanly handles every href form:
  /insolvency/insolvency-test/                    -> /insolvency-calculator/
  /insolvency/insolvency-test                     -> /insolvency-calculator
  https://host/insolvency/insolvency-test/        -> https://host/insolvency-calculator/
Anchor TEXT ("30-second insolvency test") has no slash, so it is untouched.

Nothing is written unless --apply is passed.

Usage:
  python scripts/fix_insolvency_test_link.py            # dry-run report
  python scripts/fix_insolvency_test_link.py --apply    # write changes
"""
import os, re, sys, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

STAGING_URL = os.getenv('WP_STAGING_URL', '').rstrip('/')
BA_USER     = os.getenv('WP_BASIC_AUTH_USER', '')
BA_PASS     = os.getenv('WP_BASIC_AUTH_PASS', '')
WP_USER     = os.getenv('WP_STAGING_USERNAME', '')
WP_APP_PASS = os.getenv('WP_STAGING_APP_PASSWORD', '')

BAD  = 'insolvency/insolvency-test'
GOOD = 'insolvency-calculator'


def session():
    s = requests.Session()
    s.auth = (BA_USER, BA_PASS)
    s.headers['User-Agent'] = 'CompanyDebt-LinkFix/1.0'
    s.get(f'{STAGING_URL}/wp-login.php', params={'wpe-login': 'true'})
    s.post(f'{STAGING_URL}/wp-login.php', params={'wpe-login': 'true'}, data={
        'log': WP_USER, 'pwd': WP_APP_PASS, 'wp-submit': 'Log In', 'testcookie': '1',
    }, allow_redirects=True)
    r = s.get(f'{STAGING_URL}/wp-admin/', timeout=30)
    m = (re.search(r'wpApiSettings[^}]+"nonce":"([a-f0-9]+)"', r.text)
         or re.search(r'"nonce":"([a-f0-9]+)"', r.text))
    if not m:
        raise RuntimeError('Could not extract WP nonce — check staging credentials')
    s.headers['X-WP-Nonce'] = m.group(1)
    return s


def verify_destinations(s):
    """Confirm the bad path is broken and the good path resolves."""
    for path in ('/insolvency/insolvency-test/', '/insolvency-calculator/'):
        try:
            r = s.get(f'{STAGING_URL}{path}', timeout=30, allow_redirects=True)
            print(f'  GET {path:34s} -> {r.status_code}  (final: {r.url})')
        except Exception as e:
            print(f'  GET {path:34s} -> ERROR {e}')


def crawl(s, endpoint):
    """Yield every published item as (id, slug, link, raw)."""
    page = 1
    while True:
        r = s.get(f'{STAGING_URL}/wp-json/wp/v2/{endpoint}',
                  params={'context': 'edit', 'status': 'publish',
                          'per_page': 100, 'page': page,
                          '_fields': 'id,slug,link,content'}, timeout=60)
        if r.status_code == 400:  # past last page
            break
        r.raise_for_status()
        items = r.json()
        if not items:
            break
        for it in items:
            yield (it['id'], it.get('slug', ''), it.get('link', ''),
                   it.get('content', {}).get('raw', ''))
        total_pages = int(r.headers.get('X-WP-TotalPages', page))
        if page >= total_pages:
            break
        page += 1


def patch(s, endpoint, pid, raw):
    r = s.post(f'{STAGING_URL}/wp-json/wp/v2/{endpoint}/{pid}',
               json={'content': raw},
               headers={'Content-Type': 'application/json'}, timeout=60)
    r.raise_for_status()
    return r.status_code


def main():
    apply = '--apply' in sys.argv
    if not STAGING_URL:
        print('ERROR: WP_STAGING_URL not set'); sys.exit(1)

    s = session()
    print('Destination check:')
    verify_destinations(s)
    print()

    hits = []
    for endpoint in ('pages', 'posts'):
        for pid, slug, link, raw in crawl(s, endpoint):
            n = raw.count(BAD)
            if n:
                hits.append((endpoint, pid, slug, link, n, raw))

    print(f'Affected items: {len(hits)}  (total occurrences: {sum(h[4] for h in hits)})\n')
    ok = fail = 0
    for endpoint, pid, slug, link, n, raw in hits:
        print(f'  [{endpoint}/{pid}] {slug}  x{n}  {link}')
        if apply:
            new_raw = raw.replace(BAD, GOOD)
            try:
                code = patch(s, endpoint, pid, new_raw)
                print(f'      PATCH {code}')
                ok += 1
            except Exception as e:
                print(f'      FAIL {e}')
                fail += 1
            time.sleep(0.25)

    if apply:
        print(f'\nDone: {ok} patched, {fail} failed')
    else:
        print('\n(dry run — pass --apply to write)')


if __name__ == '__main__':
    main()
