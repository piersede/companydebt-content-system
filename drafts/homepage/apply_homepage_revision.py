# -*- coding: utf-8 -*-
"""Apply the homepage relevance/hierarchy revision to page 55052 block markup.

Reads tmp/homepage-55052-original.html (exact DB dump), applies surgical
replacements + a top-level block reorder, writes tmp/homepage-55052-revised.html.

Every replacement asserts an exact expected hit count, so a stale anchor fails
the run instead of silently producing a half-edited page.
"""

import pathlib
import re
import sys

SRC = pathlib.Path("tmp/homepage-55052-original.html")
OUT = pathlib.Path("tmp/homepage-55052-revised.html")

c = SRC.read_text(encoding="utf-8")
orig_len = len(c)

# ── 1. Top-level block reorder ────────────────────────────────────────
# Offsets verified against the dump. Segments are top-level siblings, so
# slicing between consecutive starts yields complete blocks without needing
# to parse nesting.
BOUNDS = {
    "hero":      (0,     3185),
    "revhead":   (3185,  3405),
    "revwidget": (3405,  3491),
    "logos":     (3491,  5271),
    "licensed":  (5271,  8310),
    "why":       (8310,  11280),
    "services":  (11280, 19278),
    "sectors":   (19278, 20325),
    "nextsteps": (20325, 23185),
    "contact":   (23185, orig_len),
}

# Sanity-check each segment starts with the block we think it does.
EXPECT_START = {
    "hero":      '<!-- wp:acf/hero-blue ',
    "revhead":   '<!-- wp:heading {"textAlign":"center","level":2,"className":"cd-reviews-heading"} -->',
    "revwidget": '<!-- wp:acf/cd-reviews-widget ',
    "logos":     '<!-- wp:cover {"customOverlayColor":"#09285d"',
    "licensed":  '<!-- wp:cover {"customOverlayColor":"#f8f9fd"',
    "why":       '<!-- wp:cover {"overlayColor":"white","isUserOverlayColor":true,"minHeight":300',
    "services":  '<!-- wp:cover {"customOverlayColor":"#f8f9fd"',
    "sectors":   '<!-- wp:group {"className":"container home-blue"} -->',
    "nextsteps": '<!-- wp:acf/columns-with-buttons ',
    "contact":   '<!-- wp:cover {"overlayColor":"white","isUserOverlayColor":true,"isDark":false,"align":"wide"} -->',
}

seg = {}
for name, (a, b) in BOUNDS.items():
    s = c[a:b]
    if not s.startswith(EXPECT_START[name]):
        sys.exit(f"ERROR: segment '{name}' does not start as expected.\nGot: {s[:120]!r}")
    seg[name] = s

# Concatenation must be lossless.
if "".join(seg[k] for k in BOUNDS) != c:
    sys.exit("ERROR: segment split is not lossless")

# New order: answer the query, offer triage, then prove trust.
NEW_ORDER = [
    "hero",       # H1 + rewritten hero
    "services",   # Help With Limited Company Debt (was below reviews)
    "nextsteps",  # 30-second insolvency test, surfaced right after the routes
    "logos",      # press logos: compact trust band
    "why",        # Why Choose Company Debt
    "licensed",   # Licensed & Accredited Insolvency Practitioners
    "revhead",    # Trusted by UK Directors
    "revwidget",  # review carousel, now below the service answer
    "sectors",
    "contact",
]
assert sorted(NEW_ORDER) == sorted(BOUNDS), "reorder list must be a permutation"

# Normalise separators so blocks stay cleanly delimited after moving.
c = "\n\n".join(seg[k].strip("\n") for k in NEW_ORDER) + "\n"


# ── 2. Text replacements ──────────────────────────────────────────────
def sub(old, new, count=1, label=""):
    global c
    n = c.count(old)
    if n != count:
        sys.exit(f"ERROR [{label}]: expected {count} occurrence(s), found {n}\n  {old[:160]!r}")
    c = c.replace(old, new)
    print(f"  ok  {label}")


print("replacements:")

# H1
sub(
    '"block_hero_blue_title":"Expert Advice. Affordable Help.\\r\\n"',
    '"block_hero_blue_title":"Business Debt Advice for Limited Companies\\r\\n"',
    label="H1",
)

# Hero body prose (CTA group + trust bullets below it are left untouched)
sub(
    '"block_hero_blue_wysiwyg_left":"We provide clear, regulated advice to UK company '
    'directors. In one confidential call, we\'ll explain your options and help you take '
    'the right next step.\\r\\n\\r\\nIf rescue is possible, we’ll guide you through it. '
    'If not, we’ll close your company safely and minimise risk to you and your staff.\\r\\n',

    '"block_hero_blue_wysiwyg_left":"If your limited company is struggling with HMRC '
    'arrears, unpaid suppliers, loan repayments or creditor pressure, get clear business '
    'debt advice before the situation worsens.\\r\\n\\r\\nIn one confidential call, we’ll '
    'explain whether the company can recover, needs restructuring, or may need to close. '
    'If rescue is possible we’ll guide you through it. If not, we’ll close it safely '
    'and limit the risk to you and your staff.\\r\\n\\r\\nConfidential advice from licensed '
    'and regulated insolvency practitioners.\\r\\n',
    label="hero body",
)

