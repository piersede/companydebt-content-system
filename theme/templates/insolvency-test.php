<?php
/* Template Name: Insolvency Test (Multi-Step Rebuild) */
/*
 * The multi-step redesign of the /insolvency-calculator/ tool.
 * Replaces the old single-screen slider calculator (templates/quiz-insolvency.php,
 * Gravity Form 38) which had a fragile custom-button submit chain.
 *
 * Flow: intro -> cashflow -> warning signs -> position -> (conditional debt range)
 *       -> risk factors -> capture -> result. Client-side navigation + scoring,
 * capture step POSTs to Gravity Forms via the REST submissions endpoint (which
 * runs full validation and notifications without touching the fragile DOM submit
 * chain that blocked form 38). Zoho lead push runs in a proper mu-plugin hooked
 * to gform_after_submission. GA4 events fire per step via dataLayer.
 *
 * Form ID is stored in wp_options['cd_insolvency_test_form_id'] (set by
 * scripts/gf_create_insolvency_test_form.py). Template refuses to render if
 * the form does not exist.
 */

$cd_itest_form_id = (int) get_option( 'cd_insolvency_test_form_id', 0 );
$cd_itest_chris_photo = 'https://' . $_SERVER['HTTP_HOST'] . '/wp-content/uploads/2022/06/Chris-Anderson-Insolvency-Practitioner-1-300x300.jpg';

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
    <div class="cd-itest-progress-track"><div class="cd-itest-progress-fill" id="cd-itest-progressFill" style="width:0%"></div></div>
    <div class="cd-itest-progress-label" id="cd-itest-progressLabel"></div>
</div>

<button class="cd-itest-back-btn" id="cd-itest-backBtn" type="button">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg>
    Back
</button>

