<?php
/*
Plugin Name: CD Gravity Forms Hardening
Description: Honeypot enforcement, email + UK phone validation, and outreach-spam blocking
             for the Company Debt contact forms. No database writes: everything here is
             filter-based, so it deploys staging -> live as a file and reverts by deletion.

WHY THIS EXISTS
  Forms 41 and 44 declared Name, Email and Telephone as plain "text" fields, so Gravity
  Forms applied no validation at all. Measured on the newest entries per form:
    form 41  18/200 (9%)  unusable email
    form 44  10/76  (13%) unusable email
  Forms that DO use the typed email field (30, 38, 39, 40) had 0 bad emails in 622
  entries, so field typing is demonstrably the whole story for email.

  Bad emails matter beyond tidiness. cd-livechat-zoho.php only accepts a value
  containing "@", so junk arrives in Zoho with a BLANK email, and the blank then
  defeats the duplicate check so every bot creates a brand new lead. A valid email is
  also required for Google Ads enhanced conversions for leads.

KILL SWITCH
  define('CD_GF_HARDENING_OFF', true);   in wp-config.php disables everything below.
  define('CD_GF_HARDENING_DEBUG', true); logs every block to the PHP error log.
*/

if (!defined('ABSPATH')) exit;
if (defined('CD_GF_HARDENING_OFF') && CD_GF_HARDENING_OFF) return;

/* ---------------------------------------------------------------------------
 * Configuration
 * ------------------------------------------------------------------------ */

// Forms whose honeypot must be on regardless of the stored form setting.
// 30, 41 and 44 had it off; the rest are listed so a future form edit cannot
// silently turn it back off.
function cd_gf_honeypot_forms() {
    return array(6, 29, 30, 31, 38, 39, 40, 41, 44);
}

// form id => field ids holding an email address.
function cd_gf_email_fields() {
    return array(
        29 => array(4),
        30 => array(3),
        31 => array(4),
        38 => array(2),
        39 => array(2),
        40 => array(2),
        41 => array(2),  // declared as "text" in the form config
        44 => array(2),  // declared as "text" in the form config
    );
}

// form id => field ids holding a telephone number.
function cd_gf_phone_fields() {
    return array(
        29 => array(9),   // "text" in the form config
        31 => array(9),   // "text" in the form config
        38 => array(4),
        39 => array(4),
        40 => array(14),
        41 => array(3),   // "text" in the form config, optional
        44 => array(3),   // "text" in the form config, optional
    );
}

// form id => phone field ids that must NOT be compulsory.
//
// CURRENTLY EMPTY BY INSTRUCTION. The phone number stays compulsory on forms
// 29, 31, 38, 39 and 40. To relax it, restore the list below:
//
//     29 => array(9), 31 => array(9), 38 => array(4),
//     39 => array(4), 40 => array(14),
//
// The argument for relaxing it, kept here so the reasoning is not lost:
// insolvency is a distress enquiry, and a director who is frightened or
// worried about what they have already done often wants to open by email. A
// compulsory field does not get a number from that person. It gets a fake one,
// or it loses them. The stored entries show it: a real training company typed
// "0", a genuine hotmail user typed "07", one person typed their own email
// address into the phone box, and a director asking about a dormant company
// typed "111-111-1111".
//
// Note the interaction. Those four got through only because nothing checked
// the value. With the validation above in place and the field still
// compulsory, that escape route is closed, so the combination is stricter than
// this site has ever been. Anyone unwilling to give a real number now has to
// abandon the form. That is a deliberate trade of reach for contactability,
// not an oversight.
function cd_gf_optional_phone_fields() {
    return array();
}

// form id => field ids holding a free-text message, checked for outreach spam.
function cd_gf_message_fields() {
    return array(
        29 => array(7),
        31 => array(7),
        41 => array(4),
    );
}

// Reject a phone number that is neither UK nor explicitly international.
// Set to false to accept any plausible number that carries a "+" country code.
function cd_gf_require_country_code() {
    return apply_filters('cd_gf_require_country_code', true);
}

