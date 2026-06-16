"""
Clean up the case-studies-hub ACF block: remove dead links to trashed case studies,
renumber remaining items, update counts.
"""
import subprocess, os, re, json, tempfile, sys
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')

URL = os.getenv('WP_STAGING_URL').rstrip('/')
BA  = os.getenv('WP_BASIC_AUTH_USER') + ':' + os.getenv('WP_BASIC_AUTH_PASS')
WP_USER = os.getenv('WP_STAGING_USERNAME')
WP_APP_PASS = os.getenv('WP_STAGING_APP_PASSWORD')
CJ = tempfile.mktemp(suffix='.txt')

HUB_PAGE_ID = 23471

TRASHED_SLUGS = {
    'bespoke-kitchen-manufacturer','creditors-voluntary-liquidation-with-phoenix',
    'freight-forwarder','individual-voluntary-arrangement-with-new-limited-company',
    'individual-voluntary-arrangement','online-travel-agent','personal-guarantees',
    'pizza-restaurant','plumbing','recruitment-consultant','womens-fashion-store',
    'jeweller','hardware-maintenance','pet-store','corporate-finance','language-school',
    'subcontractor-agency','hairdresser','hoverboard-retailer','it-consultancy',
    'seo-consultancy','building-contractor','plastering-company','information-technology',
    'time-to-pay-and-creditor-voluntary-liquidation','dissolution',
}


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


def url_points_to_trashed(url):
    """Return True if the URL's last path segment is a trashed slug."""
    if not url:
        return False
    path = url.split('?')[0].split('#')[0].rstrip('/')
    segs = [s for s in path.split('/') if s]
    if not segs:
        return False
    return segs[-1] in TRASHED_SLUGS


def clean_acf_data(data):
    """
    Given the parsed ACF data dict for the hub-box block, remove list items
    pointing to trashed slugs, renumber remaining items, update item counts.
    Returns (new_data, report).
    """
    report = {'removed': [], 'kept': []}
    boxes_count = int(data.get('hub_boxes_boxes', 0))
    new_data = {}

    # Copy non-box fields first
    box_field_pattern = re.compile(r'^_?hub_boxes_boxes_(\d+)_')
    box_count_pattern = re.compile(r'^_?hub_boxes_boxes$')
    for k, v in data.items():
        if not box_field_pattern.match(k) and not box_count_pattern.match(k):
            new_data[k] = v

    # Process each box
    for box_idx in range(boxes_count):
        prefix = f'hub_boxes_boxes_{box_idx}'
        # Copy box-level fields (heading, style, bcg, icon, view_all, list_item count)
        box_fields = {}
        for k, v in data.items():
            if k.startswith(f'_{prefix}_') or k.startswith(f'{prefix}_'):
                # Match a list_item subfield
                m = re.match(rf'_?{re.escape(prefix)}_list_item_(\d+)_(\w+)$', k)
                if m:
                    continue  # Handle list items separately
                if k == f'{prefix}_list_item' or k == f'_{prefix}_list_item':
                    continue  # Handle item count separately
                box_fields[k] = v

        # Iterate through list items in this box
        item_count = int(data.get(f'{prefix}_list_item', 0))
        kept_items = []
        for item_idx in range(item_count):
            ip = f'{prefix}_list_item_{item_idx}'
            title = data.get(f'{ip}_title')
            url   = data.get(f'{ip}_url')
            # Gather all subfields of this item
            item_fields = {}
            for k, v in data.items():
                if k == f'{ip}_title' or k == f'_{ip}_title' \
                   or k == f'{ip}_url' or k == f'_{ip}_url':
                    item_fields[k] = v

            if url_points_to_trashed(url):
                report['removed'].append({'box': box_idx, 'idx': item_idx, 'title': title, 'url': url})
            else:
                kept_items.append({'title': title, 'url': url, 'fields': item_fields, 'orig_idx': item_idx})
                report['kept'].append({'box': box_idx, 'title': title, 'url': url})

        # Write box-level fields
        new_data.update(box_fields)

        # Write kept items with new indices
        for new_idx, item in enumerate(kept_items):
            old_ip = f'{prefix}_list_item_{item["orig_idx"]}'
            new_ip = f'{prefix}_list_item_{new_idx}'
            for old_k, v in item['fields'].items():
                new_k = old_k.replace(old_ip, new_ip)
                new_data[new_k] = v

        # Update item count for this box
        new_data[f'{prefix}_list_item'] = len(kept_items)
        # Preserve the field key reference for list_item
        ref_key = f'_{prefix}_list_item'
        if ref_key in data:
            new_data[ref_key] = data[ref_key]

    # Preserve box count
    new_data['hub_boxes_boxes'] = boxes_count
    if '_hub_boxes_boxes' in data:
        new_data['_hub_boxes_boxes'] = data['_hub_boxes_boxes']

    return new_data, report