# Soften unsubstantiated scale claim
sub(
    '<h2 class="wp-block-heading has-text-align-center cd-reviews-heading">Trusted by Thousands of UK Directors</h2>',
    '<h2 class="wp-block-heading has-text-align-center cd-reviews-heading">Trusted by UK Directors</h2>',
    label="reviews heading",
)

# Service section H2
sub(
    '<h2 class="wp-block-heading has-text-align-center has-text-color" style="color:#09285d">What We Can Help You With</h2>',
    '<h2 class="wp-block-heading has-text-align-center has-text-color" style="color:#09285d">Help With Limited Company Debt</h2>',
    label="service H2",
)

# Service intro: keep the core-expertise relevance, add triage framing + the
# one qualified liability line linking to the specialist guide.
sub(
    '<p class="has-text-align-center" style="font-size:18px">Our core expertise is helping '
    'limited company directors who face creditor pressure, cash flow problems, and '
    'debt-related issues. We offer practical and efficient methods of tackling debts through '
    'liquidation, administration, and other business rescue arrangements, with step by step '
    'guidance from a licensed practitioner.</p>\n'
    '<!-- /wp:paragraph -->',

    '<p class="has-text-align-center" style="font-size:18px">Our core expertise is helping '
    'limited company directors facing creditor pressure, cash flow problems and debts they '
    'cannot service. The right response depends on whether the business is still viable, '
    'which creditor is pressing hardest, and whether enforcement has already started.</p>\n'
    '<!-- /wp:paragraph -->\n\n'
    '<!-- wp:paragraph {"align":"center","style":{"typography":{"fontSize":"18px"}}} -->\n'
    '<p class="has-text-align-center" style="font-size:18px">Company debts normally belong to '
    'the company rather than to you personally, though '
    '<a href="/advice/are-directors-personally-liable-for-company-debts/">personal exposure '
    'can arise</a> through guarantees, an overdrawn director’s loan account or misconduct. '
    'Start with the situation that best describes yours.</p>\n'
    '<!-- /wp:paragraph -->',
    label="service intro + liability line",
)

# Relabel the vague card pointing at the Debt & Creditor Pressure Hub
sub('alt="General Debt Pressure"', 'alt="Debt and Creditor Pressure"', label="card alt")
sub(
    '<span class="cd-help-item-title">General Debt Pressure</span>',
    '<span class="cd-help-item-title">Debt &amp; Creditor Pressure</span>',
    label="card title",
)
sub(
    '<span class="cd-help-item-desc">A full review of your debts with actionable next steps.</span>',
    '<span class="cd-help-item-desc">A full review of your debts and creditor pressure, with clear next steps.</span>',
    label="card desc",
)

# Honest promise on the insolvency test now that it sits high on the page.
sub(
    '"buttons_section_buttons_1_description":"Take 30 seconds to know your exact situation and get the right advice"',
    '"buttons_section_buttons_1_description":"Answer five short questions for an initial assessment and your recommended next steps"',
    label="insolvency test description",
)


# ── 3. Rescue before closure in the third card group ──────────────────
# The site's own proposition is that rescue is explored before closure, but the
# column led with CVL. Reorder so the cards match the claim.
h3 = '<h3 class="wp-block-heading has-text-color" style="color:#09285d">Rescue and Closure Options</h3>'
start = c.index(h3)
end = c.index('<!-- /wp:column -->', start)
region = c[start:end]

cards = re.findall(r'<a class="cd-help-item cd-help-item-with-img".*?</a>', region, re.DOTALL)
if len(cards) != 4:
    sys.exit(f"ERROR: expected 4 rescue/closure cards, found {len(cards)}")

WANT = [
    "/company-rescue-solutions/company-voluntary-arrangement/",
    "/company-administration/",
    "/company-rescue-solutions/pre-packs/",
    "/liquidation/creditors-voluntary-liquidation/",
]
by_href = {}
for card in cards:
    href = re.search(r'href="([^"]+)"', card).group(1)
    by_href[href] = card
missing = [h for h in WANT if h not in by_href]
if missing:
    sys.exit(f"ERROR: rescue/closure cards missing hrefs: {missing}")

new_region = region
for card in cards:
    new_region = new_region.replace(card, "\x00CARD\x00", 1)
for href in WANT:
    new_region = new_region.replace("\x00CARD\x00", by_href[href], 1)

c = c[:start] + new_region + c[end:]
print("  ok  rescue-before-closure card order")


OUT.write_text(c, encoding="utf-8")
print(f"\noriginal len: {orig_len}")
print(f"revised len:  {len(c)}")
print(f"written:      {OUT}")
