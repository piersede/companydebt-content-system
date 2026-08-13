"""Diagnose why the Zoho hook isn't firing on Insolvency Test submissions.
Reports: is the mu-plugin loaded, is the hook registered, does GF fire it on
REST submissions, what the entry payload looks like inside the hook.
"""
from __future__ import annotations
import os, pathlib, sys, time, uuid, paramiko, requests
from dotenv import load_dotenv

ROOT = pathlib.Path(__file__).resolve().parents[1]
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
from _env import load_env as _load_env
_load_env()
REMOTE_DIR = "wp-content/mu-plugins"
BROWSER_UA = "Mozilla/5.0"

PHP = r"""<?php
if (!isset($_GET['{trigger}']) || $_GET['{trigger}'] !== '{token}') {{ return; }}
add_action('init', function() {{
    header('Content-Type: text/plain; charset=utf-8');
    // Is the Zoho mu-plugin loaded?
    $mu_exists = file_exists(WPMU_PLUGIN_DIR . '/cd-insolvency-test-zoho.php');
    echo "mu_file_exists=" . ($mu_exists ? 'yes' : 'no') . "\n";
    // Is the hook registered?
    global $wp_filter;
    $registered = array();
    if (!empty($wp_filter['gform_after_submission']) && !empty($wp_filter['gform_after_submission']->callbacks)) {{
        foreach ($wp_filter['gform_after_submission']->callbacks as $prio => $cbs) {{
            foreach ($cbs as $cb) {{
                $fn = $cb['function'];
                if (is_string($fn)) $name = $fn;
                elseif (is_array($fn)) $name = (is_object($fn[0]) ? get_class($fn[0]) : $fn[0]) . '::' . $fn[1];
                else $name = 'closure';
                $registered[] = "prio=$prio name=$name";
            }}
        }}
    }}
    echo "hooks_on_gform_after_submission=" . implode(' | ', $registered) . "\n";
    // Verify option is set
    echo "cd_insolvency_test_form_id=" . get_option('cd_insolvency_test_form_id', 'MISSING') . "\n";
    echo "cd_zoho_refresh_token_len=" . strlen((string) get_option('cd_zoho_refresh_token', '')) . "\n";
    echo "cd_zoho_last_success=" . print_r(get_option('cd_zoho_last_success','none'), true) . "\n";
    echo "cd_zoho_last_error=" . print_r(get_option('cd_zoho_last_error','none'), true) . "\n";
    // Try to reprocess entry 8298 as if it were a fresh submission — this
    // exercises the entire Zoho hook against a known-good entry.
    if (class_exists('GFAPI') && function_exists('cd_itest_zoho_push')) {{
        $entry = GFAPI::get_entry(8298);
        $form  = GFAPI::get_form((int) get_option('cd_insolvency_test_form_id', 0));
        if (is_array($entry) && is_array($form)) {{
            echo "\nreplaying entry 8298:\n";
            echo "  email in entry = " . rgar($entry, '2') . "\n";
            echo "  form id = " . $form['id'] . "\n";
            cd_itest_zoho_push($entry, $form);
            echo "\nafter replay:\n";
            echo "  cd_zoho_last_success=" . print_r(get_option('cd_zoho_last_success','none'), true) . "\n";
            echo "  cd_zoho_last_error=" . print_r(get_option('cd_zoho_last_error','none'), true) . "\n";
        }}
    }} else {{
        echo "cd_itest_zoho_push function exists=" . (function_exists('cd_itest_zoho_push') ? 'yes' : 'no') . "\n";
    }}
    @unlink(__FILE__);
    exit;
}}, 99);
"""

def _sftp():
    t = paramiko.Transport((os.environ["SFTP_HOST"], int(os.environ.get("SFTP_PORT", "2222"))))
    t.connect(username=os.environ["SFTP_USER"], password=os.environ["SFTP_PASS"])
    return t, paramiko.SFTPClient.from_transport(t)

def run() -> bool:
    token = uuid.uuid4().hex[:12]
    trigger = "cddiagzh"
    name = f"mu-cd-diag-zoho-{token}.php"
    body = PHP.format(trigger=trigger, token=token)
    local = ROOT / "tmp" / name
    local.parent.mkdir(exist_ok=True)
    local.write_text(body, encoding="utf-8")
    remote = f"{REMOTE_DIR}/{name}"
    t, s = _sftp()
    try: s.put(str(local), remote)
    finally: s.close(); t.close()
    wp_url = os.environ["WP_STAGING_URL"].rstrip("/")
    auth = (os.environ["WP_BASIC_AUTH_USER"], os.environ["WP_BASIC_AUTH_PASS"])
    time.sleep(1)
    resp = requests.get(f"{wp_url}/?{trigger}={token}", auth=auth, headers={"User-Agent": BROWSER_UA}, timeout=60)
    print(resp.text[:5000])
    local.unlink(missing_ok=True)
    t, s = _sftp()
    try:
        try: s.stat(remote); s.remove(remote)
        except FileNotFoundError: pass
    finally: s.close(); t.close()
    return True

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(0 if run() else 1)
