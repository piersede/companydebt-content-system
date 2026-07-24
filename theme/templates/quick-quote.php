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

// Staging-only flag: used to hide GF40's v2 reCAPTCHA (whose site key isn't
// registered for comdebstage, so Google renders an "invalid domain" error box).
// Never hide it in production — there it's a live, required field.
$qq_is_staging = ( isset( $_SERVER['HTTP_HOST'] ) && strpos( $_SERVER['HTTP_HOST'], 'comdebstage' ) !== false );
?>
<div class="qq<?php echo $qq_is_staging ? ' qq--staging' : ''; ?>">

	<!-- HERO + QUOTE FORM -->
	<section class="qq-hero">

		<!-- Custom landing header (logo · Google reviews · Speak to an Expert),
		     sits on the navy hero. A <div> (not <header>) so the theme's bare
		     `header{…}` rules — which set inset:0 and a transparent background —
		     don't hijack it. role="banner" preserves the landmark semantics. -->
		<div class="qq-topbar" role="banner">
			<div class="qq-topbar__inner">
				<a class="qq-topbar__logo" href="https://www.companydebt.com/">
					<img src="<?php echo esc_url( content_url( 'uploads/2023/02/logo-cd.png' ) ); ?>" alt="Company Debt" height="27">
				</a>
				<div class="qq-topbar__reviews">
					<span class="qq-topbar__stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
					<span class="qq-topbar__rtxt">Rated <strong>4.9/5</strong> on Google Reviews</span>
				</div>
				<a class="qq-topbar__cta" href="tel:08000746757">Speak to an Expert</a>
			</div>
		</div>

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
					<img class="qq-logo--ipa" src="<?php echo esc_url( content_url( 'uploads/2022/03/IPA_White_PNG.png' ) ); ?>" alt="Insolvency Practitioners Association" height="40">
					<img class="qq-logo--tma" src="<?php echo esc_url( content_url( 'uploads/2022/03/TMA_White_PNG.png' ) ); ?>" alt="Turnaround Management Association" height="47">
					<img class="qq-logo--icas" src="<?php echo esc_url( content_url( 'uploads/2026/04/icas-logo-1.png' ) ); ?>" alt="ICAS" height="26">
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

	<!-- TRUST STRIP -->
	<section class="qq-trust">
		<div class="qq-trust__inner">
			<div class="qq-trust__item">
				<span class="qq-trust__ico"><svg viewBox="0 0 24 24" width="21" height="21" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="2" width="8" height="4" rx="1"/><path d="M9 4H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-3"/><path d="m9 14 2 2 4-4"/></svg></span>
				<span class="qq-trust__txt">Simplified process</span>
			</div>
			<div class="qq-trust__item">
				<span class="qq-trust__ico"><svg viewBox="0 0 24 24" width="21" height="21" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg></span>
				<span class="qq-trust__txt">No physical meetings</span>
			</div>
			<div class="qq-trust__item">
				<span class="qq-trust__ico"><svg viewBox="0 0 24 24" width="21" height="21" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/></svg></span>
				<span class="qq-trust__txt">Liquidate from home</span>
			</div>
			<div class="qq-trust__item">
				<span class="qq-trust__ico"><svg viewBox="0 0 24 24" width="21" height="21" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h18"/></svg></span>
				<span class="qq-trust__txt">Free same-day consultation</span>
			</div>
		</div>
	</section>

	<!-- HOW IT WORKS -->
	<section class="qq-process">
		<div class="qq-process__head">
			<p class="qq-eyebrow">How it works</p>
			<h2 class="qq-h2">Our Easy 4-Step Liquidation Process</h2>
			<p class="qq-lead">From first form to formal closure, we handle the liquidation so you don't have to.</p>
		</div>
		<div class="qq-process__grid">
			<div class="qq-process__media">
				<img src="<?php echo esc_url( content_url( 'uploads/2026/07/qq-director.webp' ) ); ?>" alt="Director starting the liquidation process from home" loading="lazy">
			</div>
			<div class="qq-steps">
			<div class="qq-step">
				<span class="qq-step__ico"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7z"/><path d="M14 2v5h5"/><path d="M8 13h6"/><path d="M8 17h6"/><path d="M8 9h2"/></svg></span>
				<div><h3 class="qq-step__title">Complete the quick quote form</h3><p class="qq-step__text">Give us a few basic figures. Everything you share is fully confidential and without obligation.</p></div>
			</div>
			<div class="qq-step">
				<span class="qq-step__ico"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/></svg></span>
				<div><h3 class="qq-step__title">A licensed insolvency practitioner takes over</h3><p class="qq-step__text">Your liquidation is handled by regulated experts whose mission is to find positive solutions for directors.</p></div>
			</div>
			<div class="qq-step">
				<span class="qq-step__ico"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></span>
				<div><h3 class="qq-step__title">We close the company &amp; deal with creditors</h3><p class="qq-step__text">Company assets are realised and distributed fairly, with any surplus returned to shareholders.</p></div>
			</div>
			<div class="qq-step qq-step--final">
				<span class="qq-step__ico"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.8 10A10 10 0 1 1 17 3.34"/><path d="m9 11 3 3L22 4"/></svg></span>
				<div><h3 class="qq-step__title">The company is dissolved &amp; debts cease to exist</h3><p class="qq-step__text">The company is struck off the register, the liquidation concludes and its debts come to an end.</p></div>
			</div>
			</div>
		</div>
	</section>

	<!-- TESTIMONIAL -->
	<section class="qq-tmony">
		<div class="qq-tmony__inner">
			<p class="qq-eyebrow qq-eyebrow--on-navy">Help you can trust</p>
			<div class="qq-tmony__stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
			<p class="qq-tmony__quote">&ldquo;Calling Company Debt was one of the best decisions I&rsquo;ve ever made. I was given clear, genuine advice and a difficult time was handled sensitively and effectively.&rdquo;</p>
			<div class="qq-tmony__who">
				<img class="qq-tmony__avatar" src="<?php echo esc_url( content_url( 'uploads/2026/07/qq-avatar.webp' ) ); ?>" alt="Company Director" width="48" height="48" loading="lazy">
				<div class="qq-tmony__whotext">
					<p class="qq-tmony__name">Company Director</p>
					<p class="qq-tmony__role">Heating &amp; Plumbing Company, London</p>
				</div>
			</div>
		</div>
	</section>

	<!-- FAQ -->
	<section class="qq-faq">
		<div class="qq-faq__head">
			<p class="qq-eyebrow">Liquidation FAQs</p>
			<h2 class="qq-h2">Frequently Asked Questions</h2>
		</div>
		<div class="qq-faq__list">
			<div class="qq-faq__item">
				<button class="qq-faq__q" type="button" aria-expanded="false">
					<span>How Long Does the Process Take?</span>
					<span class="qq-faq__sign" aria-hidden="true">+</span>
				</button>
				<div class="qq-faq__a">
					<p>Whilst liquidation timeframes will vary widely depending on the size and complexity of the case, especially if there are assets that need to be realised. Once appointed it is the liquidator that is responsible for dealing with creditors, getting in the assets of the company and distributing any proceeds of sale. The director&rsquo;s responsibility is to provide the liquidator with the information to do this, the majority of which is undertaken in the first 6 months.</p>
					<p>Once a director has provided the liquidator with all the information they have requested, there is normally very little left for the director to do. So whilst a typical liquidation might last for 12&ndash;18 months, in most cases the director need have no further involvement after the first 6 months.</p>
				</div>
			</div>
			<div class="qq-faq__item">
				<button class="qq-faq__q" type="button" aria-expanded="false">
					<span>Could I Liquidate my Own Company?</span>
					<span class="qq-faq__sign" aria-hidden="true">+</span>
				</button>
				<div class="qq-faq__a">
					<p>The short answer is no, you cannot liquidate a company yourself. All company liquidations require the services of a licensed liquidator, under UK law.</p>
				</div>
			</div>
			<div class="qq-faq__item">
				<button class="qq-faq__q" type="button" aria-expanded="false">
					<span>Are Directors Entitled to Redundancy?</span>
					<span class="qq-faq__sign" aria-hidden="true">+</span>
				</button>
				<div class="qq-faq__a">
					<p>If you&rsquo;re a company director and have paid yourself via PAYE, with more than two years&rsquo; service, it&rsquo;s very likely you can claim redundancy if your company has closed due to insolvency.</p>
					<p>Claims must be made through the Redundancy Payments Service, part of the Insolvency Service, and we will tell you how to process your claim. If the claim is successful, it will then be paid by the National Insurance Fund.</p>
				</div>
			</div>
		</div>
	</section>

	<!-- AS FEATURED ON -->
	<section class="qq-featured">
		<div class="qq-featured__inner">
			<p class="qq-featured__label">As featured on</p>
			<div class="qq-featured__logos">
				<img src="<?php echo esc_url( content_url( 'uploads/2026/07/qq-press-telegraph.webp' ) ); ?>" alt="The Telegraph" height="19">
				<img src="<?php echo esc_url( content_url( 'uploads/2026/07/qq-press-bbc.webp' ) ); ?>" alt="BBC" height="17">
				<img src="<?php echo esc_url( content_url( 'uploads/2026/07/qq-press-express.webp' ) ); ?>" alt="Daily Express" height="20">
				<img src="<?php echo esc_url( content_url( 'uploads/2026/07/qq-press-ft.webp' ) ); ?>" alt="Financial Times" height="19">
				<img src="<?php echo esc_url( content_url( 'uploads/2026/07/qq-press-guardian.webp' ) ); ?>" alt="The Guardian" height="20">
				<img src="<?php echo esc_url( content_url( 'uploads/2026/07/qq-press-investopedia.webp' ) ); ?>" alt="Investopedia" height="16">
				<img src="<?php echo esc_url( content_url( 'uploads/2026/07/qq-press-fortune.webp' ) ); ?>" alt="Fortune" height="17">
			</div>
		</div>
	</section>