// Forms where a phone number we cannot read actually STOPS the submission.
//
// What is enforced is the SHAPE of the number, not whether it truly belongs to
// the person. We cannot tell those apart and should not pretend to. So "0",
// "123" and "no thanks" are refused, while a plausible but invented number is
// accepted. Anyone determined to withhold their real number still can; they
// just have to make one up that looks like a phone number. The error message
// even shows them a valid example, which is fine: the point is to stop the box
// being used as a dumping ground, not to interrogate the caller.
//
// The practical gain is that a genuine mistype now gets caught and corrected by
// the person, instead of arriving as an enquiry nobody can ring back.
function cd_gf_phone_blocking_forms() {
    return array(29, 31, 38, 39, 40, 41, 44);
}

function cd_gf_phone_blocks($form_id) {
    return in_array((int) $form_id, cd_gf_phone_blocking_forms(), true);
}

/* ---------------------------------------------------------------------------
 * Honeypot
 * ------------------------------------------------------------------------ */

// Gravity Forms 2.6.5 has no gform_enable_honeypot filter: form_display.php reads
// rgar($form, 'enableHoneypot') directly, and it appends the honeypot field BEFORE
// gform_pre_render runs, so that hook is too late to matter. gform_form_post_get_meta
// fires in GFFormsModel::get_form_meta(), which both the render and the submit path
// go through, so setting the flag there turns the honeypot on for real without
// touching the stored form.
add_filter('gform_form_post_get_meta', function ($form) {
    if (!is_array($form) || !isset($form['id'])) return $form;
    $form_id = (int) $form['id'];

    if (in_array($form_id, cd_gf_honeypot_forms(), true)) {
        $form['enableHoneypot'] = true;
    }

    // Leave the form editor showing the stored setting, so that what an admin
    // sees on screen is the truth about what is saved in the database. Every
    // other context, including the front end and the submit handler, gets the
    // relaxed rule. convert_field_objects() has already run by this point, so
    // the fields are objects rather than arrays.
    $in_form_editor = is_admin() && isset($_GET['page']) && $_GET['page'] === 'gf_edit_forms';
    $optional = cd_gf_optional_phone_fields();
    if (!$in_form_editor && isset($optional[$form_id]) && !empty($form['fields'])) {
        foreach ($form['fields'] as $field) {
            if (!is_object($field) || !in_array((int) $field->id, $optional[$form_id], true)) continue;
            $field->isRequired = false;

            // These fields hide their label, so the placeholder is the only
            // thing the user reads. Forms 29, 31 and 40 spell it "Phone*" and
            // "Your Phone*", which would go on advertising the field as
            // compulsory after it stopped being so. Trade the asterisk for the
            // word, rather than just deleting it and leaving no signal either way.
            $ph = trim((string) $field->placeholder);
            if ($ph !== '' && substr($ph, -1) === '*') {
                $field->placeholder = rtrim(substr($ph, 0, -1)) . ' (optional)';
            }
        }
    }

    return $form;
}, 10, 1);

/* ---------------------------------------------------------------------------
 * Email
 * ------------------------------------------------------------------------ */

function cd_gf_email_is_valid($raw) {
    $v = trim((string) $raw);
    if ($v === '')                                  return 'empty';
    if (preg_match('/\s/', $v))                     return 'space';
    if (!preg_match('/^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$/', $v)) return 'shape';
    if (strpos($v, '..') !== false)                 return 'shape';
    $parts  = explode('@', $v);
    $domain = strtolower(array_pop($parts));
    if (substr($domain, -1) === '.' || $domain[0] === '-') return 'shape';
    if (!function_exists('is_email') || !is_email($v))     return 'shape';
    return '';
}

/* ---------------------------------------------------------------------------
 * Phone
 *
 * normalise() returns array(normalised value, kind) where kind is one of
 * uk | intl | bare | none. "bare" means digits with no leading zero and no
 * country code, which is what nearly all of the junk looks like.
 * ------------------------------------------------------------------------ */

