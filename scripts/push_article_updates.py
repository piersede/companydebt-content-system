"""
Push update sections to 5 articles on WP staging.
Finds each post by slug, appends update HTML, sets modified date to today.
"""
import subprocess, os, re, tempfile, json, sys
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

URL  = os.getenv('WP_STAGING_URL').rstrip('/')
BA   = os.getenv('WP_BASIC_AUTH_USER') + ':' + os.getenv('WP_BASIC_AUTH_PASS')
WP_USER     = os.getenv('WP_STAGING_USERNAME')
WP_APP_PASS = os.getenv('WP_STAGING_APP_PASSWORD')

COOKIE_JAR = tempfile.mktemp(suffix='.txt')

# ── Auth ──────────────────────────────────────────────────────────────────────

def login():
    login_url = f'{URL}/wp-login.php?wpe-login=true'
    # Prime test cookie
    subprocess.run(['curl','-s','-u',BA,'-c',COOKIE_JAR,'-b',COOKIE_JAR, login_url],
                   capture_output=True)
    # POST login
    subprocess.run([
        'curl','-s','-u',BA,'-c',COOKIE_JAR,'-b',COOKIE_JAR,
        '--data-urlencode', f'log={WP_USER}',
        '--data-urlencode', f'pwd={WP_APP_PASS}',
        '-d', 'wp-submit=Log+In&redirect_to=%2Fwp-admin%2F&testcookie=1',
        '-L', login_url
    ], capture_output=True)
    with open(COOKIE_JAR) as f:
        if 'wordpress_logged_in' not in f.read():
            print('ERROR: WP login failed'); sys.exit(1)
    print('Logged in OK')


def get_nonce():
    # Use -c too so the admin request refreshes any session cookies
    r = subprocess.run(
        ['curl','-s','-u',BA,'-c',COOKIE_JAR,'-b',COOKIE_JAR, f'{URL}/wp-admin/'],
        capture_output=True)
    html = r.stdout.decode('utf-8', errors='replace')
    # Prefer the wpApiSettings REST nonce over generic nonce patterns
    m = re.search(r'wpApiSettings[^}]+\"nonce\":\"([a-f0-9]+)\"', html) \
     or re.search(r'"nonce":"([a-f0-9]+)"', html)
    if not m:
        print('ERROR: Could not get REST nonce'); sys.exit(1)
    print(f'Nonce OK: {m.group(1)[:8]}...')
    return m.group(1)


def curl_api(method, path, nonce, data=None):
    cmd = ['curl','-s','-u',BA,'-c',COOKIE_JAR,'-b',COOKIE_JAR,
           '-H', f'X-WP-Nonce: {nonce}',
           '-H', 'Content-Type: application/json',
           '-X', method,
           f'{URL}/wp-json/wp/v2{path}']
    if data:
        cmd += ['-d', json.dumps(data)]
    r = subprocess.run(cmd, capture_output=True)
    return json.loads(r.stdout.decode('utf-8', errors='replace'))


# ── Update blocks (no m-dashes) ───────────────────────────────────────────────

