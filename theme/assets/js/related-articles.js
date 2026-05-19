(function () {
  document.addEventListener("DOMContentLoaded", function () {
    const carousel = document.querySelector(".carousel-items");
    if (!carousel) {
      return;
    }

    const prevButton = document.querySelector(".carousel-prev");
    const nextButton = document.querySelector(".carousel-next");

    const SLIDE_MS = 500;
    const SLIDE_EASE = "cubic-bezier(0.4, 0, 0.2, 1)";

    let slideWidth = 25;       // percent of carousel-items width per card
    let visibleSlides = 4;
    let currentIndex = 0;
    let isTransitioning = false;

    const slides = Array.from(carousel.querySelectorAll(".carousel-item"));
    const totalSlides = slides.length;

    function setSlideWidth() {
      if (window.innerWidth <= 767) {
        slideWidth = 100;
        visibleSlides = 1;
      } else if (window.innerWidth <= 1023) {
        slideWidth = 50;
        visibleSlides = 2;
      } else if (window.innerWidth <= 1280) {
        slideWidth = 33;
        visibleSlides = 3;
      } else {
        slideWidth = 25;
        visibleSlides = 4;
      }
      carousel.style.setProperty("--slide-width", `${slideWidth}%`);
      // Clamp index if needed
      const maxIndex = Math.max(0, totalSlides - visibleSlides);
      if (currentIndex > maxIndex) currentIndex = maxIndex;
      applyTransform(false);
      updateButtons();
    }

    function applyTransform(animate) {
      carousel.style.transition = animate
        ? `transform ${SLIDE_MS}ms ${SLIDE_EASE}`
        : "none";
      carousel.style.willChange = "transform";
      carousel.style.transform = `translateX(-${currentIndex * slideWidth}%)`;
    }

    function updateButtons() {
      if (!prevButton || !nextButton) return;
      const maxIndex = Math.max(0, totalSlides - visibleSlides);
      const atStart = currentIndex <= 0;
      const atEnd = currentIndex >= maxIndex;
      prevButton.style.opacity = atStart ? "0.35" : "1";
      prevButton.style.pointerEvents = atStart ? "none" : "auto";
      nextButton.style.opacity = atEnd ? "0.35" : "1";
      nextButton.style.pointerEvents = atEnd ? "none" : "auto";
    }

    function handleNext() {
      if (isTransitioning) return;
      const maxIndex = Math.max(0, totalSlides - visibleSlides);
      if (currentIndex >= maxIndex) return;
      isTransitioning = true;
      currentIndex++;
      applyTransform(true);
      setTimeout(() => {
        isTransitioning = false;
        updateButtons();
      }, SLIDE_MS + 20);
    }

    function handlePrev() {
      if (isTransitioning) return;
      if (currentIndex <= 0) return;
      isTransitioning = true;
      currentIndex--;
      applyTransform(true);
      setTimeout(() => {
        isTransitioning = false;
        updateButtons();
      }, SLIDE_MS + 20);
    }

    setSlideWidth();

    if (nextButton) nextButton.addEventListener("click", handleNext);
    if (prevButton) prevButton.addEventListener("click", handlePrev);

    // Touch swipe
    let touchStartX = 0;
    let touchEndX = 0;

    carousel.addEventListener("touchstart", (event) => {
      touchStartX = event.touches[0].clientX;
    });

    carousel.addEventListener("touchend", (event) => {
      touchEndX = event.changedTouches[0].clientX;
      if (touchEndX < touchStartX - 50) {
        handleNext();
      } else if (touchEndX > touchStartX + 50) {
        handlePrev();
      }
    });

    window.addEventListener("resize", setSlideWidth);

    // ------------------------------------------------------------------
    // Review popup logic (preserved from the original file)
    // ------------------------------------------------------------------
    const reviewItems = document.querySelectorAll(
      ".carousel-items .cd-review-item"
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
