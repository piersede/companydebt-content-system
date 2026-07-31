"""Repoint the construction-causes guide 301 at the construction data page.

/articles/common-causes-of-construction-insolvency/ currently 301s to the
generic /insolvency/ hub. It carries at least one real external backlink
(hbkcpa.com anchors "bankruptcy is at its highest in almost ten years" at it),
so the far better target is the topical data page:
/data/construction-insolvency-statistics/ (WP page 79856, live + staging).

STAGING ONLY. The live-site equivalent must be added by hand via
wp-admin/admin.php?page=redirect-updates on companydebt.com -- this project's
.env has no production SFTP, by design.

Mechanism (same proven path as scripts/add_retail_redirect.py): SFTP a one-shot
mu-plugin that rewrites the `quickppr_redirects` + `quickppr_redirects_meta`
options, trigger it over HTTP with a token (browser UA to clear the WAF),
self-delete. Quick Redirects is the ONLY sanctioned redirect store (CLAUDE.md).

Unlike the retail script this also rewrites any ABSOLUTE-URL key whose path
matches the source, so an old absolute rule can't keep winning on production.

Usage:
    python scripts/add_construction_redirect.py
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
load_dotenv(ROOT / ".env")
REMOTE_DIR = "wp-content/mu-plugins"
BROWSER_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

SOURCE_PATH = "/articles/common-causes-of-construction-insolvency/"
TARGET = "/data/construction-insolvency-statistics/"

PHP_TEMPLATE = """<?php
/** One-shot: repoint construction-causes 301 in qppr. Trigger ?__TRIGGER__=__TOKEN__. Self-deletes. */
if (!isset($_GET['__TRIGGER__']) || $_GET['__TRIGGER__'] !== '__TOKEN__') { return; }
add_action('init', function() {
    header('Content-Type: text/plain; charset=utf-8');
    $src = '__SOURCE__';
    $dst = '__TARGET__';
    $existing = get_option('quickppr_redirects', array());
    if (!is_array($existing)) { $existing = array(); }
    $before = count($existing);
    echo "Matching existing keys:\\n";
    foreach ($existing as $k => $v) {
        $path = parse_url($k, PHP_URL_PATH);
        if ($path === $src) {
            echo "  was: {$k} => {$v}\\n";
            $existing[$k] = $dst;
        }
    }
    $existing[$src] = $dst;
    update_option('quickppr_redirects', $existing);
    $meta = get_option('quickppr_redirects_meta', array());
    if (!is_array($meta)) { $meta = array(); }
    if (!isset($meta[$src])) { $meta[$src] = array('newwindow' => '0', 'nofollow' => '0'); }
    update_option('quickppr_redirects_meta', $meta);
    $after = get_option('quickppr_redirects', array());
    echo "DONE\\nBefore: {$before}\\nAfter: " . count($after) . "\\n";
    foreach ($after as $k => $v) {
        if (parse_url($k, PHP_URL_PATH) === $src) { echo "  now: {$k} => {$v}\\n"; }
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
    return (PHP_TEMPLATE
            .replace("__TRIGGER__", trigger)
            .replace("__TOKEN__", token)
            .replace("__SOURCE__", SOURCE_PATH)
            .replace("__TARGET__", TARGET))


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
    print(f"http {resp.status_code}:\n{resp.text[:1200]}")
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
