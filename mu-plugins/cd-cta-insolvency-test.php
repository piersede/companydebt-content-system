<?php
/**
 * Plugin Name: CD Insolvency Test CTA Blocks
 * Description: In-content CTA blocks for the insolvency test, plus the CTAs that take
 *              priority over it on pages the test does not serve. Implements
 *              docs/cta-insolvency-test-wording-plan.md.
 *              Shortcodes: [cd_test_cta], [cd_advice_cta], [cd_solvent_cta],
 *              [cd_process_cta], [cd_personal_liability_cta], [cd_partnership_cta],
 *              [cd_specialist_cta], [cd_creditor_cta], [cd_hmrc_cta], [cd_closure_cta].
 * Version:     3.1.0
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
// No longer a destination. Since the solvent CTA became a phone call rather than a link
// to a guide, this is only used to detect that the reader is ON the MVL page, which gets
// its own wording. Do not turn it back into an href without re-reading plan section 1.
const CD_SOLVENT_CTA_URL = '/liquidation/members-voluntary-liquidation/';

/** One action, one label, every test block. Plan section 10. */
const CD_TEST_CTA_BUTTON = 'Check my company&rsquo;s position';

/**
 * One label on every non-urgent phone block. Section 10 asks for one action per CTA
 * type, and the site now has exactly three: this, the urgent block's "Speak to an
 * insolvency adviser now", and the test's own button. "Speak to an insolvency
 * practitioner" was mine and it is a job title, not an invitation; this is Piers's
 * wording and it is what a worried reader would actually click.
 */
const CD_ALT_CTA_BUTTON = 'Speak to an Adviser';

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
 * Reviewed page map: slug => array( variant, urgency, block size, alternative primary CTA ).
 *
 * Generated from the completed review list by scripts/build_cta_page_map.py. Only pages a
 * human has actually reviewed are in it; everything else falls to the safe default. Plan
 * sections 9 and 12: no automatic guessing from URL or title.
 *
 * The file lives in the assets sub-folder rather than beside this one because WordPress
 * auto-loads every .php directly inside mu-plugins, and this one is data, not a plugin.
 *
 * @return array<string, array{0:string,1:string,2:string,3:string}>
 */
function cd_test_cta_page_map() {
	static $map = null;
	if ( null !== $map ) { return $map; }
	$file = __DIR__ . '/cd-cta-blocks/page-map.php';
	$map  = is_readable( $file ) ? (array) require $file : array();
	return $map;
}

/**
 * The reviewed decision for the page being viewed, or null if it has not been reviewed.
 *
 * @return array{0:string,1:string,2:string,3:string}|null variant, urgency, size, alternative CTA
 */
