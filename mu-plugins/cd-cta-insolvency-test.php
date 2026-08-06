<?php
/**
 * Plugin Name: CD Insolvency Test CTA Blocks
 * Description: In-content CTA blocks driving /insolvency-calculator/, in two shapes
 *              (full card, compact inline) and four copy variants keyed to where the
 *              reader already is. Shortcode: [cd_test_cta variant="…" style="…"].
 *              Copy and styling live here rather than in post content because post
 *              content is KSES-filtered (inline <svg> is stripped on push), and because
 *              a site-wide roll-out needs one place to edit the wording.
 * Version:     2.0.0
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

const CD_TEST_CTA_URL = '/insolvency-calculator/';

/**
 * Copy variants.
 *
 * The test itself is the same four questions whichever page sends the reader to it.
 * What changes is the reader's starting point, so what changes here is the promise —
 * and each promise is limited to what the result screen actually delivers: which
 * warning signs apply, how serious the position looks, a recommended timeframe, and
 * the routes that may fit (arrangement, restructuring, administration, CVL, or
 * solvent closure where the answers support it).
 *
 * NOT a variant, deliberately: solvent closure (MVL / strike-off). The test's first
 * question offers no "yes, comfortably" answer, so a solvent director is forced into
 * a distress answer. Send those readers to the MVL pages, not here.
 *
 * @return array<string, array<string, string>>
 */
function cd_test_cta_variants() {
	return array(

		// Default. The reader suspects trouble but has had no formal action.
		// Cash-flow, HMRC arrears, general worry, rescue.
		'unsure' => array(
			'title'         => 'Could Your Company Be Insolvent?',
			'body_1'        => 'Answer four short questions about cash flow and creditor pressure.',
			'body_2'        => 'See which warning signs apply and what options may be available.',
			'button'        => 'Check my company&rsquo;s position',
			'compact_title' => 'Not Sure Where Your Company Stands?',
			'compact_body'  => 'Answer four questions in about two minutes and see which warning signs apply '
			                 . 'and what your company may be able to do next.',
			'compact_button' => 'Check My Company&rsquo;s Position',
		),

		// A statutory demand, winding-up petition, judgment, bailiffs or enforcement
		// is already in play. "Could you be insolvent?" is a question this reader has
		// moved past — the live questions are how bad it is and what is still open.
		'formal_action' => array(
			'title'         => 'How Serious Is It, and What Is Still Open?',
			'body_1'        => 'Four short questions about cash flow, what the company owes and the pressure it is under.',
			'body_2'        => 'See how serious the position looks and which routes are realistically available.',
			'button'        => 'Check where the company stands',
			'compact_title' => 'Where Does the Company Actually Stand?',
			'compact_body'  => 'Four questions, about two minutes. See how serious the position is and which '
			                 . 'routes are still open to you.',
			'compact_button' => 'Check Where the Company Stands',
		),

		// The reader is already looking at closure because the company cannot pay.
		// The useful question is whether closure is the right route.
		'closing' => array(
			'title'         => 'Is Closure the Right Route, or Is There Another?',
			'body_1'        => 'Four short questions about cash flow, debts and creditor pressure.',
			'body_2'        => 'See how serious the position is and whether liquidation, restructuring or an '
			                 . 'arrangement with creditors fits better.',
			'button'        => 'Check the company&rsquo;s position',
			'compact_title' => 'Sure Closure Is the Right Step?',
			'compact_body'  => 'Four questions in about two minutes will show how serious the position is and '
			                 . 'whether liquidation, restructuring or an arrangement fits better.',
			'compact_button' => 'Check the Company&rsquo;s Position',
		),

		// Personal guarantees, wrongful trading, disqualification worry.
		// Kept deliberately modest: the test assesses the COMPANY's position. It does
		// not assess personal exposure, and must not imply that it does.
		'personal_risk' => array(
			'title'         => 'How Bad Is the Company&rsquo;s Position?',
			'body_1'        => 'Four short questions about cash flow, debts and creditor pressure.',
			'body_2'        => 'See which warning signs apply and what to do first. The earlier the company&rsquo;s '
			                 . 'position is clear, the more room there is to act on it.',
			'button'        => 'Check the company&rsquo;s position',
			'compact_title' => 'Worried About Where This Leaves You Personally?',
			'compact_body'  => 'Start with the company&rsquo;s position. Four questions in about two minutes show '
			                 . 'how serious it is and what to do first.',
			'compact_button' => 'Check the Company&rsquo;s Position',
		),
	);
}

