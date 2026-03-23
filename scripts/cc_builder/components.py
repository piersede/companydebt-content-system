"""Reusable HTML component builders for credit card pages.

Each function returns an HTML string (not a Gutenberg block).
Use PageBuilder.raw_html() to wrap them for WordPress.
"""

from __future__ import annotations


def build_card_html(card: dict) -> str:
    """Build a single cc-card component from card data.

    Card dict keys:
        Required: name, img_url, img_alt, fit_label, verdict, facts,
                  best_for, watch_out, not_ideal, eligibility,
                  cta_url, cta_label
        Optional: summary_strip, editorial_heading, verify_source,
                  verify_date
    """
    facts_html = ''
    for fact in card['facts']:
        # Support both tuple format (label, value, modifier, qualifier)
        # and dict format {label, value, modifier, qualifier}
        if isinstance(fact, (list, tuple)):
            label, value, modifier, qualifier = fact
        else:
            label = fact['label']
            value = fact['value']
            modifier = fact.get('modifier')
            qualifier = fact.get('qualifier')

        val_class = 'cc-card__fact-value'
        if modifier == 'apr':
            val_class += ' cc-card__fact-value--apr'
        elif modifier == 'required':
            val_class += ' cc-card__fact-value--required'
        elif modifier == 'none-required':
            val_class += ' cc-card__fact-value--none-required'

        qual_html = ''
        if qualifier:
            qual_html = (
                f'\n        <span class="cc-card__fact-qualifier">'
                f'{qualifier}</span>'
            )

        facts_html += f'''
      <div class="cc-card__fact">
        <span class="cc-card__fact-label">{label}</span>
        <span class="{val_class}">{value}</span>{qual_html}
      </div>'''

    verify_source = card.get('verify_source', 'provider pricing page')
    verify_date = card.get('verify_date', '20 March 2026')

    # Generate a stable anchor ID from the card's id field
    card_anchor = card.get('id', card.get('name', '')).replace(' ', '-').lower()
    card_anchor = ''.join(c for c in card_anchor if c.isalnum() or c == '-')

    # Internal review/comparison page links for editorial take
    _REVIEW_URLS = {
        'capital_on_tap_business_credit_card': '/business-credit-cards/capital-on-tap-review/',
        'funding_circle_cashback_business_credit_card': '/business-credit-cards/funding-circle-business-credit-card-review/',
        'funding_circle_flexipay': '/business-credit-cards/flexipay-review/',
        'amex_business_gold': '/business-credit-cards/compare-american-express-business-credit-cards/',
        'amex_business_platinum': '/business-credit-cards/compare-american-express-business-credit-cards/',
        'amex_business_basic': '/business-credit-cards/compare-american-express-business-credit-cards/',
        'ba_amex_accelerating': '/business-credit-cards/compare-american-express-business-credit-cards/',
        'amazon_amex': '/business-credit-cards/compare-american-express-business-credit-cards/',
        'barclaycard_select_cashback_business_credit_card': '/business-credit-cards/compare-barclaycard-business-credit-cards/',
        'barclaycard_select_charge_card': '/business-credit-cards/compare-barclaycard-business-credit-cards/',
        'barclaycard_premium_plus_business_credit_card': '/business-credit-cards/compare-barclaycard-business-credit-cards/',
    }
    editorial_url = _REVIEW_URLS.get(card.get('id', ''), card.get('cta_url', '#'))
    editorial_target = '' if editorial_url.startswith('/') else ' target="_blank" rel="noopener noreferrer"'
    editorial_label = 'Read our full review' if card.get('id', '') in _REVIEW_URLS else 'View full card details'

    # Build notes — only render rows that have content
    notes_html = ''
    for label, key in [
        ('Best for', 'best_for'),
        ('Watch out', 'watch_out'),
        ('Not ideal if', 'not_ideal'),
        ('Eligibility', 'eligibility'),
    ]:
        val = card.get(key, '')
        if val:
            notes_html += (
                f'\n    <div class="cc-card__note">'
                f'<strong>{label}:</strong> {val}</div>'
            )

    return f'''<div class="cc-card" id="card-{card_anchor}">
  <div class="cc-card__summary-strip">{card.get('fit_label', '')}</div>

  <div class="cc-card__header">
    <div class="cc-card__image">
      <img src="{card['img_url']}" alt="{card['img_alt']}" width="100" height="60" loading="lazy" />
    </div>
    <div class="cc-card__identity">
      <h3>{card['name']}</h3>
      <div class="cc-card__verdict">{card.get('verdict', '')}</div>
    </div>
    <div class="cc-card__header-cta">
      <a href="{card['cta_url']}" class="cc-card__cta" target="_blank" rel="noopener noreferrer">{card['cta_label']} &rarr;</a>
    </div>
  </div>

  <div class="cc-card__facts">{facts_html}
  </div>

  <div class="cc-card__notes">{notes_html}
  </div>

  <div class="cc-card__footer">
    <a href="{editorial_url}" class="cc-card__editorial-toggle"{editorial_target}>{editorial_label} &rarr;</a>
    <span class="cc-card__trust">Verified against {verify_source}, {verify_date}</span>
  </div>
</div>'''