function cd_test_cta_page_entry() {
	if ( ! is_singular() ) { return null; }
	$slug = get_post_field( 'post_name', get_queried_object_id() );
	if ( ! $slug ) { return null; }
	$map = cd_test_cta_page_map();
	return isset( $map[ $slug ] ) ? $map[ $slug ] : null;
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

	$entry = cd_test_cta_page_entry();
	if ( $entry ) {
		// A reviewed page may be mapped to 'none' — the test does not serve its reader
		// (solvent company, creditor or employee audience, or a company already deep
		// inside a formal process). Plan section 7.
		if ( 'none' === $entry[0] ) { return array( 'none', '' ); }
		if ( isset( $variants[ $entry[0] ] ) ) {
			return array( $entry[0], ( 'urgent_action' === $urgency ) ? 'urgent_action' : $entry[1] );
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

	if ( ! $content ) { return; }

	$tags = array( 'cd_test_cta', 'cd_advice_cta', 'cd_solvent_cta' );
	foreach ( cd_cta_alt_wording() as $alt ) { $tags[] = $alt['tag']; }

	$used = false;
	foreach ( $tags as $tag ) {
		if ( has_shortcode( $content, $tag ) ) { $used = true; break; }
	}

	if ( ! $used ) { return; }
	cd_test_cta_enqueue();
} );

/**
 * Load the block CSS. Safe to call more than once, and called again from inside every
 * block so that anything rendering a block programmatically — a template, a filter, a
 * future placement system — gets the styling too.
 *
 * This exists because of a real failure: the CSS was gated on the shortcode appearing in
 * post content, so blocks placed by a content filter rendered as unstyled plain text
 * while every response still returned 200 with correct markup.
 */
function cd_test_cta_enqueue() {
	static $done = false;
	if ( $done || ! function_exists( 'wp_enqueue_style' ) ) { return; }
	$file = __DIR__ . '/cd-cta-blocks/cta-blocks.css';
	if ( ! is_readable( $file ) ) { return; }
	$done = true;
	wp_register_style( 'cd-test-cta', false, array(), null );
	wp_enqueue_style( 'cd-test-cta' );
	wp_add_inline_style( 'cd-test-cta', file_get_contents( $file ) );
}

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

/**
 * True when a CTA would point at the page it is sitting on. Without this the
 * solvent-closure block appears on the members' voluntary liquidation page inviting the
 * reader to visit the members' voluntary liquidation page.
 */
function cd_cta_points_here( $url ) {
	if ( ! $url || 0 === strpos( $url, 'tel:' ) ) { return false; }
	$here = is_singular() ? wp_parse_url( get_permalink( get_queried_object_id() ), PHP_URL_PATH ) : '';
	$there = wp_parse_url( $url, PHP_URL_PATH );
	return $here && $there && untrailingslashit( $here ) === untrailingslashit( $there );
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
		array( 'size' => '', 'style' => '', 'variant' => '', 'urgency' => '', 'context' => '' ),
		$atts,
		'cd_test_cta'
	);
	// Size comes from the shortcode if it says; otherwise from the page's reviewed
	// decision; otherwise large. 'style' is kept as an alias for older markup.
	$size = $atts['style'] ? $atts['style'] : $atts['size'];
	if ( ! $size ) {
		$entry = cd_test_cta_page_entry();
		if ( $entry && ! empty( $entry[2] ) ) { $size = $entry[2]; }
	}
	$size = ( 'compact' === $size ) ? 'compact' : 'large';

	cd_test_cta_enqueue();
	list( $key, $urgency ) = cd_test_cta_resolve( $atts['variant'], $atts['urgency'] );
	if ( 'none' === $key ) { return ''; }
	if ( cd_cta_points_here( CD_TEST_CTA_URL ) ) { return ''; }

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
	cd_test_cta_enqueue();
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
	cd_test_cta_enqueue();
	$atts  = shortcode_atts( array( 'context' => '' ), $atts, 'cd_solvent_cta' );

	// On the members' voluntary liquidation page itself, "explore solvent closure
	// options" would point at the page the reader is already on. An MVL is the one
	// procedure here that is not about insolvency, so it gets its own CTA.
	//
	// Wording by Piers, 6 Aug 2026. The version before it opened by explaining what an
	// MVL is to a director already reading the MVL page, and led on qualifying rather
	// than on the reason anyone is there: retained profits they want out. It also gets
	// its own button. Section 10 asks for one label per CTA type, not one label
	// everywhere, and it already makes that exception for the urgent block; an MVL
	// specialist is a genuinely different ask from general insolvency advice.
	if ( cd_cta_points_here( CD_SOLVENT_CTA_URL ) ) {
		$track = cd_test_cta_track( 'mvl-advice', '', '', 'compact', $atts['context'] );
		return '<div class="cd-cta-shell"><div class="cd-cta-compact">'
			. '<p class="cd-cta-compact__eyebrow">Members&rsquo; Voluntary Liquidation</p>'
			. '<p class="cd-cta-compact__title">Expert MVL Advice for Solvent Company Directors</p>'
			. '<p class="cd-cta-compact__body">If your company has significant retained profits, an MVL '
			. 'can be an efficient way to close the business and return funds to shareholders. Speak '
			. 'directly with an experienced licensed insolvency practitioner about the process, costs '
			. 'and whether an MVL is the right route for your company.</p>'
			. '<a class="cd-cta-compact__btn" href="tel:' . esc_attr( CD_ADVICE_CTA_TEL ) . '"' . $track . '>'
			. 'Speak to an MVL Specialist <span aria-hidden="true">&rarr;</span></a>'
			. '<p class="cd-cta-compact__reassure"><span>Call 0800 074 6757</span>'
			. '<span><strong>Confidential, and no obligation</strong></span></p>'
			. '</div></div>';
	}

	// The other five solvent pages. Wording by Piers, 6 Aug 2026, and it is deliberately
	// a phone CTA rather than a link to another guide.
	//
	// The link version was wrong twice over. It promised "compare strike-off and members'
	// voluntary liquidation" but pointed at the MVL guide, which explains one route and
	// compares nothing, so it broke the plan's first rule. And pointing it at the
	// comparison guide instead would have made it vanish from /closing-a-limited-company/,
	// which is that very guide.
	//
	// Neither problem exists once it stops being a link. The deeper point is commercial:
	// this reader may be a director sitting on substantial retained profits, and what is
	// worth offering them is an insolvency practitioner, not another article. The wording
	// works on all five pages, including for someone who came looking at strike-off and
	// has not yet realised an MVL may be the better route for the value in the company.
	$track = cd_test_cta_track( 'solvent-closure', '', '', 'compact', $atts['context'] );

	return '<div class="cd-cta-shell"><div class="cd-cta-compact">'
		. '<p class="cd-cta-compact__eyebrow">Solvent Company Closure</p>'
		. '<p class="cd-cta-compact__title">Closing a Solvent Company?</p>'
		. '<p class="cd-cta-compact__body">If your company has retained profits or assets, a '
		. 'Members&rsquo; Voluntary Liquidation may be a tax-efficient way to close and distribute '
		. 'the remaining value.</p>'
		. '<p class="cd-cta-compact__body">Speak directly with an experienced licensed insolvency '
		. 'practitioner about whether an MVL is suitable, what it will cost and how the process '
		. 'works.</p>'
		. '<a class="cd-cta-compact__btn" href="tel:' . esc_attr( CD_ADVICE_CTA_TEL ) . '"' . $track . '>'
		. 'Discuss Your Closure Options <span aria-hidden="true">&rarr;</span></a>'
		. '<p class="cd-cta-compact__reassure"><span>Call 0800 074 6757</span>'
		. '<span><strong>Confidential, and no obligation</strong></span></p>'
		. '</div></div>';
} );

