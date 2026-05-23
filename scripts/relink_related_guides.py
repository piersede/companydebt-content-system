"""
Restore links inside "Related Guides" sections across staging.

The blanket internal-link strip removed the <a> tags from these curated
guide lists but kept the text. This script finds every "Related Guides"
section, resolves each entry's guide name to a live page (slug match against
the staging inventory, plus a small validated alias map), and re-wraps it.

Usage:
  python scripts/relink_related_guides.py            # dry run
  python scripts/relink_related_guides.py --apply    # write to staging

Outputs internal-links/related-guides-relink.csv (proposed) and prints
anything it could not confidently resolve. Credentials from .env only.
"""
import os, re, sys, csv, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from html import unescape

import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')


def env(key):
    v = os.getenv(key)
    if not v:
        sys.exit(f'Missing required .env key: {key}')
    return v

STAGING_URL = env('WP_STAGING_URL').rstrip('/')
BA_USER     = env('WP_BASIC_AUTH_USER')
BA_PASS     = env('WP_BASIC_AUTH_PASS')
WP_USER     = env('WP_STAGING_USERNAME')
WP_APP_PASS = env('WP_STAGING_APP_PASSWORD')

APPLY   = '--apply' in sys.argv
OUT_CSV = 'internal-links/related-guides-relink.csv'

# Guide names whose slug does not match a page slug 1:1. Validated against the
# live inventory at runtime before use.
ALIASES = {
    'company-insolvency': '/insolvency/',
    '30-second-insolvency-test': '/insolvency/insolvency-test/',
    'insolvency-test': '/insolvency/insolvency-test/',
    'company-liquidation': '/liquidation/',
    'strike-off-and-dissolution': '/liquidation/company-strike-off-and-dissolution/',
    'cannot-pay-paye': '/hmrc/cant-pay-paye/',
    'cannot-pay-vat': '/hmrc/cant-pay-vat/',
    'problems-paying-corporation-tax': '/hmrc/problems-paying-corporation-tax-hmrc/',
    'hmrc-tax-debt-hub': '/hmrc/',
    'hmrc-personal-liability-notices': '/hmrc/personal-liability-notices/',
    'company-rescue-solutions-hub': '/company-rescue-solutions/',
    'debt-and-creditor-pressure-hub': '/debt-creditor-pressure-hub/',
    'mental-health-and-debt-stress-support': '/mental-health-debt-stress-support/',
    'statutory-demands': '/company-cash-flow-problems/what-is-a-statutory-demand-against-a-company/',
    'can-a-director-be-made-bankrupt': '/advice/can-a-director-be-made-bankrupt-if-a-business-fails/',
    'what-happens-to-directors-during-liquidation': '/liquidation/what-happens-to-directors-in-liquidation/',
    'what-happens-to-employees-in-liquidation': '/liquidation/what-happens-to-employees/',
    'when-to-stop-trading': '/liquidation/when-should-a-director-stop-trading/',
    'which-creditors-get-paid-first-in-liquidation': '/liquidation/which-creditors-get-paid-first/',
}

HEADING_RE = re.compile(r'<h[2-4][^>]*>\s*related\s+guides\s*</h[2-4]>', re.IGNORECASE)
LIST_RE    = re.compile(r'<!-- wp:list(?: \{[^}]*\})? -->(.*?)<!-- /wp:list -->', re.DOTALL)
LI_RE      = re.compile(r'<li[^>]*>(.*?)</li>', re.DOTALL | re.IGNORECASE)
TAG_RE     = re.compile(r'<[^>]+>')


def slugify(text):
    text = unescape(re.sub(r'&#\d+;|&[a-z]+;', "'", text))
    text = re.sub(r"['‘’]", '', text)
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text


def norm_anchor(text):
    return re.sub(r'\s+', ' ', unescape(text)).strip().lower()


