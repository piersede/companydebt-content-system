<?php if( have_rows('hub_boxes') ): ?>
	<?php while( have_rows('hub_boxes') ): the_row(); ?>
		<section class="section-hub-boxes">
			<h2 class="screen-reader-text">Sections</h2>
			<div class="container">
				<div class="row">
					<?php
					// check if the repeater field has rows of data
					if ( have_rows('boxes') ):
						// loop through the rows of data
						while ( have_rows('boxes') ) : the_row();
							// display a sub field value
							?>
                            <div class="col-4">
                                <div class="hub-box">
										<?php if ( get_sub_field ('icon') ) { ?>
                                            <div class="bg-image"><?php echo wp_get_attachment_image( get_sub_field( 'icon' ), 'full', false,  ["class" => "box-img"] ); ?>
                                            </div> <?php }  ?>
                                    <div class="hub-box-content">
                                        <h3 class="box-heading"><?php the_sub_field( 'heading' ); ?></h3>
	                                    <?php if( get_sub_field( 'content' ) ) {?>
                                            <div class="box-content"><?php the_sub_field( 'content' ); ?></div>
	                                    <?php } ?>

	                                    <?php if( get_sub_field( 'list_item' ) ) {?>
                                            <ul>
			                                    <?php
			                                    // check if the repeater field has rows of data
			                                    if ( have_rows('list_item') ):
				                                    // loop through the rows of data
				                                    while ( have_rows('list_item') ) : the_row();
					                                    // display a sub field value
					                                    ?>
                                                        <li>
                                                            <a href="<?php the_sub_field( 'url' ); ?>">
							                                    <?php the_sub_field( 'title' ); ?>
                                                            </a>
                                                        </li>
				                                    <?php
				                                    endwhile;
			                                    endif;
			                                    ?>
                                            </ul>
		                                    <?php if( get_sub_field( 'view_all' ) ) {?>
                                                <a class="box-link"><?php the_sub_field( 'link_view_all' ); ?></a>
		                                    <?php } ?>
	                                    <?php } ?>
                                    </div>

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