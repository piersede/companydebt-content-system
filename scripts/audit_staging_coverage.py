"""
Inbound link coverage audit using the staging content cache (not _all/ files).
This gives the true picture of what's on staging right now.
"""
import json
import re
from pathlib import Path
from collections import defaultdict

ROOT       = Path(__file__).parent.parent
CACHE_FILE = ROOT / 'content_cache.json'
INVENTORY  = ROOT / 'staging_page_inventory_fresh.json'

cache     = json.loads(CACHE_FILE.read_text(encoding='utf-8'))
inventory = json.loads(INVENTORY.read_text(encoding='utf-8'))

HREF_RE = re.compile(r'href=["\']([^"\'#?]*)["\']')

def norm(p):
    return '/' + p.strip('/') + '/'

# Build inbound link map from staging content
link_map = defaultdict(set)  # dest_path -> {source_slugs}

for src_path, meta in cache.items():
    slug = meta['slug']
    raw  = meta.get('raw', '')
    for m in HREF_RE.finditer(raw):
        dest = norm(m.group(1))
        if dest != norm(src_path):
            link_map[dest].add(slug)

# Published pages
published = {norm(k): v for k, v in inventory.items() if v['status'] == 'publish'}

# Skip utility pages
SKIP = {
    '/about-us/', '/accessibility/', '/accreditations/', '/careers/',
    '/complaints/', '/complaints-procedure/', '/content-usage-guidelines/',
    '/cookie-policy/', '/cookie-policy-company-debt/', '/feedback/',
    '/legal/', '/meet-the-team/', '/privacy-policy/', '/prize-draw-terms-conditions/',
    '/quick-quote/', '/site-map/', '/terms-conditions/', '/useful-publications/',
    '/charge-out-rates/', '/insolvency-calculator/', '/express-liquidation/',
    '/stressed-directors-guide/', '/contact-us/', '/case-studies-hub/',
}

SKIP_PREFIXES = ('/articles/', '/sectors/', '/services-to/', '/sample-letters/',
                 '/case-studies/')

def should_skip(path):
    if path in SKIP:
        return True
    return any(path.startswith(p) for p in SKIP_PREFIXES)

print('=' * 70)
print('STAGING INBOUND LINK COVERAGE (from content_cache.json)')
print('=' * 70)

counts = []
for path, entry in sorted(published.items()):
    if should_skip(path):
        continue
    slug = entry['slug']
    n = len(link_map.get(path, set()))
    counts.append((n, path, slug))

counts.sort()

zero  = [(p, s) for n, p, s in counts if n == 0]
one   = [(p, s, list(link_map.get(p, set()))) for n, p, s in counts if n == 1]
two   = [(p, s, list(link_map.get(p, set()))) for n, p, s in counts if n == 2]

print(f'\n0 inbound ({len(zero)} pages):')
for p, s in zero:
    print(f'  {p}')

print(f'\n1 inbound ({len(one)} pages):')
for p, s, srcs in one:
    print(f'  {p}  <- {srcs[0]}')

print(f'\n2 inbound ({len(two)} pages):')
for p, s, srcs in two:
    print(f'  {p}  <- {", ".join(srcs)}')

print(f'\nSummary: 0={len(zero)}  1={len(one)}  2={len(two)}')

print('\nTop 15 most-linked pages:')
for n, p, s in reversed(counts[-15:]):
    print(f'  {n:3d}  {p}')
