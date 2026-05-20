"""
Remove the editor-update-block divs from the 3 kept articles.
"""
import subprocess, os, re, json, tempfile, sys
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')

URL = os.getenv('WP_STAGING_URL').rstrip('/')
BA  = os.getenv('WP_BASIC_AUTH_USER') + ':' + os.getenv('WP_BASIC_AUTH_PASS')
WP_USER = os.getenv('WP_STAGING_USERNAME')
WP_APP_PASS = os.getenv('WP_STAGING_APP_PASSWORD')
CJ = tempfile.mktemp(suffix='.txt')

KEEP_ARTICLES = [
    (45670, '124-pints-to-save-the-pub'),
    (20594, 'how-will-carillions-insolvency-effect-its-supply-chain'),
    (20346, 'paradise-papers'),
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

def api_get(wp_id, nonce):
    cmd = ['curl','-s','-u',BA,'-c',CJ,'-b',CJ,
           '-H', f'X-WP-Nonce: {nonce}',
           '-H', 'Accept: application/json',
           f'{URL}/wp-json/wp/v2/posts/{wp_id}?context=edit']
    r = subprocess.run(cmd, capture_output=True)
    return json.loads(r.stdout.decode('utf-8', errors='replace'))

def api_post(wp_id, nonce, payload):
    cmd = ['curl','-s','-u',BA,'-c',CJ,'-b',CJ,
           '-H', f'X-WP-Nonce: {nonce}',
           '-H', 'Content-Type: application/json',
           '-X', 'POST',
           '-d', json.dumps(payload),
           f'{URL}/wp-json/wp/v2/posts/{wp_id}']
    r = subprocess.run(cmd, capture_output=True)
    return json.loads(r.stdout.decode('utf-8', errors='replace'))


def strip_update_block(content):
    """Remove all <div class="editor-update-block">...</div> blocks."""
    # Non-greedy match for the div - the block we appended ends before </article> or end of content
    pattern = re.compile(
        r'\n?<div class="editor-update-block">.*?</div>\n?',
        re.DOTALL
    )
    cleaned, n = pattern.subn('', content)
    return cleaned, n


def main():
    print('Logging in...')
    login()
    nonce = get_nonce()
    print(f'  Nonce: {nonce[:8]}...\n')

    for wp_id, slug in KEEP_ARTICLES:
        print(f'Processing: {slug}')
        post = api_get(wp_id, nonce)
        if 'id' not in post:
            print(f'  ERROR: could not fetch (resp: {post})')
            continue
        # Use raw content for editing so we don't lose anything
        raw = post.get('content', {}).get('raw') or post.get('content', {}).get('rendered', '')
        if 'editor-update-block' not in raw:
            print(f'  No update block found, skipping')
            continue
        cleaned, n = strip_update_block(raw)
        print(f'  Removed {n} block(s). New length: {len(cleaned)} (was {len(raw)})')

        resp = api_post(wp_id, nonce, {'content': cleaned})
        if 'id' in resp:
            still_present = 'editor-update-block' in resp.get('content',{}).get('rendered','')
            print(f'  Saved. Block still present in rendered: {still_present}')
            print(f'  Link: {resp.get("link","")}')
        else:
            print(f'  ERROR: {resp}')


if __name__ == '__main__':
    main()
