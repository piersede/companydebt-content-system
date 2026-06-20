<?php /* Updated: 2026-03-31T10:48:40.483Z */ ?>
<?php
    if ( ( wp_is_mobile() && empty( get_field( 'show_on_mobile' ) ) ) ) {
        return;
    }

    $exclude_from_pages = (array) get_field( 'exclude_from_pages_on_mobile' );

    if ( in_array( get_the_ID(), $exclude_from_pages ) ) {
        return;
    }
?>
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
</section>
