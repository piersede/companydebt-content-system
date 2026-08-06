<?php
/**
 * Plugin Name: CD Insolvency Test CTA Blocks
 * Description: In-content CTA blocks for the insolvency test, plus the two CTAs that
 *              take priority over it. Implements docs/cta-insolvency-test-wording-plan.md.
 *              Shortcodes: [cd_test_cta], [cd_advice_cta], [cd_solvent_cta].
 * Version:     3.0.0
 *
 * Governance rules from the plan that are ENFORCED HERE rather than left to discipline,
 * because a rule that depends on remembering it will be broken during a 230-page roll-out:
 *   - personal-risk pages get the test as a compact secondary block only (rule 4);
 *   - urgent pages get the test as a compact secondary block only, so direct contact
 *     stays the primary action (rule 3);
 *   - the button label is identical on every test block (rule 2);
 *   - variant="none" renders nothing at all (rules 5 and 7).
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

const CD_TEST_CTA_URL    = '/insolvency-calculator/';
const CD_ADVICE_CTA_TEL  = '08000746757';
const CD_SOLVENT_CTA_URL = '/liquidation/members-voluntary-liquidation/';

/** One action, one label, every test block. Plan section 10. */
const CD_TEST_CTA_BUTTON = 'Check my company&rsquo;s position';

/**
 * Wording set. Plan sections 3, 4, 5 and 17.
 *
 * Each entry may define large and compact copy. Where a variant is compact-only the
 * large copy is absent on purpose and the shortcode downgrades to compact.
 *
 * @return array<string, array<string, mixed>>
 */
function cd_test_cta_variants() {
	return array(

		// Financial pressure, but the reader has not concluded the company is insolvent.
		'early_check' => array(
			'eyebrow'         => 'Free Online Test',
			'title'           => 'Could Your Company Be Insolvent?',
			'body'            => array(
				'Answer four short questions to see which warning signs apply, how serious the '
				. 'position may be and how soon you may need to act.',
				'See which options may fit your company&rsquo;s circumstances.',
			),
			'compact_title'   => 'Not Sure Where Your Company Stands?',
			'compact_body'    => 'Use the two-minute test to check the warning signs and see how soon '
			                   . 'you may need to act.',
		),

		// Serious distress or insolvency is already likely, acknowledged or central.
		'serious_position' => array(
			'eyebrow'         => 'Free Online Test',
			'title'           => 'How Serious Is Your Company&rsquo;s Position?',
			'body'            => array(
				'Answer four short questions to see how urgent the situation may be and which '
				. 'options could fit your company&rsquo;s circumstances.',
			),
			'compact_title'   => 'Check How Serious the Position May Be',
			'compact_body'    => 'Answer four short questions to see how urgent the situation may be '
			                   . 'and which broad options could fit.',
		),

		// Personal-risk pages. Compact only, and the limitation is stated in the body
		// rather than implied — the test assesses the company, never the director.
		'personal_risk_secondary' => array(
			'compact_eyebrow' => 'Company Position Check',
			'compact_title'   => 'First, Check the Company&rsquo;s Financial Position',
			'compact_body'    => 'This test does not assess your personal liability. It can help show '
			                   . 'how serious the company&rsquo;s position may be and how quickly action '
			                   . 'could be needed.',
			'compact_only'    => true,
		),
	);
}

/**
 * The urgency modifier replaces the test block's own framing so it reads as the
 * secondary option beneath a direct-contact CTA. Plan section 4.
 */
function cd_test_cta_urgency_copy() {
	return array(
		'compact_eyebrow' => 'Two-Minute Company Check',
		'compact_title'   => 'How Urgent Is Your Company&rsquo;s Position?',
		'compact_body'    => 'Check the wider warning signs, likely urgency and which broad options '
		                   . 'may fit your company&rsquo;s circumstances.',
	);
}

/**
 * Reviewed page map: slug => array( variant, urgency ).
 *
 * Only pages a human has actually reviewed belong here. Everything else falls to the
 * safe default. Plan sections 9 and 12: no automatic guessing from URL or title.
 *
 * @return array<string, array{0:string,1:string}>
 */
function cd_test_cta_page_map() {
	return array(
		'winding-up-petitions' => array( 'serious_position', 'urgent_action' ),
	);
}

/** Plan section 9: the safe default is the less severe message, never the more severe. */
const CD_TEST_CTA_DEFAULT = 'early_check';

