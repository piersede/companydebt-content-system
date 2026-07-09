<?php
/**
 * Full-bleed template for the Pub Closures data hub (post 24589).
 * Loaded via template_include from cd-pub-closures-hub.php (not the editor).
 *
 * Unlike the default single-post template, this does NOT render the theme's
 * light page-header. The design supplies its own warm hero (H1, standfirst,
 * byline, KPI strip) from the post content, and the page renders full-bleed on
 * the warm data-hub background. Only a slim breadcrumb bar is kept for SEO/nav.
 *
 * @package CompanyDebt
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

get_header();

while ( have_posts() ) :
	the_post();
	?>
	<main class="site-main cd-hub-page">
		<div class="cd-hub-crumb">
			<div class="cd-hub-crumb__in">
				<?php
				if ( function_exists( 'yoast_breadcrumb' ) ) {
					yoast_breadcrumb( '<div class="breadcrumbs">', '</div>' );
				}
				?>
			</div>
		</div>
		<?php the_content(); ?>
	</main>
	<?php
endwhile;

if ( ! is_singular( 'testimonial' ) ) {
	get_template_part( '/template-parts/footer/footer-author' );
}
get_template_part( '/template-parts/footer/footer-cta-block' );
get_template_part( '/template-parts/footer/accreditation' );

get_footer();
