<?php if( have_rows('left_right_wyswyg_and_background_image') ): ?>
<?php while( have_rows('left_right_wyswyg_and_background_image') ): the_row(); ?>
<section class="section-left-right-wyswyg-and-background-image  <?php the_sub_field( 'orientation' ); ?> <?php if ( get_sub_field( 'add_classes' ) ) { the_sub_field( 'add_classes' );
} ?>">
	<?php echo wp_get_attachment_image( get_sub_field( 'image' ), 'full', false,  ["class" => "img"] ); ?>
    <div class="container">
        <div class="row">
            <div class="col-6 col-6-content">
                <div class="content">
	                <?php the_sub_field( 'wyswyg' ); ?>
                </div>
            </div>
        </div>
    </div>
</section>
	<?php endwhile;
endif ?>