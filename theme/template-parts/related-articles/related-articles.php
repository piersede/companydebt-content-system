<?php
    global $redirect_plugin;
    $redirects = get_option( 'quickppr_redirects' );
    
    $related_articles = array();
    $heading          = '';

    global $post;

    if ( $post && in_array( $post->post_type, array( 'post', 'page' ), true ) ) {
        $related_articles = get_field( 'be_related_articles', $post->ID );

        // Defensive: ACF stores hand-picked post IDs; skip any that aren't currently
        // published (drafts/trash/deleted IDs render as ?page_id=N → 404).
        if ( is_array( $related_articles ) ) {
            $related_articles = array_values( array_filter( $related_articles, function ( $rid ) {
                $rid = is_object( $rid ) ? (int) $rid->ID : (int) $rid;
                return $rid && get_post_status( $rid ) === 'publish';
            } ) );
        }

        if ( empty( $related_articles )  ) {
            $query_args = array(
                'post_type'      => $post->post_type,
                'post_status'    => 'publish',
                'posts_per_page' => 4,
                'fields'         => 'ids',
                'orderby'        => 'rand',
            );

            if ( $post->post_parent ) {
                $query_args['post_parent'] = $post->post_parent;
            } else {
                $cats = get_the_category( $post );

                if ( ! empty( $cats ) ) {
                    $query_args['category__in'] = wp_list_pluck( $cats, 'term_id' );
                }
            }
           
            if ( ! empty( $query_args['post_parent'] ) || ! empty( $query_args['category__in'] ) ) {
                $query = new \WP_Query( $query_args );
               
                if ( $query->have_posts() ) {
                    $related_articles = $query->get_posts();
                }
            }
        }
    }

    // Heading is locked site-wide to 'Related Articles' — the per-post ACF
    // override (be_related_articles_heading) is intentionally ignored.
    $heading = 'Related Articles';
?>
<?php 
if ( ! empty( $related_articles ) ) : 
    $total_articles = count( $related_articles );    
    ?>
<section class="be-related-articles has-carousel">
    <div class="container">
        <div class="row">
            <div class="col-12 text-center">
                <div class="related-articles-eyebrow">Continue reading</div>
                <h3 class="section-articles-title"><?php echo wp_kses_post( strip_tags( $heading, '<strong>' ) ); ?></h3>
            </div>
        </div>
        <div class="row articles-row">
                <div class="articles-carousel">
                <div class="carousel-prev">
                    <svg fill="#000000" height="24px" width="24px" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
                        viewBox="0 0 330 330" xml:space="preserve">
                    <path id="XMLID_92_" d="M111.213,165.004L250.607,25.607c5.858-5.858,5.858-15.355,0-21.213c-5.858-5.858-15.355-5.858-21.213,0.001
                        l-150,150.004C76.58,157.211,75,161.026,75,165.004c0,3.979,1.581,7.794,4.394,10.607l150,149.996
                        C232.322,328.536,236.161,330,240,330s7.678-1.464,10.607-4.394c5.858-5.858,5.858-15.355,0-21.213L111.213,165.004z"/>
                    </svg>
                </div>
                <div class="carousel-items">
	        <?php foreach ( $related_articles as $related_article_id ) :
		        $post_author = get_post_field( 'post_author', $related_article_id );
		        $user        = get_user_by( 'id', $post_author );

		        $author = $user->first_name . ' ' . $user->last_name;

		        if ( empty( trim( $author ) ) ) {
			        $author = $user->display_name;
		        }

                $thumbnail = '<img src="' . CD_THEME_URL . 'assets/images/business-banking.jpg" alt="' . get_the_title( $related_article_id ) . '">';

                if ( has_post_thumbnail( $related_article_id ) ) {
                    $thumbnail = get_the_post_thumbnail( $related_article_id, 'full' );
                }

                $link = get_permalink( $related_article_id );

                if ( $redirect_plugin && function_exists( 'cd_get_real_link' ) ) {
                    $link = cd_get_real_link( $link, $redirects );
                }
		        ?>
            <div class="col-3 carousel-item">
                <article>
                    <?php echo wp_kses_post( $thumbnail ); ?>
                    <div class="article-body">
                        <a href="<?php echo esc_url( $link ); ?>"><div class="article-title"><?php echo esc_html( get_the_title( $related_article_id ) ); ?></div></a>
                        <div class="article-meta">
                            <span class="meta-author">
                                <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H3zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/></svg>
                                <?php echo esc_html( $author ); ?>
                            </span>
                            <span class="meta-divider" aria-hidden="true"></span>
                            <span class="meta-date">
                                <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5zM1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4H1z"/></svg>
                                <?php echo esc_html( get_the_modified_date( 'j M Y', $related_article_id ) ); ?>
                            </span>
                        </div>
                    </div>
                    <a href="<?php echo esc_url( $link ); ?>" class="anchor-box-link"></a>
                </article>
            </div>
	        <?php endforeach; ?>
                </div>
                <div class="carousel-next">
                    <svg fill="#000000" height="24px" width="24px" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
                        viewBox="0 0 330 330" xml:space="preserve">
                    <path id="XMLID_92_" d="M111.213,165.004L250.607,25.607c5.858-5.858,5.858-15.355,0-21.213c-5.858-5.858-15.355-5.858-21.213,0.001
                        l-150,150.004C76.58,157.211,75,161.026,75,165.004c0,3.979,1.581,7.794,4.394,10.607l150,149.996
                        C232.322,328.536,236.161,330,240,330s7.678-1.464,10.607-4.394c5.858-5.858,5.858-15.355,0-21.213L111.213,165.004z"/>
                    </svg>
                </div>
                </div>
        </div>
    </div>

</section>
<?php endif; ?>