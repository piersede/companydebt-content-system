# -*- coding: utf-8 -*-
"""Restore the original hero body copy beneath the new H1 (page 55052).

Pulls the prose byte-for-byte out of the pre-change dump rather than retyping
it, so the mixed straight/curly apostrophes and \\r\\n spacing are exact.
Keeps the current H1 ("Help with Limited Company Debt") and the strapline.
"""

import pathlib
import sys

CUR = pathlib.Path("tmp/homepage-55052-verify-h1.html")        # byte-identical to live
ORIG = pathlib.Path("tmp/homepage-55052-original.html")        # pre-change dump
OUT = pathlib.Path("tmp/homepage-55052-heroback.html")

FIELD = '"block_hero_blue_wysiwyg_left":"'
MARK = chr(92) + 'u003cdiv class=' + chr(92) + 'u0022cd-hero-blue__cta-group'
BREAK = chr(92) + 'r' + chr(92) + 'n' + chr(92) + 'r' + chr(92) + 'n'   # \r\n\r\n

cur = CUR.read_text(encoding="utf-8")
orig = ORIG.read_text(encoding="utf-8")


def prose_span(s):
    i = s.index(FIELD) + len(FIELD)
    j = s.index(MARK, i)
    return i, j


ci, cj = prose_span(cur)
oi, oj = prose_span(orig)
cur_prose, orig_prose = cur[ci:cj], orig[oi:oj]

# Strapline is everything up to and including the first blank-line break.
if BREAK not in cur_prose:
    sys.exit("ERROR: could not isolate the strapline in current hero prose")
strapline = cur_prose.split(BREAK, 1)[0] + BREAK
if "cd-hero-strapline" not in strapline:
    sys.exit("ERROR: leading segment is not the strapline")

new_prose = strapline + orig_prose
out = cur[:ci] + new_prose + cur[cj:]

print("restored original hero copy:")
for para in orig_prose.split(BREAK):
    t = para.replace(chr(92) + 'r' + chr(92) + 'n', '').strip()
    if t:
        print("  *", t)

# Guards
CHECKS = {
    "Help with Limited Company Debt": 1,      # H1 must not change
    "cd-hero-strapline": 1,                   # strapline retained
    "Trusted by Thousands of UK Directors": 1,
    "What We Can Help You With": 1,
    "General Debt Pressure": 2,
}
for phrase, n in CHECKS.items():
    if out.count(phrase) != n:
        sys.exit(f"ERROR: '{phrase}' count {out.count(phrase)}, expected {n}")

if out.count(chr(92) + 'u003csvg') != 3:
    sys.exit("ERROR: hero tick SVGs not intact")
if "Confidential advice for directors of UK limited companies" in out:
    sys.exit("ERROR: two-sentence hero copy still present")

OUT.write_text(out, encoding="utf-8")
print("\nguards ok")
print(f"written: {OUT}  ({len(out)} chars, was {len(cur)})")