/* ---------------------------------------------------------------------------
 * Alternative primary CTAs
 *
 * 187 reviewed pages are mapped to variant 'none': the insolvency test does not serve
 * their reader. Each names an alternative primary CTA in the review, and those are
 * defined below. Two rules from the plan shape every one of them.
 *
 * Section 1 — a CTA promises only what its destination can deliver. So the HMRC block
 * says nothing about defending a tax investigation, which we do not do; it addresses
 * the affordability problem an investigation creates, which we do. The personal-risk
 * block offers a conversation about the COMPANY's position and states plainly that no
 * general guide settles personal exposure (rules 1 and 4).
 *
 * Section 10 — one consistent label per CTA type. Every phone block says "Speak to an
 * insolvency practitioner"; the urgent block keeps its own "Speak to an insolvency
 * adviser now"; the test keeps CD_TEST_CTA_BUTTON.
 *
 * Three reviewed labels deliberately have NO block and render nothing:
 *   - Page-specific guidance (14 low-intent pages: director duties, limited liability,
 *     the Companies Act, the glossary). Any CTA there interrupts a reader who is not
 *     in trouble.
 *   - Employee guidance (1). Redundancy and unpaid wages are claimed from the
 *     Insolvency Service, not from us. Nothing to sell, so nothing is shown.
 *   - Personal debt guidance (1, the IVA page). An individual's own debt is not our
 *     work.
 * Decided by Piers, 6 Aug 2026. These are decisions, not gaps.
 * ------------------------------------------------------------------------ */

