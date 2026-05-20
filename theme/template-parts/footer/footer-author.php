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
				<div class="footer-author-name"><?php echo esc_html( $author_fullname ); ?></div>
				<div class="footer-author-position"><?php echo trim( get_field('professional_position',  'user_'. $author_id ) ); ?></div>
				<div class="footer-author-description"><?php the_field('director_description',  'user_'. $author_id ); ?></div>
				<?php $_li_url = trim( (string) get_field( 'linkedin', 'user_'. $author_id ) ); ?>
				<div class="footer-author-social">
					<a class="footer-author-icon footer-author-email" href="/contact-us/" target="_blank" rel="noopener" aria-label="Contact us">
						<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect class="li-square" x="0" y="0" width="24" height="24" rx="4"/><path class="li-in" transform="translate(4 4) scale(.667)" d="M22,5V9L12,13,2,9V5A1,1,0,0,1,3,4H21A1,1,0,0,1,22,5ZM2,11.154V19a1,1,0,0,0,1,1H21a1,1,0,0,0,1-1V11.154l-10,4Z"/></svg>
					</a>
					<a class="footer-author-icon footer-author-phone" href="tel:08000746757" aria-label="Call 0800 074 6757">
						<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect class="li-square" x="0" y="0" width="24" height="24" rx="4"/><path class="li-in" transform="translate(4 4) scale(.667)" d="M21.384,17.752a2.108,2.108,0,0,1-.522,3.359,7.543,7.543,0,0,1-5.476.642C10.5,20.523,3.477,13.5,2.247,8.614a7.543,7.543,0,0,1,.642-5.476,2.108,2.108,0,0,1,3.359-.522L8.333,4.7a2.094,2.094,0,0,1,.445,2.328A3.877,3.877,0,0,1,8,8.2c-2.384,2.384,5.417,10.185,7.8,7.8a3.877,3.877,0,0,1,1.173-.781,2.092,2.092,0,0,1,2.328.445Z"/></svg>
					</a>
					<?php if ( $_li_url ) : ?>
					<a class="footer-author-icon footer-author-linkedin" href="<?php echo esc_url( $_li_url ); ?>" target="_blank" rel="noopener noreferrer" aria-label="<?php echo esc_attr( $author_fullname ); ?> on LinkedIn">
						<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect class="li-square" x="0" y="0" width="24" height="24" rx="4"/><path class="li-in" transform="translate(2.4 2.4) scale(.8)" d="M7.119 20.452H3.555V9h3.564v11.452zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.063 2.063 0 112.063 2.065zM20.447 20.452h-3.554v-5.569c0-1.328-.024-3.037-1.852-3.037-1.853 0-2.137 1.445-2.137 2.939v5.667H9.351V9h3.414v1.561h.049c.477-.9 1.637-1.852 3.37-1.852 3.602 0 4.268 2.37 4.268 5.455v6.288z"/></svg>
					</a>
					<?php endif; ?>
				</div>
            </div>
		</div>
	</div>
</section>
<script>
(function(){
	function size(){
		document.querySelectorAll('.section-footer-author').forEach(function(sec){
			var content = sec.querySelector('.col-author-content');
			var imgCol  = sec.querySelector('.row > .col-auto:first-child');
			if (!content || !imgCol) return;
			if (window.innerWidth < 900) { imgCol.style.width = ''; imgCol.style.height = ''; return; }
			var h = content.getBoundingClientRect().height;
			imgCol.style.width  = h + 'px';
			imgCol.style.height = h + 'px';
		});
	}
	if (document.readyState !== 'loading') { size(); } else { document.addEventListener('DOMContentLoaded', size); }
	window.addEventListener('load', size);
	window.addEventListener('resize', size);
})();
</script>

