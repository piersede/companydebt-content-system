"""Push article HTML to WordPress staging via SFTP + mu-plugin trigger.

This is the proven scalable path for content updates on comdebstage.wpengine.com.
It bypasses the WP REST API auth tangle (Basic-Auth gate vs App Password
collision) by:

  1. SFTP-uploading a one-shot mu-plugin PHP file + a JSON payload
  2. Triggering the plugin via a query-string URL (browser User-Agent required
     to clear the WAF)
  3. The plugin calls wp_update_post() and self-deletes both files

Environment (.env):
    SFTP_HOST, SFTP_PORT, SFTP_USER, SFTP_PASS
    WP_STAGING_URL, WP_BASIC_AUTH_USER, WP_BASIC_AUTH_PASS

Usage:
    python scripts/wp_push.py --id 77186 --file tmp/care-home-readability.html
    python scripts/wp_push.py --id 12345 --file preview/foo.html --status publish
    python scripts/wp_push.py --id 12345 --file preview/foo.html --post-type post
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

import paramiko
import requests
from dotenv import load_dotenv

ROOT = pathlib.Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

REMOTE_DIR = "/wp-content/mu-plugins"
BROWSER_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

PHP_TEMPLATE = """<?php
/**
 * One-shot WP post updater. Trigger: ?{trigger}={token}
 * Self-deletes after run.
 */
if (!isset($_GET['{trigger}']) || $_GET['{trigger}'] !== '{token}') {{
    return;
}}