function cd_gf_phone_normalise($raw) {
    $s = trim((string) $raw);
    if ($s === '') return array('', 'none');
    $digits = preg_replace('/\D/', '', $s);
    if ($digits === '') return array('', 'none');

    if (substr($s, 0, 1) === '+') {
        return (substr($digits, 0, 2) === '44')
            ? array('0' . substr($digits, 2), 'uk')
            : array('+' . $digits, 'intl');
    }
    if (substr($digits, 0, 2) === '00') {
        $d = substr($digits, 2);
        return (substr($d, 0, 2) === '44')
            ? array('0' . substr($d, 2), 'uk')
            : array('+' . $d, 'intl');
    }
    if (substr($digits, 0, 2) === '44' && strlen($digits) === 12) {
        return array('0' . substr($digits, 2), 'uk');
    }
    if (substr($digits, 0, 1) === '0') {
        return array($digits, 'uk');
    }
    // A UK mobile typed without its leading zero: 7863348067 -> 07863348067.
    // This is the single most common genuine mistake in the entry history.
    if (strlen($digits) === 10 && substr($digits, 0, 1) === '7') {
        return array('0' . $digits, 'uk');
    }
    return array($digits, 'bare');
}

// Repeated or sequential filler: 077777777777, 1201201200, 123456789.
function cd_gf_phone_is_filler($digits) {
    $core = ltrim($digits, '0');
    if ($core === '' || strlen(count_chars($core, 3)) <= 1) return true;
    foreach (array(2, 3, 4) as $n) {
        if (strlen($core) >= $n * 2) {
            $unit = substr($core, 0, $n);
            if ($core === substr(str_repeat($unit, (int) (strlen($core) / $n) + 1), 0, strlen($core))) {
                return true;
            }
        }
    }
    return in_array($core, array('123456789', '1234567890', '12345678901'), true);
}

// Returns '' when acceptable, otherwise a short reason code.
function cd_gf_phone_is_valid($raw) {
    $v = trim((string) $raw);
    if ($v === '') return '';                       // empty handled by GF's required check

    list($norm, $kind) = cd_gf_phone_normalise($v);
    $digits = preg_replace('/\D/', '', $norm);

    if (strlen($digits) < 9)                 return 'short';
    if (cd_gf_phone_is_filler($digits))      return 'filler';

    if ($kind === 'uk') {
        // Mobiles: 071 to 079, excluding 070 personal numbering, which is
        // almost entirely fraudulent traffic in this form's history.
        if (preg_match('/^07[1-9]\d{8}$/', $norm))                        return '';
        // Landline, non-geographic and freephone ranges.
        if (preg_match('/^0(1\d{8,9}|2\d{9}|3\d{9}|5\d{9}|8\d{8,9}|9\d{9})$/', $norm)) return '';
        return 'uk_shape';
    }
    if ($kind === 'intl') {
        $n = strlen($digits);
        return ($n >= 8 && $n <= 15) ? '' : 'intl_shape';
    }
    return cd_gf_require_country_code() ? 'no_country_code' : '';
}

/* ---------------------------------------------------------------------------
 * Outreach spam
 *
 * The dominant contaminant on form 29 is business to business cold outreach
 * (SEO retainers, guest posts, review selling, "Eric Jones"). It carries a
 * valid email, so it clears the honeypot, reCAPTCHA and the checks above, and
 * lands in Zoho as a real lead.
 *
 * A message is blocked when it carries a pitch signal AND no sign of genuine
 * distress. The distress test runs first and wins, so a director who mentions
 * their own website or a press release is never caught by this.
 *
 * Tuned against the 350 messages held on forms 29, 31 and 41. One signal blocks
 * 31 of them and every one is unambiguous spam: SEO retainers, guest posts,
 * Wikipedia and Trustpilot selling, "Eric Jones", crypto casino text. Zero
 * genuine enquiries were caught. Requiring two signals dropped this to 6, which
 * left most of the spam in place, so one signal is deliberate.
 * ------------------------------------------------------------------------ */

