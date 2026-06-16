"""
Generate 410 Gone rules for all 66 trashed articles.
Outputs:
  - .htaccess block (Apache syntax)
  - Redirection plugin import CSV (WP Engine compatible)
  - Plain URL list
"""
import subprocess, os, re, json, tempfile, csv
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')

URL = os.getenv('WP_STAGING_URL').rstrip('/')
BA  = os.getenv('WP_BASIC_AUTH_USER') + ':' + os.getenv('WP_BASIC_AUTH_PASS')
WP_USER = os.getenv('WP_STAGING_USERNAME')
WP_APP_PASS = os.getenv('WP_STAGING_APP_PASSWORD')
CJ = tempfile.mktemp(suffix='.txt')

TRASHED_IDS = [
    47456, 23483, 47414, 23474, 23462, 47479, 23524, 47462, 47401, 47466,
    47470, 47432, 47487, 47392, 47447, 47386, 47499, 47495, 47491, 47484,
    47474, 47442, 47436, 47420, 23510, 23505,
    59338, 57275, 52948, 52598, 52003, 49303, 45894, 22840, 23781, 46285,
    45349, 44929, 20956, 20150, 19967, 13700, 13688, 13606, 9951,  9696,
    9608,  67900, 9338,  20980, 11269, 51774, 10932, 50021, 50412, 67800,
    67805, 59226, 46571, 45481, 73803, 50409, 52832, 52944, 51921, 52342,
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
        return None


def main():
    login()
    nonce = get_nonce()
    print('Fetching URLs for trashed posts...\n')

    urls = []
    for wp_id in TRASHED_IDS:
        # status=trash needed to query trashed posts; need edit context
        p = api(f'/posts/{wp_id}?context=edit&status=trash', nonce)
        if p and 'link' in p:
            link = p['link']
            slug = p.get('slug', '')
            # Trashed posts have slug like "slug__trashed" - clean it
            if slug.endswith('__trashed'):
                slug = slug[:-9]
            # Extract path from URL (strip domain, query, anchor)
            path = re.sub(r'^https?://[^/]+', '', link).split('?')[0].split('#')[0]
            # Trashed posts may have ?preview= or modified URL - reconstruct from slug
            if '__trashed' in path or '?' in link:
                # Use the post type and slug to reconstruct
                # News articles → /articles/SLUG/
                # Case studies → varied paths
                pass
            urls.append({'id': wp_id, 'slug': slug, 'path': path, 'link': link})
            print(f'  id={wp_id:>5} {path}')
        else:
            print(f'  id={wp_id:>5} NOT FOUND')

    # Known production paths for case studies that have category prefixes
    # We need to override the WP-returned paths if they don't match the live site
    # From the dead_links_report.csv we know these paths:
    known_paths = {
        'personal-guarantees': '/case-studies/travel-agency/personal-guarantees/',
        'online-travel-agent': '/case-studies/travel-agency/online-travel-agent/',
        'time-to-pay-and-creditor-voluntary-liquidation': '/case-studies/time-to-pay-and-creditor-voluntary-liquidation/',
        'plastering-company': '/case-studies/property-construction/plastering-company/',
        'building-contractor': '/case-studies/property-and-construction/building-contractor/',
        'dissolution': '/case-studies/dissolution/',
        'corporate-finance': '/case-studies/professional-services-case-studies/corporate-finance/',
        'bespoke-kitchen-manufacturer': '/case-studies/professional-services-case-studies/bespoke-kitchen-manufacturer/',
        'recruitment-consultant': '/case-studies/professional-services-case-studies/recruitment-consultant/',
        'creditors-voluntary-liquidation-with-phoenix': '/case-studies/creditors-voluntary-liquidation-with-phoenix/',
        'individual-voluntary-arrangement-with-new-limited-company': '/case-studies/logistics/individual-voluntary-arrangement-with-new-limited-company/',
        'individual-voluntary-arrangement': '/case-studies/individual-voluntary-arrangement/',
        'pet-store': '/case-studies/retail/pet-store/',
        'jeweller': '/case-studies/retail/jeweller/',
        'womens-fashion-store': '/case-studies/retail/womens-fashion-store/',
        'hoverboard-retailer': '/case-studies/retail/hoverboard-retailer/',
        'language-school': '/case-studies/education/language-school/',
        'freight-forwarder': '/case-studies/freight-forwarder/',
        'information-technology': '/case-studies/it/information-technology/',
        'seo-consultancy': '/case-studies/it/seo-consultancy/',
        'it-consultancy': '/case-studies/it/it-consultancy/',
        'hardware-maintenance': '/case-studies/it/hardware-maintenance/',
        'pizza-restaurant': '/case-studies/restaurants-leisure/pizza-restaurant/',
        'hairdresser': '/case-studies/restaurants-leisure/hairdresser/',
        'subcontractor-agency': '/case-studies/subcontractor-agency/',
        'plumbing': '/case-studies/property-and-construction/plumbing/',
    }

    # Default path generation: news → /articles/SLUG/, case studies → /case-studies/SLUG/
    # Trashed posts return "/" for link, so we always reconstruct from slug
    for u in urls:
        if u['slug'] in known_paths:
            u['path'] = known_paths[u['slug']]
        elif u['path'] in ('/', '') or u['path'].endswith('__trashed/') or '__trashed' in u['path']:
            # Fall back to /articles/SLUG/ for news articles
            u['path'] = f'/articles/{u["slug"]}/'

    # Write the three output files
    base_dir = r'C:\Users\piers\Projects\Company Debt Content System'

    # 1. .htaccess
    with open(os.path.join(base_dir, '410_rules.htaccess'), 'w', encoding='utf-8') as f:
        f.write('# 410 Gone rules for trashed articles\n')
        f.write('# Place inside <IfModule mod_alias.c> or as standalone Redirect directives\n\n')
        for u in urls:
            f.write(f'Redirect 410 {u["path"]}\n')

    # 2. Redirection plugin CSV (URL, target, status)
    with open(os.path.join(base_dir, '410_rules_redirection_plugin.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['source','target','code','type','match_type','regex','status'])
        for u in urls:
            w.writerow([u['path'], '', '410', 'url', 'url', 'false', 'enabled'])

    # 3. Plain URL list
    with open(os.path.join(base_dir, '410_url_list.txt'), 'w', encoding='utf-8') as f:
        for u in urls:
            f.write(u['path'] + '\n')

    print(f'\nGenerated:')
    print(f'  410_rules.htaccess               ({len(urls)} rules)')
    print(f'  410_rules_redirection_plugin.csv ({len(urls)} rules)')
    print(f'  410_url_list.txt                 ({len(urls)} URLs)')


if __name__ == '__main__':
    main()
