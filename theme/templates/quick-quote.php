<?php
/**
 * Template Name: Quick Quote
 *
 * Cosmetic redesign of the /quick-quote/ page. Built in milestones.
 *
 * IMPORTANT — this template reproduces the live quote calculator's JS hooks
 * exactly so quiz-insolv.js + Gravity Form 40 keep working unchanged:
 *   - noUiSlider mounts:  #slider-range-{bank,hmrc,creditors,assets,cash-at-bank}
 *   - value displays:     span.quiz__amount#quiz__amount-{...}
 *   - the form itself:    Gravity Form 40 via shortcode (hidden gf_amount-* +
 *                         gf_personal-guarantee + gf_result fields live inside it)
 * Do NOT rename these. The design is layered on with public/qq-redesign.css.
 *
 * The page's original template assignment and Gutenberg content remain intact
 * in the database as rollback — see the template_include filter in functions.php.
 *
 * Milestone 2: hero + form card. Lower sections (how it works, testimonial,
 * FAQs, featured) are added in a later milestone.
 */

get_header();
?>
<div class="qq">

	<!-- HERO + QUOTE FORM -->
	<section class="qq-hero">
		<div class="qq-hero__inner">

			<div class="qq-hero__left">
				<span class="qq-hero__pill">Licensed &amp; Regulated Insolvency Practitioners</span>
				<h1 class="qq-hero__title">Get an Instant <br><span class="qq-accent">Company Liquidation</span> Quote</h1>
				<p class="qq-hero__sub">Move the sliders to see an immediate estimate of your liquidation fees. A fast, simple and stress-free way to understand the cost of closing your company, entirely commitment-free.</p>

				<ul class="qq-hero__ticks">
					<li><span class="qq-tick">&#10003;</span> Handled by licensed insolvency practitioners</li>
					<li><span class="qq-tick">&#10003;</span> Liquidate entirely from home, no physical meetings</li>
					<li><span class="qq-tick">&#10003;</span> Free same-day consultation &amp; clear next steps</li>
				</ul>

				<div class="qq-hero__cta">
					<a href="tel:08000746757" class="qq-btn qq-btn--solid">Get Help Now</a>
					<a href="tel:08000746757" class="qq-btn qq-btn--ghost">
						<svg viewBox="0 0 24 24" width="17" height="17" fill="currentColor" aria-hidden="true"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2a1 1 0 0 1 1.02-.24 11.36 11.36 0 0 0 3.57.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.24 1.02z"/></svg>
						0800 074 6757
					</a>
				</div>

				<div class="qq-hero__logos">
					<img src="<?php echo esc_url( content_url( 'uploads/2022/03/IPA_White_PNG.png' ) ); ?>" alt="Insolvency Practitioners Association" height="40">
					<img src="<?php echo esc_url( content_url( 'uploads/2022/03/TMA_White_PNG.png' ) ); ?>" alt="Turnaround Management Association" height="44">
				</div>
			</div>

			<!-- FORM CARD: mockup visuals over the real calculator hooks -->
			<div class="qq-card">
				<div class="qq-card__sliders">
					<p class="qq-card__eyebrow">Liabilities</p>
					<p class="qq-card__note">What does the company owe?</p>

					<div class="qq-slider">
						<div class="qq-slider__head">
							<label for="quiz__amount-bank" class="qq-slider__label">Bank</label>
							<span class="quiz__amount quiz__amount-bank qq-slider__val" id="quiz__amount-bank">&pound;0</span>
						</div>
						<div class="slider-range-noUI-container"><div id="slider-range-bank" class="slider-range-noUI"></div></div>
					</div>
					<div class="qq-slider">
						<div class="qq-slider__head">
							<label for="quiz__amount-hmrc" class="qq-slider__label">HMRC (VAT, PAYE, Corp Tax)</label>
							<span class="quiz__amount quiz__amount-hmrc qq-slider__val" id="quiz__amount-hmrc">&pound;0</span>
						</div>
						<div class="slider-range-noUI-container"><div id="slider-range-hmrc" class="slider-range-noUI"></div></div>
					</div>
					<div class="qq-slider">
						<div class="qq-slider__head">
							<label for="quiz__amount-creditors" class="qq-slider__label">Other creditors</label>
							<span class="quiz__amount quiz__amount-creditors qq-slider__val" id="quiz__amount-creditors">&pound;0</span>
						</div>
						<div class="slider-range-noUI-container"><div id="slider-range-creditors" class="slider-range-noUI"></div></div>
					</div>

					<p class="qq-card__eyebrow">Assets &amp; Cash</p>
					<p class="qq-card__note">Estimated value the company holds</p>

					<div class="qq-slider">
						<div class="qq-slider__head">
							<label for="quiz__amount-assets" class="qq-slider__label">Assets</label>
							<span class="quiz__amount quiz__amount-assets qq-slider__val" id="quiz__amount-assets">&pound;0</span>
						</div>
						<div class="slider-range-noUI-container"><div id="slider-range-assets" class="slider-range-noUI"></div></div>
					</div>
					<div class="qq-slider">
						<div class="qq-slider__head">
							<label for="quiz__amount-cash-at-bank" class="qq-slider__label">Cash at bank</label>
							<span class="quiz__amount quiz__amount-cash-at-bank qq-slider__val" id="quiz__amount-cash-at-bank">&pound;0</span>
						</div>
						<div class="slider-range-noUI-container"><div id="slider-range-cash-at-bank" class="slider-range-noUI"></div></div>
					</div>
				</div>

				<div class="qq-card__form form-wrapper">
					<?php echo do_shortcode( '[gravityform id="40" title="false" description="false" ajax="true"]' ); ?>
					<p class="qq-card__micro">&#128274; 100% confidential &amp; obligation-free. Your details are never shared.</p>
				</div>
			</div>

		</div>
	</section>

</div>

<script>
/* Cosmetic only: relabel GF40's submit button to match the design.
   Does not change the form, its fields, or the submission. */
document.addEventListener('DOMContentLoaded', function () {
	var btn = document.getElementById('gform_submit_button_40');
	if (btn) { btn.value = 'Get My Tailored Quote'; }
});
</script>

<?php
get_footer();