/**
 * The alternative-CTA wording set, keyed by the review's own label so the review column
 * and the block that renders from it cannot drift apart.
 *
 * shape 'phone'   — large card, telephone action. The primary action on the page.
 * shape 'link'    — compact card pointing at a guide that already answers the question.
 * shape 'phone_compact' — compact card, telephone action, for pages that already carry
 *                   a test block and must not gain a second dominant one (section 11).
 *
 * @return array<string, array<string, string>>
 */
function cd_cta_alt_wording() {
	return array(

		// The next three replace a single block that carried one headline across 23 pages
		// spanning pensions, leases, conduct reports and winding-up orders. That grouping
		// was a filing decision in the review, not a reader, and the headline it produced
		// was the label reworded. These are sorted by what the reader is actually afraid
		// of. Piers, 6 Aug 2026.

		// 6 pages: bank account, pensions, property, vehicles, IP, leases. The fear is
		// losing things, and not knowing what may still be touched.
		'assets' => array(
			'tag'     => 'cd_assets_cta',
			'shape'   => 'phone',
			'eyebrow' => 'Company Assets',
			'title'   => 'Worried About What Happens to Company Assets?',
			'body'    => 'Speak confidentially with an insolvency adviser about property, vehicles, '
			           . 'equipment, contracts and bank accounts, and what a director can and '
			           . 'cannot do with them.',
			'button'  => CD_ALT_CTA_BUTTON,
		),

		// 7 pages: meetings, the statement of affairs, the document list, a liquidator's
		// powers. The fear is an unfamiliar process and being caught out by it.
		'process-guidance' => array(
			'tag'     => 'cd_process_cta',
			'shape'   => 'phone',
			'eyebrow' => 'What Happens Next',
			'title'   => 'Unsure What the Process Will Ask of You?',
			'body'    => 'Speak confidentially with an insolvency adviser about meetings, '
			           . 'paperwork, deadlines, and what a liquidator can and cannot require '
			           . 'of you.',
			'button'  => CD_ALT_CTA_BUTTON,
		),

		// 2 pages. A specific event with a specific panic, so it gets its own words.
		'cva-failed' => array(
			'tag'     => 'cd_cva_cta',
			'shape'   => 'phone',
			'eyebrow' => 'When an Arrangement Collapses',
			'title'   => 'Has Your CVA Failed or Started to Slip?',
			'body'    => 'Speak confidentially with an insolvency adviser about where a collapsed '
			           . 'arrangement leaves the company, and what options are still open.',
			'button'  => CD_ALT_CTA_BUTTON,
		),

		// 6 pages. Rule 4: never imply we can rule on the reader's personal liability.
		// The body says so outright rather than leaving it to be inferred.
		'personal-liability' => array(
			'tag'     => 'cd_personal_liability_cta',
			'shape'   => 'phone',
			'eyebrow' => 'Director Personal Risk',
			'title'   => 'Worried About Your Own Exposure?',
			'body'    => 'Whether a director is personally exposed depends on what was signed, '
			           . 'what was drawn out and how the company was run in the months before. '
			           . 'No general guide can settle that. Speak to a licensed insolvency '
			           . 'practitioner about the company&rsquo;s position first.',
			'button'  => CD_ALT_CTA_BUTTON,
		),

		// 2 pages. A partnership or LLP is not a limited company, so the test does not apply,
		// but the work is still ours.
		'partnership' => array(
			'tag'     => 'cd_partnership_cta',
			'shape'   => 'phone',
			'eyebrow' => 'Partnerships and LLPs',
			'title'   => 'Is the Business a Partnership or an LLP?',
			'body'    => 'Partnership and LLP insolvency runs on different rules from a limited '
			           . 'company, and the partners&rsquo; own position is part of the picture '
			           . 'from the start. We handle both.',
			'button'  => CD_ALT_CTA_BUTTON,
		),

		// The two below replace one "Does the Structure Need Specialist Handling?" block.
		// A charity and a group company are different problems with different readers, and
		// "structure" and "specialist handling" were both filing words. Compact, because
		// these three pages also carry the test and must not gain a second large block.

		// 2 pages. The reader may be a trustee rather than a director.
		'charity' => array(
			'tag'     => 'cd_charity_cta',
			'shape'   => 'phone_compact',
			'eyebrow' => 'Charities and Non-Profits',
			'title'   => 'Running a Charity That Cannot Pay Its Bills?',
			'body'    => 'Speak confidentially with an insolvency adviser about trustee duties, '
			           . 'restricted funds, and how charity insolvency differs from a '
			           . 'company&rsquo;s.',
			'button'  => CD_ALT_CTA_BUTTON,
		),

		// 1 page. The worry is what one liquidation does to the companies around it.
		'group-company' => array(
			'tag'     => 'cd_group_cta',
			'shape'   => 'phone_compact',
			'eyebrow' => 'Group Structures',
			'title'   => 'Liquidating One Company in a Group?',
			'body'    => 'Speak confidentially with an insolvency adviser about intra-group debts, '
			           . 'guarantees, and the knock-on effect on the other companies.',
			'button'  => CD_ALT_CTA_BUTTON,
		),

		// 9 pages. The reader is owed money. We are not selling insolvency work to a
		// creditor, so this points at the guide written for them and nothing else.
		'creditor' => array(
			'tag'     => 'cd_creditor_cta',
			'shape'   => 'link',
			'eyebrow' => 'Owed Money?',
			'title'   => 'Owed Money by an Insolvent Company?',
			'body'    => 'Where your claim sits in the queue, what to submit and what you are '
			           . 'realistically likely to recover depend on the type of debt and the '
			           . 'procedure the company is in.',
			'button'  => 'Read the guide for creditors',
			'url'     => '/insolvency/insolvent-company-owes-me-money/',
		),

		// 14 pages: tax investigations, penalties, compliance checks, security bonds. We do
		// not defend investigations. We do handle a company that cannot pay what comes out
		// of one, and that is the only thing this promises.
		'hmrc-affordability' => array(
			'tag'     => 'cd_hmrc_cta',
			'shape'   => 'link',
			'eyebrow' => 'If the Bill Cannot Be Paid',
			'title'   => 'Can the Company Afford What HMRC Is Asking For?',
			'body'    => 'A penalty, assessment or settlement often lands on a company with no '
			           . 'spare cash. Time to Pay, and what happens if HMRC turns it down, are '
			           . 'set out across our HMRC debt guides.',
			'button'  => 'See the HMRC debt options',
			'url'     => '/hmrc/hmrc-debt-enforcement-hub/',
		),

		// 1 page. Mixed solvent and insolvent closure intent, so neither the test nor the
		// solvent-closure block fits; the comparison guide does.
		'closure-options' => array(
			'tag'    => 'cd_closure_cta',
			'shape'  => 'link',
			'title'  => 'Not Sure Which Closure Route Fits?',
			'body'   => 'Strike-off, members&rsquo; voluntary liquidation and creditors&rsquo; '
			          . 'voluntary liquidation each suit a different financial position. Compare '
			          . 'them before you choose.',
			'button' => 'Compare closure options',
			'url'    => '/closing-a-limited-company/',
		),
	);
}

