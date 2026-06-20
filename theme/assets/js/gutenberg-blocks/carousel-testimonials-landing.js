(function ($) {
  $(function () {
    $(".testimonial-carousel__testimonials").slick({
      infinite: true,
      slidesToShow: 1,
      slidesToScroll: 1,
      arrows: false,
      mobileFirst: true,
      responsive: [
        {
          breakpoint: 991,
          settings: {
            arrows: false,
            slidesToShow: 2,
            slidesToScroll: 1,
          },
        },
      ],
    });
  });
})(jQuery);
