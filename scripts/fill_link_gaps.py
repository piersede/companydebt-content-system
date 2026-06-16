"""
Fill internal link gaps across the whole site.

For each page below the inbound-link threshold, scans all source pages
for unlinked occurrences of anchor bank text and inserts links.

Thresholds:
  Hub pages:   5 inbound links
  All others:  3 inbound links

Usage:
  python scripts/fill_link_gaps.py            # dry run
  python scripts/fill_link_gaps.py --apply    # write to staging WP
  python scripts/fill_link_gaps.py --cluster hmrc   # one cluster only
"""
import os, re, sys, json, csv
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from collections import defaultdict

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

STAGING_URL = os.getenv('WP_STAGING_URL', '').rstrip('/')
BA_USER     = os.getenv('WP_BASIC_AUTH_USER', '')
BA_PASS     = os.getenv('WP_BASIC_AUTH_PASS', '')
WP_USER     = os.getenv('WP_STAGING_USERNAME', '')
WP_APP_PASS = os.getenv('WP_STAGING_APP_PASSWORD', '')

DRY_RUN     = '--apply' not in sys.argv
CLUSTER_ARG = next((sys.argv[i+1] for i, a in enumerate(sys.argv) if a == '--cluster'), None)

CACHE_FILE  = 'content_cache.json'
AUDIT_CSV   = 'internal_links_audit.csv'
ANCHOR_XLSX = r'C:\Users\piers\Downloads\companydebt_current_site_url_anchor_banks.xlsx'

# Pages whose inbound target is 5; everything else is 3
HUB_PATHS = {
    '/', '/insolvency/', '/liquidation/liquidation-hub/', '/hmrc/',
    '/company-rescue-solutions/', '/company-cash-flow-problems/',
    '/advice/', '/debt-creditor-pressure-hub/', '/bounce-back-loan-support-hub/',
    '/winding-up-petitions/', '/company-administration/',
    '/liquidation/creditors-voluntary-liquidation/',
    '/liquidation/compulsory-liquidation/',
    '/liquidation/members-voluntary-liquidation/',
    '/company-rescue-solutions/company-voluntary-arrangement/',
    '/what-is-a-pre-pack-administration/', '/company-rescue-solutions/pre-packs/',
    '/closing-a-limited-company/',
}

# Utility paths — skip as targets (nav/footer handles them)
SKIP_TARGETS = {
    '/meet-the-team/', '/about-us/', '/contact-us/', '/site-map/',
    '/terms-conditions/', '/privacy-policy/', '/cookie-policy/',
    '/accessibility/', '/complaints/', '/complaints-procedure/',
    '/legal/', '/content-usage-guidelines/', '/cookie-policy-company-debt/',
    '/feedback/', '/charge-out-rates/', '/useful-publications/',
    '/express-liquidation/', '/stressed-directors-guide/',
}

# Cluster keyword → path prefix mapping (for --cluster filtering)
CLUSTER_MAP = {
    'hmrc':         '/hmrc/',
    'liquidation':  '/liquidation/',
    'advice':       '/advice/',
    'cashflow':     '/company-cash-flow-problems/',
    'rescue':       '/company-rescue-solutions/',
    'insolvency':   '/insolvency/',
    'bbl':          '/bounce-back-loan-support-hub/',
    'winding':      '/winding-up-petitions/',
    'admin':        '/company-administration/',
    'sample':       '/sample-letters/',
    'sector':       '/sector',
}


def to_path(url):
    url = str(url).strip()
    url = re.sub(r'^https?://(?:www\.)?companydebt\.com', '', url)
    url = re.sub(r'^https?://[^/]+', '', url)
    if not url.startswith('/'):
        url = '/' + url
    if not url.endswith('/'):
        url += '/'
    return url


def load_anchor_bank():
    """Returns {path: [anchor1, anchor2, ...]}"""
    df = pd.read_excel(ANCHOR_XLSX, sheet_name='URL Anchors')
    df.columns = ['url', 'anchors']
    skip = ['no routine editorial', 'not normally']
    df = df[~df['anchors'].str.lower().str.contains('|'.join(skip), na=False)]
    result = {}
    for _, row in df.iterrows():
        path = to_path(row['url'])
        anchors = [a.strip() for a in str(row['anchors']).split(',') if a.strip()]
        result[path] = anchors
    return result


def load_inbound_counts(cache=None):
    """
    Build inbound link counts from the live content cache (accurate after
    in-session edits). Falls back to audit CSV if cache not provided.
    """
    inbound = defaultdict(set)
    if cache:
        # Extract all hrefs from each page's raw content
        href_re = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)
        for src_path, meta in cache.items():
            slug = meta['slug']
            raw  = meta.get('raw', '')
            for href in href_re.findall(raw):
                target = to_path(href)
                if target != src_path:
                    inbound[target].add(slug)
    else:
        with open(AUDIT_CSV, encoding='utf-8', newline='') as f:
            for row in csv.DictReader(f):
                t = row.get('target_url', '').strip()
                s = row.get('source_slug', '').strip()
                if t and s:
                    inbound[to_path(t)].add(s)
    return inbound


def load_cache():
    with open(CACHE_FILE, encoding='utf-8') as f:
        return json.load(f)


def already_linked(raw, target_path):
    """True if raw content already contains a link to target_path."""
    return target_path in raw