/**
 * Per-page wording, layered over the block's default. Keyed by slug.
 *
 * This exists because of a real editorial failure. The first version of the
 * process-advice block put one headline on 23 pages spanning company pensions, leases,
 * director conduct and winding-up orders, and that headline -- "Questions About a
 * Process Already Under Way?" -- was the internal filing label reworded. It spoke to
 * none of those readers, and it also assumed liquidation had started when the page
 * title alone never established that.
 *
 * A bucket in the review is a routing decision. It is not a reader. Where the bucket is
 * broad, the page gets its own headline and body here and only inherits the shape,
 * destination and button from the block.
 *
 * @return array<string, array{title?:string, body?:string, eyebrow?:string}>
 */
function cd_cta_page_copy() {
	return array(

		// Piers, 6 Aug 2026. Three different readers land here: someone weighing
		// liquidation up and researching the consequences, someone already in it, and a
		// director worried about their duties. The headline names the worry all three
		// share instead of asserting which one they are.
		'what-happens-after-company-liquidation' => array(
			'eyebrow' => '',
			'title'   => 'Concerned About What Happens After Liquidation?',
			'body'    => 'Speak confidentially with an insolvency adviser about director duties, '
			           . 'company debts, assets and what happens next.',
		),
	);
}

/**
 * Render one alternative CTA. Shared markup on purpose: these are seven wordings of the
 * same two cards, and a copy of the markup per block is seven places to fix a styling bug.
 */
