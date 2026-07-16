"""Set Yoast meta descriptions on the /data/ pages AND drop the stale indexable rows.

Why not just PATCH the REST meta? Because it silently does nothing visible.
Yoast 14+ renders <meta name="description"> from its own `wp_yoast_indexable`
cache table, not from post meta. Verified 2026-07-16: a REST write returned 200
and stored the value, and the page kept rendering the old 167-char description.
The cache row has to be deleted; Yoast then lazily rebuilds it from post meta.

Why not wp_push.py? It requires --file and rewrites post_content. These pages
must not have their content replaced from a possibly-stale draft just to change
a meta tag.

Mechanism: SFTP a token-guarded one-shot mu-plugin, trigger it over HTTP with a
browser UA (clears the WAF), self-delete. Same proven path as
scripts/add_prepack_redirect.py. STAGING ONLY.

Usage:
    python scripts/ahrefs_audit/push_meta_desc.py          # dry run
    python scripts/ahrefs_audit/push_meta_desc.py --apply
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

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(pathlib.Path(__file__).parent))
load_dotenv(ROOT / ".env")

from meta_desc_fixes import FIXES, LIMIT  # noqa: E402

REMOTE_DIR = "wp-content/mu-plugins"
BROWSER_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

PHP_TEMPLATE = """<?php
/** One-shot: set Yoast metadesc + drop stale indexable rows. Trigger ?__TRIGGER__=__TOKEN__. Self-deletes. */
if (!isset($_GET['__TRIGGER__']) || $_GET['__TRIGGER__'] !== '__TOKEN__') { return; }
add_action('init', function() {
    header('Content-Type: text/plain; charset=utf-8');
    global $wpdb;
    $map = array(
__PAIRS__
    );
    echo "DONE\\n";
    $tbl = $wpdb->prefix . 'yoast_indexable';
    $has_tbl = ($wpdb->get_var("SHOW TABLES LIKE '$tbl'") === $tbl);
    foreach ($map as $slug => $desc) {
        $page = get_page_by_path('data/' . $slug, OBJECT, array('page','post'));
        if (!$page) { echo "  MISSING {$slug}\\n"; continue; }
        update_post_meta($page->ID, '_yoast_wpseo_metadesc', wp_slash($desc));
        $dropped = 0;
        if ($has_tbl) {
            $dropped = (int) $wpdb->delete($tbl,
                array('object_id' => (int) $page->ID, 'object_type' => 'post'),
                array('%d', '%s'));
        }
        $stored = get_post_meta($page->ID, '_yoast_wpseo_metadesc', true);
        echo "  {$slug} id={$page->ID} len=" . strlen($stored) . " indexable_dropped={$dropped}\\n";
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
    pairs = "\n".join(
        "        '{}' => '{}',".format(slug, desc.replace("\\", "\\\\").replace("'", "\\'"))
        for slug, desc in FIXES.items()
    )
    return (PHP_TEMPLATE
            .replace("__TRIGGER__", trigger)
            .replace("__TOKEN__", token)
            .replace("__PAIRS__", pairs))


def run(apply: bool) -> bool:
    over = {s: len(d) for s, d in FIXES.items() if len(d) > LIMIT}
    if over:
        print("REFUSING: descriptions over limit:", over)
        return False
    print(f"{len(FIXES)} descriptions, all <= {LIMIT} chars")
    if not apply:
        print("\nDry run. Pass --apply to write.")
        return True

    token = uuid.uuid4().hex[:12]
    trigger = "cdmeta"
    name = f"mu-cd-meta-{token}.php"
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
            print("warning: forced removal of leftover plugin")
        except FileNotFoundError:
            print("remote cleanup confirmed (self-deleted)")
    finally:
        s.close(); t.close()
    return resp.status_code == 200 and "DONE" in resp.text


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(0 if run("--apply" in sys.argv) else 1)
