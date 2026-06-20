<?php if( have_rows('block_hero_landing_blank') ): ?>
<?php while( have_rows('block_hero_landing_blank') ): the_row(); ?>

<section class="section-landing-blank-hero <?php if ( get_sub_field( 'add_class' ) ) { the_sub_field( 'add_class' );
} ?>" style="background-color: <?php the_sub_field( 'bcg_color' ); ?>; <?php if ( get_sub_field( 'padding_top' ) ) { ?>padding-top: <?php the_sub_field( 'padding_top' );?>px;<?php } ?><?php if ( get_sub_field( 'padding_bottom' ) ) { ?> padding-bottom: <?php the_sub_field( 'padding_bottom' );?>px; <?php } ?>">
    <div class="container">
        <div class="row">
            <div class="col-3">
                <div class="landing-blank-hero-logo">
	                <?php echo wp_get_attachment_image( get_sub_field( 'logo' ), 'full', false,  ["class" => "hero-logo-img"] ); ?>
                </div>
            </div>
            <div class="col-6 landing-blank-hero-middle">
                <div class="landing-blank-hero-middle-image">
	                <?php echo wp_get_attachment_image( get_sub_field( 'image' ), 'full', false,  ["class" => "hero-img"] ); ?>
                    <?php $hero_heading_tag = is_singular() ? 'h2' : 'h1'; ?>
                    <<?php echo esc_attr( $hero_heading_tag ); ?> class="landing-blank-hero-title">
	                    <?php the_sub_field( 'title' ); ?>
                    </<?php echo esc_attr( $hero_heading_tag ); ?>>
                    <p class="landing-blank-hero-desc">
	                    <?php the_sub_field( 'description' ); ?>
                    </p>
                </div>
            </div>
            <div class="col-3">
                <a href="tel:<?php the_sub_field( 'phone' );
                ?>" class="landing-blank-hero-phone">
	                <?php the_sub_field( 'phone' ); ?>
                </a>
            </div>
        </div>
    </div>
</section>

	<?php endwhile;
endif ?>