<?php
/**
 * Template Name: Form Letter Sample
 */

get_header();

if ( have_posts() ) { ?>

	<?php
	?>
	<div class="content-container--full-width">
		<?php
		while ( have_posts() ) {
			the_post();
			$args['selected_sidebar'] = get_field( 'select_sidebar' );
			?>
			<div class="content-container">
                <div class="content">
	                <?php get_template_part( 'template-parts/header-image' ); ?>
                    <div class="container form-letter__container">
                        <div class="row">
                            <div class="col-12 page-header">
			                    <?php
			                    if ( function_exists( 'yoast_breadcrumb' ) ) {
				                    yoast_breadcrumb( '<div class="breadcrumbs">', '</div>' );
			                    }

			                    ?>
                                <h1 class="post-title"><?php the_title(); ?></h1>
                                <div><?php the_content(); ?></div>
                            </div>

                        </div>
                </div>
				<?php
				get_template_part( 'template-parts/sidebar', null, $args );
				?>
			</div>
		<?php } ?>
	</div>
	<?php
}

get_template_part( 'template-parts/footer/footer-author' );

get_template_part( 'template-parts/footer/footer-cta-block' );

get_footer();

