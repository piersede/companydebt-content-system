"""Locate and load the repo `.env`, including from a git worktree.

Why this exists
---------------
Most scripts here did:

    ROOT = pathlib.Path(__file__).resolve().parents[1]
    load_dotenv(ROOT / ".env")

That is correct in the main checkout. It is wrong in a git worktree: `ROOT`
is then `.claude/worktrees/<name>/`, which holds no `.env`, so every credential
came back empty and the script aborted saying they were "missing from .env" —
naming a file it had never looked at, while the real one sat three levels up.

That bit during a live push on 2026-08-13: `publish_to_live.py` and
`check_live_form_entries.py` both refused to run, the second of which is the
post-push safety check that confirms Gravity Forms entries survived. A safety
check that silently cannot run is worse than one that is absent, because the
operator reads the error as a config problem rather than as "the check did not
happen".

Usage
-----
    from _env import load_env
    load_env()
"""

from __future__ import annotations

import pathlib

from dotenv import load_dotenv

_SCRIPTS = pathlib.Path(__file__).resolve().parent


def find_env(start: pathlib.Path | None = None) -> pathlib.Path | None:
    """Return the nearest `.env` walking upward, or None."""
    base = (start or _SCRIPTS).resolve()
    for candidate in (base, *base.parents):
        env = candidate / ".env"
        if env.is_file():
            return env
    return None


def load_env(start: pathlib.Path | None = None) -> pathlib.Path | None:
    """Load the nearest `.env` into the environment. Returns the path used."""
    env = find_env(start)
    if env is not None:
        load_dotenv(env)
    return env


if __name__ == "__main__":
    found = find_env()
    print(found if found else "no .env found walking up from scripts/")
