(function ($) {
  $(document).ready(function () {
    const accordionItem = $(".accordion-item");
    accordionItem.on("click", function () {
      $(this)
        .children(".accordion-description")
        .slideToggle(300)
        .toggleClass("closed");
      $(this).toggleClass("closed");
    });
  });
})(jQuery);
