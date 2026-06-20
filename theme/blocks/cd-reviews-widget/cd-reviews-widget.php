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
    
    if ( have_rows( 'cd_reviews', 'options' ) ) : 
    ?>
    <section class="cd-reviews">
        <div class="container">
            <div class="row cd-reviews-wrapper">
                <div class="col-2 cd-reviews-total">
                    <div class="cd-rating-heading">Excellent</div>
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
                    <div class="cd-rating-average"><?php echo $avg_rating; ?> average</div>
                    <?php if ( ! empty( get_field( 'reviews_link', 'options' ) ) ) : ?>
                        <div class="cd-reviews-logo">
                            <a href="<?php echo esc_url( get_field( 'reviews_link', 'options' ) ); ?>" target="_blank">
                                <?php echo file_get_contents( CD_THEME_DIR . 'assets/images/reviewsio-logo.svg' ); ?>
                            </a>
                        </div>
                    <?php endif; ?>
                </div>
                <div class="col-10 cd-reviews-carousel">
                    <div class="cd-reviews-prev">
                        <svg fill="#000000" height="24px" width="24px" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
                            viewBox="0 0 330 330" xml:space="preserve">
                        <path id="XMLID_92_" d="M111.213,165.004L250.607,25.607c5.858-5.858,5.858-15.355,0-21.213c-5.858-5.858-15.355-5.858-21.213,0.001
                            l-150,150.004C76.58,157.211,75,161.026,75,165.004c0,3.979,1.581,7.794,4.394,10.607l150,149.996
                            C232.322,328.536,236.161,330,240,330s7.678-1.464,10.607-4.394c5.858-5.858,5.858-15.355,0-21.213L111.213,165.004z"/>
                        </svg>
                    </div>
                    <div class="row cd-reviews-items">
                        <?php while( have_rows('cd_reviews', 'options' ) ) : 
                            the_row(); 

                            $rating = get_sub_field( 'rating' );
                            $full_stars   = floor( $rating );
                            $partial_star = $rating - $full_stars;

                            $review_content = get_sub_field( 'review' );
                            ?>
                            <div class="cd-review-item col-3" data-index="<?php echo $counter; ?>">
                                <div class="cd-review-top">
                                    <span class="cd-review-by"><?php echo esc_html( get_sub_field( 'review_by' ) ); ?></span>
                                    <span class="cd-review-stars">
                                    <?php
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
                                    </span>
                                </div>
                                <?php if ( get_sub_field( 'verified_customer' ) ) : ?>
                                    <div class="cd-review-verifed-customer">
                                        <span class="verified-badge"><svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="currentColor" fill-rule="evenodd" d="M4.252 14H4a2 2 0 1 1 0-4h.252c.189-.734.48-1.427.856-2.064l-.18-.179a2 2 0 1 1 2.83-2.828l.178.179A8 8 0 0 1 10 4.252V4a2 2 0 1 1 4 0v.252c.734.189 1.427.48 2.064.856l.179-.18a2 2 0 1 1 2.828 2.83l-.179.178c.377.637.667 1.33.856 2.064H20a2 2 0 1 1 0 4h-.252a8 8 0 0 1-.856 2.064l.18.179a2 2 0 1 1-2.83 2.828l-.178-.179a8 8 0 0 1-2.064.856V20a2 2 0 1 1-4 0v-.252a8 8 0 0 1-2.064-.856l-.179.18a2 2 0 1 1-2.828-2.83l.179-.178A8 8 0 0 1 4.252 14M9 10l-2 2l4 4l6-6l-2-2l-4 4z"/></svg></span>
                                        <span>Verified Customer</span>
                                        </div>
                                <?php endif; ?>
                                <div class="cd-review-content"><?php echo esc_html( strlen( $review_content ) > 190 ? substr( $review_content, 0, 190 ) . '...' : $review_content ); ?></div>
                                <div class="cd-review-content-full"><?php echo esc_html( $review_content ); ?></div>
                                <?php if ( ! empty( get_sub_field( 'date_of_review' ) ) ) : ?>
                                    <div class="cd-review-bottom"><?php echo esc_html( human_time_diff( strtotime( get_sub_field( 'date_of_review' ) ) ) ); ?> ago</div>
                                <?php endif; ?>
                            </div>
                        <?php endwhile; ?>
                    </div>
                    <div class="cd-reviews-next">
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
        <div class="cd-review-details-popup-overlay"></div>
        <div class="cd-review-details-popup">
            <div class="cd-review-details-top">
                <span class="cd-review-close">
                    <svg width="24px" height="24px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M5 5L19 19M5 19L19 5" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </span>
            </div>
            <div class="cd-review-detail-main"></div>
        </div>
    </section>
<?php
endif;
