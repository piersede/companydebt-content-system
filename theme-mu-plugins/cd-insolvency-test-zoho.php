<?php
/**
 * Plugin Name: CD Insolvency Test — Zoho lead push
 * Description: Sends every submission of the Insolvency Test Gravity Form into Zoho CRM as a Lead. Deduplicates on email via Zoho's upsert. Persistent mu-plugin — not a throwaway.
 * Version: 1.1.0
 * Author: Company Debt (Claude)
 *
 * How it works:
 * - Hooks gform_entry_created for the form whose id is stored in
 *   wp_options['cd_insolvency_test_form_id'] (so staging and live can differ).
 * - Reads Zoho creds from wp_options (cd_zoho_client_id, cd_zoho_client_secret,
 *   cd_zoho_refresh_token, cd_zoho_api_domain, cd_zoho_accounts_domain).
 *   Populated by scripts/wp_set_zoho_options.py.
 * - Access token is cached in a transient (55 min TTL vs Zoho's 60 min expiry)
 *   so we don't refresh on every submission.
 * - Uses Zoho's Leads/upsert endpoint with duplicate_check_fields=Email — creates
 *   a new Lead or updates the existing one for that email.
 * - Errors are logged via error_log() and stored in the last-error option
 *   (cd_zoho_last_error) for diagnostics. Never blocks the GF submission.
 * - On failure, sends an alert email to the site admin (throttled to one
 *   per hour via a transient) so silent lead-loss can't run undetected.
 * - Registers /wp-json/cd-itest/v1/abandon to receive abandonment beacons
 *   from the template's pagehide handler.
 */

// gform_entry_created fires ONCE per saved entry, with the full entry array.
// (gform_after_submission fires multiple times from the GF REST /submissions
// endpoint — sometimes with $entry = NULL, sometimes with a partial entry.)
// Using entry_created gives us a consistent, complete payload.
add_action('gform_entry_created', 'cd_itest_zoho_push', 10, 2);

// REST route for the pagehide abandonment beacon. Previously the beacon
// POSTed to a route that didn't exist and hit WP's REST 404 handler.
add_action('rest_api_init', function () {
    register_rest_route('cd-itest/v1', '/abandon', array(
        'methods'             => 'POST',
        'callback'            => 'cd_itest_record_abandonment',
        'permission_callback' => '__return_true',
    ));
});

/**
 * Persist an abandonment event server-side (for visitors whose browsers
 * block dataLayer / GA4). Kept intentionally cheap — writes to a
 * daily-rolling counter option, no per-event DB row.
 */
function cd_itest_record_abandonment($request) {
    $body = $request->get_json_params();
    if (!is_array($body)) $body = array();
    $last_step = isset($body['last_step']) ? sanitize_key((string) $body['last_step']) : 'unknown';
    $reached   = !empty($body['reached_capture']);

    $today = gmdate('Y-m-d');
    $counts = get_option('cd_itest_abandonment_counts', array());
    if (!is_array($counts) || empty($counts['date']) || $counts['date'] !== $today) {
        $counts = array('date' => $today, 'total' => 0, 'by_step' => array(), 'reached_capture' => 0);
    }
    $counts['total']++;
    $counts['by_step'][$last_step] = (isset($counts['by_step'][$last_step]) ? $counts['by_step'][$last_step] : 0) + 1;
    if ($reached) $counts['reached_capture']++;
    update_option('cd_itest_abandonment_counts', $counts, false);
    return new \WP_REST_Response(null, 204);
}

