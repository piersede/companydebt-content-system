#!/usr/bin/env python3
"""Build a LinkedIn PDF carousel from a slide spec.

House visual system (social/linkedin-calendar-2026-07.md section 4):
  1080 x 1350 (4:5 portrait), navy base, ONE orange number per slide,
  under 25 words per slide, Lato, source footer + wordmark on every slide.

Usage:
    python scripts/build_social_carousel.py --post 1
    python scripts/build_social_carousel.py --post 1 --out social/assets/

Slide specs live in SLIDES below, keyed by post number, so regenerating a
carousel after a copy change is a one-liner rather than a rebuild.
"""
import argparse
import os
import sys

from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# --- house tokens -----------------------------------------------------------
NAVY = HexColor("#002856")
ORANGE = HexColor("#ff6600")
PANEL = HexColor("#e7f6fd")
MIDBLUE = HexColor("#98b0c5")
WHITE = HexColor("#ffffff")

W, H = 1080, 1350
MARGIN = 84

FONT_DIR = os.path.join("theme", "public", "fonts")
FONTS = {
    "Lato-Black": "lato-v17-latin-900.ttf",
    "Lato-Bold": "lato-v17-latin-700.ttf",
    "Lato": "lato-v17-latin-regular.ttf",
    "Lato-Light": "lato-v17-latin-300.ttf",
}

FOOTER_SOURCE = "Source: Insolvency Service, June 2026"
FOOTER_URL = "companydebt.com/data"
WORDMARK = "CompanyDebt"


def register_fonts(root):
    for name, filename in FONTS.items():
        path = os.path.join(root, FONT_DIR, filename)
        if not os.path.exists(path):
            sys.exit(f"Missing font: {path}")
        pdfmetrics.registerFont(TTFont(name, path))


# --- drawing helpers --------------------------------------------------------
# Vertical band available for content: above the footer, below the top margin.
BAND_TOP = 1250
BAND_BOTTOM = 130
COL = W - 2 * MARGIN

# One optical size for every headline number, so 14 and 1,845 carry equal weight.
NUM_SIZE = 300
NUM_CAP = NUM_SIZE * 0.72


def wrap(c, text, font, size, max_width):
    c.setFont(font, size)
    return simpleSplit(text, font, size, max_width)


def fit_size(text, font, max_width, preferred):
    """Shrink to fit the column, never grow past the preferred size."""
    w = pdfmetrics.stringWidth(text, font, preferred)
    return preferred if w <= max_width else preferred * max_width / w


def centre_start(block_h):
    """Top y for a block of block_h, optically centred in the content band."""
    return BAND_BOTTOM + (BAND_TOP - BAND_BOTTOM + block_h) / 2


def draw_wrapped(c, text, font, size, colour, x, y, max_width, leading=None):
    """Draw wrapped text downward from y. Returns the y below the last line."""
    leading = leading or size * 1.25
    c.setFillColor(colour)
    c.setFont(font, size)
    for line in wrap(c, text, font, size, max_width):
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_chrome(c, slide_no, total, source=FOOTER_SOURCE, url=FOOTER_URL):
    """Footer source line, url, wordmark and slide counter. Every slide.

    total <= 1 marks a single-image post: no slide counter is drawn.
    An empty source string omits the source line (for non-data posts).
    """
    if source:
        c.setFont("Lato", 20)
        c.setFillColor(MIDBLUE)
        c.drawString(MARGIN, 74, source)
    c.setFont("Lato-Bold", 20)
    c.setFillColor(MIDBLUE)
    c.drawString(MARGIN, 44, url)

    c.setFont("Lato-Black", 20)
    c.setFillColor(WHITE)
    c.drawRightString(W - MARGIN, 44, WORDMARK)

    if total > 1:
        c.setFont("Lato", 18)
        c.setFillColor(MIDBLUE)
        c.drawRightString(W - MARGIN, 74, f"{slide_no}/{total}")


KICKER_SIZE = 32
SUB_SIZE = 50
SUB_LEAD = 66
GAP_KICKER = 56
GAP_SUB = 66
RULE_H = 8


