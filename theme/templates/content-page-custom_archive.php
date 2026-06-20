<?php
/**
 * Template Name: Hub
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
get_template_part( '/template-parts/footer/footer-cta-hub-block' );
get_footer();
?>