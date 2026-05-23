"""
Comprehensive internal link audit for staging.

Fetches every published post and page from staging, extracts all internal links,
checks each target URL's HTTP status (on staging), and outputs:
  - internal_links_audit.csv    — all link instances
  - internal_links_problems.csv — non-200 targets only (404, 301, 302, 410, etc.)
"""
import os, re, csv, time, sys
from html import unescape
from urllib.parse import urlparse, urlunparse
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

STAGING_URL  = os.getenv('WP_STAGING_URL', '').rstrip('/')
BA_USER      = os.getenv('WP_BASIC_AUTH_USER', '')
BA_PASS      = os.getenv('WP_BASIC_AUTH_PASS', '')
WP_USER      = os.getenv('WP_STAGING_USERNAME', '')
WP_APP_PASS  = os.getenv('WP_STAGING_APP_PASSWORD', '')

STAGING_HOST = urlparse(STAGING_URL).netloc   # comdebstage.wpengine.com
LIVE_HOST    = 'www.companydebt.com'

AUDIT_CSV    = 'internal_links_audit.csv'
PROBLEMS_CSV = 'internal_links_problems.csv'

MAX_WORKERS  = 5
BURST_DELAY  = 0.1   # seconds between batches


def api_session():
    """Session with nginx basic auth. WP auth is handled via cookie + nonce."""
    s = requests.Session()
    s.auth = (BA_USER, BA_PASS)
    s.headers['User-Agent'] = 'CompanyDebt-LinkAudit/1.0'
    return s


def wp_login(session):
    """Log in to WP to get session cookie (nginx auth handled by session.auth)."""
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
    raise RuntimeError('Could not extract WP nonce from wp-admin')


def fetch_all_content(session, nonce):
    """Return list of dicts: id, slug, type, link, content."""
    items = []
    for post_type in ('posts', 'pages'):
        page = 1
        while True:
            r = session.get(
                f'{STAGING_URL}/wp-json/wp/v2/{post_type}',
                params={'per_page': 100, 'page': page, 'status': 'publish',
                        '_fields': 'id,slug,link,content'},
                headers={'X-WP-Nonce': nonce},
                timeout=30,
            )
            if r.status_code == 400:
                break
            r.raise_for_status()
            batch = r.json()
            if not batch:
                break
            for it in batch:
                items.append({
                    'id':   it['id'],
                    'slug': it['slug'],
                    'type': post_type.rstrip('s'),
                    'link': it.get('link', ''),
                    'content': it.get('content', {}).get('rendered', ''),
                })
            if len(batch) < 100:
                break
            page += 1
        count = sum(1 for i in items if i['type'] == post_type.rstrip('s'))
        print(f'  {post_type}: {count} items')
    return items


def extract_internal_links(content_html):
    """Return list of (href, anchor_text) for all internal links in rendered HTML."""
    links = []
    for m in re.finditer(r'<a\s[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', content_html, re.DOTALL):
        href = unescape(m.group(1)).strip()
        anchor = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if not href or href.startswith('#') or href.startswith('mailto:') or href.startswith('tel:'):
            continue
        parsed = urlparse(href)
        # Keep only links to our domain or relative paths
        if parsed.netloc and parsed.netloc not in (LIVE_HOST, STAGING_HOST):
            continue
        links.append((href, anchor))
    return links


def normalise_to_staging(href):
    """Rewrite live domain to staging domain for status checking."""
    parsed = urlparse(href)
    if parsed.netloc == LIVE_HOST:
        parsed = parsed._replace(netloc=STAGING_HOST, scheme='https')
    elif not parsed.netloc:
        parsed = parsed._replace(netloc=STAGING_HOST, scheme='https')
    return urlunparse(parsed)