UPDATES = {
    'more-small-energy-providers-face-collapse-as-crisis-deepens': {
        'html': """
<div class="editor-update-block">
<h3>What happened next</h3>
<p>The prediction that the market would shrink from around 70 suppliers to roughly 10 proved broadly accurate, though the final toll was sharper than most expected. By May 2022, 29 UK energy suppliers had collapsed, affecting close to four million domestic customers. Most were transferred via the Supplier of Last Resort process. Bulb Energy (the sixth-largest supplier, mentioned above as seeking emergency funding) entered special administration in November 2021, the largest energy company failure in UK history. It remained in administration for 13 months, backed by an estimated &pound;2.2 billion in taxpayer support, before Octopus Energy acquired its customer base in December 2022.</p>
<p>The consolidation has stuck. As of late 2025, around 18 active domestic suppliers remain, down from over 70 at the market&#8217;s peak. Six companies now hold 91% of market share.</p>
<p>For consumers, stabilisation has been partial at best. The Ofgem price cap currently stands at &pound;1,641 per year (April to June 2026), still around 35% higher than pre-crisis levels. Consumer energy debt reached &pound;4.43 billion by mid-2025, up 71% in two years, with 2.44 million households carrying arrears.</p>
<p>The crisis that looked, in autumn 2021, like a temporary supply shock turned out to reshape the market permanently. Smaller suppliers with thin hedging and no buffer capacity were simply not viable at scale. That lesson has not been forgotten by the regulator.</p>
<p><em>Note: Kwasi Kwarteng is quoted above in his capacity as Business Secretary at the time of original publication (autumn 2021). He left the role in September 2022.</em></p>
</div>
""",
        'original_date': '2021-11-01T00:00:00',
    },
    'crackdown-on-directors-who-close-companies-to-avoid-debts': {
        'html': """
<div class="editor-update-block">
<h3>What happened next</h3>
<p>The Act received Royal Assent on 15 December 2021 and the Insolvency Service moved quickly to use the new powers. For the first time, investigators could pursue directors of dissolved companies, not just those in active insolvency proceedings. Before this legislation, dissolving a company was a credible escape route: once the company was struck off, the Insolvency Service had no standing to act. That gap is now closed.</p>
<p>The primary focus has been bounce-back loan abuse. Thousands of directors received pandemic loans, dissolved their companies, and walked away. The new powers mean the Insolvency Service can now follow them. Cases have resulted in disqualifications of up to 15 years, and in serious cases, criminal prosecution and court-ordered compensation.</p>
<p>Whether the legislation has fully deterred the behaviour it targeted is a fair question. Phoenixing and informal dissolution remain common insolvency risks, and the Insolvency Service has limited capacity to pursue every case. But the legal exposure is now real in a way it was not before 2022. Directors who dissolved companies during the pandemic to sidestep their creditors are no longer untouchable.</p>
<p><em>Note: Kwasi Kwarteng is quoted above as Business Secretary. He left the role in September 2022.</em></p>
</div>
""",
        'original_date': '2021-12-15T00:00:00',
    },
    'all-dishes-off-menu-for-dacampos-my-pasta-bar': {
        'html': """
<div class="editor-update-block">
<h3>What happened next</h3>
<p>My Pasta Bar was not the end of it. The wider Gino D&#8217;Acampo restaurant operation, trading as Worldwide Restaurants, subsequently entered liquidation. Gino D&#8217;Acampo Restaurants LLP was dissolved at Companies House in March 2023. The full chain, not just the pasta concept, is gone.</p>
<p>The article&#8217;s reading of London&#8217;s changed office landscape proved accurate. City footfall never fully recovered to pre-pandemic levels. The workers who once filled restaurant covers from Monday to Friday at lunchtime are now in the office two or three days a week, if that, and spending differently when they are. Operators who built their business around a captive office crowd have had to adapt or close.</p>
<p>UK restaurant insolvencies hit record highs in 2023 and 2024, driven by the same combination of reduced footfall, higher food and energy costs, and wage pressure. The hospitality sector is smaller and more cautious than it was before Covid. The era of rapid city-centre restaurant expansion that D&#8217;Acampo&#8217;s chain represented belongs to a different set of assumptions about how people work.</p>
</div>
""",
        'original_date': '2022-01-10T00:00:00',
    },
    'bobby-davros-business-goes-bust': {
        'html': """
<div class="editor-update-block">
<h3>What happened next</h3>
<p>Davro has returned to performing. He appeared in pantomime from the 2022 season and has continued to take stage work since. The candour in his original statement, that there was simply no work and he could not earn, reflected a situation that was real but also temporary. The live entertainment and touring sector recovered strongly from 2022 onwards as venues reopened and audiences came back.</p>
<p>His company structure, a personal service company holding performance income, is standard across the entertainment industry and was not the problem. The problem was a complete income stop with no buffer. Many similar companies folded during the same period for the same reason.</p>
<p>The pandemic exposed how exposed a single-director PSC is when income stops without warning. There is no redundancy safety net, no furlough equivalent for director-shareholders who take dividends rather than salary, and no creditor patience once HMRC and bank obligations mount. Some directors were able to access director redundancy claims through the Insolvency Service. Others wound up and started again. The underlying vulnerability of the structure has not changed.</p>
</div>
""",
        'original_date': '2021-06-01T00:00:00',
    },
    'barnsley-shopping-centre-enters-receivership': {
        'html': """
<div class="editor-update-block">
<h3>What happened next</h3>
<p>The Glass Works opened in September 2022, bringing Next, TK Maxx, and a range of food and leisure tenants into the town centre on the terms the Alhambra&#8217;s older units could not match. The council&#8217;s bet on new-build retail proved correct in footfall terms.</p>
<p>The Alhambra&#8217;s fate reflects a pattern repeated across secondary UK retail. An 1980s-era shopping centre, facing a newer rival with better rents and better fit-out, cannot compete on equal terms. Receivership is often the point at which a building either finds a buyer with a plan, usually for mixed-use redevelopment, or enters a managed decline. At the time of writing the Alhambra continues to trade, though with a reduced tenant roster.</p>
<p>The wider picture for UK shopping centres is one of sustained consolidation. Locations that cannot anchor a food, leisure, or services offer alongside retail are under structural pressure regardless of ownership. The prediction in the original article, that up to 70 centres may need to close, is tracking towards reality: property analysts have consistently flagged oversupply in secondary and tertiary retail since 2019, and the pace of closures and conversions has only increased since.</p>
</div>
""",
        'original_date': '2021-09-01T00:00:00',
    },
}

