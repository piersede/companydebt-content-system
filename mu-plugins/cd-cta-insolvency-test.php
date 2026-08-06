<?php
/**
 * Plugin Name: CD Insolvency Test CTA Blocks
 * Description: Two in-content CTA blocks that drive traffic to /insolvency-calculator/.
 *              Shortcode [cd_test_cta] (full hero card) and [cd_test_cta style="compact"].
 *              Copy and styling live here rather than in post content because post content
 *              is KSES-filtered (inline <svg> and <style> are stripped on push), and because
 *              the roll-out plan needs one place to edit the copy for every page at once.
 * Version:     1.0.0
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

const CD_TEST_CTA_URL = '/insolvency-calculator/';

/**
 * Enqueue the block CSS only on singulars whose content actually uses the shortcode.
 */
add_action( 'wp_enqueue_scripts', function () {
	if ( ! is_singular() ) { return; }
	$content = get_post_field( 'post_content', get_queried_object_id() );
	if ( ! $content || ! has_shortcode( $content, 'cd_test_cta' ) ) { return; }

	$file = __DIR__ . '/cd-cta-blocks/cta-blocks.css';
	if ( ! is_readable( $file ) ) { return; }
	wp_register_style( 'cd-test-cta', false, array(), null );
	wp_enqueue_style( 'cd-test-cta' );
	wp_add_inline_style( 'cd-test-cta', file_get_contents( $file ) );
} );

/**
 * Clock + arrow icons. Inline so there is no extra request and no dependency on an
 * icon font; safe here because plugin output is not KSES-filtered.
 */
function cd_test_cta_icon( $which ) {
	$open = '<svg width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
	      . 'stroke-width="%s" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">';
	if ( 'clock' === $which ) {
		return sprintf( $open, 16, 16, '2' ) . '<circle cx="12" cy="12" r="9"></circle><path d="M12 7v5l3 3"></path></svg>';
	}
	return sprintf( $open, 18, 18, '2.5' ) . '<path d="M5 12h14M13 6l6 6-6 6"></path></svg>';
}

add_shortcode( 'cd_test_cta', function ( $atts ) {
	$atts = shortcode_atts( array( 'style' => 'full' ), $atts, 'cd_test_cta' );
	$url  = esc_url( CD_TEST_CTA_URL );

	// The outer .cd-cta-shell carries container-type so the blocks size themselves to the
	// column they are dropped into (narrow article body vs full-width page), not to the
	// viewport. A viewport media query would give a desktop-sized hero inside a 760px column.
	if ( 'compact' === $atts['style'] ) {
		return '<div class="cd-cta-shell">'
			. '<div class="cd-cta-compact">'
			. '<p class="cd-cta-compact__title">Not Sure Where Your Company Stands?</p>'
			. '<p class="cd-cta-compact__body">Answer four questions in about two minutes and see which warning '
			. 'signs apply and what your company may be able to do next.</p>'
			. '<a class="cd-cta-compact__btn" href="' . $url . '" data-cd-cta="insolvency-test-compact">'
			. 'Check My Company&rsquo;s Position <span aria-hidden="true">&rarr;</span></a>'
			. '<p class="cd-cta-compact__reassure"><span>Estimates are fine</span>'
			. '<span><strong>We only call if you ask us to</strong></span></p>'
			. '</div></div>';
	}

	return '<div class="cd-cta-shell"><div class="cd-cta-full">'
		. '<div class="cd-cta-full__meta">'
		. '<p class="cd-cta-full__eyebrow">Free Online Test</p>'
		. '<span class="cd-cta-full__timing">' . cd_test_cta_icon( 'clock' ) . '4 questions &middot; 2 minutes</span>'
		. '</div>'
		. '<div class="cd-cta-full__main">'
		. '<div class="cd-cta-full__content">'
		. '<p class="cd-cta-full__title">Could Your Company Be Insolvent?</p>'
		. '<p class="cd-cta-full__body">Answer four short questions about cash flow and creditor pressure.</p>'
		. '<p class="cd-cta-full__body">See which warning signs apply and what options may be available.</p>'
		. '<a class="cd-cta-full__btn" href="' . $url . '" data-cd-cta="insolvency-test-full">'
		. 'Check my company&rsquo;s position' . cd_test_cta_icon( 'arrow' ) . '</a>'
		. '<p class="cd-cta-full__reassure">See your result online and receive a copy by email. '
		. '<strong>We only call if you ask.</strong></p>'
		. '</div>'
		. '<div class="cd-cta-full__visual">'
		. '<img class="cd-cta-full__laptop" src="' . esc_url( plugins_url( 'cd-cta-blocks/laptop-mockup.png', __FILE__ ) ) . '" '
		. 'width="820" height="524" loading="lazy" decoding="async" '
		. 'alt="A laptop showing the first question of the insolvency test">'
		. '</div>'
		. '</div>'
		. '</div></div>';
} );
