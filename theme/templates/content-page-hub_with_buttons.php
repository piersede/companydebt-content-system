<?php
/**
 * Template Name: Hub Page
 *
 * Full-width hub layout — no sidebar. Used for section index / hub pages
 * that render the wp:acf/hub-box card grid.
 *
 * @package CompanyDebt
 */

get_header();
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

                <div class="col-12 main-content content">
                    <?php
                    ob_start();
                    the_content();
                    $content = ob_get_clean();
                    echo toc_and_footnotes_in_content( $content );
                    ?>
                </div>
            </div>
        </div>
    </div>
</main>

<?php
get_template_part( '/template-parts/footer/footer-cta-block' );
get_template_part( '/template-parts/content', 'accreditation' );
get_footer();