def check_url_status(session, url):
    """
    HEAD the URL without following redirects.
    Returns (status_code, redirect_to).
    redirect_to is the Location header value (or empty string) for 3xx responses.
    """
    try:
        r = session.head(url, allow_redirects=False, timeout=15)
        location = r.headers.get('Location', '')
        # Some servers don't respond to HEAD — fall back to GET
        if r.status_code == 405:
            r = session.get(url, allow_redirects=False, timeout=15, stream=True)
            r.close()
            location = r.headers.get('Location', '')
        return r.status_code, location
    except requests.exceptions.RequestException as e:
        return 0, str(e)


def main():
    session = api_session()

    print('Logging in to staging...')
    wp_login(session)
    nonce = get_nonce(session)
    print(f'  nonce: {nonce[:8]}...\n')

    print('Fetching all published content from staging...')
    items = fetch_all_content(session, nonce)
    print(f'Total: {len(items)} posts/pages\n')

    # Build full link inventory
    print('Extracting internal links...')
    link_rows = []   # (source_id, source_slug, source_type, target_url, anchor)
    for item in items:
        links = extract_internal_links(item['content'])
        for href, anchor in links:
            link_rows.append({
                'source_id':   item['id'],
                'source_slug': item['slug'],
                'source_type': item['type'],
                'source_url':  item['link'],
                'target_url':  href,
                'anchor':      anchor,
            })

    print(f'Found {len(link_rows)} internal link instances\n')

    # Deduplicate targets for status checking
    unique_targets = list({r['target_url'] for r in link_rows})
    print(f'Checking status of {len(unique_targets)} unique target URLs...')

    status_map = {}   # original href → (status_code, redirect_to)

    def check(href):
        staging_url = normalise_to_staging(href)
        code, location = check_url_status(session, staging_url)
        return href, code, location

    checked = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(check, href): href for href in unique_targets}
        batch_count = 0
        for future in as_completed(futures):
            href, code, location = future.result()
            status_map[href] = (code, location)
            checked += 1
            batch_count += 1
            if batch_count >= MAX_WORKERS:
                time.sleep(BURST_DELAY)
                batch_count = 0
            if checked % 50 == 0 or checked == len(unique_targets):
                print(f'  {checked}/{len(unique_targets)} checked...', end='\r')

    print(f'\nDone checking.\n')

    # Tally results
    from collections import Counter
    code_counts = Counter(status_map[h][0] for h in status_map)
    print('Status breakdown:')
    for code, count in sorted(code_counts.items()):
        label = {200: 'OK', 301: 'Redirect', 302: 'Redirect', 404: 'Not Found',
                 410: 'Gone', 0: 'Error'}.get(code, '')
        print(f'  {code} {label}: {count} unique URLs')

    # Write full audit CSV
    with open(AUDIT_CSV, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=[
            'source_id', 'source_slug', 'source_type', 'source_url',
            'target_url', 'target_status', 'redirect_to', 'anchor'])
        w.writeheader()
        for row in link_rows:
            code, location = status_map.get(row['target_url'], (0, ''))
            w.writerow({**row, 'target_status': code, 'redirect_to': location})

    # Write problems CSV (non-200)
    problems = []
    for row in link_rows:
        code, location = status_map.get(row['target_url'], (0, ''))
        if code != 200:
            problems.append({**row, 'target_status': code, 'redirect_to': location})

    with open(PROBLEMS_CSV, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=[
            'source_id', 'source_slug', 'source_type', 'source_url',
            'target_url', 'target_status', 'redirect_to', 'anchor'])
        w.writeheader()
        for row in problems:
            w.writerow(row)

    print(f'\nOutputs:')
    print(f'  {AUDIT_CSV}     — {len(link_rows)} rows')
    print(f'  {PROBLEMS_CSV}  — {len(problems)} rows (non-200 only)')
    print(f'\nProblems by source page:')
    from collections import defaultdict
    by_source = defaultdict(list)
    for p in problems:
        by_source[p['source_slug']].append(p)
    for slug, rows in sorted(by_source.items()):
        print(f'  {slug} ({len(rows)} issues)')


if __name__ == '__main__':
    main()
