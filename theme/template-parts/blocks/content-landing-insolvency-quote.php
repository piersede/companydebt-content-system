<?php if( have_rows('block_landing_insolvency_quote') ): ?>
	<?php while( have_rows('block_landing_insolvency_quote') ): the_row(); ?>
		<section class="section-block-landing-insolvency-quote <?php if ( get_sub_field( 'add_class' ) ) { the_sub_field( 'add_class' );
		} ?>" <?php if ( get_sub_field( 'padding_top' ) || get_sub_field( 'padding_bottom' ) || get_sub_field( 'background_color' )  ) { ?> style="background-color: <?php the_sub_field( 'background_color' ); ?>; <?php if ( get_sub_field( 'padding_top' ) ) { ?>padding-top: <?php the_sub_field( 'padding_top' );?>px;<?php } ?><?php if ( get_sub_field( 'padding_bottom' ) ) { ?> padding-bottom: <?php the_sub_field( 'padding_bottom' );?>px; <?php } ?>
			"<?php } ?>>
			<div class="container">
				<div class="row">
					<div class="col-12">
						<h2 class="insolvency-quote-section-title">
							<?php the_sub_field( 'title' ); ?>
						</h2>
						<div class="quote-inner">
							<div class="row">
								<div class="col-10">
									<?php the_sub_field( 'wysiwyg_left' ); ?>
								</div>
                                <div class="col-2">
	                                <?php echo wp_get_attachment_image( get_sub_field( 'photo' ), 'full', false,  ["class" => "quote-photo"] ); ?>
                                    <img src="<?php echo get_template_directory_uri(); ?>/assets/images/stars.png" alt="" class="quote-rating">
                                </div>
							</div>
						</div>
					</div>
				</div>
			</div>

		</section>
	<?php endwhile;
endif ?>