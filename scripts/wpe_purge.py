"""Purge WP page caches on staging (WP Rocket + WP Engine Varnish/memcached).

Uploads a one-shot mu-plugin via SFTP, triggers it over HTTP (browser UA to
clear the WAF), and self-deletes. Mirrors the proven pattern in wp_push.py.

Usage:
    python scripts/wpe_purge.py
"""
from __future__ import annotations

import os
import pathlib
import re
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

PHP = """<?php
/** One-shot cache purge. Trigger: ?{trigger}={token}. Self-deletes. */
if (!isset($_GET['{trigger}']) || $_GET['{trigger}'] !== '{token}') {{ return; }}
add_action('init', function() {{
    $done = [];
    if (function_exists('rocket_clean_domain')) {{ rocket_clean_domain(); $done[] = 'rocket_clean_domain'; }}
    if (function_exists('rocket_clean_minify')) {{ rocket_clean_minify(); $done[] = 'rocket_clean_minify'; }}
    if (function_exists('wp_cache_flush')) {{ wp_cache_flush(); $done[] = 'wp_cache_flush'; }}
    if (class_exists('WpeCommon')) {{
        if (method_exists('WpeCommon','purge_memcached')) {{ WpeCommon::purge_memcached(); $done[] = 'wpe_memcached'; }}
        if (method_exists('WpeCommon','purge_varnish_cache')) {{ WpeCommon::purge_varnish_cache(); $done[] = 'wpe_varnish'; }}
    }}
    if (function_exists('opcache_reset')) {{ opcache_reset(); $done[] = 'opcache_reset'; }}
    echo 'OK: purged ' . implode(',', $done);
    @unlink(__FILE__);
    exit;
}}, 1);
"""


def _sftp():
    t = paramiko.Transport((os.environ["SFTP_HOST"], int(os.environ.get("SFTP_PORT", "2222"))))
    t.connect(username=os.environ["SFTP_USER"], password=os.environ["SFTP_PASS"])
    return t, paramiko.SFTPClient.from_transport(t)


def purge() -> bool:
    token = uuid.uuid4().hex[:12]
    trigger = "cdpurge"
    name = f"mu-cd-purge-{token}.php"
    local = ROOT / "tmp" / name
    local.parent.mkdir(exist_ok=True)
    local.write_text(PHP.format(trigger=trigger, token=token), encoding="utf-8")
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
    print(f"http {resp.status_code}: {resp.text[:200]}")
    local.unlink(missing_ok=True)

    # best-effort self-delete confirmation
    t, s = _sftp()
    try:
        try:
            s.stat(remote); s.remove(remote)
            print("warning: forced removal of leftover purge plugin")
        except FileNotFoundError:
            print("remote cleanup confirmed")
    finally:
        s.close(); t.close()
    return resp.status_code == 200 and resp.text.startswith("OK:")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(0 if purge() else 1)
