<?php if( have_rows('show_sectors_front_page_cd') ): ?>
	<?php while( have_rows('show_sectors_front_page_cd') ): the_row();


$featured_posts = get_sub_field('show_sectors_front_page_cd');

if ( ! empty( $featured_posts ) ): ?>
<section class="section-sectors">
        <div class="row posts">
		    <?php foreach( $featured_posts as $featured_post ):
			    $permalink = get_permalink( $featured_post->ID );
			    $title = get_field( 'featured_sector_title' , $featured_post);
			    ?>
                <div class="col-3">
                    <div class="sector-post">
                        <a href="<?php echo esc_url( $permalink ); ?>">
                            <div class="post">
			                    <?php echo get_the_post_thumbnail($featured_post->ID, 'blog_thumbnail'); ?>
                                <h3 class="post-title"><?php echo esc_html( $title ); ?></h3>
                            </div>
                        </a>
                    </div>

                </div>
		    <?php endforeach; ?>
        </div>
</section>

<?php endif; ?>

	<?php endwhile;
endif ?>
