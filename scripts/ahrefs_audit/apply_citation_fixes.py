"""Apply the citation corrections in citation_fixes.py to drafts + staging.

Dry run by default. Pass --apply to write.

Order of operations per page:
  1. swap the href           (staging_edit.py swap-link)
  2. swap the anchor label   (staging_edit.py replace-text)
  3. mirror both into the local draft, so draft and staging do not drift

Draft and staging are BOTH updated deliberately: a staging-only edit gets
silently reverted the next time the page is rebuilt from its draft, which is
one of the ways the previous remediation pass failed to stick.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from citation_fixes import LINK_FIXES, LINK_REMOVALS

ROOT = Path(__file__).resolve().parents[2]
DRAFTS = ROOT / "drafts"
EDITOR = ROOT / "scripts" / "staging_edit.py"


def drafts_containing(needle: str) -> list[Path]:
    hits = []
    for p in sorted(DRAFTS.glob("*.html")):
        try:
            if needle in p.read_text(encoding="utf-8", errors="ignore"):
                hits.append(p)
        except OSError:
            pass
    return hits


def slug_of(draft: Path) -> str:
    """'9443_cant-pay-vat.html' -> 'cant-pay-vat'"""
    return draft.stem.split("_", 1)[1]


def run_editor(args: list[str], apply: bool) -> str:
    cmd = [sys.executable, str(EDITOR)] + args + (["--apply"] if apply else [])
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=180)
    return (r.stdout + r.stderr).strip()


def staging_url(slug: str) -> str:
    # staging_edit.py resolves by slug alone, so the path prefix is irrelevant.
    return f"https://www.companydebt.com/{slug}/"


def fix_draft(draft: Path, old: str, new: str, text_fixes, apply: bool) -> int:
    txt = draft.read_text(encoding="utf-8")
    before = txt
    txt = txt.replace(old, new)
    for o, n in text_fixes:
        txt = txt.replace(o, n)
    if txt == before:
        return 0
    n_changed = before.count(old) + sum(before.count(o) for o, _ in text_fixes)
    if apply:
        draft.write_text(txt, encoding="utf-8")
    return n_changed


def remove_li_from_draft(draft: Path, href: str, apply: bool) -> str | None:
    txt = draft.read_text(encoding="utf-8")
    pat = re.compile(r"[ \t]*<li>(?:(?!</li>).)*?" + re.escape(href) + r".*?</li>\n?", re.DOTALL)
    m = pat.search(txt)
    if not m:
        return None
    if apply:
        draft.write_text(pat.sub("", txt, count=1), encoding="utf-8")
    return m.group(0).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only", help="run a single fix id")
    ap.add_argument("--skip-staging", action="store_true")
    a = ap.parse_args()

    mode = "APPLY" if a.apply else "DRY RUN"
    print(f"=== Citation fixes [{mode}] ===\n")

    for fx in LINK_FIXES:
        if a.only and fx["id"] != a.only:
            continue
        hits = drafts_containing(fx["old"])
        print(f"\n{'-' * 74}\n[{fx['id']}]  {len(hits)} draft(s)")
        print(f"  old: {fx['old']}")
        print(f"  new: {fx['new']}")
        print(f"  why: {fx['why'][:150]}")
        for d in hits:
            slug = slug_of(d)
            n = fix_draft(d, fx["old"], fx["new"], fx["text_fixes"], a.apply)
            print(f"   draft  {d.name:<62} {n} change(s)")
            if not a.skip_staging:
                out = run_editor(["swap-link", "--url", staging_url(slug),
                                  "--old", fx["old"], "--new", fx["new"]], a.apply)
                print(f"   staging{'':<1} {out.splitlines()[0] if out else '(no output)'}")
                for o, nw in fx["text_fixes"]:
                    out2 = run_editor(["replace-text", "--url", staging_url(slug),
                                       "--old", o, "--new", nw], a.apply)
                    if out2:
                        print(f"   staging  {out2.splitlines()[0]}")

    for rm in LINK_REMOVALS:
        hits = drafts_containing(rm["old"])
        print(f"\n{'-' * 74}\n[{rm['id']}] REMOVE  {len(hits)} draft(s)")
        print(f"  why: {rm['why'][:150]}")
        for d in hits:
            li = remove_li_from_draft(d, rm["old"], a.apply)
            print(f"   draft  {d.name}")
            print(f"     removing: {(li or '(no <li> matched)')[:150]}")
            if not a.skip_staging and li:
                out = run_editor(["replace-text", "--url", staging_url(slug_of(d)),
                                  "--old", li, "--new", ""], a.apply)
                print(f"   staging  {out.splitlines()[0] if out else '(no output)'}")

    if not a.apply:
        print("\n\nDry run only. Re-run with --apply to write.")


if __name__ == "__main__":
    main()
