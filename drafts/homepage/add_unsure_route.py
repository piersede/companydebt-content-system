# -*- coding: utf-8 -*-
"""Add the 'Not sure which applies?' triage route after the service cards.

The acf/columns-with-buttons block that used to carry the 30-second insolvency
test link renders NOTHING on the front end (verified: no matching element in
the DOM, and it was already dead before this revision). So moving it up the
page does not actually surface the test. This adds the route as core Gutenberg
blocks, which do render.

Wording is deliberately conservative: the growth audit verified the test gates
its result behind mandatory name/email/phone and replies by callback, so this
does not promise an instant on-screen verdict.
"""

import pathlib
import sys

SRC = pathlib.Path("tmp/homepage-55052-revised.html")
OUT = pathlib.Path("tmp/homepage-55052-revised2.html")

c = SRC.read_text(encoding="utf-8")

# Anchor on the service-card columns specifically.
anchor = '<!-- wp:columns {"className":"cd-help-cards"} -->'
if c.count(anchor) != 1:
    sys.exit(f"ERROR: expected 1 cd-help-cards columns block, found {c.count(anchor)}")
start = c.index(anchor)

close = '<!-- /wp:columns --></div>\n<!-- /wp:group -->'
idx = c.find(close, start)
if idx == -1:
    sys.exit("ERROR: could not find the closing columns/group pair for the service cards")

NEW = (
    '<!-- /wp:columns -->\n\n'
    '<!-- wp:paragraph {"align":"center","className":"cd-help-unsure",'
    '"style":{"typography":{"fontSize":"18px"}}} -->\n'
    '<p class="has-text-align-center cd-help-unsure" style="font-size:18px">'
    '<strong>Not sure which applies?</strong> Answer five short questions in our '
    '<a href="/insolvency-calculator/">insolvency test</a> and we will come back to you '
    'with an initial assessment, or call <a href="tel:08000746757">0800 074 6757</a> '
    'to speak to a licensed practitioner.</p>\n'
    '<!-- /wp:paragraph --></div>\n'
    '<!-- /wp:group -->'
)

c = c[:idx] + NEW + c[idx + len(close):]
OUT.write_text(c, encoding="utf-8")
print(f"written: {OUT}  ({len(c)} chars)")
