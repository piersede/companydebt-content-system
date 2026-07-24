"""Dump a WordPress post's raw post_content via SFTP + mu-plugin trigger.

The read-side counterpart to wp_push_raw.py. The REST API is not usable on
this host for editing context: WP Engine's nginx Basic-Auth gate and WP
Application Passwords both occupy the Authorization header, so an authenticated
`context=edit` read collides and returns rest_forbidden_context. This uses the
same transport wp_push.py already relies on instead: SFTP a one-shot,
self-deleting mu-plugin, trigger it over HTTP, read the content straight out of
the response body between sentinels.

Use it to capture an exact byte-for-byte copy of a page's block markup before
editing it, so edits are surgical string replacements against real content
rather than hand-retyped reconstructions.

Usage:
    python scripts/wp_dump_raw.py --id 55052 --out tmp/homepage-55052-original.html
"""

from __future__ import annotations

import argparse
import os
import pathlib
import sys
import time
import uuid

import requests

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import wp_push

START = "<<<CDDUMP_START>>>"
END = "<<<CDDUMP_END>>>"

PHP_TEMPLATE = """<?php
/**
 * One-shot WP post content dumper. Trigger: ?__TRIGGER__=__TOKEN__
 * Self-deletes after run.
 */
if (!isset($_GET['__TRIGGER__']) || $_GET['__TRIGGER__'] !== '__TOKEN__') {
    return;
}

add_action('init', function() {
    $p = get_post(__POSTID__);
    if (!$p) {
        echo 'ERR: post not found';
        @unlink(__FILE__);
        exit;
    }
    header('Content-Type: text/plain; charset=utf-8');
    echo '__START__';
    echo $p->post_content;
    echo '__END__';
    @unlink(__FILE__);
    exit;
}, 1);
"""


def dump(post_id: int, out_path: pathlib.Path) -> None:
    token = uuid.uuid4().hex[:12]
    trigger = "cddump"
    php_name = f"mu-cd-dump-{token}.php"

    php_src = (
        PHP_TEMPLATE
        .replace("__TRIGGER__", trigger)
        .replace("__TOKEN__", token)
        .replace("__POSTID__", str(post_id))
        .replace("__START__", START)
        .replace("__END__", END)
    )

    tmp = wp_push.ROOT / "tmp"
    tmp.mkdir(exist_ok=True)
    php_local = tmp / php_name
    php_local.write_text(php_src, encoding="utf-8")

    remote_php = f"{wp_push.REMOTE_DIR}/{php_name}"
    print(f"post id:  {post_id}")
    print("uploading via SFTP...")
    wp_push.sftp_put(php_local, remote_php)

    wp_url = os.environ["WP_STAGING_URL"].rstrip("/")
    auth = (os.environ["WP_BASIC_AUTH_USER"], os.environ["WP_BASIC_AUTH_PASS"])
    trigger_url = f"{wp_url}/?{trigger}={token}"
    print(f"triggering: {trigger_url}")
    time.sleep(1)
    resp = requests.get(
        trigger_url, auth=auth, headers={"User-Agent": wp_push.BROWSER_UA}, timeout=120,
    )
    resp.encoding = "utf-8"
    print(f"http: {resp.status_code}")

    php_local.unlink(missing_ok=True)
    leftover = wp_push.sftp_remove_if_exists([remote_php])
    if leftover:
        print(f"warning: had to force-remove leftover files: {leftover}")
    else:
        print("remote cleanup confirmed (self-delete worked)")

    body = resp.text
    if START not in body or END not in body:
        sys.exit(f"ERROR: sentinels missing in response. First 400 chars:\n{body[:400]}")

    content = body.split(START, 1)[1].rsplit(END, 1)[0]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    print(f"content len: {len(content)}")
    print(f"written:     {out_path}")


def main() -> int:
    p = argparse.ArgumentParser(description="Dump raw WP post_content via SFTP+mu-plugin")
    p.add_argument("--id", type=int, required=True, help="WP post ID")
    p.add_argument("--out", required=True, help="Path to write raw block markup to")
    args = p.parse_args()

    dump(args.id, pathlib.Path(args.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
