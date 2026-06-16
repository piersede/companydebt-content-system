"""
Build the liquidation-cluster internal-link plan from the designed strategy files.

Inputs (all under internal-links/):
  liquidation_anchor_banks.json   curated anchor banks per target
  liquidation_link_graph.json     designed source -> targets graph
Plus staging_page_inventory.json  (target URL validation)

For every designed (source -> target) link, the script fetches the source page,
finds where a bank anchor sits naturally in the body copy, and records it.
Anchor selection rotates categories (close_variants/process/risk/contextual
BEFORE exact) and caps any single phrase at 6 uses cluster-wide, so anchor text
stays varied. A designed link that has no natural anchor in the copy is dropped
(not forced) and logged.

Usage:
  python scripts/build_liquidation_link_plan.py            # plan only -> CSVs
  python scripts/build_liquidation_link_plan.py --apply    # plan + write to staging

Outputs:
  internal-links/liquidation-cluster-plan.csv       proposed links (review this)
  internal-links/liquidation-cluster-rejected.csv   designed links with no natural anchor

Credentials read from .env only.
"""
import os, re, sys, csv, json, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from collections import Counter, defaultdict

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

APPLY = '--apply' in sys.argv

BANKS_FILE = 'internal-links/liquidation_anchor_banks.json'
GRAPH_FILE = 'internal-links/liquidation_link_graph.json'
PLAN_CSV   = 'internal-links/liquidation-cluster-plan.csv'
REJECT_CSV = 'internal-links/liquidation-cluster-rejected.csv'

GLOBAL_ANCHOR_CAP = 6   # max uses of any single anchor phrase, cluster-wide
NONEXACT_CATS = ['close_variants', 'process', 'risk_consequence', 'contextual_longtail']
CAT_ORDER = NONEXACT_CATS + ['exact']


# ---------------------------------------------------------------------------
# Anchor matching machinery
# ---------------------------------------------------------------------------

APOS_CLASS = r"(?:['‘’ʼ]|&#8217;|&#8216;|&#039;|&rsquo;|&lsquo;|&apos;)"
ELIGIBLE_BLOCK_RE = re.compile(
    r'<!-- wp:(paragraph|list)(?: \{[^}]*\})? -->(.*?)<!-- /wp:\1 -->', re.DOTALL)
INNER_EL_RE = re.compile(r'<(p|li)\b[^>]*>(.*?)</\1>', re.DOTALL | re.IGNORECASE)
A_TAG_RE    = re.compile(r'<a\b[^>]*>.*?</a>', re.DOTALL | re.IGNORECASE)
TAG_RE      = re.compile(r'<[^>]+>')


def build_anchor_regex(anchor):
    parts = []
    for ch in anchor.strip():
        if ch in "'‘’ʼ":
            parts.append(APOS_CLASS)
        elif ch.isspace():
            parts.append(r'\s+')
        else:
            parts.append(re.escape(ch))
    return re.compile(r'(?<![A-Za-z0-9])' + ''.join(parts) + r'(?![A-Za-z0-9])', re.IGNORECASE)


def norm(text):
    text = re.sub(r"['‘’ʼ]", "'", text)
    text = re.sub(r'&#8217;|&#8216;|&#039;|&rsquo;|&lsquo;|&apos;', "'", text)
    return re.sub(r'\s+', ' ', text).strip().lower()


def strip_internal_links(raw):
    """Unwrap internal <a> tags (root-relative or companydebt.com), keep the text.
    Makes --apply idempotent: cluster pages are reset before fresh links go in."""
    def repl(m):
        href  = m.group(1) if m.group(1) is not None else m.group(3)
        inner = m.group(2) if m.group(2) is not None else m.group(4)
        if href and (href.startswith('/') or 'companydebt.com' in href
                     or 'comdebstage' in href):
            return inner
        return m.group(0)
    pat = (r'<a\s[^>]*href="([^"]*)"[^>]*>(.*?)</a>'
           r'|<a\s[^>]*href=\'([^\']*)\'[^>]*>(.*?)</a>')
    return re.sub(pat, repl, raw, flags=re.DOTALL | re.IGNORECASE)


def context_ok(raw, s, e, target, phrase_owner):
    """Reject a match whose surrounding words form a phrase owned by a different
    target (e.g. 'voluntary liquidation' sitting inside 'Members' Voluntary
    Liquidation' — the longer, more-specific phrase wins)."""
    matched = norm(TAG_RE.sub('', raw[s:e]))
    pre  = norm(TAG_RE.sub(' ', raw[max(0, s - 60):s])).split()
    post = norm(TAG_RE.sub(' ', raw[e:e + 60])).split()
    extended = []
    if pre:
        extended.append(f'{pre[-1]} {matched}')
    if post:
        extended.append(f'{matched} {post[0]}')
    if pre and post:
        extended.append(f'{pre[-1]} {matched} {post[0]}')
    for phrase in extended:
        owner = phrase_owner.get(phrase)
        if owner and owner != target:
            return False
    return True


