<?php
/**
 * The template for displaying all single posts
 *
 * @link https://developer.wordpress.org/themes/basics/template-hierarchy/#single-post
 *
 * @package CompanyDebt
 */

get_header();
?>

	<main id="primary" class="site-main">
		<?php get_template_part( 'template-parts/header-image' ); ?>

		<?php
		while ( have_posts() ) :
			the_post();

			get_template_part( 'template-parts/content', get_post_type() );



//			// If comments are open or we have at least one comment, load up the comment template.
//			if ( comments_open() || get_comments_number() ) :
//				comments_template();
//			endif;

		endwhile; // End of the loop.
		?>

	</main><!-- #main -->

<?php

if ( ! is_singular( 'testimonial' ) ) {
	get_template_part( '/template-parts/footer/footer-author' );
}
get_template_part( '/template-parts/footer/footer-cta-block' );
get_template_part( '/template-parts/footer/accreditation' );

get_footer();
