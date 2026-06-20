<?php
/**
 * Template Name: Landing Page
 */

get_header();
if ( have_posts() ) { ?>

	<?php
	while ( have_posts() ) {
		the_post();
		?>
		<style>
			.cdblk-hero-landing__newspapers {
				align-items: center;
				display: flex;
				flex-wrap: wrap;
				padding-bottom: 35px;
				padding-top: 25px;
				width: 60%;
			}
		</style>
		<div class="content-container--full-width">
			<?php the_content(); ?>
		</div>
		<?php
	}
}
get_footer();
//wp_footer();