function cd_cta_render_alt( $key, $context = '' ) {
	$set = cd_cta_alt_wording();
	if ( ! isset( $set[ $key ] ) ) { return ''; }
	$c = $set[ $key ];

	// Page-specific wording wins over the block default. Only the copy is overridden;
	// shape, destination and button label stay with the block so the action stays
	// consistent site-wide (plan section 10).
	if ( is_singular() ) {
		$slug = get_post_field( 'post_name', get_queried_object_id() );
		$copy = cd_cta_page_copy();
		if ( $slug && isset( $copy[ $slug ] ) ) {
			$c = array_merge( $c, array_filter( $copy[ $slug ], 'strlen' ) );
			// An explicitly empty eyebrow means "no eyebrow on this page", which
			// array_filter has just dropped. Honour it.
			if ( isset( $copy[ $slug ]['eyebrow'] ) && '' === $copy[ $slug ]['eyebrow'] ) {
				unset( $c['eyebrow'] );
			}
		}
	}

	// A guide block pointing at the page it sits on helps nobody.
	if ( isset( $c['url'] ) && cd_cta_points_here( $c['url'] ) ) { return ''; }

	cd_test_cta_enqueue();
	$tel   = CD_ADVICE_CTA_TEL;
	$shown = '0800 074 6757';
	$size  = ( 'phone' === $c['shape'] ) ? 'large' : 'compact';
	$track = cd_test_cta_track( $key, '', '', $size, $context );

	if ( 'phone' === $c['shape'] ) {
		$eyebrow = empty( $c['eyebrow'] ) ? ''
			: '<p class="cd-cta-full__eyebrow">' . $c['eyebrow'] . '</p>';
		return '<div class="cd-cta-shell"><div class="cd-cta-full cd-cta-full--advice cd-cta-full--guide">'
			. '<div class="cd-cta-full__content">'
			. $eyebrow
			. '<p class="cd-cta-full__title">' . $c['title'] . '</p>'
			. '<p class="cd-cta-full__body">' . $c['body'] . '</p>'
			. '<a class="cd-cta-full__btn" href="tel:' . esc_attr( $tel ) . '"' . $track . '>'
			. cd_test_cta_icon( 'phone' ) . $c['button'] . '</a>'
			. '<p class="cd-cta-full__reassure">Call <a href="tel:' . esc_attr( $tel ) . '">' . $shown . '</a>. '
			. '<strong>Confidential, and no obligation.</strong></p>'
			. '</div>'
			. '</div></div>';
	}

	$out = '<div class="cd-cta-shell"><div class="cd-cta-compact">';
	if ( ! empty( $c['eyebrow'] ) ) {
		$out .= '<p class="cd-cta-compact__eyebrow">' . $c['eyebrow'] . '</p>';
	}
	$out .= '<p class="cd-cta-compact__title">' . $c['title'] . '</p>'
	      . '<p class="cd-cta-compact__body">' . $c['body'] . '</p>';

	if ( 'phone_compact' === $c['shape'] ) {
		$out .= '<a class="cd-cta-compact__btn" href="tel:' . esc_attr( $tel ) . '"' . $track . '>'
		      . $c['button'] . '</a>'
		      . '<p class="cd-cta-compact__reassure"><span>Call ' . $shown . '</span>'
		      . '<span><strong>Confidential, and no obligation</strong></span></p>';
	} else {
		$out .= '<a class="cd-cta-compact__btn" href="' . esc_url( $c['url'] ) . '"' . $track . '>'
		      . $c['button'] . ' <span aria-hidden="true">&rarr;</span></a>';
	}

	return $out . '</div></div>';
}

