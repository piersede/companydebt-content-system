<?php
/**
 * Template Name: Blank Landing Page (No header/footer)
 */
get_header();
if ( have_posts() ) {
//	wp_print_styles( 'styles' );
	wp_print_styles( 'blank-landing' );

	while ( have_posts() ) {
		the_post();
		?>
		<div class="content-container--full-width">
			<?php the_content(); ?>
		</div>
		<?php
	}
}
get_footer();
