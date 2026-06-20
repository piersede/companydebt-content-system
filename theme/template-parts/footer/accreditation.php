<?php if( have_rows('accreditation', 'option') ): ?>
<?php while( have_rows('accreditation', 'option') ): the_row(); ?>
<section class="section-footer-accreditation" aria-label="Accreditations and memberships">
    <div class="container">
        <div class="row">
            <div class="col-12">
                <div class="section-footer-accreditation-title">
	                <?php the_sub_field( 'title' ); ?>
                </div>
                    <ul class="logos">
	                    <?php
	                    // check if the repeater field has rows of data
	                    if ( have_rows('logos') ):
		                    // loop through the rows of data
		                    while ( have_rows('logos') ) : the_row();
			                    // display a sub field value
			                    ?>
                                <li class="logo-item"><?php echo wp_get_attachment_image( get_sub_field( 'logo' ), 'full', false,  ["class" => "accreditation-logo"] ); ?>
                                    </li>
		                    <?php
		                    endwhile;
	                    endif;
	                    ?>
                    </ul>
	            <?php if( get_sub_field('button') ): ?>
		            <?php $btn = get_sub_field( 'button' ); ?>
                   <a href="<?php echo $btn['url']; ?>" target="<?php echo $btn['target']; ?>" class="btn-footer-accreditation" aria-label="<?php echo esc_attr( $btn['title'] ); ?> about our accreditations and memberships"><?php echo $btn['title']; ?></a>
	            <?php endif; ?>
            </div>
        </div>
    </div>
</section>
	<?php endwhile;
endif ?>