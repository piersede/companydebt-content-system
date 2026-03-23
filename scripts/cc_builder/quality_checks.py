"""Build-time quality checks for credit card pages.

Runs automatically during page build to catch:
- H2 semantic relevance violations (Signal 5a)
- WordPress technical build quality issues
- Accessibility violations

Any FAIL-level check blocks the build. WARN-level checks are logged
but do not block.
"""

from __future__ import annotations

import html
import re
import sys
from html.parser import HTMLParser


# ── H2 semantic relevance ─────────────────────────────────────────────

# Structural H2s exempt from topic-anchoring requirements
EXEMPT_H2S = {
    'related pages',
    'methodology and disclosure',
}

# Generic H2 patterns that must include topic keywords to pass
GENERIC_H2_PATTERNS = [
    'compare cards at a glance',
    'quick comparison',
    'alternatives',
    'other options',
    'frequently asked questions',
    'questions we get asked',
    'how to choose',
    'what to do if you\'re rejected',
    'key terms explained',
    'also mentioned',
    'every card, reviewed',
    'the key differences',
    'the core difference',
    'your options at a glance',
    'your situation at a glance',
    'your credit situation',
    'how to improve your chances',
    'how to compare before you apply',
    'what to do instead',
]


def _extract_topic_keywords(title: str, page_type: str, config: dict) -> list[str]:
    """Extract keywords that H2s should reference based on page title and type."""
    keywords = []
    title_lower = title.lower()

    # Always accept 'business credit card' variants
    keywords.append('business credit card')
    keywords.append('business credit cards')

    if page_type == 'review':
        # Extract product name from title (before "Review")
        match = re.match(r'^(.+?)\s+(?:Business\s+)?(?:Credit\s+Card\s+)?Review', title, re.IGNORECASE)
        if match:
            product = match.group(1).strip()
            keywords.append(product.lower())
            # Also add individual words for multi-word products
            for word in product.split():
                if len(word) > 3 and word.lower() not in ('business', 'credit', 'card', 'the'):
                    keywords.append(word.lower())

    elif page_type in ('brand_comparison', 'brand_compare'):
        # Extract brand names
        brands = []
        if 'vs' in title_lower:
            parts = re.split(r'\s+vs\.?\s+', title, flags=re.IGNORECASE)
            brands = [p.strip().split('(')[0].strip() for p in parts]
        elif 'compare' in title_lower:
            match = re.match(r'Compare\s+(.+?)\s+Business', title, re.IGNORECASE)
            if match:
                brands.append(match.group(1).strip())
        for brand in brands:
            keywords.append(brand.lower())
            # Add common abbreviations
            if 'american express' in brand.lower():
                keywords.append('amex')
            if 'barclaycard' in brand.lower():
                keywords.append('barclaycard')
            for word in brand.split():
                if len(word) > 3:
                    keywords.append(word.lower())

    elif page_type == 'roundup':
        # Extract category from title
        category_patterns = [
            (r'(?:best\s+)?(.+?)\s+business\s+credit\s+cards?', 1),
            (r'business\s+credit\s+cards?\s+for\s+(.+?)(?:\s+\(|\s+in\s+)', 1),
        ]
        for pattern, group in category_patterns:
            match = re.search(pattern, title, re.IGNORECASE)
            if match:
                cat = match.group(group).strip().lower()
                if cat not in ('the', 'best', 'uk'):
                    keywords.append(cat)
                    for word in cat.split():
                        if len(word) > 3:
                            keywords.append(word)

        # Add specific category keywords from common page types
        if 'charge card' in title_lower:
            keywords.extend(['charge card', 'charge cards', 'business charge card'])
        if 'cashback' in title_lower or 'reward' in title_lower:
            keywords.extend(['cashback', 'reward', 'rewards'])
        if 'travel' in title_lower:
            keywords.append('travel')
        if 'avios' in title_lower or 'air miles' in title_lower:
            keywords.extend(['avios', 'air miles'])
        if 'sole trader' in title_lower:
            keywords.extend(['sole trader', 'sole traders'])
        if 'start-up' in title_lower or 'startup' in title_lower:
            keywords.extend(['start-up', 'start-ups', 'startup'])
        if 'poor credit' in title_lower:
            keywords.extend(['poor credit'])
        if 'interest-free' in title_lower or 'interest free' in title_lower:
            keywords.extend(['interest-free', 'interest free'])
        if 'low apr' in title_lower:
            keywords.extend(['low apr', 'apr'])
        if 'instant' in title_lower:
            keywords.extend(['instant', 'instant approval'])
        if 'balance transfer' in title_lower:
            keywords.extend(['balance transfer'])

    elif page_type == 'guide':
        keywords.append('business credit card')
        if 'charge card' in title_lower:
            keywords.extend(['charge card', 'charge cards', 'credit card', 'credit cards'])
        if 'balance transfer' in title_lower:
            keywords.extend(['balance transfer'])

    return list(set(k for k in keywords if k))