def big_number(c, value, sub, kicker=None):
    """The canonical slide: one orange number, one supporting line, centred."""
    size = fit_size(value, "Lato-Black", COL, NUM_SIZE)
    cap = size * 0.72
    sub_lines = wrap(c, sub, "Lato", SUB_SIZE, COL)

    block = cap + GAP_SUB + RULE_H + GAP_SUB + len(sub_lines) * SUB_LEAD
    if kicker:
        block += KICKER_SIZE + GAP_KICKER
    y = centre_start(block)

    if kicker:
        c.setFont("Lato-Bold", KICKER_SIZE)
        c.setFillColor(MIDBLUE)
        c.drawString(MARGIN, y - KICKER_SIZE, kicker.upper())
        y -= KICKER_SIZE + GAP_KICKER

    c.setFont("Lato-Black", size)
    c.setFillColor(ORANGE)
    c.drawString(MARGIN, y - cap, value)
    y -= cap + GAP_SUB

    c.setFillColor(ORANGE)
    c.rect(MARGIN, y, 120, RULE_H, stroke=0, fill=1)
    y -= GAP_SUB

    c.setFont("Lato", SUB_SIZE)
    c.setFillColor(WHITE)
    for line in sub_lines:
        y -= SUB_SIZE
        c.drawString(MARGIN, y, line)
        y -= SUB_LEAD - SUB_SIZE


def statement(c, text):
    lines = text.split("\n")
    # Largest size (capped at 88) at which every line fits the column.
    size = min([88] + [fit_size(line, "Lato-Black", COL, 88) for line in lines])
    lead = size * 1.22
    y = centre_start(len(lines) * lead)
    c.setFillColor(WHITE)
    c.setFont("Lato-Black", size)
    for line in lines:
        y -= size
        c.drawString(MARGIN, y, line)
        y -= lead - size


def stacked_bar(c):
    """Slide 3: composition of the 1,845. Orange is the administrations slice."""
    total = 1845
    segments = [
        ("CVL", 1364, MIDBLUE),
        ("Compulsory", 276, PANEL),
        ("Administrations", 191, ORANGE),
        ("CVA", 14, WHITE),
    ]
    head_size, bar_h, row = 46, 150, 84
    block = head_size + GAP_KICKER + bar_h + GAP_SUB + len(segments) * row
    y = centre_start(block)

    c.setFont("Lato-Black", head_size)
    c.setFillColor(WHITE)
    c.drawString(MARGIN, y - head_size, "What the 1,845 is made of")
    y -= head_size + GAP_KICKER

    x = MARGIN
    for _, value, colour in segments:
        seg = COL * value / total
        c.setFillColor(colour)
        c.rect(x, y - bar_h, seg, bar_h, stroke=0, fill=1)
        x += seg
    y -= bar_h + GAP_SUB

    for label, value, colour in segments:
        y -= row
        c.setFillColor(colour)
        c.rect(MARGIN, y + 8, 40, 40, stroke=0, fill=1)
        c.setFillColor(WHITE)
        c.setFont("Lato-Black", 46)
        c.drawString(MARGIN + 72, y + 6, f"{value:,}")
        c.setFont("Lato", 46)
        c.setFillColor(MIDBLUE)
        c.drawString(MARGIN + 270, y + 6, label)


def panel_note(c, heading, body):
    """A light panel for plain-English explainer slides."""
    pad, body_size, body_lead = 52, 52, 68
    lines = wrap(c, body, "Lato-Bold", body_size, COL - 2 * pad)
    box_h = len(lines) * body_lead + 2 * pad
    block = KICKER_SIZE + GAP_KICKER + box_h
    y = centre_start(block)

    c.setFont("Lato-Bold", KICKER_SIZE)
    c.setFillColor(MIDBLUE)
    c.drawString(MARGIN, y - KICKER_SIZE, heading.upper())
    y -= KICKER_SIZE + GAP_KICKER

    c.setFillColor(PANEL)
    c.rect(MARGIN, y - box_h, COL, box_h, stroke=0, fill=1)
    c.setFillColor(ORANGE)
    c.rect(MARGIN, y - box_h, 12, box_h, stroke=0, fill=1)

    ty = y - pad
    c.setFillColor(NAVY)
    c.setFont("Lato-Bold", body_size)
    for line in lines:
        ty -= body_size
        c.drawString(MARGIN + pad + 12, ty, line)
        ty -= body_lead - body_size