/**
 * One shortcode per alternative CTA, registered from the wording set so adding a block
 * means adding one entry above rather than editing in two places.
 *
 * [cd_process_cta] [cd_personal_liability_cta] [cd_partnership_cta] [cd_specialist_cta]
 * [cd_creditor_cta] [cd_hmrc_cta] [cd_closure_cta]
 */
foreach ( cd_cta_alt_wording() as $cd_alt_key => $cd_alt ) {
	add_shortcode(
		$cd_alt['tag'],
		function ( $atts ) use ( $cd_alt_key ) {
			$atts = shortcode_atts( array( 'context' => '' ), $atts, 'cd_alt_cta' );
			return cd_cta_render_alt( $cd_alt_key, $atts['context'] );
		}
	);
}
unset( $cd_alt_key, $cd_alt );

/* ---------------------------------------------------------------------------
 * Placement
 *
 * The review decides WHAT each page gets. This decides WHERE it goes, following
 * section 11 of the wording plan: the leading block sits after the opening
 * explanation, the secondary one further down before the closing sections, and no
 * page carries two dominant blocks.
 *
 * Only pages with a reviewed decision are touched. An unreviewed page gets nothing,
 * which is the same rule the wording follows: silence beats a guess.
 * ------------------------------------------------------------------------ */

/**
 * The review's "Alternative primary CTA" column, mapped to the block that renders it.
 *
 * Three labels map to '' on purpose, not for want of copy: the 14 low-intent guidance
 * pages, the employee page and the IVA page were reviewed and decided to get nothing.
 * See the note above cd_cta_alt_wording(). Anything not listed at all is an unreviewed
 * label and gets nothing rather than a stand-in.
 */
function cd_cta_alternative_block( $alt ) {
	switch ( strtolower( trim( (string) $alt ) ) ) {
		case 'direct advice':
			return do_shortcode( '[cd_advice_cta]' );
		case 'solvent closure':
			return do_shortcode( '[cd_solvent_cta]' );
		case 'company assets':
			return cd_cta_render_alt( 'assets' );
		case 'process guidance':
			return cd_cta_render_alt( 'process-guidance' );
		case 'failed cva':
			return cd_cta_render_alt( 'cva-failed' );
		case 'personal-liability guidance':
			return cd_cta_render_alt( 'personal-liability' );
		case 'partnership advice':
			return cd_cta_render_alt( 'partnership' );
		case 'charity advice':
			return cd_cta_render_alt( 'charity' );
		case 'group company advice':
			return cd_cta_render_alt( 'group-company' );
		case 'creditor guidance':
			return cd_cta_render_alt( 'creditor' );
		case 'hmrc affordability':
			return cd_cta_render_alt( 'hmrc-affordability' );
		case 'closure options':
			return cd_cta_render_alt( 'closure-options' );
	}
	return '';
}

/**
 * Remove the CTA blocks left over from earlier systems: the hand-placed .cd-cta panels
 * and the Ultimate Blocks "Get a Quick and Easy Liquidation Quote" call-to-action.
 *
 * Done at render time on purpose. Rewriting the stored text of dozens of pages is a
 * one-way operation on content nobody has a backup of; this is reversible by deleting
 * one function. The stored text should still be cleaned up properly in its own pass.
 */
function cd_cta_strip_legacy( $content ) {
	if ( false === strpos( $content, 'cd-cta:' )
	  && false === strpos( $content, 'cd-cta--' )
	  && false === strpos( $content, 'ub_call_to_action' ) ) {
		return $content;
	}
	// The legacy blocks carry their own delimiting comments, so match those rather than
	// anything class-based: the current blocks share the cd-cta prefix and must survive.
	$content = preg_replace( '#<!--\s*cd-cta:[a-z-]+\s*-->.*?<!--\s*/cd-cta:[a-z-]+\s*-->#is', '', $content );
	// Undelimited older panels: the wrapper is exactly "cd-cta cd-cta--<variant>".
	$content = preg_replace( '#<div[^>]*class="cd-cta cd-cta--[^"]*"[^>]*>.*?</div>\s*</div>#is', '', $content );
	// Ultimate Blocks "Get a Quick and Easy Liquidation Quote".
	$content = preg_replace( '#<div[^>]*class="[^"]*ub_call_to_action[^"]*"[^>]*>.*?</div>\s*</div>#is', '', $content );
	return $content;
}