def _h2_passes_relevance(h2_text: str, topic_keywords: list[str]) -> bool:
    """Check if an H2 contains at least one topic keyword."""
    h2_lower = h2_text.lower()

    # Check exemptions
    if h2_lower.strip() in EXEMPT_H2S:
        return True

    # Check if any topic keyword appears in the H2
    for kw in topic_keywords:
        if kw in h2_lower:
            return True

    return False


def validate_h2_relevance(config: dict) -> list[dict]:
    """Validate H2 semantic relevance for a page config.

    H2 relevance is advisory (WARN only). The principle is "keywords
    but natural" — H2s should read as chapter titles, not keyword
    targets. The page context already establishes the topic, so a
    contextually clear H2 like "The Rate Problem" on a Capital on Tap
    review page is fine even without the product name.

    Returns a list of violation dicts with keys:
        h2_text, reason, severity (always 'WARN')
    """
    violations = []
    title = config.get('title', '')
    page_type = config.get('page_type', 'roundup')
    topic_keywords = _extract_topic_keywords(title, page_type, config)

    for section in config.get('sections', []):
        if section.get('type') == 'heading' and section.get('level', 2) == 2:
            h2_text = section.get('text', '')
            if not _h2_passes_relevance(h2_text, topic_keywords):
                violations.append({
                    'h2_text': h2_text,
                    'reason': (
                        f'H2 has no topic keyword (may be fine if contextually clear). '
                        f'Topic keywords: {", ".join(topic_keywords[:5])}'
                    ),
                    'severity': 'WARN',
                })

    return violations


# ── WordPress build quality checks ────────────────────────────────────

class _HTMLTagChecker(HTMLParser):
    """Lightweight HTML parser for build quality checks."""

    def __init__(self):
        super().__init__()
        self.heading_levels = []  # list of (level, text)
        self.images = []  # list of {src, alt, loading, width, height}
        self.inline_onclick = 0
        self.aria_attrs = 0
        self.links_missing_rel = []
        self._current_tag = None
        self._current_data = ''

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self._current_tag = tag
            self._current_data = ''

        if tag == 'img':
            self.images.append({
                'src': attrs_dict.get('src', ''),
                'alt': attrs_dict.get('alt'),
                'loading': attrs_dict.get('loading'),
                'width': attrs_dict.get('width'),
                'height': attrs_dict.get('height'),
            })

        if tag == 'a' and attrs_dict.get('target') == '_blank':
            rel = attrs_dict.get('rel', '')
            if 'noopener' not in rel:
                self.links_missing_rel.append(attrs_dict.get('href', ''))

        # Count onclick handlers
        if 'onclick' in attrs_dict:
            self.inline_onclick += 1

        # Count ARIA attributes
        for attr_name, _ in attrs:
            if attr_name.startswith('aria-') or attr_name == 'role':
                self.aria_attrs += 1

    def handle_data(self, data):
        if self._current_tag:
            self._current_data += data

    def handle_endtag(self, tag):
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6') and self._current_tag == tag:
            level = int(tag[1])
            self.heading_levels.append((level, self._current_data.strip()))
            self._current_tag = None
            self._current_data = ''


