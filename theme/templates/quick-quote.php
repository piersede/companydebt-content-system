<?php
/**
 * Template Name: Quick Quote (Options redesign)
 *
 * Built 2026-07-27 as the "options-first" PPC redesign agreed in
 * design-handoff/quick-quote-options-page-design-brief.md, originally
 * developed on a separate page/slug (quick-quote-options) so the live
 * /quick-quote/ page was untouched while the design was reviewed.
 *
 * 2026-07-28 — approved and swapped onto /quick-quote/ itself: this file now
 * lives at templates/quick-quote.php (this content moved into that path;
 * the file itself was not renamed). The colleague's original cosmetic
 * redesign moved the other way, into templates/quick-quote-options.php, kept
 * live at /quick-quote-options/ in case it's still wanted. Nothing else
 * changed — same slugs, same post IDs, same functions.php routing, same
 * qq-redesign.css (its scoping is by CSS class, not by file path, so it
 * follows this markup automatically). Only the two template files' contents
 * were swapped, plus each page's Yoast SEO title/description to match.
 *
 * IMPORTANT — reproduces the live quote calculator's JS hooks exactly so
 * quiz-insolv.js + Gravity Form 40 keep working unchanged:
 *   - noUiSlider mounts:  #slider-range-{bank,hmrc,creditors,assets,cash-at-bank}
 *   - value displays:     span.quiz__amount#quiz__amount-{...}
 *   - the form itself:    Gravity Form 40 via shortcode (hidden gf_amount-* +
 *                         gf_personal-guarantee + gf_result fields live inside it)
 * Do NOT rename these. This page reuses Gravity Form 40 as-is (same lead
 * pipeline as /quick-quote-options/) — its field labels (Full name/Email/Phone)
 * are NOT editable here without changing the shared form. The design is
 * layered on with public/qq-redesign.css (shared file, additive rules only).
 */

get_header();

