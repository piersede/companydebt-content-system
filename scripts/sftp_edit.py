"""Reusable SFTP helper for safe theme/plugin file edits on WP staging.

Paths are RELATIVE to the SFTP home (the site root), e.g.
``wp-content/themes/company-debt-webpigment/footer.php`` — absolute ``/...``
paths fail on this server.

API (import) or CLI:
    list  <dir>
    get   <remote> [<remote> ...]        -> tmp/staging_pull/<remote>
    put   <local> <remote> [--tag TAG]   -> backs up remote to <remote>.bak-a11y-<tag>, then uploads

Every ``put`` makes a server-side backup first, so any change is reversible.
"""
from __future__ import annotations

import argparse
import os
import pathlib
import posixpath
import stat
import sys

import paramiko
from dotenv import load_dotenv

ROOT = pathlib.Path(__file__).resolve().parents[1]
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
from _env import load_env as _load_env
_load_env()
DEST = ROOT / "tmp" / "staging_pull"


def client():
    host = os.environ["SFTP_HOST"]
    port = int(os.environ.get("SFTP_PORT", "2222"))
    t = paramiko.Transport((host, port))
    t.connect(username=os.environ["SFTP_USER"], password=os.environ["SFTP_PASS"])
    return t, paramiko.SFTPClient.from_transport(t)


def _exists(s, remote: str) -> bool:
    try:
        s.stat(remote)
        return True
    except IOError:
        return False


def do_list(remote: str) -> None:
    t, s = client()
    try:
        for a in sorted(s.listdir_attr(remote), key=lambda x: x.filename):
            kind = "d" if stat.S_ISDIR(a.st_mode) else "f"
            print(f"{kind} {a.st_size:>9} {remote.rstrip('/')}/{a.filename}")
    finally:
        s.close(); t.close()


def get(remotes: list[str]) -> list[pathlib.Path]:
    t, s = client()
    out = []
    try:
        for r in remotes:
            local = DEST / r.lstrip("/")
            local.parent.mkdir(parents=True, exist_ok=True)
            s.get(r, str(local))
            print(f"pulled {r} -> {local}")
            out.append(local)
    finally:
        s.close(); t.close()
    return out


# WP Engine serves everything under the SFTP home to the public EXCEPT
# ``_wpeprivate``, which nginx answers with 403 on both staging and live.
# Backups must live there. See _backup_path() for why this is not optional.
BACKUP_ROOT = "_wpeprivate/file-backups"


def _mkdirs(s, remote_dir: str) -> None:
    """mkdir -p over SFTP. There is no recursive mkdir primitive."""
    cur = ""
    for part in remote_dir.strip("/").split("/"):
        cur = part if not cur else f"{cur}/{part}"
        try:
            s.stat(cur)
        except IOError:
            s.mkdir(cur)


def _backup_path(remote: str, tag: str) -> str:
    """Where a backup of ``remote`` goes.

    NEVER next to the original. WordPress only executes files ending in
    ``.php``; a file ending ``.bak-<tag>`` is not executed, so the web server
    hands it over as readable source text to anyone who requests the URL.

    On 25 Aug 2026 that meant 345 server files - 45 MB of theme and mu-plugin
    source - were publicly readable under wp-content, four of them holding
    working Zoho CRM and LiveChat credentials. They had been reachable since
    at least June. An .htaccess deny rule was tried first and does nothing:
    WP Engine's nginx serves static files without consulting Apache.

    So the fix is placement, not permissions. Backups go under
    ``_wpeprivate/``, which is the one directory WP Engine refuses to serve.
    """
    return f"{BACKUP_ROOT}/{remote.lstrip('/')}.bak-a11y-{tag}"


def put(local: str, remote: str, tag: str = "edit") -> None:
    t, s = client()
    try:
        if _exists(s, remote):
            bak = _backup_path(remote, tag)
            if not _exists(s, bak):
                _mkdirs(s, posixpath.dirname(bak))
                # server-side copy via read+write (no SFTP copy primitive)
                with s.open(remote, "rb") as fh:
                    data = fh.read()
                with s.open(bak, "wb") as fh:
                    fh.write(data)
                print(f"backup  {remote} -> {bak} ({len(data)} bytes)")
            else:
                print(f"backup  {bak} already exists — keeping it")
        s.put(local, remote)
        size = s.stat(remote).st_size
        print(f"PUT     {local} -> {remote} ({size} bytes)")
    finally:
        s.close(); t.close()


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("list"); p.add_argument("remote")
    p = sub.add_parser("get"); p.add_argument("remote", nargs="+")
    p = sub.add_parser("put"); p.add_argument("local"); p.add_argument("remote")
    p.add_argument("--tag", default="edit")
    a = ap.parse_args()
    if a.cmd == "list":
        do_list(a.remote)
    elif a.cmd == "get":
        get(a.remote)
    elif a.cmd == "put":
        put(a.local, a.remote, a.tag)
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
