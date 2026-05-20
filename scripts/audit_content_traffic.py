"""
Content audit: cross-reference WP article titles against GA4 traffic data.
Produces a delete/redirect/keep recommendation per article.
"""
import csv, re, json, subprocess, os, tempfile, html as html_mod, sys
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')
URL = os.getenv('WP_STAGING_URL').rstrip('/')
BA  = os.getenv('WP_BASIC_AUTH_USER') + ':' + os.getenv('WP_BASIC_AUTH_PASS')
WP_USER = os.getenv('WP_STAGING_USERNAME')
WP_APP_PASS = os.getenv('WP_STAGING_APP_PASSWORD')
CJ = tempfile.mktemp(suffix='.txt')

GA_CSV = r'C:\Users\piers\Downloads\Pages_and_screens_Page_title_and_screen_class.csv'


ARTICLE_IDS = [
    (59338, 'coffee-shop-owners-say-lattes-would-have-to-be-7-to-follow-energy-hikes', 'news'),
    (57275, '6000-fuel-hikes-taxi-sector', 'news'),
    (52948, 'leeds-dino-trail-collapses-into-administration', 'news'),
    (52598, 'failed-arena-television-leaves-trail-of-losses-and-faces-fraud-probe', 'news'),
    (52003, 'travel-firm-collapses-as-it-cannot-pay-refunds', 'news'),
    (49303, 'high-court-closes-insolvent-mini-bond-group', 'news'),
    (45894, 'bans-for-uk-directors-who-avoid-repaying-bounce-back-loans', 'news'),
    (22840, '80-homebase-stores-set-to-close-as-part-of-cva', 'news'),
    (23781, 'how-much-is-the-digital-sales-tax-going-to-affect-big-tech', 'news'),
    (20346, 'paradise-papers', 'news'),
    (46285, '39-of-hair-and-beauty-sector-still-furloughed', 'news'),
    (45670, '124-pints-to-save-the-pub', 'news'),
    (45349, 'can-manchester-united-get-out-from-under-its-455-5m-debt', 'news'),
    (44929, 'is-harley-davidson-heading-for-a-crash', 'news'),
    (20956, 'jamie-oliver-restaurant-restructure-london', 'news'),
    (20150, 'monarch-airline-insolvency', 'news'),
    (19967, 'kids-company-directors-face-disqualification-proceedings', 'news'),
    (13700, 'can-bradford-rugby-club-saved-liquidation', 'news'),
    (13688, '88-year-old-retailer-bhs-goes-company-liquidation', 'news'),
    (13606, 'pink-biscuit-manufacturer-rivington-biscuits-goes-company-administration', 'news'),
    (9951,  'insolvent-wine-scammers', 'news'),
    (9696,  'clothing-retailer-usc-close-30-unfashionable-stores', 'news'),
    (9608,  'disqualified-directors-jailed-continuing-control-companies', 'news'),
    (67900, 'find-out-why-the-transport-industry-is-prone-to-insolvency', 'news'),
    (9338,  'equestrian-failed-company-voluntary-arrangement-administration', 'news'),
    (20980, 'boulestin-avoids-closure', 'news'),
    (49767, 'cleaning-contractors', 'sector'),
    (77694, 'articles-insights-hub', 'hub'),
    (49778, 'construction', 'sector'),
    (49739, 'recruitment', 'sector'),
    (49727, 'restaurants', 'sector'),
    (49699, 'travel', 'sector'),
    (11269, 'common-causes-of-construction-insolvency', 'news'),
    (51774, 'gieves-hawkes-facing-liquidation', 'news'),
    (20594, 'how-will-carillions-insolvency-effect-its-supply-chain', 'news'),
    (10932, 'lengthy-disqualifications-for-four-directors-involved-in-vat-fraud', 'news'),
    (50021, 'scaffolder-censured-over-bounce-back-loan', 'news'),
    (50412, 'wayne-rooney-scores-21m-from-company-liquidation', 'news'),
    (47456, 'bespoke-kitchen-manufacturer', 'case_study'),
    (23483, 'creditors-voluntary-liquidation-with-phoenix', 'case_study'),
    (47414, 'freight-forwarder', 'case_study'),
    (23474, 'individual-voluntary-arrangement-with-new-limited-company', 'case_study'),
    (23462, 'individual-voluntary-arrangement', 'case_study'),
    (47479, 'online-travel-agent', 'case_study'),
    (23524, 'personal-guarantees', 'case_study'),
    (47462, 'pizza-restaurant', 'case_study'),
    (47401, 'plumbing', 'case_study'),
    (47466, 'recruitment-consultant', 'case_study'),
    (47470, 'womens-fashion-store', 'case_study'),
    (49717, 'retail', 'sector'),
    (55751, 'insolvency-rescue-fish-chip-sector', 'sector'),
    (52222, 'insolvency-rescue-solutions-for-garden-centers', 'sector'),
    (49810, 'property', 'sector'),
    (49831, 'manufacturing', 'sector'),
    (49820, 'professional-services', 'sector'),
    (49839, 'leisure', 'sector'),
    (49849, 'dry-cleaning-laundry', 'sector'),
    (49856, 'hotels', 'sector'),
    (49866, 'haulage', 'sector'),
    (49873, 'gyms', 'sector'),
    (49880, 'events', 'sector'),
    (49890, 'entertainment', 'sector'),
    (49898, 'energy', 'sector'),
    (49906, 'schools', 'sector'),
    (49706, 'taxi-companies', 'sector'),
    (49694, 'childcare', 'sector'),
    (49550, 'charity', 'sector'),
    (48758, 'automotive', 'sector'),
    (49488, 'carehomes', 'sector'),
    (47432, 'jeweller', 'case_study'),
    (67800, 'insolvencies-within-the-technology-sector', 'news'),
    (67805, 'poolmageddon-79-of-uk-pools-may-close-within-6-months', 'news'),
    (59226, 'will-the-energy-crisis-mean-the-end-for-britains-bakeries', 'news'),
    (46571, '12-year-ban-for-director-who-pocketed-covid-loan-cash', 'news'),
    (47487, 'hardware-maintenance', 'case_study'),
    (47392, 'pet-store', 'case_study'),
    (50894, 'asset-based-and-other-lenders', 'services_to'),
    (51087, 'creditors', 'services_to'),
    (50889, 'banks', 'services_to'),
    (50825, 'solicitors', 'services_to'),
    (50710, 'accountants', 'services_to'),
    (45481, 'covid-19-effects-on-cruise-industry', 'news'),
    (73803, 'british-cycle-sales-hit-39-year-low', 'news'),
    (47447, 'corporate-finance', 'case_study'),
    (47386, 'language-school', 'case_study'),
    (47499, 'subcontractor-agency', 'case_study'),
    (47495, 'hairdresser', 'case_study'),
    (47491, 'hoverboard-retailer', 'case_study'),
    (47484, 'it-consultancy', 'case_study'),
    (47474, 'seo-consultancy', 'case_study'),
    (47442, 'building-contractor', 'case_study'),
    (47436, 'plastering-company', 'case_study'),
    (47420, 'information-technology', 'case_study'),
    (23510, 'time-to-pay-and-creditor-voluntary-liquidation', 'case_study'),
    (23505, 'dissolution', 'case_study'),
    (50409, 'more-small-energy-providers-face-collapse-as-crisis-deepens', 'news'),
    (52832, 'crackdown-on-directors-who-close-companies-to-avoid-debts', 'news'),
    (52944, 'all-dishes-off-menu-for-dacampos-my-pasta-bar', 'news'),
    (51921, 'bobby-davros-business-goes-bust', 'news'),
    (52342, 'barnsley-shopping-centre-enters-receivership', 'news'),
]


