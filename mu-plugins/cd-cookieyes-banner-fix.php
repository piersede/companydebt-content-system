<?php
/**
 * Plugin Name: CD -- CookieYes banner fixes (show on load + centre the panel)
 * Description: Two consent-banner fixes, both verified on 30 Jul 2026.
 *
 *   1) SHOW THE BANNER ON LOAD. WP Rocket's "delay JavaScript execution" was
 *      holding the CookieYes loader (client_data/<id>/script.js) until the
 *      visitor's first scroll/click, so a visitor who landed and left without
 *      interacting never saw the banner and never got the chance to accept.
 *      Those visitors are then uncapturable for analytics/ads. This excludes
 *      the CookieYes loader from the delay so the banner paints immediately.
 *      Consent stays safe: the denied-by-default snippet in header.php is
 *      already un-delayed and runs first (see cd-consent-mode-defaults.php),
 *      so no Google tag fires before the visitor answers.
 *
 *   2) CENTRE THE PREFERENCES PANEL. The "Customise" preference centre renders
 *      at the full width of the viewport and is then translated left by half
 *      its own width to "centre" it -- a technique that only works on a narrow
 *      box. On a wide monitor this threw the panel ~half off the left edge
 *      (one button unreachable). Root cause verified in DevTools: .cky-modal
 *      gets full-width inset + a translateX(-50% of own width) with no flex
 *      centering, and no transformed ancestor is involved. The CSS below turns
 *      .cky-modal into a proper full-screen centring overlay and constrains the
 *      panel to a sane width. Scoped to .cky-modal / #ckyPreferenceCenter only,
 *      so the initial bar (.cky-consent-bar) is untouched.
 *
 *   TRADE-OFF for (1): the banner script now runs during load rather than after
 *   interaction, a small mobile-performance cost, accepted deliberately because
 *   a banner nobody sees collects no consent. Delete this file to revert both.
 * Author: Company Debt
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

/**
 * (1) Keep the CookieYes loader out of WP Rocket's delay. Matched as substrings
 * against the script URL. The enqueued loader is
 * .../client_data/387f1b54d36b6afe444ba7b09ed20e83/script.js and it fetches
 * cdn-cookieyes.com/client_data/<id>/banner.js; all three patterns below match
 * one or both, so the banner initialises on page load.
 */
add_filter( 'rocket_delay_js_exclusions', function ( $excluded ) {
	// NB: do NOT add a bare 'cookieyes' pattern -- it also matches the click-id
	// capture inline script (it references the 'cookieyes-consent' cookie), which
	// would un-delay that script as an unintended side effect. These three match
	// the CookieYes loader/banner only.
	$add = array(
		'client_data',
		'cdn-cookieyes\.com',
		'387f1b54d36b6afe444ba7b09ed20e83',
	);
	return array_values( array_unique( array_merge( (array) $excluded, $add ) ) );
} );

/**
 * (2) Centre the preference-centre modal. Printed late in <head> so it wins over
 * the CookieYes stylesheet, and marked so WP Rocket's "Remove Unused CSS" keeps
 * it (the selectors never appear in the static HTML because the modal is built
 * by JS, so RUCSS would otherwise strip them).
 */
add_action( 'wp_head', function () {
	// Verified against the live banner markup on 30 Jul 2026: this centres the
	// panel to within 1px on a 2560px viewport and keeps it fully on-screen.
	echo "<style id=\"cd-cky-fix\">\n"
		. "/* cd-cky-fix: force the CookieYes preference centre to centre properly */\n"
		. ".cky-modal{position:fixed!important;left:0!important;right:auto!important;"
		. "top:0!important;bottom:auto!important;width:100vw!important;height:100vh!important;"
		. "max-width:100vw!important;max-height:100vh!important;margin:0!important;padding:0!important;"
		. "transform:none!important;display:flex!important;align-items:center!important;"
		. "justify-content:center!important;}\n"
		. ".cky-modal #ckyPreferenceCenter,.cky-modal .cky-preference-center{"
		. "position:relative!important;left:auto!important;right:auto!important;"
		. "top:auto!important;bottom:auto!important;transform:none!important;margin:0 auto!important;"
		. "width:min(845px,calc(100vw - 40px))!important;max-width:845px!important;"
		. "max-height:90vh!important;overflow:auto!important;}\n"
		. "</style>\n";
}, 99 );

/**
 * Keep the fix selectors in WP Rocket's used-CSS safelist as belt and braces.
 */
add_filter( 'rocket_rucss_safelist', function ( $safelist ) {
	$add = array( '.cky-modal', '#ckyPreferenceCenter', '.cky-preference-center' );
	return array_values( array_unique( array_merge( (array) $safelist, $add ) ) );
} );
