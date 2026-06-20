<?php $buttons_section = get_field('buttons_section'); ?>
<?php if( have_rows('buttons_section') ): ?>
<?php while( have_rows('buttons_section') ): the_row(); ?>

<?php 
    $align       = get_sub_field( 'text_align' ); 
    $num_of_cols = get_sub_field( 'nr_cols' );
?>

<section class="section-columns-buttons <?php if ( get_sub_field( 'add_class' ) ) { the_sub_field( 'add_class' );
} ?>" style="background-color: <?php the_sub_field('bcg_color'); ?>">
    <div class="container">
        <?php if ( get_sub_field ('title') ) { ?>
        <div class="row">
            <div class="col-12">
                <h2 class="section-title" style="color: <?php the_sub_field('title_font_color'); ?>">
	                <?php the_sub_field( 'title' ); ?>
                </h2>
            </div>
        </div>
        <?php } ?>
        <div class="row">
	        <?php
	        // check if the repeater field has rows of data
	        if ( have_rows('buttons') ):
		        // loop through the rows of data
		        while ( have_rows('buttons') ) : the_row();
			        // display a sub field value
			        ?>
                <div class="box-wrapper col-<?php echo ceil( 12 / $num_of_cols ); ?>">
                    <a href="<?php the_sub_field( 'link' ); ?>" class="box-link">
                       <div class="box <?php echo $align ?>" style="background-color: <?php echo $buttons_section['button_bcg_color']; ?>">
                           <div class="box-image">
		                       <?php echo wp_get_attachment_image( get_sub_field( 'icon' ), 'full', false,  ["class" => "box-img"] ); ?>
                           </div>
                           <div class="box-heading" style="color: <?php echo $buttons_section['title_font_color']; ?>"><?php the_sub_field( 'heading' ); ?></div>
                           <p class="box-desc" style="color: <?php echo $buttons_section['title_font_color']; ?>"><?php the_sub_field( 'description' ); ?></p>
                       </div>
                    </a>
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