add_action('init', function() {{
    $payload_path = __DIR__ . '/{payload_name}';
    if (!file_exists($payload_path)) {{
        echo 'ERR: payload missing'; exit;
    }}
    $p = json_decode(file_get_contents($payload_path), true);
    if (!$p || !isset($p['post_id']) || !isset($p['content'])) {{
        echo 'ERR: payload invalid'; exit;
    }}

    // Run as admin so wp_update_post skips kses filtering on block content
    wp_set_current_user(1);

    // wp_update_post expects slashed input; without wp_slash, internal
    // wp_unslash strips one level of backslashes — breaks JSON unicode
    // escapes (e.g. <) inside Gutenberg block attributes.
    $update = ['ID' => (int) $p['post_id'], 'post_content' => wp_slash($p['content'])];
    if (!empty($p['title']))  $update['post_title']  = wp_slash($p['title']);
    if (!empty($p['status'])) $update['post_status'] = $p['status'];

    $r = wp_update_post($update, true);
    if (is_wp_error($r)) {{
        echo 'ERR: ' . $r->get_error_message();
    }} else {{
        $permalink = get_permalink($r);
        echo 'OK: post=' . $r . ' content_len=' . strlen($p['content']) . ' url=' . $permalink;
    }}

    wp_cache_flush();
    @unlink($payload_path);
    @unlink(__FILE__);
    exit;
}}, 1);
"""


def extract_article_content(html_path: pathlib.Path) -> tuple[str, str | None]:
    """Pull inner content of <article> tag plus optional <title>."""
    raw = html_path.read_text(encoding="utf-8")
    article = re.search(r"<article[^>]*>(.*?)</article>", raw, re.DOTALL)
    if not article:
        sys.exit(f"ERROR: no <article>...</article> block in {html_path}")
    title_m = re.search(r"<title>(.*?)</title>", raw, re.DOTALL | re.IGNORECASE)
    title = title_m.group(1).strip() if title_m else None
    return article.group(1).strip(), title


def sftp_put(local: pathlib.Path, remote: str) -> None:
    host = os.environ["SFTP_HOST"]
    port = int(os.environ.get("SFTP_PORT", "2222"))
    t = paramiko.Transport((host, port))
    t.connect(username=os.environ["SFTP_USER"], password=os.environ["SFTP_PASS"])
    s = paramiko.SFTPClient.from_transport(t)
    try:
        s.put(str(local), remote)
    finally:
        s.close(); t.close()


def sftp_remove_if_exists(remote_paths: list[str]) -> list[str]:
    """Best-effort cleanup. Returns list of paths that were still present."""
    host = os.environ["SFTP_HOST"]
    port = int(os.environ.get("SFTP_PORT", "2222"))
    leftover = []
    t = paramiko.Transport((host, port))
    t.connect(username=os.environ["SFTP_USER"], password=os.environ["SFTP_PASS"])
    s = paramiko.SFTPClient.from_transport(t)
    try:
        for p in remote_paths:
            try:
                s.stat(p)
                try:
                    s.remove(p)
                    leftover.append(p)
                except Exception:
                    pass
            except FileNotFoundError:
                pass
    finally:
        s.close(); t.close()
    return leftover


def push(post_id: int, html_path: pathlib.Path, status: str | None,
         title_override: str | None) -> None:
    content, html_title = extract_article_content(html_path)
    title = title_override or html_title

    print(f"file:        {html_path}")
    print(f"post id:     {post_id}")
    print(f"content len: {len(content)}")
    if title:
        print(f"title:       {title}")
    if status:
        print(f"status:      {status}")

    # Random token + filenames so concurrent pushes don't collide
    token = uuid.uuid4().hex[:12]
    php_name = f"mu-cd-push-{token}.php"
    payload_name = f"mu-cd-push-{token}.json"
    trigger = "cdpush"

    payload = {"post_id": post_id, "content": content}
    if title: payload["title"] = title
    if status: payload["status"] = status

    tmp = ROOT / "tmp"
    tmp.mkdir(exist_ok=True)
    php_local = tmp / php_name
    json_local = tmp / payload_name
    php_local.write_text(
        PHP_TEMPLATE.format(trigger=trigger, token=token, payload_name=payload_name),
        encoding="utf-8",
    )
    json_local.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    remote_php = f"{REMOTE_DIR}/{php_name}"
    remote_json = f"{REMOTE_DIR}/{payload_name}"

    print("uploading via SFTP...")
    sftp_put(php_local, remote_php)
    sftp_put(json_local, remote_json)

    wp_url = os.environ["WP_STAGING_URL"].rstrip("/")
    auth = (os.environ["WP_BASIC_AUTH_USER"], os.environ["WP_BASIC_AUTH_PASS"])
    trigger_url = f"{wp_url}/?{trigger}={token}"
    print(f"triggering: {trigger_url}")
    time.sleep(1)
    resp = requests.get(
        trigger_url, auth=auth, headers={"User-Agent": BROWSER_UA}, timeout=120,
    )
    print(f"http: {resp.status_code}")
    print(f"body: {resp.text[:300]}")
    url_m = re.search(r"url=(https?://\S+)", resp.text)
    if url_m:
        print(f"url:         {url_m.group(1)}")

    # Local cleanup
    php_local.unlink(missing_ok=True)
    json_local.unlink(missing_ok=True)

    # Verify remote self-delete
    leftover = sftp_remove_if_exists([remote_php, remote_json])
    if leftover:
        print(f"warning: had to force-remove leftover files: {leftover}")
    else:
        print("remote cleanup confirmed (self-delete worked)")

    if resp.status_code != 200 or not resp.text.startswith("OK:"):
        sys.exit(f"ERROR: push failed (status={resp.status_code})")


def main() -> int:
    p = argparse.ArgumentParser(description="Push WP post content via SFTP+mu-plugin")
    p.add_argument("--id", type=int, required=True, help="Existing WP post ID")
    p.add_argument("--file", required=True, help="Path to HTML file with <article>")
    p.add_argument("--status", choices=["draft", "publish", "pending", "private"],
                   help="Set post_status (omit to leave unchanged)")
    p.add_argument("--title", help="Override post_title (else uses <title> from HTML)")
    args = p.parse_args()

    html_path = pathlib.Path(args.file)
    if not html_path.exists():
        sys.exit(f"ERROR: file not found: {html_path}")

    push(args.id, html_path, args.status, args.title)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
