<?php if( have_rows('block_hero_landing') ): ?>
<?php while( have_rows('block_hero_landing') ): the_row(); ?>
<section class="section-hero-landing <?php if ( get_sub_field( 'add_class' ) ) { the_sub_field( 'add_class' );
} ?>" <?php if ( get_sub_field( 'padding_top' ) || get_sub_field( 'padding_bottom' ) ) { ?> style="<?php if ( get_sub_field( 'padding_top' ) ) { ?>padding-top: <?php the_sub_field( 'padding_top' );?>px;<?php } ?><?php if ( get_sub_field( 'padding_bottom' ) ) { ?> padding-bottom: <?php the_sub_field( 'padding_bottom' );?>px; <?php } ?>
        "<?php } ?>>
	<?php echo wp_get_attachment_image( get_sub_field( 'bcg_image' ), 'full', false,  ["class" => "hero-bg-img", "fetchpriority" => "high"] ); ?>
    <div class="container">
        <div class="row">
            <div class="col-6 col-6-left">
                <div class="site-branding">
		            <?php the_custom_logo(); ?>
                </div>
                <h1>
	                <?php the_sub_field( 'title' ); ?>
                </h1>
                <div class="hero-landing-content">
	                <?php the_sub_field( 'wysiwyg_left' ); ?>
                </div>
            </div>
            <div class="col-6 col-6-right">
                <div class="hero-col-right-top">
	                <?php echo wp_get_attachment_image( get_sub_field( 'logo_right' ), 'full', false,  ["class" => "hero-right-logo-img"] ); ?>
                    <div class="cdblk-hero-landing__separator"></div>
                    <a class="hero-landing-phone" href="tel:<?php the_field( 'header_phone_number', 'option' ); ?>ß">
	                    <?php the_field( 'header_phone_number', 'option' ); ?>
                    </a>
                </div>
	            <?php the_sub_field( 'wysiwyg_right' ); ?>

            </div>
        </div>
    </div>
</section>
        <section>
            <div class="container">
                <div class="logos">
	                <?php
	                // check if the repeater field has rows of data
	                if ( have_rows('logos_left') ):
		                // loop through the rows of data
		                while ( have_rows('logos_left') ) : the_row();
			                // display a sub field value
			                ?>
                              <div class="box-image">
							                <?php echo wp_get_attachment_image( get_sub_field( 'logo' ), 'full', false,  ["class" => "logo-box"] ); ?>
                              </div>

		                <?php
		                endwhile;
	                endif;
	                ?>
                </div>
            </div>
        </section>
	<?php endwhile;
endif ?>