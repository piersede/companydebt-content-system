<?php
wp_enqueue_style( 'review-author' );
$author_id = get_the_author_meta('ID');
$author_nickname = get_the_author_meta('nickname');
$author_fullname = get_the_author_meta('display_name');
/* Skip rendering entirely when the current context has no valid author
 * (page ID 0 / deleted user). Prevents theme from emitting broken
 * anchors like <a href="/author/">, which 404 in Ahrefs crawls.
 * Root cause was pages authored by users whose ID was 0. Added 2026-07-02. */
if ( empty( $author_id ) || ! ctype_digit( (string) $author_id ) || (int) $author_id <= 0 ) {
    return;
}

?>

<div class="content-author-rev">
	<div class="col-auto">
		<div class="content-icon">
			<img src="<?php echo esc_url( CD_THEME_URL . 'assets/images/companydebt-checkmark.svg?fresh' ) ?>" alt="reviewed-by" width="40" height="40">
		</div>
	</div>
	<div class="col-auto">
		<div class="content-author-desc">
			<div class="reviewed-author">
				<div class="reviewby">Reviewed by <?php if ( the_field ('reviewed_by_link','option') ) { ?> <div class="tooltip-review review-by-tooltip">
						<?php the_field('reviewed_by',  'option'); ?>
						<a href="<?php the_field('reviewed_by_link',  'option'); ?>">Read More</a>
					</div> <?php } ?>
				</div>
				<div class="link-author"> <?php echo $author_fullname; ?>
					<div class="tooltip-review author-bio-tooltip">
						<div class="content-author">
                            <div class="row">
                                <div class="col-4">
                                    <div class="content-author-avatar">
                                        <a href="<?php echo get_author_posts_url($author_id); ?>" aria-label="<?php echo esc_attr( $author_fullname ); ?>">
				                            <?php echo wp_get_attachment_image( get_field( 'photo',  'user_'. $author_id ), 'full', false,  ["class" => "avatar-image", "alt" => esc_attr( $author_fullname )] ); ?>
                                        </a>
                                    </div>
                                </div>
                                <div class="col-8">
                                    <div class="content-author-desc">
                                        <div class="reviewed-by">Reviewed by <a href="<?php echo get_author_posts_url($author_id); ?>"><?php echo $author_fullname; ?></a></div>
                                        <div class="social-media">
                                            <a href="<?php the_field('linkedin',  'user_'. $author_id ); ?>"><img src="<?php echo esc_url( CD_THEME_URL . 'assets/images/linkedin-square.svg' ) ?>" alt="5 Starts" width="20" height="20">
                                            </a>
                                        </div>

                                    </div>
                                </div>
                            </div>

                            <div class="row">
                                <div class="col-12">
                                    <div class="author-bio"><?php the_field('director_description',  'user_'. $author_id ); ?> </div>
                                    <a href="/meet-the-team/">Meet Our Experts</a>
                                </div>
                            </div>


						</div>
					</div>
				</div>
			</div>
			<div class="date"><?php echo get_the_modified_date() ?></div>
		</div>
	</div>

</div>