function cd_test_cta_resolve( $variant = '', $urgency = '' ) {
	$variants = cd_test_cta_variants();
	$variant  = str_replace( '-', '_', (string) $variant );
	$urgency  = str_replace( '-', '_', (string) $urgency );

	if ( 'none' === $variant ) { return array( 'none', '' ); }

	if ( $variant && isset( $variants[ $variant ] ) ) {
		return array( $variant, ( 'urgent_action' === $urgency ) ? 'urgent_action' : '' );
	}

	if ( is_singular() ) {
		$slug = get_post_field( 'post_name', get_queried_object_id() );
		$map  = cd_test_cta_page_map();
		if ( $slug && isset( $map[ $slug ] ) ) {
			$mapped = $map[ $slug ];
			// A reviewed page may be mapped to 'none' — the test does not serve its
			// reader (solvent company, creditor or employee audience, or a company
			// already deep inside a formal process). Plan section 7.
			if ( 'none' === $mapped[0] ) { return array( 'none', '' ); }
			if ( isset( $variants[ $mapped[0] ] ) ) {
				return array( $mapped[0], ( 'urgent_action' === $urgency ) ? 'urgent_action' : $mapped[1] );
			}
		}
	}
	return array( CD_TEST_CTA_DEFAULT, ( 'urgent_action' === $urgency ) ? 'urgent_action' : '' );
}

/**
 * Enqueue the block CSS only on singulars whose content actually uses one of the blocks.
 */
add_action( 'wp_enqueue_scripts', function () {
	if ( ! is_singular() ) { return; }
	$id      = get_queried_object_id();
	$content = (string) get_post_field( 'post_content', $id );

	$used = $content && (
		   has_shortcode( $content, 'cd_test_cta' )
		|| has_shortcode( $content, 'cd_advice_cta' )
		|| has_shortcode( $content, 'cd_solvent_cta' )
	);

	// The theme also injects these blocks into the pages in its own CTA map, where the
	// shortcode never appears in post content. Without this the injected block renders
	// as unstyled plain text — which is exactly what happened the first time.
	if ( ! $used && function_exists( 'cd_acta_map' ) ) {
		$map  = cd_acta_map();
		$used = isset( $map[ $id ] );
	}
	if ( ! $used ) { return; }

	$file = __DIR__ . '/cd-cta-blocks/cta-blocks.css';
	if ( ! is_readable( $file ) ) { return; }
	wp_register_style( 'cd-test-cta', false, array(), null );
	wp_enqueue_style( 'cd-test-cta' );
	wp_add_inline_style( 'cd-test-cta', file_get_contents( $file ) );
} );

/**
 * Inline icons — no extra request, no icon-font dependency. Safe here because plugin
 * output is not KSES-filtered (post content is, which is why none of this lives there).
 */
function cd_test_cta_icon( $which ) {
	$open = '<svg width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
	      . 'stroke-width="%s" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">';
	if ( 'clock' === $which ) {
		return sprintf( $open, 16, 16, '2' ) . '<circle cx="12" cy="12" r="9"></circle><path d="M12 7v5l3 3"></path></svg>';
	}
	if ( 'phone' === $which ) {
		return sprintf( $open, 18, 18, '2.2' )
		     . '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"></path></svg>';
	}
	return sprintf( $open, 18, 18, '2.5' ) . '<path d="M5 12h14M13 6l6 6-6 6"></path></svg>';
}

/** Tracking attributes. Plan section 14: state, urgency and size tracked separately. */
function cd_test_cta_track( $cta, $variant, $urgency, $size, $context ) {
	if ( '' === $context && is_singular() ) {
		$context = (string) get_post_field( 'post_name', get_queried_object_id() );
	}
	return ' data-cd-cta="' . esc_attr( $cta ) . '"'
	     . ' data-cd-variant="' . esc_attr( $variant ) . '"'
	     . ' data-cd-urgency="' . esc_attr( $urgency ) . '"'
	     . ' data-cd-size="' . esc_attr( $size ) . '"'
	     . ' data-cd-page-context="' . esc_attr( $context ) . '"';
}