function cd_gf_message_is_spam($raw) {
    $v = strtolower(trim((string) $raw));
    if ($v === '') return false;

    $genuine = '/hmrc|liquidat|insolven|winding|creditor|bounce ?back|administration|'
             . 'struck off|ccj|bailiff|\bvat\b|\bpaye\b|\bcvl\b|\bcva\b|strike off|petition|'
             . 'arrears|\bowe\b|struggling|cash ?flow|redundan|director\b/i';
    if (preg_match($genuine, $v)) return false;

    $pitch = array(
        '/\bseo\b/i', '/guest post/i', '/backlink/i', '/sponsored (post|article)/i',
        '/link building/i', '/search engine ranking/i', '/digital marketing agency/i',
        '/increase (your )?(traffic|visitors|rankings)/i', '/wikipedia page/i',
        '/trustpilot|google reviews/i', '/web ?(design|development) (services|agency)/i',
        '/explainer video/i', '/press release/i', '/\bcrypto\b|bitcoin/i',
        '/website chat assistant/i', '/lead generation (tool|service)/i',
        '/i (just )?visited (your (site|website)|companydebt)/i',
        '/(partnership|collaborat\w+) opportunit/i',
    );
    foreach ($pitch as $re) {
        if (preg_match($re, $v)) return true;
    }
    return false;
}

/* ---------------------------------------------------------------------------
 * Wiring
 * ------------------------------------------------------------------------ */

function cd_gf_log($form_id, $field_id, $reason, $value) {
    if (!defined('CD_GF_HARDENING_DEBUG') || !CD_GF_HARDENING_DEBUG) return;
    error_log(sprintf('[CD-GF] blocked form=%s field=%s reason=%s value=%s',
        $form_id, $field_id, $reason, substr((string) $value, 0, 60)));
}

add_filter('gform_field_validation', function ($result, $value, $form, $field) {
    if (empty($result['is_valid'])) return $result;   // already failing, leave the message alone

    $form_id  = isset($form['id']) ? (int) $form['id'] : 0;
    $field_id = (int) $field->id;
    $raw      = is_array($value) ? implode(' ', $value) : (string) $value;

    $emails = cd_gf_email_fields();
    if (isset($emails[$form_id]) && in_array($field_id, $emails[$form_id], true)) {
        $why = cd_gf_email_is_valid($raw);
        if ($why === 'empty' && empty($field->isRequired)) return $result;
        if ($why !== '') {
            cd_gf_log($form_id, $field_id, 'email:' . $why, $raw);
            $result['is_valid'] = false;
            $result['message']  = ($why === 'space')
                ? 'That email address contains a space. Please remove it, for example name@company.co.uk'
                : 'Please enter a valid email address, for example name@company.co.uk, so we can reply to you.';
            return $result;
        }
    }

    $phones = cd_gf_phone_fields();
    if (cd_gf_phone_blocks($form_id)
        && isset($phones[$form_id]) && in_array($field_id, $phones[$form_id], true)) {
        $why = cd_gf_phone_is_valid($raw);
        if ($why !== '') {
            cd_gf_log($form_id, $field_id, 'phone:' . $why, $raw);
            $result['is_valid'] = false;
            $result['message']  = 'Please enter a UK phone number, for example 07700 900123 or 020 7946 0958. '
                                . 'If you are outside the UK, start with your country code, for example +353 1 234 5678.';
            return $result;
        }
    }

    $messages = cd_gf_message_fields();
    if (isset($messages[$form_id]) && in_array($field_id, $messages[$form_id], true)) {
        if (cd_gf_message_is_spam($raw)) {
            cd_gf_log($form_id, $field_id, 'outreach', $raw);
            $result['is_valid'] = false;
            $result['message']  = 'This form is for company debt and insolvency enquiries only. '
                                . 'For anything else, please email info@companydebt.com';
            return $result;
        }
    }

    return $result;
}, 10, 4);

