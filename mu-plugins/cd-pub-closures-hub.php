<?php
/**
 * Plugin Name: CD Pub Closures Data Hub
 * Description: Front-end for /articles/pub-closures-in-the-uk/ (a post). Post content is
 *              KSES-filtered, so CSS + JS live in /assets and are injected here, plus a
 *              corrected Yoast title/description and Article + FAQPage JSON-LD.
 * Version:     2.1.0
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

function cd_pubhub_is_target() {
	if ( ! is_singular( 'post' ) ) { return false; }
	return 'pub-closures-in-the-uk' === get_post_field( 'post_name', get_queried_object_id() );
}

/* Full-width custom template for this post (no col-4 sidebar) */
add_filter( 'template_include', function ( $template ) {
	if ( cd_pubhub_is_target() ) {
		$t = __DIR__ . '/cd-pubhub/pub-closures-hub-template.php';
		if ( is_readable( $t ) ) { return $t; }
	}
	return $template;
}, 99 );

add_filter( 'body_class', function ( $classes ) {
	if ( cd_pubhub_is_target() ) { $classes[] = 'cd-pubhub-body'; }
	return $classes;
} );

add_action( 'wp_enqueue_scripts', function () {
	if ( ! cd_pubhub_is_target() ) { return; }
	// Brand font is Arial (system) - no web font needed.
}, 5 );

add_action( 'wp_head', function () {
	if ( ! cd_pubhub_is_target() ) { return; }
	$f = __DIR__ . '/pub-closures.css';
	if ( is_readable( $f ) ) { echo "\n<style id=\"cd-pub-hub-css\">\n" . file_get_contents( $f ) . "\n</style>\n"; }
}, 99 );

add_action( 'wp_footer', function () {
	if ( ! cd_pubhub_is_target() ) { return; }
	$f = __DIR__ . '/pub-closures.js';
	if ( is_readable( $f ) ) { echo "\n<script id=\"cd-pub-hub-js\">\n" . file_get_contents( $f ) . "\n</script>\n"; }
} );

add_filter( 'wpseo_title', function ( $t ) {
	return cd_pubhub_is_target() ? 'Pub Closures in the UK: How Many, and Why (2026 Data)' : $t;
}, 20 );
add_filter( 'wpseo_metadesc', function ( $d ) {
	return cd_pubhub_is_target() ? 'How many UK pubs have closed and why: current 2026 figures on pub numbers, permanent closures, hospitality insolvency and the cost pressures behind the decline.' : $d;
}, 20 );
/* OG + Twitter titles (Yoast keeps the old ones otherwise) */
add_filter( 'wpseo_opengraph_title', function ( $t ) {
	return cd_pubhub_is_target() ? 'Pub Closures in the UK: How Many, and Why (2026 Data)' : $t;
}, 20 );
add_filter( 'wpseo_twitter_title', function ( $t ) {
	return cd_pubhub_is_target() ? 'Pub Closures in the UK: How Many, and Why (2026 Data)' : $t;
}, 20 );
add_filter( 'wpseo_opengraph_desc', function ( $d ) {
	return cd_pubhub_is_target() ? 'Current 2026 figures on UK pub numbers, permanent closures, hospitality insolvency and the cost pressures behind the decline.' : $d;
}, 20 );

/* WP Schema Pro also emits an Article on this post; suppress it so Yoast's Article
   is the only one, alongside our Dataset + FAQPage (same approach as the data hub). */
add_filter( 'wp_schema_pro_schema_enabled', function ( $enabled, $post_id, $schema_type ) {
	return cd_pubhub_is_target() ? false : $enabled;
}, 10, 3 );
add_filter( 'wp_schema_pro_global_schema_enabled', function ( $enabled, $post_id, $type ) {
	return cd_pubhub_is_target() ? false : $enabled;
}, 10, 3 );

