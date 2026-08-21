"""Create and configure the four PPC landing pages on STAGING.

What this does, per page (idempotent, never duplicates):

  1. Find the page by slug. Create it only if it is absent.
  2. Set _wp_page_template = templates/ppc-landing.php
  3. Set _yoast_wpseo_meta-robots-noindex = 1  (PPC pages must never be indexed)
  4. Set the Yoast meta description (_yoast_wpseo_metadesc) and SEO title.
  5. Delete the page's wp_yoast_indexable row so Yoast rebuilds it. Without
     this, the meta write reports success and the rendered page does not
     change, because Yoast serves robots/title/description from that cache
     table (see scripts/wp_set_meta.py lines 53-71).
  6. Purge WP Rocket for the page.

Then it VERIFIES over HTTP by re-fetching each public URL and reading the
RENDERED HTML:

  (a) HTTP 200
  (b) <meta name="robots" ...> present and containing "noindex"
  (c) a marker only templates/ppc-landing.php can emit (the <style id="cd-ppc-styles">
      block, or the <div class="cd-ppc" data-intent="..."> wrapper). The body class
      is NOT proof: WordPress derives it from the _wp_page_template postmeta that
      this very script writes, so it appears even when the template file was never
      uploaded and page.php rendered instead.
  (d) the Gravity Forms wrapper is present, and the template's
      "form is not configured" placeholder is absent. A PPC page with no lead
      capture is the worst silent failure available here.
  (e) response body over 20,000 bytes (a plausible full page)

A 200 is not proof. This repo has a documented failure where a push returns
"200 / OK" and lands truncated content, so the render check is required.

Transport: the same one-shot, self-deleting mu-plugin used by wp_push.py,
wp_create_page.py and wp_set_meta.py. The staging REST API is unusable for
writes here (the nginx Basic-Auth gate collides with WP App Passwords).

STAGING ONLY. The script asserts the target host is the staging host and
exits if it is not. It cannot target live.

Usage:
    python scripts/deploy_ppc_pages.py                # dry run (default)
    python scripts/deploy_ppc_pages.py --confirm      # write
    python scripts/deploy_ppc_pages.py --verify-only  # re-run the checks only

--dry-run is authoritative: pass it with --confirm and nothing is written.

BEFORE THIS SCRIPT RUNS, both of these must already be true, or the verify
step fails by design:
  - theme/templates/ppc-landing.php and theme/assets/ppc/ are on the server.
  - scripts/gf_create_ppc_form.py has run and the option cd_ppc_form_id is set,
    with the id registered per docs/ppc-form-registration.md.
Full order of work: docs/ppc-landing-deployment.md
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
from urllib.parse import urlparse

import requests

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import wp_push  # noqa: E402  (importing it also loads the repo .env, worktree-safe)

# ---------------------------------------------------------------- constants

STAGING_HOST = "comdebstage.wpengine.com"
FORBIDDEN_HOSTS = {"companydebt.com", "www.companydebt.com"}

TEMPLATE = "templates/ppc-landing.php"

# WordPress body_class() derives these classes from the template slug.
#
# THEY PROVE NOTHING. get_body_class() asks is_page_template(), which is a bare
# read of the _wp_page_template postmeta - the meta THIS SCRIPT writes at
# PHP_TEMPLATE below. There is no file_exists() anywhere in that path. Run the
# deploy before uploading templates/ppc-landing.php and WordPress falls back to
# page.php, renders an empty page with full theme chrome, and still stamps the
# class on <body>. Header, nav and footer alone clear the 20,000 byte floor.
# Kept only as a secondary signal. It must never decide PASS.
BODY_CLASS_CANDIDATES = (
    "page-template-ppc-landing",
    "page-template-templatesppc-landing-php",
)

# What DOES prove the template rendered: markup only templates/ppc-landing.php
# emits. The <style id="cd-ppc-styles"> block (ppc-landing.php line 211) and the
# <div class="cd-ppc" data-intent="..."> wrapper (line 531) exist in no other
# template. Either one is decisive.
TEMPLATE_MARKER_RE = re.compile(
    r"""id=["']cd-ppc-styles["']|class=["']cd-ppc["']\s+data-intent=""",
    re.I,
)