def validate_build_quality(html_content: str) -> list[dict]:
    """Run WordPress build quality checks on generated HTML.

    Returns list of violation dicts with keys:
        check, detail, severity ('FAIL' or 'WARN')
    """
    violations = []
    checker = _HTMLTagChecker()
    try:
        checker.feed(html_content)
    except Exception:
        violations.append({
            'check': 'html_parse',
            'detail': 'HTML could not be parsed',
            'severity': 'FAIL',
        })
        return violations

    # ── Heading hierarchy ──
    prev_level = 0
    for level, text in checker.heading_levels:
        if prev_level > 0 and level > prev_level + 1:
            violations.append({
                'check': 'heading_hierarchy',
                'detail': f'Heading skip: h{prev_level} → h{level} ("{text}")',
                'severity': 'FAIL',
            })
        prev_level = level

    # ── Image optimization ──
    for i, img in enumerate(checker.images):
        if img['alt'] is None:
            violations.append({
                'check': 'image_alt',
                'detail': f'Image missing alt attribute: {img["src"][:60]}',
                'severity': 'FAIL',
            })
        if not img.get('loading') and i > 0:  # first image can be eager
            violations.append({
                'check': 'image_lazy',
                'detail': f'Image missing loading="lazy": {img["src"][:60]}',
                'severity': 'WARN',
            })
        if not img.get('width') or not img.get('height'):
            violations.append({
                'check': 'image_dimensions',
                'detail': f'Image missing width/height (CLS risk): {img["src"][:60]}',
                'severity': 'WARN',
            })

    # ── Inline onclick handlers ──
    if checker.inline_onclick > 0:
        violations.append({
            'check': 'inline_onclick',
            'detail': f'{checker.inline_onclick} inline onclick handler(s) found (CSP risk)',
            'severity': 'WARN',
        })

    # ── Links missing rel ──
    for href in checker.links_missing_rel:
        violations.append({
            'check': 'link_rel',
            'detail': f'target="_blank" without rel="noopener": {href[:60]}',
            'severity': 'FAIL',
        })

    # ── ARIA minimum ──
    if checker.aria_attrs < 2:
        violations.append({
            'check': 'aria_minimum',
            'detail': f'Only {checker.aria_attrs} ARIA attributes found (expected ≥2)',
            'severity': 'WARN',
        })

    # ── CSS !important count ──
    important_count = html_content.count('!important')
    if important_count > 35:
        violations.append({
            'check': 'css_important',
            'detail': f'{important_count} !important declarations (target: <35)',
            'severity': 'WARN',
        })

    # ── JSON-LD schema presence ──
    if 'application/ld+json' not in html_content:
        violations.append({
            'check': 'schema_missing',
            'detail': 'No JSON-LD structured data found',
            'severity': 'FAIL',
        })

    # ── Disclosure architecture ──
    if 'cc-hero-disclosure' not in html_content and 'affiliate' not in html_content.lower():
        violations.append({
            'check': 'disclosure_missing',
            'detail': 'No affiliate disclosure found in page content',
            'severity': 'FAIL',
        })

    return violations


# ── Information gain enforcement ──────────────────────────────────────

# H2s exempt from requiring information gain declarations
INFO_GAIN_EXEMPT_H2S = {
    'methodology and disclosure',
    'explore business credit cards by category',
    'individual card reviews and brand comparisons',
    'business credit card guides and explainers',
    'related pages',
}

# Minimum info gain elements per article (§12 of 10-evidence-governance.md)
MIN_ARTICLE_INFO_GAIN = 3


