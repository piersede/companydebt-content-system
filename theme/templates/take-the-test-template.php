<?php
/**
 * Template Name: Take The Test Template
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

                    <?php
                    // Hero author block -- only renders if author has a name
                    $_hero_author_id = get_the_author_meta('ID');
                    if ( $_hero_author_id ) {
                        $_hero_author_name = get_the_author_meta('display_name', $_hero_author_id);
                        if ( $_hero_author_name ) {
                            $_hero_author_photo_id = get_field('photo', 'user_'. $_hero_author_id);
                            $_hero_author_position = get_field('professional_position', 'user_'. $_hero_author_id);
                            ?>
                            <div class="hero-author">
                                <?php if ( $_hero_author_photo_id ) {
                                    echo wp_get_attachment_image( $_hero_author_photo_id, 'thumbnail', false, ["class" => "hero-author-photo", "alt" => esc_attr($_hero_author_name)] );
                                } ?>
                                <div class="hero-author-meta">
                                    <div class="hero-author-name"><?php echo esc_html($_hero_author_name); ?></div>
                                    <?php if ( $_hero_author_position ) { ?>
                                        <div class="hero-author-position"><?php echo esc_html($_hero_author_position); ?></div>
                                    <?php } ?>
                                </div>
                            </div>
                            <?php
                        }
                    }
                    ?>


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
	                    <?php dynamic_sidebar( 'sidebar-take-the-test' ); ?>
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

