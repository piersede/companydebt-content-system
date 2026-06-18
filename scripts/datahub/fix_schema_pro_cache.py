"""Fix WP Schema Pro's cached schema blob after the data-hub flatten.

WP Schema Pro stores a PRE-RENDERED schema string per post in the postmeta
`wp_schema_pro_optimized_structured_data` and prints it verbatim (it is not
regenerated on a normal content save). After the flatten, that cache still held
the OLD nested permalink in the Article node's `mainEntityOfPage.@id` on the
re-parented pages. This rewrites the cached blob in place (same segment-strip we
used everywhere else: /data/company-insolvency/ -> /data/), which fixes the @id
and survives any later Schema Pro regeneration (live regen uses get_permalink,
now flat). Idempotent. STAGING ONLY.

Mechanism: one-shot mu-plugin via SFTP, token-triggered over HTTP, self-deletes
(same pattern as wpe_purge.py / add_flatten_redirects.py).

Usage:
    python scripts/datahub/fix_schema_pro_cache.py
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
POST_IDS = "79846,79847,79848,79850"
META_KEY = "wp_schema_pro_optimized_structured_data"

PHP = r"""<?php
/** One-shot: rewrite Schema Pro cache nested->flat. Trigger ?__TRIGGER__=__TOKEN__. Self-deletes. */
if (!isset($_GET['__TRIGGER__']) || $_GET['__TRIGGER__'] !== '__TOKEN__') { return; }
add_action('init', function() {
    header('Content-Type: text/plain; charset=utf-8');
    $ids = array(__IDS__);
    $key = '__META_KEY__';
    foreach ($ids as $pid) {
        $v = get_post_meta($pid, $key, true);
        if (!$v || !is_string($v)) { echo "post={$pid} (no cache)\n"; continue; }
        $before = substr_count($v, '/data/company-insolvency/');
        if ($before === 0) { echo "post={$pid} already clean\n"; continue; }
        $new = str_replace('/data/company-insolvency/', '/data/', $v);
        update_post_meta($pid, $key, $new);
        $check = get_post_meta($pid, $key, true);
        $after = substr_count($check, '/data/company-insolvency/');
        echo "post={$pid} fixed: nested {$before} -> {$after}\n";
    }
    echo "FIX_DONE\n";
    @unlink(__FILE__);
    exit;
}, 1);
"""


def run() -> bool:
    token = uuid.uuid4().hex[:12]
    trigger = "cdfixsp"
    name = f"mu-cd-fixsp-{token}.php"
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
    return resp.status_code == 200 and "FIX_DONE" in resp.text


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(0 if run() else 1)
