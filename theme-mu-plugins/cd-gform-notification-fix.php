<?php
/**
 * Plugin Name: CD Gravity Forms — notification entry fix
 * Description: Sends Gravity Forms notifications from a hook where the saved entry is readable, so merge tags stop rendering empty. Falls back to Gravity Forms' own send if ours fails.
 * Version: 1.0.0
 * Author: Company Debt (Claude)
 *
 * THE PROBLEM
 * -----------
 * Notification emails arrive with the boilerplate text present but every
 * entry-level merge tag empty — {all_fields}, {Name:1}, {entry_id} and so on.
 * Form-level tags ({form_title}, {admin_email}) resolve fine. The entry itself
 * is saved correctly and shows all its values in wp-admin.
 *
 * Confirmed on form 46 (Insolvency Test) 2026-08-05 and form 29 (Contact Us)
 * 2026-08-06. Both send their real emails empty, yet firing the very same
 * notification on the very same stored entry via
 * POST /wp-json/gf/v2/entries/{id}/notifications renders perfectly. The entry,
 * the form config and the merge-tag syntax are therefore all fine — only the
 * entry context GF hands to its own send is broken.
 *
 * WHAT DOESN'T FIX IT (tried on form 46, all ineffective)
 * -------------------------------------------------------
 * - gform_is_asynchronous_notifications_enabled_{id} => false
 * - Rehydrating the entry at gform_entry_post_save
 * - Pre-resolving merge tags in a gform_notification filter
 *   (runs too late — the entry context has already gone)
 * - Setting the notification's 'service' key to 'wordpress'
 *
 * WHAT DOES
 * ---------
 * Take ownership of the send: reload the entry from the database and call
 * GFAPI::send_notifications() ourselves, then suppress GF's own attempt.
 *
 * THE SAFETY NET
 * --------------
 * These are the site's main lead emails, so a failure here must never mean
 * NO email. gform_entry_created runs BEFORE GF's own notification send, so:
 *   1. we send first and record success against the entry id;
 *   2. the suppression filter only suppresses when that record exists.
 * If our send throws or the entry can't be reloaded, nothing is suppressed and
 * GF's native send proceeds exactly as it does today. Worst case is therefore
 * the current behaviour, never silence.
 */

if (!defined('ABSPATH')) { exit; }

/**
 * Forms whose notifications this plugin owns. Explicit list rather than
 * "all forms" so the blast radius is reviewable. Adjust via the filter.
 */
function cd_gfn_owned_form_ids() {
    $ids = array(
        6,   // Feedback Form
        29,  // Contact Us - Our Advisors are Here to Get You Started
        30,  // Download Stressed Directors Guide
        31,  // Sectors Contact Form
        39,  // Book a Free Meeting
        40,  // Quick Quote
        41,  // Contact Us
        44,  // Home Page - Contact Block
        46,  // Insolvency Test
    );
    return apply_filters('cd_gfn_owned_form_ids', $ids);
}

function cd_gfn_owns_form($form) {
    $id = (int) rgar($form, 'id');
    return $id && in_array($id, cd_gfn_owned_form_ids(), true);
}

// Entry ids whose notifications we have successfully sent ourselves.
$GLOBALS['cd_gfn_sent_ok']    = array();
// True only while our own GFAPI::send_notifications() call is in flight.
$GLOBALS['cd_gfn_in_our_send'] = false;

/**
 * Send the notifications ourselves, with an entry freshly loaded from the DB.
 * Priority 5 so this runs before other integrations that might modify state.
 */
add_action('gform_entry_created', 'cd_gfn_send_notifications', 5, 2);
function cd_gfn_send_notifications($entry, $form) {
    if (!cd_gfn_owns_form($form)) return;
    if (!class_exists('GFAPI')) return;

    $entry_id = absint(rgar($entry, 'id'));
    if (!$entry_id) return;   // no id → don't suppress, let GF handle it

    $fresh = \GFAPI::get_entry($entry_id);
    if (is_wp_error($fresh) || !is_array($fresh)) return;  // → GF handles it

    /**
     * Lets other plugins adjust the entry used for the EMAIL only (the stored
     * entry is untouched). The Insolvency Test uses this to swap its raw JSON
     * payload for a plain-English summary.
     */
    $fresh = apply_filters('cd_gfn_entry_for_notification', $fresh, $form);

    $GLOBALS['cd_gfn_in_our_send'] = true;
    try {
        \GFAPI::send_notifications($form, $fresh, 'form_submission');
        // Only now is it safe to suppress GF's own attempt.
        $GLOBALS['cd_gfn_sent_ok'][$entry_id] = true;
        if (class_exists('GFCommon')) {
            \GFCommon::log_debug("[cd-gfn] sent notifications for entry {$entry_id} (form " . rgar($form, 'id') . ')');
        }
    } catch (\Throwable $e) {
        // Deliberately do NOT record success — GF's native send will run.
        error_log('[cd-gform-notification-fix] send failed for entry ' . $entry_id . ': ' . $e->getMessage());
        update_option('cd_gfn_last_error', array(
            'time' => time(), 'entry_id' => $entry_id,
            'form_id' => (int) rgar($form, 'id'), 'message' => $e->getMessage(),
        ), false);
    } finally {
        $GLOBALS['cd_gfn_in_our_send'] = false;
    }
}

/**
 * Suppress GF's own send — but ONLY for an entry we have already emailed
 * ourselves. Any other case falls through untouched.
 */
add_filter('gform_disable_notification', 'cd_gfn_suppress_native', PHP_INT_MAX, 5);
function cd_gfn_suppress_native($is_disabled, $notification, $form, $entry, $data = array()) {
    if (!empty($GLOBALS['cd_gfn_in_our_send'])) {
        return $is_disabled;               // our own send — let it through
    }
    if (!cd_gfn_owns_form($form)) {
        return $is_disabled;               // not ours
    }
    $entry_id = is_array($entry) ? absint(rgar($entry, 'id')) : 0;
    if ($entry_id && !empty($GLOBALS['cd_gfn_sent_ok'][$entry_id])) {
        return true;                       // already emailed — suppress the duplicate
    }
    return $is_disabled;                   // we didn't send → let GF try
}
