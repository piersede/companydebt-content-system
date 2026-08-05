<?php
/* Template Name: Quiz Insolvency */

get_header();
?>
<main id="primary" class="site-main cd-calc-main">
    <div class="content">
        <div class="container">

            <?php // ── HERO ─────────────────────────────────────────────── ?>
            <div class="cd-calc-hero">
                <span class="cd-calc-hero__pill">Free &middot; Confidential &middot; No obligation</span>
                <h1 class="post-title cd-calc-hero__title">30-Second Company Insolvency Test</h1>
                <p class="cd-calc-hero__subhead">Enter a few estimated figures to get an initial indication of your limited company&rsquo;s financial position. This is not a formal insolvency assessment.</p>
                <div class="cd-calc-hero__reviews">
                    <span class="cd-calc-hero__stars" aria-hidden="true">
                        <svg viewBox="0 0 20 20" width="18" height="18"><path d="M10 1.5l2.6 5.3 5.9.9-4.3 4.1 1 5.8L10 15l-5.2 2.6 1-5.8L1.5 7.7l5.9-.9z"/></svg>
                        <svg viewBox="0 0 20 20" width="18" height="18"><path d="M10 1.5l2.6 5.3 5.9.9-4.3 4.1 1 5.8L10 15l-5.2 2.6 1-5.8L1.5 7.7l5.9-.9z"/></svg>
                        <svg viewBox="0 0 20 20" width="18" height="18"><path d="M10 1.5l2.6 5.3 5.9.9-4.3 4.1 1 5.8L10 15l-5.2 2.6 1-5.8L1.5 7.7l5.9-.9z"/></svg>
                        <svg viewBox="0 0 20 20" width="18" height="18"><path d="M10 1.5l2.6 5.3 5.9.9-4.3 4.1 1 5.8L10 15l-5.2 2.6 1-5.8L1.5 7.7l5.9-.9z"/></svg>
                        <svg viewBox="0 0 20 20" width="18" height="18"><path d="M10 1.5l2.6 5.3 5.9.9-4.3 4.1 1 5.8L10 15l-5.2 2.6 1-5.8L1.5 7.7l5.9-.9z"/></svg>
                    </span>
                    <span class="cd-calc-hero__reviews-text"><strong>Excellent</strong> &middot; rated 5.0 by clients on Reviews.io</span>
                </div>
            </div>

            <?php // ── MEGABOX ──────────────────────────────────────────── ?>
            <div class="cd-calc-megabox quiz-content">
                <div class="quiz-tab-container">
                    <div class="quiz-tab-content">

                        <div class="cd-calc-grid">

                            <?php // ── LEFT: questions ──────────────────── ?>
                            <div class="quiz-tab-pane quiz-tab-1 active cd-calc-questions" id="quiz-tab-1" role="tabpanel">

                                <?php // Q1 — how much owed ?>
                                <section class="cd-calc-q">
                                    <div class="cd-calc-q__head">
                                        <span class="cd-calc-qnum">1</span>
                                        <h2 class="cd-calc-q__title">How Much Does Your Company Currently Owe?</h2>
                                    </div>
                                    <p class="cd-calc-help">Use approximate outstanding balances. Enter &pound;0 where the company owes nothing in a category.</p>
                                    <div class="cd-calc-q__body">
                                        <div class="cd-calc-srow">
                                            <div class="cd-calc-srow__head">
                                                <label for="quiz-amount-bank">Bank loans, overdrafts and other finance</label>
                                                <span class="cd-calc-money">
                                                    <span class="cd-calc-money__sign" aria-hidden="true">&pound;</span>
                                                    <input type="text" class="quiz-amount quiz-amount-bank cd-calc-money__input" id="quiz-amount-bank" inputmode="numeric" autocomplete="off" value="0">
                                                </span>
                                            </div>
                                            <div id="slider-range-bank" class="slider-range-noUI cd-calc-slider"></div>
                                        </div>
                                        <div class="cd-calc-srow">
                                            <div class="cd-calc-srow__head">
                                                <label for="quiz-amount-hmrc">HMRC: VAT, PAYE and Corporation Tax</label>
                                                <span class="cd-calc-money">
                                                    <span class="cd-calc-money__sign" aria-hidden="true">&pound;</span>
                                                    <input type="text" class="quiz-amount quiz-amount-hmrc cd-calc-money__input" id="quiz-amount-hmrc" inputmode="numeric" autocomplete="off" value="0">
                                                </span>
                                            </div>
                                            <div id="slider-range-hmrc" class="slider-range-noUI cd-calc-slider"></div>
                                        </div>
                                        <div class="cd-calc-srow">
                                            <div class="cd-calc-srow__head">
                                                <label for="quiz-amount-creditors">Suppliers and other trade creditors</label>
                                                <span class="cd-calc-money">
                                                    <span class="cd-calc-money__sign" aria-hidden="true">&pound;</span>
                                                    <input type="text" class="quiz-amount quiz-amount-creditors cd-calc-money__input" id="quiz-amount-creditors" inputmode="numeric" autocomplete="off" value="0">
                                                </span>
                                            </div>
                                            <div id="slider-range-creditors" class="slider-range-noUI cd-calc-slider"></div>
                                        </div>
                                        <div class="cd-calc-total">
                                            <span class="cd-calc-total__label">Estimated total liabilities</span>
                                            <span class="cd-calc-total__val" id="cd-total-owed">&pound;0</span>
                                        </div>
                                    </div>
                                </section>

                                <?php // Q2 — assets ?>
                                <section class="cd-calc-q">
                                    <div class="cd-calc-q__head">
                                        <span class="cd-calc-qnum">2</span>
                                        <h2 class="cd-calc-q__title">What Could Your Company&rsquo;s Assets Realistically Be Worth?</h2>
                                    </div>
                                    <div class="cd-calc-q__body">
                                        <div class="cd-calc-srow">
                                            <div class="cd-calc-srow__head">
                                                <label for="quiz-amount-assets">Estimated realisable value of cash, unpaid invoices, stock, equipment and property</label>
                                                <span class="cd-calc-money">
                                                    <span class="cd-calc-money__sign" aria-hidden="true">&pound;</span>
                                                    <input type="text" class="quiz-amount quiz-amount-assets cd-calc-money__input" id="quiz-amount-assets" inputmode="numeric" autocomplete="off" value="0">
                                                </span>
                                            </div>
                                            <div id="slider-range-assets" class="slider-range-noUI cd-calc-slider"></div>
                                        </div>
                                        <p class="cd-calc-help">Use the amount the company could realistically sell or collect, rather than the original purchase price or accounting value.</p>
                                    </div>
                                </section>

                                <?php // Q3 — personal guarantee (JS-bound radios preserved) ?>
                                <section class="cd-calc-q">
                                    <div class="cd-calc-q__head">
                                        <span class="cd-calc-qnum">3</span>
                                        <h2 class="cd-calc-q__title">Have You Signed a Personal Guarantee for Any Company Borrowing?</h2>
                                    </div>
                                    <p class="cd-calc-help cd-calc-help--center">This does not determine whether the company is insolvent, but it may affect your personal liability.</p>
                                    <div class="cd-calc-q__body cd-calc-q__body--center">
                                        <div class="quiz-yes-no">
                                            <div class="quiz-radio-container">
                                                <input type="radio" id="quiz-yes" class="quiz-radio" name="guarantee" value="yes">
                                                <label for="quiz-yes">Yes</label>
                                            </div>
                                            <div class="quiz-radio-container">
                                                <input type="radio" id="quiz-no" class="quiz-radio" name="guarantee" value="no">
                                                <label for="quiz-no">No</label>
                                            </div>
                                        </div>
                                    </div>
                                </section>

                            </div>

                            <?php // ── RIGHT: results + form ────────────── ?>
                            <div class="quiz-tab-pane quiz-tab-2 cd-calc-side" id="quiz-tab-2" role="tabpanel">

                                <?php // Estimated position (navy) ?>
                                <section class="cd-calc-position">
                                    <h2 class="cd-calc-position__title">Simple Balance-Sheet Estimate</h2>
                                    <div class="cd-calc-position__rows">
                                        <div class="cd-calc-position__row">
                                            <span>Estimated liabilities</span>
                                            <span class="cd-calc-position__num" id="cd-pos-debts">&pound;0</span>
                                        </div>
                                        <div class="cd-calc-position__row">
                                            <span>Estimated realisable assets</span>
                                            <span class="cd-calc-position__num" id="cd-pos-assets">&pound;0</span>
                                        </div>
                                    </div>
                                    <div class="cd-calc-position__figure">
                                        <div class="cd-calc-position__amount" id="cd-pos-shortfall">&pound;0</div>
                                        <div class="cd-calc-position__caption" id="cd-pos-caption">Estimated balance-sheet shortfall</div>
                                    </div>
                                    <p class="cd-calc-position__note">This is a simple comparison of the figures entered. It does not assess whether the company can pay its debts as they fall due and is not a formal insolvency determination.</p>
                                </section>

                                <?php // Instant results + form (navy) ?>
                                <section class="cd-calc-form">
                                    <div class="form-container">
                                        <div class="form-group">
                                            <h2 class="cd-calc-form__title">Get Your Initial Assessment</h2>
                                            <p class="cd-calc-form__lead">Enter your details to see your initial result. You can also request a free, confidential call to discuss your company&rsquo;s position.</p>
                                            <?php echo do_shortcode( '[gravityform name="Insolvency Calculator" title="false" ajax="true"]' ); ?>
                                            <div class="cd-get-results-container">
                                                <?php // The native GF submit (#gform_submit_button_38) is hidden by
                                                      // style.css; a plain HTML5 `form="gform_38"` submit skipped GF's
                                                      // own onclick + AJAX hook so the form never posted. Click the
                                                      // hidden native button instead — that runs GF's onclick (sets
                                                      // gf_submitting_38 + triggers the form's submit handler chain). ?>
                                                <button type="button" class="cd-get-results-btn" onclick="var b=document.getElementById('gform_submit_button_38'); if(b){b.click();} return false;">Show My Initial Result</button>
                                            </div>
                                            <p class="cd-calc-form__micro">Free &middot; Confidential &middot; No obligation</p>
                                            <p class="cd-calc-form__privacy">We will use these details to provide your assessment and contact you about your company&rsquo;s position. Read our <a href="/privacy-policy/">Privacy Policy</a>.</p>
                                        </div>
                                    </div>
                                </section>

                            </div>

                        </div>

                        <?php // ── Full-width guide band — hidden to match approved design 2026-07-22; flip to true to restore ?>
                        <?php if ( false ) : ?>
                        <div class="cd-guide-band">
                            <div class="form-sidebar">
                                <div class="form-sidebar-text">
                                    <h4>Download Our Stressed Director's Guide</h4>
                                    <ul class="form-sidebar-checklist">
                                        <li class="form-sidebar-item">What are the Implications of Insolvency for Directors?</li>
                                        <li class="form-sidebar-item">Your Company's Health Risk</li>
                                        <li class="form-sidebar-item">What Strategies are Available?</li>
                                        <li class="form-sidebar-item">What's the Liquidation Process?</li>
                                        <li class="form-sidebar-item">Role of the Insolvency Practitioner</li>
                                        <li class="form-sidebar-item">Dealing with HMRC Pressure</li>
                                    </ul>
                                    <a href="#" class="form-sidebar-cta" target="_blank" rel="noopener">Download the Guide</a>
                                </div>
                                <div class="form-sidebar-image">
                                    <img width="150" height="183" src="<?php echo CD_THEME_URL . 'assets/images/guide-220.png'; ?>" alt="Stressed Directors Guide">
                                </div>
                            </div>
                        </div>
                        <?php endif; ?>

                    </div>
                </div>
            </div>

            <?php // ── Results view (shown after submit, replaces hero + calculator) ── ?>
            <div class="cd-results" id="cd-results" style="display:none;" aria-live="polite">
                <h2 class="cd-results__heading">Based on the figures entered, this initial check indicates:</h2>
                <div class="cd-results__stamp is-insolvent" id="cd-results-stamp">
                    <span class="cd-results__verdict" id="cd-verdict">POSSIBLE INSOLVENCY RISK</span>
                </div>
                <div class="cd-results__body" id="cd-results-body"></div>
                <div class="cd-results__trust">
                    <svg class="cd-results__lock" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                    <span>Free, confidential and without obligation</span>
                </div>
                <div class="cd-results__cta">
                    <a href="/contact-us/" class="cd-results__btn">Speak to an Insolvency Adviser</a>
                </div>
            </div>

        </div>
    </div>

