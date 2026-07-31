#!/usr/bin/env python3
"""
Plain-English check: is there finished work sitting on a branch that never
made it into main?

Run it any time:  python scripts/check_unmerged_branches.py

Exits 1 (and prints a loud warning) if any branch has commits main doesn't
have and the newest of those commits is more than STALE_DAYS old. Exits 0
otherwise.
"""

import subprocess
import sys
from datetime import datetime, timezone

STALE_DAYS = 2  # branches idle longer than this get flagged


def run(*args):
    return subprocess.run(
        ["git", *args], capture_output=True, text=True, check=True
    ).stdout.strip()


def main():
    try:
        run("rev-parse", "--is-inside-work-tree")
    except subprocess.CalledProcessError:
        print("Not inside a git repo — nothing to check.")
        return 0

    # --format gives the bare branch name, with no decoration to strip. Parsing
    # the default output breaks on the markers git puts in column 1: "*" for the
    # current branch and "+" for a branch checked out in another worktree. This
    # repo uses worktrees constantly, so "+" lines used to parse down to "+" and
    # crash on "git rev-list main..+" — the check died exactly when it mattered.
    branches = [
        b.strip()
        for b in run(
            "branch", "--no-merged", "main", "--format=%(refname:short)"
        ).splitlines()
        if b.strip()
    ]
    branches = [b for b in branches if b != "main"]

    if not branches:
        print("All clear — every branch's work is already in main.")
        return 0

    flagged = []
    for b in branches:
        count = int(run("rev-list", "--count", f"main..{b}"))
        if count == 0:
            continue
        last_commit_iso = run("log", "-1", "--format=%aI", b)
        last_commit_dt = datetime.fromisoformat(last_commit_iso)
        age_days = (datetime.now(timezone.utc) - last_commit_dt).days
        subject = run("log", "-1", "--format=%s", b)
        flagged.append((b, count, age_days, subject))

    if not flagged:
        print("All clear — every branch's work is already in main.")
        return 0

    stale = [f for f in flagged if f[2] >= STALE_DAYS]

    print("=" * 70)
    if stale:
        print("PIERS — YOU NEED TO MERGE NOW.")
        print()
        print("Finished work is sitting on a branch, not in main. If you don't")
        print("merge it, it's easy to forget it exists and lose track of it.")
    else:
        print("Heads up - you have branch work not yet in main (still fresh).")
    print("=" * 70)
    print()

    for branch, count, age, subject in sorted(flagged, key=lambda f: -f[2]):
        tag = "STALE" if age >= STALE_DAYS else "recent"
        plural = "commit" if count == 1 else "commits"
        print(f"  [{tag:>6}] {branch}")
        print(f"           {count} {plural} not in main, newest is {age} day(s) old")
        print(f"           latest: \"{subject}\"")
        print()

    print("To merge a branch into main:")
    print("  git checkout main")
    print("  git merge --no-ff <branch-name>")
    print("  git push origin main")
    print("  git branch -d <branch-name>   (once merged, delete it)")

    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
