(function () {
  document.addEventListener("DOMContentLoaded", function () {
    const carousel = document.querySelector(".cd-reviews-items");
    const prevButton = document.querySelector(".cd-reviews-prev");
    const nextButton = document.querySelector(".cd-reviews-next");
    let currentIndex = 0;
    let prevIndex = 0;
    const slides = document.querySelectorAll(".cd-review-item");
    const totalSlides = slides.length;

    function setSlideWidth() {
      if (window.innerWidth <= 767) {
        slideWidth = 100;
      } else if (window.innerWidth > 767 && window.innerWidth <= 1280) {
        slideWidth = 50;
      } else {
        slideWidth = 33.3333;
      }
      carousel.style.setProperty("--slide-width", `${slideWidth}%`);
    }

    function handleNext() {
      carousel.classList.add("sliding-transition");

      prevIndex = currentIndex;
      currentIndex = (currentIndex + 1) % totalSlides;

      carousel.style.transform = `translateX(-${slideWidth}%)`;

      setTimeout(() => {
        carousel.appendChild(slides[prevIndex]);
        carousel.classList.remove("sliding-transition");
        carousel.style.transform = "";
      }, 500);
    }

    function handlePrev() {
      prevIndex = currentIndex;
      currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;

      carousel.style.transform = `translateX(-${slideWidth}%)`;
      carousel.insertBefore(slides[currentIndex], carousel.firstChild);

      setTimeout(() => {
        carousel.style.transform = "";
        carousel.classList.add("sliding-transition");
      }, 10);

      setTimeout(() => {
        carousel.classList.remove("sliding-transition");
      }, 490);
    }

    nextButton.addEventListener("click", handleNext);
    prevButton.addEventListener("click", handlePrev);

    let touchStartX = 0;
    let touchEndX = 0;

    const handleSwipe = () => {
      if (touchEndX < touchStartX) {
        handleNext();
      } else if (touchEndX > touchStartX) {
        handlePrev();
      }
    };

    carousel.addEventListener("touchstart", (event) => {
      touchStartX = event.touches[0].clientX;
    });

    carousel.addEventListener("touchend", (event) => {
      touchEndX = event.changedTouches[0].clientX;
      handleSwipe();
    });

    setSlideWidth();
    window.addEventListener("resize", setSlideWidth);

    setInterval(function () {
      handleNext();
    }, 4000);

    const reviewItems = document.querySelectorAll(
      ".cd-reviews-items .cd-review-item"
    );

    const reviewDetailMain = document.querySelector(
      ".cd-review-details-popup .cd-review-detail-main"
    );

    const reviewDetailsPopup = document.querySelector(
      ".cd-review-details-popup"
    );

    const reviewDetailsPopupOverlay = document.querySelector(
      ".cd-review-details-popup-overlay"
    );

    const closeButton = document.querySelector(
      ".cd-review-details-popup .cd-review-close"
    );

    function handleClick(event) {
      const clickedItem = event.currentTarget;

      const innerHTML = clickedItem.innerHTML;

      if (reviewDetailMain) {
        reviewDetailMain.innerHTML = innerHTML;

        const contentElements = reviewDetailMain.querySelectorAll(
          ".cd-review-content, .cd-review-content-full"
        );
        contentElements.forEach((el) => {
          if (el.classList.contains("cd-review-content")) {
            el.style.display = "none";
          }
          if (el.classList.contains("cd-review-content-full")) {
            el.style.display = "block";
          }
        });
      }

      if (reviewDetailsPopup) {
        reviewDetailsPopup.style.display = "block";
      }
      if (reviewDetailsPopupOverlay) {
        reviewDetailsPopupOverlay.style.display = "block";
      }
    }

    function closePopup() {
      if (reviewDetailsPopup) {
        reviewDetailsPopup.style.display = "none";
      }
      if (reviewDetailsPopupOverlay) {
        reviewDetailsPopupOverlay.style.display = "none";
      }
    }

    if (closeButton) {
      closeButton.addEventListener("click", closePopup);
    }

    reviewItems.forEach((item) => {
      item.addEventListener("click", handleClick);
    });
  });
})();