def mythcard(c, kicker, lines, sub, cta=None):
    """Single-image statement card. `lines` is a list of (text, colour_key)
    where colour_key in {'white','orange'}; each is one big headline line.
    For myth/legal posts that carry no number to verify.
    """
    palette = {"white": WHITE, "orange": ORANGE}
    head_size = 92
    head_lead = head_size * 1.16
    sub_lines = wrap(c, sub, "Lato", SUB_SIZE, COL)
    cta_lines = wrap(c, cta, "Lato-Bold", 34, COL) if cta else []

    block = (KICKER_SIZE + GAP_KICKER + len(lines) * head_lead + GAP_SUB
             + len(sub_lines) * SUB_LEAD + (GAP_SUB + len(cta_lines) * 46 if cta_lines else 0))
    y = centre_start(block)

    c.setFont("Lato-Bold", KICKER_SIZE)
    c.setFillColor(MIDBLUE)
    c.drawString(MARGIN, y - KICKER_SIZE, kicker.upper())
    y -= KICKER_SIZE + GAP_KICKER

    c.setFont("Lato-Black", head_size)
    for text, ck in lines:
        y -= head_size
        c.setFillColor(palette[ck])
        c.drawString(MARGIN, y, text)
        y -= head_lead - head_size
    y -= GAP_SUB

    c.setFont("Lato", SUB_SIZE)
    c.setFillColor(WHITE)
    for line in sub_lines:
        y -= SUB_SIZE
        c.drawString(MARGIN, y, line)
        y -= SUB_LEAD - SUB_SIZE

    if cta_lines:
        y -= GAP_SUB
        c.setFillColor(ORANGE)
        c.rect(MARGIN, y - 4, 120, RULE_H, stroke=0, fill=1)
        y -= GAP_SUB - 10
        c.setFont("Lato-Bold", 34)
        c.setFillColor(MIDBLUE)
        for line in cta_lines:
            y -= 34
            c.drawString(MARGIN, y, line)
            y -= 12


def title(c, kicker, head, sub=None):
    """Carousel cover: kicker, large headline, optional sub."""
    head_size = 76
    head_lead = head_size * 1.16
    head_lines = wrap(c, head, "Lato-Black", head_size, COL)
    sub_lines = wrap(c, sub, "Lato", SUB_SIZE, COL) if sub else []
    block = (KICKER_SIZE + GAP_KICKER + len(head_lines) * head_lead
             + (GAP_SUB + len(sub_lines) * SUB_LEAD if sub_lines else 0))
    y = centre_start(block)

    c.setFont("Lato-Bold", KICKER_SIZE)
    c.setFillColor(ORANGE)
    c.drawString(MARGIN, y - KICKER_SIZE, kicker.upper())
    y -= KICKER_SIZE + GAP_KICKER

    c.setFont("Lato-Black", head_size)
    c.setFillColor(WHITE)
    for line in head_lines:
        y -= head_size
        c.drawString(MARGIN, y, line)
        y -= head_lead - head_size
    if sub_lines:
        y -= GAP_SUB
        c.setFont("Lato", SUB_SIZE)
        c.setFillColor(MIDBLUE)
        for line in sub_lines:
            y -= SUB_SIZE
            c.drawString(MARGIN, y, line)
            y -= SUB_LEAD - SUB_SIZE


def sign(c, n, text, of=7, label="SIGN"):
    """Numbered list slide: one big orange numeral, one white statement.

    `label` sets the index word (SIGN, MISTAKE, STEP, ...).
    """
    num_size, stmt_size = 200, 60
    stmt_lead = stmt_size * 1.2
    stmt_lines = wrap(c, text, "Lato-Black", stmt_size, COL)
    block = KICKER_SIZE + 30 + num_size * 0.72 + GAP_SUB + len(stmt_lines) * stmt_lead
    y = centre_start(block)

    c.setFont("Lato-Bold", KICKER_SIZE)
    c.setFillColor(MIDBLUE)
    c.drawString(MARGIN, y - KICKER_SIZE, f"{label} {n} OF {of}")
    y -= KICKER_SIZE + 30

    c.setFont("Lato-Black", num_size)
    c.setFillColor(ORANGE)
    c.drawString(MARGIN, y - num_size * 0.72, str(n))
    y -= num_size * 0.72 + GAP_SUB

    c.setFont("Lato-Black", stmt_size)
    c.setFillColor(WHITE)
    for line in stmt_lines:
        y -= stmt_size
        c.drawString(MARGIN, y, line)
        y -= stmt_lead - stmt_size


