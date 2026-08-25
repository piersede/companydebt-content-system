"""Find server source files that the public web server will hand over as text.

WHY THIS EXISTS
---------------
WordPress only EXECUTES files ending in ``.php``. A file named
``cd-livechat-secrets.php.bak-a11y-cdlc6`` does not end in ``.php``, so it is
never executed - the web server treats it as a static file and returns the raw
PHP source to anyone who requests the URL. No login, no password.

On 25 Aug 2026 that meant 345 files (45 MB of theme and mu-plugin source) were
publicly readable under ``wp-content`` on companydebt.com. Four of them held the
then-current Zoho CRM client secret and refresh token, and a LiveChat secret.
They had been reachable since at least June. Our own SFTP edit helper created
them, one per edit, and past file-system copies carried them from staging to
live.

``audit_mu_plugins.py`` did not catch it, and could not: it asks "does this file
EXECUTE and do damage", and deliberately skips ``.bak-*`` because those do not
execute. The risk was never execution. It was readability.

Two fixes went in together, and this script guards the pair:

1. ``sftp_edit.py`` now writes backups to ``_wpeprivate/file-backups/``. That is
   the one directory WP Engine answers with 403 on both staging and live.
2. This scanner fails if anything backup-shaped reappears inside the web root,
   or if a known backup path is still publicly readable on the target site.

An ``.htaccess`` deny rule was tried first and does nothing. WP Engine's nginx
serves static files without consulting Apache. The fix has to be placement.

USAGE
    python scripts/audit_exposed_files.py                 # staging, full walk
    python scripts/audit_exposed_files.py --target live   # live, HTTP probe only

Exit codes: 0 clean, 1 exposed files found.
"""
from __future__ import annotations

import argparse
import base64
import os
import pathlib
import posixpath
import random
import re
import stat
import sys
import urllib.error
import urllib.request

import paramiko

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _env import load_env as _load_env  # noqa: E402

_load_env()

# Our backups have a distinctive shape: a REAL code extension, then a second
# suffix. "cd-livechat-secrets.php.bak-a11y-cdlc6". Anchoring on the code
# extension is what separates them from library files that legitimately ship
# names like "es.array.copy-within.js" or "phpunit.xml.dist" - matching those
# turned the first version of this scan into noise nobody would read twice.
BACKUP_SHAPED = re.compile(
    r"\.(?:php|js|css|html?|inc|json|xml)\.(?:bak|off|old|orig|save|copy|tmp|swp|disabled)",
    re.I,
)

# Third-party trees. We do not create backups here and cannot clean them anyway.
SKIP_DIRS = ("node_modules", "vendor", "/dist/", "bower_components")

# Directories the web server exposes. _wpeprivate is deliberately absent: it is
# the safe destination, and walking it would report every backup as a finding.
WEB_ROOTS = ["wp-content/mu-plugins", "wp-content/themes", "wp-content/plugins",
             "wp-content/uploads"]

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124 Safari/537.36"


def _sftp():
    t = paramiko.Transport((os.environ["SFTP_HOST"], int(os.environ.get("SFTP_PORT", "2222"))))
    t.connect(username=os.environ["SFTP_USER"], password=os.environ["SFTP_PASS"])
    return t, paramiko.SFTPClient.from_transport(t)


def walk_web_root(s, root: str, depth: int = 0, out=None):
    """Every backup-shaped file the web server can reach, under one root."""
    out = [] if out is None else out
    if depth > 4:
        return out
    try:
        entries = s.listdir_attr(root)
    except IOError:
        return out
    for a in entries:
        path = posixpath.join(root, a.filename)
        if stat.S_ISDIR(a.st_mode):
            if a.filename in SKIP_DIRS:
                continue
            walk_web_root(s, path, depth + 1, out)
        elif BACKUP_SHAPED.search(a.filename):
            out.append((path, a.st_size))
    return out


def fetch(base: str, path: str, auth: str | None):
    req = urllib.request.Request(f"{base.rstrip('/')}/{path.lstrip('/')}?cb={random.randrange(10**6)}")
    req.add_header("User-Agent", UA)
    if auth:
        req.add_header("Authorization", "Basic " + base64.b64encode(auth.encode()).decode())
    try:
        return urllib.request.urlopen(req, timeout=45).read()
    except urllib.error.HTTPError:
        return None
    except Exception:
        return None


def readable_as_source(body: bytes | None) -> bool:
    """True when the server handed back raw source instead of blocking it."""
    return bool(body) and body.lstrip()[:5].lower() == b"<?php"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", choices=["staging", "live"], default="staging")
    args = ap.parse_args()

    if args.target == "live":
        base, auth = os.environ.get("CD_LIVE_URL", "https://www.companydebt.com"), None
    else:
        base = os.environ["WP_STAGING_URL"]
        auth = f"{os.environ['WP_BASIC_AUTH_USER']}:{os.environ['WP_BASIC_AUTH_PASS']}"

    findings: list[str] = []

    # Layer 1 - the authoritative one, staging only: is anything backup-shaped
    # sitting inside a directory the web server serves?
    if args.target == "staging":
        t, s = _sftp()
        try:
            found = []
            for root in WEB_ROOTS:
                walk_web_root(s, root, out=found)
        finally:
            s.close()
            t.close()
        if found:
            total = sum(sz for _, sz in found)
            print(f"{len(found)} backup-shaped file(s) inside the web root "
                  f"({total / 1024 / 1024:.1f} MB):\n")
            for p, sz in sorted(found, key=lambda x: -x[1])[:25]:
                print(f"  {sz:>9}b  {p}")
            if len(found) > 25:
                print(f"  ... and {len(found) - 25} more")
            findings.append("files inside the web root")
        else:
            print("No backup-shaped files inside the web root.")

    # Layer 2 - both targets: does the site actually hand any of them over?
    # A path list is not needed for a clean install; these are the shapes that
    # leaked in Aug 2026, kept as a regression probe.
    probes = [
        "wp-content/mu-plugins/cd-livechat-secrets.php.bak-a11y-cdlc6",
        "wp-content/mu-plugins/cd-gform-hardening.php.off-hold-20260729",
        "wp-content/themes/company-debt-webpigment/header.php.bak-a11y-consent-default-20260729",
    ]
    served = [p for p in probes if readable_as_source(fetch(base, p, auth))]
    if served:
        print(f"\n{len(served)} known backup path(s) STILL PUBLICLY READABLE on {args.target}:")
        for p in served:
            print(f"  {base.rstrip('/')}/{p}")
        findings.append(f"paths readable on {args.target}")
    else:
        print(f"None of the known backup paths are readable on {args.target}.")

    # The private directory must stay private, or the fix is not a fix.
    if readable_as_source(fetch(base, "_wpeprivate/file-backups/wp-content/mu-plugins/"
                                      "cd-livechat-secrets.php.bak-a11y-cdlc6", auth)):
        print(f"\n_wpeprivate is being SERVED on {args.target}. The backup location is not safe.")
        findings.append("_wpeprivate served")

    if findings:
        print(f"\nFAIL: {'; '.join(findings)}.")
        print("Move them with the recipe in docs/exposed-source-files.md. Do NOT run a "
              "file-system copy to live until this reads clean.")
        return 1
    print("\nPASS: no server source is publicly readable.")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
