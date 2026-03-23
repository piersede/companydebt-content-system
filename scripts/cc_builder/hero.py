"""Hero zone components for credit card pages.

Builds the v4 hero zone: two-column grid layout with editorial content
(verdict, verification, trust strip) on the left and top-pick featured
card on the right. Below the grid sits the "also consider" compact
card strip.

The hero zone CSS uses the .cc-hero- prefix to avoid collisions with
the WP theme.
"""

from __future__ import annotations


def build_top_pick_card(card: dict, config: dict) -> str:
    """Build the Top Pick featured card for the hero zone right column.

    Args:
        card: Full card data dict (from cards JSON).
        config: Hero config from page config with optional overrides.
    """
    label = config.get('top_pick_label', 'Top Pick')
    features = config.get('top_pick_features', [])
    tagline = config.get('top_pick_tagline', '')
    cta_url = card.get('cta_url', '#')
    cta_label = card.get('cta_label', 'View Details')
    img_url = card.get('img_url', '')
    img_alt = card.get('img_alt', card.get('name', ''))
    product_name = card.get('name', '')

    # Build feature list
    features_html = ''
    for feat in features:
        features_html += f'<li>{feat}</li>\n'

    # Image or fallback logo
    if img_url and not img_url.startswith('['):
        logo_html = f'<img src="{img_url}" alt="{img_alt}" width="140" height="74" loading="eager" />'
    else:
        initials = ''.join(w[0] for w in card.get('bank', 'XX').split()[:2]).upper()
        logo_html = initials

    # Optional tagline
    tagline_html = ''
    if tagline:
        tagline_html = f'\n  <div class="cc-hero-tp__tagline">{tagline}</div>'

    return f'''<div class="cc-hero-tp">
  <div class="cc-hero-tp__label">{label}</div>
  <h3 class="cc-hero-tp__name">{product_name}</h3>{tagline_html}
  <div class="cc-hero-tp__logo">{logo_html}</div>
  <ul class="cc-hero-tp__list">
    {features_html}
  </ul>
  <a href="{cta_url}" class="cc-hero-tp__cta" target="_blank" rel="noopener noreferrer">{cta_label} &rarr;</a>
</div>'''


def build_metadata_line(config: dict) -> str:
    """Build the compact inline metadata line that sits directly below the H1.

    No box, no border, no background — just quiet factual text.

    Args:
        config: Page config with verification_date, card count, etc.
    """
    card_count = len(config.get('card_ids', [])) + len(config.get('separate_card_ids', []))
    verify_date = config.get('verification_date', 'March 2026')

    return (
        f'<p class="cc-hero-meta">'
        f'<strong>{card_count}</strong> cards reviewed'
        f' &middot; <strong>Independently</strong> assessed'
        f' &middot; Rates verified <strong>{verify_date}</strong>'
        f'</p>'
    )


