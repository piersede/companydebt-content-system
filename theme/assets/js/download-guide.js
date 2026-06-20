(function () {
  var $ = jQuery;

  $(document).ready(function () {
    document.addEventListener("gform_confirmation_loaded", function (event) {
      triggerDownload();
    });

    var $downloadButton = $(".widget__download_d22_1-button");
    var $lightbox = $(".widget__download-lightbox");

    function hideLightbox() {
      $lightbox.css("visibility", "hidden").css("height", "0");
    }

    if ($downloadButton.length > 0) {
      $downloadButton.on("click", function () {
        $lightbox.css("visibility", "visible").css("height", "100%");
        $(document).scrollTop(0);
      });

      $(".widget__download-lightbox__container-close").on(
        "click",
        hideLightbox
      );

      $("body, html").on("keydown", function (event) {
        if (event.keyCode === 27) {
          hideLightbox();
        }
      });
    }
  });
})();