def validate_info_gain(config: dict) -> list[dict]:
    """Validate information gain declarations in a page config.

    Rules enforced (from 10-evidence-governance.md §12):
    - Article-level: at least 3 net-new value elements declared
    - H2-level: every content H2 must have at least one info_gain element
    - Each element must specify what is novel and its source

    Page configs must include an 'info_gain' dict keyed by H2 text,
    where each value is a list of strings describing the novel element.
    Navigation-only and methodology H2s are exempt.

    Returns list of violation dicts.
    """
    violations = []
    info_gain = config.get('info_gain', {})

    # Collect all content H2s from sections
    content_h2s = []
    for section in config.get('sections', []):
        if section.get('type') == 'heading' and section.get('level', 2) == 2:
            h2_text = section.get('text', '')
            if h2_text.lower().strip() not in INFO_GAIN_EXEMPT_H2S:
                content_h2s.append(h2_text)

    # Check: info_gain dict must exist
    if not info_gain:
        violations.append({
            'check': 'info_gain_missing',
            'detail': (
                'No info_gain declarations found. Every page must declare '
                'its information gain elements per H2 section.'
            ),
            'severity': 'FAIL',
        })
        return violations

    # Build a normalized lookup for info_gain keys (decode HTML entities)
    _norm = lambda s: html.unescape(s)
    info_gain_norm = {_norm(k): v for k, v in info_gain.items()}

    # Check: each content H2 must have at least one info_gain element
    for h2_text in content_h2s:
        h2_norm = _norm(h2_text)
        elements = info_gain.get(h2_text, []) or info_gain_norm.get(h2_norm, [])
        if not elements:
            violations.append({
                'check': 'info_gain_h2',
                'h2_text': h2_text,
                'detail': (
                    'H2 section has no declared information gain element. '
                    'Every content H2 must contain at least one fact, '
                    'framework, or caveat that competitors omit.'
                ),
                'severity': 'FAIL',
            })

    # Check: article-level minimum (count total elements across all H2s)
    total_elements = sum(len(v) for v in info_gain.values() if isinstance(v, list))
    if total_elements < MIN_ARTICLE_INFO_GAIN:
        violations.append({
            'check': 'info_gain_article',
            'detail': (
                f'Only {total_elements} info gain element(s) declared across '
                f'the article. Minimum is {MIN_ARTICLE_INFO_GAIN}.'
            ),
            'severity': 'FAIL',
        })

    # Check: each element must be a non-empty string (not a placeholder)
    for h2_text, elements in info_gain.items():
        if not isinstance(elements, list):
            violations.append({
                'check': 'info_gain_format',
                'h2_text': h2_text,
                'detail': 'info_gain value must be a list of strings',
                'severity': 'FAIL',
            })
            continue
        for elem in elements:
            if not isinstance(elem, str) or len(elem.strip()) < 10:
                violations.append({
                    'check': 'info_gain_empty',
                    'h2_text': h2_text,
                    'detail': (
                        f'Info gain element too short or empty: "{elem}". '
                        'Each element must describe what is novel and its source.'
                    ),
                    'severity': 'FAIL',
                })

    return violations


# ── Primary source enforcement ───────────────────────────────────────

# Competitor/aggregator sources that must never appear as product data sources
BANNED_SOURCES = [
    'moneysupermarket', 'moneysavingexpert', 'nerdwallet', 'finder',
    'forbes advisor', 'totallymoney', 'gocompare', 'comparethemarket',
    'creditcards.com', 'uswitch', 'which?', 'money.co.uk',
    'bankrate', 'creditkarma', 'credit karma', 'merchant savvy',
]

# Patterns that indicate a banned source is being used as a product data source
# (not just mentioned in passing for rhetorical contrast)
SOURCE_CITATION_PATTERNS = [
    r'source:\s*',
    r'according\s+to\s+',
    r'data\s+from\s+',
    r'cross-referenced\s+against\s+',
    r'verified\s+(?:against|by|from|via)\s+',
    r'sourced\s+from\s+',
    r'reported\s+by\s+',
    r'published\s+by\s+',
]


