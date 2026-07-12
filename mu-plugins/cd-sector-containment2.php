<?php
/**
 * Plugin Name: CD -- Sector page containment (interim, pre-design)
 * Description: Interim CSS containment for the rebuilt /sectors/ (and
 *   /services-to/) pages while the Claude Design visual build is pending. The
 *   sector template runs global theme transforms (footer.php) that were built
 *   for the OLD sector design and have no matching CSS on the rebuilt pages, so
 *   they mangle the clean content. This neutralises the two that make the page
 *   look broken:
 *     1) cd-faq-icon: an injected FAQ icon rendering at ~946px (the giant icon).
 *     2) cd-callout-summary-cards: transforms .cd-callout--summary into a
 *        .cd-callout__grid of unstyled full-width cards; we hide the generated
 *        grid and show the original paragraphs as one clean box instead.
 *   Scoped to sector/services-to posts. Reversible: delete this file.
 *   Added 2026-07-11. Remove once Claude Design ships the sector styles.
 * Author: Company Debt
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

add_action( 'wp_head', function () {
	if ( ! ( is_singular( 'post' ) && ( in_category( 'sectors' ) || in_category( 'services-to' ) ) ) ) {
		return;
	}
	?>
<style id="cd-sector-containment">
/* 1) Hide the oversized injected FAQ icon (leftover old-sector decoration). */
.category-sectors .cd-faq-icon-wrap, .category-sectors .cd-faq-icon,
.category-services-to .cd-faq-icon-wrap, .category-services-to .cd-faq-icon { display: none !important; }

/* 2) Revert the summary-card transform to a single clean box. */
.category-sectors .cd-callout--summary .cd-callout__grid,
.category-services-to .cd-callout--summary .cd-callout__grid { display: none !important; }
body.category-sectors .cd-callout--summary > p,
body.category-sectors .cd-callout--summary[data-cd-summary-transformed] > p,
body.category-services-to .cd-callout--summary > p,
body.category-services-to .cd-callout--summary[data-cd-summary-transformed] > p { display: block !important; margin: 0 0 8px !important; }
.category-sectors .cd-callout--summary > p:last-child,
.category-services-to .cd-callout--summary > p:last-child { margin-bottom: 0 !important; }
.category-sectors .cd-callout--summary,
.category-services-to .cd-callout--summary {
	background: #f1f5f9 !important;
	border-left: 4px solid #0b2545 !important;
	border-radius: 6px !important;
	padding: 16px 20px !important;
	margin: 22px 0 !important;
	display: block !important;
}
</style>
	<?php
}, 99 );