def cta(c, head, url, sub=None):
    """Closing slide: white headline, orange rule, orange url."""
    head_size = 66
    head_lead = head_size * 1.18
    head_lines = wrap(c, head, "Lato-Black", head_size, COL)
    sub_lines = wrap(c, sub, "Lato", SUB_SIZE, COL) if sub else []
    block = (len(head_lines) * head_lead + GAP_SUB + RULE_H + GAP_SUB + 54
             + (GAP_SUB + len(sub_lines) * SUB_LEAD if sub_lines else 0))
    y = centre_start(block)

    c.setFont("Lato-Black", head_size)
    c.setFillColor(WHITE)
    for line in head_lines:
        y -= head_size
        c.drawString(MARGIN, y, line)
        y -= head_lead - head_size
    y -= GAP_SUB

    c.setFillColor(ORANGE)
    c.rect(MARGIN, y, 120, RULE_H, stroke=0, fill=1)
    y -= GAP_SUB

    c.setFont("Lato-Bold", 54)
    c.setFillColor(ORANGE)
    y -= 54
    c.drawString(MARGIN, y, url)
    if sub_lines:
        y -= GAP_SUB
        c.setFont("Lato", SUB_SIZE)
        c.setFillColor(MIDBLUE)
        for line in sub_lines:
            y -= SUB_SIZE
            c.drawString(MARGIN, y, line)
            y -= SUB_LEAD - SUB_SIZE


def mythfact(c, kicker, myth, fact, tag=None):
    """Signature debunk card for the myths pillar: a struck-through MYTH panel
    over an orange FACT panel. `myth` should be short (fits 1-2 lines struck).
    Legal/principle posts only; no statistic on the card.
    """
    label_size, myth_size, fact_size = 34, 62, 62
    myth_lead, fact_lead = myth_size * 1.16, fact_size * 1.16
    myth_lines = wrap(c, myth, "Lato-Black", myth_size, COL)
    fact_lines = wrap(c, fact, "Lato-Black", fact_size, COL)

    gap_panel = 90
    block = (KICKER_SIZE + GAP_KICKER
             + label_size + 24 + len(myth_lines) * myth_lead + gap_panel
             + label_size + 24 + len(fact_lines) * fact_lead)
    y = centre_start(block)

    if kicker:
        c.setFont("Lato-Bold", KICKER_SIZE)
        c.setFillColor(MIDBLUE)
        c.drawString(MARGIN, y - KICKER_SIZE, kicker.upper())
        y -= KICKER_SIZE + GAP_KICKER

    # MYTH panel: muted, struck through
    c.setFont("Lato-Black", label_size)
    c.setFillColor(MIDBLUE)
    c.drawString(MARGIN, y - label_size, "MYTH")
    y -= label_size + 24
    c.setFont("Lato-Black", myth_size)
    c.setFillColor(MIDBLUE)
    for line in myth_lines:
        y -= myth_size
        c.drawString(MARGIN, y, line)
        lw = pdfmetrics.stringWidth(line, "Lato-Black", myth_size)
        c.setLineWidth(5)
        c.setStrokeColor(ORANGE)
        c.line(MARGIN, y + myth_size * 0.32, MARGIN + lw, y + myth_size * 0.32)
        y -= myth_lead - myth_size
    y -= gap_panel

    # FACT panel: full white with an orange label
    c.setFont("Lato-Black", label_size)
    c.setFillColor(ORANGE)
    c.drawString(MARGIN, y - label_size, "FACT")
    y -= label_size + 24
    c.setFont("Lato-Black", fact_size)
    c.setFillColor(WHITE)
    for line in fact_lines:
        y -= fact_size
        c.drawString(MARGIN, y, line)
        y -= fact_lead - fact_size


