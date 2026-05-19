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

    let slideWidth = 25;
    let visibleSlides = 4;
    let isTransitioning = false;

    function setSlideWidth() {
      if (window.innerWidth <= 767) {
        slideWidth = 100;
        visibleSlides = 1;
      } else if (window.innerWidth > 767 && window.innerWidth <= 1023) {
        slideWidth = 50;
        visibleSlides = 2;
      } else if (window.innerWidth > 1023 && window.innerWidth <= 1280) {
        slideWidth = 33;
        visibleSlides = 3;
      } else {
        slideWidth = 25;
        visibleSlides = 4;
      }
      carousel.style.setProperty("--slide-width", `${slideWidth}%`);
    }

    // Enable transition via inline style (avoids any CSS-class cascade issues)
    function enableTransition() {
      carousel.style.transition = `transform ${SLIDE_MS}ms ${SLIDE_EASE}`;
      carousel.style.willChange = "transform";
    }
    function disableTransition() {
      carousel.style.transition = "none";
    }

    function handleNext() {
      if (isTransitioning) return;
      isTransitioning = true;

      enableTransition();
      // Trigger slide on next frame so the browser commits the transition style
      // before mutating transform (otherwise transform jumps without animating)
      requestAnimationFrame(() => {
        carousel.style.transform = `translateX(-${slideWidth}%)`;
      });

      setTimeout(() => {
        // Animation done. Suspend transition, mutate DOM, reset transform,
        // force a synchronous reflow so the snap-back doesn't animate, then
        // re-enable transition for the next click.
        disableTransition();
        carousel.appendChild(carousel.firstElementChild);
        carousel.style.transform = "translateX(0)";
        void carousel.offsetWidth; // force reflow
        isTransitioning = false;
      }, SLIDE_MS + 20); // small buffer to make sure the visual animation has fully painted
    }

    function handlePrev() {
      if (isTransitioning) return;
      isTransitioning = true;

      // Pre-position: move last to start, jump transform left by one slide
      // (no transition) so the layout is identical to the current visual,
      // then transition back to translateX(0) on the next frame.
      disableTransition();
      carousel.insertBefore(carousel.lastElementChild, carousel.firstElementChild);
      carousel.style.transform = `translateX(-${slideWidth}%)`;
      void carousel.offsetWidth; // commit the no-transition state

      requestAnimationFrame(() => {
        enableTransition();
        carousel.style.transform = "translateX(0)";
      });

      setTimeout(() => {
        isTransitioning = false;
      }, SLIDE_MS + 20);
    }

    setSlideWidth();

    if (nextButton) nextButton.addEventListener("click", handleNext);
    if (prevButton) prevButton.addEventListener("click", handlePrev);

    let touchStartX = 0;
    let touchEndX = 0;

    const handleSwipe = () => {
      if (touchEndX < touchStartX - 50) {
        handleNext();
      } else if (touchEndX > touchStartX + 50) {
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

    window.addEventListener("resize", () => {
      setSlideWidth();
    });

    // Autoslide disabled
    // setInterval(function () { handleNext(); }, 4000);

    // ------------------------------------------------------------------
    // Review popup logic (preserved from the original file — used by
    // testimonials-style carousels elsewhere on the site; does nothing
    // when .carousel-items contains article cards).
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
