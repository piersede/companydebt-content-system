#!/usr/bin/env python3
"""Build Gutenberg blocks with logos, card-meta, and CTA buttons."""

import json
import re
import os
import tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGOS = {
    'Lloyds': (54386, 'https://busexp1stg.wpengine.com/wp-content/uploads/2024/02/Lloyds-Mini-Header.png', 'Lloyds Bank logo'),
    'Metro Bank': (65794, 'https://busexp1stg.wpengine.com/wp-content/uploads/2024/12/metro-bank.png', 'Metro Bank logo'),
    'HSBC': (45726, 'https://busexp1stg.wpengine.com/wp-content/uploads/2023/08/HSBC-Commercial.png', 'HSBC logo'),
    'Santander': (65797, 'https://busexp1stg.wpengine.com/wp-content/uploads/2024/12/santander.png', 'Santander logo'),
    'NatWest': (45528, 'https://busexp1stg.wpengine.com/wp-content/uploads/2023/08/NatWest-Large.png', 'NatWest logo'),
    'Barclaycard': (65800, 'https://busexp1stg.wpengine.com/wp-content/uploads/2024/12/barclaycard.png', 'Barclaycard logo'),
    'Capital on Tap': (69230, 'https://busexp1stg.wpengine.com/wp-content/uploads/2025/06/capitalontap.png', 'Capital on Tap logo'),
}

CTAS = {
    'Lloyds': 'https://www.lloydsbank.com/business/business-cards/business-credit-card.html',
    'Metro Bank': 'https://www.metrobankonline.co.uk/business/borrowing/products/credit-card/',
    'HSBC': 'https://www.business.hsbc.uk/en-gb/products/business-credit-card',
    'Santander': 'https://www.santander.co.uk/business/credit-cards',
    'NatWest': 'https://www.natwest.com/business/cards/business-credit-card.html',
    'Barclaycard': 'https://www.barclaycard.co.uk/business/cards/credit-cards/select-cashback',
    'Capital on Tap': 'https://www.capitalontap.com/en/business-credit-cards/',
}

blocks = []


def add(text):
    blocks.append(text)


def para(text):
    add(f'<!-- wp:paragraph -->\n<p>{text.strip()}</p>\n<!-- /wp:paragraph -->')


def heading(level, text):
    add(
        f'<!-- wp:heading {{"level":{level}}} -->\n'
        f'<h{level} class="wp-block-heading">{text.strip()}</h{level}>\n'
        f'<!-- /wp:heading -->'
    )


def img_block(bank):
    mid, url, alt = LOGOS[bank]
    # Uniform container: 317x200px with object-fit:contain for all logos
    add(
        f'<!-- wp:html -->\n'
        f'<div style="background:#f8f2ff;border-radius:6px;width:317px;height:200px;'
        f'display:flex;align-items:center;justify-content:center;padding:20px;'
        f'margin-bottom:16px;box-sizing:border-box">'
        f'<img src="{url}" alt="{alt}" '
        f'style="max-width:100%;max-height:160px;object-fit:contain;display:block"/>'
        f'</div>\n'
        f'<!-- /wp:html -->'
    )


def cta_block(bank):
    url = CTAS.get(bank, '#')
    add(
        f'<!-- wp:buttons -->\n'
        f'<div class="wp-block-buttons">'
        f'<!-- wp:button {{"style":{{"border":{{"radius":"10px"}}}},"className":"is-style-fill"}} -->\n'
        f'<div class="wp-block-button is-style-fill">'
        f'<a class="wp-block-button__link wp-element-button" href="{url}" '
        f'style="border-radius:10px;background-color:#7a3f9d" target="_blank" rel="noopener noreferrer">'
        f'View {bank} Card</a>'
        f'</div>\n'
        f'<!-- /wp:button -->'
        f'</div>\n'
        f'<!-- /wp:buttons -->'
    )


def table_block(thtml):
    add(
        f'<!-- wp:table {{"className":"is-style-stripes"}} -->\n'
        f'<figure class="wp-block-table is-style-stripes">{thtml.strip()}</figure>\n'
        f'<!-- /wp:table -->'
    )


def list_block(lhtml):
    add(f'<!-- wp:list {{"ordered":true}} -->\n{lhtml.strip()}\n<!-- /wp:list -->')


def group_start(cls, style):
    add(
        f'<!-- wp:group {{"className":"{cls}"}} -->\n'
        f'<div class="wp-block-group {cls}" style="{style}">'
    )


def group_end():
    add('</div>\n<!-- /wp:group -->')


def raw_html(markup):
    add(f'<!-- wp:html -->\n{markup.strip()}\n<!-- /wp:html -->')