<div class="cd-itest-panel">

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
        <a class="cd-itest-proof-strip" href="https://www.reviews.io/company-reviews/store/companydebt-com" target="_blank" rel="noopener">
            <span class="cd-itest-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
            <span><strong>Excellent</strong> &middot; Rated 5.0 on Reviews.io</span>
        </a>
        <div class="cd-itest-cta-row">
            <button class="cd-itest-btn-primary cd-itest-btn-primary--intro" type="button" data-cd-goto="cashflow">Check My Company&rsquo;s Position</button>
            <p class="cd-itest-value-reassure">A few short questions &middot; Personalised result &middot; No obligation</p>
            <p class="cd-itest-phone-alt">Prefer to speak to someone now? Call <a href="tel:08000746757">0800 074 6757</a> for a confidential conversation.</p>
        </div>
        <p class="cd-itest-reg-line cd-itest-reg-line--centered">Company Debt has helped UK company directors since 2007. Where formal insolvency work is required, it is handled by licensed insolvency practitioners regulated by the Insolvency Practitioners Association.</p>
        <p class="cd-itest-disclaimer">This check identifies common warning signs and provides initial guidance. It is not a formal insolvency opinion.</p>
    </section>

    <?php // ── STEP 1 · CASHFLOW (auto-advance) ─────────────────────────── ?>
    <section class="cd-itest-step" data-stage="1" id="cd-itest-step-cashflow" role="group" aria-label="Question 1 of 4: cashflow">
        <h2 class="cd-itest-q">Can the company currently pay its bills when they fall due?</h2>
        <ul class="cd-itest-options" id="cd-itest-opts-cashflow">
            <li class="cd-itest-opt"><input type="radio" name="cd_cashflow" id="cd-cf-1" value="comfortable"><label for="cd-cf-1">Yes, comfortably</label></li>
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
        <h2 class="cd-itest-q">Which best describes the company&rsquo;s overall financial position?</h2>
        <ul class="cd-itest-options" id="cd-itest-opts-position">
            <li class="cd-itest-opt"><input type="radio" name="cd_position" id="cd-pos-1" value="assets_more"><label for="cd-pos-1">Its available cash and assets are probably worth more than it owes</label></li>
            <li class="cd-itest-opt"><input type="radio" name="cd_position" id="cd-pos-2" value="about_same"><label for="cd-pos-2">They are probably worth about the same</label></li>
            <li class="cd-itest-opt"><input type="radio" name="cd_position" id="cd-pos-3" value="debts_more"><label for="cd-pos-3">The company probably owes more than its cash and assets are worth</label></li>
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
    <section class="cd-itest-step" data-stage="5" id="cd-itest-step-capture" role="group" aria-label="Your details">
        <h2 class="cd-itest-q">Where Should We Send Your Result?</h2>
        <p class="cd-itest-lede">Enter your details to view your personalised result and receive a copy by email.</p>
        <div class="cd-itest-field-grid">
            <div class="cd-itest-field"><label for="cd-c-name">First name</label><input type="text" id="cd-c-name" autocomplete="given-name" placeholder="Jordan"></div>
            <div class="cd-itest-field"><label for="cd-c-email">Email address</label><input type="email" id="cd-c-email" autocomplete="email" placeholder="you@company.co.uk"></div>
        </div>
        <div class="cd-itest-field" style="margin-bottom:20px">
            <label>Would you like an adviser to talk through your result?</label>
            <ul class="cd-itest-options cd-itest-options--compact">
                <li class="cd-itest-opt"><input type="radio" name="cd_callpref" id="cd-cp-yes" value="yes"><label for="cd-cp-yes">Yes, please call me</label></li>
                <li class="cd-itest-opt"><input type="radio" name="cd_callpref" id="cd-cp-no" value="no"><label for="cd-cp-no">No, email only</label></li>
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
        <p class="cd-itest-error" id="cd-itest-err-capture">Please add your name, a valid email address, and choose whether you would like a call.</p>
        <p class="cd-itest-error" id="cd-itest-err-network" style="display:none">We could not save your details just now. Please try again, or call <a href="tel:08000746757">0800 074 6757</a>.</p>

        <div class="cd-itest-sidebar-trust">
            <div class="cd-itest-expert-row">
                <div class="cd-itest-expert-photo">
                    <img src="<?php echo esc_url( $cd_itest_chris_photo ); ?>" alt="Chris Andersen, Licensed Insolvency Practitioner" width="64" height="64" loading="lazy">
                </div>
                <div>
                    <div class="cd-itest-expert-name">Chris Andersen</div>
                    <div class="cd-itest-expert-role">Licensed Insolvency Practitioner</div>
                </div>
            </div>
            <ul>
                <li><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>Your result is emailed immediately; a call only happens if you request one</li>
                <li><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>Any conversation is confidential and without obligation</li>
                <li><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>Company Debt has advised UK company directors since 2007</li>
                <li><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>Formal insolvency appointments are handled by licensed insolvency practitioners</li>
                <li><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>Rated 5.0 by clients on Reviews.io</li>
                <li><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>We will not sell your details</li>
                <li><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>Prefer to talk now? Call <a href="tel:08000746757">0800 074 6757</a></li>
            </ul>
        </div>
    </section>

    <?php // ── STEP 6 · RESULT (post-capture) ──────────────────────────── ?>
    <section class="cd-itest-step" data-stage="6" id="cd-itest-step-result" role="group" aria-label="Your result">
        <div id="cd-itest-resultConfirmBanner" class="cd-itest-proof-strip" style="display:none;margin-bottom:24px"></div>
        <span class="cd-itest-result-badge" id="cd-itest-resultBadge"></span>
        <h2 class="cd-itest-result-title" id="cd-itest-resultTitle"></h2>
        <p class="cd-itest-result-urgency" id="cd-itest-resultUrgency"></p>
        <div class="cd-itest-result-section"><h3>Why you received this result</h3><ul id="cd-itest-resultReasons"></ul></div>
        <div id="cd-itest-pgNote" class="cd-itest-pg-note" style="display:none">You indicated that you may have signed a personal guarantee. This does not determine whether the company is insolvent, but it may affect your personal exposure if the company cannot repay the borrowing. Do not make payments or transfer assets without first understanding the terms of the guarantee.</div>
        <div class="cd-itest-result-section"><h3>Options that may be relevant</h3><ul id="cd-itest-resultOptions"></ul></div>
        <p class="cd-itest-note-sm">Prefer to talk sooner? Call <a href="tel:08000746757">0800 074 6757</a> &mdash; a member of our team is ready to help.</p>
    </section>

</div>
<?php endif; // form-id guard ?>

<style id="cd-itest-css">
/*
 * Insolvency Test — page-scoped styles. All rules are prefixed cd-itest- and
 * anchored to body.page-template-insolvency-test so nothing leaks to other pages.
 * Design tokens mirror the design-handoff bundle (2026-08-05).
 */
