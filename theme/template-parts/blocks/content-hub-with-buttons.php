<section class="section-hub-with-buttons">
    <div class="container">
        <div class="row">
	        <?php
	        // check if the repeater field has rows of data
	        if ( have_rows('post_buttons') ):
	        // loop through the rows of data
	        while ( have_rows('post_buttons') ) : the_row();
	        // display a sub field value
	        ?>
                <div class="col-4">
                    <a href="<?php the_sub_field( 'link' ); ?>">
                        <div class="hub-box">
	                       <div class="hub-box-top">
		                       <?php if ( get_sub_field ('select_icon_or_image') == 0) { ?>
                                   <div class="bg-image"><?php echo wp_get_attachment_image( get_sub_field( 'media_file' ), 'full', false,  ["class" => "box-img"] ); ?>
                                   </div> <?php } else { ?>
			                       <?php echo wp_get_attachment_image( get_sub_field( 'media_file' ), 'full', false,  ["class" => "box-icon"] ); ?>
		                       <?php } ?>
                               <h3 class="box-heading"><?php the_sub_field( 'title' ); ?></h3>
                               <?php if ( get_sub_field ('description')) { ?>
                               <div class="box-content"><?php the_sub_field( 'description' ); ?>
                               </div>
	                        <?php } ?>
                           </div>
                            <div class="hub-box-bottom">
                                <div class="read-more-btn"><?php the_sub_field( 'read_more' ); ?>
                            </div>
                            </div>
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