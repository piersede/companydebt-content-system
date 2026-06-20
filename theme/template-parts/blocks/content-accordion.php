<?php if( have_rows('block_accordion') ): ?>
<?php while( have_rows('block_accordion') ): the_row(); ?>
<section class="section-accordion <?php if ( get_sub_field( 'add_class' ) ) { the_sub_field( 'add_class' );} ?>">
	<div class="container">
		<div class="row">
			<div class="col-12">
				<?php
				// check if the repeater field has rows of data
				if ( have_rows('accordion') ):
				// loop through the rows of data
				while ( have_rows('accordion') ) : the_row();
				// display a sub field value
				?>
				<div class="accordion-item">
					<div class="accordion-item-header closed">
                    <?php if ( get_sub_field ('icon') ) { ?>
						<div class="accordion-title-img">
							<?php echo wp_get_attachment_image( get_sub_field( 'icon' ), 'full', false,  ["class" => "accordion-icon"] ); ?>
						</div>
						<?php } ?>
						<div class="accordion-title">
							<?php the_sub_field( 'heading' ); ?>
						</div>
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
