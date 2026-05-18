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
				<div class="footer-author-eyebrow">Article written by</div>
				<div class="footer-author-name">
				<a href="<?php echo get_author_posts_url($author_id); ?>"><?php echo $author_fullname ?></a><span class="footer-author-position">, <?php echo trim( get_field('professional_position',  'user_'. $author_id ) ); ?></span>
				</div>
				<div class="footer-author-description"><?php the_field('director_description',  'user_'. $author_id ); ?></div>
				<?php $_li_url = trim( (string) get_field( 'linkedin', 'user_'. $author_id ) ); ?>
				<?php if ( $_li_url ) : ?>
				<div class="footer-author-social">
					<a class="footer-author-linkedin" href="<?php echo esc_url( $_li_url ); ?>" target="_blank" rel="noopener noreferrer" aria-label="<?php echo esc_attr( $author_fullname ); ?> on LinkedIn">
						<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.024-3.037-1.852-3.037-1.853 0-2.137 1.445-2.137 2.939v5.667H9.351V9h3.414v1.561h.049c.477-.9 1.637-1.852 3.37-1.852 3.602 0 4.268 2.37 4.268 5.455v6.288zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.063 2.063 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
					</a>
				</div>
				<?php endif; ?>
            </div>
		</div>
	</div>
</section>