</div>

<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How Long Does the Process Take?","acceptedAnswer":{"@type":"Answer","text":"Whilst liquidation timeframes vary widely depending on the size and complexity of the case, once appointed the liquidator is responsible for dealing with creditors, realising the company's assets and distributing any proceeds. The director provides the liquidator with the information to do this, the majority within the first 6 months. Whilst a typical liquidation might last 12-18 months, in most cases the director need have no further involvement after the first 6 months."}},{"@type":"Question","name":"Could I Liquidate my Own Company?","acceptedAnswer":{"@type":"Answer","text":"No, you cannot liquidate a company yourself. All company liquidations require the services of a licensed liquidator, under UK law."}},{"@type":"Question","name":"Are Directors Entitled to Redundancy?","acceptedAnswer":{"@type":"Answer","text":"If you're a company director and have paid yourself via PAYE, with more than two years' service, it's very likely you can claim redundancy if your company has closed due to insolvency. Claims are made through the Redundancy Payments Service, part of the Insolvency Service, and if successful are paid by the National Insurance Fund."}}]}
</script>

<script>
/* Cosmetic only: relabel GF40's submit button to match the design.
   Does not change the form, its fields, or the submission. */
document.addEventListener('DOMContentLoaded', function () {
	var btn = document.getElementById('gform_submit_button_40');
	if (btn) { btn.value = 'Get My Tailored Quote'; }

	// Sticky header: transparent (blends into hero) at the top, frosted glass
	// once scrolled — matches the mockup's scroll behaviour.
	var topbar = document.querySelector('.qq-topbar');
	if (topbar) {
		var onScroll = function () {
			topbar.classList.toggle('is-glass', window.pageYOffset > 8);
		};
		onScroll();
		window.addEventListener('scroll', onScroll, { passive: true });
	}

	// Cosmetic placeholder text to match the design (GF40 field settings unchanged).
	var ph = { 'input_40_16': 'Full name*', 'input_40_2': 'Email*', 'input_40_14': 'Phone*' };
	Object.keys(ph).forEach(function (id) {
		var el = document.getElementById(id);
		if (el) { el.setAttribute('placeholder', ph[id]); }
	});

	// Value fields: the calculator writes "£ 25,000" as one string. Split it into
	// £ (left) + figure (right) so the dashed field matches the mockup. Purely a
	// display reformat — the slider, hidden GF amount fields and quote logic are
	// untouched. Loop-guarded via data-fig so it never fights the calculator.
	document.querySelectorAll('.quiz__amount').forEach(function (span) {
		var reformat = function () {
			var fig = span.textContent.replace(/[£\s]/g, '').trim() || '0';
			var figEl = span.querySelector('.qq-fig');
			// already in our split form with the right figure? leave it (prevents loops)
			if (figEl && figEl.textContent === fig) { return; }
			span.innerHTML = '<span class="qq-cur">£</span><span class="qq-fig">' + fig + '</span>';
		};
		reformat();
		new MutationObserver(reformat).observe(span, { childList: true, characterData: true, subtree: true });
	});

	// Keep the FAQ heading as designed. A site-wide theme script relabels FAQ
	// headings to "FAQs About {title}", which reads awkwardly here; hold ours.
	var faqH2 = document.querySelector('.qq-faq__head .qq-h2');
	if (faqH2) {
		var wantHeading = 'Frequently Asked Questions';
		faqH2.textContent = wantHeading;
		var mo = new MutationObserver(function () {
			if (faqH2.textContent !== wantHeading) { faqH2.textContent = wantHeading; }
		});
		mo.observe(faqH2, { childList: true, characterData: true, subtree: true });
		setTimeout(function () { mo.disconnect(); }, 4000);
	}

	// FAQ accordion (progressive enhancement; answers are in the DOM + schema regardless)
	document.querySelectorAll('.qq-faq__q').forEach(function (q) {
		q.addEventListener('click', function () {
			var item = q.closest('.qq-faq__item');
			var open = item.classList.toggle('is-open');
			q.setAttribute('aria-expanded', open ? 'true' : 'false');
			var sign = q.querySelector('.qq-faq__sign');
			if (sign) { sign.textContent = open ? '−' : '+'; }
		});
	});
});
</script>

<?php
get_footer();
