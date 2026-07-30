#!/usr/bin/env python3
"""Corpus-wide statutory citation accuracy audit.

Crawlers only catch citations whose LINK 404s. That misses the failure mode
that actually bit us: a citation whose link resolves fine while the text names
a section or schedule that does not exist. The Finance Act 2020 "Schedule 28"
and "Schedule 26" fabrications both survived because /ukpga/2020/14/contents
is a perfectly valid URL.

So this runs two independent layers:

  Layer 1 (--urls)  every legislation.gov.uk link in drafts/ is fetched; any
                    non-200 is a citation pointing at something that does not
                    exist. Also flags anchor text that contradicts its own URL
                    (text says "section 98", URL says /schedule/28).

  Layer 2 (--prose) learns Act-name -> legislation.gov.uk base URL from the
                    links already in the corpus, then takes every
                    "<Act> ... section/Schedule N" claim in the prose and
                    checks that unit actually exists under that Act.

Layer 2 is deliberately noisy: it attributes a unit to the nearest preceding
Act name, so a sentence like "the Finance Act 2020 ... and the Insolvency Act
1986 (sections 124 and 214)" misattributes s.124 to FA2020. Treat its output
as a triage list to read by hand, not a defect list. Layer 1 is precise.

Usage:
    python scripts/audit_citations.py                     # both layers
    python scripts/audit_citations.py --urls              # layer 1 only
    python scripts/audit_citations.py --prose             # layer 2 only
    python scripts/audit_citations.py --out report.md

Read-only: it never edits drafts.
"""

from __future__ import annotations

import argparse
import re
import time
import urllib.error
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRAFTS = ROOT / "drafts"
UA = {"User-Agent": "CompanyDebt-citation-audit/1.0"}

TAG_RE = re.compile(r"<[^>]+>")
LINK_RE = re.compile(
    r'<a\s+[^>]*href="(https://www\.legislation\.gov\.uk[^"]*)"[^>]*>(.*?)</a>',
    re.I | re.S,
)
BASE_RE = re.compile(
    r'href="https://www\.legislation\.gov\.uk/([a-z]+/[^/"]+/[^/"]+)[^"]*"[^>]*>(.*?)</a>',
    re.I | re.S,
)
ACT_RE = re.compile(r"\b((?:[A-Z][A-Za-z'()]*\s+){1,7}Act\s+((?:19|20)\d{2}))", re.U)
UNIT_IN_TEXT_RE = re.compile(
    r"\b(section|schedule|part|rule|regulation|article)s?\s+([0-9A-Za-z.]+)", re.I
)
UNIT_IN_URL_RE = re.compile(
    r"/(section|schedule|part|rule|regulation|article)/([^/?#]+)", re.I
)
PROSE_UNIT_RE = re.compile(
    r"\b(?:(section|sections|s\.|ss\.)\s*([0-9]+[A-Za-z]*)"
    r"|(Schedule|Sched\.|Sch\.|Sch)\s*([0-9]+[A-Za-z]*|[A-Z]\d+))",
    re.I,
)


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def fetch_status(url: str):
    req = urllib.request.Request(url, headers=UA)
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                return r.status
        except urllib.error.HTTPError as e:
            return e.code
        except Exception:
            if attempt:
                return "ERR"
            time.sleep(1.5)
    return "ERR"


def check_statuses(urls: list[str]) -> dict:
    with ThreadPoolExecutor(max_workers=6) as ex:
        return dict(zip(urls, ex.map(fetch_status, urls)))


# ---------------------------------------------------------------------------
# Layer 1: link resolution + anchor-text/URL agreement.
# ---------------------------------------------------------------------------


def collect_links() -> list[tuple[str, str, str]]:
    out = []
    for f in sorted(DRAFTS.glob("*.html")):
        html = f.read_text(encoding="utf-8", errors="replace")
        for url, inner in LINK_RE.findall(html):
            out.append((f.name, url.replace("&amp;", "&"), norm(TAG_RE.sub("", inner))))
    return out


def anchor_url_conflict(url: str, text: str) -> str | None:
    """Anchor text names a unit the URL contradicts, or None."""
    tm = UNIT_IN_TEXT_RE.search(text)
    um = UNIT_IN_URL_RE.search(url)
    if not tm or not um:
        return None
    t_unit, t_num = tm.group(1).lower(), tm.group(2)
    u_unit, u_num = um.group(1).lower(), um.group(2)
    if t_unit != u_unit or t_num.lower() != u_num.lower():
        return f"text says {t_unit} {t_num}, URL says {u_unit} {u_num}"
    return None


