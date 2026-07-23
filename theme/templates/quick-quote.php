<?php
/**
 * Template Name: Quick Quote
 *
 * Cosmetic redesign of the /quick-quote/ page. Built in milestones; this
 * first version renders the existing page content unchanged so the template
 * swap can be verified as a no-op before any redesign is layered on.
 *
 * The page's original template assignment (Insolvency Landing Page) and its
 * Gutenberg content remain in the database untouched — reverting is a matter
 * of removing the template_include filter in functions.php (or reassigning
 * the page template in wp-admin).
 */

get_header();

if ( have_posts() ) {
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
