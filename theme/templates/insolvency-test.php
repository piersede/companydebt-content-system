<?php
/* Template Name: Insolvency Test (Multi-Step Rebuild) */
/*
 * /insolvency-calculator/ — multi-step guided assessment.
 *
 * This template is markup-only. Style and behaviour live in dedicated files
 * and are enqueued from functions.php:
 *   theme/assets/css/insolvency-test.css   (design system + component styles)
 *   theme/assets/js/insolvency-test.js     (client-side flow + GF REST submit)
 *
 * The capture form is a real Gravity Form (id stored in wp_options
 * ['cd_insolvency_test_form_id'], set by scripts/gf_create_insolvency_test_form.py).
 * Lead pushed to Zoho via wp-content/mu-plugins/cd-insolvency-test-zoho.php
 * on the gform_entry_created hook. GA4 events fire via dataLayer through GTM.
 */

$cd_itest_form_id = (int) get_option( 'cd_insolvency_test_form_id', 0 );

// Chris Andersen headshot — the same file used on the site's author pages.
// Falls back to the theme placeholder if the file has been renamed on live.
$cd_itest_chris_photo = 'https://' . $_SERVER['HTTP_HOST']
    . '/wp-content/uploads/2022/06/Chris-Anderson-Insolvency-Practitioner-1-300x300.jpg';

get_header();
?>
<main id="primary" class="site-main cd-itest-main" data-cd-form-id="<?php echo esc_attr( $cd_itest_form_id ); ?>">

<?php if ( ! $cd_itest_form_id ) : ?>
    <div style="max-width:720px;margin:60px auto;padding:24px;border:1px solid #ffd9b3;background:#fff6ef;border-radius:10px;font-family:Arial,sans-serif;color:#a13f00">
        <strong>Insolvency Test not yet initialised.</strong>
        <p>Run <code>python scripts/gf_create_insolvency_test_form.py</code> to create the capture form, then reload this page.</p>
    </div>
<?php else : ?>

<div class="cd-itest-progress-wrap" id="cd-itest-progressWrap" style="display:none">
    <div class="cd-itest-progress-track"><div class="cd-itest-progress-fill" id="cd-itest-progressFill"></div></div>
    <div class="cd-itest-progress-label" id="cd-itest-progressLabel"></div>
</div>

<button class="cd-itest-back-btn" id="cd-itest-backBtn" type="button" aria-label="Back to previous step">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg>
    Back
</button>

