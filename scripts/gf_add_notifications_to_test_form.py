"""One-shot: add the internal + visitor notifications to form 46 (Insolvency Test).

Copies the internal recipient address from form 38 (the old calculator) so the
new form's leads land in the same inbox — no need to reconfigure recipients.
Also adds a visitor result email templated with the tier and next steps.

Idempotent: skips adding a notification if one with the same 'name' already
exists on the form.
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

PHP = r"""<?php
/** One-shot: add notifications to the Insolvency Test form. Trigger: ?{trigger}={token}. Self-deletes. */
if (!isset($_GET['{trigger}']) || $_GET['{trigger}'] !== '{token}') {{ return; }}
add_action('init', function() {{
    if (!class_exists('GFAPI')) {{ echo 'ERR: GFAPI missing'; @unlink(__FILE__); exit; }}

    $target_id = (int) get_option('cd_insolvency_test_form_id', 0);
    if (!$target_id) {{ echo 'ERR: cd_insolvency_test_form_id option not set'; @unlink(__FILE__); exit; }}

    // Discover the internal recipient from form 38 (the old calculator) so leads
    // continue to land in the same inbox with no manual reconfiguration.
    $internal_to = '';
    $form38 = GFAPI::get_form(38);
    if ($form38 && !empty($form38['notifications'])) {{
        foreach ($form38['notifications'] as $n) {{
            if (!empty($n['to']) && strpos($n['to'], '{{admin_email}}') === false && !empty($n['to']) && filter_var(explode(',', $n['to'])[0], FILTER_VALIDATE_EMAIL)) {{
                $internal_to = $n['to'];
                break;
            }}
        }}
    }}
    if (!$internal_to) {{ $internal_to = get_option('admin_email'); }}

    $form = GFAPI::get_form($target_id);
    if (!$form) {{ echo 'ERR: form ' . $target_id . ' missing'; @unlink(__FILE__); exit; }}
    if (empty($form['notifications'])) $form['notifications'] = array();

    // Helper to add-if-not-present (matches on 'name').
    $ensure = function(&$form, $name, $spec) {{
        foreach ($form['notifications'] as $n) {{
            if (isset($n['name']) && $n['name'] === $name) return false;
        }}
        $spec['id'] = uniqid('cd_', true);
        $spec['name'] = $name;
        $spec['event'] = 'form_submission';
        $spec['isActive'] = true;
        $form['notifications'][$spec['id']] = $spec;
        return true;
    }};

    // --- Internal lead notification ---
    $internal_message = "New Insolvency Test lead received.\n\n"
        . "Risk tier: {{Risk tier:6}}\n"
        . "Wants call: {{Wants call:3}}\n"
        . "Preferred time: {{Preferred time:5}}\n\n"
        . "Name: {{First name:1}}\n"
        . "Email: {{Email:2}}\n"
        . "Phone: {{Phone:4}}\n\n"
        . "Landing page: {{Landing page:8}}\n"
        . "Referring page: {{Referring page:9}}\n\n"
        . "Quiz payload (JSON):\n{{Quiz payload:7}}\n";
    $added_internal = $ensure($form, 'Insolvency Test — internal lead', array(
        'to'       => $internal_to,
        'fromName' => 'Company Debt Website',
        'from'     => '{{admin_email}}',
        'subject'  => 'Insolvency Test lead — {{Risk tier:6}} — {{First name:1}}',
        'message'  => $internal_message,
        'disableAutoformat' => false,
    ));

    // --- Visitor result email ---
    $visitor_message = "Hi {{First name:1}},\n\n"
        . "Thank you for completing our Insolvency Test. Based on your answers, the initial result is:\n\n"
        . "**{{Risk tier:6}}**\n\n"
        . "This is an initial guidance result, not a formal insolvency opinion. If you have any questions or would like to talk through your position, "
        . "you can reach a member of our team on 0800 074 6757 or reply to this email.\n\n"
        . "Warm regards,\n"
        . "Company Debt\n"
        . "Licensed Insolvency Practitioners\n"
        . "https://www.companydebt.com\n";
    $added_visitor = $ensure($form, 'Insolvency Test — visitor result', array(
        'toType'   => 'field',
        'to'       => '2',  // Email field id
        'fromName' => 'Company Debt',
        'from'     => 'info@companydebt.com',
        'subject'  => 'Your Insolvency Test result — {{Risk tier:6}}',
        'message'  => $visitor_message,
        'disableAutoformat' => false,
    ));

    $res = GFAPI::update_form($form);
    if (is_wp_error($res)) {{
        echo 'ERR: update failed: ' . $res->get_error_message();
    }} else {{
        echo 'OK: internal_added=' . ($added_internal ? 'yes' : 'skip') . ' | visitor_added=' . ($added_visitor ? 'yes' : 'skip') . ' | internal_to=' . $internal_to;
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
    trigger = "cdgfnot"
    name = f"mu-cd-gf-notifications-{token}.php"
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
