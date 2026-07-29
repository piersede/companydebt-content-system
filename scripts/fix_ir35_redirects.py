"""Fix the two broken IR35 contractor redirects in Quick Redirects.

Found during the construction redirect audit (scripts/dump_qppr_rules.py):

  /ir35-contractor                                     -> / (the homepage)
  /hmrc-tax-investigations/hmrcs-ir35-investigations-different/
      how-do-i-close-a-company-due-to-ir35-reforms/    -> a 404

Both were aimed at /closing-a-limited-company/ir35-contractor/, which does not
exist on live or staging. The first had been given up on and dumped at the
homepage; the second still 301s straight into a 404.

Both URLs are about closing a company as a contractor, so both now go to
/closing-a-limited-company/ -- which exists, and which the surviving relative
sibling rule (/how-do-i-close-a-company-due-to-ir35-reforms/) already uses.

Rules are matched by URL PATH so absolute and relative keys move together, and
a relative key is added so each rule fires (and can be verified) on staging.

STAGING ONLY -- production needs the same edits by hand in
wp-admin/admin.php?page=redirect-updates.

Usage:
    python scripts/fix_ir35_redirects.py
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

TARGET = "/closing-a-limited-company/"

# source path -> final target (relative). Note the first key has no trailing
# slash, which is how it is stored in qppr.
REDIRECTS = {
    "/ir35-contractor": TARGET,
    "/hmrc-tax-investigations/hmrcs-ir35-investigations-different/how-do-i-close-a-company-due-to-ir35-reforms/": TARGET,
}

PHP_TEMPLATE = """<?php
/** One-shot: fix broken IR35 301s in qppr. Trigger ?__TRIGGER__=__TOKEN__. Self-deletes. */
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