// Staging-only flag: used to hide GF40's v2 reCAPTCHA (whose site key isn't
// registered for comdebstage, so Google renders an "invalid domain" error box).
// Never hide it in production — there it's a live, required field.
$qq_is_staging = ( isset( $_SERVER['HTTP_HOST'] ) && strpos( $_SERVER['HTTP_HOST'], 'comdebstage' ) !== false );
?>
<div class="qq qq-v2<?php echo $qq_is_staging ? ' qq--staging' : ''; ?>">

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

			<!-- v2: the pill leads the left column so the grid's align-items:start
			     lines the form card up with the pill (brow), not the H1 below it. -->
			<div class="qq-hero__grid">
			<div class="qq-hero__left">
				<span class="qq-hero__pill">Licensed and Regulated Insolvency Practitioners</span>
				<h1 class="qq-hero__title">Understand Your Company&rsquo;s <span class="qq-accent">Options</span></h1>
				<p class="qq-hero__sub">Whether you are considering closing your limited company, struggling with company debts or hoping the business can continue, answer a few questions about its current financial position. We will explain the realistic options, likely costs and next steps. You do not need to know which insolvency procedure, if any, the company requires.</p>

				<ul class="qq-hero__ticks">
					<li><span class="qq-tick">&#10003;</span> Clear advice on rescue, restructuring and closure</li>
					<li><span class="qq-tick">&#10003;</span> Confidential help from an experienced insolvency team</li>
					<li><span class="qq-tick">&#10003;</span> Clear costs before you make any decision</li>
					<li><span class="qq-tick">&#10003;</span> No pressure and no obligation to proceed</li>
				</ul>

				<div class="qq-hero__cta">
					<a href="tel:08000746757" class="qq-btn qq-btn--solid">Get Help Now</a>
					<a href="tel:08000746757" class="qq-btn qq-btn--ghost">
						<svg viewBox="0 0 24 24" width="17" height="17" fill="currentColor" aria-hidden="true"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2a1 1 0 0 1 1.02-.24 11.36 11.36 0 0 0 3.57.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.24 1.02z"/></svg>
						0800 074 6757
					</a>
				</div>
				<p class="qq-hero__micro">
					<span class="qq-hero__micro-ico" aria-hidden="true"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg></span>
					You do not need exact figures. Reasonable estimates are fine.
				</p>

				<div class="qq-hero__logos">
					<img class="qq-logo--ipa" src="<?php echo esc_url( content_url( 'uploads/2022/03/IPA_White_PNG.png' ) ); ?>" alt="Insolvency Practitioners Association" height="40">
					<img class="qq-logo--tma" src="<?php echo esc_url( content_url( 'uploads/2022/03/TMA_White_PNG.png' ) ); ?>" alt="Turnaround Management Association" height="47">
					<img class="qq-logo--icas" src="<?php echo esc_url( content_url( 'uploads/2026/04/icas-logo-1.png' ) ); ?>" alt="ICAS" height="26">
				</div>
			</div>

			<!-- FORM CARD: mockup visuals over the real calculator hooks -->
			<div class="qq-card" id="quick-quote-form">
				<div class="qq-card__sliders">
					<p class="qq-card__step">Your situation</p>
					<p class="qq-card__privacy">&#128274; Your figures stay confidential. Used only to prepare your options.</p>
					<p class="qq-card__eyebrow">What Does the Company Owe?</p>

					<div class="qq-slider">
						<div class="qq-slider__head">
							<label for="quiz__amount-bank" class="qq-slider__label">Bank borrowing</label>
							<span class="quiz__amount quiz__amount-bank qq-slider__val" id="quiz__amount-bank">&pound;0</span>
						</div>
						<div class="slider-range-noUI-container"><div id="slider-range-bank" class="slider-range-noUI"></div></div>
					</div>
					<div class="qq-slider">
						<div class="qq-slider__head">
							<label for="quiz__amount-hmrc" class="qq-slider__label">HMRC debt</label>
							<span class="quiz__amount quiz__amount-hmrc qq-slider__val" id="quiz__amount-hmrc">&pound;0</span>
						</div>
						<div class="slider-range-noUI-container"><div id="slider-range-hmrc" class="slider-range-noUI"></div></div>
					</div>
					<div class="qq-slider">
						<div class="qq-slider__head">
							<label for="quiz__amount-creditors" class="qq-slider__label">Suppliers and other creditors</label>
							<span class="quiz__amount quiz__amount-creditors qq-slider__val" id="quiz__amount-creditors">&pound;0</span>
						</div>
						<div class="slider-range-noUI-container"><div id="slider-range-creditors" class="slider-range-noUI"></div></div>
					</div>

					<p class="qq-card__eyebrow">What Does the Company Own?</p>

					<div class="qq-slider">
						<div class="qq-slider__head">
							<label for="quiz__amount-assets" class="qq-slider__label">Company assets</label>
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
					<p class="qq-card__step">Your details</p>
					<p class="qq-card__privacy">&#128337; We aim to call you back by 5pm the same working day.</p>
					<?php echo do_shortcode( '[gravityform id="40" title="false" description="false" ajax="true"]' ); ?>
					<div class="qq-card__trust">
						<span class="qq-card__trust-item"><span aria-hidden="true">&#9733;</span> 4.9/5 on Google Reviews</span>
						<span class="qq-card__trust-item"><span aria-hidden="true">&#128737;</span> Licensed insolvency practitioners</span>
					</div>
					<p class="qq-card__micro">&#128274; Confidential. No obligation to proceed.</p>
				</div>
			</div>
			</div>

		</div>
	</section>

	<!-- TRUST STRIP -->
	<section class="qq-trust">
		<div class="qq-trust__inner">
			<div class="qq-trust__item">
				<span class="qq-trust__ico"><svg viewBox="0 0 24 24" width="21" height="21" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></span>
				<span class="qq-trust__txt">Confidential and no obligation</span>
			</div>
			<div class="qq-trust__item">
				<span class="qq-trust__ico"><svg viewBox="0 0 24 24" width="21" height="21" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="2" width="8" height="4" rx="1"/><path d="M9 4H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-3"/><path d="m9 14 2 2 4-4"/></svg></span>
				<span class="qq-trust__txt">Licensed insolvency practitioners</span>
			</div>
			<div class="qq-trust__item">
				<span class="qq-trust__ico"><svg viewBox="0 0 24 24" width="21" height="21" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg></span>
				<span class="qq-trust__txt">Clear explanation of your options and costs</span>
			</div>
			<div class="qq-trust__item">
				<span class="qq-trust__ico"><svg viewBox="0 0 24 24" width="21" height="21" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/></svg></span>
				<span class="qq-trust__txt">Most cases can be handled remotely</span>
			</div>
		</div>
	</section>

	<!-- HOW IT WORKS -->
	<section class="qq-process">
		<div class="qq-process__head">
			<p class="qq-eyebrow">How it works</p>
			<h2 class="qq-h2">A Clear Four-Step Process</h2>
			<p class="qq-lead">You do not need to diagnose the problem yourself. Tell us what is happening and we will explain the realistic options.</p>
		</div>
		<div class="qq-process__grid">
			<div class="qq-process__media">
				<img src="<?php echo esc_url( content_url( 'uploads/2022/03/Girl-with-Laptiop.jpg' ) ); ?>" alt="Director reviewing company finances from home" loading="lazy">
			</div>
			<div class="qq-steps">
			<div class="qq-step">
				<span class="qq-step__ico"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7z"/><path d="M14 2v5h5"/><path d="M8 13h6"/><path d="M8 17h6"/><path d="M8 9h2"/></svg></span>
				<div><h3 class="qq-step__title">Tell Us About the Company</h3><p class="qq-step__text">Provide a few approximate figures about the company&rsquo;s debts, assets and current financial position.</p></div>
			</div>
			<div class="qq-step">
				<span class="qq-step__ico"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></span>
				<div><h3 class="qq-step__title">Speak With an Experienced Adviser</h3><p class="qq-step__text">A member of our insolvency team will review the information with you and ask any further questions needed to understand the situation.</p></div>
			</div>
			<div class="qq-step">
				<span class="qq-step__ico"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/></svg></span>
				<div><h3 class="qq-step__title">Understand the Realistic Options</h3><p class="qq-step__text">We will explain whether the company may have a viable route forward or whether closure should be considered. This may include informal arrangements, restructuring or a formal insolvency process.</p></div>
			</div>
			<div class="qq-step qq-step--final">
				<span class="qq-step__ico"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.8 10A10 10 0 1 1 17 3.34"/><path d="m9 11 3 3L22 4"/></svg></span>
				<div><h3 class="qq-step__title">Decide What Happens Next</h3><p class="qq-step__text">You will receive a clear explanation of the likely process and costs. You can then decide whether to proceed, with no pressure or obligation.</p></div>
			</div>
			</div>
		</div>
		<p class="qq-process__note">If a formal insolvency procedure is appropriate and you choose to proceed, it will be handled by a licensed insolvency practitioner.</p>
	</section>

	<!-- POSSIBLE OPTIONS -->
	<section class="qq-options">
		<div class="qq-options__head">
			<p class="qq-eyebrow">Possible options</p>
			<h2 class="qq-h2">What Options Could Be Available?</h2>
			<p class="qq-lead">The right approach depends on the company&rsquo;s debts, assets, cash flow and future prospects.</p>
		</div>
		<div class="qq-options__grid">
			<div class="qq-option">
				<h3 class="qq-option__title">Continue or Rescue the Business</h3>
				<p class="qq-option__text">If the business is viable, this can mean better cash flow, negotiating with creditors, or a formal restructuring process.</p>
			</div>
			<div class="qq-option">
				<h3 class="qq-option__title">Close an Insolvent Company</h3>
				<p class="qq-option__text">Where recovery isn&rsquo;t realistic, a Creditors&rsquo; Voluntary Liquidation closes the company in an orderly way.</p>
			</div>
			<div class="qq-option">
				<h3 class="qq-option__title">Consider Another Route</h3>
				<p class="qq-option__text">Some companies suit a different closure or insolvency procedure. We&rsquo;ll explain which after reviewing your position.</p>
			</div>
		</div>
		<p class="qq-options__foot">You do not need to choose an option before contacting us.</p>
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
			<p class="qq-eyebrow">Company debt and insolvency</p>
			<h2 class="qq-h2">Frequently Asked Questions</h2>
		</div>
		<div class="qq-faq__list">
			<div class="qq-faq__item">
				<button class="qq-faq__q" type="button" aria-expanded="false">
					<span>Do I Need to Know Which Option the Company Requires?</span>
					<span class="qq-faq__sign" aria-hidden="true">+</span>
				</button>
				<div class="qq-faq__a">
					<p>No. Many directors contact us before they know whether the company can continue, needs restructuring or should close.</p>
					<p>Tell us what is happening and we will explain which options appear realistic. You are not expected to understand insolvency procedures before asking for help.</p>
				</div>
			</div>
			<div class="qq-faq__item">
				<button class="qq-faq__q" type="button" aria-expanded="false">
					<span>Can the Company Still Be Rescued?</span>
					<span class="qq-faq__sign" aria-hidden="true">+</span>
				</button>
				<div class="qq-faq__a">
					<p>Possibly. This depends on whether the underlying business is viable, why the financial problems arose and whether the company can meet its future costs.</p>
					<p>Possible solutions may include improving cash flow, negotiating with creditors, agreeing a Time to Pay arrangement with HMRC or considering a formal restructuring procedure. We will also tell you honestly if rescue does not appear realistic.</p>
				</div>
			</div>
			<div class="qq-faq__item">
				<button class="qq-faq__q" type="button" aria-expanded="false">
					<span>How Much Does It Cost to Liquidate a Company?</span>
					<span class="qq-faq__sign" aria-hidden="true">+</span>
				</button>
				<div class="qq-faq__a">
					<p>The cost depends on factors including the number of creditors, employees and company assets, the quality of the accounting records and the complexity of the case.</p>
					<p>The figures you provide can be used to give an initial indication. The final fee and everything included in it should be explained clearly before you decide whether to proceed.</p>
				</div>
			</div>
			<div class="qq-faq__item">
				<button class="qq-faq__q" type="button" aria-expanded="false">
					<span>Do I Have to Proceed After Making an Enquiry?</span>
					<span class="qq-faq__sign" aria-hidden="true">+</span>
				</button>
				<div class="qq-faq__a">
					<p>No. Completing the form or speaking with our team does not commit you to a formal insolvency procedure. You can ask questions, consider the information and decide what to do without any pressure to appoint us.</p>
				</div>
			</div>
			<div class="qq-faq__item">
				<button class="qq-faq__q" type="button" aria-expanded="false">
					<span>Will the Company&rsquo;s Debts Become My Personal Debts?</span>
					<span class="qq-faq__sign" aria-hidden="true">+</span>
				</button>
				<div class="qq-faq__a">
					<p>Directors are not normally personally responsible for debts taken out in the company&rsquo;s name. However, you may remain responsible for debts covered by a personal guarantee.</p>
					<p>Personal liability can also arise in some circumstances involving director conduct or particular liabilities. We will ask about any personal guarantees or related concerns during the consultation.</p>
				</div>
			</div>
			<div class="qq-faq__item">
				<button class="qq-faq__q" type="button" aria-expanded="false">
					<span>Could I Qualify for Director Redundancy?</span>
					<span class="qq-faq__sign" aria-hidden="true">+</span>
				</button>
				<div class="qq-faq__a">
					<p>Some company directors may qualify for statutory redundancy and other employment-related payments if they were also genuine employees of the company.</p>
					<p>Eligibility depends on factors including employment status, working arrangements and length of service. The Redundancy Payments Service assesses each claim and makes the final decision.</p>
				</div>
			</div>
			<div class="qq-faq__item">
				<button class="qq-faq__q" type="button" aria-expanded="false">
					<span>How Long Does a Company Liquidation Take?</span>
					<span class="qq-faq__sign" aria-hidden="true">+</span>
				</button>
				<div class="qq-faq__a">
					<p>The timescale varies according to the company&rsquo;s size and complexity, the assets that need to be realised and any matters that require investigation.</p>
					<p>A typical liquidation may remain open for 12 to 18 months, although the director&rsquo;s main involvement is usually concentrated near the beginning of the process. The likely timescale should be explained before you proceed.</p>
				</div>
			</div>
		</div>
	</section>

	<!-- FINAL CTA -->
	<section class="qq-finalcta">
		<div class="qq-finalcta__inner">
			<h2 class="qq-h2">Understand Your Company&rsquo;s Options</h2>
			<p class="qq-finalcta__text">Answer a few questions about the company&rsquo;s current financial position. We will explain the realistic options, likely costs and next steps. There is no obligation to proceed.</p>
			<a href="#quick-quote-form" class="qq-btn qq-btn--solid">Understand My Options</a>
			<p class="qq-finalcta__sub">or speak confidentially with an adviser on <a href="tel:08000746757" style="color:#fff;">0800 074 6757</a></p>
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
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Do I Need to Know Which Option the Company Requires?","acceptedAnswer":{"@type":"Answer","text":"No. Many directors contact us before they know whether the company can continue, needs restructuring or should close. Tell us what is happening and we will explain which options appear realistic. You are not expected to understand insolvency procedures before asking for help."}},{"@type":"Question","name":"Can the Company Still Be Rescued?","acceptedAnswer":{"@type":"Answer","text":"Possibly. This depends on whether the underlying business is viable, why the financial problems arose and whether the company can meet its future costs. Possible solutions may include improving cash flow, negotiating with creditors, agreeing a Time to Pay arrangement with HMRC or considering a formal restructuring procedure. We will also tell you honestly if rescue does not appear realistic."}},{"@type":"Question","name":"How Much Does It Cost to Liquidate a Company?","acceptedAnswer":{"@type":"Answer","text":"The cost depends on factors including the number of creditors, employees and company assets, the quality of the accounting records and the complexity of the case. The figures you provide can be used to give an initial indication. The final fee and everything included in it should be explained clearly before you decide whether to proceed."}},{"@type":"Question","name":"Do I Have to Proceed After Making an Enquiry?","acceptedAnswer":{"@type":"Answer","text":"No. Completing the form or speaking with our team does not commit you to a formal insolvency procedure. You can ask questions, consider the information and decide what to do without any pressure to appoint us."}},{"@type":"Question","name":"Will the Company's Debts Become My Personal Debts?","acceptedAnswer":{"@type":"Answer","text":"Directors are not normally personally responsible for debts taken out in the company's name. However, you may remain responsible for debts covered by a personal guarantee. Personal liability can also arise in some circumstances involving director conduct or particular liabilities."}},{"@type":"Question","name":"Could I Qualify for Director Redundancy?","acceptedAnswer":{"@type":"Answer","text":"Some company directors may qualify for statutory redundancy and other employment-related payments if they were also genuine employees of the company. Eligibility depends on factors including employment status, working arrangements and length of service. The Redundancy Payments Service assesses each claim and makes the final decision."}},{"@type":"Question","name":"How Long Does a Company Liquidation Take?","acceptedAnswer":{"@type":"Answer","text":"The timescale varies according to the company's size and complexity, the assets that need to be realised and any matters that require investigation. A typical liquidation may remain open for 12 to 18 months, although the director's main involvement is usually concentrated near the beginning of the process."}}]}
</script>

<script>
/* Cosmetic only: relabel GF40's submit button to match the design.
   Does not change the form, its fields, or the submission. */
document.addEventListener('DOMContentLoaded', function () {
	var btn = document.getElementById('gform_submit_button_40');
	if (btn) { btn.value = 'Understand My Options'; }

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
