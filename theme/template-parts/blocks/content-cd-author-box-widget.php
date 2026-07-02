<?php
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

$args['selected_sidebar'] = get_field( 'select_sidebar' );
?>
            <div class="content-author">
                <div class="col-auto">
                    <div class="content-author-avatar">
                        <a href="<?php echo get_author_posts_url($author_id); ?>">
					        <?php echo wp_get_attachment_image( get_field( 'photo',  'user_'. $author_id ), 'full', false,  ["class" => "avatar-image", "alt" => "Avatar Image"] ); ?>
                        </a>
                    </div>
                </div>
                <div class="col-auto">
                    <div class="content-author-desc">
                        <div class="reviewed-by"><a href="<?php echo get_author_posts_url($author_id); ?>"><?php echo $author_fullname; ?></a></div>
                        <div class="author-position"><?php the_field('professional_position', 'user_'. $author_id ); ?></div>
                        <div class="date"><?php echo get_the_modified_date() ?></div>
                    </div>
                </div>
            </div>
