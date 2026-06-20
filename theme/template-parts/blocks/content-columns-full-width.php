<?php
$section_bg = get_field('columns_full_width')['section_heading']['colors']['background_color'];
$supertitle_color = get_field('columns_full_width')['section_heading']['colors']['supertitle_color'];
$title_color = get_field('columns_full_width')['section_heading']['colors']['title_color'];
$box_bg = get_field('columns_full_width')['section_heading']['colors']['box_color'];
$box_text_color = get_field('columns_full_width')['section_heading']['colors']['text_color'];

if( have_rows('columns_full_width') ): ?>
<?php while( have_rows('columns_full_width') ): the_row(); ?>
<section class="section-columns-full-width <?php if ( get_sub_field( 'add_classes' ) ) { the_sub_field( 'add_classes' );
} ?>" style="background-color: <?php echo $section_bg; ?>">
    <div class="container">
        <div class="row">
            <div class="col-12 text-center">
		<?php if( have_rows('section_heading') ): ?>
			<?php while( have_rows('section_heading') ): the_row(); ?>
				<?php if ( get_sub_field ('supertitle')) { ?>
                <div class="section-supertitle" style="color: <?php echo $supertitle_color; ?>"><?php the_sub_field( 'supertitle' ); ?></div>
				<?php } ?>
					<?php if ( get_sub_field ('title')) { ?>
	            <h3 class="section-title" style="color: <?php echo $title_color; ?>"><?php the_sub_field( 'title' ); ?></h3>
					<?php } ?>
						<?php if ( get_sub_field ('description')) { ?>
                <div class="description" style="color: <?php echo $title_color; ?>"><?php the_sub_field( 'description' ); ?></div>
						<?php } ?>
			<?php endwhile;
		endif ?>
            </div>
        </div>
        <div class="row boxes" style = "color: <?php echo $box_text_color; ?>">
	        <?php
	        // check if the repeater field has rows of data
	        if ( have_rows('items') ):
	        // loop through the rows of data
	        while ( have_rows('items') ) : the_row();
	        // display a sub field value
	        ?>
            <div class="col-3" style="background-color: <?php echo $box_bg; ?>">
                <div class="box">
	                <?php echo wp_get_attachment_image( get_sub_field( 'image' ), 'full', false,  ["class" => "box-img"] ); ?>
                    <?php if ( get_sub_field ('heading')) { ?>
                    <div class="box-title"><?php the_sub_field( 'heading' ); ?></div>
	            <?php } ?>
		        <?php if ( get_sub_field ('description')) { ?>
                    <div class="box-description"><?php the_sub_field( 'description' ); ?></div>
		        <?php } ?>
                </div>
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