def login():
    login_url = f'{URL}/wp-login.php?wpe-login=true'
    subprocess.run(['curl','-s','-u',BA,'-c',CJ,'-b',CJ, login_url], capture_output=True)
    subprocess.run(['curl','-s','-u',BA,'-c',CJ,'-b',CJ,
                    '--data-urlencode', f'log={WP_USER}',
                    '--data-urlencode', f'pwd={WP_APP_PASS}',
                    '-d','wp-submit=Log+In&testcookie=1','-L', login_url], capture_output=True)


def get_nonce():
    r = subprocess.run(['curl','-s','-u',BA,'-c',CJ,'-b',CJ, f'{URL}/wp-admin/'], capture_output=True)
    html = r.stdout.decode('utf-8', errors='replace')
    return (re.search(r'wpApiSettings[^}]+"nonce":"([a-f0-9]+)"', html)
            or re.search(r'"nonce":"([a-f0-9]+)"', html)).group(1)


def api(path, nonce):
    r = subprocess.run(['curl','-s','-u',BA,'-c',CJ,'-b',CJ,
                        '-H', f'X-WP-Nonce: {nonce}',
                        f'{URL}/wp-json/wp/v2{path}'], capture_output=True)
    return json.loads(r.stdout.decode('utf-8', errors='replace'))


def normalise(s):
    """Aggressive normalisation for fuzzy title matching."""
    s = html_mod.unescape(s or '')
    s = re.sub(r'<[^>]+>', '', s)
    s = s.lower()
    s = re.sub(r'[‘’“”–—\'""]', '', s)
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    # Remove common suffix noise
    for noise in ['case study creditors voluntary liquidation', 'case study cvl',
                  'case study', 'creditors voluntary liquidation', 'cvl',
                  'company debt ltd', 'company debt']:
        s = s.replace(noise, '')
    return re.sub(r'\s+', ' ', s).strip()