/* ---------------------------------------------------------------------------
 * Correct the theme's phone rule
 *
 * company-debt-webpigment/functions.php:769 hooks gform_validation and rejects
 * any field labelled or placeheld "Telephone" unless the value starts with one
 * of 020, 0161, 028, 07, 20, 161, 28, 7. That is London, Manchester, Belfast
 * and mobiles only, so every other UK area code is turned away: 0121
 * Birmingham, 0113 Leeds, 0117 Bristol, 0141 Glasgow, 029 Cardiff, and any
 * number entered as +44. It also accepts 070 personal numbering, which is the
 * range the fraudulent traffic actually uses. The only fields carrying that
 * label are forms 41 and 44, the two forms this job is about.
 *
 * The evidence that it is rejecting real people: across 200 entries on form 41
 * not one stored value breaks that rule and not one is a regional landline,
 * while form 29, which the rule does not cover, holds regional landlines
 * normally over the same period. Compliant data with no counterexamples is the
 * signature of a filter at the door, not of how people actually type.
 *
 * gform_validation runs after gform_field_validation, so the theme also
 * overwrites the specific message set above with a bare "Invalid Phone number".
 * Rather than edit a theme file owned by someone else, this re-runs the check
 * at a later priority and restores the correct verdict. Deleting this plugin
 * restores the theme's behaviour exactly.
 * ------------------------------------------------------------------------ */

add_filter('gform_validation', function ($result) {
    if (empty($result['form']['fields'])) return $result;
    $form_id = isset($result['form']['id']) ? (int) $result['form']['id'] : 0;
    $phones  = cd_gf_phone_fields();
    if (!isset($phones[$form_id])) return $result;

    foreach ($result['form']['fields'] as $field) {
        if (!in_array((int) $field->id, $phones[$form_id], true)) continue;

        $value = rgpost('input_' . $field->id);
        $why   = cd_gf_phone_is_valid($value);

        // An empty box must fall through to the clearing branch below, not be
        // skipped. The theme's rule asks whether the value STARTS WITH one of
        // its prefixes, and an empty string starts with none of them, so it
        // fails an empty box too. That has quietly made the "optional"
        // Telephone field on forms 41 and 44 compulsory in practice, and told
        // the visitor "Invalid Phone number" rather than asking for anything.
        // Where the field genuinely is required, Gravity Forms has already set
        // its own "This field is required." message, which we leave alone
        // because we only ever clear the theme's exact wording.

        if ($why === '' || !cd_gf_phone_blocks($form_id)) {
            // Either the number is fine, or this form does not block on the
            // phone at all and the value is whatever the visitor chose to type.
            // Clear a failure only if it is the theme's phone verdict, so bad
            // words and other checks are left intact.
            if (!empty($field->failed_validation)
                && (string) $field->validation_message === 'Invalid Phone number') {
                $field->failed_validation  = false;
                $field->validation_message = '';
            }
        } else {
            $field->failed_validation  = true;
            $field->validation_message = 'Please enter a UK phone number, for example 07700 900123 or '
                . '020 7946 0958. If you are outside the UK, start with your country code, for example '
                . '+353 1 234 5678.';
        }
    }

    // Recompute the overall verdict from what is actually still failing.
    $any = false;
    foreach ($result['form']['fields'] as $field) {
        if (!empty($field->failed_validation)) { $any = true; break; }
    }
    $result['is_valid'] = !$any;
    return $result;
}, 20, 1);

// Store phone numbers in a single consistent format, so the number that reaches
// the entry, the notification email and the Zoho Mobile field is dialable.
add_filter('gform_save_field_value', function ($value, $lead, $field, $form) {
    if (!is_object($field) || !isset($form['id'])) return $value;
    $phones  = cd_gf_phone_fields();
    $form_id = (int) $form['id'];
    if (!isset($phones[$form_id]) || !in_array((int) $field->id, $phones[$form_id], true)) return $value;
    if (trim((string) $value) === '') return $value;

    list($norm, $kind) = cd_gf_phone_normalise($value);
    return ($kind === 'uk' || $kind === 'intl') ? $norm : $value;
}, 10, 4);