body.page-template-insolvency-test {
    --cdi-navy:#002856;
    --cdi-navy-dark:#102a43;
    --cdi-orange:#ff6600;
    --cdi-text:#2a2a2e;
    --cdi-grey:#52606d;
    --cdi-bg:#f4f6f8;
    --cdi-border:rgba(0,40,86,.14);
    --cdi-sp-1:10px; --cdi-sp-2:20px; --cdi-sp-3:30px; --cdi-sp-4:40px; --cdi-sp-5:52px; --cdi-sp-6:64px;
    --cdi-fs-xs:13px; --cdi-fs-sm:15px; --cdi-fs-base:16px; --cdi-fs-md:18px; --cdi-fs-lg:24px; --cdi-fs-xl:32px;
    background: var(--cdi-bg) !important;
}
body.page-template-insolvency-test .cd-itest-main {
    max-width: 1040px; margin: 0 auto; padding: var(--cdi-sp-5) var(--cdi-sp-2) var(--cdi-sp-6);
    font-family: Arial, "Segoe UI", Roboto, -apple-system, sans-serif;
    color: var(--cdi-text); line-height: 1.6; font-size: var(--cdi-fs-base);
}
body.page-template-insolvency-test .cd-itest-main *,
body.page-template-insolvency-test .cd-itest-main *::before,
body.page-template-insolvency-test .cd-itest-main *::after { box-sizing: border-box; }

