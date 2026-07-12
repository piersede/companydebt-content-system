<?php
/**
 * Plugin Name: CD -- Gravity Forms lead journey in notifications
 * Description: Adds a "Lead journey" block to the TEAM notification email for
 *   every Gravity Form, site-wide, so you can see WHERE a visitor was before
 *   they filled the form -- not just the form's own page.
 *
 *   It reads the first-party attribution cookies set by the theme's
 *   assets/js/cd-attribution.js (the "Lead-source attribution" block in
 *   functions.php, added 2026-07-09). Those cookies travel with the
 *   submission POST, so they are available here at notification time -- unlike
 *   the entry META, which functions.php only writes on gform_after_submission,
 *   AFTER notifications have already been sent.
 *
 *   Surfaced (only lines that have a value are shown):
 *     - Page before the form  (cd_cta_origin_url + placement + link text)
 *     - Session landing page   (cd_landing_url)
 *     - Referrer               (cd_referrer_domain, e.g. google.com / (direct))
 *     - Form page              ($entry['source_url'] -- always present)
 *     - Campaign / click IDs   (cd_utm_* , gclid/gbraid/wbraid/msclkid/fbclid)
 *
 *   IMPORTANT limitation (by design of the capture script): the journey
 *   cookies are CONSENT-GATED (fail-closed) and the "page before" is only set
 *   when the visitor clicked an internal CTA. When there is no journey data we
 *   say so explicitly, so a blank is never mistaken for a bug.
 *
 *   Only internal/team notifications are touched (recipient not routed to a
 *   form field), so the enquirer's autoresponder is never affected.
 *
 *   Added 2026-07-10. Self-contained -- safe to remove as one file.
 * Author: Company Debt
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

add_filter( 'gform_notification', 'cd_add_lead_journey_to_notification', 10, 3 );

/**
 * Build an absolute URL from a stored path-or-URL value.
 */
function cd_lj_abs_url( $path_or_url ) {
	$v = trim( (string) $path_or_url );
	if ( '' === $v ) {
		return '';
	}
	if ( preg_match( '#^https?://#i', $v ) ) {
		return esc_url_raw( $v );
	}
	return esc_url_raw( home_url( '/' === substr( $v, 0, 1 ) ? $v : '/' . $v ) );
}

/**
 * Read one attribution cookie, trimmed.
 */
function cd_lj_cookie( $suffix ) {
	$k = 'cd_' . $suffix;
	return isset( $_COOKIE[ $k ] ) ? trim( wp_unslash( $_COOKIE[ $k ] ) ) : '';
}

/**
 * Append the visitor's journey to internal (team) notifications.
 *
 * @param array $notification
 * @param array $form
 * @param array $entry
 * @return array
 */
function cd_add_lead_journey_to_notification( $notification, $form, $entry ) {

	// Skip autoresponders sent back to the enquirer (routed to a form field).
	$to_type = isset( $notification['toType'] ) ? $notification['toType'] : '';
	if ( 'field' === $to_type ) {
		return $notification;
	}

	$rows = array();

	// 1) The page they were on before the form (the useful bit).
	$origin = cd_lj_cookie( 'cta_origin_url' );
	if ( '' !== $origin ) {
		$url    = cd_lj_abs_url( $origin );
		$extras = array();
		$place  = cd_lj_cookie( 'cta_origin_placement' );
		$text   = cd_lj_cookie( 'cta_text' );
		if ( '' !== $place ) { $extras[] = esc_html( $place ) . ' link'; }
		if ( '' !== $text )  { $extras[] = '&ldquo;' . esc_html( $text ) . '&rdquo;'; }
		$suffix = $extras ? ' <span style="color:#666;">(' . implode( ' &middot; ', $extras ) . ')</span>' : '';
		$rows['Page before the form'] = sprintf( '<a href="%1$s">%1$s</a>%2$s', $url, $suffix );
	}

	// 2) Session landing page (first page of the visit).
	$landing = cd_lj_cookie( 'landing_url' );
	if ( '' !== $landing ) {
		$url = cd_lj_abs_url( $landing );
		$rows['Session landing page'] = sprintf( '<a href="%1$s">%1$s</a>', $url );
	}

	// 3) Referrer domain.
	$ref = cd_lj_cookie( 'referrer_domain' );
	if ( '' !== $ref ) {
		$rows['Came from'] = esc_html( $ref );
	}

	// 4) Form page itself (native, always present).
	$source_url = isset( $entry['source_url'] ) ? trim( $entry['source_url'] ) : '';
	if ( '' !== $source_url ) {
		$safe = esc_url( $source_url );
		$rows['Form page'] = sprintf( '<a href="%1$s">%1$s</a>', $safe );
	}

	// 5) Campaign / click IDs, if any.
	$channel = array();
	foreach ( array( 'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term' ) as $k ) {
		$v = cd_lj_cookie( $k );
		if ( '' !== $v ) { $channel[] = esc_html( $k ) . '=' . esc_html( $v ); }
	}
	foreach ( array( 'gclid', 'gbraid', 'wbraid', 'msclkid', 'fbclid' ) as $k ) {
		if ( '' !== cd_lj_cookie( $k ) ) { $channel[] = esc_html( $k ); }
	}
	if ( $channel ) {
		$rows['Campaign'] = implode( ' &middot; ', $channel );
	}

	// Assemble. Distinguish "no journey captured" from a missing feature.
	$has_journey = ( '' !== $origin || '' !== $landing || '' !== $ref );

	$html  = '<div style="margin-top:20px;padding-top:14px;border-top:1px solid #e0e0e0;font-size:14px;">';
	$html .= '<p style="margin:0 0 8px;"><strong>Lead journey</strong></p>';
	$html .= '<table cellpadding="0" cellspacing="0" style="font-size:14px;line-height:1.5;">';
	foreach ( $rows as $label => $value ) {
		$html .= '<tr>'
			. '<td style="padding:2px 12px 2px 0;color:#666;vertical-align:top;white-space:nowrap;">' . esc_html( $label ) . '</td>'
			. '<td style="padding:2px 0;vertical-align:top;">' . $value . '</td>'
			. '</tr>';
	}
	$html .= '</table>';
	if ( ! $has_journey ) {
		$html .= '<p style="margin:8px 0 0;color:#888;font-style:italic;">'
			. 'No journey data captured &mdash; the visitor either declined analytics cookies '
			. 'or reached the form directly (no internal CTA click).</p>';
	}
	$html .= '</div>';

	$notification['message'] = (string) $notification['message'] . $html;

	return $notification;
}
