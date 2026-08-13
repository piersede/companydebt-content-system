#!/usr/bin/env python
"""Find out which mu-plugin files are present on LIVE, without executing any of them.

Read-only. A WP Engine "file system only" copy carries every file, so throwaway one-shot
helpers left on staging end up on live, where there is no password wall in front of them.
On 2026-08-06 two of them turned out to be sitting on companydebt.com: unauthenticated
endpoints that grant themselves administrator rights.

How the check works. Requesting an mu-plugin file directly runs it, but every one of
these scripts checks for its token in the query string and returns immediately when it is
absent, so a request WITHOUT the token produces an empty 200 and no side effect. A file
that is not there falls through to WordPress and gives a 404 with a full error page. So:

    200 + tiny body  -> present
    500 + tiny body  -> present (errors when run outside its normal context)
    404 + big body   -> absent

Never add the token to these requests. The token is what makes the script act.

    python scripts/sweep_live_mu_plugins.py
"""
from __future__ import annotations

import os
import pathlib
import sys

import paramiko
import requests
from dotenv import load_dotenv

ROOT = pathlib.Path(__file__).resolve().parents[1]
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
from _env import load_env as _load_env
_load_env()
LIVE = os.environ.get("CD_LIVE_URL", "https://www.companydebt.com").rstrip("/")
MU = "wp-content/mu-plugins"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) cd-live-sweep"

# Names from past clean-ups that are not on staging any more but may still be on live.
# The 2026-07-29 purge removed 71 files and did not record their names; these are the
# ones recoverable from docs/archive/codex-push-payloads/.
KNOWN_PAST = [
    "acf_cta_reader_0ae4c9c987d34b08.php",
    "acf_cta_v2_updater_28baade4858f4585.php",
    "mu-cd-push-e696d84b6c16.php",
    "cd-resave.php",
]

# A file whose name says it is a one-shot, whatever it currently contains.
THROWAWAY_HINTS = ("mu-cd-push", "mu-cd-pushraw", "codex-push", "acf_cta_", "cd-resave")


def staging_php_names() -> list[str]:
    t = paramiko.Transport((os.environ["SFTP_HOST"], int(os.environ.get("SFTP_PORT", "2222"))))
    t.connect(username=os.environ["SFTP_USER"], password=os.environ["SFTP_PASS"])
    sftp = paramiko.SFTPClient.from_transport(t)
    try:
        return sorted(n for n in sftp.listdir(MU) if n.endswith(".php"))
    finally:
        sftp.close()
        t.close()


def archived_codex_names() -> list[str]:
    d = ROOT / "docs" / "archive" / "codex-push-payloads"
    if not d.is_dir():
        return []
    return sorted(f"{p.stem}.php" for p in d.glob("codex-push-*.html"))


def probe(session: requests.Session, name: str) -> tuple[bool, str]:
    r = session.get(f"{LIVE}/{MU}/{name}", timeout=40)
    present = r.status_code != 404
    return present, f"{r.status_code} {len(r.content)}b"


def main() -> int:
    names = sorted(set(staging_php_names()) | set(KNOWN_PAST) | set(archived_codex_names()))
    s = requests.Session()
    s.headers["User-Agent"] = UA

    print(f"probing {len(names)} filenames against {LIVE}\n")
    present, absent, suspect = [], [], []
    for n in names:
        ok, detail = probe(s, n)
        (present if ok else absent).append(n)
        if ok and any(h in n for h in THROWAWAY_HINTS):
            suspect.append((n, detail))
        print(f"  {'PRESENT' if ok else 'absent ':<8} {detail:<10} {n}")

    print(f"\n{len(present)} present on live, {len(absent)} absent")
    if suspect:
        print(f"\n{len(suspect)} THROWAWAY SCRIPT(S) ON LIVE - remove via WP Engine:")
        for n, detail in suspect:
            print(f"    {MU}/{n}   ({detail})")
        print("\nDo NOT open these with their token in the URL. The token is what runs them.")
    else:
        print("\nNo throwaway one-shots found on live.")
    return 1 if suspect else 0


if __name__ == "__main__":
    sys.exit(main())
