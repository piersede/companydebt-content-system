"""Push raw Gutenberg post_content to WordPress staging via SFTP + mu-plugin.

Sibling of wp_push.py, for pages that are NOT <article>-wrapped draft HTML —
e.g. the homepage, which is built from ACF blocks (acf/hero-blue,
acf/columns-with-buttons, etc.) mixed with core Gutenberg blocks. Feeding a
page like that through wp_push.py's extract_article_content() would either
fail to find an <article> tag or, if one were faked, replace the entire
post_content with just that fragment and destroy the block structure.

This script takes the full raw block markup verbatim (captured with
wp_dump_raw.py, edited in place) and pushes it as-is.

KSES: wp_push.py relies on wp_set_current_user(1) alone to dodge kses. That is
NOT sufficient on this host — a push of homepage markup silently stripped the
inline <svg> tick icons out of the hero trust bullets while still returning
"OK". This template calls kses_remove_filters() explicitly before the update,
which is what actually keeps inline SVG intact. Verify with wp_dump_raw.py
after every push; the HTTP 200 proves nothing.

Usage:
    python scripts/wp_push_raw.py --id 55052 --file tmp/homepage-content.html
    python scripts/wp_push_raw.py --id 55052 --file tmp/homepage-content.html \
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
 * One-shot raw post_content updater. Trigger: ?__TRIGGER__=__TOKEN__
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
    if (!$p || !isset($p['post_id']) || !isset($p['content'])) {
        echo 'ERR: payload invalid'; exit;
    }

    wp_set_current_user(1);

    // wp_set_current_user() alone does not reliably detach the kses filters on
    // this host, and kses strips inline <svg>/<circle>/<path> out of block
    // markup without any error. Detach them explicitly.
    if (function_exists('kses_remove_filters')) {
        kses_remove_filters();
    }

    // Yoast title/description live in post meta. Write them BEFORE
    // wp_update_post so the indexable rebuild on save_post reads fresh values.
    $meta_done = [];
    if (!empty($p['meta']) && is_array($p['meta'])) {
        foreach ($p['meta'] as $mk => $mv) {
            update_post_meta((int) $p['post_id'], $mk, wp_slash($mv));
            $meta_done[] = $mk;
        }
    }

    $update = ['ID' => (int) $p['post_id'], 'post_content' => wp_slash($p['content'])];
    if (!empty($p['title']))  $update['post_title']  = wp_slash($p['title']);
    if (!empty($p['status'])) $update['post_status'] = $p['status'];

    $r = wp_update_post($update, true);
    if (is_wp_error($r)) {
        echo 'ERR: ' . $r->get_error_message();
    } else {
        // Yoast serves <title>/meta description from its own indexable cache
        // table, which does not reliably refresh on save_post. Drop the row.
        $rebuilt = 0;
        if (!empty($meta_done)) {
            global $wpdb;
            $tbl = $wpdb->prefix . 'yoast_indexable';
            if ($wpdb->get_var("SHOW TABLES LIKE '$tbl'") === $tbl) {
                $rebuilt = (int) $wpdb->delete(
                    $tbl,
                    ['object_id' => (int) $p['post_id'], 'object_type' => 'post'],
                    ['%d', '%s']
                );
            }
        }

        if (function_exists('rocket_clean_post')) {
            rocket_clean_post((int) $p['post_id']);
        }

        $stored = get_post((int) $p['post_id'])->post_content;
        echo 'OK: post=' . $r
           . ' sent_len=' . strlen($p['content'])
           . ' stored_len=' . strlen($stored)
           . ' svg_sent=' . substr_count($p['content'], '<svg')
           . ' svg_stored=' . substr_count($stored, '<svg')
           . ' meta=[' . implode(',', $meta_done) . ']'
           . ' indexable_rows_dropped=' . $rebuilt
           . ' url=' . get_permalink($r);
    }

    wp_cache_flush();
    @unlink($payload_path);
    @unlink(__FILE__);
    exit;
}, 1);
"""


def push_raw(post_id: int, content_path: pathlib.Path, status: str | None,
             title: str | None, meta: dict[str, str] | None = None) -> None:
    content = content_path.read_text(encoding="utf-8")

    print(f"file:        {content_path}")
    print(f"post id:     {post_id}")
    print(f"content len: {len(content)}")
    if title:
        print(f"title:       {title}")
    if status:
        print(f"status:      {status}")

    token = uuid.uuid4().hex[:12]
    trigger = "cdpush"
    php_name = f"mu-cd-pushraw-{token}.php"
    payload_name = f"mu-cd-pushraw-{token}.json"

    payload = {"post_id": post_id, "content": content}
    if title: payload["title"] = title
    if status: payload["status"] = status
    if meta: payload["meta"] = meta

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
        sys.exit(f"ERROR: push failed (status={resp.status_code})")

    m = re.search(r"svg_sent=(\d+) svg_stored=(\d+)", resp.text)
    if m and m.group(1) != m.group(2):
        sys.exit(f"ERROR: kses stripped inline SVG "
                 f"(sent {m.group(1)}, stored {m.group(2)})")


def main() -> int:
    p = argparse.ArgumentParser(description="Push raw Gutenberg post_content via SFTP+mu-plugin")
    p.add_argument("--id", type=int, required=True, help="Existing WP post ID")
    p.add_argument("--file", required=True, help="Path to file with full raw block markup")
    p.add_argument("--status", choices=["draft", "publish", "pending", "private"],
                   help="Set post_status (omit to leave unchanged)")
    p.add_argument("--title", help="Override post_title")
    p.add_argument("--seo-title", help="Yoast SEO title (the <title> tag)")
    p.add_argument("--seo-desc", help="Yoast meta description")
    args = p.parse_args()

    content_path = pathlib.Path(args.file)
    if not content_path.exists():
        sys.exit(f"ERROR: file not found: {content_path}")

    meta: dict[str, str] = {}
    if args.seo_title: meta["_yoast_wpseo_title"] = args.seo_title
    if args.seo_desc:  meta["_yoast_wpseo_metadesc"] = args.seo_desc

    push_raw(args.id, content_path, args.status, args.title, meta or None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
