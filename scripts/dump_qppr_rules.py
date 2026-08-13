"""Dump every Quick Redirects (qppr) rule from staging to a local TSV.

Read-only. Quick Redirects is the only sanctioned redirect store on this site
(CLAUDE.md), so this option IS the redirect map. Having it locally makes it
possible to audit targets in bulk -- e.g. "which retired pages 301 to a generic
hub instead of the page that actually answers the query".

Same transport as the other qppr scripts: SFTP a one-shot, self-deleting
mu-plugin, trigger it over HTTP with a token (browser UA to clear the WAF),
read the payload between sentinels.

Usage:
    python scripts/dump_qppr_rules.py --out tmp/qppr-rules.tsv
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
START = "<<<CDQPPR_START>>>"
END = "<<<CDQPPR_END>>>"

PHP_TEMPLATE = """<?php
/** One-shot qppr rule dumper. Trigger ?__TRIGGER__=__TOKEN__. Self-deletes. */
if (!isset($_GET['__TRIGGER__']) || $_GET['__TRIGGER__'] !== '__TOKEN__') { return; }
add_action('init', function() {
    header('Content-Type: text/plain; charset=utf-8');
    $rules = get_option('quickppr_redirects', array());
    if (!is_array($rules)) { $rules = array(); }
    echo "__START__\\n";
    foreach ($rules as $src => $dst) {
        if (is_array($dst)) { $dst = isset($dst['url']) ? $dst['url'] : json_encode($dst); }
        echo $src . "\\t" . $dst . "\\n";
    }
    echo "__END__\\n";
    @unlink(__FILE__);
    exit;
}, 1);
"""


def _sftp():
    t = paramiko.Transport((os.environ["SFTP_HOST"], int(os.environ.get("SFTP_PORT", "2222"))))
    t.connect(username=os.environ["SFTP_USER"], password=os.environ["SFTP_PASS"])
    return t, paramiko.SFTPClient.from_transport(t)


def run(out: pathlib.Path) -> bool:
    token = uuid.uuid4().hex[:12]
    trigger = "cdqppr"
    name = f"mu-cd-qppr-{token}.php"
    php = (PHP_TEMPLATE
           .replace("__TRIGGER__", trigger)
           .replace("__TOKEN__", token)
           .replace("__START__", START)
           .replace("__END__", END))
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
                        headers={"User-Agent": BROWSER_UA}, timeout=180)
    local.unlink(missing_ok=True)

    t, s = _sftp()
    try:
        try:
            s.stat(remote); s.remove(remote)
            print("warning: forced removal of leftover dump plugin")
        except FileNotFoundError:
            print("remote cleanup confirmed (self-deleted)")
    finally:
        s.close(); t.close()

    if START not in resp.text or END not in resp.text:
        print(f"http {resp.status_code}: sentinels missing\n{resp.text[:500]}")
        return False
    body = resp.text.split(START, 1)[1].split(END, 1)[0].strip("\n")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body + "\n", encoding="utf-8")
    print(f"wrote {len(body.splitlines())} rules -> {out}")
    return True


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="tmp/qppr-rules.tsv")
    a = ap.parse_args()
    raise SystemExit(0 if run(ROOT / a.out) else 1)
