<?php if( have_rows('block_landing_insolvency_timeline') ): ?>
	<?php while( have_rows('block_landing_insolvency_timeline') ): the_row(); ?>
		<section class="section-block-landing-insolvency-timeline <?php if ( get_sub_field( 'add_class' ) ) { the_sub_field( 'add_class' );
		} ?>" <?php if ( get_sub_field( 'padding_top' ) || get_sub_field( 'padding_bottom' ) || get_sub_field( 'background_color' ) ) { ?> style="<?php if ( get_sub_field( 'padding_top' ) ) { ?>padding-top: <?php the_sub_field( 'padding_top' );?>px;<?php } ?><?php if ( get_sub_field( 'padding_bottom' ) ) { ?> padding-bottom: <?php the_sub_field( 'padding_bottom' );?>px; <?php } ?> <?php if ( get_sub_field( 'background_color' ) ) { ?> background-color: <?php the_sub_field( 'background_color' );?>; <?php } ?>
			"<?php } ?>>
			<div class="container">
				<div class="row">
					<div class="col-12">
						<?php
						// check if the repeater field has rows of data
						if ( have_rows('timeline_block') ):
							$counter = 0;
							// loop through the rows of data
							while ( have_rows('timeline_block') ) : the_row();
								$counter++;
								// display a sub field value
								?>
                                <div class="timeline-item">
                                    <div class="timeline-number"><?php echo $counter; ?></div>
                                    <div class="timeline-item-content">
                                        <div class="timeline-item-heading">
		                                    <?php the_sub_field( 'heading' ); ?>
                                        </div>
                                        <div class="timeline-item-description">
		                                    <?php the_sub_field( 'description' ); ?>
                                        </div>
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