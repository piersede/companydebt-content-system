"""
Safe, idempotent staging content editor for Ahrefs remediation.

Resolves a page/post on staging by its URL, reads RAW block content
(context=edit), applies a targeted edit, and PATCHes it back.

All edits are reported with before/after match counts so callers can verify.
Nothing is written unless --apply is passed.

Commands:
  show     --url URL
  swap-link --url URL --old OLD_HREF [--new NEW_HREF] [--apply]
              (omit --new to UNWRAP the link, leaving the anchor text)
  set-alt  --url URL --img IMG_SUBSTR --alt "alt text" [--apply]

URLs may be live (www.companydebt.com) or staging; both resolve to the
same staging post by slug.

Usage examples:
  python scripts/staging_edit.py show --url https://www.companydebt.com/liquidation/
  python scripts/staging_edit.py swap-link --url <page> --old <bad> --new <good> --apply
  python scripts/staging_edit.py set-alt  --url <page> --img samaritans --alt "Samaritans logo" --apply
"""
import os, re, sys, argparse, html
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

STAGING_URL  = os.getenv('WP_STAGING_URL', '').rstrip('/')
BA_USER      = os.getenv('WP_BASIC_AUTH_USER', '')
BA_PASS      = os.getenv('WP_BASIC_AUTH_PASS', '')
WP_USER      = os.getenv('WP_STAGING_USERNAME', '')
WP_APP_PASS  = os.getenv('WP_STAGING_APP_PASSWORD', '')

STAGING_HOST = urlparse(STAGING_URL).netloc
LIVE_HOST    = 'www.companydebt.com'


def session():
    s = requests.Session()
    s.auth = (BA_USER, BA_PASS)
    s.headers['User-Agent'] = 'CompanyDebt-AhrefsFix/1.0'
    s.get(f'{STAGING_URL}/wp-login.php', params={'wpe-login': 'true'})
    s.post(f'{STAGING_URL}/wp-login.php', params={'wpe-login': 'true'}, data={
        'log': WP_USER, 'pwd': WP_APP_PASS, 'wp-submit': 'Log In', 'testcookie': '1',
    }, allow_redirects=True)
    r = s.get(f'{STAGING_URL}/wp-admin/', timeout=30)
    m = (re.search(r'wpApiSettings[^}]+"nonce":"([a-f0-9]+)"', r.text)
         or re.search(r'"nonce":"([a-f0-9]+)"', r.text))
    if not m:
        raise RuntimeError('Could not extract WP nonce — check staging credentials')
    s.headers['X-WP-Nonce'] = m.group(1)
    return s


def slug_from_url(url):
    path = urlparse(url).path.strip('/')
    return path.split('/')[-1] if path else ''


def resolve_post(s, url):
    """Return (endpoint, id, slug, link) for the staging post matching url's slug."""
    slug = slug_from_url(url)
    if not slug:
        return None
    for endpoint in ('pages', 'posts'):
        r = s.get(f'{STAGING_URL}/wp-json/wp/v2/{endpoint}',
                  params={'slug': slug, 'context': 'edit',
                          '_fields': 'id,slug,link,content', 'status': 'publish'},
                  timeout=30)
        if r.status_code != 200:
            continue
        for item in r.json():
            if item.get('slug') == slug:
                return (endpoint, item['id'], item['slug'], item.get('link', ''),
                        item.get('content', {}).get('raw', ''))
    return None


def patch(s, endpoint, post_id, raw):
    r = s.post(f'{STAGING_URL}/wp-json/wp/v2/{endpoint}/{post_id}',
               json={'content': raw},
               headers={'Content-Type': 'application/json'}, timeout=30)
    r.raise_for_status()
    return r.status_code


def to_live(href):
    if STAGING_HOST in href:
        return href.replace(STAGING_HOST, LIVE_HOST)
    return href


def variants(href):
    """All literal forms a link might take in stored content."""
    out = set()
    for h in {href, to_live(href), href.replace(LIVE_HOST, STAGING_HOST)}:
        out.add(h)
        # path-only form
        p = urlparse(h)
        if p.netloc in (LIVE_HOST, STAGING_HOST):
            out.add(p.path + (('?' + p.query) if p.query else ''))
    return {h for h in out if h}


def cmd_swap_link(s, url, old, new, apply):
    res = resolve_post(s, url)
    if not res:
        print(f'NOT_FOUND on staging: {url}')
        return
    endpoint, pid, slug, link, raw = res
    new = to_live(new) if new else None
    modified = raw
    total = 0
    for ov in variants(old):
        for q in ('"', "'"):
            if new:
                token = f'href={q}{ov}{q}'
                cnt = modified.count(token)
                if cnt:
                    modified = modified.replace(token, f'href={q}{new}{q}')
                    total += cnt
            else:
                # unwrap: <a ...href="ov"...>TEXT</a> -> TEXT
                pat = re.compile(r'<a\b[^>]*href=' + re.escape(q) + re.escape(ov)
                                 + re.escape(q) + r'[^>]*>(.*?)</a>', re.DOTALL)
                modified, n = pat.subn(lambda m: m.group(1), modified)
                total += n
    print(f'[{slug}] ({endpoint}/{pid}) matches={total}  old={old}  new={new or "(unwrap)"}')
    if total and apply:
        print(f'  PATCH {patch(s, endpoint, pid, modified)}')
    elif total:
        print('  (dry run — pass --apply to write)')