function cd_itest_zoho_push($entry, $form) {
    // Trace every hook invocation so we can tell whether we're being called at
    // all + whether GF is passing a saved entry or a partial stub.
    $trace = array(
        'time'        => time(),
        'form_id'     => is_array($form) ? (int) rgar($form, 'id') : 'not-array',
        'entry_type'  => gettype($entry),
        'entry_id'    => is_array($entry) ? (int) rgar($entry, 'id') : 'not-array',
        'entry_keys'  => is_array($entry) ? implode(',', array_slice(array_keys($entry), 0, 30)) : 'not-array',
        // trim() so a whitespace-only "email" doesn't get counted as present.
        'has_email'   => is_array($entry) ? (bool) trim((string) rgar($entry, '2')) : false,
    );
    update_option('cd_zoho_last_hook_trace', $trace, false);

    $target_id = (int) get_option('cd_insolvency_test_form_id', 0);
    if (!$target_id || (int) $form['id'] !== $target_id) {
        return; // not our form
    }

    // Guard: skip if the entry isn't fully saved yet. GF's REST /submissions
    // endpoint fires gform_after_submission with a partial entry array (no id,
    // no field values) on one internal code path — reload the persisted entry
    // by id from the DB when needed so we always work with real values.
    $entry_id = (int) rgar($entry, 'id');
    if (!$entry_id) {
        cd_itest_zoho_record_error('empty_entry_id', 'Hook fired with empty entry id — skipping', array('trace' => $trace));
        return;
    }
    $fresh = \GFAPI::get_entry($entry_id);
    if (is_array($fresh)) {
        $entry = $fresh;
    }

    try {
        $token = cd_itest_zoho_access_token();
        if (!$token) {
            cd_itest_zoho_record_error('no_access_token', 'Could not obtain Zoho access token');
            return;
        }

        // Extract entry field values by pinned IDs (see gf_create_insolvency_test_form.py).
        $first = trim((string) rgar($entry, '1'));
        $email = trim((string) rgar($entry, '2'));
        $wants_call = trim((string) rgar($entry, '3'));
        $phone = trim((string) rgar($entry, '4'));
        $pref_time = trim((string) rgar($entry, '5'));
        $risk_tier = trim((string) rgar($entry, '6'));
        $quiz_payload = trim((string) rgar($entry, '7'));
        $landing = trim((string) rgar($entry, '8'));
        $referring = trim((string) rgar($entry, '9'));

        if (!$email) {
            cd_itest_zoho_record_error('missing_email', 'Entry has no email; skipping Zoho push', array('entry_id' => $entry_id));
            return;
        }

        // Zoho Lead mandatory Last_Name workaround: split first field on first space
        // if it contains one, else use a sentinel so ops can tell these apart from
        // regular leads.
        $first_name = $first;
        $last_name  = '(Insolvency Test)';
        if (strpos($first, ' ') !== false) {
            $parts = explode(' ', $first, 2);
            $first_name = trim($parts[0]);
            $last_name  = trim($parts[1]) ?: $last_name;
        }

        // Compose description
        $desc = "Source: Insolvency Test (/insolvency-calculator/)\n";
        $desc .= "Risk tier: {$risk_tier}\n";
        $desc .= "Wants call: {$wants_call}\n";
        if ($pref_time) $desc .= "Preferred time: {$pref_time}\n";
        if ($landing)   $desc .= "Landing page: {$landing}\n";
        if ($referring) $desc .= "Referring page: {$referring}\n";
        if ($quiz_payload) {
            $desc .= "\nQuiz payload:\n" . $quiz_payload . "\n";
        }

        $lead = array(
            'First_Name'  => $first_name,
            'Last_Name'   => $last_name,
            'Email'       => $email,
            'Phone'       => $phone,
            'Lead_Source' => 'Insolvency Test',
            'Lead_Status' => 'Not Contacted',
            'Description' => $desc,
        );

        $api_domain = rtrim((string) get_option('cd_zoho_api_domain', 'https://www.zohoapis.com'), '/');
        $url = $api_domain . '/crm/v3/Leads/upsert';

        $body = wp_json_encode(array(
            'data' => array($lead),
            'duplicate_check_fields' => array('Email'),
            'trigger' => array('workflow'), // let Zoho workflows fire on this upsert
        ));

        $resp = wp_remote_post($url, array(
            'timeout' => 20,
            'headers' => array(
                'Authorization' => 'Zoho-oauthtoken ' . $token,
                'Content-Type'  => 'application/json',
                'Accept'        => 'application/json',
            ),
            'body' => $body,
        ));

        if (is_wp_error($resp)) {
            cd_itest_zoho_record_error('http_error', $resp->get_error_message());
            return;
        }
        $code = wp_remote_retrieve_response_code($resp);
        $rbody = wp_remote_retrieve_body($resp);
        if ($code < 200 || $code >= 300) {
            // If token was rejected mid-life (expired despite our TTL), clear the
            // cache so the next attempt re-fetches, then retry once inline.
            if ($code === 401) {
                delete_transient('cd_zoho_access_token');
                $token = cd_itest_zoho_access_token();
                if ($token) {
                    $resp = wp_remote_post($url, array(
                        'timeout' => 20,
                        'headers' => array(
                            'Authorization' => 'Zoho-oauthtoken ' . $token,
                            'Content-Type'  => 'application/json',
                            'Accept'        => 'application/json',
                        ),
                        'body' => $body,
                    ));
                    if (is_wp_error($resp)) {
                        cd_itest_zoho_record_error('retry_http_error', $resp->get_error_message(), array('entry_id' => $entry_id));
                        return;
                    }
                    $code = wp_remote_retrieve_response_code($resp);
                    $rbody = wp_remote_retrieve_body($resp);
                }
            }
            if ($code < 200 || $code >= 300) {
                cd_itest_zoho_record_error('non_2xx', "Zoho returned {$code}", array(
                    'entry_id' => $entry_id,
                    'body'     => substr((string) $rbody, 0, 500),
                ));
                return;
            }
        }

        $decoded = json_decode($rbody, true);
        $zoho_id = '';
        if (is_array($decoded) && !empty($decoded['data'][0]['details']['id'])) {
            $zoho_id = (string) $decoded['data'][0]['details']['id'];
        }

        // Store Zoho lead id back on the GF entry so ops can trace it.
        if ($zoho_id) {
            gform_update_meta($entry['id'], 'cd_zoho_lead_id', $zoho_id);
        }
        update_option('cd_zoho_last_success', array(
            'time'       => time(),
            'entry_id'   => rgar($entry, 'id'),
            'zoho_id'    => $zoho_id,
            'email'      => $email,
            'risk_tier'  => $risk_tier,
        ), false);
    } catch (\Throwable $e) {
        cd_itest_zoho_record_error('exception', $e->getMessage());
    }
}

