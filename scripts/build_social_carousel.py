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
WORDMARK = "COMPANY DEBT"


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


def draw_chrome(c, slide_no, total):
    """Footer source line, url, wordmark and slide counter. Every slide."""
    c.setFont("Lato", 20)
    c.setFillColor(MIDBLUE)
    c.drawString(MARGIN, 74, FOOTER_SOURCE)
    c.setFont("Lato-Bold", 20)
    c.drawString(MARGIN, 44, FOOTER_URL)

    c.setFont("Lato-Black", 20)
    c.setFillColor(WHITE)
    c.drawRightString(W - MARGIN, 44, WORDMARK)

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
    size = 88
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
    ]
}


def render(c, kind, spec, slide_no, total):
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, stroke=0, fill=1)

    if kind == "cover":
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

    draw_chrome(c, slide_no, total)
    c.showPage()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--post", type=int, required=True)
    ap.add_argument("--out", default=os.path.join("social", "assets"))
    ap.add_argument("--root", default=".")
    args = ap.parse_args()

    if args.post not in SLIDES:
        sys.exit(f"No slide spec for post {args.post}. Add one to SLIDES.")

    register_fonts(args.root)
    os.makedirs(os.path.join(args.root, args.out), exist_ok=True)
    path = os.path.join(args.root, args.out, f"post-{args.post:02d}-carousel.pdf")

    slides = SLIDES[args.post]
    c = canvas.Canvas(path, pagesize=(W, H))
    c.setTitle(f"Company Debt: LinkedIn post {args.post}")
    for i, (kind, spec) in enumerate(slides, 1):
        render(c, kind, spec, i, len(slides))
    c.save()

    size_kb = os.path.getsize(path) / 1024
    print(f"Wrote {path}")
    print(f"{len(slides)} slides, {W}x{H} (4:5), {size_kb:.0f} KB")


if __name__ == "__main__":
    main()
