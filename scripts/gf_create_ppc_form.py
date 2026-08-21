"""One-shot: create the "PPC - Request a Confidential Call" Gravity Form.

This is the form used by the new PPC landing pages. It is modelled on form 39
(Book a Free Meeting) but adds a leading "Your situation" radio and a hidden
"Intent" field so we can tell which ad intent page produced the lead.

Mechanics are the same as scripts/gf_create_insolvency_test_form.py: upload a
self-deleting one-shot mu-plugin over SFTP, hit it with a tokenised URL so that
GFAPI is loaded, then confirm the remote file is gone.

Idempotent. If a form with the same title already exists, the script re-uses
that form's id instead of creating a duplicate, and it will still add the
notification and confirmation if they are missing. Safe to run twice.

Staging only. It reads WP_STAGING_URL and refuses to run unless both the HTTP
target and SFTP_HOST resolve to the staging host (see staging_base() and
staging_sftp_host()).

The resulting form id is stored in wp_options['cd_ppc_form_id'] so the landing
page templates can read it rather than hard-coding a number.

AFTER RUNNING THIS: the form id has to be registered in three other places
before the form is fully wired up. See docs/ppc-form-registration.md.

Field ids are pinned. Do not renumber them without updating the landing page
templates and the field maps in mu-plugins/cd-gform-hardening.php.

    1  radio   Your situation    (required)
    2  text    Your name         (required)
    3  phone   Telephone number  (required, international format)
    4  email   Email address     (required)
    5  text    Company name      (optional)
    6  hidden  Intent            (prepopulated from the landing page)
"""
from __future__ import annotations

import os
import pathlib
import sys
import time
import uuid
from urllib.parse import urlparse

import paramiko
import requests

ROOT = pathlib.Path(__file__).resolve().parents[1]
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
from _env import load_env as _load_env
_load_env()

REMOTE_DIR = "wp-content/mu-plugins"
BROWSER_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Staging-only guard. Same shape as scripts/deploy_ppc_pages.py. The docstring
# used to claim there was "no way to target live"; nothing enforced it, and the
# SFTP upload went wherever SFTP_HOST pointed.
STAGING_HOST = "comdebstage.wpengine.com"
STAGING_SFTP_HOST = "comdebstage.sftp.wpengine.com"
FORBIDDEN_HOSTS = {"companydebt.com", "www.companydebt.com"}

FORM_TITLE = "PPC - Request a Confidential Call"
OPTION_KEY = "cd_ppc_form_id"

# Admin recipients. Deliberately no businessexpert.co.uk address: an audit found
# that address does not belong on Company Debt forms. Deliberately no aabrs.com
# address either; AABRS is a separate site and was not asked for here.
ADMIN_RECIPIENTS = "info@companydebt.com,tony@companydebt.com,piers@companydebt.com"