def distribution(c, kicker, hero, hero_sub, segments, note=None):
    """Single-image: one hero number over a horizontal stacked distribution bar.

    segments = [(label, pct, colour_key), ...] summing to ~100. colour_key in
    {'mid','panel','orange'}. Every number here must be verified from source.
    """
    palette = {"mid": MIDBLUE, "panel": PANEL, "orange": ORANGE}
    hero_size = fit_size(hero, "Lato-Black", COL, NUM_SIZE)
    hero_cap = hero_size * 0.72
    sub_lines = wrap(c, hero_sub, "Lato", SUB_SIZE, COL)
    bar_h, seg_gap = 130, 200
    note_lines = wrap(c, note, "Lato", 30, COL) if note else []

    block = (KICKER_SIZE + GAP_KICKER + hero_cap + GAP_SUB + len(sub_lines) * SUB_LEAD
             + seg_gap + bar_h + 70 + (GAP_SUB + len(note_lines) * 42 if note_lines else 0))
    y = centre_start(block)

    c.setFont("Lato-Bold", KICKER_SIZE)
    c.setFillColor(MIDBLUE)
    c.drawString(MARGIN, y - KICKER_SIZE, kicker.upper())
    y -= KICKER_SIZE + GAP_KICKER

    c.setFont("Lato-Black", hero_size)
    c.setFillColor(ORANGE)
    c.drawString(MARGIN, y - hero_cap, hero)
    y -= hero_cap + GAP_SUB

    c.setFont("Lato", SUB_SIZE)
    c.setFillColor(WHITE)
    for line in sub_lines:
        y -= SUB_SIZE
        c.drawString(MARGIN, y, line)
        y -= SUB_LEAD - SUB_SIZE
    y -= seg_gap - (SUB_LEAD - SUB_SIZE)

    # stacked bar
    x = MARGIN
    for label, pct, ck in segments:
        seg = COL * pct / 100.0
        c.setFillColor(palette[ck])
        c.rect(x, y - bar_h, seg, bar_h, stroke=0, fill=1)
        c.setFillColor(NAVY if ck in ("panel", "orange") else WHITE)
        c.setFont("Lato-Black", 40)
        c.drawString(x + 16, y - bar_h + 46, f"{pct:.0f}%")
        x += seg
    # labels under the bar
    x = MARGIN
    c.setFont("Lato", 26)
    for label, pct, ck in segments:
        seg = COL * pct / 100.0
        c.setFillColor(ORANGE if ck == "orange" else MIDBLUE)
        c.drawString(x, y - bar_h - 40, label)
        x += seg
    y -= bar_h + 70

    if note_lines:
        y -= GAP_SUB
        c.setFont("Lato", 30)
        c.setFillColor(MIDBLUE)
        for line in note_lines:
            y -= 30
            c.drawString(MARGIN, y, line)
            y -= 12


def hbar(c, title, rows, unit, highlight, note=None):
    """Single-image horizontal bar chart. rows = [(label, value), ...].

    One series highlighted in orange, the rest mid-blue. Values printed at the
    end of each bar. Sits in the full content band with a title above.
    """
    title_size, row_h, gap = 46, 88, 20
    title_lines = wrap(c, title, "Lato-Black", title_size, COL)
    note_size = 30
    note_lines = wrap(c, note, "Lato", note_size, COL) if note else []

    chart_h = len(rows) * row_h
    block = (len(title_lines) * title_size * 1.2 + GAP_KICKER + chart_h
             + (GAP_SUB + len(note_lines) * note_size * 1.35 if note_lines else 0))
    y = centre_start(block)

    c.setFillColor(WHITE)
    c.setFont("Lato-Black", title_size)
    for line in title_lines:
        y -= title_size
        c.drawString(MARGIN, y, line)
        y -= title_size * 0.2
    y -= GAP_KICKER

    label_w, label_size = 440, 31
    bar_max = COL - label_w - 96
    vmax = max(v for _, v in rows)
    for label, value in rows:
        y -= row_h
        colour = ORANGE if label == highlight else MIDBLUE
        bar_w = bar_max * value / vmax
        c.setFillColor(colour)
        c.rect(MARGIN + label_w, y + 12, bar_w, row_h - gap, stroke=0, fill=1)
        c.setFillColor(WHITE if label == highlight else MIDBLUE)
        c.setFont("Lato-Bold" if label == highlight else "Lato", label_size)
        c.drawString(MARGIN, y + 26, label)
        c.setFont("Lato-Black", 36)
        c.setFillColor(ORANGE if label == highlight else WHITE)
        c.drawString(MARGIN + label_w + bar_w + 20, y + 22, unit.format(value))

    if note_lines:
        y -= GAP_SUB
        c.setFont("Lato", note_size)
        c.setFillColor(MIDBLUE)
        for line in note_lines:
            y -= note_size
            c.drawString(MARGIN, y, line)
            y -= note_size * 0.35


