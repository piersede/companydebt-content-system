<section class="section-hero-blue <?php if ( get_sub_field( 'add_class' ) ) { the_sub_field( 'add_class' );
} ?>">
	<div class="container">
		<?php if( have_rows('block_hero_blue') ): ?>
        <?php while( have_rows('block_hero_blue') ): the_row(); ?>
		<div class="row">
			<div class="col-6-hero-blue">
				<h1 class="hero-blue-title">
					<?php the_sub_field( 'title' ); ?>
				</h1>
				<div class="hero-blue-desc">
					<?php the_sub_field( 'wysiwyg_left' ); ?>
				</div>
			</div>
            <?php
if ( !wp_is_mobile() ) { ?>
			<div class="col-6-hero-blue">
				<?php echo wp_get_attachment_image( get_sub_field( 'image' ), 'full', false,  ["class" => "hero-blue-image", "alt" => "CompanyDebt HomePage"] ); ?>
			</div>
            <?php } ?>
		</div>
    <?php endwhile;
    endif ?>
	</div>
</section>