# The Gravity Forms wrapper div, e.g. <div class='gform_wrapper gravity-theme'
# id='gform_wrapper_47'>. Matched on the id attribute so the template's own CSS
# rule ".cd-ppc-form .gform_wrapper" cannot be mistaken for a rendered form.
GF_WRAPPER_RE = re.compile(r"""id=["']gform_wrapper_\d+["']""", re.I)

# The template's graceful else branch when get_option('cd_ppc_form_id') is unset
# (ppc-landing.php line 598). This is the NORMAL state until
# scripts/gf_create_ppc_form.py has been run. The page still weighs more than
# 20,000 bytes and is still noindexed, so nothing else here catches it.
# Matched with the class= prefix so the CSS rule .cd-ppc-form-missing (line 402)
# does not trigger it.
FORM_MISSING_RE = re.compile(r"""class=["']cd-ppc-form-missing["']""", re.I)

MIN_RENDER_BYTES = 20000

PAGES = [
    {
        "slug": "ppc-liquidate-company",
        "title": "Need to Liquidate Your Company? | Company Debt",
        "metadesc": (
            "Speak to a licensed insolvency practitioner about liquidating your "
            "limited company. We explain the process, the cost, and what it means "
            "for you as a director."
        ),
    },
    {
        "slug": "ppc-company-debt",
        "title": "Need to Close a Company That Can't Pay Its Debts? | Company Debt",
        "metadesc": (
            "Your company cannot pay what it owes. Talk to a licensed insolvency "
            "practitioner about closing it properly, the options open to you, and "
            "where your personal risk sits."
        ),
    },
    {
        "slug": "ppc-hmrc-debt",
        "title": "Can't Pay HMRC? | Company Debt",
        "metadesc": (
            "Behind on VAT, PAYE or Corporation Tax? Get advice from a licensed "
            "insolvency practitioner on Time to Pay, enforcement, and what happens "
            "if the arrears keep growing."
        ),
    },
    {
        "slug": "ppc-winding-up-petition",
        "title": "Facing a Winding-Up Petition? | Company Debt",
        "metadesc": (
            "A winding-up petition puts your company days from compulsory "
            "liquidation. Speak to a licensed insolvency practitioner today about "
            "how to stop it and what happens next."
        ),
    },
]

# ---------------------------------------------------------------- transport

