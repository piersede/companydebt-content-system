<?php
/**
 * The template for displaying all pages
 *
 * This is the template that displays all pages by default.
 * Please note that this is the WordPress construct of pages
 * and that other 'pages' on your WordPress site may use a
 * different template.
 *
 * @link https://developer.wordpress.org/themes/basics/template-hierarchy/
 *
 * @package CompanyDebt
 */

get_header();
$author_id = get_the_author_meta('ID');
$author_nickname = get_the_author_meta('nickname');
$args['selected_sidebar'] = get_field( 'select_sidebar' );

?>

<main id="primary" class="site-main">
    <div class="content">
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
                <div class="col-8 main-content">
	                <?php
	                get_template_part( '/template-parts/review-author' );
	                ?>
					<?php 
                        ob_start();
                        the_content(); 
                        $content = ob_get_clean();
                        
                        echo toc_and_footnotes_in_content( $content );
                    ?>
	                <?php if ( have_rows('article_sources') ) { get_template_part( '/template-parts/footer/article-sources' );} ?>
                </div>
                <div class="col-4">
                    <aside class="widget-area">
	                    <?php dynamic_sidebar( 'sidebar-primary' ); ?>
                    </aside>
                </div>
            </div>
        </div>
    </div>
</main>

<?php

get_template_part( '/template-parts/footer/footer-author' );
get_template_part( '/template-parts/footer/footer-cta-block' );
get_template_part( '/template-parts/content', 'accreditation' );
get_footer();

