#!/usr/bin/env python3
"""
Convert low-APR article HTML body into WordPress Gutenberg block markup.
Reads the HTML preview file, extracts the body, and outputs block-formatted JSON.
"""

import re
import json
import os
import tempfile

def build_blocks():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(base, 'preview', 'low-apr-business-credit-cards.html')

    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Extract body between verdict-box and </div></main>
    start = html.find('<div class="verdict-box">')
    end = html.find('\n</div>\n</main>')
    if start == -1 or end == -1:
        raise ValueError("Could not find content boundaries")

    body = html[start:end].strip()

    blocks = []

    def p(text):
        """Add a paragraph block."""
        blocks.append(f'<!-- wp:paragraph -->\n<p>{text.strip()}</p>\n<!-- /wp:paragraph -->')

    def h(level, text):
        """Add a heading block."""
        blocks.append(
            f'<!-- wp:heading {{"level":{level}}} -->\n'
            f'<h{level} class="wp-block-heading">{text.strip()}</h{level}>\n'
            f'<!-- /wp:heading -->'
        )

    def raw_html(markup):
        """Add a custom HTML block."""
        blocks.append(f'<!-- wp:html -->\n{markup.strip()}\n<!-- /wp:html -->')

    def table_block(table_html):
        """Add a table block."""
        blocks.append(
            f'<!-- wp:table {{"className":"is-style-stripes"}} -->\n'
            f'<figure class="wp-block-table is-style-stripes">{table_html.strip()}</figure>\n'
            f'<!-- /wp:table -->'
        )

    def list_block(list_html):
        """Add an ordered list block."""
        blocks.append(
            f'<!-- wp:list {{"ordered":true}} -->\n'
            f'{list_html.strip()}\n'
            f'<!-- /wp:list -->'
        )

    def group_start(class_name, style_str):
        """Open a group block."""
        blocks.append(
            f'<!-- wp:group {{"className":"{class_name}"}} -->\n'
            f'<div class="wp-block-group {class_name}" style="{style_str}">'
        )

    def group_end():
        blocks.append('</div>\n<!-- /wp:group -->')

    # --- Process the body section by section ---

    # 1. Verdict box
    vb = re.search(r'<div class="verdict-box">\s*<p>(.*?)</p>\s*</div>', body, re.DOTALL)
    if vb:
        group_start('verdict-box', 'border-left:4px solid #3b5bdb;background-color:#f0f4ff;padding:18px 20px;border-radius:0 6px 6px 0')
        p(vb.group(1))
        group_end()

    # 2. Everything between verdict-box and first card-block
    after_vb = body[vb.end():] if vb else body

    # Split into major chunks: card-blocks, tables, headings, paragraphs, lists, methodology
    # Strategy: use regex to find all top-level elements in order

    # First, identify card-block boundaries and other major elements
    # We'll process the content linearly

    # Remove the verdict box (already handled)
    remaining = after_vb.strip()

    # Process line by line / element by element
    pos = 0
    while pos < len(remaining):
        chunk = remaining[pos:]

        # Skip whitespace and HTML comments
        ws = re.match(r'\s*(?:<!--[^>]*-->)?\s*', chunk)
        if ws:
            pos += ws.end()
            chunk = remaining[pos:]
            if not chunk:
                break

        # Card block
        card_match = re.match(r'<div class="card-block">(.*?)\n  </div>', chunk, re.DOTALL)
        if card_match:
            card_inner = card_match.group(1)
            group_start('card-block', 'border:1px solid #e5e5e5;border-radius:6px;padding:22px 24px;background:#fafafa')

            # H3
            h3 = re.search(r'<h3[^>]*>(.*?)</h3>', card_inner, re.DOTALL)
            if h3:
                h(3, h3.group(1))

            # Card meta (as raw HTML block - custom layout)
            meta = re.search(r'(<div class="card-meta">.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>)', card_inner, re.DOTALL)
            if not meta:
                # Try simpler pattern
                meta = re.search(r'(<div class="card-meta">.*?)\n    </div>', card_inner, re.DOTALL)
            if meta:
                raw_html(meta.group(1).strip() + '\n    </div>')

            # Paragraphs after card-meta
            # Find all <p> tags in the card
            for pm in re.finditer(r'<p[^>]*>(.*?)</p>', card_inner, re.DOTALL):
                p(pm.group(1))

            group_end()
            pos += card_match.end()
            continue

        # Methodology section
        meth_match = re.match(r'<div class="methodology">(.*?)</div>\s*$', chunk, re.DOTALL)
        if meth_match:
            meth_inner = meth_match.group(1)
            group_start('methodology', 'border:1px solid #eee;border-radius:6px;padding:20px 24px;background:#f9f9f9')
            for elem in re.finditer(r'<(h2|p)[^>]*>(.*?)</\1>', meth_inner, re.DOTALL):
                if elem.group(1) == 'h2':
                    h(2, elem.group(2))
                else:
                    p(elem.group(2))
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
            h(level, h_match.group(2))
            pos += h_match.end()
            continue

        # Paragraph (including those with <em>)
        p_match = re.match(r'<p[^>]*>(.*?)</p>', chunk, re.DOTALL)
        if p_match:
            p(p_match.group(1))
            pos += p_match.end()
            continue

        # Standalone <em> (the verification note)
        em_match = re.match(r'<em>(.*?)</em>', chunk, re.DOTALL)
        if em_match:
            p(f'<em>{em_match.group(1)}</em>')
            pos += em_match.end()
            continue

        # Skip any unrecognized character
        pos += 1

    content = '\n\n'.join(blocks)
    print(f'Generated {len(blocks)} blocks')
    print(f'Content: {len(content)} chars')

    out_path = os.path.join(tempfile.gettempdir(), 'wp_push_blocks.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({'content': content}, f, ensure_ascii=False)
    print(f'Written to {out_path}')
    return out_path


if __name__ == '__main__':
    build_blocks()