def detect_bank(card_html):
    """Detect bank from H3 heading only, not full card body text."""
    h3 = re.search(r'<h3[^>]*>(.*?)</h3>', card_html, re.DOTALL)
    if h3:
        title = h3.group(1).lower()
        for bank in LOGOS:
            if bank.lower() in title:
                return bank
    return None


def main():
    html_path = os.path.join(BASE, 'preview', 'low-apr-business-credit-cards.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    start = html.find('<div class="verdict-box">')
    end = html.find('\n</div>\n</main>')
    body = html[start:end].strip()

    # 1. Verdict box
    vb = re.search(r'<div class="verdict-box">\s*<p>(.*?)</p>\s*</div>', body, re.DOTALL)
    if vb:
        group_start('verdict-box',
                     'border-left:4px solid #3b5bdb;background-color:#f0f4ff;'
                     'padding:18px 20px;border-radius:0 6px 6px 0')
        para(vb.group(1))
        group_end()

    remaining = body[vb.end():].strip() if vb else body
    pos = 0

    while pos < len(remaining):
        chunk = remaining[pos:]

        # Skip whitespace and HTML comments
        ws = re.match(r'\s*(?:<!--[^>]*-->)?\s*', chunk)
        if ws and ws.end() > 0:
            pos += ws.end()
            chunk = remaining[pos:]
            if not chunk:
                break

        # Card block
        card_match = re.match(r'<div class="card-block">(.*?)\n  </div>', chunk, re.DOTALL)
        if card_match:
            card_inner = card_match.group(1)
            bank = detect_bank(card_inner)

            group_start('card-block',
                        'border:1px solid #e5e5e5;border-radius:6px;'
                        'padding:22px 24px;background:#fafafa;'
                        'margin-bottom:32px')

            # Logo image
            if bank and bank in LOGOS:
                img_block(bank)

            # H3
            h3 = re.search(r'<h3[^>]*>(.*?)</h3>', card_inner, re.DOTALL)
            if h3:
                heading(3, h3.group(1))

            # Card meta — render as raw HTML block
            meta = re.search(r'(<div class="card-meta">.*?)\n    </div>', card_inner, re.DOTALL)
            if meta:
                raw_html(meta.group(1).strip() + '\n    </div>')

            # Paragraphs
            for pm in re.finditer(r'<p[^>]*>(.*?)</p>', card_inner, re.DOTALL):
                para(pm.group(1))

            # CTA button
            if bank and bank in CTAS:
                cta_block(bank)

            group_end()
            pos += card_match.end()
            continue

        # Methodology section
        meth_match = re.match(r'<div class="methodology">(.*?)</div>\s*$', chunk, re.DOTALL)
        if meth_match:
            meth_inner = meth_match.group(1)
            group_start('methodology',
                        'border:1px solid #eee;border-radius:6px;'
                        'padding:20px 24px;background:#f9f9f9')
            for elem in re.finditer(r'<(h2|p)[^>]*>(.*?)</\1>', meth_inner, re.DOTALL):
                if elem.group(1) == 'h2':
                    heading(2, elem.group(2))
                else:
                    para(elem.group(2))
            group_end()
            pos += meth_match.end()
            continue

        # Table
        tbl_match = re.match(r'(<table.*?</table>)', chunk, re.DOTALL)
        if tbl_match:
            table_block(tbl_match.group(1))
            pos += tbl_match.end()
            continue

        # Ordered list
        ol_match = re.match(r'(<ol.*?</ol>)', chunk, re.DOTALL)
        if ol_match:
            list_block(ol_match.group(1))
            pos += ol_match.end()
            continue

        # Heading
        h_match = re.match(r'<(h[1-6])[^>]*>(.*?)</\1>', chunk, re.DOTALL)
        if h_match:
            level = int(h_match.group(1)[1])
            heading(level, h_match.group(2))
            pos += h_match.end()
            continue

        # Paragraph
        p_match = re.match(r'<p[^>]*>(.*?)</p>', chunk, re.DOTALL)
        if p_match:
            para(p_match.group(1))
            pos += p_match.end()
            continue

        # Standalone em
        em_match = re.match(r'<em>(.*?)</em>', chunk, re.DOTALL)
        if em_match:
            para(f'<em>{em_match.group(1)}</em>')
            pos += em_match.end()
            continue

        pos += 1

    content = '\n\n'.join(blocks)
    print(f'Generated {len(blocks)} blocks, {len(content)} chars')

    out_path = os.path.join(tempfile.gettempdir(), 'wp_push_final.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({'content': content}, f, ensure_ascii=False)
    print(f'Written to {out_path}')


if __name__ == '__main__':
    main()
