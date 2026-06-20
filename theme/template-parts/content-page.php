<?php
/**
 * Template part for displaying page content in page.php
 *
 * @link https://developer.wordpress.org/themes/basics/template-hierarchy/
 *
 * @package CompanyDebt
 */

?>

<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
<!--	<header class="entry-header">-->
<!--		--><?php //the_title( '<h1 class="entry-title">', '</h1>' ); ?>
<!--	</header>-->
<!---->
<!--	--><?php //company_debt_webpigment_post_thumbnail(); ?>

	<div class="entry-content">
	<?php 
		ob_start();
		the_content(); 
		$content = ob_get_clean();
		
		echo toc_and_footnotes_in_content( $content );

		wp_link_pages(
			array(
				'before' => '<div class="page-links">' . esc_html__( 'Pages:', 'company-debt-webpigment' ),
				'after'  => '</div>',
			)
		);
		?>
	</div><!-- .entry-content -->


</article><!-- #post-<?php the_ID(); ?> -->
