<?php
/**
 * Template Name: Full Width Page
 */

get_header();
?>
<main id="primary" class="section-full-width-page site-main">
	<?php get_template_part( 'template-parts/header-image' ); ?>
	<div class="container">
		<div class="row">
			<div class="col-12 page-header">
				<?php
				if ( function_exists( 'yoast_breadcrumb' ) ) {
					yoast_breadcrumb( '<div class="breadcrumbs">', '</div>' );
				}

				?>
				<h1 class="post-title"><?php the_title(); ?></h1>
			</div>
			<div class="col-12 main-content content">
				<?php the_content(); ?>
			</div>
		</div>
	</div>
</main>
<?php
/* Skip the "Get in Touch Today" CTA on pages that already have their own form
 * in the main content — duplicating the CTA below would be redundant.
 *  - 57472: /contact-us/
 *  - 57942: /stressed-directors-guide/
 * Other pages on this template (/site-map/, future additions) still get it. */
if ( ! is_page( array( 57472, 57942 ) ) ) {
    get_template_part( '/template-parts/footer/footer-cta-block' );
}
get_footer();
?>