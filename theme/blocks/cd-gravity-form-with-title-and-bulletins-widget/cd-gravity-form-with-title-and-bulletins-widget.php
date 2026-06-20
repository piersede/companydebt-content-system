<?php
/**
 * Testimonial Block template.
 *
 * @param array $block The block settings and attributes.
 */

if ( ( wp_is_mobile() && empty( get_field( 'show_on_mobile' ) ) ) ) {
    return;
}

$exclude_from_pages = (array) get_field( 'exclude_from_pages_on_mobile' );

if ( in_array( get_the_ID(), $exclude_from_pages ) ) {
    return;
}
?>
<!-- cache-check:1775135890 -->
<section class="section-cd-gravity-form-widget gf-widget">
    <div class="gf-widget-pill">Contact us</div>
	<?php if ( get_field( 'title' ) ) : ?>
        <h3><?php the_field( 'title' ); ?></h3>
	<?php endif; ?>
	<?php if ( get_field( 'description' ) ) : ?>
        <div class="cd-gravity-form-desc"><?php the_field( 'description' ); ?></div>
	<?php endif; ?>
    <div class="form">
		<?php echo do_shortcode( get_field( 'form_id' ) ); ?>
    </div>
    <div class="gf-widget-reassurance">100% Free and Confidential Advice</div>
    <script>document.addEventListener("DOMContentLoaded",function(){var e=document.querySelectorAll(".section-cd-gravity-form-widget .contact_disclaimer");e.forEach(function(el){el.style.setProperty("display","none","important")})});</script>
</section>