"""Flatten the remaining construction-guide redirect chains in Quick Redirects.

Audit of the full qppr map (scripts/dump_qppr_rules.py) found the retired
construction guide sat at the end of a 3-hop chain that dead-ended on the
generic /insolvency/ hub:

    /construction-industry-insolvency-trends/
      -> /news/common-causes-of-construction-insolvency/
        -> /articles/common-causes-of-construction-insolvency/
          -> /insolvency/

The tail was repointed at /data/construction-insolvency-statistics/ by
scripts/add_construction_redirect.py. This flattens the two upstream hops onto
the same target so every legacy construction URL is a single 301, and flattens
the 2-hop energy-costs rule onto its already-correct final destination.

Rules are matched by URL PATH, so both the absolute-URL keys (which fire on
production) and any relative key are rewritten together. Targets are written
relative so they work on staging and production alike.

STAGING ONLY -- production needs the same edits by hand in
wp-admin/admin.php?page=redirect-updates.

Usage:
    python scripts/flatten_construction_redirects.py
"""
from __future__ import annotations

import json
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

# source path -> final target (relative)
REDIRECTS = {
    "/construction-industry-insolvency-trends/": "/data/construction-insolvency-statistics/",
    "/news/common-causes-of-construction-insolvency/": "/data/construction-insolvency-statistics/",
    "/articles/energy-costs-will-increase-construction-insolvencies/": "/company-cash-flow-problems/cant-pay-business-energy/",
}

PHP_TEMPLATE = """<?php
/** One-shot: flatten construction 301 chains in qppr. Trigger ?__TRIGGER__=__TOKEN__. Self-deletes. */
if (!isset($_GET['__TRIGGER__']) || $_GET['__TRIGGER__'] !== '__TOKEN__') { return; }
add_action('init', function() {
    header('Content-Type: text/plain; charset=utf-8');
    $map = json_decode('__MAP__', true);
    $existing = get_option('quickppr_redirects', array());
    if (!is_array($existing)) { $existing = array(); }
    $before = count($existing);
    foreach ($map as $src => $dst) {
        foreach ($existing as $k => $v) {
            if (parse_url($k, PHP_URL_PATH) === $src) {
                echo "  was: {$k} => {$v}\\n";
                $existing[$k] = $dst;
            }
        }
        // Absolute-URL keys only fire on production; add the relative key so the
        // rule also works on staging and can actually be verified there.
        $existing[$src] = $dst;
    }
    update_option('quickppr_redirects', $existing);
    $meta = get_option('quickppr_redirects_meta', array());
    if (!is_array($meta)) { $meta = array(); }
    foreach ($map as $src => $dst) {
        if (!isset($meta[$src])) { $meta[$src] = array('newwindow' => '0', 'nofollow' => '0'); }
    }
    update_option('quickppr_redirects_meta', $meta);
    $after = get_option('quickppr_redirects', array());
    echo "DONE\\nBefore: {$before}\\nAfter: " . count($after) . "\\n";
    foreach ($map as $src => $dst) {
        foreach ($after as $k => $v) {
            if (parse_url($k, PHP_URL_PATH) === $src) { echo "  now: {$k} => {$v}\\n"; }
        }
    }
    @unlink(__FILE__);
    exit;
}, 1);
"""


def _sftp():
    t = paramiko.Transport((os.environ["SFTP_HOST"], int(os.environ.get("SFTP_PORT", "2222"))))
    t.connect(username=os.environ["SFTP_USER"], password=os.environ["SFTP_PASS"])
    return t, paramiko.SFTPClient.from_transport(t)


def run() -> bool:
    token = uuid.uuid4().hex[:12]
    trigger = "cdredir"
    name = f"mu-cd-redir-{token}.php"
    php = (PHP_TEMPLATE
           .replace("__TRIGGER__", trigger)
           .replace("__TOKEN__", token)
           .replace("__MAP__", json.dumps(REDIRECTS).replace("'", "\\'")))
    local = ROOT / "tmp" / name
    local.parent.mkdir(exist_ok=True)
    local.write_text(php, encoding="utf-8")
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
    print(f"http {resp.status_code}:\n{resp.text[:1500]}")
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