def get_paragraphs(raw):
    """Eligible paragraph/list-item text spans: list of (para_id, start, end)."""
    out = []
    for bm in ELIGIBLE_BLOCK_RE.finditer(raw):
        body_start = bm.start(2)
        for em in INNER_EL_RE.finditer(bm.group(2)):
            out.append((len(out), body_start + em.start(2), body_start + em.end(2)))
    return out


def clean_hits(rx, raw, ts, te):
    """Yield regex hits inside [ts,te) not enclosed by an <a> tag."""
    a_spans = [(m.start(), m.end()) for m in A_TAG_RE.finditer(raw, ts, te)]
    for hm in rx.finditer(raw, ts, te):
        s, e = hm.start(), hm.end()
        if not any(a_s <= s and e <= a_e for a_s, a_e in a_spans):
            yield s, e


def context_snippet(raw, s, e):
    before = TAG_RE.sub('', raw[max(0, s - 90):s])
    anchor = TAG_RE.sub('', raw[s:e])
    after  = TAG_RE.sub('', raw[e:e + 90])
    return re.sub(r'\s+', ' ', f'{before}[[{anchor}]]{after}').strip()


# ---------------------------------------------------------------------------
# WordPress REST client
# ---------------------------------------------------------------------------

def api_session():
    s = requests.Session()
    s.auth = (BA_USER, BA_PASS)
    s.headers['User-Agent'] = 'CompanyDebt-LinkPlan/1.0'
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
    for pat in (r'wpApiSettings[^}]+"nonce":"([a-f0-9]+)"', r'"nonce":"([a-f0-9]+)"'):
        m = re.search(pat, r.text)
        if m:
            return m.group(1)
    raise RuntimeError('Could not extract WP nonce')


