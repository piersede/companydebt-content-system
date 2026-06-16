"""
Delete 66 articles on WP staging — sends them to trash (recoverable).
Keeps: 124-pints-to-save-the-pub, how-will-carillions-insolvency-effect-its-supply-chain, paradise-papers
"""
import subprocess, os, re, json, tempfile, sys
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')

URL = os.getenv('WP_STAGING_URL').rstrip('/')
BA  = os.getenv('WP_BASIC_AUTH_USER') + ':' + os.getenv('WP_BASIC_AUTH_PASS')
WP_USER = os.getenv('WP_STAGING_USERNAME')
WP_APP_PASS = os.getenv('WP_STAGING_APP_PASSWORD')
CJ = tempfile.mktemp(suffix='.txt')

KEEP_SLUGS = {
    '124-pints-to-save-the-pub',
    'how-will-carillions-insolvency-effect-its-supply-chain',
    'paradise-papers',
}

DELETE_LIST = [
    # ── Case studies (26) ────────────────────────────────────────
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
    (47432, 'jeweller', 'case_study'),
    (47487, 'hardware-maintenance', 'case_study'),
    (47392, 'pet-store', 'case_study'),
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

    # ── News articles (40 — all news except keep list) ───────────
    (59338, 'coffee-shop-owners-say-lattes-would-have-to-be-7-to-follow-energy-hikes', 'news'),
    (57275, '6000-fuel-hikes-taxi-sector', 'news'),
    (52948, 'leeds-dino-trail-collapses-into-administration', 'news'),
    (52598, 'failed-arena-television-leaves-trail-of-losses-and-faces-fraud-probe', 'news'),
    (52003, 'travel-firm-collapses-as-it-cannot-pay-refunds', 'news'),
    (49303, 'high-court-closes-insolvent-mini-bond-group', 'news'),
    (45894, 'bans-for-uk-directors-who-avoid-repaying-bounce-back-loans', 'news'),
    (22840, '80-homebase-stores-set-to-close-as-part-of-cva', 'news'),
    (23781, 'how-much-is-the-digital-sales-tax-going-to-affect-big-tech', 'news'),
    (46285, '39-of-hair-and-beauty-sector-still-furloughed', 'news'),
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
    (11269, 'common-causes-of-construction-insolvency', 'news'),
    (51774, 'gieves-hawkes-facing-liquidation', 'news'),
    (10932, 'lengthy-disqualifications-for-four-directors-involved-in-vat-fraud', 'news'),
    (50021, 'scaffolder-censured-over-bounce-back-loan', 'news'),
    (50412, 'wayne-rooney-scores-21m-from-company-liquidation', 'news'),
    (67800, 'insolvencies-within-the-technology-sector', 'news'),
    (67805, 'poolmageddon-79-of-uk-pools-may-close-within-6-months', 'news'),
    (59226, 'will-the-energy-crisis-mean-the-end-for-britains-bakeries', 'news'),
    (46571, '12-year-ban-for-director-who-pocketed-covid-loan-cash', 'news'),
    (45481, 'covid-19-effects-on-cruise-industry', 'news'),
    (73803, 'british-cycle-sales-hit-39-year-low', 'news'),
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


def delete_post(wp_id, nonce):
    # No ?force=true → goes to trash, recoverable from WP admin
    cmd = ['curl','-s','-u',BA,'-c',CJ,'-b',CJ,
           '-H', f'X-WP-Nonce: {nonce}',
           '-X','DELETE',
           f'{URL}/wp-json/wp/v2/posts/{wp_id}']
    r = subprocess.run(cmd, capture_output=True)
    try:
        return json.loads(r.stdout.decode('utf-8', errors='replace'))
    except Exception:
        return {'raw': r.stdout.decode('utf-8', errors='replace')[:200]}


def main():
    print('Verifying no KEEP slugs in delete list...')
    for wp_id, slug, cat in DELETE_LIST:
        if slug in KEEP_SLUGS:
            print(f'ABORT: KEEP slug "{slug}" found in delete list!')
            sys.exit(1)
    print(f'  Clean. {len(DELETE_LIST)} articles to trash.\n')

    print('Logging in...')
    login()
    nonce = get_nonce()
    print(f'  Nonce: {nonce[:8]}...\n')

    print(f'Trashing {len(DELETE_LIST)} articles...\n')
    ok = 0
    failed = []
    for i, (wp_id, slug, cat) in enumerate(DELETE_LIST, 1):
        resp = delete_post(wp_id, nonce)
        status = resp.get('status', resp.get('code', '?'))
        if status == 'trash' or (isinstance(resp.get('previous'), dict) and resp['previous'].get('status') in ('publish','trash')):
            print(f'  [{i:>2}/{len(DELETE_LIST)}] {slug[:55]:55} TRASHED')
            ok += 1
        else:
            print(f'  [{i:>2}/{len(DELETE_LIST)}] {slug[:55]:55} ERROR ({status})')
            failed.append((slug, status))

    print(f'\n{"=" * 60}\nSummary:\n  Trashed:  {ok}\n  Failed:   {len(failed)}')
    if failed:
        for slug, err in failed:
            print(f'  FAIL: {slug} ({err})')


if __name__ == '__main__':
    main()
