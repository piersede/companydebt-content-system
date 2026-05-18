<?php
$author_id = get_the_author_meta('ID');
$author_nickname = get_the_author_meta('nickname');
$author_first_name = get_the_author_meta('first_name');
$author_fullname = get_the_author_meta('display_name');

// Trust metadata pills shown below the credential line.
// Placeholder list for now; can be moved to an ACF user repeater field
// ('trust_pills') later for per-author customisation.
$_trust_pills = array(
    'Licensed by IPA',
    'ICAS Member',
    'TMA Member',
);
?>
<section class="section-footer-author">
	<div class="container">
		<div class="row">
			<div class="col-auto">
				<?php echo wp_get_attachment_image( get_field( 'photo',  'user_'. $author_id ), 'full', false,  ["class" => "avatar-image", "alt" => "Avatar Image"] ); ?>
            </div>
			<div class="col-auto col-author-content">
				<div class="footer-author-name">
				Written by <a href="<?php echo get_author_posts_url($author_id); ?>"><?php echo $author_fullname ?></a>
				</div>
				<div class="footer-author-position"><?php the_field('professional_position',  'user_'. $author_id ); ?></div>
				<?php if ( ! empty( $_trust_pills ) ) : ?>
				<div class="footer-author-trust-row">
					<?php foreach ( $_trust_pills as $_pill ) : ?>
						<span class="footer-author-trust-pill"><?php echo esc_html( $_pill ); ?></span>
					<?php endforeach; ?>
				</div>
				<?php endif; ?>
                <div class="social-media">
                    <a href="<?php the_field('linkedin',  'user_'. $author_id ); ?>"><img src="https://comdebstage.wpengine.com/wp-content/uploads/2022/03/linkedin_white_30.png" alt="5 Starts" width="30" height="30"></a>

                </div>
				<div class="footer-author-description"><?php the_field('director_description',  'user_'. $author_id ); ?></div>
			    <div class="footer-author-links">
                    <a href="/meet-the-team/">Meet our experts</a>
                    <a href="<?php echo get_author_posts_url($author_id); ?>">More from this author</a>
                </div>
            </div>
		</div>
	</div>
</section>


