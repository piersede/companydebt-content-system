<?php if( have_rows('article_sources')  ): ?>
	<?php while( have_rows('article_sources') && (get_field('article_sources')['title'] )  ): the_row();  ?>
		<?php if (!get_sub_field('content') )  { continue; } ?>
	<section class="section-article-sources">
        <div class="container">
            <div class="row">
                <div class="col-12">
                    <div class="article-sources-title">
	                    <?php the_sub_field( 'title' ); ?>
                    </div>
                    <div class="article-sources-content">
		                <?php the_sub_field( 'content' ); ?>
                    </div>
                </div>
            </div>
        </div>
    </section>
	<?php endwhile;
endif ?>

