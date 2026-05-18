<?php
$author_id = get_the_author_meta('ID');
$author_nickname = get_the_author_meta('nickname');
$author_first_name = get_the_author_meta('first_name');
$author_fullname = get_the_author_meta('display_name');
?>
<section class="section-footer-author">
	<div class="container">
		<div class="row">
			<div class="col-auto">
				<?php echo wp_get_attachment_image( get_field( 'photo',  'user_'. $author_id ), 'full', false,  ["class" => "avatar-image", "alt" => "Avatar Image"] ); ?>
            </div>
			<div class="col-auto col-author-content">
				<div class="footer-author-eyebrow">ARTICLE WRITTEN BY</div>
				<div class="footer-author-name">
				<a href="<?php echo get_author_posts_url($author_id); ?>"><?php echo $author_fullname ?></a><span class="footer-author-position">, <?php echo trim( get_field('professional_position',  'user_'. $author_id ) ); ?></span>
				</div>
                <div class="social-media">
                    <a href="<?php the_field('linkedin',  'user_'. $author_id ); ?>"><img src="https://comdebstage.wpengine.com/wp-content/uploads/2022/03/linkedin_white_30.png" alt="5 Starts" width="30" height="30"></a>

                </div>
				<div class="footer-author-description"><?php the_field('director_description',  'user_'. $author_id ); ?></div>
            </div>
		</div>
	</div>
</section>


