/* eslint func-names: ["error", "never"] */
/* eslint-env jquery */
/* eslint-disable import/prefer-default-export */

(function ($) {
	let formInputs;
	let redundancyPay = 0;
	let email;
	let limit;
	let factor;
	let redunCalcService;
	let redunCalcAge;
	let redunCalcWage;

	function nextButtonPageOneText() {
		$('.gform_page:nth-child(1) .gform_next_button').val('Get my Calculation');
	}

	function calcPartUnder() {
		redundancyPay += factor * formInputs.yearsService * formInputs.weeklyWage;
	}

	function calcPartOver() {
		if (formInputs.age >= limit) {
			if (formInputs.age - formInputs.yearsService >= limit) {
				redundancyPay += factor * formInputs.yearsService * formInputs.weeklyWage;
				formInputs.yearsService = 0;
			} else {
				redundancyPay += factor * (formInputs.age - limit) * formInputs.weeklyWage;
				formInputs.yearsService = formInputs.yearsService - formInputs.age + limit;
			}
		}
	}

	function calculateCompensation() {
		if (formInputs.yearsService > 20) {
			formInputs.yearsService = 20;
		}
		if (formInputs.weeklyWage > 538) {
			formInputs.weeklyWage = 538;
		}
		calcPartOver(formInputs, (limit = 41), (factor = 1.5), redundancyPay);
		calcPartOver(formInputs, (limit = 22), (factor = 1), redundancyPay);
		calcPartUnder(formInputs, (limit = 0), (factor = 0.5), redundancyPay);
	}

	function getEnteredFields() {
		formInputs = {
			age: redunCalcAge.val(),
			yearsService: redunCalcService.val(),
			weeklyWage: redunCalcWage.val(),
		};
		email = $('.redun_calc__email input').val();

		calculateCompensation(formInputs, redundancyPay);

		redundancyPay = new Intl.NumberFormat('en-GB', {
			style: 'currency',
			currency: 'GBP',
			minimumFractionDigits: 0,
		}).format(redundancyPay);
	}

	function redunCalclFormHandling() {
		$(document).on('gform_page_loaded', function (event, formId, currentPage) {
			const pageNr = parseInt(currentPage, 10);
			switch (true) {
				case pageNr === 1:
					redundancyPay = 0;
					nextButtonPageOneText();
					break;
				case pageNr === 2:
					redundancyPay = 0;
					$('.gform_page .gform_next_button').val('View Results');
					break;
				case pageNr === 3:
					redundancyPay = 0;
					getEnteredFields();
					$('.redun_calc__amount').text(redundancyPay);
					$('.redun_calc__email_3 input').val(email);
					break;
				default:
			}
		});
	}

	function checkDigitsOnly(event) {
		if (event.keyCode < 48 || event.keyCode > 57) {
			event.preventDefault();
		}
	}

	function addEventListeners() {
		redunCalcService = $('.redun_calc__service input');
		redunCalcAge = $('.redun_calc__age input');
		redunCalcWage = $('.redun_calc__wage input');

		if (redunCalcService.length > 0) {
			[redunCalcService, redunCalcAge, redunCalcWage].forEach(function (input) {
				input.on('keypress', function (event) {
					checkDigitsOnly(event);
				});
			});
			[redunCalcService, redunCalcAge, redunCalcWage].forEach(function (input) {
				input.on('paste', function (event) {
					event.preventDefault();
				});
			});
		}

		// if (redunCalcAge.length > 0) {
		// 	redunCalcAge.on('blur');
		// 	{
		// 		console.log('check age');
		// 	}
		// }
	}

	$(document).ready(function () {
		// GF Redundancy Calculator Form
		if ($('.redun_calc__form').length > 0) {
			addEventListeners();
			nextButtonPageOneText();
			redunCalclFormHandling();
		}
	});
})(jQuery);
