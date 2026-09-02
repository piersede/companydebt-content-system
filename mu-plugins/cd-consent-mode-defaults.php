<?php
/* Plugin Name: CD Consent Mode defaults - keep the pre-GTM snippet un-delayed
 *
 * Context (29 Jul 2026)
 * --------------------
 * The Consent Mode v2 *default* snippet lives in the theme header.php, directly
 * above the GTM container snippet, because GTM is printed before wp_head() and
 * therefore no WordPress hook can get in front of it.
 *
 * The danger is WP Rocket. Its "delay JavaScript execution" feature rewrites
 * inline scripts to type="text/rocketlazyloadscript" and holds them until the
 * first user interaction. That already happens to the cd-livechat-zoho.php
 * inline script on this site. A *delayed* consent default is not a consent
 * default at all - the Google tags would initialise with no consent state and
 * write _ga / _gcl_* cookies before the visitor has answered the banner. That
 * is precisely the failure observed on 29 Jul 2026.
 *
 * So: this file does one job - tell WP Rocket to leave that snippet alone.
 * The marker string 'cd-consent-default' appears in a comment inside the
 * snippet purely so these filters have something stable to match on.
 *
 * Verify after deploying (do NOT trust a 200):
 *   1. View source. The snippet must render with NO type attribute, or
 *      type="text/javascript" - never type="text/rocketlazyloadscript".
 *   2. In the browser console on a clean profile, before touching the banner:
 *        window.cdConsentDefaultApplied            -> true
 *        google_tag_data.ics.usedDefault           -> true
 *        google_tag_data.ics.wasSetLate            -> false
 *        google_tag_data.ics.entries.ad_storage    -> default:false
 *
 *      Do NOT check `implicit` on those entries. It reads true on a correctly
 *      working page (verified on live 2026-09-02, with the default sitting as
 *      dataLayer entry 0 and every Google ping carrying gcs=G100). The flags
 *      that actually catch a missing or late default are usedDefault and
 *      wasSetLate. The July 2026 audit read `implicit` as proof the default was
 *      absent; that was true then only because usedDefault was false too.
 *        document.cookie                           -> no _ga, no _gcl_*
 */
if (!defined('ABSPATH')) exit;

/* Keep the consent default out of WP Rocket's "delay JS execution". */
add_filter('rocket_delay_js_exclusions', function ($excluded) {
    $excluded = is_array($excluded) ? $excluded : array();
    $excluded[] = 'cd-consent-default';
    return array_values(array_unique($excluded));
});

/* Belt and braces: keep it out of inline-JS minification/combination too, so the
   marker comment the filter above matches on cannot be stripped out. */
add_filter('rocket_excluded_inline_js_content', function ($excluded) {
    $excluded = is_array($excluded) ? $excluded : array();
    $excluded[] = 'cd-consent-default';
    return array_values(array_unique($excluded));
});
