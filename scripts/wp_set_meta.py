"""Set arbitrary postmeta key/value pairs on an existing WP post via SFTP +
mu-plugin (sibling of wp_push.py / wp_create_page.py). For metadata-only
changes (noindex flags, custom fields) that don't touch post_content.

Usage:
    python scripts/wp_set_meta.py --id 80717 --meta _yoast_wpseo_meta-robots-noindex=1
    python scripts/wp_set_meta.py --id 80717 --meta foo=bar --meta baz=qux
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time
import uuid

import requests

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import wp_push
import os

PHP_TEMPLATE = """<?php
/**
 * One-shot postmeta setter. Trigger: ?__TRIGGER__=__TOKEN__
 * Self-deletes after run.
 */
if (!isset($_GET['__TRIGGER__']) || $_GET['__TRIGGER__'] !== '__TOKEN__') {
    return;
}

add_action('init', function() {
    $payload_path = __DIR__ . '/__PAYLOAD__';
    if (!file_exists($payload_path)) {
        echo 'ERR: payload missing'; exit;
    }
    $p = json_decode(file_get_contents($payload_path), true);
    if (!$p || !isset($p['post_id']) || !isset($p['meta'])) {
        echo 'ERR: payload invalid'; exit;
    }

    wp_set_current_user(1);

    $done = [];
    foreach ($p['meta'] as $mk => $mv) {
        update_post_meta((int) $p['post_id'], $mk, wp_slash($mv));
        $done[] = $mk . '=' . $mv;
    }

    // Yoast serves robots/title/description from its own wp_yoast_indexable
    // cache table at render time, not live from postmeta — that row does not
    // reliably refresh on a bare update_post_meta(). Drop it so Yoast
    // rebuilds it from the postmeta we just wrote on the next request.
    $rebuilt = 0;
    global $wpdb;
    $tbl = $wpdb->prefix . 'yoast_indexable';
    if ($wpdb->get_var("SHOW TABLES LIKE '$tbl'") === $tbl) {
        $rebuilt = (int) $wpdb->delete(
            $tbl,
            ['object_id' => (int) $p['post_id'], 'object_type' => 'post'],
            ['%d', '%s']
        );
    }

    if (function_exists('rocket_clean_post')) {
        rocket_clean_post((int) $p['post_id']);
    }
    wp_cache_flush();

    echo 'OK: post=' . $p['post_id'] . ' set=[' . implode(',', $done) . ']'
       . ' indexable_rows_dropped=' . $rebuilt;

    @unlink($payload_path);
    @unlink(__FILE__);
    exit;
}, 1);
"""


def set_meta(post_id: int, meta: dict[str, str]) -> None:
    token = uuid.uuid4().hex[:12]
    trigger = "cdsetmeta"
    php_name = f"mu-cd-setmeta-{token}.php"
    payload_name = f"mu-cd-setmeta-{token}.json"

    payload = {"post_id": post_id, "meta": meta}

    tmp = wp_push.ROOT / "tmp"
    tmp.mkdir(exist_ok=True)
    php_local = tmp / php_name
    json_local = tmp / payload_name
    php_local.write_text(
        PHP_TEMPLATE
        .replace("__TRIGGER__", trigger)
        .replace("__TOKEN__", token)
        .replace("__PAYLOAD__", payload_name),
        encoding="utf-8",
    )
    json_local.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    remote_php = f"{wp_push.REMOTE_DIR}/{php_name}"
    remote_json = f"{wp_push.REMOTE_DIR}/{payload_name}"

    print(f"post id: {post_id}")
    print(f"meta:    {meta}")
    print("uploading via SFTP...")
    wp_push.sftp_put(php_local, remote_php)
    wp_push.sftp_put(json_local, remote_json)

    wp_url = os.environ["WP_STAGING_URL"].rstrip("/")
    auth = (os.environ["WP_BASIC_AUTH_USER"], os.environ["WP_BASIC_AUTH_PASS"])
    trigger_url = f"{wp_url}/?{trigger}={token}"
    print(f"triggering: {trigger_url}")
    time.sleep(1)
    resp = requests.get(
        trigger_url, auth=auth, headers={"User-Agent": wp_push.BROWSER_UA}, timeout=120,
    )
    print(f"http: {resp.status_code}")
    print(f"body: {resp.text[:400]}")

    php_local.unlink(missing_ok=True)
    json_local.unlink(missing_ok=True)

    leftover = wp_push.sftp_remove_if_exists([remote_php, remote_json])
    if leftover:
        print(f"warning: had to force-remove leftover files: {leftover}")
    else:
        print("remote cleanup confirmed (self-delete worked)")

    if resp.status_code != 200 or not resp.text.startswith("OK:"):
        sys.exit(f"ERROR: set-meta failed (status={resp.status_code})")


def main() -> int:
    p = argparse.ArgumentParser(description="Set postmeta via SFTP+mu-plugin")
    p.add_argument("--id", type=int, required=True, help="Existing WP post ID")
    p.add_argument("--meta", action="append", required=True, help="key=value, repeatable")
    args = p.parse_args()

    meta: dict[str, str] = {}
    for item in args.meta:
        if "=" not in item:
            sys.exit(f"ERROR: --meta must be key=value, got: {item}")
        k, v = item.split("=", 1)
        meta[k] = v

    set_meta(args.id, meta)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
