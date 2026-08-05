"""Voice / human-authorship self-audit: analyse a page and record the attestation.

The mechanical gate (`article_audit.py`) requires a CURRENT voice-audit record
before a page can pass. This tool produces that record. It exists so the voice
step in `editorial-os/docs/human-authorship-voice-engine.md` cannot be silently
skipped the way it was on 2026-07-30.

Usage
-----
Analyse (no write) -- prints the mechanical metrics + the subjective checklist:
    python scripts/voice_audit.py --slug what-happens-to-directors-in-liquidation

Record the attestation AFTER genuinely doing the voice pass (Opus):
    python scripts/voice_audit.py --slug <slug> --record \
        --by claude-opus-4-8 --scenes 6 --bite 3 \
        --tone pass --rhythm pass --read-aloud pass --verdict pass \
        --notes "persona warmth top+decision point; 3 asymmetrical lines"

The mechanical numbers (pronoun density, zero-you sections, rhythm, prose hash)
are measured and written automatically. The subjective fields (--scenes, --bite,
--tone, --rhythm, --read-aloud, --verdict, --notes) are YOUR attestation that the
non-mechanical checks in the voice engine were actually reviewed. Record the pass
honestly; a false attestation defeats the purpose of the gate.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import voice_metrics as vm

SCRIPTS_DIR = Path(__file__).resolve().parent
REPO = SCRIPTS_DIR.parent
AUDIT_DIR = REPO / "editorial-os" / "voice-audits"

# CLAUDE.md rule: "after 4+ passes still reading AI-edited, stop patching and
# redraft fresh from spec". This threshold is measured from git history: count
# commits touching the draft file since the last commit tagged 'redraft:' in
# its message (or since the file was created if there is no such marker).
REDRAFT_PASS_CEILING = 4


def count_passes_since_redraft(draft_path: Path) -> tuple[int, str]:
    """
    Return (pass_count, baseline_ref) where pass_count is the number of git
    commits touching the draft file since the most recent 'redraft:' marker
    commit (or since file creation). baseline_ref is the SHA of the marker
    commit, or 'file-creation' if no marker.

    A 'redraft:' marker is any commit whose subject line starts with 'redraft:'
    (case-insensitive). Use it to signal a fresh baseline after iterative edits
    would otherwise accumulate AI signature.
    """
    try:
        rel = str(draft_path.relative_to(REPO))
    except ValueError:
        rel = str(draft_path)
    try:
        # Find the most recent commit whose subject starts with 'redraft:' AND
        # touches this file. If none exists, we count all commits touching it.
        result = subprocess.run(
            ["git", "-C", str(REPO), "log", "--format=%H%x00%s", "--", rel],
            capture_output=True, text=True, timeout=10, encoding="utf-8", errors="replace",
        )
        if result.returncode != 0:
            return (0, "git-unavailable")
        lines = [l for l in result.stdout.splitlines() if l.strip()]
        # Walk from newest to oldest; pass_count is the number of commits above
        # the marker (i.e., commits newer than the last redraft baseline).
        baseline_ref = "file-creation"
        pass_count = len(lines)
        for i, line in enumerate(lines):
            try:
                sha, subject = line.split("\x00", 1)
            except ValueError:
                continue
            if subject.lower().startswith("redraft:"):
                pass_count = i  # commits ABOVE this marker
                baseline_ref = sha[:12]
                break
        return (pass_count, baseline_ref)
    except (FileNotFoundError, subprocess.TimeoutExpired, subprocess.SubprocessError):
        return (0, "git-error")


def find_draft(slug: str) -> Path | None:
    matches = sorted((REPO / "drafts").glob(f"*_{slug}.html"))
    if not matches:
        matches = [f for f in (REPO / "drafts").glob("*.html") if slug in f.name]
    return matches[0] if matches else None


def record_path(slug: str) -> Path:
    return AUDIT_DIR / f"{slug}.json"


def analyse(raw: str) -> dict:
    return vm.full_report(raw)


def print_analysis(slug: str, rep: dict) -> None:
    m = rep["metrics"]
    print(f"Voice self-audit -- {slug}")
    print(f"  prose_sha : {rep['prose_sha'][:16]}...")
    print(f"  body words: {m['words']}")
    print(f"  you/your  : {m['you']:>3}  = {m['you_per_1k']}/1k   (floor {vm.YOU_FLOOR}, ceiling {vm.YOU_CEILING})")
    print(f"  we/our/us : {m['we']:>3}  = {m['we_per_1k']}/1k   (floor {vm.WE_FLOOR})")
    print(f"  I/my      : {m['i']:>3}  = {m['i_per_1k']}/1k   (ceiling {vm.I_CEILING})")
    zy = rep["sections_over_200w_without_you"]
    print(f"  sections >200w with zero 'you': {len(zy)}" + (f"  {[s['section'] for s in zy]}" if zy else "  (pass)"))
    r = rep["rhythm"]
    print(f"  rhythm    : paras={r['paras']} cv={r['cv']} uniform={r['uniform']}")
    print(f"  scene proxy (loose, not a gate metric): {rep['scene_proxy']}")
    print()
    print("  Subjective checks you must review by hand (voice engine self-audit):")
    print("   - >=3 concrete scenes per 1,000 words (real moments, not category labels)")
    print("   - >=2 lines of genuine evaluative bite / >=1 asymmetrical compression line")
    print("   - tone shifts by section (not one even register)")
    print("   - read aloud: no monotone run of same-shape paragraphs")
    print("   - persona warmth near the top and at the decision point")


def do_record(slug: str, raw: str, args, draft_path: Path) -> int:
    rep = analyse(raw)

    # CLAUDE.md redraft rule: block --record when the draft has been iterated
    # on more than REDRAFT_PASS_CEILING times since the last 'redraft:' marker.
    # Iterative patching accumulates AI signature; the honest fix is to redraft
    # from spec, not keep polishing. Override with --override-redraft-rule if
    # a specific case genuinely warrants continuing the iteration.
    pass_count, baseline_ref = count_passes_since_redraft(draft_path)
    if pass_count >= REDRAFT_PASS_CEILING and not args.override_redraft_rule and not args.redraft_now:
        print(
            f"ERROR: {pass_count} commits touch this draft since the last 'redraft:' marker "
            f"(baseline {baseline_ref}). CLAUDE.md rule: after {REDRAFT_PASS_CEILING}+ passes stop patching and "
            f"redraft fresh from spec. Options:\n"
            f"  --redraft-now             : record a fresh baseline (make sure your next commit "
            f"subject starts with 'redraft:' so the counter resets)\n"
            f"  --override-redraft-rule R : force through with reason R recorded in the audit log",
            file=sys.stderr,
        )
        return 3

    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    record = {
        "slug": slug,
        "audited_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "audited_by": args.by,
        "prose_sha": rep["prose_sha"],
        "passes_since_baseline": {
            "count": pass_count,
            "baseline_ref": baseline_ref,
            "override_reason": args.override_redraft_rule or None,
            "redraft_now": bool(args.redraft_now),
        },
        "measured": {
            "metrics": rep["metrics"],
            "sections_over_200w_without_you": rep["sections_over_200w_without_you"],
            "rhythm": rep["rhythm"],
            "scene_proxy": rep["scene_proxy"],
        },
        "attested": {
            "concrete_scenes": args.scenes,
            "evaluative_bite_lines": args.bite,
            "tone_modulation": args.tone,
            "rhythm_varied": args.rhythm,
            "read_aloud_ok": args.read_aloud,
            "notes": args.notes,
            "stranger_read_report": args.stranger_read_report or None,
        },
        "verdict": args.verdict,
    }
    record_path(slug).write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(f"Recorded voice audit: {record_path(slug).relative_to(REPO)}")
    print(f"  verdict={args.verdict}  prose_sha={rep['prose_sha'][:16]}...")
    print(f"  passes since baseline: {pass_count} (baseline={baseline_ref})")
    if args.verdict != "pass":
        print("  NOTE: verdict is not 'pass' -- the gate will still fail until it is.")
    if pass_count >= REDRAFT_PASS_CEILING - 1 and not args.override_redraft_rule and not args.redraft_now:
        print(f"  WARNING: {pass_count} passes since redraft baseline; the next --record will require --redraft-now or --override-redraft-rule.")
    if not args.stranger_read_report and pass_count >= 2:
        print("  WARNING: no --stranger-read-report supplied; from pass 3 onward, consider running scripts/stranger_read.py to catch clever prose the writer cannot see.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Voice/human-authorship self-audit and attestation.")
    ap.add_argument("--slug", help="Page slug (drafts/*_<slug>.html)")
    ap.add_argument("--file", help="Explicit draft path (overrides --slug lookup)")
    ap.add_argument("--record", action="store_true", help="Write the attestation record")
    ap.add_argument("--by", default="unknown", help="Who/what ran the pass, e.g. claude-opus-4-8")
    ap.add_argument("--scenes", type=int, default=0, help="Concrete scenes you counted")
    ap.add_argument("--bite", type=int, default=0, help="Evaluative-bite/asymmetrical lines you counted")
    ap.add_argument("--tone", choices=["pass", "fail"], default="fail", help="Tone modulates by section?")
    ap.add_argument("--rhythm", choices=["pass", "fail"], default="fail", help="Rhythm varied (read-aloud)?")
    ap.add_argument("--read-aloud", dest="read_aloud", choices=["pass", "fail"], default="fail",
                    help="Read-aloud flatness check")
    ap.add_argument("--verdict", choices=["pass", "fail"], default="fail", help="Overall voice verdict")
    ap.add_argument("--notes", default="", help="Short free-text attestation notes")
    ap.add_argument("--stranger-read-report", dest="stranger_read_report",
                    help="Path to a stranger-read report (see scripts/stranger_read.py). "
                         "Recommended from pass 3 onwards; catches clever prose the writer cannot see.")
    ap.add_argument("--override-redraft-rule", dest="override_redraft_rule",
                    help="Reason string. Forces --record through the 4-pass redraft ceiling. "
                         "Recorded in the audit log for reviewer visibility.")
    ap.add_argument("--redraft-now", dest="redraft_now", action="store_true",
                    help="Signal that this record is the fresh baseline after a redraft. "
                         "Your next commit subject MUST start with 'redraft:' to reset the counter.")
    args = ap.parse_args()

    if not args.slug and not args.file:
        print("ERROR: pass --slug or --file", file=sys.stderr)
        return 2

    if args.file:
        draft = Path(args.file)
        slug = args.slug or draft.stem.split("_", 1)[-1]
    else:
        draft = find_draft(args.slug)
        slug = args.slug
    if not draft or not draft.exists():
        print(f"ERROR: draft not found for slug/file: {args.slug or args.file}", file=sys.stderr)
        return 2

    raw = draft.read_text(encoding="utf-8")

    if args.record:
        return do_record(slug, raw, args, draft)

    print_analysis(slug, analyse(raw))
    rec = record_path(slug)
    print()
    if rec.exists():
        data = json.loads(rec.read_text(encoding="utf-8"))
        fresh = data.get("prose_sha") == vm.prose_sha(raw)
        print(f"Existing record: verdict={data.get('verdict')} audited_at={data.get('audited_at')} "
              f"fresh={'yes' if fresh else 'NO -- prose changed, re-record'}")
    else:
        print("No voice-audit record yet. After the pass, re-run with --record and the attested flags.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