def build_tabbed_card_html(card: dict, card_index: int = 0) -> str:
    """Build a tabbed product card: fixed summary top + 3-tab content area.

    Tabs: Overview | Card Details | Eligibility
    The top section (strip, header with image/name/verdict/CTA, 2 key stats)
    is always visible. Tabs organise the deeper detail below.

    Args:
        card: Full card data dict with overrides already merged.
        card_index: Index for unique tab IDs when multiple cards on page.
    """
    verify_source = card.get('verify_source', 'provider pricing page')
    verify_date = card.get('verify_date', '20 March 2026')

    card_anchor = card.get('id', card.get('name', '')).replace(' ', '-').lower()
    card_anchor = ''.join(c for c in card_anchor if c.isalnum() or c == '-')
    tab_prefix = f'cctab-{card_index}'

    # ── Fixed top: strip + header + 2 key stats ──
    # Pick the two most useful headline stats: Annual Fee + Rewards/APR
    headline_facts = []
    for fact in card.get('facts', []):
        if isinstance(fact, (list, tuple)):
            label, value = fact[0], fact[1]
        else:
            label, value = fact['label'], fact['value']
        if label.lower() in ('annual fee', 'rewards', 'representative apr',
                             'amazon cashback', 'card type'):
            headline_facts.append((label, value))
        if len(headline_facts) >= 2:
            break

    headline_html = ''
    for label, value in headline_facts:
        headline_html += (
            f'<div class="cc-tab-card__stat">'
            f'<span class="cc-tab-card__stat-label">{label}</span>'
            f'<span class="cc-tab-card__stat-value">{value}</span>'
            f'</div>'
        )

    # ── Tab 1: Overview (recommendation framing) ──
    overview_items = ''
    for label, key in [
        ('Best for', 'best_for'),
        ('Watch out', 'watch_out'),
        ('Not ideal if', 'not_ideal'),
    ]:
        val = card.get(key, '')
        if val:
            overview_items += (
                f'<div class="cc-tab-card__item">'
                f'<strong>{label}:</strong> {val}</div>\n'
            )
    # Verdict is already shown as the summary sentence in the header.
    # No need to repeat the full text in the Overview tab.

    # ── Tab 2: Card Details (structured facts) ──
    details_items = ''
    for fact in card.get('facts', []):
        if isinstance(fact, (list, tuple)):
            label, value, modifier, qualifier = fact
        else:
            label = fact['label']
            value = fact['value']
            qualifier = fact.get('qualifier')
        qual = f' <span class="cc-tab-card__qual">{qualifier}</span>' if qualifier else ''
        details_items += (
            f'<div class="cc-tab-card__detail-row">'
            f'<span class="cc-tab-card__detail-label">{label}</span>'
            f'<span class="cc-tab-card__detail-value">{value}{qual}</span>'
            f'</div>\n'
        )

    # ── Tab 3: Eligibility & Watch Outs ──
    elig_items = ''
    for label, key in [
        ('Eligibility', 'eligibility'),
        ('Not ideal if', 'not_ideal'),
        ('Watch out', 'watch_out'),
    ]:
        val = card.get(key, '')
        if val:
            elig_items += (
                f'<div class="cc-tab-card__item">'
                f'<strong>{label}:</strong> {val}</div>\n'
            )

    return f'''<div class="cc-tab-card" id="card-{card_anchor}">
  <div class="cc-tab-card__strip">{card.get('fit_label', '')}</div>

  <div class="cc-tab-card__header">
    <div class="cc-tab-card__image">
      <img src="{card.get('img_url', '')}" alt="{card.get('img_alt', '')}" width="100" height="60" loading="lazy" />
    </div>
    <div class="cc-tab-card__identity">
      <h3>{card['name']}</h3>
      <div class="cc-tab-card__summary">{card.get('verdict', '').split('.')[0]}.</div>
    </div>
    <div class="cc-tab-card__header-cta">
      <a href="{card.get('cta_url', '#')}" class="cc-tab-card__cta" target="_blank" rel="noopener noreferrer">{card.get('cta_label', 'View Details')} &rarr;</a>
    </div>
  </div>

  <div class="cc-tab-card__stats">
    {headline_html}
  </div>

  <div class="cc-tab-card__tabs" role="tablist">
    <button class="cc-tab-card__tab cc-tab-card__tab--active" role="tab" id="{tab_prefix}-tab-overview" data-tab="{tab_prefix}-overview" aria-selected="true" aria-controls="{tab_prefix}-overview" tabindex="0">Overview</button>
    <button class="cc-tab-card__tab" role="tab" id="{tab_prefix}-tab-details" data-tab="{tab_prefix}-details" aria-selected="false" aria-controls="{tab_prefix}-details" tabindex="-1">Card details</button>
    <button class="cc-tab-card__tab" role="tab" id="{tab_prefix}-tab-eligibility" data-tab="{tab_prefix}-eligibility" aria-selected="false" aria-controls="{tab_prefix}-eligibility" tabindex="-1">Eligibility</button>
  </div>

  <div class="cc-tab-card__panel cc-tab-card__panel--active" id="{tab_prefix}-overview" role="tabpanel" aria-labelledby="{tab_prefix}-tab-overview">
    {overview_items}
  </div>

  <div class="cc-tab-card__panel" id="{tab_prefix}-details" role="tabpanel" aria-labelledby="{tab_prefix}-tab-details" aria-hidden="true">
    {details_items}
  </div>

  <div class="cc-tab-card__panel" id="{tab_prefix}-eligibility" role="tabpanel" aria-labelledby="{tab_prefix}-tab-eligibility" aria-hidden="true">
    {elig_items}
  </div>

  <div class="cc-tab-card__footer">
    <span class="cc-tab-card__trust">Verified against {verify_source}, {verify_date}</span>
  </div>
</div>'''


