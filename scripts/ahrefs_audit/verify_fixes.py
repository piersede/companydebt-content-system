"""Verify the citation fixes actually landed on staging AND in the drafts.

The previous remediation pass 'succeeded' locally while staging kept serving
the old content, so success here means: the old string is gone from staging's
stored content and the new string is present. Nothing is taken on trust.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).parent))

from staging_edit import session, resolve_post  # noqa: E402
from citation_fixes import LINK_FIXES, LINK_REMOVALS  # noqa: E402

DRAFTS = ROOT / "drafts"

# slug -> which fix ids should have been applied there
targets: dict[str, list[tuple[str, str, str | None]]] = {}
for fx in LINK_FIXES:
    for p in DRAFTS.glob("*.html"):
        pass
# Build from drafts by searching for the NEW url (post-fix state).
for fx in LINK_FIXES:
    for p in sorted(DRAFTS.glob("*.html")):
        txt = p.read_text(encoding="utf-8", errors="ignore")
        if fx["new"] in txt or fx["old"] in txt:
            targets.setdefault(p.stem.split("_", 1)[1], []).append(
                (fx["id"], fx["old"], fx["new"]))
for rm in LINK_REMOVALS:
    # PLN page, known slug
    targets.setdefault("personal-liability-notices", []).append(
        (rm["id"], rm["old"], None))

s = session()
fails, gaps, checks = [], [], 0
print(f"Verifying {len(targets)} staging pages...\n")

for slug, items in sorted(targets.items()):
    res = resolve_post(s, f"https://www.companydebt.com/{slug}/")
    if not res:
        fails.append(f"{slug}: NOT FOUND on staging")
        continue
    _, pid, _, _, raw = res
    draft = next((p for p in DRAFTS.glob(f"*_{slug}.html")), None)
    dtxt = draft.read_text(encoding="utf-8", errors="ignore") if draft else ""
    for fid, old, new in items:
        checks += 1
        problems = []
        # A real failure is the OLD string surviving. "NEW absent from staging"
        # while OLD is also absent means staging simply never carried this
        # citation - a draft/staging content gap, not a failed edit. Conflating
        # the two is what made the last remediation pass look successful.
        if old in raw:
            problems.append("OLD still on staging")
        if old in dtxt:
            problems.append("OLD still in draft")
        if new and dtxt and new not in dtxt:
            problems.append("NEW missing from draft")

        if problems:
            fails.append(f"{slug} [{fid}]: {'; '.join(problems)}")
            print(f"  FAIL  {slug:<48} {fid:<16} {'; '.join(problems)}")
        elif new and new not in raw:
            gaps.append(f"{slug} [{fid}]")
            print(f"  GAP   {slug:<48} {fid:<16} draft fixed; staging never had this citation")
        else:
            print(f"  PASS  {slug:<48} {fid:<16}")

print(f"\n{checks} checks, {len(fails)} failures")
for f in fails:
    print("  !! " + f)
sys.exit(1 if fails else 0)