def load_ga_data():
    """Load GA4 CSV and return a list of (title, views, active_users, avg_engagement)."""
    rows = []
    with open(GA_CSV, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            if line.startswith('Page title'):
                continue
            r = next(csv.reader([line]))
            if len(r) < 5:
                continue
            try:
                title = r[0]
                views = int(r[1])
                users = int(r[2])
                eng = float(r[4]) if r[4] else 0.0
                rows.append({'title': title, 'views': views, 'users': users, 'eng': eng})
            except (ValueError, IndexError):
                continue
    return rows


def match_traffic(wp_title, ga_rows):
    """Find best matching GA row for a WP title. Returns dict with views/users or zeros."""
    if not wp_title:
        return {'views': 0, 'users': 0, 'eng': 0.0, 'matched_title': None}
    target = normalise(wp_title)
    # Try exact match on normalised
    for r in ga_rows:
        if normalise(r['title']) == target:
            return {'views': r['views'], 'users': r['users'], 'eng': r['eng'], 'matched_title': r['title']}
    # Try contains
    for r in ga_rows:
        nr = normalise(r['title'])
        if target in nr or nr in target:
            if len(target) > 15 and len(nr) > 15:
                return {'views': r['views'], 'users': r['users'], 'eng': r['eng'], 'matched_title': r['title']}
    return {'views': 0, 'users': 0, 'eng': 0.0, 'matched_title': None}


def recommend(article):
    cat = article['cat']
    views = article['views']
    users = article['users']
    eng = article['eng']
    # Sector pages: always KEEP regardless of traffic
    if cat == 'sector':
        return 'KEEP-REFRESH', 'Sector landing page; refresh content properly'
    if cat == 'hub':
        return 'KEEP', 'Hub page'
    if cat == 'services_to':
        return 'KEEP-LIGHT', 'Partner referral page'
    # Case studies
    if cat == 'case_study':
        if users < 5:
            return 'REVIEW-DELETE', f'Case study, {users} users in 12mo'
        return 'KEEP-LIGHT', f'Case study, {users} users'
    # News articles
    if cat == 'news':
        if users == 0:
            return 'DELETE', 'Zero traffic 12mo'
        if users < 10:
            return 'DELETE', f'Only {users} users in 12mo'
        if users < 50:
            return 'REDIRECT', f'{users} users; redirect to topical hub'
        if users < 200:
            return 'REVIEW-REFRESH', f'{users} users; worth proper rewrite or delete'
        # Higher traffic: worth refreshing
        return 'KEEP-REFRESH', f'{users} users; proper rewrite worth it'
    return 'REVIEW', 'Unclassified'


def main():
    print('Logging in to WP staging...')
    login()
    nonce = get_nonce()
    print('Logged in.\n')

    print('Loading GA4 data...')
    ga_rows = load_ga_data()
    print(f'  {len(ga_rows)} GA rows loaded\n')

    print('Fetching WP titles and cross-referencing...')
    results = []
    for i, (wp_id, slug, cat) in enumerate(ARTICLE_IDS, 1):
        p = api(f'/posts/{wp_id}', nonce)
        if 'id' not in p:
            p = api(f'/pages/{wp_id}', nonce)
        title = ''
        link = ''
        if 'id' in p:
            title = p.get('title', {}).get('rendered', '')
            title = html_mod.unescape(re.sub(r'<[^>]+>', '', title)).strip()
            link = p.get('link', '')
        traffic = match_traffic(title, ga_rows)
        results.append({
            'id': wp_id, 'slug': slug, 'cat': cat, 'title': title, 'link': link,
            **traffic,
        })
        if i % 20 == 0:
            print(f'  {i}/{len(ARTICLE_IDS)}')

    # Add recommendation
    for r in results:
        rec, reason = recommend(r)
        r['rec'] = rec
        r['reason'] = reason

    # Output sorted by recommendation severity then by users
    rec_order = {'DELETE': 0, 'REVIEW-DELETE': 1, 'REDIRECT': 2, 'REVIEW-REFRESH': 3,
                 'KEEP-LIGHT': 4, 'KEEP-REFRESH': 5, 'KEEP': 6, 'REVIEW': 7}
    results.sort(key=lambda x: (rec_order.get(x['rec'], 99), x['users']))

    out_path = r'C:\Users\piers\Projects\Company Debt Content System\content_audit.csv'
    with open(out_path, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['rec', 'cat', 'wp_id', 'slug', 'users_12mo', 'views_12mo', 'avg_eng_sec', 'reason', 'matched_ga_title', 'wp_title', 'link'])
        for r in results:
            w.writerow([r['rec'], r['cat'], r['id'], r['slug'], r['users'], r['views'],
                       round(r['eng'],1), r['reason'], r['matched_title'] or '', r['title'], r['link']])
    print(f'\nWrote {out_path}\n')

    # Summary
    from collections import Counter
    by_rec = Counter(r['rec'] for r in results)
    print('=' * 60)
    print('AUDIT SUMMARY')
    print('=' * 60)
    for rec in ['DELETE', 'REVIEW-DELETE', 'REDIRECT', 'REVIEW-REFRESH', 'KEEP-LIGHT', 'KEEP-REFRESH', 'KEEP', 'REVIEW']:
        n = by_rec.get(rec, 0)
        if n:
            print(f'  {rec:20} {n}')
    print()
    # Print the DELETE list specifically
    print('DELETE candidates (zero or near-zero traffic):')
    print('-' * 60)
    for r in results:
        if r['rec'] in ('DELETE', 'REVIEW-DELETE'):
            print(f'  [{r["users"]:>3} users] {r["slug"][:55]}')


if __name__ == '__main__':
    main()
