"""Create a new WP page via SFTP + mu-plugin trigger (sibling of wp_push.py).

The REST API is unusable here (nginx Basic-Auth gate collides with WP App
Passwords), so page creation uses the same one-shot, self-deleting mu-plugin
transport as wp_push.py / wp_dump_raw.py: SFTP a trigger PHP file, hit it over
HTTP through the nginx gate, the plugin runs wp_insert_post() as admin and
self-deletes.

Usage:
    python scripts/wp_create_page.py --slug quick-quote-options \
        --title "Understand Your Company's Options" \
        --template templates/insolvency-landing-page.php \
        --status publish \
        --seo-title "..." --seo-desc "..."
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import sys
import time
import uuid

import requests

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import wp_push

PHP_TEMPLATE = """<?php
/**
 * One-shot WP page creator. Trigger: ?__TRIGGER__=__TOKEN__
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
    if (!$p || !isset($p['slug'])) {
        echo 'ERR: payload invalid'; exit;
    }

    wp_set_current_user(1);

    $existing = get_page_by_path($p['slug'], OBJECT, 'page');
    if ($existing) {
        echo 'ERR: page with slug already exists, id=' . $existing->ID;
        @unlink($payload_path);
        @unlink(__FILE__);
        exit;
    }

    $postarr = [
        'post_type'    => 'page',
        'post_name'    => $p['slug'],
        'post_title'   => $p['title'],
        'post_content' => isset($p['content']) ? $p['content'] : '',
        'post_status'  => isset($p['status']) ? $p['status'] : 'draft',
    ];
    $new_id = wp_insert_post($postarr, true);
    if (is_wp_error($new_id)) {
        echo 'ERR: ' . $new_id->get_error_message();
        @unlink($payload_path);
        @unlink(__FILE__);
        exit;
    }

    if (!empty($p['template'])) {
        update_post_meta($new_id, '_wp_page_template', $p['template']);
    }
    if (!empty($p['meta']) && is_array($p['meta'])) {
        foreach ($p['meta'] as $mk => $mv) {
            update_post_meta($new_id, $mk, wp_slash($mv));
        }
    }

    wp_cache_flush();
    echo 'OK: post=' . $new_id . ' url=' . get_permalink($new_id);

    @unlink($payload_path);
    @unlink(__FILE__);
    exit;
}, 1);
"""


def create(slug: str, title: str, template: str | None, status: str,
           content: str, meta: dict[str, str] | None = None) -> None:
    token = uuid.uuid4().hex[:12]
    trigger = "cdcreate"
    php_name = f"mu-cd-create-{token}.php"
    payload_name = f"mu-cd-create-{token}.json"

    payload = {"slug": slug, "title": title, "status": status, "content": content}
    if template:
        payload["template"] = template
    if meta:
        payload["meta"] = meta

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

    print(f"slug:     {slug}")
    print(f"title:    {title}")
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
        sys.exit(f"ERROR: create failed (status={resp.status_code})")

    m = re.search(r"post=(\d+)", resp.text)
    if m:
        print(f"post id:  {m.group(1)}")


def main() -> int:
    p = argparse.ArgumentParser(description="Create a new WP page via SFTP+mu-plugin")
    p.add_argument("--slug", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--template", help="_wp_page_template value, e.g. templates/foo.php")
    p.add_argument("--status", choices=["draft", "publish", "pending", "private"], default="draft")
    p.add_argument("--content", default="", help="post_content (often irrelevant if the template hardcodes markup)")
    p.add_argument("--seo-title")
    p.add_argument("--seo-desc")
    args = p.parse_args()

    meta: dict[str, str] = {}
    if args.seo_title:
        meta["_yoast_wpseo_title"] = args.seo_title
    if args.seo_desc:
        meta["_yoast_wpseo_metadesc"] = args.seo_desc

    create(args.slug, args.title, args.template, args.status, args.content, meta or None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