def cmd_set_alt(s, url, img, alt, apply):
    res = resolve_post(s, url)
    if not res:
        print(f'NOT_FOUND on staging: {url}')
        return
    endpoint, pid, slug, link, raw = res
    modified = raw
    changed = 0
    # find <img ...> tags whose src contains img substring
    def fix_img(m):
        nonlocal changed
        tag = m.group(0)
        if img not in tag:
            return tag
        if re.search(r'\balt=', tag):
            new_tag = re.sub(r'\balt=(["\']).*?\1', f'alt="{html.escape(alt, quote=True)}"', tag, count=1)
        else:
            new_tag = tag[:-1].rstrip() + f' alt="{html.escape(alt, quote=True)}"' + tag[-1]
        if new_tag != tag:
            changed += 1
        return new_tag
    modified = re.sub(r'<img\b[^>]*?/?>', fix_img, modified)
    print(f'[{slug}] ({endpoint}/{pid}) img~={img}  imgs_updated={changed}  alt="{alt}"')
    if changed and apply:
        print(f'  PATCH {patch(s, endpoint, pid, modified)}')
    elif changed:
        print('  (dry run — pass --apply to write)')


def cmd_add_class(s, url, contains, cls, apply):
    """Add a CSS class to any <p> whose inner content contains `contains`.
    Idempotent: skips paragraphs that already carry the class."""
    res = resolve_post(s, url)
    if not res:
        print(f'NOT_FOUND on staging: {url}')
        return
    endpoint, pid, slug, link, raw = res
    matched = 0
    modified = 0

    def repl(m):
        nonlocal matched, modified
        attrs, inner = m.group(1), m.group(2)
        if contains not in inner:
            return m.group(0)
        matched += 1
        cm = re.search(r'class=(["\'])(.*?)\1', attrs)
        if cm:
            classes = cm.group(2).split()
            if cls in classes:
                return m.group(0)  # already present — no-op
            new_attrs = attrs[:cm.start()] + f'class="{(cm.group(2) + " " + cls).strip()}"' + attrs[cm.end():]
        else:
            new_attrs = attrs + f' class="{cls}"'
        modified += 1
        return f'<p{new_attrs}>{inner}</p>'

    new_raw = re.sub(r'<p\b([^>]*)>(.*?)</p>', repl, raw, flags=re.DOTALL)
    print(f'[{slug}] ({endpoint}/{pid}) contains~="{contains[:40]}"  matched={matched}  modified={modified}  class={cls}')
    if modified and apply:
        print(f'  PATCH {patch(s, endpoint, pid, new_raw)}')
    elif modified:
        print('  (dry run — pass --apply to write)')
    elif matched:
        print('  (already has class — no change)')


def cmd_show(s, url):
    res = resolve_post(s, url)
    if not res:
        print(f'NOT_FOUND on staging: {url}')
        return
    endpoint, pid, slug, link, raw = res
    print(f'[{slug}] ({endpoint}/{pid})  link={link}  raw_len={len(raw)}')
    print('--- RAW (first 4000 chars) ---')
    print(raw[:4000])


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('show'); p.add_argument('--url', required=True)
    p = sub.add_parser('swap-link'); p.add_argument('--url', required=True)
    p.add_argument('--old', required=True); p.add_argument('--new', default='')
    p.add_argument('--apply', action='store_true')
    p = sub.add_parser('set-alt'); p.add_argument('--url', required=True)
    p.add_argument('--img', required=True); p.add_argument('--alt', required=True)
    p.add_argument('--apply', action='store_true')
    p = sub.add_parser('add-class'); p.add_argument('--url', required=True)
    p.add_argument('--contains', required=True); p.add_argument('--class', dest='cls', required=True)
    p.add_argument('--apply', action='store_true')
    a = ap.parse_args()

    s = session()
    if a.cmd == 'show':
        cmd_show(s, a.url)
    elif a.cmd == 'swap-link':
        cmd_swap_link(s, a.url, a.old, a.new or None, a.apply)
    elif a.cmd == 'set-alt':
        cmd_set_alt(s, a.url, a.img, a.alt, a.apply)
    elif a.cmd == 'add-class':
        cmd_add_class(s, a.url, a.contains, a.cls, a.apply)


if __name__ == '__main__':
    main()