def fetch_pages(session, nonce, wanted_paths):
    """Fetch raw content for the given set of page paths. Returns {path: {...}}."""
    pages = {}
    for post_type in ('posts', 'pages'):
        page = 1
        while True:
            r = session.get(
                f'{STAGING_URL}/wp-json/wp/v2/{post_type}',
                params={'per_page': 100, 'page': page, 'status': 'publish',
                        'context': 'edit', '_fields': 'id,slug,link,type,content'},
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
                if path in wanted_paths:
                    pages[path] = {
                        'id': it['id'], 'slug': it['slug'], 'type': it['type'],
                        'raw': strip_internal_links(it.get('content', {}).get('raw', '')),
                    }
            if len(batch) < 100:
                break
            page += 1
    return pages


def patch_content(session, post_type, post_id, raw, nonce):
    endpoint = 'posts' if post_type == 'post' else 'pages'
    r = session.post(f'{STAGING_URL}/wp-json/wp/v2/{endpoint}/{post_id}',
                     json={'content': raw},
                     headers={'X-WP-Nonce': nonce, 'Content-Type': 'application/json'},
                     timeout=30)
    r.raise_for_status()
    return r.status_code


# ---------------------------------------------------------------------------
# Planning
# ---------------------------------------------------------------------------

def plan_source(path, raw, banks, targets, anchor_use, phrase_owner):
    """Return (placements, rejections) for one source page."""
    paragraphs = get_paragraphs(raw)
    used_paras = set()
    placements = []
    rejections = []

    for target in targets:
        if target == path:
            continue
        bank = banks.get(target)
        if not bank:
            rejections.append({'target': target, 'reason': 'no_anchor_bank'})
            continue

        chosen = None
        for cat in CAT_ORDER:
            for anchor in bank.get(cat, []):
                if anchor_use[anchor] >= GLOBAL_ANCHOR_CAP:
                    continue
                rx = build_anchor_regex(anchor)
                for pid, ts, te in paragraphs:
                    if pid in used_paras:
                        continue
                    for s, e in clean_hits(rx, raw, ts, te):
                        if context_ok(raw, s, e, target, phrase_owner):
                            chosen = (target, anchor, cat, (s, e), pid)
                            break
                    if chosen:
                        break
                if chosen:
                    break
            if chosen:
                break

        if chosen:
            target, anchor, cat, (s, e), pid = chosen
            used_paras.add(pid)
            anchor_use[anchor] += 1
            placements.append({
                'target': target, 'anchor_text': raw[s:e], 'anchor_category': cat,
                'start': s, 'end': e, 'para_id': pid,
                'context': context_snippet(raw, s, e),
                'pos_pct': round(100 * pid / max(1, len(paragraphs))),
            })
        else:
            rejections.append({'target': target, 'reason': 'no_natural_anchor_in_copy'})

    return placements, rejections


def apply_placements(raw, rows):
    for p in sorted(rows, key=lambda x: x['_start'], reverse=True):
        s, e = p['_start'], p['_end']
        raw = raw[:s] + f'<a href="{p["target_url"]}">' + raw[s:e] + '</a>' + raw[e:]
    return raw


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    banks = {k: v for k, v in json.load(open(BANKS_FILE, encoding='utf-8')).items()
             if not k.startswith('_')}
    graph = {k: v for k, v in json.load(open(GRAPH_FILE, encoding='utf-8')).items()
             if not k.startswith('_')}

    mode = 'APPLY' if APPLY else 'PLAN (dry run)'
    print(f'=== Liquidation cluster link plan — {mode} ===\n')

    session = api_session()
    print('Logging in to staging...')
    wp_login(session)
    nonce = get_nonce(session)
    print(f'  nonce: {nonce[:8]}...\n')

    print(f'Fetching {len(graph)} source pages...')
    pages = fetch_pages(session, nonce, set(graph.keys()))
    print(f'  fetched {len(pages)}\n')

    missing = [p for p in graph if p not in pages]
    if missing:
        print(f'WARNING: {len(missing)} graph pages not found on staging:')
        for m in missing:
            print(f'  {m}')
        print()

    # phrase -> owning target, for the context guard (longest-phrase-wins)
    phrase_owner = {}
    for tgt, bank in banks.items():
        for cat in ('exact', 'close_variants'):
            for a in bank.get(cat, []):
                phrase_owner.setdefault(norm(a), tgt)

    anchor_use = Counter()
    all_placements = []   # rows for CSV
    all_rejections = []

    # Deterministic order: graph insertion order (hub -> core -> sub-spokes)
    for path in graph:
        if path not in pages:
            continue
        pg = pages[path]
        raw = pg['raw']
        if not raw:
            continue
        placements, rejections = plan_source(path, raw, banks, graph[path]['targets'],
                                             anchor_use, phrase_owner)
        live = 'https://www.companydebt.com' + path
        for p in placements:
            all_placements.append({
                'source_url': live, 'source_slug': pg['slug'],
                'group': graph[path].get('group', ''),
                'target_url': p['target'], 'anchor_text': p['anchor_text'],
                'anchor_category': p['anchor_category'],
                'exact_match': 'yes' if p['anchor_category'] == 'exact' else 'no',
                'page_position_pct': p['pos_pct'],
                'context_snippet': p['context'],
                '_id': pg['id'], '_type': pg['type'],
                '_start': p['start'], '_end': p['end'],
            })
        for r in rejections:
            all_rejections.append({
                'source_url': live, 'target_url': r['target'], 'reason': r['reason'],
            })

    # ----- write CSVs -----
    plan_cols = ['source_url', 'source_slug', 'group', 'target_url', 'anchor_text',
                 'anchor_category', 'exact_match', 'page_position_pct', 'context_snippet']
    with open(PLAN_CSV, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=plan_cols)
        w.writeheader()
        for row in all_placements:
            w.writerow({k: row[k] for k in plan_cols})

    with open(REJECT_CSV, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['source_url', 'target_url', 'reason'])
        w.writeheader()
        for row in all_rejections:
            w.writerow(row)

    # ----- summary -----
    designed = sum(len(graph[p]['targets']) for p in graph if p in pages)
    placed = len(all_placements)
    print('--- SUMMARY ---')
    print(f'Designed links:  {designed}')
    print(f'Placed:          {placed}  ({100*placed//max(1,designed)}%)')
    print(f'Dropped:         {len(all_rejections)}  (no natural anchor in copy)')

    by_target = Counter(r['target_url'] for r in all_placements)
    exact_by_target = Counter(r['target_url'] for r in all_placements if r['exact_match'] == 'yes')
    print('\nInbound links placed (top 12):')
    for t, n in by_target.most_common(12):
        ex = exact_by_target.get(t, 0)
        print(f'  {n:>3}  ({ex} exact, {100*ex//n}%)  {t}')

    cat_mix = Counter(r['anchor_category'] for r in all_placements)
    print('\nAnchor category mix (whole cluster):')
    for c in CAT_ORDER:
        n = cat_mix.get(c, 0)
        print(f'  {c}: {n}  ({100*n//max(1,placed)}%)')

    pages_no_links = [p for p in graph if p in pages
                      and not any(r['source_slug'] == pages[p]['slug'] for r in all_placements)]
    print(f'\nSource pages receiving 0 placed outbound links: {len(pages_no_links)}')

    print(f'\nOutputs:')
    print(f'  {PLAN_CSV}')
    print(f'  {REJECT_CSV}')

    # ----- apply -----
    if APPLY:
        print('\n--- APPLYING TO STAGING ---')
        by_page = defaultdict(list)
        for row in all_placements:
            by_page[(row['_id'], row['_type'], row['source_slug'])].append(row)
        patched = 0
        for (pid, ptype, slug), rows in by_page.items():
            src_path = next(p for p in graph if p in pages and pages[p]['id'] == pid)
            new_raw = apply_placements(pages[src_path]['raw'], rows)
            if new_raw != pages[src_path]['raw']:
                status = patch_content(session, ptype, pid, new_raw, nonce)
                patched += 1
                print(f'  [{slug}] +{len(rows)} link(s) (HTTP {status})')
                time.sleep(0.15)
        print(f'\nApplied to {patched} pages.')
    else:
        print('\nDry run. Review the plan CSV, then re-run with --apply.')


if __name__ == '__main__':
    main()
