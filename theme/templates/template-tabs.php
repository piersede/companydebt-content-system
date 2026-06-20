<?php 
/* 
 * Template Name: Tabbed Link List 
 */

get_header();

if ( have_posts() ) : ?>
	<?php
	while ( have_posts() ) :
		the_post();
		?>
		<main class="tabs-template">
            <div class="tabs-header" style="background-image: url(<?php echo esc_url( get_the_post_thumbnail_url( get_the_ID(), 'full' ) ); ?>); background-color: <?php the_field( 'header_background_color' ); ?>">
                <h1><?php the_title(); ?></h1>
            </div>
			<?php the_content(); ?>
        </main>
		<?php
	endwhile;
endif;

get_footer();
