<?php 
if( have_rows('block_carousel_testimonials_boxes') ): 
	$testmonials_query = new \WP_Query(
		array(
			'post_type'      => 'testimonial',
			'post_status'    => 'publish',
			'fields'         => 'ids',
			'posts_per_page' => get_field('block_carousel_testimonials_boxes')['nr_of_posts'] ?? 4
		)
	);
	
	?>
<?php while( have_rows('block_carousel_testimonials_boxes') ): the_row(); ?>
<section class="section-carousel-testimonials-landing <?php if ( get_sub_field( 'add_class' ) ) { the_sub_field( 'add_class' );
} ?>" <?php if ( get_sub_field( 'padding_top' ) || get_sub_field( 'padding_bottom' ) || get_sub_field( 'background_color' ) ) { ?> style="<?php if ( get_sub_field( 'padding_top' ) ) { ?>padding-top: <?php the_sub_field( 'padding_top' );?>px;<?php } ?><?php if ( get_sub_field( 'padding_bottom' ) ) { ?> padding-bottom: <?php the_sub_field( 'padding_bottom' );?>px; <?php } ?> <?php if ( get_sub_field( 'background_color' ) ) { ?> background-color: <?php the_sub_field( 'background_color' );?>; <?php } ?>
        "<?php } ?>>
	<div class="container">
		<div class="row">
            <div class="col-12">
                <h2 class="testimonial-carousel-heading">
		            <?php the_sub_field( 'heading' ); ?>
                </h2>
            </div>
			<div class="col-12 col-md-10">
				<?php if ( $testmonials_query->have_posts() ) : ?>
					<div class="testimonial-carousel__testimonials">
						<?php foreach ( $testmonials_query->posts as $testimonial_id ) : ?>
							<div class="testimonial-carousel__testimonial">
								<div class="testimonial-carousel__testimonial-inner">
									<div class="testimonial-rating">
										<img src="<?php echo esc_url( CD_THEME_URL . 'assets/images/stars.png' ) ?>" alt="5 Starts" width="123" height="21">
									</div>
									<div class="testimonial-content"><?php echo wp_kses_post( get_the_content( null, false, $testimonial_id ) ); ?></div>
									<div class="testimonial-meta">
										<span><?php the_field( 'name', $testimonial_id ); ?>,</span>
										<span><?php the_field( 'company', $testimonial_id ); ?></span>
									</div>
								</div>
							</div>
						<?php endforeach; ?>
					</div>
				<?php endif; ?>
			</div>
		</div>
	</div>
</section>
	<?php endwhile;
endif ?>