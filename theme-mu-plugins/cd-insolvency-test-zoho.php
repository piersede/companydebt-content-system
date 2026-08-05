<?php
/**
 * Plugin Name: CD Insolvency Test — Zoho lead push
 * Description: Sends every submission of the Insolvency Test Gravity Form into Zoho CRM as a Lead. Deduplicates on email via Zoho's upsert. Persistent mu-plugin — not a throwaway.
 * Version: 1.0.0
 * Author: Company Debt (Claude)
 *
 * How it works:
 * - Hooks gform_after_submission_<form_id> where <form_id> is read from
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
 */

// gform_entry_created fires ONCE per saved entry, with the full entry array.
// (gform_after_submission fires multiple times from the GF REST /submissions
// endpoint — sometimes with $entry = NULL, sometimes with a partial entry.)
// Using entry_created gives us a consistent, complete payload.
add_action('gform_entry_created', 'cd_itest_zoho_push', 10, 2);

function cd_itest_zoho_push($entry, $form) {
    // Trace every hook invocation so we can tell whether we're being called at
    // all + whether GF is passing a saved entry or a partial stub.
    $trace = array(
        'time'        => time(),
        'form_id'     => is_array($form) ? (int) rgar($form, 'id') : 'not-array',
        'entry_type'  => gettype($entry),
        'entry_id'    => is_array($entry) ? (int) rgar($entry, 'id') : 'not-array',
        'entry_keys'  => is_array($entry) ? implode(',', array_slice(array_keys($entry), 0, 30)) : 'not-array',
        'has_email'   => is_array($entry) ? (bool) rgar($entry, '2') : false,
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
                    $code = wp_remote_retrieve_response_code($resp);
                    $rbody = wp_remote_retrieve_body($resp);
                }
            }
            if ($code < 200 || $code >= 300) {
                cd_itest_zoho_record_error('non_2xx', "Zoho returned {$code}", array('body' => substr((string) $rbody, 0, 500)));
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
}
