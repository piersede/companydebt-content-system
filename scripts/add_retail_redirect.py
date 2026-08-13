"""Add the retail-guide -> retail data-hub page 301 to Quick Redirects (qppr).

The existing "Retail Insolvency in the UK" guide (/insolvency/retail-industry-
insolvency-trends/, WP page 20268) is being superseded by the new data-hub
page /data/retail-insolvency-statistics/ (WP page 80679, built 2026-07-22).
User confirmed: redirect the old URL to the new one.

This adds the STAGING-side rule only, for verification. The live-site
equivalent must be added by hand via wp-admin/admin.php?page=redirect-updates
on companydebt.com -- this project's .env has no production write credentials
(WP_SITE_URL / WP_APP_PASSWORD / prod SFTP are all absent), which is by
design (Claude works on staging; production pushes are the user's own).

Mechanism (same proven path as scripts/add_prepack_redirect.py):
SFTP a one-shot mu-plugin that appends to the `quickppr_redirects` +
`quickppr_redirects_meta` options, trigger it over HTTP with a token (browser
UA to clear the WAF), self-delete. This is the ONLY sanctioned redirect store
(CLAUDE.md). Appends -- never clobbers existing rules. Idempotent. STAGING ONLY.

Usage:
    python scripts/add_retail_redirect.py
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

ROOT = pathlib.Path(__file__).resolve().parents[1]
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
from _env import load_env as _load_env
_load_env()
REMOTE_DIR = "wp-content/mu-plugins"
BROWSER_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

REDIRECTS = {
    "/insolvency/retail-industry-insolvency-trends/": "/data/retail-insolvency-statistics/",
}

PHP_TEMPLATE = """<?php
/** One-shot: append retail-guide 301 to qppr. Trigger ?__TRIGGER__=__TOKEN__. Self-deletes. */
if (!isset($_GET['__TRIGGER__']) || $_GET['__TRIGGER__'] !== '__TOKEN__') { return; }
add_action('init', function() {
    header('Content-Type: text/plain; charset=utf-8');
    $new = array(
__PAIRS__
    );
    $existing = get_option('quickppr_redirects', array());
    if (!is_array($existing)) { $existing = array(); }
    $before = count($existing);
    foreach ($new as $src => $dst) { $existing[$src] = $dst; }
    update_option('quickppr_redirects', $existing);
    $meta = get_option('quickppr_redirects_meta', array());
    if (!is_array($meta)) { $meta = array(); }
    foreach ($new as $src => $dst) { $meta[$src] = array('newwindow' => '0', 'nofollow' => '0'); }
    update_option('quickppr_redirects_meta', $meta);
    $after = get_option('quickppr_redirects', array());
    echo "DONE\\nBefore: {$before}\\nAfter: " . count($after) . "\\n";
    foreach ($new as $src => $dst) {
        $got = isset($after[$src]) ? $after[$src] : 'MISSING';
        echo "  {$src} => {$got}\\n";
    }
    @unlink(__FILE__);
    exit;
}, 1);
"""


def _sftp():
    t = paramiko.Transport((os.environ["SFTP_HOST"], int(os.environ.get("SFTP_PORT", "2222"))))
    t.connect(username=os.environ["SFTP_USER"], password=os.environ["SFTP_PASS"])
    return t, paramiko.SFTPClient.from_transport(t)


def build_php(trigger: str, token: str) -> str:
    pairs = "\n".join(
        f"        '{src}' => '{dst}'," for src, dst in REDIRECTS.items()
    )
    return (PHP_TEMPLATE
            .replace("__TRIGGER__", trigger)
            .replace("__TOKEN__", token)
            .replace("__PAIRS__", pairs))


def run() -> bool:
    token = uuid.uuid4().hex[:12]
    trigger = "cdredir"
    name = f"mu-cd-redir-{token}.php"
    local = ROOT / "tmp" / name
    local.parent.mkdir(exist_ok=True)
    local.write_text(build_php(trigger, token), encoding="utf-8")
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
    print(f"http {resp.status_code}:\n{resp.text[:600]}")
    local.unlink(missing_ok=True)

    t, s = _sftp()
    try:
        try:
            s.stat(remote); s.remove(remote)
            print("warning: forced removal of leftover redirect plugin")
        except FileNotFoundError:
            print("remote cleanup confirmed (self-deleted)")
    finally:
        s.close(); t.close()
    return resp.status_code == 200 and "DONE" in resp.text


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(0 if run() else 1)