def build_hero_zone(config: dict, all_cards: list[dict], verdict_text: str = '') -> str:
    """Build the complete v4 hero zone HTML.

    Two-column grid layout:
    - Left: verdict text, verification notice, trust strip
    - Right: Top Pick card
    - Below (full width): Also Consider strip

    Args:
        config: Full page config dict. Must have 'hero' key.
        all_cards: All loaded card data dicts.
        verdict_text: Verdict/subtitle text for the left column.

    Returns:
        Complete hero zone HTML string, or empty string if no hero config.
    """
    from cc_builder.data.loader import load_card

    hero_config = config.get('hero')
    if not hero_config:
        return ''

    # ── Right column: Top Pick card ──
    tp_html = ''
    tp_card_id = hero_config.get('top_pick_card_id')
    if tp_card_id:
        try:
            tp_card = load_card(tp_card_id)
            tp_html = build_top_pick_card(tp_card, hero_config)
        except FileNotFoundError:
            import sys
            print(f'WARNING: Top pick card not found: {tp_card_id}', file=sys.stderr)

    # ── Left column: verdict + verification ──
    left_parts = []

    if verdict_text:
        left_parts.append(
            f'<p class="cc-hero-verdict">{verdict_text}</p>'
        )

    # Shortened verification notice (date already in metadata line)
    left_parts.append(
        '<p class="cc-hero-verify">Confirm current terms before applying.</p>'
    )

    # Top-of-page affiliate disclosure (tier 1 of three-tier architecture)
    left_parts.append(
        '<p class="cc-hero-disclosure">'
        'Some links on this page are affiliate links. '
        'See our <a href="/editorial-policy/">methodology</a> for details.'
        '</p>'
    )

    left_html = '\n'.join(left_parts)

    # ── Two-column hero grid ──
    grid_html = f'''<div class="cc-hero-grid">
  <div class="cc-hero-left">
    {left_html}
  </div>
  <div class="cc-hero-right">
    {tp_html}
  </div>
</div>'''

    # ── Also Consider strip (full width, below grid) ──
    also_html = ''
    also_configs = hero_config.get('also_consider', [])
    if also_configs:
        rows_html = ''
        for ac in also_configs[:3]:
            try:
                card = load_card(ac['card_id'])
            except FileNotFoundError:
                import sys
                print(f'WARNING: Also-consider card not found: {ac["card_id"]}', file=sys.stderr)
                continue

            badge = ac.get('badge', '')
            tagline = ac.get('tagline', '')
            cta_url = card.get('cta_url', '#')

            badge_html = f'<span class="cc-hero-also__tag">{badge}</span>' if badge else ''

            img_url = card.get('img_url', '')
            if img_url and not img_url.startswith('['):
                logo_html = f'<img src="{img_url}" alt="{card.get("img_alt", "")}" width="44" height="28" loading="lazy" />'
            else:
                initials = ''.join(w[0] for w in card.get('bank', 'XX').split()[:2]).upper()
                logo_html = initials

            display_name = ac.get('short_name') or card.get('name', '').replace(' Business Credit Card', '').replace(' Credit Card', '')

            rows_html += f'''<div class="cc-hero-also__row">
      <div class="cc-hero-also__thumb">{logo_html}</div>
      <div class="cc-hero-also__body">
        {badge_html}
        <div class="cc-hero-also__name">{display_name}</div>
        <div class="cc-hero-also__desc">{tagline}</div>
      </div>
      <a href="{cta_url}" class="cc-hero-also__link" target="_blank" rel="noopener noreferrer">View details &rarr;</a>
    </div>\n'''

        if rows_html:
            also_html = f'''<div class="cc-hero-also">
  <div class="cc-hero-also__label">Also Consider</div>
  <button class="cc-hero-also__toggle">Show alternatives &#x25BC;</button>
  <div class="cc-hero-also__list">
    {rows_html}
  </div>
</div>'''

    # Unified hero JS: replace subheading with metadata line, rebuild
    # author/readtime/date into a single strip, reposition disclosure.
    card_count = len(config.get('card_ids', [])) + len(config.get('separate_card_ids', []))
    verify_date = config.get('verification_date', 'March 2026')
    from cc_builder.js import CC_HERO_META_JS
    hero_js = (
        '<script>(function(){'
        # 1. Replace subheading text with metadata
        'var sub=document.querySelector("p.subheading");'
        'if(sub){'
        f'sub.textContent="{card_count} cards reviewed'
        f' \\u00b7 Independently assessed'
        f' \\u00b7 Rates verified {verify_date}";'
        'sub.style.fontSize="16px";'
        'sub.style.color="rgb(0,0,0)";'
        'sub.style.lineHeight="18.4px";'
        '}'
        # 2. Rebuild author/readtime/date strip + reposition disclosure
        f'{CC_HERO_META_JS}'
        # 3. Also-consider toggle (replaces inline onclick)
        'var alsoBtn=document.querySelector(".cc-hero-also__toggle");'
        'if(alsoBtn){'
        'alsoBtn.addEventListener("click",function(){'
        'var l=alsoBtn.nextElementSibling;'
        'if(!l)return;'
        'l.classList.toggle("cc-hero-also--expanded");'
        'alsoBtn.textContent=l.classList.contains("cc-hero-also--expanded")'
        '?"Hide alternatives \\u25B2":"Show alternatives \\u25BC";'
        '});'
        '}'
        '})();</script>'
    )

    # Static author attribution fallback (non-JS, for E-E-A-T on YMYL pages)
    author_fallback = (
        '<noscript><p class="cc-hero-author-fallback" style="font-size:14px;color:#666;margin:8px 0 0;">'
        'Reviewed by the Company Debt editorial team'
        '</p></noscript>'
    )

    return f'{hero_js}\n<div class="cc-hero-zone">\n{grid_html}\n{also_html}\n</div>\n{author_fallback}'
