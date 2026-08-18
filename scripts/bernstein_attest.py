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

Two kinds of record
-------------------
A page can satisfy the check in one of two ways, and the record says which.

  pipeline-run   The stages were actually run, and the page was written or
                 rewritten through them. This is what a new page or a real
                 redraft produces.

  verification   Somebody read an existing page against the stage criteria and
                 either confirmed it holds up, or fixed the specific things that
                 did not. No redraft.

The second exists because most pages that lose their exemption lose it for a
five-word fact correction, not a rewrite. A full pipeline run on those is a lot
of work to reach the conclusion "it was fine". The point of going back to a page
is to CHECK it, and to fix only what fails.

A verification is a weaker claim than a pipeline run, and it is stored as such,
so nobody later reads one as the other. Both are hashed against the prose in the
same way, so a later edit invalidates either. The freshness discipline does not
soften.

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
    python scripts/bernstein_attest.py --slug <slug> --verify \
        --by claude-opus-5 --checked review,humanise,gate \
        --outcome pass --notes "read against the stage criteria, nothing to fix"
    python scripts/bernstein_attest.py --build-baseline         # one-off seed
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
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
# bernstein.js STAGE_SEQUENCE, plus the review-class stage packs that exist in
# runtime-packs/stages/ and are run as their own passes.
PIPELINE_STAGES = ["research", "outline", "brief", "source-grounding", "draft", "review",
                   "adversarial-review", "trust-pass", "revise", "humanise",
                   "final-polish", "gate", "publish"]

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


