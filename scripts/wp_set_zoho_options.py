"""One-shot: plant Zoho OAuth credentials into WP options on staging.

The Insolvency Test mu-plugin (cd-insolvency-test-zoho.php) reads its Zoho
credentials from wp_options rather than from wp-config or the environment,
so the plugin is self-contained and site-portable. This script copies the
CD_ZOHO_* values from local .env into the site's option store via a
one-shot mu-plugin.

Options set:
  cd_zoho_client_id
  cd_zoho_client_secret
  cd_zoho_refresh_token
  cd_zoho_api_domain
  cd_zoho_accounts_domain  (accounts.zoho.com for the .com data centre)

Re-runnable; simply overwrites the existing option values.
"""
from __future__ import annotations

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
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
from _env import load_env as _load_env
_load_env()
REMOTE_DIR = "wp-content/mu-plugins"
BROWSER_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


def _env(key: str) -> str:
    v = os.getenv(key, "")
    return v.strip().strip('"').strip("'")


PHP_TEMPLATE = r"""<?php
/** One-shot: set Zoho creds as WP options. Trigger: ?{trigger}={token}. Self-deletes. */
if (!isset($_GET['{trigger}']) || $_GET['{trigger}'] !== '{token}') {{ return; }}
add_action('init', function() {{
    update_option('cd_zoho_client_id',       '{client_id}');
    update_option('cd_zoho_client_secret',   '{client_secret}');
    update_option('cd_zoho_refresh_token',   '{refresh_token}');
    update_option('cd_zoho_api_domain',      '{api_domain}');
    update_option('cd_zoho_accounts_domain', 'https://accounts.zoho.com');
    echo 'OK: Zoho creds planted';
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
    trigger = "cdzohoopt"
    name = f"mu-cd-zoho-opts-{token}.php"

    body = PHP_TEMPLATE.format(
        trigger=trigger,
        token=token,
        client_id=_env("CD_ZOHO_CLIENT_ID"),
        client_secret=_env("CD_ZOHO_CLIENT_SECRET"),
        refresh_token=_env("CD_ZOHO_REFRESH_TOKEN"),
        api_domain=_env("CD_ZOHO_API_DOMAIN") or "https://www.zohoapis.com",
    )
    local = ROOT / "tmp" / name
    local.parent.mkdir(exist_ok=True)
    local.write_text(body, encoding="utf-8")
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
    print(f"http {resp.status_code}: {resp.text[:300]}")
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
