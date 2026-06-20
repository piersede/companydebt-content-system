<?php if( have_rows('block_wysiwyg') ): ?>
<?php while( have_rows('block_wysiwyg') ): the_row(); ?>

<section class="wysiwyg <?php if ( get_sub_field( 'add_class' ) ) { the_sub_field( 'add_class' );
} ?>" <?php if ( get_sub_field( 'padding_top' ) || get_sub_field( 'padding_bottom' ) ) { ?> style="<?php if ( get_sub_field( 'padding_top' ) ) { ?>padding-top: <?php the_sub_field( 'padding_top' );?>px;<?php } ?><?php if ( get_sub_field( 'padding_bottom' ) ) { ?> padding-bottom: <?php the_sub_field( 'padding_bottom' );?>px; <?php } ?>
"<?php } ?>>
    <div class="content">
	    <?php the_sub_field( 'wysiwyg' ); ?>
    </div>
</section>

	<?php endwhile;
endif ?>