/**
 * Which variant a page gets, in priority order:
 *   1. the shortcode's own variant="…"
 *   2. the per-page map below (slug => variant), for pages the roll-out has reviewed
 *   3. the default, 'unsure'
 *
 * Deliberately no keyword-guessing from slugs: guessing wrong here means telling a
 * director who has a petition in hand that they might want to check whether the
 * company is insolvent. An unreviewed page gets the neutral default instead.
 *
 * @return array<string, string>
 */
function cd_test_cta_page_map() {
	return array(
		'winding-up-petitions' => 'formal_action',
	);
}

function cd_test_cta_resolve_variant( $requested = '' ) {
	$variants = cd_test_cta_variants();
	$requested = str_replace( '-', '_', (string) $requested );
	if ( $requested && isset( $variants[ $requested ] ) ) { return $requested; }

	if ( is_singular() ) {
		$slug = get_post_field( 'post_name', get_queried_object_id() );
		$map  = cd_test_cta_page_map();
		if ( $slug && isset( $map[ $slug ] ) && isset( $variants[ $map[ $slug ] ] ) ) {
			return $map[ $slug ];
		}
	}
	return 'unsure';
}

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
	$atts = shortcode_atts( array( 'style' => 'full', 'variant' => '' ), $atts, 'cd_test_cta' );

	$key = cd_test_cta_resolve_variant( $atts['variant'] );
	$v   = cd_test_cta_variants()[ $key ];
	$url = esc_url( CD_TEST_CTA_URL );

	// The outer .cd-cta-shell carries container-type so the blocks size themselves to
	// the column they are dropped into (narrow article body vs full-width page), not to
	// the viewport. A viewport media query would give a desktop-sized hero inside a
	// 760px column.
	if ( 'compact' === $atts['style'] ) {
		$tag = 'insolvency-test-compact-' . str_replace( '_', '-', $key );
		return '<div class="cd-cta-shell"><div class="cd-cta-compact">'
			. '<p class="cd-cta-compact__title">' . $v['compact_title'] . '</p>'
			. '<p class="cd-cta-compact__body">' . $v['compact_body'] . '</p>'
			. '<a class="cd-cta-compact__btn" href="' . $url . '" data-cd-cta="' . esc_attr( $tag ) . '">'
			. $v['compact_button'] . ' <span aria-hidden="true">&rarr;</span></a>'
			. '<p class="cd-cta-compact__reassure"><span>Estimates are fine</span>'
			. '<span><strong>We only call if you ask us to</strong></span></p>'
			. '</div></div>';
	}

	$tag = 'insolvency-test-full-' . str_replace( '_', '-', $key );
	return '<div class="cd-cta-shell"><div class="cd-cta-full">'
		. '<div class="cd-cta-full__meta">'
		. '<p class="cd-cta-full__eyebrow">Free Online Test</p>'
		. '<span class="cd-cta-full__timing">' . cd_test_cta_icon( 'clock' ) . '4 questions &middot; 2 minutes</span>'
		. '</div>'
		. '<div class="cd-cta-full__main">'
		. '<div class="cd-cta-full__content">'
		. '<p class="cd-cta-full__title">' . $v['title'] . '</p>'
		. '<p class="cd-cta-full__body">' . $v['body_1'] . '</p>'
		. '<p class="cd-cta-full__body">' . $v['body_2'] . '</p>'
		. '<a class="cd-cta-full__btn" href="' . $url . '" data-cd-cta="' . esc_attr( $tag ) . '">'
		. $v['button'] . cd_test_cta_icon( 'arrow' ) . '</a>'
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