// Runs late on purpose: these blocks are added by something further down the filter
// chain than the placement below, so stripping them at the same time did nothing.
add_filter( 'the_content', 'cd_cta_strip_legacy', 99 );

add_filter( 'the_content', function ( $content ) {
	if ( ! is_singular() || ! is_main_query() ) { return $content; }

	// This theme renders the_content outside the formal loop, so in_the_loop() cannot
	// gate here. Compare ids instead: related-post snippets carry a different one.
	$id = get_queried_object_id();
	if ( get_the_ID() && get_the_ID() !== $id ) { return $content; }

	// Only a page that already places one of THESE blocks is left alone, to avoid
	// rendering it twice. Legacy CTA markup does not veto the reviewed decision — it
	// gets stripped below instead. (An earlier version of this guard also skipped on
	// legacy markup, which silently blocked the roll-out on every page still carrying
	// an old block. That was invented, not policy.)
	if ( false !== strpos( $content, 'cd-cta-shell' ) ) { return $content; }

	$entry = cd_test_cta_page_entry();
	if ( ! $entry ) { return $content; }

	list( $variant, $urgency, $size, $alt ) = array_pad( $entry, 4, '' );

	$lead = '';   // after the opening explanation
	$later = '';  // before the closing sections

	if ( 'none' === $variant ) {
		$lead = cd_cta_alternative_block( $alt );
	} elseif ( 'urgent_action' === $urgency ) {
		// Plan rule 3: on a deadline page direct contact leads and the test follows.
		$lead  = cd_cta_alternative_block( $alt ? $alt : 'direct advice' );
		$later = do_shortcode( '[cd_test_cta]' );
	} elseif ( 'compact' === $size ) {
		// A page can be reviewed as "the test helps, but something else should lead". The
		// three charity, non-profit and group-company pages are the only ones: the test
		// establishes severity, specialist advice remains the main action. 'Direct advice'
		// is excluded here on purpose — on a non-urgent page it is the fallback recorded
		// against most of the corpus, and promoting it would silently add a phone card to
		// eighty pages nobody reviewed for one.
		$leader = ( $alt && 'direct advice' !== strtolower( trim( $alt ) ) )
			? cd_cta_alternative_block( $alt )
			: '';
		if ( '' !== $leader ) { $lead = $leader; }
		$later = do_shortcode( '[cd_test_cta]' );
	} else {
		$lead = do_shortcode( '[cd_test_cta]' );
		$long = ( preg_match_all( '/<h2[ >]/i', $content ) >= 6 );
		if ( $long ) {
			// Plan section 11 allows one large block plus one compact reminder, and no
			// more. On a long guide a single CTA a quarter of the way in is easy to
			// scroll past and never see again.
			$later = do_shortcode( '[cd_test_cta size="compact"]' );
		}
	}

	if ( '' === $lead && '' === $later ) { return $content; }

	if ( ! preg_match_all( '/<h2[ >]/i', $content, $m, PREG_OFFSET_CAPTURE ) ) {
		return $content . $lead . $later;
	}
	$offsets = array();
	foreach ( $m[0] as $hit ) { $offsets[] = $hit[1]; }
	$count = count( $offsets );

	$needed = ( '' !== $lead && '' !== $later ) ? 3 : 2;
	if ( $count < $needed ) {
		return $content . $lead . $later;
	}

	$lead_at  = $offsets[1];            // before the second H2, i.e. after the opening section
	$later_at = $offsets[ $count - 1 ]; // before the last H2, usually the FAQ or related guides

	// Insert the later one first so the earlier offset stays valid.
	if ( '' !== $later ) {
		$content = substr( $content, 0, $later_at ) . $later . substr( $content, $later_at );
	}
	if ( '' !== $lead ) {
		$content = substr( $content, 0, $lead_at ) . $lead . substr( $content, $lead_at );
	}
	return $content;
}, 20 );