def to_path(url):
    for dom in ('https://comdebstage.wpengine.com', 'http://comdebstage.wpengine.com',
                'https://www.companydebt.com', 'http://www.companydebt.com'):
        url = url.replace(dom, '')
    url = url.split('?')[0].split('#')[0]
    return url or '/'


def api_session():
    s = requests.Session()
    s.auth = (BA_USER, BA_PASS)
    s.headers['User-Agent'] = 'CompanyDebt-RelatedGuides/1.0'
    return s


def wp_login(session):
    lu = f'{STAGING_URL}/wp-login.php'
    session.get(lu, params={'wpe-login': 'true'})
    session.post(lu, params={'wpe-login': 'true'}, data={
        'log': WP_USER, 'pwd': WP_APP_PASS, 'wp-submit': 'Log In', 'testcookie': '1',
    }, allow_redirects=True)


def get_nonce(session):
    r = session.get(f'{STAGING_URL}/wp-admin/', timeout=30)
    for pat in (r'wpApiSettings[^}]+"nonce":"([a-f0-9]+)"', r'"nonce":"([a-f0-9]+)"'):
        m = re.search(pat, r.text)
        if m:
            return m.group(1)
    raise RuntimeError('Could not extract WP nonce')


def fetch_all(session, nonce):
    items = []
    for post_type in ('posts', 'pages'):
        page = 1
        while True:
            r = session.get(f'{STAGING_URL}/wp-json/wp/v2/{post_type}',
                params={'per_page': 100, 'page': page, 'status': 'publish',
                        'context': 'edit', '_fields': 'id,slug,link,type,title,content'},
                headers={'X-WP-Nonce': nonce}, timeout=60)
            if r.status_code == 400:
                break
            r.raise_for_status()
            batch = r.json()
            if not batch:
                break
            for it in batch:
                path = (it.get('link', '')
                        .replace('https://comdebstage.wpengine.com', '')
                        .replace('https://www.companydebt.com', '') or '/')
                items.append({
                    'id': it['id'], 'slug': it['slug'], 'type': it['type'], 'path': path,
                    'title': it.get('title', {}).get('rendered', ''),
                    'raw': it.get('content', {}).get('raw', ''),
                })
            if len(batch) < 100:
                break
            page += 1
    return items


def patch(session, post_type, pid, content, nonce):
    endpoint = 'posts' if post_type == 'post' else 'pages'
    r = session.post(f'{STAGING_URL}/wp-json/wp/v2/{endpoint}/{pid}',
                     json={'content': content},
                     headers={'X-WP-Nonce': nonce, 'Content-Type': 'application/json'},
                     timeout=30)
    r.raise_for_status()
    return r.status_code


def relink_list_block(list_html, resolve, own_path):
    """Re-link unlinked guide names in one Related Guides list block.
    Returns (new_html, [(name, path)], [unresolved])."""
    done, unresolved = [], []

    def fix_li(m):
        li = m.group(1)
        # already has an internal link on the lead text? leave it.
        if re.match(r'\s*(<strong>)?\s*<a\b', li, re.IGNORECASE):
            return m.group(0)
        # guide name = text before the first colon
        plain = TAG_RE.sub('', li)
        name = plain.split(':', 1)[0].strip()
        if not name or len(name) > 70:
            return m.group(0)
        path = resolve(name, own_path)
        if not path or path == own_path:
            if name:
                unresolved.append(name)
            return m.group(0)
        # wrap the first occurrence of the name text in the li (outside tags)
        name_rx = re.compile(re.escape(name).replace(r'\ ', r'\s+'), re.IGNORECASE)
        wrapped = [False]

        def wrap(mm):
            if wrapped[0]:
                return mm.group(0)
            wrapped[0] = True
            return f'<a href="{path}">{mm.group(0)}</a>'

        new_li = name_rx.sub(wrap, li, count=1)
        if wrapped[0]:
            done.append((name, path))
        return f'<li>{new_li}</li>'

    new_html = LI_RE.sub(fix_li, list_html)
    return new_html, done, unresolved