def fetch_page(nonce):
    cmd = ['curl','-s','-u',BA,'-c',CJ,'-b',CJ,
           '-H', f'X-WP-Nonce: {nonce}',
           f'{URL}/wp-json/wp/v2/pages/{HUB_PAGE_ID}?context=edit']
    r = subprocess.run(cmd, capture_output=True)
    return json.loads(r.stdout.decode('utf-8', errors='replace'))


def save_page(nonce, content):
    cmd = ['curl','-s','-u',BA,'-c',CJ,'-b',CJ,
           '-H', f'X-WP-Nonce: {nonce}',
           '-H', 'Content-Type: application/json',
           '-X', 'POST',
           '-d', json.dumps({'content': content}),
           f'{URL}/wp-json/wp/v2/pages/{HUB_PAGE_ID}']
    r = subprocess.run(cmd, capture_output=True)
    return json.loads(r.stdout.decode('utf-8', errors='replace'))


def main():
    login()
    nonce = get_nonce()
    print(f'Nonce: {nonce[:8]}...\n')

    page = fetch_page(nonce)
    raw = page.get('content',{}).get('raw') or page.get('content',{}).get('rendered','')
    print(f'Original content length: {len(raw)}')

    # Find the ACF hub-box block
    m = re.search(r'<!-- wp:acf/hub-box (\{.*?\}) /-->', raw, re.DOTALL)
    if not m:
        print('Could not find acf/hub-box block')
        sys.exit(1)

    block_json_str = m.group(1)
    block = json.loads(block_json_str)
    data = block.get('data', {})
    print(f'ACF data fields: {len(data)}')

    # Clean
    new_data, report = clean_acf_data(data)
    print(f'\nRemoved items: {len(report["removed"])}')
    for r in report['removed']:
        print(f'  - [box {r["box"]}] {r["title"]:35} -> {r["url"]}')
    print(f'\nKept items: {len(report["kept"])}')
    for r in report['kept']:
        print(f'  + [box {r["box"]}] {r["title"]:35} -> {r["url"]}')

    # Rebuild block
    block['data'] = new_data
    new_block_json = json.dumps(block, separators=(',', ':'), ensure_ascii=False)
    new_content = raw[:m.start()] + f'<!-- wp:acf/hub-box {new_block_json} /-->' + raw[m.end():]
    print(f'\nNew content length: {len(new_content)}')

    resp = save_page(nonce, new_content)
    if 'id' in resp:
        print(f'\nSaved OK. Modified: {resp.get("modified","")[:10]}')
        print(f'Link: {resp.get("link","")}')
        # Verify the dead links are gone in rendered
        new_rendered = resp.get('content',{}).get('rendered','')
        remaining = [s for s in TRASHED_SLUGS if s in new_rendered]
        if remaining:
            print(f'\nWARNING: {len(remaining)} trashed slugs still appear in rendered:')
            for s in remaining:
                print(f'  {s}')
        else:
            print('\nVerified: no trashed slugs remain in rendered content.')
    else:
        print(f'\nERROR: {resp}')


if __name__ == '__main__':
    main()
