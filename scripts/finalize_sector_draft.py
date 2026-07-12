"""Finalize a sector-page draft for the gate.

Two mechanical steps the humanise/draft packs call for (see
runtime-packs/stages/humanise.md): escape FAQ accordion panelTitle HTML so it
does not render as literal junk, then split any paragraph over ~400 chars at a
sentence boundary so the readability gate passes. Voice/content is untouched.

    python scripts/finalize_sector_draft.py --file drafts/52222_garden-centres.html
"""
from __future__ import annotations

import argparse
import re


def escape_panel_titles(t: str) -> tuple[str, int]:
    bs = chr(92)
    lt, gt = bs + "u003c", bs + "u003e"
    n = t.count('"panelTitle":"<strong>')
    t = t.replace('"panelTitle":"<strong>', '"panelTitle":"' + lt + "strong" + gt)
    t = t.replace('</strong>"} -->', lt + "/strong" + gt + '"} -->')
    return t, n


def _sentences(inner: str) -> list[str]:
    out, depth, start = [], 0, 0
    for i, ch in enumerate(inner):
        if ch == "<":
            depth += 1
        elif ch == ">":
            depth -= 1
        elif ch == "." and depth == 0 and i + 1 < len(inner) and inner[i + 1] == " ":
            out.append(inner[start:i + 1].strip())
            start = i + 2
    tail = inner[start:].strip()
    if tail:
        out.append(tail)
    return out


def _plain(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s)


def split_long_paragraphs(t: str, limit: int = 400, target: int = 380) -> tuple[str, int]:
    counter = {"n": 0}

    def repl(m: re.Match) -> str:
        inner = m.group(1).strip()
        if len(_plain(inner)) <= limit:
            return m.group(0)
        sents = _sentences(inner)
        if len(sents) < 2:
            return m.group(0)
        groups, cur = [], ""
        for s in sents:
            cand = (cur + " " + s).strip() if cur else s
            if cur and len(_plain(cand)) > target:
                groups.append(cur)
                cur = s
            else:
                cur = cand
        if cur:
            groups.append(cur)
        counter["n"] += 1
        return "\n".join(f"<p>{g}</p>" for g in groups)

    t = re.sub(r"<p>(.*?)</p>", repl, t, flags=re.S)
    return t, counter["n"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    a = ap.parse_args()
    t = open(a.file, encoding="utf-8").read()
    t, esc = escape_panel_titles(t)
    t, split = split_long_paragraphs(t)
    open(a.file, "w", encoding="utf-8").write(t)
    over = sum(1 for p in re.findall(r"<p>(.*?)</p>", t, re.S) if len(_plain(p)) > 400)
    print(f"panelTitles escaped: {esc} | paragraphs split: {split} | over-400 remaining: {over}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
