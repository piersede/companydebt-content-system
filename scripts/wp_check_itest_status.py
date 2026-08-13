"""One-shot: report status of the Insolvency Test on staging.
Dumps: form_id, latest 3 entries (id + email + tier), and Zoho last-success / last-error.
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
    $fid = (int) get_option('cd_insolvency_test_form_id', 0);
    echo "form_id=$fid\n";
    if ($fid && class_exists('GFAPI')) {{
        $entries = GFAPI::get_entries($fid, array(), array('key'=>'id','direction'=>'DESC'), array('page_size'=>5));
        foreach ($entries as $e) {{
            $zoho_id = gform_get_meta($e['id'], 'cd_zoho_lead_id');
            echo "entry " . $e['id']
                . " | date=" . $e['date_created']
                . " | name=" . rgar($e,'1')
                . " | email=" . rgar($e,'2')
                . " | tier=" . rgar($e,'6')
                . " | zoho=" . ($zoho_id ?: '-')
                . "\n";
        }}
    }}
    echo "\nlast success: " . print_r(get_option('cd_zoho_last_success', 'none'), true);
    echo "\nlast error:   " . print_r(get_option('cd_zoho_last_error',   'none'), true);
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
    trigger = "cditeststat"
    name = f"mu-cd-itest-status-{token}.php"
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
    print(resp.text[:3000])
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