add_action( 'wp_head', function () {
	if ( ! cd_pubhub_is_target() ) { return; }
	$url = get_permalink();
	$csv = home_url( '/wp-content/uploads/2026/07/pub-closures-data.csv' );
	$graph = array(
		'@context' => 'https://schema.org',
		'@graph' => array(
			array(
				'@type' => 'Dataset',
				'name' => 'UK Pub Closures: Numbers, Permanent Losses, Insolvency and Costs (2000 to 2026)',
				'description' => 'A compiled dataset on the decline of UK pubs: long-run pub stock, permanent pub losses in England and Wales, hospitality company insolvency, the 2025 to 2026 cost stack (wages, employer National Insurance, business rates and alcohol duty), drinking behaviour and pint prices. Figures are drawn from the House of Commons Library, BBPA, the Insolvency Service, ONS, VOA, HMRC, GOV.UK and NHS England.',
				'url' => $url,
				'isAccessibleForFree' => true,
				'license' => 'https://creativecommons.org/licenses/by/4.0/',
				'creator' => array( '@type' => 'Organization', 'name' => 'Company Debt', 'url' => home_url( '/' ) ),
				'publisher' => array( '@type' => 'Organization', 'name' => 'Company Debt' ),
				'temporalCoverage' => '2000/2026',
				'spatialCoverage' => array( '@type' => 'Place', 'name' => 'United Kingdom' ),
				'dateModified' => get_the_modified_date( 'Y-m-d' ),
				'keywords' => array( 'UK pub closures', 'number of pubs', 'permanent pub losses', 'hospitality insolvency', 'business rates', 'alcohol duty', 'pub statistics' ),
				'variableMeasured' => array( 'Number of pubs in the UK', 'Permanent pub losses (England and Wales)', 'Pub closures per year and quarter', 'Accommodation and food service company insolvencies', 'Company insolvency rate per 10,000 businesses', 'Business births and deaths', 'Business rateable value change', 'Alcohol duty rates', 'Adults not drinking in the last 12 months', 'Average price of a pint' ),
				'distribution' => array(
					array( '@type' => 'DataDownload', 'encodingFormat' => 'text/csv', 'contentUrl' => $csv ),
				),
			),
			array(
				'@type' => 'FAQPage',
				'mainEntity' => array(
                array( '@type' => 'Question', 'name' => 'How many pubs are left in the UK?', 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => 'There were around 45,000 pubs in the UK in 2024, according to the House of Commons Library citing the British Beer and Pub Association, down from 60,800 in 2000. This is a stock figure for the whole UK, and it is a different measure from the number of pubs closing in any single year.' ) ),
                array( '@type' => 'Question', 'name' => 'How many pubs closed in 2025 and 2026?', 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => 'Ryan\'s analysis of government rating-list data put permanent pub losses in England and Wales at 366 in 2025. The BBPA counted 161 closures across Britain in the first quarter of 2026, up from 128 in the same quarter of 2025. The two use different definitions and cover different areas, so they will not match exactly.' ) ),
                array( '@type' => 'Question', 'name' => 'What is the main reason pubs are closing?', 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => 'There is no single cause. The measurable drivers are a rising cost stack, in higher wages, employer National Insurance, business rates and alcohol duty, landing at the same time as softer demand, particularly among younger adults. Accommodation and food service has had the highest company insolvency rate of any sector every year since 2015.' ) ),
                array( '@type' => 'Question', 'name' => 'Is a pub closure the same as an insolvency?', 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => 'No. A pub can close without any formal insolvency, and a pub company can become insolvent while its sites keep trading under a new owner. Insolvency Service figures count company insolvencies in the accommodation and food service sector, which is wider than pubs alone and is not a count of closed premises.' ) ),
                array( '@type' => 'Question', 'name' => 'What should I do if my pub cannot pay its debts?', 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => 'Get advice while you still have options. Depending on whether the business is viable, the routes include a Time to Pay arrangement with HMRC, a Company Voluntary Arrangement, administration, or a Creditors\' Voluntary Liquidation. If a winding-up petition has been threatened or issued, the timescale is short, so early advice from a licensed insolvency practitioner matters.' ) )
				),
			),
		),
	);
	echo '<script type="application/ld+json" id="cd-pub-hub-schema">' . wp_json_encode( $graph, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) . "</script>\n";
}, 31 );
