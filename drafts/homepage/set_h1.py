# -*- coding: utf-8 -*-
"""Set the homepage H1 (page 55052) without touching anything else."""

import pathlib
import re
import sys

NEW_H1 = "Help with Limited Company Debt"

src = pathlib.Path("tmp/homepage-55052-verify-corrected.html")  # byte-identical to live
out = pathlib.Path("tmp/homepage-55052-h1.html")

c = src.read_text(encoding="utf-8")

pat = re.compile(r'("block_hero_blue_title":")(.*?)(",")')
m = pat.search(c)
if not m:
    sys.exit("ERROR: could not locate block_hero_blue_title")

old_val = m.group(2)
print(f"old H1: {old_val!r}")

# Preserve whatever trailing escape sequence the field carries.
trailing = ""
mt = re.search(r'((?:\\r|\\n)+)$', old_val)
if mt:
    trailing = mt.group(1)

new_val = NEW_H1 + trailing
c2 = c[:m.start(2)] + new_val + c[m.end(2):]
print(f"new H1: {new_val!r}")

# Guards: nothing else may move.
for phrase, n in [
    ("Trusted by Thousands of UK Directors", 1),
    ("What We Can Help You With", 1),
    ("Expert Advice. Affordable Help.", 1),
    ("General Debt Pressure", 2),
]:
    if c2.count(phrase) != n:
        sys.exit(f"ERROR: '{phrase}' count {c2.count(phrase)}, expected {n}")

if len(c2) - len(c) != len(new_val) - len(old_val):
    sys.exit("ERROR: unexpected length delta")

out.write_text(c2, encoding="utf-8")
print("guards ok")
print(f"written: {out}  ({len(c2)} chars, was {len(c)})")