# --- slide specs ------------------------------------------------------------
SLIDES = {
    1: [
        ("cover", {}),
        ("number", dict(value="1,845", sub="Total company insolvencies. Flat on May. Down 10% on the year.",
                        kicker="June 2026, England and Wales")),
        ("stack", {}),
        ("number", dict(value="191", sub="Administrations. Up 45% on May.", kicker="The number everyone quoted")),
        ("number", dict(value="~60", sub="Connected real estate companies inside that figure.",
                        kicker="What was in it")),
        ("number", dict(value="~130", sub="Administrations without them. Level with May.",
                        kicker="Take them out")),
        ("panel", dict(heading="Plain English",
                       body="Administration hands control to an administrator. The business may be sold. "
                            "The company and the director's position usually are not.")),
        ("number", dict(value="14", sub="Company voluntary arrangements. Down 44% in a month.",
                        kicker="The line worth watching")),
        ("statement", dict(text="The rise is real.\nIt is a quarter,\nnot 80%.")),
        ("outro", {}),
    ],
    5: [
        ("hbar", dict(
            title="How long large UK firms take to pay a supplier",
            unit="{:.1f}",
            highlight="Manufacturing",
            rows=[
                ("Manufacturing", 47.4),
                ("Wholesale and retail", 38.5),
                ("Construction", 34.7),
                ("Professional services", 34.5),
                ("Transport and storage", 34.4),
                ("Accommodation and food", 33.7),
                ("Information and comms", 33.6),
                ("Admin and support", 29.9),
                ("Education", 24.8),
                ("Finance and insurance", 24.3),
            ],
            note="Average days to pay an invoice, by sector. 6,882 companies, Dec 2024 to May 2026.")),
    ],
    # Post PG: legal-principle myth post, no statistic. Grounded in
    # drafts/22785 (reviewed by licensed IPs). No number to verify.
    20: [
        ("mythcard", dict(
            kicker="What the bank did not spell out",
            lines=[("Limited liability", "white"),
                   ("has a hole in it.", "orange")],
            sub="It is called a personal guarantee. If your company has a loan, lease or "
                "overdraft, you have very likely signed one.",
            cta="What it commits you to, before you sign the next one. Confidential.")),
    ],
    # Post 21: Myth/Fact variant of the personal-guarantee post. Pillar template.
    21: [
        ("mythfact", dict(
            kicker="Personal guarantees",
            myth="Limited liability protects everything I own.",
            fact="Not a penny of it, on any debt you have personally guaranteed.")),
    ],
    # Post 25: warning-signs self-check carousel. Signs grounded in drafts/68123
    # (IP-reviewed). No statutory figure; CTA to the diagnostic calculator.
    25: [
        ("title", dict(kicker="A two-minute director's check",
                       head="7 signs your business is under more strain than the numbers show.")),
        ("sign", dict(n=1, of=7, text="Money out has beaten money in for months, not weeks.")),
        ("sign", dict(n=2, of=7, text="You have started dipping into the VAT or PAYE money to get through the month.")),
        ("sign", dict(n=3, of=7, text="Creditor letters stop saying reminder and start setting deadlines.")),
        ("sign", dict(n=4, of=7, text="The management accounts arrive late, because you would rather not look.")),
        ("sign", dict(n=5, of=7, text="Your invoice finance advance is quietly cut. A supplier moves you to pro-forma.")),
        ("sign", dict(n=6, of=7, text="A CCJ lands, and it is on the public record within days.")),
        ("sign", dict(n=7, of=7, text="Past a certain point, the law expects you to put creditors first.")),
        ("statement", dict(text="One of these is a wobble.\nThree is a pattern.\nThe pattern is easier\nto fix early.")),
        ("cta", dict(head="A two-minute check. No accounts needed. See where you stand.",
                     url="companydebt.com/insolvency-calculator",
                     sub="A screening tool from licensed insolvency practitioners. Not a formal opinion.")),
    ],
    # Post 26: "mistakes" companion to post 25. Each grounded: wrongful trading
    # (s.214), preferences (s.239), undervalue (s.238) all confirmed in corpus.
    # No number on slides; CTA to the personal-liability page.
    26: [
        ("title", dict(kicker="When a company can't pay",
                       head="7 moves that turn the company's debt into your debt.")),
        ("sign", dict(n=1, of=7, label="MISTAKE", text="Keep trading and running up new debts after you know it can't recover.")),
        ("sign", dict(n=2, of=7, label="MISTAKE", text="Repay your own director's loan before the other creditors.")),
        ("sign", dict(n=3, of=7, label="MISTAKE", text="Clear one creditor you care about, or a family member, ahead of the rest.")),
        ("sign", dict(n=4, of=7, label="MISTAKE", text="Sell the assets or the client book cheaply to a company you also own.")),
        ("sign", dict(n=5, of=7, label="MISTAKE", text="Spend the VAT and PAYE money to keep trading.")),
        ("sign", dict(n=6, of=7, label="MISTAKE", text="Stop opening the HMRC post and hope it goes quiet.")),
        ("sign", dict(n=7, of=7, label="MISTAKE", text="Strike the company off to make the debt disappear.")),
        ("statement", dict(text="None of these starts\nas a plan.\nEach is where panic leads.\nAdvice early avoids all seven.")),
        ("cta", dict(head="If the company can't pay, get the options before you act.",
                     url="companydebt.com/advice",
                     sub="When a director becomes personally liable. Free initial call, confidential.")),
    ],
    # Post 27: single impactful stat. CVLs = 1,364 of 1,845 = 74% (gov.uk June
    # 2026 commentary: "CVLs comprised 74% of the total"). Verified this session.
    27: [
        ("number", dict(value="74%",
                        sub="of company insolvencies were creditors' voluntary liquidations: the route a company starts itself, not one the court forces.",
                        kicker="UK company insolvencies, June 2026")),
    ],
    # Post 28: topical BBL guarantee. gov.uk COVID loan repayment data, March
    # 2026: £11.82bn guarantee settled, £1.58bn against suspected fraud. All
    # figures primary-source verified this session.
    28: [
        ("number", dict(value="£11.82bn",
                        sub="has been paid out on the government's Bounce Back Loan guarantee for loans that were not repaid. £1.58bn of it on suspected fraud.",
                        kicker="Bounce Back Loans, as at March 2026")),
    ],
    # Post 12: simple stats-hub promo. 1 in 198 = 10,000 / 50.5 rate, verified
    # from gov.uk June 2026 commentary (rate 50.5 per 10k, prior year 52.4).
    12: [
        ("number", dict(value="1 in 198",
                        sub="UK companies entered insolvency in the year to June 2026.",
                        kicker="How common is it, really?")),
    ],
    # Post 22: Myth/Fact, overdrawn director's loan. Grounded in drafts/75111
    # (Chris Andersen byline). s.455 33.75% verified on gov.uk 2026-07-22.
    22: [
        ("mythfact", dict(
            kicker="Director's loan accounts",
            myth="It's my company, so it's my money.",
            fact="An overdrawn loan account is a debt the liquidator will reclaim from you.")),
    ],
    # Post 23: Myth/Fact, strike-off/dissolution. Grounded in the live page
    # (creditors restore within 6yr, HMRC 20yr; DS01 £13). No number on card.
    23: [
        ("mythfact", dict(
            kicker="Striking off a company",
            myth="Dissolve the company and the debts die with it.",
            fact="Creditors can block it, restore the company, and pursue you.")),
    ],
    # Post 24: Myth/Fact, Bounce Back Loan. Grounded in the live page + draft
    # 43745. NB no personal guarantee on BBLs; risk is company debt + evasion,
    # not a called PG. No number on card.
    24: [
        ("mythfact", dict(
            kicker="Bounce Back Loans",
            myth="Dissolve the company and the Bounce Back Loan disappears.",
            fact="It doesn't. The lender blocks the strike-off, and the attempt looks like evasion.")),
    ],
    # Post 11: verified 2026-07-22 by recomputing from the gov.uk bulk export.
    # Window 2025-01-11 to 2026-07-05, ~6,600 companies, latest report each.
    11: [
        ("distribution", dict(
            kicker="How large UK firms pay, 18 months to July 2026",
            hero="12%",
            hero_sub="of invoices from large UK companies are paid more than 60 days after they are issued.",
            segments=[
                ("Within 30 days", 59.7, "mid"),
                ("31 to 60 days", 28.3, "panel"),
                ("Later than 60", 12.0, "orange"),
            ],
            note="Self-reported, unaudited, large companies only. ~6,600 companies, latest report each.")),
    ],
}