def find_unlinked_anchor(raw, anchor):
    """
    Find first occurrence of anchor text NOT inside an <a> tag.
    Returns (start, end) of the anchor text, or None.
    """
    pattern = re.compile(re.escape(anchor), re.IGNORECASE)
    for m in pattern.finditer(raw):
        start, end = m.start(), m.end()
        # Check if this match is inside an existing <a>...</a>
        preceding = raw[:start]
        # Count unclosed <a tags before this position
        open_a  = len(re.findall(r'<a\b[^>]*>', preceding))
        close_a = len(re.findall(r'</a>', preceding))
        if open_a > close_a:
            continue  # inside an existing link
        # Also skip if inside a heading tag (h1/h2/h3)
        last_open_tag = re.findall(r'<(h[1-3]|a)\b', preceding)
        last_close_tag = re.findall(r'</(h[1-3]|a)>', preceding)
        # Simple check: don't link inside headings
        open_h = sum(1 for t in last_open_tag if t.startswith('h'))
        close_h = sum(1 for t in last_close_tag if t.startswith('h'))
        if open_h > close_h:
            continue
        return (start, end, m.group(0))
    return None


def insert_link(raw, start, end, original_text, href):
    """Wrap original_text at (start, end) with an <a> tag."""
    return raw[:start] + f'<a href="{href}">{original_text}</a>' + raw[end:]


def api_session():
    s = requests.Session()
    s.auth = (BA_USER, BA_PASS)
    s.headers['User-Agent'] = 'CompanyDebt-LinkFiller/1.0'
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

    print('Loading data...')
    anchor_bank  = load_anchor_bank()
    cache        = load_cache()
    inbound      = load_inbound_counts(cache)  # use live cache, not stale CSV

    # Build a lookup: slug -> path (for checking already-linked sources)
    slug_to_path = {meta['slug']: path for path, meta in cache.items()}

    # Determine which targets need more links
    gaps = []
    for path, anchors in anchor_bank.items():
        if path in SKIP_TARGETS:
            continue
        if CLUSTER_ARG and not any(path.startswith(v) for v in
                                    [CLUSTER_MAP.get(CLUSTER_ARG, CLUSTER_ARG)]):
            continue
        threshold = 5 if path in HUB_PATHS else 3
        current   = len(inbound.get(path, set()))
        needed    = max(0, threshold - current)
        if needed > 0:
            gaps.append((needed, path, anchors))

    gaps.sort(key=lambda x: (-x[0], x[1]))  # most-needed first
    print(f'Pages needing more links: {len(gaps)}')
    print(f'  (threshold: hubs=5, others=3)\n')

    # For each gap target, find source pages that can supply a link
    # We work through the cache and track pending edits per source page
    # so we batch all changes to a source page in one PATCH call.

    # pending_edits[source_path] = {target_path: (anchor_used, new_raw)}
    # We build new_raw incrementally as we add more links to the same source.
    working_raw   = {path: meta['raw'] for path, meta in cache.items()}
    # Track newly added links: target_path -> set of source paths added this run
    new_inbound   = defaultdict(set)
    edits_by_source = defaultdict(list)  # source_path -> [(target_path, anchor)]

    total_links_added = 0
    targets_fixed     = 0

    for needed, target_path, anchors in gaps:
        # How many more do we still need (accounting for links added this run)?
        threshold = 5 if target_path in HUB_PATHS else 3
        current   = len(inbound.get(target_path, set())) + len(new_inbound[target_path])
        still_needed = threshold - current
        if still_needed <= 0:
            continue

        links_added_this_target = 0
        print(f'\n[{target_path}]  have={current}  need={still_needed}')

        # Also try slug-derived phrases as fallback anchors
        slug = target_path.strip('/').split('/')[-1]
        slug_phrase = slug.replace('-', ' ')
        extra_anchors = [slug_phrase] if slug_phrase not in [a.lower() for a in anchors] else []

        for anchor in anchors + extra_anchors:
            if links_added_this_target >= still_needed:
                break

            # Scan all source pages for this anchor
            for src_path, meta in cache.items():
                if links_added_this_target >= still_needed:
                    break
                if src_path == target_path:
                    continue  # no self-links
                if meta['slug'] in inbound.get(target_path, set()):
                    continue  # already links to target
                if src_path in new_inbound[target_path]:
                    continue  # already scheduled to link

                raw = working_raw[src_path]
                if not raw:
                    continue

                result = find_unlinked_anchor(raw, anchor)
                if result is None:
                    continue

                start, end, original = result
                new_raw = insert_link(raw, start, end, original, target_path)
                working_raw[src_path] = new_raw
                new_inbound[target_path].add(src_path)
                edits_by_source[src_path].append((target_path, anchor, meta))
                links_added_this_target += 1
                total_links_added += 1
                print(f'  + [{meta["slug"]}] "{anchor}"')

        final = len(inbound.get(target_path, set())) + len(new_inbound[target_path])
        if final >= (5 if target_path in HUB_PATHS else 3):
            targets_fixed += 1

    print(f'\n{"="*60}')
    print(f'Links to add:    {total_links_added}')
    print(f'Targets fixed:   {targets_fixed} / {len(gaps)}')

    if not edits_by_source:
        print('Nothing to apply.')
        return

    if DRY_RUN:
        print('\nRe-run with --apply to write changes.')
        return

    # Apply: PATCH each modified source page once with all its accumulated changes
    print('\nLogging in and applying...')
    session = api_session()
    wp_login(session)
    nonce = get_nonce(session)
    print(f'  nonce: {nonce[:8]}...\n')

    patched = 0
    for src_path, edit_list in sorted(edits_by_source.items()):
        meta     = cache[src_path]
        endpoint = meta['endpoint']
        post_id  = meta['id']
        slug     = meta['slug']
        new_raw  = working_raw[src_path]
        try:
            status = patch_content(session, endpoint, post_id, new_raw, nonce)
            patched += 1
            print(f'[{slug}] {len(edit_list)} link(s) -> HTTP {status}')
        except Exception as e:
            print(f'[{slug}] ERROR: {e}')

    print(f'\nDone. {patched} pages patched, {total_links_added} links added.')


if __name__ == '__main__':
    main()