# PHP one-shot. Braces are doubled because this string goes through .format().
PHP = r"""<?php
/** One-shot: create/find the PPC confidential-call GF form. Trigger: ?{trigger}={token}. Self-deletes. */
if (!isset($_GET['{trigger}']) || $_GET['{trigger}'] !== '{token}') {{ return; }}
// Belt and braces: once the correct token has reached this file it must not
// survive the request, even if the work below dies with a fatal error before
// one of the explicit @unlink() calls is reached. Every named exit path below
// unlinks as well; this covers the unnamed ones.
register_shutdown_function(function() {{ @unlink(__FILE__); }});
add_action('init', function() {{
    if (!class_exists('GFAPI')) {{ echo 'ERR: GFAPI missing'; @unlink(__FILE__); exit; }}

    $title       = '{form_title}';
    $option_key  = '{option_key}';
    $admin_to    = '{admin_to}';

    $situation_choices = array(
        array('text' => 'I think the company needs to close',    'value' => 'close'),
        array('text' => "The company can't pay its debts or HMRC", 'value' => 'cantpay'),
        array('text' => 'A creditor is taking legal action',     'value' => 'legal'),
        array('text' => "I'm worried about my personal position", 'value' => 'personal'),
        array('text' => "I'm not sure what to do",               'value' => 'unsure'),
    );

    $fields = array(
        // allowsPrepopulate + inputName are REQUIRED for the landing page's
        // field_values situation=... to preselect a radio choice. Gravity Forms
        // silently ignores a field_values key for any field that has not opted
        // in, so without these two keys the preselection is dead data.
        array(
            'id' => 1, 'type' => 'radio', 'label' => 'Your situation',
            'isRequired' => true, 'choices' => $situation_choices,
            'enableChoiceValue' => true,
            'allowsPrepopulate' => true, 'inputName' => 'situation',
        ),
        array('id' => 2, 'type' => 'text',  'label' => 'Your name',       'isRequired' => true),
        // phoneFormat MUST be 'international'. Gravity Forms defaults a phone
        // field to 'standard', which is US-format validation: it rejects every
        // UK number and the REST error message comes back EMPTY, so the failure
        // looks like nothing at all. Found live on form 46, 2026-08-05.
        array(
            'id' => 3, 'type' => 'phone', 'label' => 'Telephone number',
            'isRequired' => true, 'phoneFormat' => 'international',
        ),
        // A real 'email' field, never 'text'. Forms 41 and 44 declared theirs as
        // text and produced 9-13% unusable addresses, which permanently breaks
        // enhanced conversions in Google Ads.
        array('id' => 4, 'type' => 'email', 'label' => 'Email address', 'isRequired' => true),
        array('id' => 5, 'type' => 'text',  'label' => 'Company name',  'isRequired' => false),
        // Records which ad intent page produced the lead. The landing page sets
        // it with ?intent=... or a hidden input named "intent".
        array(
            'id' => 6, 'type' => 'hidden', 'label' => 'Intent',
            'isRequired' => false, 'allowsPrepopulate' => true, 'inputName' => 'intent',
        ),
    );

    // Confirmation MUST be type 'message', not a redirect. The Google Ads
    // conversion trigger keys off the .gform_confirmation_message_<id> element
    // appearing in place; a redirect never renders it and the conversion is lost.
    $confirmation = array(
        'id'        => 'default',
        'name'      => 'Default confirmation',
        'isDefault' => true,
        'type'      => 'message',
        # Deliberately does NOT name who makes the callback. The first inbound call
        # is handled by an answering service so the practitioners are not pulled off
        # casework (owner, 2026-08-21). Whether a form callback is placed by a
        # practitioner or by the team is unconfirmed, so this claims neither.
        'message'   => '<p>Thank you. We will call you back on the number you gave us to talk through your position. Everything you tell us is confidential and there is no charge for the first conversation.</p>',
        'disableAutoformat' => true,
    );

    $notification_name = 'PPC - admin lead';
    $notification_message = "New PPC enquiry from the paid landing pages.\n\n"
        . "Intent: {{Intent:6}}\n"
        . "Situation: {{Your situation:1}}\n\n"
        . "Name: {{Your name:2}}\n"
        . "Telephone: {{Telephone number:3}}\n"
        . "Email: {{Email address:4}}\n"
        . "Company: {{Company name:5}}\n\n"
        . "Entry: {{entry_id}}\n"
        // date_dmy, not date_mdy: this is a UK site and 09/04/2026 read as
        // 9 April instead of 4 September.
        . "Submitted (site time): {{date_dmy}}\n";
    $notification_spec = array(
        'isActive'  => true,
        'name'      => $notification_name,
        'event'     => 'form_submission',
        'to'        => $admin_to,
        'toType'    => 'email',
        'fromName'  => 'Company Debt Website',
        'from'      => '{{admin_email}}',
        'replyTo'   => '{{Email address:4}}',
        'subject'   => 'PPC lead [{{Intent:6}}] - {{Your situation:1}} - {{Your name:2}}',
        'message'   => $notification_message,
        'disableAutoformat' => false,
    );

    // ---- Idempotent lookup on title -------------------------------------
    $existing_id = 0;
    foreach (GFAPI::get_forms() as $f) {{
        if (isset($f['title']) && $f['title'] === $title) {{ $existing_id = (int) $f['id']; break; }}
    }}

    if ($existing_id) {{
        // Do not touch the fields of a form that already exists; someone may
        // have edited it in wp-admin. Only top up the notification and the
        // confirmation if they went missing.
        $form = GFAPI::get_form($existing_id);
        $changed = false;

        if (empty($form['notifications'])) {{ $form['notifications'] = array(); }}
        $have_notification = false;
        foreach ($form['notifications'] as $n) {{
            if (isset($n['name']) && $n['name'] === $notification_name) {{ $have_notification = true; break; }}
        }}
        if (!$have_notification) {{
            $nid = uniqid('cd_', true);
            $notification_spec['id'] = $nid;
            $form['notifications'][$nid] = $notification_spec;
            $changed = true;
        }}

        if (empty($form['confirmations'])) {{
            $form['confirmations'] = array('default' => $confirmation);
            $changed = true;
        }}

        if ($changed) {{
            $res = GFAPI::update_form($form);
            if (is_wp_error($res)) {{
                echo 'ERR: update failed: ' . $res->get_error_message();
                @unlink(__FILE__);
                exit;
            }}
        }}

        update_option($option_key, $existing_id);
        echo 'OK: existing form_id=' . $existing_id . ' | topped_up=' . ($changed ? 'yes' : 'no');
        @unlink(__FILE__);
        exit;
    }}

    // ---- Fresh create ----------------------------------------------------
    $nid = uniqid('cd_', true);
    $notification_spec['id'] = $nid;

    $form = array(
        'title'          => $title,
        'description'    => 'Callback request used by the PPC landing pages. The hidden Intent field records which ad intent page produced the lead.',
        'labelPlacement'  => 'top_label',
        'button'         => array('type' => 'text', 'text' => 'Request a confidential call'),
        'fields'         => $fields,
        'confirmations'  => array('default' => $confirmation),
        'notifications'  => array($nid => $notification_spec),
        'enableHoneypot' => true,
        'useCurrentUserAsAuthor' => false,
        'nextFieldId'    => 7,
    );

    $new_id = GFAPI::add_form($form);
    if (is_wp_error($new_id)) {{
        echo 'ERR: create failed: ' . $new_id->get_error_message();
        @unlink(__FILE__);
        exit;
    }}
    update_option($option_key, (int) $new_id);
    echo 'OK: created form_id=' . (int) $new_id;
    @unlink(__FILE__);
    exit;
}}, 1);
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
            "gf_create_ppc_form.py is staging only."
        )
    if host != STAGING_HOST:
        sys.exit(
            "REFUSING TO RUN: target host is '" + host + "', expected '"
            + STAGING_HOST + "'. gf_create_ppc_form.py is staging only."
        )
    return url


def staging_sftp_host() -> str:
    """Return SFTP_HOST, refusing anything that is not the staging SFTP host."""
    host = os.environ.get("SFTP_HOST", "").strip().lower()
    if not host:
        sys.exit("ERROR: SFTP_HOST is not set in .env")
    if host != STAGING_SFTP_HOST:
        sys.exit(
            "REFUSING TO RUN: SFTP_HOST is '" + host + "', expected '"
            + STAGING_SFTP_HOST + "'. gf_create_ppc_form.py is staging only."
        )
    return host


def _sftp():
    t = paramiko.Transport((staging_sftp_host(), int(os.environ.get("SFTP_PORT", "2222"))))
    t.connect(username=os.environ["SFTP_USER"], password=os.environ["SFTP_PASS"])
    return t, paramiko.SFTPClient.from_transport(t)


def run() -> bool:
    # Check both targets before anything is written to a server.
    wp_url = staging_base()
    staging_sftp_host()

    token = uuid.uuid4().hex[:12]
    trigger = "cdppcform"
    name = f"mu-cd-gf-create-ppc-form-{token}.php"
    local = ROOT / "tmp" / name
    local.parent.mkdir(exist_ok=True)
    local.write_text(
        PHP.format(
            trigger=trigger,
            token=token,
            form_title=FORM_TITLE,
            option_key=OPTION_KEY,
            admin_to=ADMIN_RECIPIENTS,
        ),
        encoding="utf-8",
    )
    remote = f"{REMOTE_DIR}/{name}"

    t, s = _sftp()
    try:
        s.put(str(local), remote)
    finally:
        s.close(); t.close()

    auth = (os.environ["WP_BASIC_AUTH_USER"], os.environ["WP_BASIC_AUTH_PASS"])
    time.sleep(1)

    # The cleanup MUST run even if the trigger raises. A timeout or a dropped
    # connection used to leave an executing mu-plugin on the server for good.
    resp = None
    try:
        resp = requests.get(f"{wp_url}/?{trigger}={token}", auth=auth,
                            headers={"User-Agent": BROWSER_UA}, timeout=60)
        print(f"http {resp.status_code}: {resp.text[:400]}")
    finally:
        local.unlink(missing_ok=True)
        try:
            t, s = _sftp()
            try:
                try:
                    s.stat(remote); s.remove(remote)
                    print("warning: forced removal of leftover mu-plugin")
                except FileNotFoundError:
                    print("remote cleanup confirmed")
            finally:
                s.close(); t.close()
        except Exception as cleanup_err:  # noqa: BLE001
            print(
                f"CLEANUP FAILED: {cleanup_err}. Remove {remote} by hand, then "
                "run scripts/audit_mu_plugins.py."
            )

    ok = resp is not None and resp.status_code == 200 and resp.text.startswith("OK:")
    if ok:
        print("next: follow the checklist in docs/ppc-form-registration.md")
    return ok


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(0 if run() else 1)
