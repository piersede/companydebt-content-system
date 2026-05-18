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
				<div class="footer-author-social">
					<a class="footer-author-icon footer-author-email" href="/contact-us/" target="_blank" rel="noopener" aria-label="Contact us">
						<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect class="li-square" x="0" y="0" width="24" height="24" rx="3"/><path class="li-in" d="M5 7h14a1 1 0 0 1 1 1v.41l-8 4.8-8-4.8V8a1 1 0 0 1 1-1zm-1 3.58V16a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-5.42l-7.49 4.49a1 1 0 0 1-1.02 0L4 10.58z"/></svg>
					</a>
					<a class="footer-author-icon footer-author-phone" href="tel:08000746757" aria-label="Call 0800 074 6757">
						<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect class="li-square" x="0" y="0" width="24" height="24" rx="3"/><path class="li-in" d="M8.62 12.79a13.05 13.05 0 0 0 5.59 5.59l1.86-1.86a.97.97 0 0 1 1.02-.24c1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1v2.92c0 .55-.45 1-1 1A15 15 0 0 1 5 6.07c0-.55.45-1 1-1h2.92c.55 0 1 .45 1 1 0 1.24.2 2.45.57 3.57.11.35.03.74-.25 1.02l-1.62 1.62z" transform="translate(-1 -1)"/></svg>
					</a>
					<?php if ( $_li_url ) : ?>
					<a class="footer-author-icon footer-author-linkedin" href="<?php echo esc_url( $_li_url ); ?>" target="_blank" rel="noopener noreferrer" aria-label="<?php echo esc_attr( $author_fullname ); ?> on LinkedIn">
						<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect class="li-square" x="0" y="0" width="24" height="24" rx="3"/><path class="li-in" d="M7.119 20.452H3.555V9h3.564v11.452zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.063 2.063 0 112.063 2.065zM20.447 20.452h-3.554v-5.569c0-1.328-.024-3.037-1.852-3.037-1.853 0-2.137 1.445-2.137 2.939v5.667H9.351V9h3.414v1.561h.049c.477-.9 1.637-1.852 3.37-1.852 3.602 0 4.268 2.37 4.268 5.455v6.288z"/></svg>
					</a>
					<?php endif; ?>
				</div>
            </div>
		</div>
	</div>
</section>