def build_section_divider(label: str) -> str:
    """Build a visual section divider with label."""
    return (
        f'<div class="cc-section-divider">'
        f'<span class="cc-section-divider__label">{label}</span>'
        f'</div>'
    )



def build_v4_comparison_table(
    cards: list[dict],
    config: dict,
    page_config: dict | None = None,
) -> str:
    """Build a v4 comparison table: 6-column desktop, stacked mobile cards.

    Args:
        cards: List of card data dicts (from JSON).
        config: comparison_table_config from page config with keys:
            - badge_map: dict of card_id -> {text, color}
            - feature_keys: list of card dict keys to show as features
            - footer_text: verification/source footer text
        page_config: Full page config (for card_overrides lookup).

    Returns:
        Complete HTML string for the comparison table.
    """
    badge_map = config.get('badge_map', {})
    feature_keys = config.get('feature_keys', ['reward_type', 'card_type'])
    footer_text = config.get('footer_text', '')
    overrides = (page_config or {}).get('card_overrides', {})

    rows_html = ''
    for i, card in enumerate(cards):
        card_id = card.get('id', card.get('card_id', f'card-{i}'))
        card_overrides = overrides.get(card_id, {})

        # Card name + logo cell
        img_url = card.get('img_url', '')
        img_alt = card.get('img_alt', card.get('name', ''))
        if img_url and not img_url.startswith('['):
            logo_html = f'<img src="{img_url}" alt="{img_alt}" width="40" height="24" loading="lazy" />'
        else:
            initials = ''.join(
                w[0] for w in card.get('bank', 'XX').split()[:2]
            ).upper()
            logo_html = f'<span style="font-weight:700;font-size:12px;color:#666">{initials}</span>'

        badge_html = ''
        badge_info = badge_map.get(card_id)
        if badge_info:
            color = badge_info.get('color', 'gold')
            badge_html = (
                f'<div class="cc-ct__badge cc-ct__badge--{color}">'
                f'{badge_info["text"]}</div>'
            )

        display_name = card.get('short_name', card['name'])
        card_cell = (
            f'<div class="cc-ct__card-cell">'
            f'<div class="cc-ct__card-logo">{logo_html}</div>'
            f'<div><div class="cc-ct__card-name">{display_name}</div>'
            f'{badge_html}</div></div>'
        )

        # Annual fee
        annual_fee = card.get('annual_fee', 'Check provider')

        # APR / type — show "N/A" for charge cards with no APR
        apr = card.get('apr', card.get('representative_apr', ''))
        card_type = card.get('card_type', '')
        if not apr and 'charge' in card_type.lower():
            apr = 'N/A (pay in full monthly)'
        apr_cell = f'<div class="cc-ct__apr">{apr}</div>'
        if card_type:
            apr_cell += f'<div class="cc-ct__type">{card_type}</div>'

        # Best for
        best_for = card_overrides.get('best_for', card.get('best_for', ''))

        # Features (compact list)
        features_html = '<ul class="cc-ct__features">'
        for fk in feature_keys:
            val = card.get(fk, '')
            if val and not val.startswith('['):
                features_html += f'<li>{val}</li>'
        features_html += '</ul>'

        # Action — uniform short label in comparison table
        cta_url = card.get('cta_url', '#')
        action_html = (
            f'<a href="{cta_url}" class="cc-ct__action-link" '
            f'target="_blank" rel="noopener noreferrer">View details &rarr;</a>'
        )

        # Detail toggle
        detail_id = f'cc-ct-detail-{i}'
        toggle_html = (
            f'<button class="cc-ct__detail-toggle" data-detail="{detail_id}">'
            f'More detail ▼</button>'
        )

        # Main row
        rows_html += (
            f'<tr>'
            f'<td data-label="Card">{card_cell}{toggle_html}</td>'
            f'<td data-label="Annual fee">{annual_fee}</td>'
            f'<td data-label="APR / Type">{apr_cell}</td>'
            f'<td data-label="Best for">{best_for}</td>'
            f'<td data-label="Key features">{features_html}</td>'
            f'<td data-label="Action">{action_html}</td>'
            f'</tr>\n'
        )

        # Expandable detail row
        watch_out = card_overrides.get('watch_out', card.get('watch_out', ''))
        not_ideal = card_overrides.get('not_ideal', card.get('not_ideal', ''))
        eligibility = card_overrides.get('eligibility', card.get('eligibility', ''))
        verdict = card_overrides.get('verdict', card.get('verdict', ''))

        detail_blocks = ''
        if verdict:
            detail_blocks += (
                f'<div class="cc-ct__detail-block">'
                f'<div class="cc-ct__detail-label">Our take</div><p>{verdict}</p></div>'
            )
        if watch_out:
            detail_blocks += (
                f'<div class="cc-ct__detail-block">'
                f'<div class="cc-ct__detail-label">Watch out</div><p>{watch_out}</p></div>'
            )
        if not_ideal:
            detail_blocks += (
                f'<div class="cc-ct__detail-block">'
                f'<div class="cc-ct__detail-label">Not ideal if</div><p>{not_ideal}</p></div>'
            )
        if eligibility:
            detail_blocks += (
                f'<div class="cc-ct__detail-block">'
                f'<div class="cc-ct__detail-label">Eligibility</div><p>{eligibility}</p></div>'
            )

        rows_html += (
            f'<tr class="cc-ct__detail-row" id="{detail_id}">'
            f'<td colspan="6"><div class="cc-ct__detail-inner">'
            f'{detail_blocks}</div></td></tr>\n'
        )

    footer_html = ''
    if footer_text:
        footer_html = f'<div class="cc-ct__footer">{footer_text}</div>'

    return (
        f'<div class="cc-ct">'
        f'<table class="cc-ct__table">'
        f'<thead><tr>'
        f'<th>Card</th><th>Annual fee</th><th>APR / Type</th>'
        f'<th>Best for</th><th>Key features</th><th>Action</th>'
        f'</tr></thead>'
        f'<tbody>{rows_html}</tbody>'
        f'</table>'
        f'{footer_html}'
        f'</div>'
    )