PHP_TEMPLATE = """<?php
/**
 * One-shot PPC landing page deployer. Trigger: ?__TRIGGER__=__TOKEN__
 * Finds-or-creates one page, sets template + Yoast meta, drops the Yoast
 * indexable cache row, purges WP Rocket. Self-deletes after run.
 */
if (!isset($_GET['__TRIGGER__']) || $_GET['__TRIGGER__'] !== '__TOKEN__') {
    return;
}

// Belt and braces: if PHP dies with a fatal anywhere below, the shutdown
// handler still removes this file. Without it, a killed client or a fatal
// between the token check and a named exit strands an executing mu-plugin
// on the server. 71 such leftovers were found on 2026-07-29.
register_shutdown_function(function() {
    @unlink(__DIR__ . '/__PAYLOAD__');
    @unlink(__FILE__);
});

add_action('init', function() {
    $payload_path = __DIR__ . '/__PAYLOAD__';
    if (!file_exists($payload_path)) {
        // Self-delete on EVERY exit path. An mu-plugin left on the server runs
        // on every request forever.
        echo 'ERR: payload missing';
        @unlink(__FILE__);
        exit;
    }
    $p = json_decode(file_get_contents($payload_path), true);
    if (!$p || empty($p['slug']) || empty($p['title'])) {
        echo 'ERR: payload invalid';
        @unlink($payload_path);
        @unlink(__FILE__);
        exit;
    }

    wp_set_current_user(1);

    $action = 'found';
    $existing = get_page_by_path($p['slug'], OBJECT, 'page');
    if ($existing) {
        $post_id = (int) $existing->ID;
        // Never duplicate. Only lift a non-public status back to publish.
        if ($existing->post_status !== 'publish') {
            wp_update_post(['ID' => $post_id, 'post_status' => 'publish']);
            $action = 'republished';
        }
    } else {
        $post_id = wp_insert_post([
            'post_type'    => 'page',
            'post_name'    => $p['slug'],
            'post_title'   => $p['title'],
            'post_content' => '',
            'post_status'  => 'publish',
        ], true);
        if (is_wp_error($post_id)) {
            echo 'ERR: ' . $post_id->get_error_message();
            @unlink($payload_path);
            @unlink(__FILE__);
            exit;
        }
        $post_id = (int) $post_id;
        $action = 'created';
    }

    update_post_meta($post_id, '_wp_page_template', $p['template']);
    $done = ['_wp_page_template'];
    foreach ($p['meta'] as $mk => $mv) {
        update_post_meta($post_id, $mk, wp_slash($mv));
        $done[] = $mk;
    }

    // Yoast serves robots/title/description from wp_yoast_indexable at render
    // time, not live from postmeta, and that row does not reliably refresh on
    // a bare update_post_meta(). Drop it so Yoast rebuilds from the postmeta
    // just written. Skipping this is the known "write succeeded, page
    // unchanged" failure.
    $rebuilt = 0;
    global $wpdb;
    $tbl = $wpdb->prefix . 'yoast_indexable';
    if ($wpdb->get_var("SHOW TABLES LIKE '$tbl'") === $tbl) {
        $rebuilt = (int) $wpdb->delete(
            $tbl,
            ['object_id' => $post_id, 'object_type' => 'post'],
            ['%d', '%s']
        );
    }

    $rocket = 'no';
    if (function_exists('rocket_clean_post')) {
        rocket_clean_post($post_id);
        $rocket = 'yes';
    }
    wp_cache_flush();

    echo 'OK: action=' . $action
       . ' post=' . $post_id
       . ' url=' . get_permalink($post_id)
       . ' meta=[' . implode(',', $done) . ']'
       . ' indexable_rows_dropped=' . $rebuilt
       . ' rocket_purged=' . $rocket;

    @unlink($payload_path);
    @unlink(__FILE__);
    exit;
}, 1);
"""


def staging_base() -> str:
    """Return the staging base URL, refusing anything that is not staging."""
    url = os.environ.get("WP_STAGING_URL", "").rstrip("/")
    if not url:
        sys.exit("ERROR: WP_STAGING_URL is not set in .env")
    host = (urlparse(url).hostname or "").lower()
    if host in FORBIDDEN_HOSTS:
        sys.exit(
            "REFUSING TO RUN: " + host + " is the LIVE site. "
            "deploy_ppc_pages.py is staging only."
        )
    if host != STAGING_HOST:
        sys.exit(
            "REFUSING TO RUN: target host is '" + host + "', expected '"
            + STAGING_HOST + "'. deploy_ppc_pages.py is staging only."
        )
    return url


def staging_auth() -> tuple[str, str]:
    user = os.environ.get("WP_BASIC_AUTH_USER", "")
    pw = os.environ.get("WP_BASIC_AUTH_PASS", "")
    if not user or not pw:
        sys.exit("ERROR: WP_BASIC_AUTH_USER / WP_BASIC_AUTH_PASS missing from .env")
    return (user, pw)