# Footer source line per post (defaults to the insolvency release).
# Empty string = no source line (legal/principle posts carry no dataset).
SOURCES = {
    5: "Source: UK payment practices reporting, 6,882 companies",
    11: "Source: gov.uk payment practices export, recomputed 22 Jul 2026",
    28: "Source: gov.uk COVID loan guarantee schemes data, March 2026",
    20: "",
    21: "",
    22: "",
    23: "",
    24: "",
    25: "",
    26: "",
}

# Footer URL per post (defaults to the data hub).
URLS = {
    20: "companydebt.com/advice",
    21: "companydebt.com/advice",
    22: "companydebt.com/advice",
    23: "companydebt.com/liquidation",
    24: "companydebt.com/bounce-back-loan-support-hub",
    25: "companydebt.com/insolvency-calculator",
    26: "companydebt.com/advice",
    28: "companydebt.com/bounce-back-loan-support-hub",
}


def render(c, kind, spec, slide_no, total, source=FOOTER_SOURCE, url=FOOTER_URL):
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, stroke=0, fill=1)

    if kind == "hbar":
        hbar(c, **spec)
    elif kind == "title":
        title(c, **spec)
    elif kind == "sign":
        sign(c, **spec)
    elif kind == "cta":
        cta(c, **spec)
    elif kind == "mythcard":
        mythcard(c, **spec)
    elif kind == "mythfact":
        mythfact(c, **spec)
    elif kind == "distribution":
        distribution(c, **spec)
    elif kind == "cover":
        big_number(c, "80%", "Administrations, year to June 2026. Mostly one group.",
                   kicker="Company insolvency statistics")
    elif kind == "number":
        big_number(c, **spec)
    elif kind == "stack":
        stacked_bar(c)
    elif kind == "panel":
        panel_note(c, **spec)
    elif kind == "statement":
        statement(c, spec["text"])
    elif kind == "outro":
        head, url_size, src_size = 68, 54, 32
        head_lines = wrap(c, "Full figures by procedure, by sector, back to 2000.",
                          "Lato-Black", head, COL)
        src = ("Insolvency Service, Company Insolvency Statistics June 2026. "
               "Accredited official statistics.")
        src_lines = wrap(c, src, "Lato", src_size, COL)
        block = (len(head_lines) * head * 1.22 + GAP_SUB + url_size + GAP_SUB
                 + len(src_lines) * src_size * 1.35)
        y = centre_start(block)

        c.setFillColor(WHITE)
        c.setFont("Lato-Black", head)
        for line in head_lines:
            y -= head
            c.drawString(MARGIN, y, line)
            y -= head * 0.22
        y -= GAP_SUB

        c.setFont("Lato-Bold", url_size)
        c.setFillColor(ORANGE)
        y -= url_size
        c.drawString(MARGIN, y, "companydebt.com/data")
        y -= GAP_SUB

        c.setFont("Lato", src_size)
        c.setFillColor(MIDBLUE)
        for line in src_lines:
            y -= src_size
            c.drawString(MARGIN, y, line)
            y -= src_size * 0.35

    draw_chrome(c, slide_no, total, source, url)
    c.showPage()


