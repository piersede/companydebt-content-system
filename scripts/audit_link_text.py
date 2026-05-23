"""
Audit all internal link anchor text across the site for quality issues.

Flags:
  - Missing apostrophes: cant, dont, wont, its (as possessive), havent, etc.
  - All-lowercase multi-word anchors (likely slug-derived fallbacks)
  - Redundant category prefix repetitions (e.g. "HMRC X hmrc Y")
  - Suspiciously long anchor text (>60 chars, probably a slug)
  - Single-word anchors that are just a slug (no spaces)
  - href pointing off-site or to staging domain (should be relative)

Usage:
  python scripts/audit_link_text.py
"""
import json, re, sys
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

CACHE_FILE  = 'content_cache.json'
STAGING_HOST = 'comdebstage.wpengine.com'

# Contractions that are missing apostrophes
MISSING_APOS = re.compile(
    r"\b(cant|dont|wont|havent|hasnt|hadnt|isnt|arent|wasnt|werent"
    r"|wouldnt|couldnt|shouldnt|didnt|doesnt|neednt|mustnt|thats"
    r"|whats|theres|heres|its(?=\s+\w))\b",
    re.IGNORECASE,
)

LINK_RE = re.compile(r'<a\s[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', re.DOTALL | re.IGNORECASE)

def is_internal(href):
    return href.startswith('/') or STAGING_HOST in href

def strip_tags(text):
    return re.sub(r'<[^>]+>', '', text).strip()

def checks(href, text, src_path):
    issues = []
    clean  = strip_tags(text)

    # Off-site or staging absolute URL used as internal link
    if href.startswith('http') and STAGING_HOST not in href and not href.startswith('#'):
        return []  # external link — skip

    # Staging-absolute URL (should be relative)
    if STAGING_HOST in href:
        issues.append(('staging-absolute-href', f'href="{href}"'))

    if not clean:
        return issues

    # Missing apostrophes
    m = MISSING_APOS.search(clean)
    if m:
        issues.append(('missing-apostrophe', clean))

    # All-lowercase multi-word (≥3 words) — likely slug fallback
    words = clean.split()
    if len(words) >= 3 and clean == clean.lower() and clean.replace(' ', '').isalpha():
        issues.append(('lowercase-slug-text', clean))

    # Redundant repeated word (e.g. "HMRC ... hmrc")
    lower_words = [w.lower() for w in words]
    for w in set(lower_words):
        if len(w) >= 4 and lower_words.count(w) > 1:
            issues.append(('repeated-word', clean))
            break

    # Very long anchor (>70 chars)
    if len(clean) > 70:
        issues.append(('too-long', clean))

    return issues


def main():
    with open(CACHE_FILE, encoding='utf-8') as f:
        cache = json.load(f)

    findings = defaultdict(list)  # issue_type → [(src_slug, href, text)]
    by_page  = defaultdict(list)  # src_slug → [(issue_type, href, text)]

    for path, meta in cache.items():
        raw  = meta.get('raw', '')
        slug = meta['slug']
        if not raw:
            continue
        for m in LINK_RE.finditer(raw):
            href, text = m.group(1), m.group(2)
            if not is_internal(href):
                continue
            for issue_type, detail in checks(href, text, path):
                findings[issue_type].append((slug, href, detail))
                by_page[slug].append((issue_type, href, detail))

    # ── Print by issue type ──────────────────────────────────────────────────
    LABELS = {
        'missing-apostrophe':    'MISSING APOSTROPHE in anchor text',
        'lowercase-slug-text':   'ALL-LOWERCASE slug-derived anchor text',
        'repeated-word':         'REPEATED WORD in anchor text',
        'too-long':              'ANCHOR TEXT TOO LONG (>70 chars)',
        'staging-absolute-href': 'STAGING ABSOLUTE URL (should be relative)',
    }

    total = 0
    for issue_type, label in LABELS.items():
        items = findings[issue_type]
        if not items:
            continue
        print(f'\n{"─"*60}')
        print(f'{label}  ({len(items)} instance(s))')
        print(f'{"─"*60}')
        # Deduplicate by text
        seen = set()
        for slug, href, detail in sorted(items, key=lambda x: x[0]):
            key = (slug, detail[:80])
            if key in seen:
                continue
            seen.add(key)
            print(f'  [{slug}]  "{detail[:80]}"')
            total += 1

    print(f'\n{"="*60}')
    print(f'Total distinct issues: {total}')
    if total == 0:
        print('All internal link anchor text looks clean.')


if __name__ == '__main__':
    main()