def deploy_one(page: dict, base: str, auth: tuple[str, str]) -> dict:
    """Run the one-shot deployer for a single page. Returns a result dict."""
    token = uuid.uuid4().hex[:12]
    trigger = "cdppc"
    php_name = "mu-cd-ppc-" + token + ".php"
    payload_name = "mu-cd-ppc-" + token + ".json"

    payload = {
        "slug": page["slug"],
        "title": page["title"],
        "template": TEMPLATE,
        "meta": {
            "_yoast_wpseo_meta-robots-noindex": "1",
            "_yoast_wpseo_title": page["title"],
            "_yoast_wpseo_metadesc": page["metadesc"],
        },
    }

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

    remote_php = wp_push.REMOTE_DIR + "/" + php_name
    remote_json = wp_push.REMOTE_DIR + "/" + payload_name

    print("  uploading one-shot deployer for /" + page["slug"] + "/ ...")
    wp_push.sftp_put(php_local, remote_php)
    wp_push.sftp_put(json_local, remote_json)

    trigger_url = base + "/?" + trigger + "=" + token
    time.sleep(1)

    # The trigger request and the cleanup MUST be paired. Without the finally,
    # any exception here (timeout, connection reset) skips the SFTP removal and
    # strands an executing mu-plugin on the server permanently.
    status_code = None
    body = ""
    try:
        resp = requests.get(
            trigger_url, auth=auth, headers={"User-Agent": wp_push.BROWSER_UA},
            timeout=120,
        )
        status_code = resp.status_code
        body = resp.text.strip()
        print("  http " + str(status_code) + ": " + body[:300])
    finally:
        php_local.unlink(missing_ok=True)
        json_local.unlink(missing_ok=True)
        try:
            leftover = wp_push.sftp_remove_if_exists([remote_php, remote_json])
            if leftover:
                print("  warning: had to force-remove leftover files: " + str(leftover))
        except Exception as exc:  # noqa: BLE001 - must never mask the real error
            print("  CLEANUP FAILED. Remove these from the server BY HAND: "
                  + remote_php + ", " + remote_json + " (" + str(exc)[:160] + ")")

    if status_code != 200 or not body.startswith("OK:"):
        return {"ok": False, "action": "error", "post_id": None, "raw": body[:300]}

    m_id = re.search(r"post=(\d+)", body)
    m_action = re.search(r"action=(\w+)", body)
    action = m_action.group(1) if m_action else "unknown"
    post_id = int(m_id.group(1)) if m_id else None
    if action == "created":
        print("  CREATED page id " + str(post_id))
    else:
        print("  FOUND existing page id " + str(post_id)
              + " (no duplicate made, action=" + action + ")")
    return {"ok": True, "action": action, "post_id": post_id, "raw": body[:300]}


# ---------------------------------------------------------------- verify

def verify_one(slug: str, base: str, auth: tuple[str, str]) -> dict:
    url = base + "/" + slug + "/"
    res = {
        "slug": slug,
        "url": url,
        "status": None,
        "bytes": 0,
        "http_200": False,
        "noindex": False,
        "template_ok": False,
        "form_ok": False,
        "form_missing_notice": False,
        "body_class": False,
        "size_ok": False,
    }
    try:
        resp = requests.get(
            url, auth=auth, headers={"User-Agent": wp_push.BROWSER_UA},
            timeout=60, allow_redirects=True,
        )
    except requests.RequestException as exc:
        res["error"] = str(exc)[:160]
        return res

    html = resp.text
    res["status"] = resp.status_code
    res["bytes"] = len(resp.content)
    res["http_200"] = resp.status_code == 200
    res["size_ok"] = res["bytes"] > MIN_RENDER_BYTES

    m = re.search(r"<meta[^>]+name=[\"']robots[\"'][^>]*>", html, re.I)
    if m:
        res["noindex"] = "noindex" in m.group(0).lower()
        res["robots_tag"] = m.group(0)[:120]

    # Decisive: markup only ppc-landing.php emits.
    res["template_ok"] = bool(TEMPLATE_MARKER_RE.search(html))

    # Decisive: the enquiry form actually rendered.
    res["form_missing_notice"] = bool(FORM_MISSING_RE.search(html))
    res["form_ok"] = bool(GF_WRAPPER_RE.search(html)) and not res["form_missing_notice"]

    # Secondary only. See BODY_CLASS_CANDIDATES: this is a postmeta echo, not
    # evidence the template file exists on the server.
    m_body = re.search(r"<body[^>]*>", html, re.I)
    if m_body:
        res["body_class"] = any(c in m_body.group(0) for c in BODY_CLASS_CANDIDATES)

    return res