.cd-itest-progress-wrap { max-width: 720px; margin: 0 auto var(--cdi-sp-3); }
.cd-itest-progress-track { height: 8px; background: #e2e7ec; border-radius: 999px; overflow: hidden; }
.cd-itest-progress-fill  { height: 100%; background: var(--cdi-orange); border-radius: 999px; transition: width .35s ease; }
.cd-itest-progress-label { font-size: var(--cdi-fs-xs); color: var(--cdi-grey); margin-top: var(--cdi-sp-1); font-weight: 600; }

.cd-itest-back-btn {
    display: none; align-items: center; gap: var(--cdi-sp-1);
    background: none; border: none; color: var(--cdi-grey);
    font-size: var(--cdi-fs-sm); font-weight: 700; cursor: pointer;
    margin: 0 auto var(--cdi-sp-2); padding: var(--cdi-sp-1) 0;
    max-width: 720px; width: 100%;
}
.cd-itest-back-btn.cd-itest-show { display: inline-flex; }

.cd-itest-panel {
    background: #fff; border: 1px solid var(--cdi-border); border-radius: 14px;
    box-shadow: 0 1px 3px rgba(0,40,86,.06);
    padding: var(--cdi-sp-5); max-width: 720px; min-height: 460px; margin: 0 auto;
    transition: min-height .25s ease;
}
.cd-itest-step { display: none; }
.cd-itest-step.cd-itest-step--active { display: block; animation: cdItestFade .3s ease; }
@keyframes cdItestFade { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }

body.page-template-insolvency-test .cd-itest-h1 {
    font-size: var(--cdi-fs-xl); line-height: 1.3; color: var(--cdi-navy);
    margin: 0 0 var(--cdi-sp-2); font-weight: 800;
}
body.page-template-insolvency-test .cd-itest-q {
    font-size: var(--cdi-fs-lg); line-height: 1.35; color: var(--cdi-navy);
    margin: 0 0 var(--cdi-sp-3); font-weight: 800;
}
.cd-itest-lede     { font-size: var(--cdi-fs-md); color: var(--cdi-grey); margin: 0 0 var(--cdi-sp-3); }
.cd-itest-lede-sub { font-size: var(--cdi-fs-sm); color: var(--cdi-grey); margin: 0 0 var(--cdi-sp-3); }
.cd-itest-note-sm  { color: var(--cdi-grey); font-size: var(--cdi-fs-sm); margin: 0; }
.cd-itest-reg-line { font-size: var(--cdi-fs-sm); color: var(--cdi-grey); margin: 0; line-height: 1.6; }
.cd-itest-reg-line--centered { text-align: center; margin: var(--cdi-sp-3) 0 0; }

.cd-itest-trust-list { list-style: none; margin: 0 0 var(--cdi-sp-3); padding: 0; display: grid; gap: var(--cdi-sp-1); }
.cd-itest-trust-list li { display: flex; gap: var(--cdi-sp-1); align-items: center; font-size: var(--cdi-fs-sm); color: var(--cdi-text); font-weight: 500; }
.cd-itest-trust-list li svg { flex-shrink: 0; color: var(--cdi-navy); opacity: .55; }

.cd-itest-proof-strip {
    display: flex; flex-wrap: wrap; align-items: center; gap: var(--cdi-sp-1);
    background: var(--cdi-bg); border: 1px solid var(--cdi-border);
    border-radius: 10px; padding: var(--cdi-sp-2); margin: 0 0 var(--cdi-sp-2);
    text-decoration: none; color: inherit;
}
.cd-itest-proof-strip:hover { text-decoration: none; color: inherit; }
.cd-itest-stars { color: var(--cdi-orange); letter-spacing: 1px; font-size: var(--cdi-fs-sm); }
.cd-itest-proof-strip strong { color: var(--cdi-navy); }
.cd-itest-proof-strip span    { font-size: var(--cdi-fs-sm); color: var(--cdi-grey); }

.cd-itest-cta-row {
    display: flex; flex-direction: column; align-items: center;
    text-align: center; gap: var(--cdi-sp-2); margin-top: var(--cdi-sp-1);
}
.cd-itest-value-reassure { font-size: var(--cdi-fs-sm); color: var(--cdi-grey); margin: 0; }
.cd-itest-phone-alt      { font-size: var(--cdi-fs-sm); color: var(--cdi-grey); margin: 0; }
.cd-itest-phone-alt a    { font-weight: 700; color: var(--cdi-navy); }

.cd-itest-disclaimer {
    font-size: var(--cdi-fs-xs); color: var(--cdi-grey); text-align: center;
    margin: var(--cdi-sp-3) 0 0; padding: var(--cdi-sp-3) 0 0;
    border-top: 1px solid var(--cdi-border);
}

.cd-itest-btn-primary {
    background: var(--cdi-orange) !important; color: #fff !important; border: none;
    border-radius: 999px; padding: var(--cdi-sp-2) var(--cdi-sp-4);
    font-size: var(--cdi-fs-md); font-weight: 800; cursor: pointer;
    text-decoration: none; display: inline-block; width: 100%; text-align: center;
    line-height: 1.4; font-family: inherit;
}
.cd-itest-btn-primary:hover { background: #e65c00 !important; color: #fff !important; }
.cd-itest-btn-primary:disabled { background: #d8dee3 !important; cursor: not-allowed; }
.cd-itest-btn-primary--intro { width: 78%; align-self: center; }

.cd-itest-options { list-style: none; margin: 0 0 var(--cdi-sp-3); padding: 0; display: grid; gap: var(--cdi-sp-2); }
.cd-itest-options--compact { margin-bottom: var(--cdi-sp-1); }
.cd-itest-opt { position: relative; }
.cd-itest-opt input {
    position: absolute; opacity: 0; inset: 0; cursor: pointer;
    width: 100%; height: 100%; margin: 0;
}
.cd-itest-opt label {
    display: flex; align-items: center; min-height: 44px;
    padding: var(--cdi-sp-2) var(--cdi-sp-3);
    border: 2px solid var(--cdi-border); border-radius: 10px;
    font-size: var(--cdi-fs-base); font-weight: 600; color: var(--cdi-text);
    cursor: pointer; transition: border-color .15s, background .15s;
    background: #fff;
}
.cd-itest-opt input:checked + label { border-color: var(--cdi-orange); background: #fff6ef; }
.cd-itest-opt input:focus-visible + label { outline: 2px solid var(--cdi-navy); outline-offset: 2px; }

.cd-itest-field-grid { display: grid; gap: var(--cdi-sp-2); margin-bottom: var(--cdi-sp-3); }
.cd-itest-field label { display: block; font-size: var(--cdi-fs-xs); font-weight: 700; color: var(--cdi-navy); margin-bottom: var(--cdi-sp-1); }
.cd-itest-field input[type=text],
.cd-itest-field input[type=email],
.cd-itest-field input[type=tel] {
    width: 100%; padding: var(--cdi-sp-2);
    border: 2px solid var(--cdi-border); border-radius: 10px;
    font-size: var(--cdi-fs-base); font-family: inherit;
    background: #fff; color: var(--cdi-text);
}
.cd-itest-field input:focus { outline: none; border-color: var(--cdi-navy); }

.cd-itest-error { color: #b3261e; font-size: var(--cdi-fs-xs); font-weight: 600; margin-top: var(--cdi-sp-2); display: none; }
.cd-itest-error.cd-itest-show { display: block; }

.cd-itest-reveal { display: none; margin-top: calc(var(--cdi-sp-1) * -1); padding-top: var(--cdi-sp-1); }
.cd-itest-reveal.cd-itest-show { display: grid; gap: var(--cdi-sp-2); margin-bottom: var(--cdi-sp-3); }

.cd-itest-result-badge {
    display: inline-block; padding: var(--cdi-sp-1) var(--cdi-sp-2);
    border-radius: 999px; font-weight: 800; font-size: var(--cdi-fs-sm);
    letter-spacing: .02em; margin-bottom: var(--cdi-sp-2);
}
.cd-itest-badge-none   { background: #e6f4ea; color: #1e6b3a; }
.cd-itest-badge-some   { background: #fff3cd; color: #8a6100; }
.cd-itest-badge-sig    { background: #ffe3cc; color: #a13f00; }
.cd-itest-badge-urgent { background: #fde2e1; color: #a3231b; }

body.page-template-insolvency-test .cd-itest-result-title {
    font-size: var(--cdi-fs-lg); font-weight: 800; color: var(--cdi-navy); margin: 0 0 var(--cdi-sp-1);
}
.cd-itest-result-urgency { font-size: var(--cdi-fs-sm); font-weight: 700; color: var(--cdi-orange); margin: 0 0 var(--cdi-sp-3); }
.cd-itest-result-section { margin-bottom: var(--cdi-sp-3); }
.cd-itest-result-section h3 { font-size: var(--cdi-fs-sm); color: var(--cdi-navy); margin: 0 0 var(--cdi-sp-1); text-transform: uppercase; letter-spacing: .03em; }
.cd-itest-result-section ul { margin: 0; padding-left: var(--cdi-sp-3); }
.cd-itest-result-section p  { margin: 0 0 var(--cdi-sp-1); color: var(--cdi-grey); font-size: var(--cdi-fs-base); }

.cd-itest-pg-note {
    background: #fff6ef; border: 1px solid #ffd9b3; border-radius: 10px;
    padding: var(--cdi-sp-2); font-size: var(--cdi-fs-sm); color: var(--cdi-text);
    margin-bottom: var(--cdi-sp-3);
}

.cd-itest-sidebar-trust {
    background: var(--cdi-bg); border: 1px solid var(--cdi-border);
    border-radius: 12px; padding: var(--cdi-sp-3); margin-top: var(--cdi-sp-4);
}
.cd-itest-expert-row { display: flex; flex-wrap: wrap; gap: var(--cdi-sp-2); align-items: center; margin-bottom: var(--cdi-sp-2); }
.cd-itest-expert-photo { width: 64px; height: 64px; border-radius: 50%; overflow: hidden; flex-shrink: 0; }
.cd-itest-expert-photo img { width: 100%; height: 100%; object-fit: cover; }
.cd-itest-expert-name { font-weight: 800; color: var(--cdi-navy); font-size: var(--cdi-fs-sm); }
.cd-itest-expert-role { font-size: var(--cdi-fs-xs); color: var(--cdi-grey); }
.cd-itest-sidebar-trust ul { list-style: none; margin: 0; padding: 0; display: grid; gap: var(--cdi-sp-1); font-size: var(--cdi-fs-xs); color: var(--cdi-grey); }
.cd-itest-sidebar-trust li { display: flex; gap: var(--cdi-sp-1); align-items: flex-start; }
.cd-itest-sidebar-trust li svg { flex-shrink: 0; margin-top: 3px; color: var(--cdi-orange); }
.cd-itest-sidebar-trust li a { color: var(--cdi-navy); font-weight: 700; }

@media (max-width: 640px) {
    .cd-itest-panel { padding: var(--cdi-sp-3) var(--cdi-sp-2); min-height: 0; }
    body.page-template-insolvency-test .cd-itest-h1 { font-size: 27px; }
    body.page-template-insolvency-test .cd-itest-q  { font-size: 21px; }
    body.page-template-insolvency-test .cd-itest-result-title { font-size: 21px; }
    .cd-itest-btn-primary--intro { width: 100%; }
}
</style>

<script id="cd-itest-js">
/*
 * Insolvency Test — client-side flow. Vanilla JS, no dependency on jQuery
 * or on Gravity Forms client scripts (both of which held up the old form-38
 * submit chain). The capture step POSTs to Gravity Forms via the REST
 * submissions endpoint (/wp-json/gf/v2/forms/{id}/submissions), which runs
 * full validation and notifications server-side — no DOM click intercept
 * to fight with.
 *
 * dataLayer events power funnel tracking through GTM-5GTD9ZP.
 */
(function () {
    var root = document.querySelector('.cd-itest-main');
    if (!root) return;
    var FORM_ID = parseInt(root.getAttribute('data-cd-form-id'), 10);
    if (!FORM_ID) return;

    var answers = { cashflow: null, warning: [], position: null, debtRange: null, risk: [] };
    var stepHistory = ['intro'];
    var STAGES = { intro:0, cashflow:0.2, warning:0.4, position:0.55, debtrange:0.68, risk:0.85, capture:0.95, result:1 };
    var LABELS = { cashflow:'Step 1 of 4', warning:'Step 2 of 4', position:'Step 3 of 4', debtrange:'Step 3 of 4', risk:'Step 4 of 4', capture:'Your result is ready', result:'' };
    var startedAt = 0;
    var reachedCapture = false;
    var submitted = false;

    window.dataLayer = window.dataLayer || [];
    function ga(event, params) {
        window.dataLayer.push(Object.assign({ event: event, tool: 'insolvency_test' }, params || {}));
    }

    function goTo(id) {
        var steps = document.querySelectorAll('.cd-itest-step');
        for (var i = 0; i < steps.length; i++) steps[i].classList.remove('cd-itest-step--active');
        var next = document.getElementById('cd-itest-step-' + id);
        if (!next) return;
        next.classList.add('cd-itest-step--active');
        if (stepHistory[stepHistory.length - 1] !== id) stepHistory.push(id);
        var pw = document.getElementById('cd-itest-progressWrap');
        var back = document.getElementById('cd-itest-backBtn');
        if (id === 'intro' || id === 'result') {
            pw.style.display = 'none';
            back.classList.remove('cd-itest-show');
        } else {
            pw.style.display = 'block';
            document.getElementById('cd-itest-progressFill').style.width = (STAGES[id] * 100) + '%';
            document.getElementById('cd-itest-progressLabel').textContent = LABELS[id] || '';
            back.classList.add('cd-itest-show');
        }
        try { window.scrollTo({ top: 0, behavior: 'instant' }); } catch (e) { window.scrollTo(0, 0); }
        if (id === 'capture') reachedCapture = true;
    }
    function goBack() {
        if (stepHistory.length < 2) return;
        stepHistory.pop();
        var prev = stepHistory[stepHistory.length - 1];
        stepHistory.pop();
        goTo(prev);
    }

    function noneToggle(name, noneId) {
        var none = document.getElementById(noneId);
        var group = document.querySelectorAll('input[name="' + name + '"]');
        for (var i = 0; i < group.length; i++) {
            (function (i) {
                group[i].addEventListener('change', function () {
                    if (group[i].id === noneId) {
                        if (group[i].checked) {
                            for (var j = 0; j < group.length; j++) {
                                if (group[j].id !== noneId) group[j].checked = false;
                            }
                        }
                    } else if (group[i].checked) {
                        none.checked = false;
                    }
                });
            })(i);
        }
    }
    noneToggle('cd_warning', 'cd-w-none');
    noneToggle('cd_risk', 'cd-r-none');

    // --- Auto-advance single-choice screens ---
    var cf = document.querySelectorAll('input[name="cd_cashflow"]');
    for (var i = 0; i < cf.length; i++) {
        cf[i].addEventListener('change', function (e) {
            answers.cashflow = e.target.value;
            ga('insolvency_test_step_complete', { step: 'cashflow', answer: e.target.value });
            setTimeout(function () { goTo('warning'); }, 350);
        });
    }
    var pos = document.querySelectorAll('input[name="cd_position"]');
    for (var i = 0; i < pos.length; i++) {
        pos[i].addEventListener('change', function (e) {
            answers.position = e.target.value;
            ga('insolvency_test_step_complete', { step: 'position', answer: e.target.value });
            setTimeout(function () {
                if (e.target.value === 'debts_more' || answers.cashflow === 'late' || answers.cashflow === 'cannot') goTo('debtrange');
                else goTo('risk');
            }, 350);
        });
    }
    var dr = document.querySelectorAll('input[name="cd_debtrange"]');
    for (var i = 0; i < dr.length; i++) {
        dr[i].addEventListener('change', function (e) {
            answers.debtRange = e.target.value;
            ga('insolvency_test_step_complete', { step: 'debtrange', answer: e.target.value });
            setTimeout(function () { goTo('risk'); }, 350);
        });
    }

    // --- Delegated click handling for goto + submit + back ---
    root.addEventListener('click', function (e) {
        var t = e.target.closest('[data-cd-goto]');
        if (t) {
            var id = t.getAttribute('data-cd-goto');
            if (id === 'cashflow' && !startedAt) {
                startedAt = Date.now();
                ga('insolvency_test_start', {});
            }
            goTo(id);
            return;
        }
        var s = e.target.closest('[data-cd-submit]');
        if (s) {
            var which = s.getAttribute('data-cd-submit');
            if (which === 'warning') {
                answers.warning = [].map.call(document.querySelectorAll('input[name="cd_warning"]:checked'), function (x) { return x.value; }).filter(function (v) { return v !== 'none'; });
                ga('insolvency_test_step_complete', { step: 'warning', answer: answers.warning.join(',') || 'none' });
                goTo('position');
            } else if (which === 'risk') {
                answers.risk = [].map.call(document.querySelectorAll('input[name="cd_risk"]:checked'), function (x) { return x.value; }).filter(function (v) { return v !== 'none'; });
                ga('insolvency_test_step_complete', { step: 'risk', answer: answers.risk.join(',') || 'none' });
                goTo('capture');
            }
        }
    });
    document.getElementById('cd-itest-backBtn').addEventListener('click', goBack);

    // --- Callback fields toggle ---
    var cpAll = document.querySelectorAll('input[name="cd_callpref"]');
    for (var i = 0; i < cpAll.length; i++) {
        cpAll[i].addEventListener('change', function () {
            var yes = document.getElementById('cd-cp-yes').checked;
            document.getElementById('cd-itest-callbackFields').classList.toggle('cd-itest-show', yes);
        });
    }

    // --- Scoring / result render ---
    function computeResult() {
        var score = 0, reasons = [], forceUrgent = false;
        var cf = answers.cashflow;
        if (cf === 'difficulty') { score += 2; reasons.push('the company can only pay its bills with difficulty'); }
        else if (cf === 'late')    { score += 4; reasons.push('some payments to creditors are already late'); }
        else if (cf === 'cannot')  { score += 6; forceUrgent = true; reasons.push('the company cannot currently pay everyone it owes'); }
        else if (cf === 'unsure')  { score += 2; reasons.push('there is uncertainty about whether the company can meet its current commitments'); }
        var wmap = {
            hmrc_overdue: [3, 'HMRC payments are overdue'],
            payroll_risk: [3, 'payroll may not be met'],
            supplier_pressure: [2, 'suppliers are chasing payment or reducing credit'],
            bank_limit: [2, 'the bank account or overdraft is at its limit'],
            personal_funds_reliance: [2, 'the company is relying on personal funds to keep going']
        };
        for (var i = 0; i < answers.warning.length; i++) {
            var m = wmap[answers.warning[i]];
            if (m) { score += m[0]; reasons.push(m[1]); }
        }
        if (answers.position === 'debts_more') { score += 3; reasons.push('the company probably owes more than its cash and assets are worth'); }
        else if (answers.position === 'unsure') { score += 1; reasons.push('it is unclear whether the company’s assets cover what it owes'); }
        var drmap = { '25-50k':1, '50-100k':1, '100-250k':2, 'over250k':3 };
        if (drmap[answers.debtRange]) score += drmap[answers.debtRange];
        if (answers.risk.indexOf('statutory') > -1) { score += 6; forceUrgent = true; reasons.push('a statutory demand, winding-up petition or enforcement notice has been received'); }
        if (answers.risk.indexOf('stopped_trading') > -1) { score += 4; reasons.push('the company has stopped trading'); }
        if (answers.risk.indexOf('preferential') > -1) { score += 2; reasons.push('you are having to decide which creditors to pay ahead of others'); }

        var level, badgeClass, urgency, opts;
        if (forceUrgent || score >= 14) {
            level = 'Urgent Professional Review Recommended';
            badgeClass = 'cd-itest-badge-urgent';
            urgency = 'Recommended action: seek urgent advice today';
            opts = ["Creditors' Voluntary Liquidation", "Administration", "Immediate advice from a licensed insolvency practitioner"];
        } else if (score >= 8) {
            level = 'Significant Insolvency Risk';
            badgeClass = 'cd-itest-badge-sig';
            urgency = 'Recommended action: speak to an adviser within 48 hours';
            opts = ['Company Voluntary Arrangement', "Creditors' Voluntary Liquidation", 'Formal negotiation with creditors'];
        } else if (score >= 4) {
            level = 'Some Warning Signs';
            badgeClass = 'cd-itest-badge-some';
            urgency = 'Recommended action: review within the next seven days';
            opts = ['Time to Pay arrangement with HMRC', 'Informal negotiation with creditors', 'Solvent closure or strike-off where appropriate'];
        } else {
            level = 'No Immediate Warning Identified';
            badgeClass = 'cd-itest-badge-none';
            urgency = 'Recommended action: keep monitoring cash flow and creditor payments';
            opts = ['Continue monitoring cash flow', 'Keep creditor payments up to date'];
        }
        if (reasons.length === 0) reasons.push('no significant warning signs were identified across your answers');

        var badge = document.getElementById('cd-itest-resultBadge');
        badge.className = 'cd-itest-result-badge ' + badgeClass;
        badge.textContent = level;
        document.getElementById('cd-itest-resultTitle').textContent = level;
        document.getElementById('cd-itest-resultUrgency').textContent = urgency;
        document.getElementById('cd-itest-resultReasons').innerHTML = reasons.slice(0, 5).map(function (r) {
            return '<li>' + r.charAt(0).toUpperCase() + r.slice(1) + '</li>';
        }).join('');
        document.getElementById('cd-itest-resultOptions').innerHTML = opts.map(function (o) { return '<li>' + o + '</li>'; }).join('');
        document.getElementById('cd-itest-pgNote').style.display = answers.risk.indexOf('personal_guarantee') > -1 ? 'block' : 'none';

        return { level: level, score: score, forceUrgent: forceUrgent };
    }

    // --- Capture submit (GF REST) ---
    var captureBtn = document.getElementById('cd-itest-capture-submit');
    var emailRe = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
    captureBtn.addEventListener('click', function () {
        if (submitted) return;
        var name = document.getElementById('cd-c-name').value.trim();
        var email = document.getElementById('cd-c-email').value.trim();
        var callpref = document.querySelector('input[name="cd_callpref"]:checked');
        var errValidation = document.getElementById('cd-itest-err-capture');
        var errNetwork = document.getElementById('cd-itest-err-network');
        errNetwork.style.display = 'none';
        if (!name || !emailRe.test(email) || !callpref) {
            errValidation.classList.add('cd-itest-show');
            return;
        }
        errValidation.classList.remove('cd-itest-show');
        var phone = document.getElementById('cd-c-phone').value.trim();
        var calltime = (document.querySelector('input[name="cd_calltime"]:checked') || {}).value || '';

        var result = computeResult();

        // Gravity Forms /wp-json/gf/v2/forms/{id}/submissions accepts flat form-data
        // with input_N keys — NOT the {input_values: {...}} JSON shape the docs suggest
        // (that shape 400s with "This field is required" on every field). Verified 2026-08-05.
        var fd = new FormData();
        fd.append('input_1', name);
        fd.append('input_2', email);
        fd.append('input_3', callpref.value);           // yes/no
        fd.append('input_4', phone);
        fd.append('input_5', calltime);
        fd.append('input_6', result.level);             // tier
        fd.append('input_7', JSON.stringify({
            answers: answers,
            score: result.score,
            forceUrgent: result.forceUrgent,
            duration_ms: startedAt ? (Date.now() - startedAt) : 0
        }));
        fd.append('input_8', location.href);
        fd.append('input_9', document.referrer || '');

        captureBtn.disabled = true;
        captureBtn.textContent = 'Sending…';

        var url = '/wp-json/gf/v2/forms/' + FORM_ID + '/submissions';
        fetch(url, {
            method: 'POST',
            credentials: 'same-origin',
            body: fd
        }).then(function (r) {
            return r.json().then(function (d) { return { ok: r.ok, status: r.status, data: d }; });
        }).then(function (res) {
            if (!res.ok || !res.data || (res.data.is_valid === false)) {
                captureBtn.disabled = false;
                captureBtn.textContent = 'See My Result';
                errNetwork.style.display = 'block';
                ga('insolvency_test_capture_failed', { status: res.status, reason: (res.data && res.data.validation_messages) ? 'validation' : 'network' });
                return;
            }
            submitted = true;
            var banner = document.getElementById('cd-itest-resultConfirmBanner');
            if (callpref.value === 'yes') {
                banner.innerHTML = '<span>Sent to ' + escapeHtml(email) + '. An adviser will call you' + (calltime ? ' ' + calltime.toLowerCase() : '') + ' to talk through your result.</span>';
            } else {
                banner.innerHTML = '<span>Sent to ' + escapeHtml(email) + '. Email only &mdash; no call will be made unless you request one.</span>';
            }
            banner.style.display = 'flex';
            goTo('result');
            ga('insolvency_test_result', { tier: result.level, score: result.score });
            ga('insolvency_test_callback_requested', { callback: callpref.value === 'yes' ? 'yes' : 'no' });
        }).catch(function () {
            captureBtn.disabled = false;
            captureBtn.textContent = 'See My Result';
            errNetwork.style.display = 'block';
            ga('insolvency_test_capture_failed', { reason: 'network' });
        });
    });

    function escapeHtml(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' }[c]; }); }

    // --- Abandonment tracking: fire once if the visitor started but never reached capture submit ---
    var abandonSent = false;
    window.addEventListener('pagehide', function () {
        if (abandonSent || !startedAt || submitted) return;
        var lastStep = stepHistory[stepHistory.length - 1] || 'intro';
        try {
            var data = { event: 'insolvency_test_abandonment', tool: 'insolvency_test', last_step: lastStep, reached_capture: reachedCapture };
            // dataLayer push may not survive unload; also fire a beacon
            window.dataLayer.push(data);
            if (navigator.sendBeacon) navigator.sendBeacon('/wp-json/cd-itest/v1/abandon', new Blob([JSON.stringify(data)], { type: 'application/json' }));
        } catch (e) {}
        abandonSent = true;
    });
})();
</script>

</main>
<?php get_footer();
