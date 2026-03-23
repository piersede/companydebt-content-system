"""Single-product review page assembler.

Used for pages like "Capital on Tap Review", "Funding Circle Review".
Focuses on one card/product with expanded editorial depth.
"""

from __future__ import annotations
from cc_builder.gutenberg import PageBuilder
from cc_builder.css import CC_TOC_CSS, CC_CARD_CSS, CC_HERO_CSS, CC_COMPARISON_TABLE_CSS, generate_editorial_css
from cc_builder.js import CC_TOC_HTML, CC_TOC_JS, CC_TOC_START, CC_COMPARISON_TABLE_JS
from cc_builder.components import build_card_html, build_section_divider, build_faq_html, build_article_schema
from cc_builder.hero import build_hero_zone


def assemble(config: dict, cards: list[dict], separate_cards: list[dict] | None = None) -> str:
    """Assemble a single-product review page.

    Args:
        config: Page configuration with 'sections' list.
        cards: Usually a single card (the reviewed product).
        separate_cards: Optional alternative cards mentioned.

    Section types (in addition to roundup types):
        review_card    - The main reviewed product card (expanded)
        pros_cons      - Structured pros/cons list
        alternatives   - Brief mention of alternative cards
        faq            - FAQ accordion with schema markup
    """
    pb = PageBuilder()

    # If hero_zone is present, collect verdict text for it and suppress standalone verdict_box
    has_hero = config.get('hero') and any(s['type'] == 'hero_zone' for s in config['sections'])
    verdict_text = ''
    if has_hero:
        for s in config['sections']:
            if s['type'] == 'verdict_box':
                verdict_text = s.get('text', '')
                break

    for section in config['sections']:
        stype = section['type']

        if stype == 'css':
            pb.raw_html(CC_TOC_CSS)
            pb.raw_html(CC_CARD_CSS)
            pb.raw_html(CC_COMPARISON_TABLE_CSS)
            if config.get('hero'):
                pb.raw_html(CC_HERO_CSS)
            # Editorial layout CSS (no comparison table for reviews)
            pb.raw_html(generate_editorial_css(
                config['wp_page_id'], include_comparison_table=False))
            # Page-specific CSS overrides
            if config.get('page_css'):
                pb.raw_html(f'<style>\n{config["page_css"]}\n</style>')

        elif stype == 'toc':
            pb.raw_html(CC_TOC_HTML)

        elif stype == 'verdict_box':
            if has_hero:
                continue
            pb.group_start(
                'verdict-box',
                'border-left:4px solid #3b5bdb;background-color:#f0f4ff;'
                'padding:18px 20px;border-radius:0 6px 6px 0'
            )
            pb.para(section['text'])
            pb.group_end()

        elif stype == 'prose':
            for p in section['paragraphs']:
                pb.para(p)

        elif stype == 'heading':
            pb.heading(section.get('level', 2), section['text'])

        elif stype == 'table':
            pb.table_block(section['html'])

        elif stype == 'list':
            pb.list_block(section['html'])

        elif stype == 'divider':
            pb.raw_html(build_section_divider(section.get('label', 'Full review')))

        elif stype == 'review_card':
            # Render the main reviewed card
            if cards:
                pb.raw_html(build_card_html(cards[0]))

        elif stype == 'card_list':
            for card in cards:
                pb.raw_html(build_card_html(card))

        elif stype == 'card_list_separate':
            if separate_cards:
                for card in separate_cards:
                    pb.raw_html(build_card_html(card))

        elif stype == 'alternatives':
            # Brief cards for alternatives section
            if separate_cards:
                for card in separate_cards:
                    pb.raw_html(build_card_html(card))

        elif stype == 'pros_cons':
            # Structured pros/cons
            pros_html = ''.join(f'<li>{p}</li>' for p in section.get('pros', []))
            cons_html = ''.join(f'<li>{c}</li>' for c in section.get('cons', []))
            html = (
                f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;margin:16px 0">'
                f'<div style="padding:16px 20px;border-left:3px solid #2e7d32;background:#f8fdf8;border-radius:0 6px 6px 0">'
                f'<strong style="color:#1b6e1f;font-size:13px;text-transform:uppercase;letter-spacing:0.05em">Strengths</strong>'
                f'<ul style="margin:8px 0 0;padding-left:18px;font-size:14px;line-height:1.6">{pros_html}</ul></div>'
                f'<div style="padding:16px 20px;border-left:3px solid #d48806;background:#fffbf5;border-radius:0 6px 6px 0">'
                f'<strong style="color:#a86a00;font-size:13px;text-transform:uppercase;letter-spacing:0.05em">Limitations</strong>'
                f'<ul style="margin:8px 0 0;padding-left:18px;font-size:14px;line-height:1.6">{cons_html}</ul></div>'
                f'</div>'
            )
            pb.raw_html(html)

        elif stype == 'comparison_table':
            if 'html' in section:
                pb.table_block(section['html'])
            else:
                from cc_builder.components import build_v4_comparison_table
                ct_config = section.get('config') or config.get('comparison_table_config', {})
                card_scope = section.get('cards', 'all')
                if card_scope == 'main':
                    ct_cards = list(cards)
                elif card_scope == 'separate':
                    ct_cards = list(separate_cards or [])
                else:
                    ct_cards = cards + (separate_cards or [])
                pb.raw_html(build_v4_comparison_table(ct_cards, ct_config, config))

        elif stype == 'methodology':
            pb.group_start(
                'methodology',
                'border:1px solid #eee;border-radius:6px;'
                'padding:20px 24px 28px 24px;background:#f9f9f9'
            )
            for p in section['paragraphs']:
                pb.para(p)
            pb.group_end()

        elif stype == 'hero_zone':
            all_cards = list(cards) + (separate_cards or [])
            hero_html = build_hero_zone(config, all_cards, verdict_text=verdict_text)
            if hero_html:
                pb.raw_html(hero_html)

        elif stype == 'toc_start':
            pb.raw_html(CC_TOC_START)

        elif stype == 'faq':
            faq_out = build_faq_html(section.get('items', []))
            if faq_out:
                pb.raw_html(faq_out)

        elif stype == 'spacer':
            pb.para('&nbsp;')

        elif stype == 'toc_js':
            pb.raw_html(CC_TOC_JS)
            pb.raw_html(CC_COMPARISON_TABLE_JS)
            schema = build_article_schema(config)
            if schema:
                pb.raw_html(schema)

    return pb.build()
