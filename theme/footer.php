<?php
/**
 * The template for displaying the footer
 *
 * Contains the closing of the #content div and all content after.
 *
 * @link https://developer.wordpress.org/themes/basics/template-files/#template-partials
 *
 * @package CompanyDebt
 */

global $post;

if ( $post && ( get_field( 'enable_related_articles', $post->ID ) || ! metadata_exists( 'post', $post->ID, 'enable_related_articles' ) ) ) {
    get_template_part( '/template-parts/related-articles/related-articles' );
}
?>
    <?php if ( ! is_page_template( 'templates/blank-landing-page.php' ) ) : ?>

	<footer id="colophon" class="site-footer">
		<?php if( current_user_can( 'administrator' ) ) { ?>
            <div class="chat-img">
                <img src="<?php echo esc_url( get_template_directory_uri(  ) . '/assets/images/chat-person.jpeg' ) ?>" height="60" width="60" alt="chat person" title="Company Debt chat" class="chat-person-img">

            </div>

		<?php } ?>

		<div class="container">
            <div class="row">
                <div class="col-6">
                    <div class="site-branding">
	                    <?php if ( is_page_template( 'templates/design-22-v1.php' ) ) { ?>
                        <a href="https://www.companydebt.com">
                            <img src="<?php echo esc_url( CD_THEME_URL . 'assets/images/logo-design22-1-text-pink.png' ); ?>" height="56" width="227" alt="Company Debt Logo" title="Company Debt" class="header__logo">
                        </a>
                        <?php } else { ?>
		                <?php the_custom_logo(); ?>
                        <?php } ?>
                    </div><!-- .site-branding -->
                    <div class="footer-tagline"><?php the_field( 'tagline', 'option' );?></div>
                </div>
                <div class="col-6">
                    <ul class="social-icons">
	                    <?php
	                    // check if the repeater field has rows of data
	                    if ( have_rows('socials', 'option') ):
		                    // loop through the rows of data
		                    while ( have_rows('socials', 'option') ) : the_row();
			                    // display a sub field value
			                    ?>
                                <li><a href="<?php the_sub_field( 'link' ); ?>"><?php echo wp_get_attachment_image( get_sub_field( 'icon' ), 'full', false,  ["class" => "social-media-icon"] ); ?>
                                    </a></li>
			                <?php
			                endwhile;
		                endif;
		                ?>
                    </ul>
                </div>
            </div>
            <div class="row">
                <div class="col-3">
                    <?php dynamic_sidebar( 'footer-section-1-sidebar' ); ?>
                </div>
                <div class="col-3">
                    <?php dynamic_sidebar( 'footer-section-2-sidebar' ); ?>
                </div>
                <div class="col-3">
                    <?php dynamic_sidebar( 'footer-section-3-sidebar' ); ?>
                </div>
                <div class="col-3">
                    <?php dynamic_sidebar( 'footer-section-4-sidebar' ); ?>
                </div>
                <div class="col-12">
                    <div class="footer_disclaimer"><a href="/privacy-policy/">Privacy Policy</a> | <a href="/terms-and-conditions/">Terms and Conditions</a> | <a href="/cookie-policy/">Cookie Policy</a> | <a href="/sitemap_index.xml">Site Map</a><br><br><?php the_field( 'disclaimer', 'option' ); ?></div>
                </div>
            </div>
        </div>
	</footer><!-- #colophon -->
    <?php endif; ?>
</div><!-- #page -->

<?php wp_footer(); ?>
<div id="back-to-top">
    <span class="back-top-top-btn">
        <img src="<?php echo esc_url( CD_THEME_URL . 'assets/images/white_arrow_up.svg' ); ?>" alt="Up">
    </span>
</div>
</body>
</html>
