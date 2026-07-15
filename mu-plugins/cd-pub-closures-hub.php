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
	return cd_pubhub_is_target() ? 'UK Pub Closures 2026: Latest Figures and Reasons' : $t;
}, 20 );
add_filter( 'wpseo_metadesc', function ( $d ) {
	return cd_pubhub_is_target() ? '161 pubs closed across Britain in the first quarter of 2026. See the latest UK pub closure, insolvency and cost data, and why pubs are under pressure.' : $d;
}, 20 );
/* OG + Twitter titles (Yoast keeps the old ones otherwise) */
add_filter( 'wpseo_opengraph_title', function ( $t ) {
	return cd_pubhub_is_target() ? 'UK Pub Closures 2026: Latest Figures and Reasons' : $t;
}, 20 );
add_filter( 'wpseo_twitter_title', function ( $t ) {
	return cd_pubhub_is_target() ? 'UK Pub Closures 2026: Latest Figures and Reasons' : $t;
}, 20 );
add_filter( 'wpseo_opengraph_desc', function ( $d ) {
	return cd_pubhub_is_target() ? '161 pubs closed across Britain in the first quarter of 2026. See the latest UK pub closure, insolvency and cost data, and why pubs are under pressure.' : $d;
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
                array( '@type' => 'Question', 'name' => 'How many pubs are left in the UK in 2026?', 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => 'The latest full UK estimate puts the number of pubs at around 45,000, but this figure relates to 2024 rather than 2026. It is down from 60,800 in 2000 and 55,400 in 2010. No newer UK-wide stock total has been published, so 45,000 is the most current reliable estimate rather than a confirmed 2026 count.' ) ),
                array( '@type' => 'Question', 'name' => 'How many UK pubs closed in 2025?', 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => 'Rating-list analysis found 366 pubs were permanently lost in England and Wales during 2025, meaning they were demolished or converted to other uses rather than temporarily closed. Separately, insolvencies among pub, bar and nightclub operators rose to 789 across Britain in the year to 31 December 2025. These measures count different events and should not be added together.' ) ),
                array( '@type' => 'Question', 'name' => 'How many pubs closed in the first quarter of 2026?', 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => 'The British Beer and Pub Association recorded 161 pub closures across Britain in the first three months of 2026, almost two a day and 26% more than the 128 recorded in the same quarter of 2025. The BBPA estimated those closures cost around 2,400 jobs. This is a single-quarter figure and should not be read as a full-year total.' ) ),
                array( '@type' => 'Question', 'name' => 'Why are so many pubs closing in the UK?', 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => 'There is no single cause. Labour costs, employer National Insurance, business rates and alcohol duty have all risen together, while alcohol consumption has fallen, particularly among younger adults. Accommodation and food services has recorded the highest company insolvency rate of any sector every year since 2015, which shows how little margin many venues have to absorb rising costs.' ) ),
                array( '@type' => 'Question', 'name' => 'Is a pub closure the same as a pub-company insolvency?', 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => 'No. A pub can close without any formal insolvency, and a pub company can enter insolvency while its sites keep trading under a new operator. Closure counts record premises going dark, while insolvency figures record companies entering a formal procedure. The 3,296 accommodation and food insolvencies in the year to May 2026 also cover hotels and restaurants, not pubs alone.' ) ),
                array( '@type' => 'Question', 'name' => 'Which parts of the UK are losing the most pubs?', 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => 'Every region of England and Wales lost pubs in 2025. The steepest declines were in the East Midlands, the North West, and Yorkshire and the Humber. Exact pub counts by region are not published in the underlying rating-list source, so we name the hardest-hit regions rather than giving precise regional figures that cannot be verified.' ) ),
                array( '@type' => 'Question', 'name' => 'What should a pub director do if the business cannot pay its debts?', 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => 'Get advice early, while options remain open. The first question is whether the pub is viable before debt repayments, tax arrears or an unsustainable lease. Depending on the answer, routes include a Time to Pay arrangement with HMRC, a Company Voluntary Arrangement, administration, or a Creditors\' Voluntary Liquidation. If a winding-up petition is threatened, the timescale is short, so speak to a licensed insolvency practitioner quickly.' ) )
				),
			),
		),
	);
	echo '<script type="application/ld+json" id="cd-pub-hub-schema">' . wp_json_encode( $graph, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) . "</script>\n";
}, 31 );
