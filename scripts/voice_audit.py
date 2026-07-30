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
import sys
from datetime import datetime, timezone
from pathlib import Path

import voice_metrics as vm

SCRIPTS_DIR = Path(__file__).resolve().parent
REPO = SCRIPTS_DIR.parent
AUDIT_DIR = REPO / "editorial-os" / "voice-audits"


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


def do_record(slug: str, raw: str, args) -> int:
    rep = analyse(raw)
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    record = {
        "slug": slug,
        "audited_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "audited_by": args.by,
        "prose_sha": rep["prose_sha"],
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
        },
        "verdict": args.verdict,
    }
    record_path(slug).write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(f"Recorded voice audit: {record_path(slug).relative_to(REPO)}")
    print(f"  verdict={args.verdict}  prose_sha={rep['prose_sha'][:16]}...")
    if args.verdict != "pass":
        print("  NOTE: verdict is not 'pass' -- the gate will still fail until it is.")
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
        return do_record(slug, raw, args)

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
