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

/*
 * Notification handling for this form now lives in the site-wide
 * cd-gform-notification-fix.php mu-plugin (the same fault turned out to
 * affect the contact forms too). All this plugin does is supply the
 * plain-English answer summary for the email copy of the entry.
 */
add_filter('cd_gfn_entry_for_notification', 'cd_itest_entry_for_notification', 10, 2);
function cd_itest_entry_for_notification($entry, $form) {
    $target_id = (int) get_option('cd_insolvency_test_form_id', 0);
    if (!$target_id || (int) rgar($form, 'id') !== $target_id) {
        return $entry;
    }
    // Swap the raw JSON payload for a readable summary. Affects the EMAIL
    // only — the stored entry and the Zoho push keep the machine-readable
    // JSON (that push runs separately with its own copy of the entry).
    $entry['7'] = cd_itest_humanise_answers(rgar($entry, '7'));
    return $entry;
}

// REST route for the pagehide abandonment beacon. Previously the beacon
// POSTed to a route that didn't exist and hit WP's REST 404 handler.
add_action('rest_api_init', function () {
    register_rest_route('cd-itest/v1', '/abandon', array(
        'methods'             => 'POST',
        'callback'            => 'cd_itest_record_abandonment',
        'permission_callback' => '__return_true',
    ));

    // One-shot bootstrap for the live environment. Runs the DB-side setup
    // the WPE files-only copy can't do: plants Zoho credentials, creates
    // the Gravity Form (idempotent — reuses an existing one with the same
    // title), adds the two notifications, and restores page 53942 to the
    // insolvency-test template. Requires manage_options capability (admin
    // app-password auth). Self-disables via wp_options['cd_itest_bootstrap_done']
    // after first success — no follow-up code removal needed.
    register_rest_route('cd-itest/v1', '/bootstrap', array(
        'methods'             => 'POST',
        'callback'            => 'cd_itest_bootstrap',
        'permission_callback' => function () { return current_user_can('manage_options'); },
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

        // Zoho requires a Last_Name on every Lead. Prefer the optional surname
        // field (10). If it's blank, fall back to splitting the first-name box
        // on a space (people often type a full name there), and only as a last
        // resort use a sentinel — which reads badly on a CRM record
        // ("Karen (Insolvency Test)"), hence the surname field added 2026-08-06.
        $surname    = trim((string) rgar($entry, '10'));
        $first_name = $first;
        $last_name  = '';

        if ($surname !== '') {
            $last_name = $surname;
        } elseif (strpos($first, ' ') !== false) {
            $parts      = explode(' ', $first, 2);
            $first_name = trim($parts[0]);
            $last_name  = trim($parts[1]);
        }
        if ($last_name === '') {
            $last_name = '(no surname given)';
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
 * Turn the stored quiz JSON into a plain-English summary for the internal
 * lead email. Whoever picks up the phone needs to see what the director
 * actually said, not a JSON blob.
 *
 * Falls back to returning the input unchanged if it isn't decodable, so a
 * payload-shape change can never blank the email.
 */
function cd_itest_humanise_answers($json) {
    $raw = trim((string) $json);
    if ($raw === '') return '';
    $d = json_decode($raw, true);
    if (!is_array($d)) return $raw;

    $a = isset($d['answers']) && is_array($d['answers']) ? $d['answers'] : array();

    $cashflow = array(
        'difficulty' => 'Can pay, but only with difficulty',
        'late'       => 'Some payments are already late',
        'cannot'     => 'Cannot pay everything',
        'unsure'     => 'Not sure',
    );
    $warning = array(
        'hmrc_overdue'            => 'HMRC payments overdue',
        'payroll_risk'            => 'Payroll may not be met',
        'supplier_pressure'       => 'Suppliers chasing / reducing credit',
        'bank_limit'              => 'Bank account or overdraft at its limit',
        'personal_funds_reliance' => 'Relying on personal funds',
    );
    $position = array(
        'assets_more' => 'Cash and assets worth more than it owes',
        'about_same'  => 'Cash and assets worth about the same as it owes',
        'debts_more'  => 'Owes more than its cash and assets are worth',
        'unsure'      => 'Not sure',
    );
    $debtrange = array(
        'under10k'  => 'Under £10,000',
        '10-25k'    => '£10,000 – £25,000',
        '25-50k'    => '£25,000 – £50,000',
        '50-100k'   => '£50,000 – £100,000',
        '100-250k'  => '£100,000 – £250,000',
        'over250k'  => 'More than £250,000',
        'unsure'    => 'Not sure',
    );
    $risk = array(
        'personal_guarantee' => 'Has signed a personal guarantee',
        'statutory'          => 'Statutory demand / winding-up petition / enforcement notice received',
        'stopped_trading'    => 'Company has stopped trading',
        'preferential'       => 'Deciding which creditors to pay',
    );

    $map_one = function ($map, $key) {
        if ($key === null || $key === '') return '—';
        return isset($map[$key]) ? $map[$key] : $key;
    };
    $map_many = function ($map, $vals) {
        if (!is_array($vals) || !$vals) return 'None selected';
        $out = array();
        foreach ($vals as $v) $out[] = isset($map[$v]) ? $map[$v] : $v;
        return implode("\n  • ", $out);
    };

    $lines = array();
    $lines[] = 'Can the company pay its bills?  ' . $map_one($cashflow, rgar($a, 'cashflow'));
    $lines[] = '';
    $lines[] = 'Warning signs happening now:';
    $lines[] = '  • ' . $map_many($warning, isset($a['warning']) ? $a['warning'] : array());
    $lines[] = '';
    $lines[] = 'Owns vs owes:  ' . $map_one($position, rgar($a, 'position'));
    if (!empty($a['debtRange'])) {
        $lines[] = 'Roughly owed in total:  ' . $map_one($debtrange, $a['debtRange']);
    }
    $lines[] = '';
    $lines[] = 'Risk factors:';
    $lines[] = '  • ' . $map_many($risk, isset($a['risk']) ? $a['risk'] : array());

    if (isset($d['score'])) {
        $lines[] = '';
        $lines[] = 'Score: ' . (int) $d['score'] . (!empty($d['forceUrgent']) ? ' (urgent trigger fired)' : '');
    }
    if (!empty($d['duration_ms'])) {
        $lines[] = 'Time taken: ' . max(1, (int) round(((int) $d['duration_ms']) / 1000)) . ' seconds';
    }

    return implode("\n", $lines);
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

/**
 * One-shot bootstrap endpoint. Idempotent, self-disabling. Called once
 * against live from scripts/live_bootstrap_insolvency_test.py after the
 * WPE files-only copy runs. Auth via admin app-password (manage_options
 * capability). Body: { zoho: { client_id, client_secret, refresh_token,
 * api_domain, accounts_domain } }. Returns per-step status.
 */
function cd_itest_bootstrap($request) {
    $steps = array();
    $body  = $request->get_json_params();
    if (!is_array($body)) $body = array();
    $zoho  = isset($body['zoho']) && is_array($body['zoho']) ? $body['zoho'] : array();

    $done_before = (bool) get_option('cd_itest_bootstrap_done');

    // If the full bootstrap has already run, only the Zoho-credentials step
    // may be re-executed as a top-up (in case the first bootstrap POST was
    // sent with an empty zoho payload). Everything else is refused via 409
    // to keep the endpoint from reconfiguring form/notifications/page later.
    $zoho_only = $done_before;

    // Step 1: Zoho credentials (only set the ones supplied AND currently empty).
    $zoho_keys = array(
        'client_id'       => 'cd_zoho_client_id',
        'client_secret'   => 'cd_zoho_client_secret',
        'refresh_token'   => 'cd_zoho_refresh_token',
        'api_domain'      => 'cd_zoho_api_domain',
        'accounts_domain' => 'cd_zoho_accounts_domain',
    );
    $zoho_set = 0; $zoho_skipped = 0;
    foreach ($zoho_keys as $body_key => $opt_key) {
        if (empty($zoho[$body_key])) { $zoho_skipped++; continue; }
        if (get_option($opt_key)) { $zoho_skipped++; continue; }
        update_option($opt_key, (string) $zoho[$body_key], false);
        $zoho_set++;
    }
    $steps['zoho_options'] = "set={$zoho_set} skipped={$zoho_skipped}";

    // Top-up mode: bootstrap has already run, we only touched Zoho options,
    // return early without re-touching form/notifications/page.
    if ($zoho_only) {
        return new \WP_REST_Response(array(
            'ok'    => true,
            'mode'  => 'zoho-topup',
            'steps' => $steps,
        ), 200);
    }

    if (!class_exists('GFAPI')) {
        $steps['gf_form']       = 'error: GFAPI missing';
        $steps['notifications'] = 'skipped';
        $steps['page_53942']    = 'skipped';
        return new \WP_REST_Response(array('ok' => false, 'steps' => $steps), 500);
    }

    // Step 2: create the Insolvency Test form if it doesn't already exist.
    $form_id = (int) get_option('cd_insolvency_test_form_id', 0);
    if (!$form_id) {
        // Look for an existing form with the same title before creating a
        // duplicate (mirrors gf_create_insolvency_test_form.py behaviour).
        $existing_id = 0;
        foreach (\GFAPI::get_forms() as $f) {
            if (isset($f['title']) && $f['title'] === 'Insolvency Test') {
                $existing_id = (int) $f['id']; break;
            }
        }
        if ($existing_id) {
            $form_id = $existing_id;
            update_option('cd_insolvency_test_form_id', $form_id);
            $steps['gf_form'] = "existing:{$form_id}";
        } else {
            $spec = array(
                'title'          => 'Insolvency Test',
                'description'    => 'Capture step for the multi-step insolvency test at /insolvency-calculator/. Do not add fields here without updating the template.',
                'labelPlacement' => 'top_label',
                'button'         => array('type' => 'text', 'text' => 'Submit'),
                'fields' => array(
                    array('id' => 1, 'type' => 'text',     'label' => 'First name',     'isRequired' => true),
                    array('id' => 2, 'type' => 'email',    'label' => 'Email',          'isRequired' => true),
                    array('id' => 3, 'type' => 'radio',    'label' => 'Wants call',     'isRequired' => true,
                          'choices' => array(
                              array('text' => 'Yes', 'value' => 'yes'),
                              array('text' => 'No',  'value' => 'no'),
                          )),
                    // phoneFormat MUST be 'international' — GF defaults phone
                    // fields to 'standard', which is US-format validation and
                    // rejects every UK number (found live 2026-08-05: it was
                    // silently blocking every "Yes, please call me" submission).
                    array('id' => 4, 'type' => 'phone',    'label' => 'Phone',          'isRequired' => false, 'phoneFormat' => 'international'),
                    array('id' => 5, 'type' => 'text',     'label' => 'Preferred time', 'isRequired' => false),
                    array('id' => 6, 'type' => 'text',     'label' => 'Risk tier',      'isRequired' => false),
                    array('id' => 7, 'type' => 'textarea', 'label' => 'Quiz payload',   'isRequired' => false),
                    array('id' => 8, 'type' => 'text',     'label' => 'Landing page',   'isRequired' => false),
                    array('id' => 9, 'type' => 'text',     'label' => 'Referring page', 'isRequired' => false),
                    array('id' => 10, 'type' => 'text',    'label' => 'Last name',      'isRequired' => false),
                ),
                'confirmations' => array(
                    'default' => array(
                        'id' => 'default', 'name' => 'Default confirmation', 'isDefault' => true,
                        'type' => 'message', 'message' => 'Received.', 'disableAutoformat' => true,
                    ),
                ),
                'notifications' => array(),
                'useCurrentUserAsAuthor' => false,
                'nextFieldId'   => 11,
            );
            $new_id = \GFAPI::add_form($spec);
            if (is_wp_error($new_id)) {
                $steps['gf_form'] = 'error: ' . $new_id->get_error_message();
            } else {
                $form_id = (int) $new_id;
                update_option('cd_insolvency_test_form_id', $form_id);
                $steps['gf_form'] = "created:{$form_id}";
            }
        }
    } else {
        $steps['gf_form'] = "existing:{$form_id}";
    }

    // Step 3: notifications (idempotent — add-if-missing by name).
    $notif_added_internal = false;
    $notif_added_visitor  = false;
    if ($form_id) {
        $form = \GFAPI::get_form($form_id);
        if (is_array($form)) {
            // Discover the internal recipient from form 38 (the old calc) so
            // leads land in the same inbox with no manual reconfiguration.
            $internal_to = '';
            $form38 = \GFAPI::get_form(38);
            if ($form38 && !empty($form38['notifications'])) {
                foreach ($form38['notifications'] as $n) {
                    if (!empty($n['to']) && filter_var(explode(',', $n['to'])[0], FILTER_VALIDATE_EMAIL)) {
                        $internal_to = $n['to']; break;
                    }
                }
            }
            if (!$internal_to) $internal_to = get_option('admin_email');

            if (empty($form['notifications'])) $form['notifications'] = array();
            $has_named = function ($form, $name) {
                foreach ($form['notifications'] as $n) if (isset($n['name']) && $n['name'] === $name) return true;
                return false;
            };

            if (!$has_named($form, 'Insolvency Test — internal lead')) {
                $id = uniqid('cd_', true);
                $form['notifications'][$id] = array(
                    'id' => $id, 'name' => 'Insolvency Test — internal lead', 'event' => 'form_submission', 'isActive' => true, 'service' => 'wordpress',
                    'to' => $internal_to, 'fromName' => 'Company Debt Website', 'from' => '{admin_email}',
                    'subject' => 'Insolvency Test lead — {Risk tier:6} — {First name:1}',
                    'message' => "New Insolvency Test lead received.\n\nRisk tier: {Risk tier:6}\nWants call: {Wants call:3}\nPreferred time: {Preferred time:5}\n\nName: {First name:1}\nEmail: {Email:2}\nPhone: {Phone:4}\n\nLanding page: {Landing page:8}\nReferring page: {Referring page:9}\n\nQuiz payload (JSON):\n{Quiz payload:7}\n",
                    'disableAutoformat' => false,
                );
                $notif_added_internal = true;
            }
            if (!$has_named($form, 'Insolvency Test — visitor result')) {
                $id = uniqid('cd_', true);
                $form['notifications'][$id] = array(
                    'id' => $id, 'name' => 'Insolvency Test — visitor result', 'event' => 'form_submission', 'isActive' => true, 'service' => 'wordpress',
                    'toType' => 'field', 'to' => '2',
                    'fromName' => 'Company Debt', 'from' => 'info@companydebt.com',
                    'subject' => 'Your Insolvency Test result — {Risk tier:6}',
                    'message' => "Hi {First name:1},\n\nThank you for completing our Insolvency Test. Based on your answers, the initial result is:\n\n**{Risk tier:6}**\n\nThis is an initial guidance result, not a formal insolvency opinion. If you have any questions or would like to talk through your position, you can reach a member of our team on 0800 074 6757 or reply to this email.\n\nWarm regards,\nCompany Debt\nLicensed Insolvency Practitioners\nhttps://www.companydebt.com\n",
                    'disableAutoformat' => false,
                );
                $notif_added_visitor = true;
            }
            if ($notif_added_internal || $notif_added_visitor) {
                $res = \GFAPI::update_form($form);
                if (is_wp_error($res)) {
                    $steps['notifications'] = 'error: ' . $res->get_error_message();
                } else {
                    $steps['notifications'] = 'added: '
                        . ($notif_added_internal ? 'internal ' : '')
                        . ($notif_added_visitor  ? 'visitor'   : '');
                }
            } else {
                $steps['notifications'] = 'existing';
            }
        }
    } else {
        $steps['notifications'] = 'skipped (no form id)';
    }

    // Step 4: restore page 53942 to the insolvency-test template.
    $page_id = 53942;
    $post = get_post($page_id);
    if (!$post) {
        $steps['page_53942'] = 'error: page missing';
    } else {
        $tpl_now = get_post_meta($page_id, '_wp_page_template', true);
        if ($tpl_now === 'templates/insolvency-test.php') {
            $steps['page_53942'] = 'already-on-template';
        } else {
            update_post_meta($page_id, '_wp_page_template', 'templates/insolvency-test.php');
            $res = wp_update_post(array(
                'ID'           => $page_id,
                'post_content' => '<!-- Insolvency Test — content rendered by templates/insolvency-test.php -->',
                'post_status'  => 'publish',
            ), true);
            if (is_wp_error($res)) {
                $steps['page_53942'] = 'error: ' . $res->get_error_message();
            } else {
                clean_post_cache($page_id);
                if (function_exists('rocket_clean_post'))   { rocket_clean_post($page_id); }
                if (function_exists('rocket_clean_domain')) { rocket_clean_domain(); }
                if (class_exists('WpeCommon')) {
                    if (method_exists('WpeCommon', 'purge_memcached'))     WpeCommon::purge_memcached();
                    if (method_exists('WpeCommon', 'purge_varnish_cache')) WpeCommon::purge_varnish_cache();
                }
                $steps['page_53942'] = "updated (was: {$tpl_now})";
            }
        }
    }

    update_option('cd_itest_bootstrap_done', array('time' => time(), 'steps' => $steps), false);
    return new \WP_REST_Response(array('ok' => true, 'steps' => $steps), 200);
}
