/*
 * Insolvency Test — client-side behaviour.
 * Loaded via wp_enqueue_script('cd-insolvency-test', …) only when
 * the template templates/insolvency-test.php is active.
 *
 * Design brief: tmp/new_calc_design/design_handoff_insolvency_test/
 *
 * No jQuery dependency. No Gravity Forms client script dependency.
 * The capture step submits to /wp-json/gf/v2/forms/{form_id}/submissions
 * with flat form-data (verified 2026-08-05: the {input_values: {...}}
 * JSON shape 400s on every field despite what the GF docs suggest).
 *
 * GA4 events fire via dataLayer through GTM-5GTD9ZP:
 *   insolvency_test_start
 *   insolvency_test_step_complete   (step, answer)
 *   insolvency_test_result           (tier, score)
 *   insolvency_test_callback_requested (callback = yes|no)
 *   insolvency_test_abandonment      (last_step, reached_capture)
 *   insolvency_test_capture_failed   (status, reason)
 */
(function () {
    var root = document.querySelector('.cd-itest-main');
    if (!root) return;
    var FORM_ID = parseInt(root.getAttribute('data-cd-form-id'), 10);
    if (!FORM_ID) return;

    // -----------------------------------------------------------------
    // State
    // -----------------------------------------------------------------
    var answers = { cashflow: null, warning: [], position: null, debtRange: null, risk: [] };
    var stepHistory = ['intro'];
    var startedAt = 0;
    var reachedCapture = false;
    var submitted = false;

    var STAGES = {
        intro: 0, cashflow: 0.20, warning: 0.40, position: 0.55,
        debtrange: 0.68, risk: 0.85, capture: 0.95, result: 1
    };
    var LABELS = {
        cashflow:  'Step 1 of 4',
        warning:   'Step 2 of 4',
        position:  'Step 3 of 4',
        debtrange: 'Step 3 of 4',
        risk:      'Step 4 of 4',
        capture:   'Your result is ready',
        result:    ''
    };

    // -----------------------------------------------------------------
    // Helpers
    // -----------------------------------------------------------------
    window.dataLayer = window.dataLayer || [];
    function ga(event, params) {
        window.dataLayer.push(Object.assign({ event: event, tool: 'insolvency_test' }, params || {}));
    }
    function escapeHtml(s) {
        return String(s).replace(/[&<>"']/g, function (c) {
            return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
        });
    }

    // -----------------------------------------------------------------
    // Navigation
    // -----------------------------------------------------------------
    function goTo(id) {
        var steps = document.querySelectorAll('.cd-itest-step');
        for (var i = 0; i < steps.length; i++) steps[i].classList.remove('cd-itest-step--active');
        var next = document.getElementById('cd-itest-step-' + id);
        if (!next) return;
        next.classList.add('cd-itest-step--active');
        if (stepHistory[stepHistory.length - 1] !== id) stepHistory.push(id);

        var panel = document.querySelector('.cd-itest-panel');
        var pw = document.getElementById('cd-itest-progressWrap');
        var back = document.getElementById('cd-itest-backBtn');

        // Progress bar + Back button visibility toggled via .cd-itest-show
        // class (not inline style) because the CSS uses `display: … !important`
        // on the base rule to beat the site's global !important rules, and
        // !important beats inline style.
        if (id === 'intro' || id === 'result') {
            pw.classList.remove('cd-itest-show');
            back.classList.remove('cd-itest-show');
        } else {
            pw.classList.add('cd-itest-show');
            document.getElementById('cd-itest-progressFill').style.width = (STAGES[id] * 100) + '%';
            document.getElementById('cd-itest-progressLabel').textContent = LABELS[id] || '';
            back.classList.add('cd-itest-show');
        }
        // Panel min-height belongs to intro only; other screens size to content.
        if (panel) panel.classList.toggle('cd-itest-panel--intro', id === 'intro');

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

    // -----------------------------------------------------------------
    // "None of these" mutual-exclusion for checkbox groups
    // -----------------------------------------------------------------
    function noneToggle(name, noneId) {
        var none = document.getElementById(noneId);
        if (!none) return;
        var group = document.querySelectorAll('input[name="' + name + '"]');
        for (var i = 0; i < group.length; i++) {
            (function (input) {
                input.addEventListener('change', function () {
                    if (input.id === noneId) {
                        if (input.checked) {
                            for (var j = 0; j < group.length; j++) {
                                if (group[j].id !== noneId) group[j].checked = false;
                            }
                        }
                    } else if (input.checked) {
                        none.checked = false;
                    }
                });
            })(group[i]);
        }
    }
    noneToggle('cd_warning', 'cd-w-none');
    noneToggle('cd_risk',    'cd-r-none');

    // -----------------------------------------------------------------
    // Auto-advance single-choice screens
    // -----------------------------------------------------------------
    (function bindCashflow() {
        var els = document.querySelectorAll('input[name="cd_cashflow"]');
        for (var i = 0; i < els.length; i++) {
            els[i].addEventListener('change', function (e) {
                answers.cashflow = e.target.value;
                ga('insolvency_test_step_complete', { step: 'cashflow', answer: e.target.value });
                setTimeout(function () { goTo('warning'); }, 350);
            });
        }
    })();
    (function bindPosition() {
        var els = document.querySelectorAll('input[name="cd_position"]');
        for (var i = 0; i < els.length; i++) {
            els[i].addEventListener('change', function (e) {
                answers.position = e.target.value;
                ga('insolvency_test_step_complete', { step: 'position', answer: e.target.value });
                setTimeout(function () {
                    // Conditional branch: only go to debtrange if the answers
                    // suggest debts might be significant.
                    if (e.target.value === 'debts_more' || answers.cashflow === 'late' || answers.cashflow === 'cannot') {
                        goTo('debtrange');
                    } else {
                        goTo('risk');
                    }
                }, 350);
            });
        }
    })();
    (function bindDebtRange() {
        var els = document.querySelectorAll('input[name="cd_debtrange"]');
        for (var i = 0; i < els.length; i++) {
            els[i].addEventListener('change', function (e) {
                answers.debtRange = e.target.value;
                ga('insolvency_test_step_complete', { step: 'debtrange', answer: e.target.value });
                setTimeout(function () { goTo('risk'); }, 350);
            });
        }
    })();

    // -----------------------------------------------------------------
    // Delegated click handling — [data-cd-goto] and [data-cd-submit]
    // -----------------------------------------------------------------
    root.addEventListener('click', function (e) {
        var g = e.target.closest('[data-cd-goto]');
        if (g) {
            var id = g.getAttribute('data-cd-goto');
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
                answers.warning = [].map.call(
                    document.querySelectorAll('input[name="cd_warning"]:checked'),
                    function (x) { return x.value; }
                ).filter(function (v) { return v !== 'none'; });
                ga('insolvency_test_step_complete', { step: 'warning', answer: answers.warning.join(',') || 'none' });
                goTo('position');
            } else if (which === 'risk') {
                answers.risk = [].map.call(
                    document.querySelectorAll('input[name="cd_risk"]:checked'),
                    function (x) { return x.value; }
                ).filter(function (v) { return v !== 'none'; });
                ga('insolvency_test_step_complete', { step: 'risk', answer: answers.risk.join(',') || 'none' });
                goTo('capture');
            }
        }
    });
    document.getElementById('cd-itest-backBtn').addEventListener('click', goBack);

    // Callback fields toggle (Yes reveals phone + preferred time)
    (function bindCallpref() {
        var els = document.querySelectorAll('input[name="cd_callpref"]');
        for (var i = 0; i < els.length; i++) {
            els[i].addEventListener('change', function () {
                var yes = document.getElementById('cd-cp-yes').checked;
                document.getElementById('cd-itest-callbackFields').classList.toggle('cd-itest-show', yes);
            });
        }
    })();

    // -----------------------------------------------------------------
    // Scoring + result render
    // -----------------------------------------------------------------
    function computeResult() {
        var cf = answers.cashflow;
        var hasStatutory         = answers.risk.indexOf('statutory') > -1;
        var hasStoppedTrading    = answers.risk.indexOf('stopped_trading') > -1;
        var hasPreferential      = answers.risk.indexOf('preferential') > -1;
        var hasPersonalGuarantee = answers.risk.indexOf('personal_guarantee') > -1;
        var hasPayrollRisk       = answers.warning.indexOf('payroll_risk') > -1;
        var cannotPay            = cf === 'cannot';
        var todayJustified       = hasStatutory || cannotPay || hasPayrollRisk;

        var score = 0, reasons = [], forceUrgent = false;
        if (cf === 'difficulty')      { score += 2; reasons.push('The company can only pay its bills with difficulty'); }
        else if (cf === 'late')       { score += 4; reasons.push('Some payments to creditors are already late'); }
        else if (cf === 'cannot')     { score += 6; forceUrgent = true; reasons.push('The company cannot currently pay all its bills'); }
        else if (cf === 'unsure')     { score += 2; reasons.push('There is uncertainty about whether the company can meet its current commitments'); }

        var wmap = {
            hmrc_overdue:            [3, 'HMRC payments are overdue'],
            payroll_risk:            [3, 'Payroll may not be met'],
            supplier_pressure:       [2, 'Suppliers are chasing payment or reducing credit'],
            bank_limit:              [2, 'The bank account or overdraft is at its limit'],
            personal_funds_reliance: [2, 'The company is relying on personal funds to keep going']
        };
        for (var i = 0; i < answers.warning.length; i++) {
            var m = wmap[answers.warning[i]];
            if (m) { score += m[0]; reasons.push(m[1]); }
        }

        // Position — visitor's estimate, phrased softly.
        if (answers.position === 'debts_more') { score += 3; reasons.push('The company may owe more than its cash and assets are worth'); }
        else if (answers.position === 'unsure') { score += 1; reasons.push('It is unclear whether the company’s assets cover what it owes'); }

        var drmap = { '25-50k': 1, '50-100k': 1, '100-250k': 2, 'over250k': 3 };
        if (drmap[answers.debtRange]) score += drmap[answers.debtRange];

        if (hasStatutory)      { score += 6; forceUrgent = true; reasons.push('A statutory demand, winding-up petition or enforcement notice has been received'); }
        if (hasStoppedTrading) { score += 4; reasons.push('The company has stopped trading'); }
        if (hasPreferential)   { score += 2; reasons.push('You are having to decide which creditors to pay ahead of others'); }

        // Tier
        var level, verdict, badgeClass, urgency;
        if (forceUrgent || score >= 14) {
            level = 'Urgent Review Recommended';
            verdict = 'Your answers indicate several serious insolvency warning signs.';
            badgeClass = 'cd-itest-badge-urgent';
            urgency = todayJustified
                ? 'Recommended next step: Speak to a licensed insolvency practitioner today.'
                : 'Recommended next step: Speak to a licensed insolvency practitioner within the next 48 hours.';
        } else if (score >= 8) {
            level = 'Significant Insolvency Risk';
            verdict = 'The signs in your answers point to significant insolvency risk.';
            badgeClass = 'cd-itest-badge-sig';
            urgency = 'Recommended next step: Speak to a licensed insolvency practitioner within the next 48 hours.';
        } else if (score >= 4) {
            level = 'Some Warning Signs';
            verdict = 'A few warning signs are worth reviewing.';
            badgeClass = 'cd-itest-badge-some';
            urgency = 'Recommended next step: Review the position within the next seven days.';
        } else {
            level = 'No Immediate Warning Signs';
            verdict = 'No immediate warning signs came up in your answers.';
            badgeClass = 'cd-itest-badge-none';
            urgency = 'Recommended next step: Keep monitoring cash flow and creditor payments.';
        }

        // "What to Do Now" — condition-aware
        var steps = [];
        if (forceUrgent || score >= 8) {
            steps.push('Arrange a confidential review today so that the company’s full position can be assessed.');
        } else if (score >= 4) {
            steps.push('Arrange a confidential review within the next few days so that the position can be assessed properly.');
        } else {
            steps.push('Keep monitoring cash flow and creditor payments and re-check the position if it changes.');
        }
        if (forceUrgent || score >= 8) {
            steps.push('Take care not to favour particular creditors, repay connected parties or transfer company assets outside normal business activity.');
        }
        if (hasPayrollRisk) {
            steps.push('Work out how employees will be paid this cycle and what cash is available to meet payroll.');
        }
        if (score >= 4) {
            steps.push('Gather any available bank balances, creditor totals, HMRC correspondence and personal guarantee documents.');
        }

        // Options list — CVL/Admin only surface when answers support them.
        var opts = [];
        var optsIntro = '';
        if (score < 4) {
            optsIntro = 'For a position with no immediate warning signs, the useful actions are usually:';
            opts.push('Continue monitoring cash flow');
            opts.push('Keep creditor payments up to date');
            opts.push('Re-run this check if the position changes');
        } else if (score < 8) {
            optsIntro = 'For the warning signs shown, a professional review might explore:';
            opts.push('A Time to Pay arrangement with HMRC');
            opts.push('Informal negotiation with creditors to buy time');
            if (answers.position === 'assets_more' || answers.position === 'about_same') {
                opts.push('Solvent closure or strike-off if the company is winding down and can meet its debts');
            }
        } else {
            optsIntro = 'Depending on the company’s full circumstances, possible routes may include:';
            opts.push('An agreement or repayment arrangement with creditors');
            if (!hasStoppedTrading) {
                opts.push('Restructuring or company rescue options');
                opts.push('Administration, where there is a viable business or assets to protect');
            }
            opts.push('Creditors’ Voluntary Liquidation if the company cannot continue');
        }

        // Render
        var badge = document.getElementById('cd-itest-resultBadge');
        badge.className = 'cd-itest-result-badge ' + badgeClass;
        badge.textContent = level;
        document.getElementById('cd-itest-resultTitle').textContent = verdict;
        document.getElementById('cd-itest-resultUrgency').textContent = urgency;

        var reasonsEl = document.getElementById('cd-itest-resultReasons');
        var reasonsSection = document.getElementById('cd-itest-resultReasonsSection');
        if (reasons.length === 0) {
            reasonsSection.style.display = 'none';
        } else {
            reasonsSection.style.display = 'block';
            reasonsEl.innerHTML = reasons.slice(0, 6).map(function (r) {
                return '<li>' + escapeHtml(r) + '</li>';
            }).join('');
        }

        document.getElementById('cd-itest-resultSteps').innerHTML = steps.map(function (s) {
            return '<li>' + escapeHtml(s) + '</li>';
        }).join('');
        document.getElementById('cd-itest-resultOptionsIntro').textContent = optsIntro;
        document.getElementById('cd-itest-resultOptions').innerHTML = opts.map(function (o) {
            return '<li>' + escapeHtml(o) + '</li>';
        }).join('');

        // Class toggle rather than inline style — see progress-wrap note above.
        document.getElementById('cd-itest-pgNote').classList.toggle('cd-itest-show', hasPersonalGuarantee);
        document.getElementById('cd-itest-creditorNote').classList.toggle('cd-itest-show', hasPreferential);

        return { level: level, score: score, forceUrgent: forceUrgent };
    }

    // -----------------------------------------------------------------
    // Capture submit → Gravity Forms REST → result screen
    // -----------------------------------------------------------------
    var captureBtn = document.getElementById('cd-itest-capture-submit');
    var emailRe = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

    captureBtn.addEventListener('click', function () {
        if (submitted) return;

        var name = document.getElementById('cd-c-name').value.trim();
        var email = document.getElementById('cd-c-email').value.trim();
        // callpref defaults to "no" (checked in HTML) so it's always present —
        // fall back to that if for any reason the DOM query misses.
        var callpref = document.querySelector('input[name="cd_callpref"]:checked') || { value: 'no' };
        var errValidation = document.getElementById('cd-itest-err-capture');
        var errNetwork = document.getElementById('cd-itest-err-network');
        errNetwork.style.display = 'none';

        if (!name || !emailRe.test(email)) {
            errValidation.classList.add('cd-itest-show');
            return;
        }
        errValidation.classList.remove('cd-itest-show');

        var phone    = document.getElementById('cd-c-phone').value.trim();
        var calltime = (document.querySelector('input[name="cd_calltime"]:checked') || {}).value || '';

        var result = computeResult();

        // GF REST /submissions expects flat form-data with input_N keys — not
        // the {input_values: {...}} JSON shape the docs suggest (verified
        // 2026-08-05: that shape 400s on every field).
        var fd = new FormData();
        fd.append('input_1', name);
        fd.append('input_2', email);
        fd.append('input_3', callpref.value);
        fd.append('input_4', phone);
        fd.append('input_5', calltime);
        fd.append('input_6', result.level);
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

        fetch('/wp-json/gf/v2/forms/' + FORM_ID + '/submissions', {
            method: 'POST',
            credentials: 'same-origin',
            body: fd
        }).then(function (r) {
            return r.json().then(function (d) { return { ok: r.ok, status: r.status, data: d }; });
        }).then(function (res) {
            if (!res.ok || !res.data || res.data.is_valid === false) {
                captureBtn.disabled = false;
                captureBtn.textContent = 'See My Result';
                errNetwork.style.display = 'block';
                ga('insolvency_test_capture_failed', {
                    status: res.status,
                    reason: (res.data && res.data.validation_messages) ? 'validation' : 'network'
                });
                return;
            }
            submitted = true;

            var banner = document.getElementById('cd-itest-resultConfirmBanner');
            var tick = '<svg class="cd-itest-confirm-quiet__tick" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>';
            if (callpref.value === 'yes') {
                banner.innerHTML = tick + '<span>Your result has been sent to ' + escapeHtml(email) +
                    '. An adviser will call you' + (calltime ? ' ' + calltime.toLowerCase() : '') + '.</span>';
            } else {
                banner.innerHTML = tick + '<span>Your result has been sent to ' + escapeHtml(email) +
                    '. You selected email only — we will not call unless you request one.</span>';
            }
            banner.classList.add('cd-itest-show');

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

    // -----------------------------------------------------------------
    // Abandonment tracking — one shot per pageview
    // -----------------------------------------------------------------
    var abandonSent = false;
    window.addEventListener('pagehide', function () {
        if (abandonSent || !startedAt || submitted) return;
        var lastStep = stepHistory[stepHistory.length - 1] || 'intro';
        try {
            var data = {
                event: 'insolvency_test_abandonment',
                tool: 'insolvency_test',
                last_step: lastStep,
                reached_capture: reachedCapture
            };
            window.dataLayer.push(data);
            if (navigator.sendBeacon) {
                navigator.sendBeacon('/wp-json/cd-itest/v1/abandon', new Blob([JSON.stringify(data)], { type: 'application/json' }));
            }
        } catch (e) {}
        abandonSent = true;
    });
})();
