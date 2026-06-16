"""
Restore all pages/posts to their previous WP revision.
Uses the revision immediately before the most recent change (index [1]).

Usage:
  python scripts/restore_from_revisions.py            # dry run
  python scripts/restore_from_revisions.py --apply    # write to staging
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


def api_session():
    s = requests.Session()
    s.auth = (BA_USER, BA_PASS)
    s.headers['User-Agent'] = 'CompanyDebt-Restore/1.0'
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


def fetch_all_ids(session, nonce):
    items = []
    for post_type in ('posts', 'pages'):
        page = 1
        while True:
            r = session.get(
                f'{STAGING_URL}/wp-json/wp/v2/{post_type}',
                params={'per_page': 100, 'page': page, 'status': 'publish',
                        '_fields': 'id,slug,type'},
                headers={'X-WP-Nonce': nonce},
                timeout=30,
            )
            if r.status_code == 400:
                break
            r.raise_for_status()
            batch = r.json()
            if not batch:
                break
            items.extend(batch)
            if len(batch) < 100:
                break
            page += 1
    return items


def get_previous_revision(session, endpoint, post_id, nonce):
    """Return the raw content of the revision just before the most recent one, or None."""
    r = session.get(
        f'{STAGING_URL}/wp-json/wp/v2/{endpoint}/{post_id}/revisions',
        params={'per_page': 2, 'context': 'edit'},
        headers={'X-WP-Nonce': nonce},
        timeout=30,
    )
    if r.status_code != 200:
        return None
    revisions = r.json()
    if len(revisions) < 2:
        return None  # Only one revision means no prior state to restore to
    # Revisions are ordered newest first — index [1] is before our change
    return revisions[1].get('content', {}).get('raw', '')


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
        print('DRY RUN — no changes will be written. Pass --apply to write.\n')

    session = api_session()
    print('Logging in to staging...')
    wp_login(session)
    nonce = get_nonce(session)
    print(f'  nonce: {nonce[:8]}...\n')

    print('Fetching all published posts and pages...')
    items = fetch_all_ids(session, nonce)
    print(f'  {len(items)} items found\n')

    restored = 0
    skipped  = 0

    for item in items:
        post_id   = item['id']
        slug      = item['slug']
        post_type = item.get('type', 'page')
        endpoint  = 'posts' if post_type == 'post' else 'pages'

        prev_raw = get_previous_revision(session, endpoint, post_id, nonce)

        if prev_raw is None:
            skipped += 1
            continue

        print(f'  RESTORE [{slug}]')

        if not DRY_RUN:
            status = patch_content(session, endpoint, post_id, prev_raw, nonce)
            print(f'    patched (HTTP {status})')

        restored += 1

    print(f'\n{"Would restore" if DRY_RUN else "Restored"} {restored} pages.')
    print(f'Skipped {skipped} (no prior revision).')
    if DRY_RUN:
        print('\nRun with --apply to write changes.')


if __name__ == '__main__':
    main()