def validate_primary_sources(config: dict) -> list[dict]:
    """Check that no competitor/aggregator sites are cited as product data sources.

    Scans all prose paragraphs in the config for banned source names appearing
    in citation contexts. Mentions of competitors for rhetorical contrast
    (e.g. 'most comparison sites bury this') are not flagged.

    Returns list of violation dicts.
    """
    violations = []

    # Collect all text content from sections
    for section in config.get('sections', []):
        paragraphs = section.get('paragraphs', [])
        if isinstance(paragraphs, str):
            paragraphs = [paragraphs]

        # Also check FAQ items
        items = section.get('items', [])
        for item in items:
            if isinstance(item, dict):
                for key in ('a', 'answer'):
                    if key in item:
                        paragraphs.append(item[key])

        for para in paragraphs:
            if not isinstance(para, str):
                continue
            para_lower = para.lower()

            for banned in BANNED_SOURCES:
                if banned not in para_lower:
                    continue
                # Check if it appears in a citation context
                for pattern in SOURCE_CITATION_PATTERNS:
                    # Look for pattern followed by (within 40 chars) the banned source
                    combined = pattern + r'.{0,40}' + re.escape(banned)
                    if re.search(combined, para_lower):
                        # Extract a snippet around the match
                        idx = para_lower.index(banned)
                        start = max(0, idx - 30)
                        end = min(len(para), idx + len(banned) + 30)
                        snippet = para[start:end].replace('\n', ' ')
                        violations.append({
                            'check': 'primary_source',
                            'detail': (
                                f'Competitor source "{banned}" cited as product data source: '
                                f'...{snippet}...'
                            ),
                            'severity': 'FAIL',
                        })
                        break  # Don't double-flag same source in same paragraph

    return violations


# ── Combined runner ────────────────────────────────────────────────────

def run_all_checks(config: dict, html_content: str) -> tuple[bool, list[dict]]:
    """Run all quality checks and return (passed, violations).

    passed is False if any FAIL-level violation exists.
    """
    all_violations = []

    # H2 relevance (config-level)
    h2_violations = validate_h2_relevance(config)
    all_violations.extend(h2_violations)

    # Information gain (config-level)
    info_gain_violations = validate_info_gain(config)
    all_violations.extend(info_gain_violations)

    # Primary source enforcement (config-level)
    source_violations = validate_primary_sources(config)
    all_violations.extend(source_violations)

    # Build quality (HTML-level)
    build_violations = validate_build_quality(html_content)
    all_violations.extend(build_violations)

    # Determine pass/fail
    has_fails = any(v.get('severity') == 'FAIL' for v in all_violations)

    return (not has_fails), all_violations


def print_report(violations: list[dict], slug: str) -> None:
    """Print a formatted quality check report to stderr."""
    if not violations:
        print(f'  ✓ {slug}: All quality checks passed', file=sys.stderr)
        return

    fails = [v for v in violations if v.get('severity') == 'FAIL']
    warns = [v for v in violations if v.get('severity') == 'WARN']

    if fails:
        print(f'\n  FAIL  {slug}: {len(fails)} failure(s), {len(warns)} warning(s)',
              file=sys.stderr)
    else:
        print(f'\n  WARN  {slug}: {len(warns)} warning(s)', file=sys.stderr)

    for v in fails:
        check = v.get('check', 'h2_relevance')
        detail = v.get('detail', v.get('reason', ''))
        h2 = v.get('h2_text', '')
        if h2:
            print(f'    FAIL  [{check}] "{h2}": {detail}', file=sys.stderr)
        else:
            print(f'    FAIL  [{check}] {detail}', file=sys.stderr)

    for v in warns:
        check = v.get('check', 'h2_relevance')
        detail = v.get('detail', v.get('reason', ''))
        h2 = v.get('h2_text', '')
        if h2:
            print(f'    WARN  [{check}] "{h2}": {detail}', file=sys.stderr)
        else:
            print(f'    WARN  [{check}] {detail}', file=sys.stderr)
