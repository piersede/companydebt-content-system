<?php
/**
 * Template Name: About Us Page
 */


get_header();
if ( have_posts() ) { ?>

	<?php
	while ( have_posts() ) {
		the_post();
		?>

<main id="primary" class="section-full-width-page section-about-content site-main">
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
	}
}
//get_template_part( '/template-parts/footer/accreditation' );
get_template_part( '/template-parts/footer/footer-cta-block' );
get_footer();
?>


