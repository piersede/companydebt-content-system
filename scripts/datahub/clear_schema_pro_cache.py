"""Clear WP Schema Pro's cached schema blob for the data-hub pages.

WP Schema Pro stores a PRE-RENDERED schema string per post in the postmeta
`wp_schema_pro_optimized_structured_data` and, when present, prints it verbatim
and RETURNS before its own `wp_schema_pro_schema_enabled` filter runs (see
class-bsf-aiosrs-pro-markup.php::schema_markup). The mu-plugin
cd-insolvency-data-hub.php now disables Schema Pro on these pages via that
filter, but the filter is bypassed while a cached blob exists. This deletes the
cache for the five data-hub posts so the next render regenerates it empty (the
filter then suppresses the Article/WebPage). Idempotent. STAGING ONLY.

Mechanism: one-shot mu-plugin via SFTP, token-triggered over HTTP, self-deletes
(same pattern as fix_schema_pro_cache.py / wpe_purge.py).

Usage:
    python scripts/datahub/clear_schema_pro_cache.py
"""
from __future__ import annotations

import os
import pathlib
import sys
import time
import uuid

import paramiko
import requests
from dotenv import load_dotenv

ROOT = pathlib.Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")
REMOTE_DIR = "wp-content/mu-plugins"
BROWSER_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
# Hub (data), flagship, tracker, dissolutions, payment.
POST_IDS = "79845,77399,79847,79848,79850"
META_KEY = "wp_schema_pro_optimized_structured_data"

PHP = r"""<?php
/** One-shot: delete Schema Pro cache for data-hub posts. Trigger ?__TRIGGER__=__TOKEN__. Self-deletes. */
if (!isset($_GET['__TRIGGER__']) || $_GET['__TRIGGER__'] !== '__TOKEN__') { return; }
add_action('init', function() {
    header('Content-Type: text/plain; charset=utf-8');
    $ids = array(__IDS__);
    $key = '__META_KEY__';
    foreach ($ids as $pid) {
        $had = get_post_meta($pid, $key, true) ? 'had-cache' : 'empty';
        delete_post_meta($pid, $key);
        echo "post={$pid} {$had} -> deleted\n";
    }
    echo "CLEAR_DONE\n";
    @unlink(__FILE__);
    exit;
}, 1);
"""


def run() -> bool:
    token = uuid.uuid4().hex[:12]
    trigger = "cdclrsp"
    name = f"mu-cd-clrsp-{token}.php"
    local = ROOT / "tmp" / name
    local.parent.mkdir(exist_ok=True)
    local.write_text(
        PHP.replace("__TRIGGER__", trigger)
           .replace("__TOKEN__", token)
           .replace("__IDS__", POST_IDS)
           .replace("__META_KEY__", META_KEY),
        encoding="utf-8",
    )
    remote = f"{REMOTE_DIR}/{name}"

    t = paramiko.Transport((os.environ["SFTP_HOST"], int(os.environ.get("SFTP_PORT", "2222"))))
    t.connect(username=os.environ["SFTP_USER"], password=os.environ["SFTP_PASS"])
    s = paramiko.SFTPClient.from_transport(t)
    try:
        s.put(str(local), remote)
    finally:
        s.close(); t.close()

    wp_url = os.environ["WP_STAGING_URL"].rstrip("/")
    auth = (os.environ["WP_BASIC_AUTH_USER"], os.environ["WP_BASIC_AUTH_PASS"])
    time.sleep(1)
    resp = requests.get(f"{wp_url}/?{trigger}={token}", auth=auth,
                        headers={"User-Agent": BROWSER_UA}, timeout=120)
    print(f"http {resp.status_code}:\n{resp.text[:1000]}")
    local.unlink(missing_ok=True)

    t = paramiko.Transport((os.environ["SFTP_HOST"], int(os.environ.get("SFTP_PORT", "2222"))))
    t.connect(username=os.environ["SFTP_USER"], password=os.environ["SFTP_PASS"])
    s = paramiko.SFTPClient.from_transport(t)
    try:
        try:
            s.stat(remote); s.remove(remote); print("(forced cleanup)")
        except FileNotFoundError:
            print("(self-deleted)")
    finally:
        s.close(); t.close()
    return resp.status_code == 200 and "CLEAR_DONE" in resp.text


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(0 if run() else 1)