add_shortcode( 'cd_test_cta', function ( $atts ) {
	$atts = shortcode_atts(
		array( 'size' => 'large', 'style' => '', 'variant' => '', 'urgency' => '', 'context' => '' ),
		$atts,
		'cd_test_cta'
	);
	// 'style' kept as an alias so the pilot page's existing markup keeps working.
	$size = $atts['style'] ? $atts['style'] : $atts['size'];
	$size = ( 'compact' === $size ) ? 'compact' : 'large';

	list( $key, $urgency ) = cd_test_cta_resolve( $atts['variant'], $atts['urgency'] );
	if ( 'none' === $key ) { return ''; }

	$v = cd_test_cta_variants()[ $key ];

	// Enforced downgrades — see the governance note at the top of this file.
	if ( ! empty( $v['compact_only'] ) || 'urgent_action' === $urgency ) { $size = 'compact'; }

	$url   = esc_url( CD_TEST_CTA_URL );
	$track = cd_test_cta_track( 'insolvency-test', $key, $urgency, $size, $atts['context'] );

	if ( 'compact' === $size ) {
		$copy = ( 'urgent_action' === $urgency ) ? cd_test_cta_urgency_copy() : $v;
		$eyebrow = isset( $copy['compact_eyebrow'] ) ? $copy['compact_eyebrow'] : '';

		$out  = '<div class="cd-cta-shell"><div class="cd-cta-compact">';
		if ( $eyebrow ) {
			$out .= '<p class="cd-cta-compact__eyebrow">' . $eyebrow . '</p>';
		}
		$out .= '<p class="cd-cta-compact__title">' . $copy['compact_title'] . '</p>'
		      . '<p class="cd-cta-compact__body">' . $copy['compact_body'] . '</p>'
		      . '<a class="cd-cta-compact__btn" href="' . $url . '"' . $track . '>'
		      . CD_TEST_CTA_BUTTON . ' <span aria-hidden="true">&rarr;</span></a>'
		      . '<p class="cd-cta-compact__reassure"><span>Estimates are fine</span>'
		      . '<span><strong>We only call if you ask us to</strong></span></p>'
		      . '</div></div>';
		return $out;
	}

	$body = '';
	foreach ( $v['body'] as $para ) {
		$body .= '<p class="cd-cta-full__body">' . $para . '</p>';
	}

	return '<div class="cd-cta-shell"><div class="cd-cta-full">'
		. '<div class="cd-cta-full__meta">'
		. '<p class="cd-cta-full__eyebrow">' . $v['eyebrow'] . '</p>'
		. '<span class="cd-cta-full__timing">' . cd_test_cta_icon( 'clock' ) . '4 questions &middot; 2 minutes</span>'
		. '</div>'
		. '<div class="cd-cta-full__main">'
		. '<div class="cd-cta-full__content">'
		. '<p class="cd-cta-full__title">' . $v['title'] . '</p>'
		. $body
		. '<a class="cd-cta-full__btn" href="' . $url . '"' . $track . '>'
		. CD_TEST_CTA_BUTTON . cd_test_cta_icon( 'arrow' ) . '</a>'
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

/**
 * Primary CTA for pages about formal creditor action. Plan section 4.
 * Deliberately says nothing about the specific action: the plan forbids implying the
 * test or the page can assess a petition, stop enforcement or read a court order.
 *
 * The headline can be overridden per page where the page supports a narrower claim.
 */
add_shortcode( 'cd_advice_cta', function ( $atts ) {
	$atts = shortcode_atts(
		array( 'title' => 'Facing Formal Creditor Action?', 'context' => '' ),
		$atts,
		'cd_advice_cta'
	);
	$tel   = CD_ADVICE_CTA_TEL;
	$shown = '0800 074 6757';
	$track = cd_test_cta_track( 'direct-advice', '', 'urgent_action', 'large', $atts['context'] );

	return '<div class="cd-cta-shell"><div class="cd-cta-full cd-cta-full--advice">'
		. '<div class="cd-cta-full__content">'
		. '<p class="cd-cta-full__title">' . esc_html( $atts['title'] ) . '</p>'
		. '<p class="cd-cta-full__body">Deadlines can be short. Speak to an insolvency adviser about the '
		. 'action already under way and the options that may still be available.</p>'
		. '<a class="cd-cta-full__btn" href="tel:' . esc_attr( $tel ) . '"' . $track . '>'
		. cd_test_cta_icon( 'phone' ) . 'Speak to an insolvency adviser now</a>'
		. '<p class="cd-cta-full__reassure">Call <a href="tel:' . esc_attr( $tel ) . '">' . $shown . '</a>. '
		. '<strong>Confidential, and no obligation.</strong></p>'
		. '</div>'
		. '</div></div>';
} );

/**
 * Solvent-closure CTA — what solvent-company pages get INSTEAD of the test, because the
 * test's first question has no "yes, comfortably" answer and forces a healthy company
 * into a distress answer. Plan sections 6A, 7.1 and 16.
 */
add_shortcode( 'cd_solvent_cta', function ( $atts ) {
	$atts  = shortcode_atts( array( 'context' => '' ), $atts, 'cd_solvent_cta' );
	$track = cd_test_cta_track( 'solvent-closure', '', '', 'compact', $atts['context'] );

	return '<div class="cd-cta-shell"><div class="cd-cta-compact">'
		. '<p class="cd-cta-compact__title">Looking to Close a Solvent Company?</p>'
		. '<p class="cd-cta-compact__body">Compare strike-off and members&rsquo; voluntary liquidation, '
		. 'including when each route may be suitable.</p>'
		. '<a class="cd-cta-compact__btn" href="' . esc_url( CD_SOLVENT_CTA_URL ) . '"' . $track . '>'
		. 'Explore solvent closure options <span aria-hidden="true">&rarr;</span></a>'
		. '</div></div>';
} );