def main():
    os.makedirs('internal-links', exist_ok=True)
    mode = 'APPLY' if APPLY else 'DRY RUN'
    print(f'=== Related Guides relink — {mode} ===\n')

    session = api_session()
    print('Logging in...')
    wp_login(session)
    nonce = get_nonce(session)
    print('Fetching all content...')
    items = fetch_all(session, nonce)
    print(f'  {len(items)} pages/posts\n')

    # resolver maps
    slug_to_path = {it['slug']: it['path'] for it in items}
    valid_paths  = {it['path'] for it in items}
    aliases = {k: v for k, v in ALIASES.items() if v in valid_paths}

    # pre-strip audit record: exact original (page, anchor) -> target
    audit_map, audit_global = {}, {}
    if os.path.exists('internal_links_audit.csv'):
        for r in csv.DictReader(open('internal_links_audit.csv', encoding='utf-8')):
            a = norm_anchor(r.get('anchor', ''))
            tgt = to_path(r.get('target_url', ''))
            src = to_path(r.get('source_url', ''))
            if not a or not tgt or tgt not in valid_paths:
                continue
            audit_map[(src, a)] = tgt
            audit_global.setdefault(a, set()).add(tgt)
        print(f'  audit record: {len(audit_map)} (page,anchor) entries\n')

    def resolve(name, source_path):
        a = norm_anchor(name)
        # 1. exact pre-strip record for this page
        t = audit_map.get((source_path, a))
        if t:
            return t
        # 2. pre-strip record, globally unambiguous
        g = audit_global.get(a)
        if g and len(g) == 1:
            return next(iter(g))
        # 3. slug match against the live inventory
        s = slugify(name)
        if s in slug_to_path:
            return slug_to_path[s]
        # 4. validated alias
        if s in aliases:
            return aliases[s]
        return None

    rows, all_unresolved = [], []
    pages_changed = 0
    patched = 0

    for it in items:
        raw = it['raw']
        if not raw or not HEADING_RE.search(raw):
            continue
        # for each Related Guides heading, fix the next list block
        new_raw = raw
        page_done = []
        for hm in HEADING_RE.finditer(raw):
            lm = LIST_RE.search(raw, hm.end())
            if not lm:
                continue
            fixed, done, unresolved = relink_list_block(lm.group(1), resolve, it['path'])
            all_unresolved += [(it['slug'], u) for u in unresolved]
            if done:
                # replace this specific list block in new_raw
                old_block = lm.group(0)
                new_block = old_block.replace(lm.group(1), fixed, 1)
                new_raw = new_raw.replace(old_block, new_block, 1)
                page_done += done
        if page_done:
            pages_changed += 1
            for name, path in page_done:
                rows.append({'source_path': it['path'], 'guide_name': name, 'target': path})
            if APPLY and new_raw != raw:
                status = patch(session, it['type'], it['id'], new_raw, nonce)
                patched += 1
                print(f'  [{it["slug"]}] relinked {len(page_done)} entr(y/ies) (HTTP {status})')
                time.sleep(0.15)

    with open(OUT_CSV, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['source_path', 'guide_name', 'target'])
        w.writeheader()
        w.writerows(rows)

    print(f'\n--- SUMMARY ---')
    print(f'Related Guides entries relinked: {len(rows)} across {pages_changed} pages')
    if all_unresolved:
        uniq = sorted(set(n for _, n in all_unresolved))
        print(f'\nUnresolved guide names ({len(uniq)} distinct) — left untouched:')
        for n in uniq:
            print(f'  "{n}"')
    print(f'\nProposed relinks written to {OUT_CSV}')
    if APPLY:
        print(f'Applied to {patched} pages.')
    else:
        print('Dry run — re-run with --apply to write.')


if __name__ == '__main__':
    main()
