"""Append the data-hub flatten 301s to the Quick Redirects (qppr) plugin.

Redirects the retired nested URLs to their new flat homes:

  /data/company-insolvency/                          -> /data/
  /data/company-insolvency/winding-up-petition-tracker/   -> /data/winding-up-petition-tracker/
  /data/company-insolvency/dissolutions-vs-insolvencies/  -> /data/dissolutions-vs-insolvencies/
  /data/company-insolvency/payment-practices-late-payment/-> /data/payment-practices-late-payment/

Mechanism (same proven path as wpe_purge.py): SFTP a one-shot mu-plugin that
appends to the `quickppr_redirects` + `quickppr_redirects_meta` options, trigger
it over HTTP with a token (browser UA to clear the WAF), self-delete. This is the
ONLY sanctioned redirect store (CLAUDE.md). Appends — never clobbers existing
rules. Idempotent. STAGING ONLY.

Usage:
    python scripts/datahub/add_flatten_redirects.py
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

REDIRECTS = {
    "/data/company-insolvency/": "/data/",
    "/data/company-insolvency/winding-up-petition-tracker/": "/data/winding-up-petition-tracker/",
    "/data/company-insolvency/dissolutions-vs-insolvencies/": "/data/dissolutions-vs-insolvencies/",
    "/data/company-insolvency/payment-practices-late-payment/": "/data/payment-practices-late-payment/",
}

PHP_TEMPLATE = """<?php
/** One-shot: append data-hub flatten 301s to qppr. Trigger ?__TRIGGER__=__TOKEN__. Self-deletes. */
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
