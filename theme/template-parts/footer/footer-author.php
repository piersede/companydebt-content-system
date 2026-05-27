<?php
$author_id = get_the_author_meta('ID');
$author_nickname = get_the_author_meta('nickname');
$author_first_name = get_the_author_meta('first_name');
$author_fullname = get_the_author_meta('display_name');
$_li_url = trim( (string) get_field( 'linkedin', 'user_'. $author_id ) );
$_first_name_for_label = $author_first_name ? $author_first_name : strtok( $author_fullname, ' ' );
?>
<section class="section-footer-author">
	<div class="container">
		<div class="row">
			<div class="col-auto">
				<?php echo wp_get_attachment_image( get_field( 'photo',  'user_'. $author_id ), 'full', false,  ["class" => "avatar-image", "alt" => "Avatar Image"] ); ?>
            </div>
			<div class="col-auto col-author-content">
				<div class="footer-author-eyebrow">
					<svg class="footer-author-eyebrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg>
					<span>Expertly reviewed by</span>
				</div>
				<div class="footer-author-name"><?php echo esc_html( $author_fullname ); ?></div>
				<div class="footer-author-position"><?php echo trim( get_field('professional_position',  'user_'. $author_id ) ); ?></div>
				<?php
				$_pills = array_filter( array_map( 'trim', array(
					(string) get_field( 'trust_pill_1', 'user_' . $author_id ),
					(string) get_field( 'trust_pill_2', 'user_' . $author_id ),
					(string) get_field( 'trust_pill_3', 'user_' . $author_id ),
				) ) );
				if ( ! empty( $_pills ) ) : ?>
				<div class="footer-author-pills">
					<?php foreach ( $_pills as $_pill ) : ?>
					<span class="footer-author-pill">
						<svg class="footer-author-pill-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg>
						<?php echo esc_html( $_pill ); ?>
					</span>
					<?php endforeach; ?>
				</div>
				<?php endif; ?>
			</div>
			<div class="col-auto col-author-actions">
				<a class="footer-author-action" href="/contact-us/" target="_blank" rel="noopener">
					<span class="footer-author-action-icon">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 4l-8 5L4 8V6l8 5 8-5v2z"/></svg>
					</span>
					<span class="footer-author-action-label">Email <?php echo esc_html( $_first_name_for_label ); ?></span>
					<span class="footer-author-action-arrow">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
					</span>
				</a>
				<?php if ( $_li_url ) : ?>
				<a class="footer-author-action" href="<?php echo esc_url( $_li_url ); ?>" target="_blank" rel="noopener noreferrer">
					<span class="footer-author-action-icon">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M19 0h-14C2.24 0 0 2.24 0 5v14c0 2.76 2.24 5 5 5h14c2.76 0 5-2.24 5-5V5c0-2.76-2.24-5-5-5zM8 19H5V8h3v11zM6.5 6.73c-.97 0-1.75-.79-1.75-1.76 0-.97.78-1.76 1.75-1.76s1.75.79 1.75 1.76c0 .97-.78 1.76-1.75 1.76zM20 19h-3v-5.6c0-3.37-4-3.11-4 0V19h-3V8h3v1.76c1.4-2.58 7-2.77 7 2.47V19z"/></svg>
					</span>
					<span class="footer-author-action-label"><?php echo esc_html( $_first_name_for_label ); ?>&rsquo; LinkedIn Profile</span>
					<span class="footer-author-action-arrow">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
					</span>
				</a>
				<?php endif; ?>
				<a class="footer-author-action" href="tel:08000746757" aria-label="Call 0800 074 6757">
					<span class="footer-author-action-icon">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.384,17.752a2.108,2.108,0,0,1-.522,3.359,7.543,7.543,0,0,1-5.476.642C10.5,20.523,3.477,13.5,2.247,8.614a7.543,7.543,0,0,1,.642-5.476,2.108,2.108,0,0,1,3.359-.522L8.333,4.7a2.094,2.094,0,0,1,.445,2.328A3.877,3.877,0,0,1,8,8.2c-2.384,2.384,5.417,10.185,7.8,7.8a3.877,3.877,0,0,1,1.173-.781,2.092,2.092,0,0,1,2.328.445Z"/></svg>
					</span>
					<span class="footer-author-action-label">Give us a Call</span>
					<span class="footer-author-action-arrow">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
					</span>
				</a>
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
			var h = Math.max(content.getBoundingClientRect().height, 175);
			imgCol.style.width  = h + 'px';
			imgCol.style.height = h + 'px';
		});
	}
	if (document.readyState !== 'loading') { size(); } else { document.addEventListener('DOMContentLoaded', size); }
	window.addEventListener('load', size);
	window.addEventListener('resize', size);
})();
</script>
