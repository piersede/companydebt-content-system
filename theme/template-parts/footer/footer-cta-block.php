<section class="footer-cta-block" aria-label="Speak to our team">
	<div class="container">
		<div class="row">
			<div class="col-12 col-md-7 footer-cta-block-content">
				<div class="footer-cta-eyebrow"><svg class="footer-cta-eyebrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg><span>Need confidential advice?</span></div>
				<?php /* "Get in Touch Today" — was an <h2> until 20260605. Demoted
				 * to <div> on request: it should not act as a section heading
				 * in the document outline (this CTA block appears on many
				 * templates and was creating duplicate-H2 noise). The visual
				 * treatment is unchanged — the `.footer-cta-block .footer-cta-block-content
				 * .footer-cta-title` rule in style.css owns all font, colour
				 * and margin properties and targets the class, so the
				 * tag swap leaves computed style byte-identical. */ ?>
				<div class="footer-cta-title">Get in Touch Today</div>
				<?php the_field( 'default_cta_content', 'option' ); ?>
				<div class="footer-cta-action-row"><a class="footer-cta-button" href="tel:08000746757"><svg class="footer-cta-button-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg><span>0800 074 6757</span></a><div class="footer-cta-hours"><span class="footer-cta-hours__days">Mon-Fri</span><span class="footer-cta-hours__time">8AM - 8PM</span></div></div>
				<div class="footer-cta-trust">
					<span class="footer-cta-trust-pill">
						<svg class="footer-cta-trust-pill-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg>
						100% Confidential
					</span>
					<span class="footer-cta-trust-pill">
						<svg class="footer-cta-trust-pill-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg>
						Real Experts
					</span>
					<span class="footer-cta-trust-pill">
						<svg class="footer-cta-trust-pill-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg>
						Same-Day Support
					</span>
				</div>
			</div>
			<div class="col-12 col-md-5 footer-cta-block-form">
				<?php echo do_shortcode( '[gravityform id="29" title="false" description="false" ajax="true"]' ); ?>
				<script>
				(function(){
					function reorderCTAForm(){
						var section = document.querySelector('.footer-cta-block');
						if (!section) return;
						var disc = section.querySelector('#field_29_10');
						var footer = section.querySelector('.gform_footer');
						if (disc && footer && footer.parentNode) {
							/* a11y: a bare <li> moved out of its <ul> orphans the list item
							   (axe-listitem). Keep it valid by relocating it inside a
							   role=list <ul> styled to be visually invisible. Idempotent. */
							if (disc.parentNode && disc.parentNode.classList && disc.parentNode.classList.contains('cd-cta-disc-list')) return;
							var wrap = document.createElement('ul');
							wrap.className = 'cd-cta-disc-list';
							wrap.setAttribute('role', 'list');
							wrap.style.cssText = 'list-style:none;margin:0;padding:0;';
							footer.parentNode.insertBefore(wrap, footer.nextSibling);
							wrap.appendChild(disc);
						}
					}
					document.addEventListener('DOMContentLoaded', reorderCTAForm);
					if (window.jQuery) { jQuery(document).on('gform_post_render', reorderCTAForm); }
				})();
				</script>
			</div>
		</div>
	</div>
</section>
