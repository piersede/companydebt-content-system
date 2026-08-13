"""Pull files/dirs from WP staging via SFTP for local inspection/editing.

Mirrors the connection pattern in wp_push.py. Read-only against staging:
downloads remote paths into tmp/staging_pull/ preserving structure.

Usage:
    python scripts/sftp_pull.py --list /wp-content/themes/company-debt-webpigment/inc
    python scripts/sftp_pull.py --get /wp-content/themes/company-debt-webpigment/inc/init.php
    python scripts/sftp_pull.py --get-tree /wp-content/themes/company-debt-webpigment/inc/Content
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


def _client():
    host = os.environ["SFTP_HOST"]
    port = int(os.environ.get("SFTP_PORT", "2222"))
    t = paramiko.Transport((host, port))
    t.connect(username=os.environ["SFTP_USER"], password=os.environ["SFTP_PASS"])
    return t, paramiko.SFTPClient.from_transport(t)


def do_list(remote: str) -> None:
    t, s = _client()
    try:
        for a in sorted(s.listdir_attr(remote), key=lambda x: x.filename):
            kind = "d" if stat.S_ISDIR(a.st_mode) else "f"
            print(f"{kind} {a.st_size:>9} {remote.rstrip('/')}/{a.filename}")
    finally:
        s.close(); t.close()


def _get_one(s, remote: str) -> pathlib.Path:
    local = DEST / remote.lstrip("/")
    local.parent.mkdir(parents=True, exist_ok=True)
    s.get(remote, str(local))
    print(f"pulled {remote} -> {local}")
    return local


def do_get(remotes: list[str]) -> None:
    t, s = _client()
    try:
        for r in remotes:
            _get_one(s, r)
    finally:
        s.close(); t.close()


def _walk_get(s, remote: str) -> None:
    for a in s.listdir_attr(remote):
        rp = posixpath.join(remote, a.filename)
        if stat.S_ISDIR(a.st_mode):
            _walk_get(s, rp)
        else:
            _get_one(s, rp)


def do_get_tree(remote: str) -> None:
    t, s = _client()
    try:
        _walk_get(s, remote)
    finally:
        s.close(); t.close()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--list")
    p.add_argument("--get", nargs="+")
    p.add_argument("--get-tree")
    a = p.parse_args()
    if a.list:
        do_list(a.list)
    if a.get:
        do_get(a.get)
    if a.get_tree:
        do_get_tree(a.get_tree)
    if not (a.list or a.get or a.get_tree):
        p.error("nothing to do")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