/**
 * Get a cached-or-refreshed Zoho access token. Returns string or false.
 */
function cd_itest_zoho_access_token() {
    $cached = get_transient('cd_zoho_access_token');
    if ($cached) return $cached;

    $accounts = rtrim((string) get_option('cd_zoho_accounts_domain', 'https://accounts.zoho.com'), '/');
    $client_id = (string) get_option('cd_zoho_client_id', '');
    $client_secret = (string) get_option('cd_zoho_client_secret', '');
    $refresh = (string) get_option('cd_zoho_refresh_token', '');
    if (!$client_id || !$client_secret || !$refresh) return false;

    $resp = wp_remote_post($accounts . '/oauth/v2/token', array(
        'timeout' => 20,
        'body' => array(
            'refresh_token' => $refresh,
            'client_id'     => $client_id,
            'client_secret' => $client_secret,
            'grant_type'    => 'refresh_token',
        ),
    ));
    if (is_wp_error($resp)) {
        cd_itest_zoho_record_error('refresh_wp_err', $resp->get_error_message());
        return false;
    }
    $code = wp_remote_retrieve_response_code($resp);
    $body = wp_remote_retrieve_body($resp);
    $d = json_decode($body, true);
    if ($code >= 200 && $code < 300 && !empty($d['access_token'])) {
        // Zoho tokens live 1h; cache for 55min so we refresh with margin.
        set_transient('cd_zoho_access_token', $d['access_token'], 55 * MINUTE_IN_SECONDS);
        return $d['access_token'];
    }
    cd_itest_zoho_record_error('refresh_failed', "code={$code} body=" . substr((string) $body, 0, 300));
    return false;
}

function cd_itest_zoho_record_error($kind, $message, $extra = array()) {
    $rec = array_merge(array(
        'time'    => time(),
        'kind'    => $kind,
        'message' => $message,
    ), $extra);
    update_option('cd_zoho_last_error', $rec, false);
    error_log('[cd-insolvency-test-zoho] ' . $kind . ': ' . $message);

    // Alert the admin so a silent lead-drop can't run undetected — throttled
    // to one email per hour per error-kind so a persistent outage doesn't
    // spam the inbox.
    $throttle_key = 'cd_zoho_alert_sent__' . md5($kind);
    if (get_transient($throttle_key)) return;
    set_transient($throttle_key, 1, HOUR_IN_SECONDS);

    $to = get_option('admin_email');
    if (!$to) return;
    $site = wp_parse_url(home_url(), PHP_URL_HOST);
    $entry_id = isset($extra['entry_id']) ? (int) $extra['entry_id'] : 0;
    $subject = '[' . $site . '] Insolvency Test → Zoho push failing (' . $kind . ')';
    $body_lines = array(
        'The Insolvency Test capture form is submitting successfully but the Zoho lead push is failing.',
        '',
        'Failure kind: ' . $kind,
        'Message:      ' . $message,
        'Time (UTC):   ' . gmdate('c'),
        'Entry ID:     ' . ($entry_id ?: 'none'),
        '',
        'This alert is throttled to one email per hour per failure kind.',
        'Diagnose via wp_options[cd_zoho_last_error] and the WP error log.',
        'If the credentials are missing, run scripts/wp_set_zoho_options.py against this environment.',
    );
    wp_mail($to, $subject, implode("\n", $body_lines));
}
