"""One-shot: dump ALL entries for form 46, splitting by status."""
from __future__ import annotations
import os, pathlib, sys, time, uuid, paramiko, requests
from dotenv import load_dotenv
ROOT = pathlib.Path(__file__).resolve().parents[1]
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
from _env import load_env as _load_env
_load_env()
REMOTE_DIR = "wp-content/mu-plugins"

# PHP body — no PHP curly-braces interpolation (avoid Python format collisions).
PHP = r"""<?php
if (!isset($_GET['TRIG']) || $_GET['TRIG'] !== 'TOK') { return; }
add_action('init', function() {
    header('Content-Type: text/plain; charset=utf-8');
    if (!class_exists('GFAPI')) { echo 'no GFAPI'; @unlink(__FILE__); exit; }
    $statuses = array('active','spam','trash');
    foreach ($statuses as $st) {
        $entries = \GFAPI::get_entries(46, array('status' => $st), array('key'=>'id','direction'=>'DESC'), array('page_size'=>20));
        echo strtoupper($st) . ' entries in form 46: (' . count($entries) . ')' . "\n";
        foreach ($entries as $e) {
            $id     = isset($e['id']) ? $e['id'] : '?';
            $date   = isset($e['date_created']) ? $e['date_created'] : '?';
            $status = isset($e['status']) ? $e['status'] : '?';
            $email  = rgar($e, '2');
            echo '  id=' . $id . ' date=' . $date . ' status=' . $status . ' email=' . $email . "\n";
        }
        echo "\n";
    }
    $cnt = \GFAPI::count_entries(46);
    echo 'count_entries(46) = ' . $cnt . "\n";
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
    trigger = "cddumpent"
    name = f"mu-cd-dump-entries-{token}.php"
    body = PHP.replace('TRIG', trigger).replace('TOK', token)
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
    resp = requests.get(f"{wp_url}/?{trigger}={token}", auth=auth, headers={"User-Agent": "Mozilla/5.0"}, timeout=60)
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
