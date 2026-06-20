(function ($) {
  $(function () {
    $(".tab__link--container").on("click", function () {
      $(".tab__link--container").removeClass("active");
      $(".tab__content").hide();
      $(this).addClass("active");
      $(`.${$(this).data("value")}`).show();
    });
  });
})(jQuery);
