<?php if( have_rows('block_bottom_line') ): ?>
	<?php while( have_rows('block_bottom_line') ): the_row();  ?>
        <?php if (!get_sub_field('heading') ) { continue; } ?>
		<section class="section-bottom-line <?php if ( get_sub_field( 'add_class' ) ) { the_sub_field( 'add_class' );
		} ?>" style="border-left-color: <?php the_sub_field( 'border_color' ); ?>">
			<div class="container">
				<div class="row">
                    <div class="col-12">
                        <div class="bottom-line-heading">
	                        <?php the_sub_field( 'heading' ); ?>
                        </div>
                    </div>
                    <div class="bottom-line-content">
						<?php echo wp_get_attachment_image( get_sub_field( 'icon' ), array( get_sub_field( 'image_width'), 0 ), false,  ["class" => "bottom-line-img"] ); ?>
                        <div class="bottom-line-description">
							<?php the_sub_field( 'description' ); ?>
                        </div>
                    </div>
				</div>
			</div>
		</section>
	<?php endwhile;
	wp_enqueue_style( 'webp-js-scroll' );
	wp_enqueue_script( 'webp-js-scroll' );
endif ?>
