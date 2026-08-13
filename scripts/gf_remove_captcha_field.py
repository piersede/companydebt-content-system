"""One-shot: remove field 16 (hidden reCAPTCHA v2) from Gravity Forms form 38 on staging.

Same pattern as scripts/wpe_purge.py — SFTP a mu-plugin, trigger it via HTTP,
self-delete. This removes the CAPTCHA field entirely from form 38's config so
Gravity Forms' client-side submit no longer blocks on grecaptcha.getResponse().

Field 16 was the same v2 checkbox that got hidden by theme CSS
`#gform_38 #field_38_16{display:none!important}`. Friday's session
removed it but it has returned on staging (2026-08-05).
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

# NOTE: the trigger token is a placeholder — real value injected at runtime.
PHP = r"""<?php
/** One-shot: remove captcha field 16 from GF form 38. Trigger: ?{trigger}={token}. Self-deletes. */
if (!isset($_GET['{trigger}']) || $_GET['{trigger}'] !== '{token}') {{ return; }}
add_action('init', function() {{
    if (!class_exists('GFAPI')) {{ echo 'ERR: GFAPI missing'; @unlink(__FILE__); exit; }}
    $form = GFAPI::get_form(38);
    if (!$form || is_wp_error($form)) {{ echo 'ERR: form 38 not found'; @unlink(__FILE__); exit; }}
    $before = [];
    foreach ($form['fields'] as $f) {{
        $before[] = $f->id . ':' . $f->type . '(' . (isset($f->label) ? $f->label : '-') . ')';
    }}
    $removed = 0;
    $new_fields = [];
    foreach ($form['fields'] as $f) {{
        if ((int)$f->id === 16 || (isset($f->type) && $f->type === 'captcha')) {{
            $removed++;
            continue;
        }}
        $new_fields[] = $f;
    }}
    $form['fields'] = $new_fields;
    $res = GFAPI::update_form($form);
    if (is_wp_error($res)) {{
        echo 'ERR: update failed: ' . $res->get_error_message();
    }} else {{
        echo 'OK: removed=' . $removed . ' | before=[' . implode('|', $before) . ']';
    }}
    @unlink(__FILE__);
    exit;
}}, 1);
"""


def _sftp():
    t = paramiko.Transport((os.environ["SFTP_HOST"], int(os.environ.get("SFTP_PORT", "2222"))))
    t.connect(username=os.environ["SFTP_USER"], password=os.environ["SFTP_PASS"])
    return t, paramiko.SFTPClient.from_transport(t)


def run() -> bool:
    token = uuid.uuid4().hex[:12]
    trigger = "cdgfstrip"
    name = f"mu-cd-gf-strip-captcha-{token}.php"
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
                        headers={"User-Agent": BROWSER_UA}, timeout=60)
    print(f"http {resp.status_code}: {resp.text[:600]}")
    local.unlink(missing_ok=True)

    # best-effort cleanup
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
    raise SystemExit(0 if run() else 1)
