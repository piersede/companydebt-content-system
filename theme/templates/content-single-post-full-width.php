<?php
/**
 * Template Name: Single Post Full Width
 * Template Post Type: post
 */

get_header();

if ( have_posts() ) { ?>
        <main id="primary" class="content site-main">
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
                    <div class="col-12 main-content">
                        <?php the_content(); ?>
                        <?php if ( have_rows('article_sources') ) { get_template_part( '/template-parts/footer/article-sources' );} ?>
                        <?php get_template_part( 'template-parts/social' ); ?>
                    </div>
                </div>
            </div>
        </main>
	<?php
}


get_template_part( '/template-parts/content', 'accreditation' );
get_template_part( '/template-parts/footer/footer-cta-block' );

get_footer();