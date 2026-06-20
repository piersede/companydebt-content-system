(function ($) {
  $(function () {
    $(".article-sources-title").on("click", function () {
      $(this).toggleClass("active");
      $(this).parent().find(".article-sources-content").slideToggle();
    });

    $(".section-related-menu-widget li.menu-item-has-children a").on(
      "click",
      function (e) {
        e.stopPropagation();
      }
    );

    $(".section-related-menu-widget li.menu-item-has-children").on(
      "click",
      function (e) {
        $(this).toggleClass("active-sub-menu");
        $(this).find("ul.sub-menu").slideToggle();
      }
    );
  });
})(jQuery);
