<?php if( have_rows('block_landing_accordion') ): ?>
	<?php while( have_rows('block_landing_accordion') ): the_row(); ?>

		<section class="section-block-landing-insolvency-accordion <?php if ( get_sub_field( 'add_class' ) ) { the_sub_field( 'add_class' );
		} ?>" style="background-color: <?php the_sub_field( 'background_color' ); ?>;">
			<div class="container">
				<div class="row">
					<div class="col-12">
						<h2 class="insolvency-accordion-section-title"><?php the_sub_field( 'title' ); ?></h2>

						<?php
						// check if the repeater field has rows of data
						if ( have_rows('accordion') ):
							// loop through the rows of data
							while ( have_rows('accordion') ) : the_row();
								// display a sub field value
								?>
								<div class="accordion-item">
									<div class="accordion-item-header closed">
                                        <div class="accordion-title-img">
                                            <img src="<?php echo get_template_directory_uri(); ?>/assets/images/sign-plus.png" alt="" width="55px" height="45px" class="quote-rating">
                                        </div>
										<h3 class="accordion-title">
											<?php the_sub_field( 'heading' ); ?>
										</h3>
									</div>
									<div class="accordion-description closed">
										<?php the_sub_field( 'description' ); ?>
									</div>
								</div>
							<?php
							endwhile;
						endif;
						?>
					</div>
				</div>
			</div>
		</section>

	<?php endwhile;
endif ?>


<script>
    (function ($) {
        $(document).ready(function () {
            const accordionItem = $('.accordion-item');
            accordionItem.on('click', function () {
                $(this)
                    .children('.accordion-description')
                    .slideToggle(300)
                    .toggleClass('closed');
                $(this).toggleClass('closed');
            });
        });
    })(jQuery);
</script>

