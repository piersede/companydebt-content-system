<?php
/**
 * Template Name: Front Page
 */


get_header();
if ( have_posts() ) { ?>

	<?php
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
