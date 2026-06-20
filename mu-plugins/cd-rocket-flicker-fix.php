<?php
/**
 * Plugin Name: CD -- v2 redesign render fixes (no-flicker)
 * Description: Two jobs, both to kill the v1->v2 "flicker" caused by WP Rocket
 *   delaying the v2 feature-flag/render scripts until first interaction:
 *   1) SERVER-RENDER the Free Insolvency Test sidebar widget (#block-20) as the
 *      v2 ".cd-itest" layout, so it is baked into the (cached) HTML on first
 *      paint instead of being rewritten by delayed JS. Retires data-insolvency-v2.
 *   2) Keep the remaining early flag script un-delayed + header CSS safelisted so
 *      the still-flag-gated bits (footer v2, topnav logo/phone, reviews-hide,
 *      toc-sidebar, narrow-sidebar) apply on load, not on interaction.
 *   Added 2026-06-20. Remove this file to revert (the original v1 widget HTML and
 *   the footer JS path are untouched).
 * Author: Company Debt
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

/**
 * 1) Server-render the Free Insolvency Test widget (#block-20).
 *
 * The widget is a Block widget whose v1 content carries the distinctive
 * ".content-cd-list-with-button" class (unique to this widget site-wide). We
 * swap that inner block HTML for the v2 ".cd-itest" tree -- the exact markup the
 * old footer.php "cd-insolvency-widget-v2" script used to build client-side.
 * Because this runs server-side it lands in the WP Rocket cache: no JS, no
 * data-insolvency-v2 flag, no visibility:hidden reveal-gate.
 *
 * The CTA href is preserved from the original widget (falls back to the
 * canonical test URL), matching the old JS behaviour.
 */
function cd_itest_v2_markup( $href ) {
	$ico_check  = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="5 12 10 17 19 7"/></svg>';
	$ico_lock   = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>';
	$ico_shield = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l8 4v6c0 5-3.5 9-8 10-4.5-1-8-5-8-10V6l8-4z"/><polyline points="9 12 11 14 15 10"/></svg>';
	$ico_arrow  = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="13 6 19 12 13 18"/></svg>';

	$benefit = function ( $title, $sub ) use ( $ico_check ) {
		return '<li><span class="cd-itest__check">' . $ico_check . '</span>'
			. '<span class="cd-itest__benefit-body">'
			. '<span class="cd-itest__benefit-title">' . esc_html( $title ) . '</span>'
			. '<span class="cd-itest__benefit-sub">' . esc_html( $sub ) . '</span>'
			. '</span></li>';
	};
	$trust = function ( $icon, $text ) {
		return '<li><span class="cd-itest__trust-icon">' . $icon . '</span>' . esc_html( $text ) . '</li>';
	};

	return '<div class="cd-itest">'
		. '<div class="cd-itest__eyebrow">30-SECOND TEST</div>'
		. '<div class="cd-itest__headline">Is Your Company Insolvent?</div>'
		. '<p class="cd-itest__subhead">Answer 5 quick questions and get an instant assessment.</p>'
		. '<div class="cd-itest__mockup" role="img" aria-label="Insolvency test preview"></div>'
		. '<ul class="cd-itest__benefits">'
			. $benefit( 'Instant assessment', 'See your result immediately' )
			. $benefit( 'Recommended next steps', 'Clear guidance tailored to you' )
			. $benefit( 'Free expert guidance', 'Speak to our specialists' )
		. '</ul>'
		. '<a class="cd-itest__cta" href="' . esc_url( $href ) . '"><span>Start the 30-Second Test</span>'
			. '<span class="cd-itest__cta-arrow">' . $ico_arrow . '</span></a>'
		. '<ul class="cd-itest__trust">'
			. $trust( $ico_lock, 'No signup required' )
			. $trust( $ico_shield, '100% confidential' )
		. '</ul>'
		. '</div>';
}

add_filter( 'widget_block_content', function ( $content ) {
	// Only the insolvency-test widget carries this class.
	if ( false === strpos( $content, 'content-cd-list-with-button' ) ) {
		return $content;
	}
	$href = '/insolvency-calculator/';
	if ( preg_match( '/href="([^"]+)"/', $content, $m ) ) {
		$href = $m[1];
	}
	return cd_itest_v2_markup( $href );
}, 10, 1 );

/**
 * 2) Do NOT delay the early flag-setter (sets the still-active flags before
 *    <body>) and the topnav v2 logo/phone script. Without this WP Rocket holds
 *    them to first interaction and the still-flagged bits flicker. The
 *    de-flagged subsystems (topnav colours, sticky nav, licensed + insolvency
 *    widgets) no longer rely on these, so only the genuinely-still-flagged
 *    scripts remain excluded.
 */
add_filter( 'rocket_delay_js_exclusions', function ( $excluded ) {
	$add = array(
		'cd-v2-flags-early',
		'cd-topnav-v2-flag',
		'cd-topnav-phone-icon',
		// content-based fallback for the early flag-setter
		"setAttribute\('data-topnav-v2'",
	);
	return array_values( array_unique( array_merge( (array) $excluded, $add ) ) );
} );

/**
 * 3) Keep the header / primary-nav styling in WP Rocket's "used" CSS so it is
 *    not stripped as unused (which left the header unstyled until interaction).
 *    These selectors are now unconditional (de-flagged), so they must survive
 *    Remove Unused CSS.
 */
add_filter( 'rocket_rucss_safelist', function ( $safelist ) {
	$add = array(
		'header',
		'.site-header',
		'#masthead',
		'.main-navigation',
		'.menu-header-menu-container',
		'.sub-menu',
		'.custom-logo',
		'.custom-logo-link',
		'.header-phone',
	);
	return array_values( array_unique( array_merge( (array) $safelist, $add ) ) );
} );
