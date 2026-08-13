"""One-shot: create the "Insolvency Test" Gravity Form + store its ID.

Runs via a temporary mu-plugin (same pattern as scripts/wpe_purge.py) so that
GFAPI is available. Idempotent — if a form with the same title already exists,
it re-uses that form's ID rather than creating a duplicate.

Also sets wp_options['cd_insolvency_test_form_id'] to the resulting form ID,
which the templates/insolvency-test.php template reads to know which form to
POST the capture step to.

Field IDs are pinned so the template's `input_1` … `input_9` references stay
stable across staging and live. Do not renumber without updating the template.
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

# PHP one-shot: idempotent form creation + option write. Runs on ?trigger=token.
PHP = r"""<?php
/** One-shot: create/find Insolvency Test GF form and store its ID. Trigger: ?{trigger}={token}. Self-deletes. */
if (!isset($_GET['{trigger}']) || $_GET['{trigger}'] !== '{token}') {{ return; }}
add_action('init', function() {{
    if (!class_exists('GFAPI')) {{ echo 'ERR: GFAPI missing'; @unlink(__FILE__); exit; }}

    $title = 'Insolvency Test';

    // Idempotent lookup: reuse an existing form with the same title if present.
    $existing_id = 0;
    $all = GFAPI::get_forms();
    foreach ($all as $f) {{
        if (isset($f['title']) && $f['title'] === $title) {{ $existing_id = (int) $f['id']; break; }}
    }}

    if ($existing_id) {{
        update_option('cd_insolvency_test_form_id', $existing_id);
        echo 'OK: existing form_id=' . $existing_id;
        @unlink(__FILE__);
        exit;
    }}

    // Fresh form spec. Field IDs are pinned to match templates/insolvency-test.php.
    $form = array(
        'title'        => $title,
        'description'  => 'Capture step for the multi-step insolvency test at /insolvency-calculator/. Do not add fields here without updating the template.',
        'labelPlacement' => 'top_label',
        'button'       => array('type' => 'text', 'text' => 'Submit'),
        'fields' => array(
            array('id' => 1, 'type' => 'text',     'label' => 'First name',       'isRequired' => true),
            array('id' => 2, 'type' => 'email',    'label' => 'Email',            'isRequired' => true),
            array('id' => 3, 'type' => 'radio',    'label' => 'Wants call',       'isRequired' => true,
                  'choices' => array(
                      array('text' => 'Yes', 'value' => 'yes'),
                      array('text' => 'No',  'value' => 'no'),
                  )),
            array('id' => 4, 'type' => 'phone',    'label' => 'Phone',            'isRequired' => false),
            array('id' => 5, 'type' => 'text',     'label' => 'Preferred time',   'isRequired' => false),
            array('id' => 6, 'type' => 'text',     'label' => 'Risk tier',        'isRequired' => false),
            array('id' => 7, 'type' => 'textarea', 'label' => 'Quiz payload',     'isRequired' => false,
                  'description' => 'JSON payload: answers, score, duration_ms.'),
            array('id' => 8, 'type' => 'text',     'label' => 'Landing page',     'isRequired' => false),
            array('id' => 9, 'type' => 'text',     'label' => 'Referring page',   'isRequired' => false),
        ),
        'confirmations' => array(
            'default' => array(
                'id'          => 'default',
                'name'        => 'Default confirmation',
                'isDefault'   => true,
                'type'        => 'message',
                'message'     => 'Received.',
                'disableAutoformat' => true,
            ),
        ),
        'notifications' => array(),
        'useCurrentUserAsAuthor' => false,
        'nextFieldId' => 10,
    );

    $new_id = GFAPI::add_form($form);
    if (is_wp_error($new_id)) {{
        echo 'ERR: create failed: ' . $new_id->get_error_message();
        @unlink(__FILE__);
        exit;
    }}
    update_option('cd_insolvency_test_form_id', (int) $new_id);
    echo 'OK: created form_id=' . (int) $new_id;
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
    trigger = "cdgfcreate"
    name = f"mu-cd-gf-create-insolvency-test-{token}.php"
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
    raise SystemExit(0 if run() else 1)
