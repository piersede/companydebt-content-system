/* eslint-env jquery */
// /* global noUiSlider */
/* eslint no-undef: "error" */

(function ($) {
  $(document).ready(function () {
    let bankAmount = 0;
    let hmrcAmount = 0;
    let creditorsAmount = 0;
    let assetsAmount = 0;
    let isSolvent = false;
    $(".gf_amount-bank input").val(bankAmount);
    $(".gf_amount-hmrc input").val(hmrcAmount);
    $(".gf_amount-creditors input").val(creditorsAmount);
    $(".gf_amount-assets input").val(assetsAmount);
    $(".gf_personal-guarantee input").val("Yes");
    $(".gf_result input").val("Not Calculated");
    const bankSlider = document.getElementById("slider-range-bank");
    const hmrcSlider = document.getElementById("slider-range-hmrc");
    const creditorsSlider = document.getElementById("slider-range-creditors");
    const assetsSlider = document.getElementById("slider-range-assets");

    noUiSlider.create(bankSlider, {
      start: [0],
      step: 1000,
      range: {
        min: [0],
        max: [350000],
      },
      connect: "lower",
    });
    noUiSlider.create(hmrcSlider, {
      start: [0],
      step: 1000,
      range: {
        min: [0],
        max: [350000],
      },
      connect: "lower",
    });
    noUiSlider.create(creditorsSlider, {
      start: [0],
      step: 1000,
      range: {
        min: [0],
        max: [350000],
      },
      connect: "lower",
    });
    noUiSlider.create(assetsSlider, {
      start: [0],
      step: 1000,
      range: {
        min: [0],
        max: [350000],
      },
      connect: "lower",
    });
    /* eslint-disable */
    function checkSolvency() {
      if (
        parseInt(bankAmount) +
          parseInt(hmrcAmount) +
          parseInt(creditorsAmount) >
        parseInt(assetsAmount)
      ) {
        $(".gf_result input").val("Insolvent");
        isSolvent = false;
      } else {
        $(".gf_result input").val("Solvent");
        isSolvent = true;
      }
    }
    /* eslint-disable */
    const bankAmountSlider = document.getElementById("quiz-amount-bank");
    const hmrcAmountSlider = document.getElementById("quiz-amount-hmrc");
    const creditorsAmountSlider = document.getElementById(
      "quiz-amount-creditors"
    );
    const assetsAmountSlider = document.getElementById("quiz-amount-assets");

    bankSlider.noUiSlider.on("update", function (values, handle) {
      bankAmount = values[handle];
      $(".gf_amount-bank input").val(bankAmount);
      bankAmountSlider.innerHTML =
        "£ " + Intl.NumberFormat("gb-GB").format(bankAmount);
      checkSolvency();
    });

    hmrcSlider.noUiSlider.on("update", function (values, handle) {
      hmrcAmount = values[handle];
      $(".gf_amount-hmrc input").val(hmrcAmount);
      hmrcAmountSlider.innerHTML =
        "£ " + Intl.NumberFormat("gb-GB").format(hmrcAmount);
      checkSolvency();
    });

    creditorsSlider.noUiSlider.on("update", function (values, handle) {
      creditorsAmount = values[handle];
      $(".gf_amount-creditors input").val(creditorsAmount);
      creditorsAmountSlider.innerHTML =
        "£ " + Intl.NumberFormat("gb-GB").format(creditorsAmount);
      checkSolvency();
    });

    assetsSlider.noUiSlider.on("update", function (values, handle) {
      assetsAmount = values[handle];
      $(".gf_amount-assets input").val(assetsAmount);
      assetsAmountSlider.innerHTML =
        "£ " + Intl.NumberFormat("gb-GB").format(assetsAmount);
      checkSolvency();
    });
    /* eslint-enable */

    const quizTabTitleOne = $(".quiz-nav .nav-item-1");
    const quizTabTitleTwo = $(".quiz-nav .nav-item-2");
    const quizTabTitleThree = $(".quiz-nav .nav-item-3");

    function activateTabTwo() {
      $("#quiz-tab-1").removeClass("active");
      $("#quiz-tab-2").addClass("active");
      $("#quiz-tab-3").removeClass("active");
      quizTabTitleOne.removeClass("active");
      quizTabTitleTwo.addClass("active");
      quizTabTitleThree.removeClass("active");
      $(".quiz-tab-container").addClass("tab-2");
      $("html, body").animate({ scrollTop: 0 }, "fast");
    }

    function changeActiveTab() {
      quizTabTitleTwo.removeClass("active");
      quizTabTitleThree.addClass("active");
    }

    function calculateSolvency() {
      if (!isSolvent) {
        $(".quiz-answer").addClass("insolvent");
      } else {
        $(".quiz-answer").addClass("solvent");
      }
    }

    function addEventListeners() {
      const quizRadioContainer = $(".quiz-radio-container");
      quizRadioContainer.on("click", function () {
        if (
          $(this).children(".quiz-radio")[0].checked === false ||
          $(this).hasClass("active") === false
        ) {
          $(this).addClass("active");
          $(this).siblings().removeClass("active");
          $(this).children(".quiz-radio")[0].checked = true;
          $(this).siblings().children(".quiz-radio")[0].checked = false;
          $(".gf_personal-guarantee input").val($(this)[0].outerText);
        }
      });
      const buttonNextScreenOne = $("#quiz-tab-1 .quiz-button");
      buttonNextScreenOne.on("click", activateTabTwo);

      $(document).on("gform_confirmation_loaded", function () {
        calculateSolvency();
        changeActiveTab();
        $("html, body").animate({ scrollTop: 0 }, "fast");
      });
    }
    addEventListeners();
  });
})(jQuery);
