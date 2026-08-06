"""Find (and optionally remove) throwaway one-shot scripts in staging mu-plugins.

MANDATORY pre-flight before any code push to live. A WP Engine "file system only"
copy takes EVERY file, and everything in wp-content/mu-plugins executes on every
request with no way to disable it from wp-admin. One-shot helpers left behind by
past sessions - content pushers, batch fixers, dumpers, inspectors - therefore go
live too. Several are wp_update_post() endpoints reachable by anyone with the URL,
guarded only by a static query token and no login check.

On 2026-07-29 this found 71 of them, including four 50-60KB codex-push-*.php files
holding base64-encoded article bodies. See docs/staging-to-live-push.md.

Usage:
    python scripts/audit_mu_plugins.py            # report only, writes nothing
    python scripts/audit_mu_plugins.py --delete   # back up to tmp/ then remove

Classification: a file is "throwaway" when it is guarded by a $_GET token, calls
exit, and registers at most two hooks - i.e. it does one thing on demand and is
not persistent functionality. KEEP is an explicit allowlist and the script aborts
rather than delete anything on it.
"""
from __future__ import annotations

import argparse
import datetime
import os
import pathlib
import re
import stat
import sys

import paramiko
from dotenv import load_dotenv

ROOT = pathlib.Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

MU = "wp-content/mu-plugins"

# Real functionality. Never deleted. Add to this list, never remove from it
# without checking what the plugin actually does.
KEEP = {
    "cd-410-gone.php",
    "cd-a11y-fixes.php",
    "cd-consent-mode-defaults.php",
    "cd-faq-schema.php",
    "cd-fix-indexables.php",
    "cd-gform-hardening.php",
    "cd-gform-source-page.php",
    "cd-insolvency-data-hub.php",
    "cd-layout-fixes.php",
    "cd-livechat-secrets.php",
    "cd-livechat-zoho.php",
    "cd-pub-closures-hub.php",
    "cd-resave.php",
    "cd-rocket-flicker-fix.php",
    "cd-sector-containment2.php",
    "cd-seo-meta-rest.php",
    "cd-server-render.php",
    "mu-plugin.php",
}
KEEP_PREFIXES = ("wpe-", "wpengine-", "slt-")  # WP Engine / security core

HOOK = re.compile(r"add_(action|filter)\s*\(")
GET = re.compile(r"\$_GET\[")
# A one-shot bails out early when its token is absent. Both spellings are used:
# `exit;` and a bare top-level `return;`. Matching only exit missed two
# unauthenticated admin endpoints that had been sitting in mu-plugins for weeks.
BAIL = re.compile(r"^\s*(?:\}\s*)?(?:exit|return)\s*;", re.M)
TOKEN = re.compile(r"\$_GET\['([a-z0-9_]+)'\]\s*!==?\s*'([^']{4,})'")
B64 = re.compile(r"base64_decode\s*\(")
# Privilege escalation with no login check. On its own this is enough to condemn a
# file regardless of how it is shaped: it makes the request act as user 1.
ELEVATE = re.compile(r"wp_set_current_user\s*\(\s*1\s*\)")


def client():
    host = os.environ["SFTP_HOST"]
    port = int(os.environ.get("SFTP_PORT", "2222"))
    t = paramiko.Transport((host, port))
    t.connect(username=os.environ["SFTP_USER"], password=os.environ["SFTP_PASS"])
    return t, paramiko.SFTPClient.from_transport(t)


def classify(sftp):
    """Return (throwaway, kept). throwaway = [(name, size, token, has_payload)]."""
    throwaway, kept = [], []
    for a in sorted(sftp.listdir_attr(MU), key=lambda x: x.filename):
        fn = a.filename
        if stat.S_ISDIR(a.st_mode) or not fn.endswith(".php"):
            continue  # .bak-* files do not execute; they are the rollback path
        if fn in KEEP or fn.startswith(KEEP_PREFIXES):
            kept.append(fn)
            continue
        body = sftp.open(f"{MU}/{fn}", "rb").read().decode("utf-8", "replace")

        one_shot = GET.search(body) and BAIL.search(body) and len(HOOK.findall(body)) <= 2
        elevates = bool(ELEVATE.search(body))
        empty = len(body.strip()) < 10  # a 0-byte leftover from a push helper

        if one_shot or elevates or empty:
            m = TOKEN.search(body)
            guard = f"{m.group(1)}={m.group(2)}" if m else ("empty file" if empty else "-")
            if elevates:
                guard += "  ** RUNS AS ADMIN, NO LOGIN CHECK **"
            throwaway.append((fn, a.st_size, guard, bool(B64.search(body))))
        else:
            kept.append(fn)
    return throwaway, kept


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--delete", action="store_true",
                    help="back up to tmp/ then remove from staging")
    args = ap.parse_args()

    t, sftp = client()
    try:
        throwaway, kept = classify(sftp)

        print(f"{len(throwaway)} throwaway script(s) in {MU}; {len(kept)} kept\n")
        payloads = []
        for fn, size, token, has_payload in throwaway:
            flag = "  <-- HAS ENCODED PAYLOAD, archive before deleting" if has_payload else ""
            print(f"  {size:>7}  {fn}   guard: {token}{flag}")
            if has_payload:
                payloads.append(fn)

        if not throwaway:
            print("Clean. Safe to run the file-system copy.")
            return 0

        if not args.delete:
            print("\nReport only - nothing written. Re-run with --delete to remove.")
            if payloads:
                print(f"WARNING: {len(payloads)} file(s) carry an encoded payload. Decode and "
                      f"archive to docs/archive/ BEFORE deleting.")
            return 0

        # Guard: never delete allowlisted functionality.
        names = {fn for fn, _, _, _ in throwaway}
        collision = names & KEEP
        if collision:
            print(f"\nABORT: keep-list collision: {sorted(collision)}", file=sys.stderr)
            return 2

        stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = ROOT / "tmp" / f"deleted-mu-plugins-{stamp}"
        backup.mkdir(parents=True, exist_ok=True)
        for fn, _, _, _ in throwaway:
            remote = f"{MU}/{fn}"
            (backup / fn).write_bytes(sftp.open(remote, "rb").read())
            sftp.remove(remote)
        print(f"\nBacked up to {backup} and removed {len(throwaway)} file(s) from staging.")
        print("Now re-render the homepage, /contact-us/ and /uk-insolvency-statistics/ and "
              "check for fatal errors BEFORE running the copy to live.")
        return 0
    finally:
        sftp.close()
        t.close()


if __name__ == "__main__":
    raise SystemExit(main())