def to_png(pdf_path, png_path):
    """Rasterise a single-page PDF to a 1080x1350 PNG (scale 1 = 72dpi = 1080px)."""
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(pdf_path)
    doc[0].render(scale=1).to_pil().save(png_path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--post", type=int, required=True)
    ap.add_argument("--out", default=os.path.join("social", "assets"))
    ap.add_argument("--root", default=".")
    args = ap.parse_args()

    if args.post not in SLIDES:
        sys.exit(f"No slide spec for post {args.post}. Add one to SLIDES.")

    register_fonts(args.root)
    out_dir = os.path.join(args.root, args.out)
    os.makedirs(out_dir, exist_ok=True)

    slides = SLIDES[args.post]
    source = SOURCES.get(args.post, FOOTER_SOURCE)
    url = URLS.get(args.post, FOOTER_URL)
    single = len(slides) == 1
    kind = "image" if single else "carousel"
    pdf_path = os.path.join(out_dir, f"post-{args.post:02d}-{kind}.pdf")

    c = canvas.Canvas(pdf_path, pagesize=(W, H))
    c.setTitle(f"Company Debt: LinkedIn post {args.post}")
    for i, (slide_kind, spec) in enumerate(slides, 1):
        render(c, slide_kind, spec, i, len(slides), source, url)
    c.save()

    print(f"Wrote {pdf_path}")
    if single:
        png_path = os.path.join(out_dir, f"post-{args.post:02d}-image.png")
        to_png(pdf_path, png_path)
        size_kb = os.path.getsize(png_path) / 1024
        print(f"Wrote {png_path}")
        print(f"Single image, {W}x{H} (4:5), {size_kb:.0f} KB")
    else:
        size_kb = os.path.getsize(pdf_path) / 1024
        print(f"{len(slides)} slides, {W}x{H} (4:5), {size_kb:.0f} KB")


if __name__ == "__main__":
    main()