<?php // ── Calculator wiring: display + two-way binding + live results ──────
   // The external quiz-insolvency.js creates the noUiSliders and keeps the
   // hidden Gravity Form fields (.gf_amount-* / .gf_result) populated. This
   // script owns DISPLAY ONLY: slider<->field sync, thousands formatting, the
   // "Total owed" row, and the live "Your Estimated Position" panel. It never
   // submits or alters the form; typed values are written straight to the same
   // hidden GF fields so what the director sees is what is submitted. ?>
<script>
(function(){
  var FIELDS = [
    { slider:"slider-range-bank",      input:"quiz-amount-bank",      hidden:".gf_amount-bank input" },
    { slider:"slider-range-hmrc",      input:"quiz-amount-hmrc",      hidden:".gf_amount-hmrc input" },
    { slider:"slider-range-creditors", input:"quiz-amount-creditors", hidden:".gf_amount-creditors input" },
    { slider:"slider-range-assets",    input:"quiz-amount-assets",    hidden:".gf_amount-assets input" }
  ];
  var MAX = 350000; // matches the noUiSlider range in quiz-insolvency.js — keep the two in sync
  var nf = new Intl.NumberFormat("en-GB");
  var gbp = function(v){ return "£" + nf.format(Math.round(v)); };
  var num = function(raw){ var n = Math.round(parseFloat(String(raw).replace(/[^\d.]/g, ""))); return isNaN(n) ? 0 : n; };

  function readHidden(sel){ var el = document.querySelector(sel); return el ? num(el.value) : 0; }

  function updateResults(){
    var bank = readHidden(FIELDS[0].hidden),
        hmrc = readHidden(FIELDS[1].hidden),
        cred = readHidden(FIELDS[2].hidden),
        assets = readHidden(FIELDS[3].hidden);
    var debts = bank + hmrc + cred;
    var net = debts - assets;
    var set = function(id, txt){ var e = document.getElementById(id); if (e) e.textContent = txt; };
    set("cd-total-owed", gbp(debts));
    set("cd-pos-debts", gbp(debts));
    set("cd-pos-assets", gbp(assets));
    set("cd-pos-shortfall", gbp(Math.abs(net)));
    set("cd-pos-caption", net >= 0 ? "Estimated balance-sheet shortfall" : "Estimated balance-sheet surplus");
    var panel = document.querySelector(".cd-calc-position");
    if (panel) panel.classList.toggle("is-surplus", net < 0);
    // keep the submitted Result field correct even for typed-only input
    var verdict = (debts > assets) ? "Insolvent" : "Solvent";
    var result = document.querySelector(".gf_result input");
    if (result) result.value = verdict;
    // remember the verdict so the results view can show it after the form is replaced
    window.__cdVerdict = verdict.toUpperCase();
  }

  // Run even if the DOM is already parsed (WP Rocket delay-JS can inject this
  // inline script after DOMContentLoaded has fired — a plain listener would never run).
  (function(cb){ if (document.readyState !== "loading") { cb(); } else { document.addEventListener("DOMContentLoaded", cb); } })(function(){
    setTimeout(function(){
      FIELDS.forEach(function(f){
        var slider = document.getElementById(f.slider);
        var input  = document.getElementById(f.input);
        if (!input) return;
        var typing = false;

        // slider drag -> visible field + results (external JS already wrote the hidden field)
        if (slider && slider.noUiSlider) {
          slider.noUiSlider.on("update", function(values){
            if (typing) return;
            input.value = nf.format(Math.round(values[0]));
            updateResults();
          });
        }

        // typing -> slider position + hidden field (typed value is authoritative) + results
        input.addEventListener("input", function(){
          typing = true;
          var val = num(this.value);
          if (val > MAX) val = MAX;
          if (slider && slider.noUiSlider) slider.noUiSlider.set(val);
          var hidden = document.querySelector(f.hidden);
          if (hidden) hidden.value = val;
          updateResults();
          typing = false;
        });

        input.addEventListener("focus", function(){ this.select(); });
        input.addEventListener("blur", function(){ this.value = nf.format(num(this.value)); });
      });

      // Seed opening figures so the tool is alive on arrival (matches approved design).
      var SEED = [60000, 35000, 45000, 40000];
      FIELDS.forEach(function(f, i){
        var slider = document.getElementById(f.slider);
        if (slider && slider.noUiSlider) { slider.noUiSlider.set(SEED[i]); }
        else { var input = document.getElementById(f.input); if (input) { input.value = nf.format(SEED[i]); var h = document.querySelector(f.hidden); if (h) h.value = SEED[i]; } }
      });

      // Placeholder copy in the contact fields (matches approved design).
      var PH = { "input_38_1": "Jane Smith", "input_38_3": "Acme Trading Ltd", "input_38_2": "jane@company.co.uk", "input_38_4": "07700 900000" };
      Object.keys(PH).forEach(function(id){ var e = document.getElementById(id); if (e) { e.setAttribute("placeholder", PH[id]); } });

      // Cosmetic label copy (visual only — Gravity Forms field config + notifications unchanged).
      var LBL = { "field_38_1": "Full name", "field_38_3": "Company name", "field_38_2": "Email address", "field_38_4": "Phone number", "field_38_5": "Preferred callback day" };
      Object.keys(LBL).forEach(function(id){ var l = document.querySelector("#" + id + " .gfield_label"); if (l) { l.textContent = LBL[id]; } });
      // Required-field legend copy (visual only).
      var reqLegend = document.querySelector("#gform_38 .gform_required_legend");
      if (reqLegend) { reqLegend.textContent = "Required field"; }

      updateResults();
    }, 300);
  });

  // GF AJAX confirmation fires after a successful submit — swap the calculator
  // for the full-width results view, carrying the computed verdict across.
  var VERDICT_LABEL = {
    INSOLVENT: "POSSIBLE INSOLVENCY RISK",
    SOLVENT: "NO BALANCE-SHEET SHORTFALL INDICATED"
  };
  var RESULTS_COPY = {
    INSOLVENT: [
      "The company’s estimated liabilities are greater than the estimated realisable value of its assets. This may indicate balance-sheet insolvency, but it is not a formal determination and does not assess whether the company can pay its debts as they fall due.",
      "If you requested a callback, one of our advisers will contact you to discuss the figures in more detail. Please also check your email for the Stressed Director’s Guide."
    ],
    SOLVENT: [
      "The figures entered do not show a balance-sheet shortfall. However, a company can still be insolvent if it cannot pay its debts as they fall due. This result is an initial indication, not a formal assessment.",
      "If you requested a callback, one of our advisers will contact you to discuss the figures in more detail. Please also check your email for the Stressed Director’s Guide."
    ]
  };
  function showResults(){
    var verdict = window.__cdVerdict || "INSOLVENT";
    var vEl = document.getElementById("cd-verdict");
    if (vEl) vEl.textContent = VERDICT_LABEL[verdict] || VERDICT_LABEL.INSOLVENT;
    var body = document.getElementById("cd-results-body");
    if (body) {
      var paras = RESULTS_COPY[verdict] || RESULTS_COPY.INSOLVENT;
      body.innerHTML = paras.map(function(t){ return "<p>" + t + "</p>"; }).join("");
    }
    var stamp = document.getElementById("cd-results-stamp");
    if (stamp) {
      stamp.classList.remove("is-insolvent", "is-solvent");
      stamp.classList.add(verdict === "SOLVENT" ? "is-solvent" : "is-insolvent");
    }
    var hero = document.querySelector(".cd-calc-hero");
    var mega = document.querySelector(".cd-calc-megabox");
    if (hero) hero.style.display = "none";
    if (mega) mega.style.display = "none";
    var results = document.getElementById("cd-results");
    if (results) { results.style.display = "block"; results.classList.add("is-visible"); }
    window.scrollTo(0, 0);
  }
  window.cdShowResults = showResults; // manual preview hook
  // Bind once jQuery is available. jQuery loads later (footer / WP Rocket delay-JS),
  // so a one-time `if (window.jQuery)` check ran too early and silently skipped this,
  // leaving "Show My Initial Result" with nothing to reveal the results. Poll instead.
  (function bindGf(){
    if (window.jQuery) { window.jQuery(document).on("gform_confirmation_loaded", showResults); }
    else { setTimeout(bindGf, 50); }
  })();
})();
</script>
</main>

<?php
get_footer(); ?>
