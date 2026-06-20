<?php 
    $reviews = get_field( 'cd_reviews', 'options' );

    if ( empty( $reviews ) ) {
        return;
    }

    $total_reviews      = count( $reviews );
    $total_rating_score = 0.00;
    foreach ( $reviews as $review ) {
        $total_rating_score += floatval( $review['rating'] );
    }

    $avg_rating = floatval( $total_rating_score / $total_reviews );

    $counter = 0;

    $link = get_field( 'reviews_link', 'options' );
    
    if ( have_rows( 'cd_reviews', 'options' ) ) : 
    ?>
    <section class="cd-reviews-sidebar">
        <div class="container">
        <?php if ( $link ) : ?>
            <a href="<?php echo esc_url( get_field( 'reviews_link', 'options' ) ); ?>" target="_blank">
            <?php endif; ?>
            <div class="row cd-reviews-sidebar-wrapper">
                <div class="col-6 cd-reviews-sidebar-total">
                    <div class="cd-reviews-sidebar-logo">
                            <?php echo file_get_contents( CD_THEME_DIR . 'assets/images/reviewsio-logo.svg' ); ?>
                    </div>
                </div>
                <div class="col-6">
                    <div class="cd-reviews-sidebar-meta">
                        <div class="cd-reviews-sidebar-total-label">
                            <?php 
                                printf( 
                                    'Read our <strong>%d</strong> reviews',
                                    (int) $total_reviews
                                )
                            ?>
                        </div>
                        <div class="cd-review-stars">
                            <?php
                                $full_stars   = floor( $avg_rating );
                                $partial_star = $avg_rating - $full_stars;
                                for ( $i = 1; $i <= 5; $i++ ) {
                                    if ( $i <= $full_stars ) {
                                        echo '<div class="star full"></div>';
                                    } elseif ( $i == $full_stars + 1 && $partial_star > 0 ) {
                                        $percentage = round( $partial_star * 100 );
                                        echo '<div class="star perc-' . $percentage . '"></div>';
                                    } else {
                                        echo '<div class="star"></div>';
                                    }
                                }
                            ?>
                        </div>
                    </div>
                </div>
            </div>
            <?php if ( $link ) : ?>
            </a>
            <?php endif; ?>
        </div>
    </section>
<?php
endif;
