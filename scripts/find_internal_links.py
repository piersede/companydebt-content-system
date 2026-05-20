"""
Find internal links across all published WP content that point to any of the 66 trashed article slugs.
Output: a report grouped by source page → which dead URLs it links to.
"""
import subprocess, os, re, json, tempfile, csv
from dotenv import load_dotenv
from html import unescape
load_dotenv(dotenv_path='.env')

URL = os.getenv('WP_STAGING_URL').rstrip('/')
BA  = os.getenv('WP_BASIC_AUTH_USER') + ':' + os.getenv('WP_BASIC_AUTH_PASS')
WP_USER = os.getenv('WP_STAGING_USERNAME')
WP_APP_PASS = os.getenv('WP_STAGING_APP_PASSWORD')
CJ = tempfile.mktemp(suffix='.txt')

# All trashed slugs (66)
TRASHED_SLUGS = [
    # Case studies (26)
    'bespoke-kitchen-manufacturer','creditors-voluntary-liquidation-with-phoenix',
    'freight-forwarder','individual-voluntary-arrangement-with-new-limited-company',
    'individual-voluntary-arrangement','online-travel-agent','personal-guarantees',
    'pizza-restaurant','plumbing','recruitment-consultant','womens-fashion-store',
    'jeweller','hardware-maintenance','pet-store','corporate-finance','language-school',
    'subcontractor-agency','hairdresser','hoverboard-retailer','it-consultancy',
    'seo-consultancy','building-contractor','plastering-company','information-technology',
    'time-to-pay-and-creditor-voluntary-liquidation','dissolution',
    # News (40)
    'coffee-shop-owners-say-lattes-would-have-to-be-7-to-follow-energy-hikes',
    '6000-fuel-hikes-taxi-sector','leeds-dino-trail-collapses-into-administration',
    'failed-arena-television-leaves-trail-of-losses-and-faces-fraud-probe',
    'travel-firm-collapses-as-it-cannot-pay-refunds',
    'high-court-closes-insolvent-mini-bond-group',
    'bans-for-uk-directors-who-avoid-repaying-bounce-back-loans',
    '80-homebase-stores-set-to-close-as-part-of-cva',
    'how-much-is-the-digital-sales-tax-going-to-affect-big-tech',
    '39-of-hair-and-beauty-sector-still-furloughed',
    'can-manchester-united-get-out-from-under-its-455-5m-debt',
    'is-harley-davidson-heading-for-a-crash',
    'jamie-oliver-restaurant-restructure-london',
    'monarch-airline-insolvency',
    'kids-company-directors-face-disqualification-proceedings',
    'can-bradford-rugby-club-saved-liquidation',
    '88-year-old-retailer-bhs-goes-company-liquidation',
    'pink-biscuit-manufacturer-rivington-biscuits-goes-company-administration',
    'insolvent-wine-scammers','clothing-retailer-usc-close-30-unfashionable-stores',
    'disqualified-directors-jailed-continuing-control-companies',
    'find-out-why-the-transport-industry-is-prone-to-insolvency',
    'equestrian-failed-company-voluntary-arrangement-administration',
    'boulestin-avoids-closure','common-causes-of-construction-insolvency',
    'gieves-hawkes-facing-liquidation',
    'lengthy-disqualifications-for-four-directors-involved-in-vat-fraud',
    'scaffolder-censured-over-bounce-back-loan',
    'wayne-rooney-scores-21m-from-company-liquidation',
    'insolvencies-within-the-technology-sector',
    'poolmageddon-79-of-uk-pools-may-close-within-6-months',
    'will-the-energy-crisis-mean-the-end-for-britains-bakeries',
    '12-year-ban-for-director-who-pocketed-covid-loan-cash',
    'covid-19-effects-on-cruise-industry',
    'british-cycle-sales-hit-39-year-low',
    'more-small-energy-providers-face-collapse-as-crisis-deepens',
    'crackdown-on-directors-who-close-companies-to-avoid-debts',
    'all-dishes-off-menu-for-dacampos-my-pasta-bar',
    'bobby-davros-business-goes-bust',
    'barnsley-shopping-centre-enters-receivership',
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
    cmd = ['curl','-s','-u',BA,'-c',CJ,'-b',CJ,
           '-H', f'X-WP-Nonce: {nonce}',
           f'{URL}/wp-json/wp/v2{path}']
    r = subprocess.run(cmd, capture_output=True)
    try:
        return json.loads(r.stdout.decode('utf-8', errors='replace'))
    except Exception:
        return []

def fetch_all(post_type, nonce):
    """Paginate through a post type fetching id, slug, link, content."""
    out = []
    page = 1
    while True:
        batch = api(f'/{post_type}?per_page=100&page={page}&status=publish&_fields=id,slug,link,content', nonce)
        if not isinstance(batch, list) or not batch:
            break
        out.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return out


def find_links(content_html, trashed_set):
    """Find all href attributes pointing to a trashed slug."""
    found = []
    # Match href="...slug..." where slug is anywhere in the URL path
    for m in re.finditer(r'href=["\']([^"\']+)["\']', content_html):
        href = unescape(m.group(1))
        # Skip external links not on our domain
        if 'companydebt.com' not in href and not href.startswith('/') and not href.startswith('http'):
            continue
        # Get the path portion
        path = href.split('?')[0].split('#')[0]
        # Extract slug — last non-empty segment
        segs = [s for s in path.rstrip('/').split('/') if s]
        if not segs:
            continue
        last = segs[-1]
        if last in trashed_set:
            found.append({'href': href, 'slug': last})
    return found


def main():
    trashed_set = set(TRASHED_SLUGS)
    print(f'Scanning for internal links to {len(trashed_set)} trashed slugs...\n')

    login()
    nonce = get_nonce()
    print('Logged in.\n')

    all_content = []
    for post_type in ['posts','pages']:
        print(f'Fetching {post_type}...')
        items = fetch_all(post_type, nonce)
        print(f'  {len(items)} items')
        all_content.extend([(post_type, it) for it in items])

    print(f'\nScanning {len(all_content)} pages for dead internal links...\n')
    findings = []
    for post_type, item in all_content:
        content = item.get('content',{}).get('rendered','')
        links = find_links(content, trashed_set)
        if links:
            findings.append({
                'source_id': item['id'],
                'source_slug': item['slug'],
                'source_link': item.get('link',''),
                'source_type': post_type,
                'dead_links': links,
            })

    # Output
    print(f'Found {len(findings)} source pages with dead internal links.\n')
    print('=' * 80)
    by_dead_slug = {}
    for f in findings:
        for dl in f['dead_links']:
            by_dead_slug.setdefault(dl['slug'], []).append({
                'source_slug': f['source_slug'],
                'source_link': f['source_link'],
                'href': dl['href'],
            })
    print(f'\nDead slugs being linked to ({len(by_dead_slug)}):')
    for dead_slug, sources in sorted(by_dead_slug.items(), key=lambda x: -len(x[1])):
        print(f'  [{len(sources):>2} link(s)] {dead_slug}')

    # CSV output
    out = r'C:\Users\piers\Projects\Company Debt Content System\dead_links_report.csv'
    with open(out, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['source_id','source_slug','source_type','source_link','dead_slug','dead_href'])
        for finding in findings:
            for dl in finding['dead_links']:
                w.writerow([finding['source_id'], finding['source_slug'], finding['source_type'],
                           finding['source_link'], dl['slug'], dl['href']])
    print(f'\nReport: {out}')


if __name__ == '__main__':
    main()
