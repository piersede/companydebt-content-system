"""Read or string-replace an ACF *options* field on staging via a one-shot
mu-plugin (same drop / HTTP-trigger / self-delete pattern as wpe_purge.py).

ACF options live in wp_options, not post content and not a theme file, so they
can't be reached by the REST content layer or SFTP file edits. This does a
precise, reversible str_replace inside the stored value (no blind overwrite).

Usage:
  python scripts/wp_acf_option.py get  --field footnotes_description
  python scripts/wp_acf_option.py replace --field footnotes_description \
        --old-b64 <base64> --new-b64 <base64>   [--apply]
"""
from __future__ import annotations

import argparse
import base64
import os
import pathlib
import sys
import time
import uuid

import paramiko
import requests
from dotenv import load_dotenv

ROOT = pathlib.Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
REMOTE_DIR = "wp-content/mu-plugins"
BROWSER_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

GET_PHP = """<?php
/** One-shot ACF option read. Self-deletes. */
if (!isset($_GET['{trigger}']) || $_GET['{trigger}'] !== '{token}') {{ return; }}
add_action('init', function() {{
    $v = function_exists('get_field') ? get_field('{field}', 'option') : '(no-acf)';
    echo 'VAL:' . base64_encode((string)$v);
    @unlink(__FILE__); exit;
}}, 99);
"""

REPLACE_PHP = """<?php
/** One-shot ACF option str_replace. Self-deletes. */
if (!isset($_GET['{trigger}']) || $_GET['{trigger}'] !== '{token}') {{ return; }}
add_action('init', function() {{
    $old = base64_decode('{old_b64}');
    $new = base64_decode('{new_b64}');
    $v = (string) get_field('{field}', 'option');
    $n = substr_count($v, $old);
    if ($n === 1 && {apply}) {{
        update_field('{field}', str_replace($old, $new, $v), 'option');
        echo 'REPLACED:' . $n;
    }} else {{
        echo 'MATCHES:' . $n . ($n===1 ? ' (dry-run)' : ' (no write)');
    }}
    @unlink(__FILE__); exit;
}}, 99);
"""


def _sftp():
    t = paramiko.Transport((os.environ["SFTP_HOST"], int(os.environ.get("SFTP_PORT", "2222"))))
    t.connect(username=os.environ["SFTP_USER"], password=os.environ["SFTP_PASS"])
    return t, paramiko.SFTPClient.from_transport(t)


def _run(php: str) -> str:
    token = uuid.uuid4().hex[:12]
    trigger = "cdacf"
    name = f"mu-cd-acf-{token}.php"
    local = ROOT / "tmp" / name
    local.parent.mkdir(exist_ok=True)
    local.write_text(php.replace("{trigger}", trigger).replace("{token}", token), encoding="utf-8")
    remote = f"{REMOTE_DIR}/{name}"
    t, s = _sftp()
    try:
        s.put(str(local), remote)
    finally:
        s.close(); t.close()
    wp_url = os.environ["WP_STAGING_URL"].rstrip("/")
    auth = (os.environ["WP_BASIC_AUTH_USER"], os.environ["WP_BASIC_AUTH_PASS"])
    time.sleep(1)
    resp = requests.get(f"{wp_url}/?{trigger}={token}", auth=auth,
                        headers={"User-Agent": BROWSER_UA}, timeout=120)
    local.unlink(missing_ok=True)
    # best-effort cleanup
    t, s = _sftp()
    try:
        try:
            s.stat(remote); s.remove(remote)
        except FileNotFoundError:
            pass
    finally:
        s.close(); t.close()
    return resp.text


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("get"); g.add_argument("--field", required=True)
    r = sub.add_parser("replace"); r.add_argument("--field", required=True)
    r.add_argument("--old-b64", required=True); r.add_argument("--new-b64", required=True)
    r.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    if a.cmd == "get":
        out = _run(GET_PHP.replace("{field}", a.field))
        if "VAL:" in out:
            val = base64.b64decode(out.split("VAL:", 1)[1].strip()).decode("utf-8", "replace")
            print(val)
        else:
            print("UNEXPECTED:", out[:300])
    elif a.cmd == "replace":
        php = (REPLACE_PHP.replace("{field}", a.field)
               .replace("{old_b64}", a.old_b64).replace("{new_b64}", a.new_b64)
               .replace("{apply}", "true" if a.apply else "false"))
        print(_run(php)[:300])


if __name__ == "__main__":
    main()
