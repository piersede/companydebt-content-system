<?php if( have_rows('block_tilted_content_two_columns') ): ?>
<?php while( have_rows('block_tilted_content_two_columns') ): the_row(); ?>
<section class="section-tilted-content-two-cols <?php if ( get_sub_field( 'add_class' ) ) { the_sub_field( 'add_class' );
} ?>" <?php if (get_sub_field('background_color')) { ?> style="background-color: <?php the_sub_field('background_color'); } ?>">
    <div class="container">

        <div class="row">
            <div class="col-12">
		<?php if ( get_sub_field ('supertitle')) { ?>
                <div class="tilted-content-supertitle">
	                <?php the_sub_field( 'supertitle' ); ?>
                </div>
		<?php } ?>
		<?php if ( get_sub_field ('heading')) { ?>
            <div class="tilted-content-heading">
		            <?php the_sub_field( 'heading' ); ?>
                </div>
		<?php } ?>
		<?php if ( get_sub_field ('excerpt')) { ?>
                <div class="tilted-content-excerpt">
		            <?php the_sub_field( 'excerpt' ); ?>
                </div>
		<?php } ?>
		<?php if ( get_sub_field ('subheading')) { ?>
                <div class="tilted-content-subheading">
		            <?php the_sub_field( 'subheading' ); ?>
                </div>
		<?php } ?>
		<?php if ( get_sub_field ('content')) { ?>
                <div class="tilted-content-content">
		            <?php the_sub_field( 'content' ); ?>
                </div>
		<?php } ?>
            </div>
        </div>

    </div>
</section>
	<?php endwhile;
endif ?>