<div class="cd-itest-panel cd-itest-panel--intro">

    <?php // ── STEP 0 · INTRO ─────────────────────────────────────────── ?>
    <section class="cd-itest-step cd-itest-step--active" data-stage="0" id="cd-itest-step-intro" role="group" aria-label="Introduction">
        <h1 class="cd-itest-h1">Worried Your Company May Be Insolvent?</h1>
        <p class="cd-itest-lede">Answer a few short questions to receive a personalised initial result showing the warning signs that apply, how serious the position may be and what your company may need to do next.</p>
        <p class="cd-itest-lede-sub">Financial pressure does not always mean that a company is insolvent. This check helps you understand the position more clearly.</p>
        <ul class="cd-itest-trust-list">
            <li><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>Takes around two minutes</li>
            <li><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>Estimates are fine &mdash; no accounts required</li>
            <li><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>Your answers are treated confidentially</li>
            <li><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>No credit check or Companies House search</li>
        </ul>
        <?php // Checklist leads directly into the CTA — no boxed panel between
              // the reassurance points and the button. The Reviews.io line
              // moved to the bottom of the screen as a small unboxed line
              // (below reg-line, above the disclaimer). ?>
        <div class="cd-itest-cta-row">
            <button class="cd-itest-btn-primary cd-itest-btn-primary--intro" type="button" data-cd-goto="cashflow">Check My Company&rsquo;s Position</button>
            <p class="cd-itest-value-reassure">Takes around two minutes &middot; Personalised result &middot; No obligation</p>
            <p class="cd-itest-phone-alt">Prefer to speak to someone now? Call <a href="tel:08000746757">0800 074 6757</a> for a confidential conversation.</p>
        </div>
        <p class="cd-itest-reg-line cd-itest-reg-line--centered">Helping UK company directors since 2007. Formal insolvency work is handled by licensed insolvency practitioners regulated by the Insolvency Practitioners Association.</p>
        <a class="cd-itest-reviews-line" href="https://www.reviews.io/company-reviews/store/companydebt-com" target="_blank" rel="noopener">
            <span class="cd-itest-reviews-line__stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</span> Rated Excellent on Reviews.io
        </a>
        <p class="cd-itest-disclaimer">This check identifies common warning signs and provides initial guidance. It is not a formal insolvency opinion.</p>
    </section>

    <?php // ── STEP 1 · CASHFLOW (auto-advance) ─────────────────────────── ?>
    <section class="cd-itest-step" data-stage="1" id="cd-itest-step-cashflow" role="group" aria-label="Question 1 of 4: cashflow">
        <h2 class="cd-itest-q">Can the company currently pay its bills when they fall due?</h2>
        <?php // "Yes, comfortably" removed 2026-08-05 (Piers): a director in
              // that position would not have started this check, so offering
              // it as an answer implied the tool is for anyone rather than
              // for people already worried about the company. The JS scorer
              // has no handler for 'comfortable' so nothing else needs
              // touching there. ?>
        <ul class="cd-itest-options" id="cd-itest-opts-cashflow">
            <li class="cd-itest-opt"><input type="radio" name="cd_cashflow" id="cd-cf-2" value="difficulty"><label for="cd-cf-2">Yes, but only with difficulty</label></li>
            <li class="cd-itest-opt"><input type="radio" name="cd_cashflow" id="cd-cf-3" value="late"><label for="cd-cf-3">Some payments are already late</label></li>
            <li class="cd-itest-opt"><input type="radio" name="cd_cashflow" id="cd-cf-4" value="cannot"><label for="cd-cf-4">No, it cannot pay everything</label></li>
            <li class="cd-itest-opt"><input type="radio" name="cd_cashflow" id="cd-cf-5" value="unsure"><label for="cd-cf-5">I&rsquo;m not sure</label></li>
        </ul>
    </section>

    <?php // ── STEP 2 · WARNING SIGNS (checkboxes + continue) ──────────── ?>
    <section class="cd-itest-step" data-stage="2" id="cd-itest-step-warning" role="group" aria-label="Question 2 of 4: warning signs">
        <h2 class="cd-itest-q">Which of these are happening now?</h2>
        <p class="cd-itest-lede-sub">Select all that apply.</p>
        <ul class="cd-itest-options" id="cd-itest-opts-warning">
            <li class="cd-itest-opt"><input type="checkbox" name="cd_warning" id="cd-w-1" value="hmrc_overdue"><label for="cd-w-1">HMRC payments are overdue</label></li>
            <li class="cd-itest-opt"><input type="checkbox" name="cd_warning" id="cd-w-2" value="payroll_risk"><label for="cd-w-2">Payroll may not be met</label></li>
            <li class="cd-itest-opt"><input type="checkbox" name="cd_warning" id="cd-w-3" value="supplier_pressure"><label for="cd-w-3">Suppliers are chasing or reducing credit</label></li>
            <li class="cd-itest-opt"><input type="checkbox" name="cd_warning" id="cd-w-4" value="bank_limit"><label for="cd-w-4">The bank account or overdraft is at its limit</label></li>
            <li class="cd-itest-opt"><input type="checkbox" name="cd_warning" id="cd-w-5" value="personal_funds_reliance"><label for="cd-w-5">Personal funds are keeping the company going</label></li>
            <li class="cd-itest-opt"><input type="checkbox" name="cd_warning" id="cd-w-none" value="none"><label for="cd-w-none">None of these</label></li>
        </ul>
        <button class="cd-itest-btn-primary" type="button" data-cd-submit="warning">Continue</button>
    </section>

    <?php // ── STEP 3 · POSITION (auto-advance, conditional branch) ────── ?>
    <section class="cd-itest-step" data-stage="3" id="cd-itest-step-position" role="group" aria-label="Question 3 of 4: financial position">
        <h2 class="cd-itest-q">Which Best Describes the Company&rsquo;s Overall Financial Position?</h2>
        <ul class="cd-itest-options" id="cd-itest-opts-position">
            <li class="cd-itest-opt"><input type="radio" name="cd_position" id="cd-pos-1" value="assets_more"><label for="cd-pos-1">The company&rsquo;s cash and assets are worth more than everything it owes</label></li>
            <li class="cd-itest-opt"><input type="radio" name="cd_position" id="cd-pos-2" value="about_same"><label for="cd-pos-2">The company&rsquo;s cash and assets are worth about the same as everything it owes</label></li>
            <li class="cd-itest-opt"><input type="radio" name="cd_position" id="cd-pos-3" value="debts_more"><label for="cd-pos-3">The company owes more than its cash and assets are worth</label></li>
            <li class="cd-itest-opt"><input type="radio" name="cd_position" id="cd-pos-4" value="unsure"><label for="cd-pos-4">I&rsquo;m not sure</label></li>
        </ul>
    </section>

    <?php // ── STEP 3b · DEBT RANGE (conditional, auto-advance) ────────── ?>
    <section class="cd-itest-step" data-stage="3" id="cd-itest-step-debtrange" role="group" aria-label="Question 3 continued: debt range">
        <h2 class="cd-itest-q">Roughly how much does the company owe in total?</h2>
        <ul class="cd-itest-options" id="cd-itest-opts-debtrange">
            <li class="cd-itest-opt"><input type="radio" name="cd_debtrange" id="cd-dr-1" value="under10k"><label for="cd-dr-1">Under &pound;10,000</label></li>
            <li class="cd-itest-opt"><input type="radio" name="cd_debtrange" id="cd-dr-2" value="10-25k"><label for="cd-dr-2">&pound;10,000&ndash;&pound;25,000</label></li>
            <li class="cd-itest-opt"><input type="radio" name="cd_debtrange" id="cd-dr-3" value="25-50k"><label for="cd-dr-3">&pound;25,000&ndash;&pound;50,000</label></li>
            <li class="cd-itest-opt"><input type="radio" name="cd_debtrange" id="cd-dr-4" value="50-100k"><label for="cd-dr-4">&pound;50,000&ndash;&pound;100,000</label></li>
            <li class="cd-itest-opt"><input type="radio" name="cd_debtrange" id="cd-dr-5" value="100-250k"><label for="cd-dr-5">&pound;100,000&ndash;&pound;250,000</label></li>
            <li class="cd-itest-opt"><input type="radio" name="cd_debtrange" id="cd-dr-6" value="over250k"><label for="cd-dr-6">More than &pound;250,000</label></li>
            <li class="cd-itest-opt"><input type="radio" name="cd_debtrange" id="cd-dr-7" value="unsure"><label for="cd-dr-7">I&rsquo;m not sure</label></li>
        </ul>
    </section>

    <?php // ── STEP 4 · RISK FACTORS (checkboxes + continue) ───────────── ?>
    <section class="cd-itest-step" data-stage="4" id="cd-itest-step-risk" role="group" aria-label="Question 4 of 4: risk factors">
        <h2 class="cd-itest-q">Do any of these apply?</h2>
        <p class="cd-itest-lede-sub">Select all that apply.</p>
        <ul class="cd-itest-options" id="cd-itest-opts-risk">
            <li class="cd-itest-opt"><input type="checkbox" name="cd_risk" id="cd-r-1" value="personal_guarantee"><label for="cd-r-1">I have signed a personal guarantee for company borrowing</label></li>
            <li class="cd-itest-opt"><input type="checkbox" name="cd_risk" id="cd-r-2" value="statutory"><label for="cd-r-2">The company has received a statutory demand, winding-up petition or enforcement notice</label></li>
            <li class="cd-itest-opt"><input type="checkbox" name="cd_risk" id="cd-r-3" value="stopped_trading"><label for="cd-r-3">The company has stopped trading</label></li>
            <li class="cd-itest-opt"><input type="checkbox" name="cd_risk" id="cd-r-4" value="preferential"><label for="cd-r-4">The company cannot pay everyone and I am having to decide which creditors to pay</label></li>
            <li class="cd-itest-opt"><input type="checkbox" name="cd_risk" id="cd-r-none" value="none"><label for="cd-r-none">None of these</label></li>
        </ul>
        <button class="cd-itest-btn-primary" type="button" data-cd-submit="risk">See My Result</button>
    </section>

    <?php // ── STEP 5 · CAPTURE (value exchange before result) ─────────── ?>
    <?php // Rebuilt 2026-08-05 per Piers's spec: heading reframed ("Your
          // Result Is Ready"), call-preference options styled as visible
          // radio cards with a subtitle rather than plain input-lookalikes,
          // "No, email only" defaulted to checked so the low-pressure route
          // is the path of least resistance, large sidebar trust panel
          // (including Chris Andersen photo + Reviews.io claim) replaced
          // with two short reassurance lines directly under the CTA. The
          // practitioner attribution moved to the result page, where the
          // named authority actually earns its keep. ?>
    <section class="cd-itest-step" data-stage="5" id="cd-itest-step-capture" role="group" aria-label="Your details">
        <h2 class="cd-itest-q">Your Result Is Ready</h2>
        <p class="cd-itest-lede">Enter your details to view your personalised result and receive a copy by email.</p>

        <div class="cd-itest-field-grid">
            <div class="cd-itest-field"><label for="cd-c-name">First name</label><input type="text" id="cd-c-name" autocomplete="given-name" placeholder="Jordan"></div>
            <div class="cd-itest-field"><label for="cd-c-email">Email address</label><input type="email" id="cd-c-email" autocomplete="email" placeholder="you@company.co.uk"></div>
        </div>

        <div class="cd-itest-field cd-itest-callpref">
            <label class="cd-itest-callpref__q">Would You Like Someone to Talk Through Your Result?</label>
            <ul class="cd-itest-options cd-itest-callpref-options">
                <li class="cd-itest-opt cd-itest-opt--rich">
                    <input type="radio" name="cd_callpref" id="cd-cp-yes" value="yes">
                    <label for="cd-cp-yes">
                        <span class="cd-itest-opt__title">Yes, please call me</span>
                        <span class="cd-itest-opt__sub">I would like a confidential call about my result.</span>
                    </label>
                </li>
                <li class="cd-itest-opt cd-itest-opt--rich">
                    <input type="radio" name="cd_callpref" id="cd-cp-no" value="no" checked>
                    <label for="cd-cp-no">
                        <span class="cd-itest-opt__title">No, email only</span>
                        <span class="cd-itest-opt__sub">Send my result by email. No call will be made.</span>
                    </label>
                </li>
            </ul>
        </div>

        <div class="cd-itest-reveal" id="cd-itest-callbackFields">
            <div class="cd-itest-field"><label for="cd-c-phone">Phone number</label><input type="tel" id="cd-c-phone" autocomplete="tel" placeholder="07&hellip;"></div>
            <div class="cd-itest-field"><label>Preferred time</label>
                <ul class="cd-itest-options cd-itest-options--compact">
                    <li class="cd-itest-opt"><input type="radio" name="cd_calltime" id="cd-ct-1" value="Morning"><label for="cd-ct-1">Morning</label></li>
                    <li class="cd-itest-opt"><input type="radio" name="cd_calltime" id="cd-ct-2" value="Afternoon"><label for="cd-ct-2">Afternoon</label></li>
                    <li class="cd-itest-opt"><input type="radio" name="cd_calltime" id="cd-ct-3" value="Evening"><label for="cd-ct-3">Evening</label></li>
                    <li class="cd-itest-opt"><input type="radio" name="cd_calltime" id="cd-ct-4" value="Any time"><label for="cd-ct-4">Any time</label></li>
                </ul>
            </div>
        </div>

        <button class="cd-itest-btn-primary" type="button" id="cd-itest-capture-submit">See My Result</button>
        <p class="cd-itest-error" id="cd-itest-err-capture">Please add your name and a valid email address.</p>
        <p class="cd-itest-error" id="cd-itest-err-network" style="display:none">We could not save your details just now. Please try again, or call <a href="tel:08000746757">0800 074 6757</a>.</p>

        <p class="cd-itest-capture-reassure">Your result will be sent immediately. A call will only be made if you request one.</p>
        <p class="cd-itest-capture-trust">Your details are treated confidentially. Company Debt has helped UK company directors since 2007, with formal insolvency work handled by licensed insolvency practitioners.</p>
        <p class="cd-itest-capture-phone">Prefer to speak now? Call <a href="tel:08000746757">0800 074 6757</a>.</p>
    </section>

    <?php // ── STEP 6 · RESULT (post-capture) ──────────────────────────── ?>
    <section class="cd-itest-step" data-stage="6" id="cd-itest-step-result" role="group" aria-label="Your result">

        <span class="cd-itest-result-badge" id="cd-itest-resultBadge"></span>
        <h2 class="cd-itest-result-title" id="cd-itest-resultTitle"></h2>
        <p class="cd-itest-result-urgency" id="cd-itest-resultUrgency"></p>

        <div class="cd-itest-result-section" id="cd-itest-resultReasonsSection">
            <h3>Warning Signs Identified</h3>
            <ul id="cd-itest-resultReasons"></ul>
        </div>

        <div id="cd-itest-pgNote" class="cd-itest-callout cd-itest-callout--warm" style="display:none">
            <h4 class="cd-itest-callout__title">You Mentioned a Personal Guarantee</h4>
            <p>A personal guarantee does not determine whether the company is insolvent, but it could make you personally responsible for some borrowing if the company cannot repay it. Have the guarantee reviewed before making decisions based on it.</p>
        </div>

        <div id="cd-itest-creditorNote" class="cd-itest-callout cd-itest-callout--warn" style="display:none">
            <h4 class="cd-itest-callout__title">You Mentioned Deciding Which Creditors to Pay</h4>
            <p>Until the position has been reviewed, take care not to favour particular creditors, repay connected parties or transfer company assets outside normal business activity.</p>
        </div>

        <div class="cd-itest-result-section">
            <h3>What to Do Now</h3>
            <ol class="cd-itest-steps-ol" id="cd-itest-resultSteps"></ol>
        </div>

        <div class="cd-itest-result-section" id="cd-itest-resultOptionsSection">
            <h3>What a Professional Review May Consider</h3>
            <p class="cd-itest-result-section__intro" id="cd-itest-resultOptionsIntro"></p>
            <ul id="cd-itest-resultOptions"></ul>
            <p class="cd-itest-result-section__note">These are possible routes rather than recommendations. The appropriate option depends on a review of the company&rsquo;s full financial position.</p>
        </div>

        <?php // Practitioner attribution — moved here from the capture screen
              // where Piers felt Chris's photo + "Licensed Insolvency
              // Practitioner" role next to the form made a nervous user
              // think they were entering a formal insolvency process.
              // Post-result it earns its keep as professional authority. ?>
        <div class="cd-itest-attribution">
            <div class="cd-itest-attribution__photo">
                <img src="<?php echo esc_url( $cd_itest_chris_photo ); ?>" alt="Chris Andersen, Licensed Insolvency Practitioner" width="56" height="56" loading="lazy">
            </div>
            <p class="cd-itest-attribution__text">
                This assessment has been developed with input from licensed insolvency practitioners, including <strong>Chris Andersen</strong>.
            </p>
        </div>

        <div class="cd-itest-cta-block">
            <h3>Speak to Someone About Your Result</h3>
            <a href="tel:08000746757" class="cd-itest-btn-primary cd-itest-btn-primary--cta">Request a Confidential Call</a>
            <p class="cd-itest-note-sm">Prefer to speak now? Call <a href="tel:08000746757">0800 074 6757</a> for a confidential conversation about your result.</p>
        </div>

        <div id="cd-itest-resultConfirmBanner" class="cd-itest-confirm-quiet" style="display:none"></div>

        <p class="cd-itest-disclaimer">This screening result is based on the answers provided. It identifies warning signs but is not a formal determination of insolvency.</p>
    </section>

</div>

<?php endif; // form-id guard ?>

</main>
<?php get_footer();