def last_prose_change(slug: str, path: Path) -> str | None:
    """Date the CURRENT prose of this draft first appeared, from git history.

    Walks the commits that touched the file, newest first, recomputing the prose
    hash at each until it stops matching what is on disk. Table, comment and
    attribute edits do not move the hash, so they do not count as prose changes.
    Returns None when git cannot say.
    """
    import subprocess
    rel = path.relative_to(REPO).as_posix()
    try:
        log = subprocess.run(["git", "-C", str(REPO), "log", "--format=%H %cI", "--", rel],
                             capture_output=True, text=True, timeout=60).stdout.splitlines()
    except Exception:  # noqa: BLE001
        return None
    current = vm.prose_sha(path.read_text(encoding="utf-8", errors="replace"))
    found = None
    for line in log:
        if not line.strip():
            continue
        commit, _, when = line.partition(" ")
        try:
            blob = subprocess.run(["git", "-C", str(REPO), "show", f"{commit}:{rel}"],
                                  capture_output=True, text=True, timeout=60).stdout
        except Exception:  # noqa: BLE001
            break
        if not blob or vm.prose_sha(blob) != current:
            break
        found = when[:10]
    return found


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
            return False, ("attestation STALE: the prose changed after it was written, "
                           "so the page owes another look")
        kind = data.get("kind") or "pipeline-run"
        covered = (data.get("stages_completed") or []) + (data.get("stages_checked") or [])
        missing = [s for s in REQUIRED_STAGES if s not in covered]
        if missing:
            return False, f"attested but missing required stage(s): {', '.join(missing)}"
        word = "verified" if kind == "verification" else "pipeline attested"
        return True, f"{word} {data.get('attested_at')} by {data.get('attested_by')}"
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
    ap.add_argument("--record", action="store_true",
                    help="Record that the pipeline stages were actually run.")
    ap.add_argument("--verify", action="store_true",
                    help=("Record that an existing page was CHECKED against the stage "
                          "criteria, and fixed only where it failed. A weaker claim than "
                          "--record, stored as such."))
    ap.add_argument("--checked", default="",
                    help="--verify only: comma-separated stage criteria checked")
    ap.add_argument("--outcome", choices=["pass", "fixed"], default=None,
                    help=("--verify only: 'pass' if the page held up as written, "
                          "'fixed' if specific things were corrected"))
    ap.add_argument("--by", default="", help="Who/what ran the stages, e.g. claude-opus-5")
    ap.add_argument("--stages", default="", help="Comma-separated stages completed")
    ap.add_argument("--task", default="", help="draft | rewrite | review | trust-pass")
    ap.add_argument("--notes", default="")
    ap.add_argument("--build-baseline", action="store_true",
                    help="One-off: grandfather every page that has no attestation yet.")
    ap.add_argument("--baseline-recent-days", type=int, default=30,
                    help=("--build-baseline only: refuse to grandfather a page whose prose "
                          "changed within this many days. Default 30."))
    args = ap.parse_args()

    RUNS_DIR.mkdir(parents=True, exist_ok=True)

    if args.build_baseline:
        # A baseline is meant to excuse pages that PREDATE the requirement. Built
        # naively it does the opposite: it records whatever the prose looks like
        # today, so an edit made outside the pipeline this morning gets a
        # permanent pass. That is exactly what happened on 2026-08-17, hours
        # after a 26-page sweep. So anything edited recently is held back, and
        # listed, rather than blessed.
        cutoff = (date.today() - timedelta(days=args.baseline_recent_days)).isoformat()
        pages, held = {}, []
        for f in sorted(DRAFTS.glob("*.html")):
            slug = f.stem.split("_", 1)[1] if "_" in f.stem else f.stem
            if (RUNS_DIR / f"{slug}.json").exists():
                continue
            changed = last_prose_change(slug, f)
            if changed and changed >= cutoff:
                held.append((slug, changed))
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
        if held:
            print(f"\nHELD BACK: {len(held)} page(s) had prose edited since {cutoff}.")
            print("These are NOT grandfathered. Check each one and record the result:")
            for slug, when in sorted(held, key=lambda x: x[1], reverse=True):
                print(f"  {when}  {slug}")
        return 0

    if not args.slug:
        ap.error("--slug is required (or use --build-baseline)")

    draft = find_draft(args.slug)
    if not draft:
        print(f"ERROR: no draft found for slug '{args.slug}'")
        return 2
    raw = draft.read_text(encoding="utf-8", errors="replace")

    if args.verify:
        checked = [c.strip() for c in args.checked.split(",") if c.strip()]
        missing = [st for st in REQUIRED_STAGES if st not in checked]
        if missing:
            print(f"ERROR: refusing to record. Not checked: {', '.join(missing)}")
            print(f"       A verification must at least cover: {', '.join(REQUIRED_STAGES)}")
            return 2
        if not args.by:
            print("ERROR: --by is required, so the record says who checked it")
            return 2
        if not args.outcome:
            print("ERROR: --outcome is required: 'pass' if the page held up, "
                  "'fixed' if things were corrected")
            return 2
        if args.outcome == "fixed" and not args.notes:
            print("ERROR: --notes is required when --outcome is 'fixed'. "
                  "Say what was wrong, or the record is worthless to the next reader.")
            return 2
        rec = {
            "slug": args.slug,
            "kind": "verification",
            "attested_at": date.today().isoformat(),
            "attested_by": args.by,
            "task": args.task or "verify",
            "prose_sha": vm.prose_sha(raw),
            "stages_checked": checked,
            "outcome": args.outcome,
            "unknown_stages": [st for st in checked if st not in PIPELINE_STAGES],
            "local_state_present": bool(local_stage_history(args.slug)),
            "notes": args.notes,
        }
        out = RUNS_DIR / f"{args.slug}.json"
        out.write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
        print(f"Recorded Bernstein verification: {out}")
        print(f"  checked   : {', '.join(checked)}")
        print(f"  outcome   : {args.outcome}")
        print(f"  prose_sha : {rec['prose_sha'][:16]}...")
        if rec["unknown_stages"]:
            print(f"  WARNING: not pipeline stage names: {', '.join(rec['unknown_stages'])}")
        return 0

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
        "kind": "pipeline-run",
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
