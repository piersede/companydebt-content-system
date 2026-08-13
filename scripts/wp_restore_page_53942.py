"""One-shot: restore page 53942 (/insolvency-calculator/) to the new
insolvency-test template + minimal content. Reverses the Friday redirect stopgap.

Sets:
  - page_template = 'templates/insolvency-test.php'
  - post_content  = a small placeholder (the template drives the whole page)
  - post_status   = 'publish' (already publish, but re-asserted)
  - post_title    = original title if we can extract it, else current title

Safe to re-run. Runs on staging by default; pass --target=live to run on live.
"""
from __future__ import annotations

import argparse
import os
import pathlib
import sys
import time
import uuid

import paramiko
import requests
from dotenv import load_dotenv

ROOT = pathlib.Path(__file__).resolve().parents[1]
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
from _env import load_env as _load_env
_load_env()
REMOTE_DIR = "wp-content/mu-plugins"
BROWSER_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Minimal placeholder content — the template renders the whole page from PHP.
PLACEHOLDER = "<!-- Insolvency Test — content rendered by templates/insolvency-test.php -->"

PHP = r"""<?php
/** One-shot: restore page {page_id} to the insolvency-test template. Trigger: ?{trigger}={token}. Self-deletes. */
if (!isset($_GET['{trigger}']) || $_GET['{trigger}'] !== '{token}') {{ return; }}
add_action('init', function() {{
    $page_id = {page_id};
    $tpl     = 'templates/insolvency-test.php';
    $content = '{placeholder}';

    $before = get_post_meta($page_id, '_wp_page_template', true);
    $post = get_post($page_id);
    if (!$post) {{
        echo 'ERR: page ' . $page_id . ' not found';
        @unlink(__FILE__);
        exit;
    }}

    update_post_meta($page_id, '_wp_page_template', $tpl);
    $res = wp_update_post(array(
        'ID'           => $page_id,
        'post_content' => $content,
        'post_status'  => 'publish',
    ), true);
    if (is_wp_error($res)) {{
        echo 'ERR: update failed: ' . $res->get_error_message();
        @unlink(__FILE__);
        exit;
    }}
    // Yoast: bump indexable so canonical/meta re-generate.
    if (function_exists('yoast_ping_indexable')) {{
        yoast_ping_indexable($page_id);
    }}
    // Clear common caches to make the change visible immediately.
    clean_post_cache($page_id);
    if (function_exists('rocket_clean_post')) {{ rocket_clean_post($page_id); }}
    if (function_exists('rocket_clean_domain')) {{ rocket_clean_domain(); }}
    if (class_exists('WpeCommon')) {{
        if (method_exists('WpeCommon','purge_memcached')) WpeCommon::purge_memcached();
        if (method_exists('WpeCommon','purge_varnish_cache')) WpeCommon::purge_varnish_cache();
    }}

    echo 'OK: page ' . $page_id . ' | tpl before=' . ($before ?: 'default') . ' | tpl now=' . get_post_meta($page_id, '_wp_page_template', true);
    @unlink(__FILE__);
    exit;
}}, 1);
"""


def _sftp():
    t = paramiko.Transport((os.environ["SFTP_HOST"], int(os.environ.get("SFTP_PORT", "2222"))))
    t.connect(username=os.environ["SFTP_USER"], password=os.environ["SFTP_PASS"])
    return t, paramiko.SFTPClient.from_transport(t)


def run(page_id: int) -> bool:
    token = uuid.uuid4().hex[:12]
    trigger = "cdrestore"
    name = f"mu-cd-restore-page-{page_id}-{token}.php"

    body = PHP.format(page_id=page_id, trigger=trigger, token=token, placeholder=PLACEHOLDER)
    local = ROOT / "tmp" / name
    local.parent.mkdir(exist_ok=True)
    local.write_text(body, encoding="utf-8")
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
                        headers={"User-Agent": BROWSER_UA}, timeout=60)
    print(f"http {resp.status_code}: {resp.text[:400]}")
    local.unlink(missing_ok=True)

    t, s = _sftp()
    try:
        try:
            s.stat(remote); s.remove(remote)
            print("warning: forced removal of leftover mu-plugin")
        except FileNotFoundError:
            print("remote cleanup confirmed")
    finally:
        s.close(); t.close()
    return resp.status_code == 200 and resp.text.startswith("OK:")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser()
    p.add_argument('--page-id', type=int, default=53942)
    args = p.parse_args()
    raise SystemExit(0 if run(args.page_id) else 1)
