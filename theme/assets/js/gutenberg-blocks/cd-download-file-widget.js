(function ($) {
  $(function () {
    $(".widget-download-button").on("click", function () {
      $(".section-widget-download-popup-wrapper").css("display", "flex");
      $("body, html").css("overflow", "hidden");
    });

    $(".download-popup-widget-close").on("click", function () {
      $(".section-widget-download-popup-wrapper").hide();
      $("body, html").css("overflow", "auto");
    });
  });
})(jQuery);
