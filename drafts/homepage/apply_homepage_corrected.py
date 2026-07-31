# -*- coding: utf-8 -*-
"""Apply the CORRECTED homepage brief to page 55052.

Base is the ORIGINAL pre-change dump, not the previous revision, so the
authority-first section order, "Trusted by Thousands of UK Directors" and
"What We Can Help You With" are all restored by construction rather than by
un-picking edits.

Per section 10 ("Claude should make only the following changes"), this applies:
  1. H1 -> "Limited Company Debt Advice"
  2. strapline retained as supporting copy, not the H1
  3. hero rewritten to two short sentences
  4. original section order preserved (base file already has it)
  5. "thousands" retained (untouched in base)
  6. "What We Can Help You With" retained (untouched in base)
  7. rescue options before liquidation (the one improvement this brief keeps)
 11. "businesses" qualified where it could imply sole traders are served

Every replacement asserts an exact hit count so a stale anchor fails loudly.
"""

import pathlib
import re
import sys

SRC = pathlib.Path("tmp/homepage-55052-original.html")
OUT = pathlib.Path("tmp/homepage-55052-corrected.html")

c = SRC.read_text(encoding="utf-8")
orig_len = len(c)


def sub(old, new, label, count=1):
    global c
    n = c.count(old)
    if n != count:
        sys.exit(f"ERROR [{label}]: expected {count}, found {n}\n  {old[:150]!r}")
    c = c.replace(old, new)
    print(f"  ok  {label}")


print("replacements:")

# ── 1 + 2 + 3. Hero ───────────────────────────────────────────────────
sub(
    '"block_hero_blue_title":"Expert Advice. Affordable Help.\\r\\n"',
    '"block_hero_blue_title":"Limited Company Debt Advice\\r\\n"',
    "H1 -> Limited Company Debt Advice",
)

# The ACF hero block has only a title field and a wysiwyg field: there is no
# eyebrow/strapline field, so the strapline is carried as the first line of the
# body. Inline style because there is no safe shared stylesheet to add a rule to.
STRAPLINE = (
    '\\u003cspan class=\\u0022cd-hero-strapline\\u0022 style=\\u0022display:block;'
    'font-size:14px;letter-spacing:0.12em;text-transform:uppercase;opacity:0.85;'
    'margin-bottom:14px;\\u0022\\u003eExpert Advice. Affordable Help.\\u003c/span\\u003e'
)

sub(
    '"block_hero_blue_wysiwyg_left":"We provide clear, regulated advice to UK company '
    'directors. In one confidential call, we\'ll explain your options and help you take '
    'the right next step.\\r\\n\\r\\nIf rescue is possible, we’ll guide you through it. '
    'If not, we’ll close your company safely and minimise risk to you and your staff.\\r\\n',

    '"block_hero_blue_wysiwyg_left":"' + STRAPLINE + '\\r\\n\\r\\n'
    'Confidential advice for directors of UK limited companies facing HMRC arrears, '
    'creditor pressure, unpaid suppliers or cash-flow problems. Understand the options '
    'for rescue, restructuring or closure before the situation worsens.\\r\\n',
    "hero: strapline + two short sentences",
)

# ── 11. Qualify "businesses" so sole traders are not implied ──────────
sub(
    '<li>Specialists in advising Small and Medium-Sized Businesses</li>',
    '<li>Specialists in advising small and medium-sized limited companies</li>',
    "qualify: Why Choose bullet",
)
sub(
    'Company Debt supports SMEs throughout the UK with hands-on insolvency and restructuring advice.',
    'Company Debt supports SME limited companies throughout the UK with hands-on insolvency and restructuring advice.',
    "qualify: SME sentence",
)
sub(
    'We Help Small &amp; Medium Businesses <span class="orange-underline">Just Like You</span>',
    'We Help Small &amp; Medium Companies <span class="orange-underline">Just Like You</span>',
    "qualify: sectors heading",
)


# ── 7. Rescue and restructuring before liquidation ───────────────────
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
by_href = {re.search(r'href="([^"]+)"', card).group(1): card for card in cards}
missing = [h for h in WANT if h not in by_href]
if missing:
    sys.exit(f"ERROR: missing hrefs: {missing}")

new_region = region
for card in cards:
    new_region = new_region.replace(card, "\x00C\x00", 1)
for href in WANT:
    new_region = new_region.replace("\x00C\x00", by_href[href], 1)

c = c[:start] + new_region + c[end:]
print("  ok  rescue before liquidation (CVA, Administration, Pre-Pack, CVL)")


# ── Guard: things this brief says must NOT change ────────────────────
MUST_KEEP = {
    "Trusted by Thousands of UK Directors": 1,
    "What We Can Help You With": 1,
    "General Debt Pressure": 2,          # alt attribute + card title
}
print("\nmust-keep guard:")
for phrase, expected in MUST_KEEP.items():
    n = c.count(phrase)
    if n != expected:
        sys.exit(f"ERROR: '{phrase}' count {n}, expected {expected}")
    print(f"  ok  '{phrase}' present ({n})")

# Section order must match the original exactly.
def order(s):
    keys = [
        ('hero', '<!-- wp:acf/hero-blue '),
        ('reviews', '"className":"cd-reviews-heading"'),
        ('logos', '"customOverlayColor":"#09285d"'),
        ('accreditations', 'Licensed &amp; Accredited</span> Insolvency Practitioners'),
        ('why', 'Why Choose</span> Company Debt'),
        ('services', 'What We Can Help You With'),
        ('sectors', 'We Help Small &amp; Medium Companies'),
        ('contact', 'Contact Us Today'),
    ]
    return [k for k, _ in sorted(((k, s.index(v)) for k, v in keys), key=lambda t: t[1])]

got = order(c)
EXPECT = ['hero', 'reviews', 'logos', 'accreditations', 'why', 'services', 'sectors', 'contact']
if got != EXPECT:
    sys.exit(f"ERROR: section order is {got}, expected {EXPECT}")
print(f"  ok  authority-first order preserved: {' > '.join(got)}")

OUT.write_text(c, encoding="utf-8")
print(f"\noriginal len: {orig_len}\ncorrected len: {len(c)}\nwritten: {OUT}")