def print_table(rows: list[dict]) -> bool:
    print("")
    print("VERIFY (rendered HTML, not just the response code)")
    print("-" * 104)
    header = (
        "slug".ljust(26) + " " + "200".ljust(5) + " " + "noindex".ljust(9) + " "
        + "template".ljust(10) + " " + "form".ljust(6) + " "
        + "bytes".rjust(9) + "  result"
    )
    print(header)
    print("-" * 104)
    all_pass = True
    for r in rows:
        ok = (
            r["http_200"] and r["noindex"] and r["template_ok"]
            and r["form_ok"] and r["size_ok"]
        )
        all_pass = all_pass and ok
        print(
            r["slug"].ljust(26) + " "
            + ("yes" if r["http_200"] else "NO").ljust(5) + " "
            + ("yes" if r["noindex"] else "NO").ljust(9) + " "
            + ("yes" if r["template_ok"] else "NO").ljust(10) + " "
            + ("yes" if r["form_ok"] else "NO").ljust(6) + " "
            + str(r["bytes"]).rjust(9) + "  "
            + ("PASS" if ok else "FAIL")
        )
        if not ok:
            if not r["http_200"]:
                print("    -> HTTP status " + str(r.get("status")) + " " + str(r.get("error", "")))
            if not r["noindex"]:
                print("    -> robots meta: " + str(r.get("robots_tag", "NOT FOUND in HTML")))
            if not r["template_ok"]:
                print("    -> ppc-landing.php did not render. No 'cd-ppc-styles' block "
                      "and no 'cd-ppc' wrapper in the HTML.")
                print("       Most likely the template file is not on the server yet, so "
                      "WordPress fell back to page.php.")
                if r["body_class"]:
                    print("       NOTE: the page-template body class IS present. That class "
                          "comes from postmeta, not from the file. It is not proof.")
            if not r["form_ok"]:
                if r["form_missing_notice"]:
                    print("    -> the template printed its 'form is not configured' "
                          "placeholder. The option cd_ppc_form_id is unset.")
                    print("       Run scripts/gf_create_ppc_form.py, then set the option. "
                          "See docs/ppc-form-registration.md.")
                else:
                    print("    -> no Gravity Forms wrapper in the HTML. This page captures "
                          "no leads.")
            if not r["size_ok"]:
                print("    -> only " + str(r["bytes"]) + " bytes, under the "
                      + str(MIN_RENDER_BYTES) + " floor "
                      "(this is the truncated-push signature)")
    print("-" * 104)
    print("OVERALL: " + ("PASS" if all_pass else "FAIL"))
    return all_pass


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(
        description="Create and configure the four PPC landing pages on STAGING.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--confirm", action="store_true",
                    help="actually write. Without it the script only prints the plan.")
    ap.add_argument("--dry-run", action="store_true", default=False,
                    help="explicit no-op mode. This is also the default, and it "
                         "OVERRIDES --confirm if both are given.")
    ap.add_argument("--verify-only", action="store_true",
                    help="skip all writes, just re-run the render checks")
    args = ap.parse_args()

    # --dry-run is authoritative. An operator who adds the explicit safety flag
    # must never get a write run, whatever else is on the command line.
    dry_run_won = args.dry_run and args.confirm
    if dry_run_won:
        args.confirm = False

    base = staging_base()
    auth = staging_auth()

    print("target:   " + base + "   (staging)")
    print("template: " + TEMPLATE)
    print("pages:    " + str(len(PAGES)))
    print("")

    if args.verify_only:
        rows = [verify_one(p["slug"], base, auth) for p in PAGES]
        return 0 if print_table(rows) else 1

    if not args.confirm:
        if dry_run_won:
            print("--dry-run OVERRODE --confirm. Nothing will be written.")
            print("Drop --dry-run if you really meant to apply the changes.")
            print("")
        print("DRY RUN - nothing will be written. Re-run with --confirm to apply.")
        print("")
        for p in PAGES:
            print("  /" + p["slug"] + "/")
            print("    title            " + p["title"])
            print("    template         " + TEMPLATE)
            print("    noindex          _yoast_wpseo_meta-robots-noindex = 1")
            print("    meta description " + p["metadesc"])
            print("    then             drop the Yoast indexable row, purge WP Rocket")
            print("    verify           " + base + "/" + p["slug"] + "/")
            print("")
        print("Plan only. No page was created, changed or purged.")
        return 0

    results = []
    for p in PAGES:
        print("/" + p["slug"] + "/")
        results.append(deploy_one(p, base, auth))
        print("")

    failed = [r for r in results if not r["ok"]]
    if failed:
        print("WARNING: " + str(len(failed)) + " page(s) failed to deploy. Verifying anyway.")

    print("waiting 5s for caches to settle before verifying...")
    time.sleep(5)

    rows = [verify_one(p["slug"], base, auth) for p in PAGES]
    ok = print_table(rows)
    if not ok or failed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