# ── Main ──────────────────────────────────────────────────────────────────────

def find_post(slug, nonce):
    for pt in ['posts', 'pages']:
        data = curl_api('GET', f'/{pt}?slug={slug}&per_page=1', nonce)
        if isinstance(data, list) and data:
            return data[0], pt
    # Try all types
    types = curl_api('GET', '/types', nonce)
    skip = {'attachment','nav_menu_item','wp_block','wp_template','wp_template_part',
            'wp_navigation','wp_font_family','wp_font_face'}
    for pt_key, pt_info in types.items():
        if pt_key in skip or pt_key in ('posts','pages'):
            continue
        rest_base = pt_info.get('rest_base', pt_key) if isinstance(pt_info, dict) else pt_key
        data = curl_api('GET', f'/{rest_base}?slug={slug}&per_page=1', nonce)
        if isinstance(data, list) and data:
            return data[0], rest_base
    return None, None


def append_update(current_content, update_html):
    """Append update block before closing article tag or at end."""
    if '</article>' in current_content:
        return current_content.replace('</article>', update_html + '</article>', 1)
    return current_content + update_html


def run():
    login()
    nonce = get_nonce()

    results = []
    for slug, update in UPDATES.items():
        print(f'\nProcessing: {slug}')
        post, post_type = find_post(slug, nonce)
        if not post:
            print(f'  ERROR: Post not found'); results.append((slug, 'NOT FOUND', '')); continue

        post_id = post['id']
        current_date = post.get('date', '')
        current_content = post.get('content', {}).get('rendered', '')
        print(f'  Found: id={post_id} type={post_type} date={current_date[:10]}')

        # Check if update block already exists
        if 'editor-update-block' in current_content:
            print(f'  SKIP: Update block already present')
            results.append((slug, 'ALREADY UPDATED', post.get('link','')))
            continue

        new_content = append_update(current_content, update['html'])

        payload = {
            'content': new_content,
            'date': update['original_date'],   # restore approximate original date
        }

        resp = curl_api('POST', f'/{post_type}/{post_id}', nonce, payload)
        if 'id' in resp:
            link = resp.get('link', '')
            modified = resp.get('modified', '')[:10]
            print(f'  Updated OK. Modified: {modified}  Link: {link}')
            results.append((slug, 'OK', link))
        else:
            print(f'  ERROR: {resp.get("message", resp)}')
            results.append((slug, 'ERROR', str(resp)))

    print('\n\nSummary:')
    print('-' * 60)
    for slug, status, link in results:
        print(f'  {status:15}  {slug[:45]}')
        if link and status == 'OK':
            print(f'               {link}')


if __name__ == '__main__':
    run()