def _decode_html_entities(text: str) -> str:
    """Decode HTML entities to Unicode for clean JSON-LD output."""
    import html as _html
    return _html.unescape(text)


def build_faq_html(items: list[dict]) -> str:
    """Build FAQ accordion HTML + JS + FAQPage JSON-LD schema.

    Uses native <details>/<summary> for no-JS fallback, enhanced with JS
    for class-based styling and aria attributes.

    Args:
        items: List of dicts with 'q' (question) and 'a' (answer) keys.
               'a' can be a string or list of paragraph strings.

    Returns:
        Combined HTML string (accordion + JS + schema script tag).
        Returns empty string if items is empty.
    """
    if not items:
        return ''

    chevron = (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
        '<polyline points="9 18 15 12 9 6"/></svg>'
    )

    rows = ''
    schema_items = []
    for idx, item in enumerate(items):
        q = item['q']
        a = item['a']
        a_html = ''.join(f'<p>{p}</p>' for p in a) if isinstance(a, list) else f'<p>{a}</p>'
        rows += (
            f'<li class="cc-faq__item">'
            f'<details class="cc-faq__details">'
            f'<summary class="cc-faq__question">'
            f'{q}<span class="cc-faq__icon">{chevron}</span>'
            f'</summary>'
            f'<div class="cc-faq__answer">{a_html}</div>'
            f'</details>'
            f'</li>'
        )
        import json as _json
        # Decode HTML entities to Unicode for clean JSON-LD
        clean_q = _json.dumps(_decode_html_entities(q))[1:-1]
        clean_a = _json.dumps(_decode_html_entities(a_html))[1:-1]
        schema_items.append(
            f'{{"@type":"Question","name":"{clean_q}",'
            f'"acceptedAnswer":{{"@type":"Answer","text":"{clean_a}"}}}}'
        )

    faq_html = f'<div class="cc-faq"><ul class="cc-faq__list">{rows}</ul></div>'

    schema_json = (
        '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":['
        + ','.join(schema_items) + ']}'
    )

    # JS enhances details/summary with class toggles for styled animation
    faq_js = (
        '<script>'
        'document.querySelectorAll(".cc-faq__details").forEach(function(d){'
        'd.addEventListener("toggle",function(){'
        'var item=d.closest(".cc-faq__item");'
        'if(d.open){item.classList.add("cc-faq__item--open");}'
        'else{item.classList.remove("cc-faq__item--open");}'
        '});'
        '});'
        '</script>'
    )

    schema_block = f'<script type="application/ld+json">{schema_json}</script>'

    return faq_html + faq_js + schema_block


def build_article_schema(config: dict) -> str:
    """Build Article + Person structured data for YMYL trust signals.

    Args:
        config: Full page config dict with title, verification_date, slug, etc.

    Returns:
        Script tag with JSON-LD Article schema, or empty string if no title.
    """
    title = config.get('title', '')
    if not title:
        return ''

    verify_date = config.get('verification_date', '20 March 2026')
    slug = config.get('slug', '')
    url = f'https://businessexpert.co.uk/business-credit-cards/{slug}/' if slug else ''

    import json as _json
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": _decode_html_entities(title),
        "dateModified": verify_date,
        "url": url,
        "author": {
            "@type": "Organization",
            "name": "BusinessExpert",
            "url": "https://businessexpert.co.uk/about/"
        },
        "publisher": {
            "@type": "Organization",
            "name": "BusinessExpert",
            "url": "https://businessexpert.co.uk/"
        }
    }

    return f'<script type="application/ld+json">{_json.dumps(schema, ensure_ascii=False)}</script>'
