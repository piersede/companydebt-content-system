<?php
/**
 * Template Name: Design 2022 Version 1
 */

get_header();

$bcg_image_id = get_post_thumbnail_id();
$bcg_srcset   = wp_get_attachment_image_srcset( $bcg_image_id );

if ( have_posts() ) {
	while ( have_posts() ) {
		the_post();
		?>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;300;400;500;600;700;900&display=swap');
        </style>

        <main id="primary" class="site-main">
            <div class="content">
                <section class="page-header">
	                <?php echo wp_get_attachment_image( get_post_thumbnail_id() ); ?>
                    <div class="container">
                        <div class="row">
                            <div class="col-12">
                                <h1 class="page-title"><?php the_title(); ?></h1>
                            </div>
                        </div>
                    </div>
                </section>
                <section class="section-design-22-content">
                    <div class="container">
                        <div class="row space-between">
                            <div class="col-8 main-content">
				                <?php the_content(); ?>
                            </div>
                            <div class="col-4">
                                <aside class="widget-area">
	                                <?php dynamic_sidebar( 'design22v1-sidebar' ); ?>
                                </aside>
                            </div>
                        </div>
                    </div>
                </section>

            </div>
        </main>


	<?php }
}

wp_print_styles( 'accreditation' );
get_template_part( 'template-parts/content', 'accreditation' );

wp_print_styles( 'site-footer' );
get_footer();