def run_urls() -> list[str]:
    links = collect_links()
    urls = sorted({u for _, u, _ in links})
    status = check_statuses(urls)
    bad = {u: s for u, s in status.items() if s != 200}
    conflicts = [
        (f, u, t, d)
        for f, u, t in links
        if (d := anchor_url_conflict(u, t))
    ]

    lines = [
        "## Layer 1: link resolution and anchor/URL agreement",
        "",
        f"- Links checked: {len(links)} ({len(urls)} unique URLs)",
        f"- Non-200 URLs: {len(bad)}",
        f"- Anchor text contradicting its own URL: {len(conflicts)}",
        "",
        "### Dead citations (non-200)",
    ]
    if bad:
        for u, s in sorted(bad.items()):
            lines.append(f"- `{s}` {u}")
            for w in sorted({f for f, uu, _ in links if uu == u}):
                lines.append(f"    - drafts/{w}")
    else:
        lines.append("- none")
    lines += ["", "### Anchor text contradicts its own URL",
              "",
              "Many of these are benign: a range like \"sections 170 to 177\"",
              "legitimately links to the Part landing page. Read before acting.",
              ""]
    if conflicts:
        for f, u, t, d in conflicts:
            lines.append(f"- drafts/{f}: {d}")
            lines.append(f"    - text: {t[:160]}")
            lines.append(f"    - url:  {u}")
    else:
        lines.append("- none")
    return lines + [""]


# ---------------------------------------------------------------------------
# Layer 2: prose claims about sections/schedules that may not exist.
# ---------------------------------------------------------------------------


def learn_act_bases() -> dict[str, str]:
    """Map Act name -> legislation.gov.uk base path, by majority vote over links."""
    votes: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for f in DRAFTS.glob("*.html"):
        html = f.read_text(encoding="utf-8", errors="replace")
        for base, inner in BASE_RE.findall(html):
            m = ACT_RE.search(norm(TAG_RE.sub("", inner)))
            if m:
                votes[norm(m.group(1))][base] += 1
    return {a: max(b.items(), key=lambda kv: kv[1])[0] for a, b in votes.items()}


def run_prose() -> list[str]:
    bases = learn_act_bases()
    claims = []
    for f in sorted(DRAFTS.glob("*.html")):
        text = norm(TAG_RE.sub(" ", f.read_text(encoding="utf-8", errors="replace")))
        for am in ACT_RE.finditer(text):
            act = norm(am.group(1))
            base = bases.get(act)
            if not base:
                continue
            um = PROSE_UNIT_RE.search(text[am.end():am.end() + 120])
            if not um:
                continue
            unit, num = ("section", um.group(2)) if um.group(1) else ("schedule", um.group(4))
            claims.append((
                f.name, act, unit, num,
                f"https://www.legislation.gov.uk/{base}/{unit}/{num}",
                norm(text[max(0, am.start() - 60):am.end() + 120]),
            ))

    status = check_statuses(sorted({c[4] for c in claims}))
    bad = [c for c in claims if status.get(c[4]) != 200]

    lines = [
        "## Layer 2: prose citation claims (TRIAGE LIST, high false-positive rate)",
        "",
        f"- Act -> URL mappings learned from corpus links: {len(bases)}",
        f"- Prose citation claims checked: {len(claims)}",
        f"- Claims naming a unit that does not resolve: {len(bad)}",
        "",
        "A flag here usually means the unit belongs to a DIFFERENT Act named",
        "later in the same sentence, which this heuristic cannot see. Read the",
        "context line before changing anything.",
        "",
    ]
    seen = set()
    for fname, act, unit, num, url, sent in bad:
        key = (fname, act, unit, num)
        if key in seen:
            continue
        seen.add(key)
        lines.append(f"- drafts/{fname}: **{act}, {unit} {num}** -> `{status.get(url)}`")
        lines.append(f"    - context: {sent[:220]}")
    if not bad:
        lines.append("- none")
    return lines + [""]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--urls", action="store_true", help="run layer 1 only")
    ap.add_argument("--prose", action="store_true", help="run layer 2 only")
    ap.add_argument("--out", type=Path, help="write the report to a file as well")
    args = ap.parse_args()

    both = not (args.urls or args.prose)
    lines = ["# Statutory citation accuracy audit (drafts/)", ""]
    if both or args.urls:
        lines += run_urls()
    if both or args.prose:
        lines += run_prose()

    report = "\n".join(lines)
    print(report)
    if args.out:
        args.out.write_text(report, encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
