"""Tracked attestation that a page went through the Bernstein pipeline.

Why this exists
---------------
`editorial-os/bernstein-state/` is in .gitignore. That makes it local to one
machine and invisible in worktrees, in git history and in review. On 2026-08-17
a full redraft of closing-a-limited-company was written, gated at 33/33 and
pushed to staging without a single Bernstein stage being opened, and nothing
anywhere could show that afterwards. The operator asked how the rule became
optional; the answer is that the evidence was never durable.

So this script writes a *tracked* record, next to the voice audits, which
already work for exactly this reason. `article_audit.py` check 34 then requires
one whose prose hash matches the current draft. Any prose edit invalidates it,
which forces the pipeline to be re-run rather than outrun. That is the same
mechanism that makes the voice-audit check (26) hard to dodge.

What it records is an attestation, not proof. It cannot verify that the stage
work was done well. It can make skipping it visible, which is the part that
failed.

Grandfathering
--------------
Roughly 300 drafts predate this check and have no pipeline trail. Failing all
of them at once would make the gate useless noise, so `--build-baseline`
records the current prose hash of every page that has no attestation. Those
pages pass while their prose is untouched. The moment the prose changes, the
baseline no longer matches and the page owes a real pipeline run. The rule
therefore binds on everything written or rewritten from now on, and disturbs
nothing that is merely sitting there.

Usage
-----
    python scripts/bernstein_attest.py --slug <slug>            # show status
    python scripts/bernstein_attest.py --slug <slug> --record \
        --by claude-opus-5 --stages research,draft,review,revise,humanise,gate \
        --notes "..."
    python scripts/bernstein_attest.py --build-baseline         # one-off seed
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
REPO = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))
import voice_metrics as vm  # noqa: E402

RUNS_DIR = REPO / "editorial-os" / "bernstein-runs"
BASELINE = RUNS_DIR / "_baseline.json"
LOCAL_STATE = REPO / "editorial-os" / "bernstein-state"
DRAFTS = REPO / "drafts"

# The stages bernstein.js itself requires before the gate stage will accept a
# page (STAGE_REQUIREMENTS.gate), plus the gate stage. Kept in this order so a
# reader can see what a complete run looks like.
PIPELINE_STAGES = ["research", "draft", "review", "revise", "humanise", "gate"]

# A rewrite of a published page does not always need 'research'. These are the
# stages that must always appear, whatever the task.
REQUIRED_STAGES = ["review", "humanise", "gate"]


def find_draft(slug: str) -> Path | None:
    hits = sorted(DRAFTS.glob(f"*_{slug}.html"))
    return hits[0] if hits else None


def read_baseline() -> dict:
    if not BASELINE.exists():
        return {}
    try:
        return json.loads(BASELINE.read_text(encoding="utf-8")).get("pages", {})
    except Exception:  # noqa: BLE001
        return {}


def local_stage_history(slug: str) -> list[str]:
    """Stages marked completed in the untracked local state, if it is present.

    Used only to pre-fill --stages so an operator does not retype what the
    pipeline already knows. Absence proves nothing: the directory is gitignored
    and simply will not exist in a worktree.
    """
    state = LOCAL_STATE / slug / "state.json"
    if not state.exists():
        return []
    try:
        data = json.loads(state.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return []
    done = []
    for entry in data.get("stage_history", []):
        if entry.get("status") == "completed" and entry.get("stage") not in done:
            done.append(entry["stage"])
    return done


def status(slug: str, raw: str) -> tuple[bool, str]:
    """Return (ok, human-readable reason). Mirrors article_audit check 34."""
    sha = vm.prose_sha(raw)
    rec = RUNS_DIR / f"{slug}.json"
    if rec.exists():
        try:
            data = json.loads(rec.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            return False, f"attestation unreadable: {e}"
        if data.get("prose_sha") != sha:
            return False, ("attestation STALE: the prose changed after the pipeline ran, "
                           "so the page owes another pass through it")
        missing = [s for s in REQUIRED_STAGES if s not in (data.get("stages_completed") or [])]
        if missing:
            return False, f"attested but missing required stage(s): {', '.join(missing)}"
        return True, f"pipeline attested {data.get('attested_at')} by {data.get('attested_by')}"
    base = read_baseline()
    if slug in base:
        if base[slug] == sha:
            return True, "grandfathered: predates the check and the prose is unchanged"
        return False, ("grandfathered baseline no longer matches: the prose has been edited, "
                       "so this page now needs a real Bernstein run")
    return False, "no Bernstein attestation for this page"


def main() -> int:
    ap = argparse.ArgumentParser(description="Tracked Bernstein pipeline attestation.")
    ap.add_argument("--slug")
    ap.add_argument("--record", action="store_true")
    ap.add_argument("--by", default="", help="Who/what ran the stages, e.g. claude-opus-5")
    ap.add_argument("--stages", default="", help="Comma-separated stages completed")
    ap.add_argument("--task", default="", help="draft | rewrite | review | trust-pass")
    ap.add_argument("--notes", default="")
    ap.add_argument("--build-baseline", action="store_true",
                    help="One-off: grandfather every page that has no attestation yet.")
    args = ap.parse_args()

    RUNS_DIR.mkdir(parents=True, exist_ok=True)

    if args.build_baseline:
        pages = {}
        for f in sorted(DRAFTS.glob("*.html")):
            slug = f.stem.split("_", 1)[1] if "_" in f.stem else f.stem
            if (RUNS_DIR / f"{slug}.json").exists():
                continue
            pages[slug] = vm.prose_sha(f.read_text(encoding="utf-8", errors="replace"))
        BASELINE.write_text(json.dumps({
            "_comment": ("Grandfather map for article_audit.py check 34. Each entry is the prose "
                         "hash of a page that predates the Bernstein attestation requirement. "
                         "While the hash matches, the page passes. Edit the prose and it stops "
                         "matching, and the page must then go through the pipeline. Do not add "
                         "entries by hand to dodge the check."),
            "_built": date.today().isoformat(),
            "pages": pages,
        }, indent=2) + "\n", encoding="utf-8")
        print(f"Baseline written: {len(pages)} page(s) grandfathered -> {BASELINE}")
        return 0

    if not args.slug:
        ap.error("--slug is required (or use --build-baseline)")

    draft = find_draft(args.slug)
    if not draft:
        print(f"ERROR: no draft found for slug '{args.slug}'")
        return 2
    raw = draft.read_text(encoding="utf-8", errors="replace")

    if not args.record:
        ok, reason = status(args.slug, raw)
        print(f"Bernstein attestation -- {args.slug}")
        print(f"  prose_sha : {vm.prose_sha(raw)[:16]}...")
        print(f"  status    : {'OK' if ok else 'FAIL'} -- {reason}")
        seen = local_stage_history(args.slug)
        print(f"  local state: {', '.join(seen) if seen else 'none in this worktree (gitignored)'}")
        return 0 if ok else 1

    stages = [s.strip() for s in args.stages.split(",") if s.strip()] or local_stage_history(args.slug)
    if not stages:
        print("ERROR: --stages is required (nothing found in local state to fall back on)")
        return 2
    missing = [s for s in REQUIRED_STAGES if s not in stages]
    if missing:
        print(f"ERROR: refusing to record. Missing required stage(s): {', '.join(missing)}")
        print(f"       Required at minimum: {', '.join(REQUIRED_STAGES)}")
        return 2
    if not args.by:
        print("ERROR: --by is required, so the record says who ran it")
        return 2

    rec = {
        "slug": args.slug,
        "attested_at": date.today().isoformat(),
        "attested_by": args.by,
        "task": args.task or None,
        "prose_sha": vm.prose_sha(raw),
        "stages_completed": stages,
        "unknown_stages": [s for s in stages if s not in PIPELINE_STAGES],
        "local_state_present": bool(local_stage_history(args.slug)),
        "notes": args.notes,
    }
    out = RUNS_DIR / f"{args.slug}.json"
    out.write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    print(f"Recorded Bernstein attestation: {out}")
    print(f"  stages    : {', '.join(stages)}")
    print(f"  prose_sha : {rec['prose_sha'][:16]}...")
    if rec["unknown_stages"]:
        print(f"  WARNING: not pipeline stage names: {', '.join(rec['unknown_stages'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
