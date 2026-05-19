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
						<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect class="li-square" x="0" y="0" width="24" height="24" rx="4"/><path class="li-in" transform="translate(5.875,2.8671875)" d="M0 0 C0.98484375 -0.00128906 1.9696875 -0.00257812 2.984375 -0.00390625 C4.02078125 -0.00003906 5.0571875 0.00382813 6.125 0.0078125 C7.67960938 0.00201172 7.67960938 0.00201172 9.265625 -0.00390625 C10.25046875 -0.00261719 11.2353125 -0.00132813 12.25 0 C13.16007812 0.00112793 14.07015625 0.00225586 15.0078125 0.00341797 C17.125 0.1328125 17.125 0.1328125 18.125 1.1328125 C18.22481214 3.8101263 18.26379875 6.45585425 18.25 9.1328125 C18.25580078 10.25816406 18.25580078 10.25816406 18.26171875 11.40625 C18.25161053 17.00620197 18.25161053 17.00620197 17.125 18.1328125 C15.50242456 18.2319782 13.87560169 18.26361027 12.25 18.265625 C11.26515625 18.26691406 10.2803125 18.26820312 9.265625 18.26953125 C8.22921875 18.26566406 7.1928125 18.26179688 6.125 18.2578125 C4.57039062 18.26361328 4.57039062 18.26361328 2.984375 18.26953125 C1.99953125 18.26824219 1.0146875 18.26695313 0 18.265625 C-0.91007813 18.26449707 -1.82015625 18.26336914 -2.7578125 18.26220703 C-4.875 18.1328125 -4.875 18.1328125 -5.875 17.1328125 C-5.97481214 14.4554987 -6.01379875 11.80977075 -6 9.1328125 C-6.00386719 8.38257813 -6.00773438 7.63234375 -6.01171875 6.859375 C-5.99935063 0.00743546 -5.99935063 0.00743546 0 0 Z"/></svg>
					</a>
					<a class="footer-author-icon footer-author-phone" href="tel:08000746757" aria-label="Call 0800 074 6757">
						<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect class="li-square" x="0" y="0" width="24" height="24" rx="4"/><path class="li-in" transform="translate(8,0)" d="M0 0 C0.99 2.97 1.98 5.94 3 9 C2.01 9.33 1.02 9.66 0 10 C0.70339566 12.50965614 0.70339566 12.50965614 2 15 C4.04105639 15.88693303 4.04105639 15.88693303 6 16 C6.33 15.01 6.66 14.02 7 13 C9.97 13.99 12.94 14.98 16 16 C16.36527887 20.50510605 16.36527887 20.50510605 14.7890625 22.640625 C11.8487087 24.87478029 9.07689099 24.46598123 5.50390625 24.3515625 C0.56694046 23.65838478 -2.12537929 20.9928127 -5.3125 17.375 C-7.70399297 14.00919508 -8.17784786 12.15713384 -8.25 8.0625 C-8.27578125 7.18722656 -8.3015625 6.31195312 -8.328125 5.41015625 C-8 3 -8 3 -6.65234375 1.1953125 C-4.39186011 -0.43993099 -2.72022409 -0.22055871 0 0 Z"/></svg>
					</a>
					<?php if ( $_li_url ) : ?>
					<a class="footer-author-icon footer-author-linkedin" href="<?php echo esc_url( $_li_url ); ?>" target="_blank" rel="noopener noreferrer" aria-label="<?php echo esc_attr( $author_fullname ); ?> on LinkedIn">
						<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect class="li-square" x="0" y="0" width="24" height="24" rx="4"/><path class="li-in" d="M7.119 20.452H3.555V9h3.564v11.452zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.063 2.063 0 112.063 2.065zM20.447 20.452h-3.554v-5.569c0-1.328-.024-3.037-1.852-3.037-1.853 0-2.137 1.445-2.137 2.939v5.667H9.351V9h3.414v1.561h.049c.477-.9 1.637-1.852 3.37-1.852 3.602 0 4.268 2.37 4.268 5.455v6.288z"/></svg>
					</a>
					<?php endif; ?>
				</div>
            </div>
		</div>
	</div>
</section>


