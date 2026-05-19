(function () {
  document.addEventListener("DOMContentLoaded", function () {
    const carousel = document.querySelector(".carousel-items");
    if (!carousel) {
      return;
    }

    const prevButton = document.querySelector(".carousel-prev");
    const nextButton = document.querySelector(".carousel-next");

    const FADE_MS = 250;
    let visibleSlides = 4;
    let isTransitioning = false;

    function setVisibleSlides() {
      if (window.innerWidth <= 767) {
        visibleSlides = 1;
      } else if (window.innerWidth <= 1023) {
        visibleSlides = 2;
      } else if (window.innerWidth <= 1280) {
        visibleSlides = 3;
      } else {
        visibleSlides = 4;
      }
    }

    function fadeIn(el) {
      if (!el) return;
      el.style.transition = "none";
      el.style.opacity = "0";
      // Commit the opacity:0 in this frame, then animate to 1 on the next
      void el.offsetWidth;
      el.style.transition = `opacity ${FADE_MS}ms ease`;
      el.style.opacity = "1";
      setTimeout(() => {
        el.style.transition = "";
        el.style.opacity = "";
      }, FADE_MS + 30);
    }

    function handleNext() {
      if (isTransitioning) return;
      isTransitioning = true;

      // Rotate DOM: move first card to the end (the off-screen card on the
      // right -- which is the new rightmost visible card -- is now in slot N)
      carousel.appendChild(carousel.firstElementChild);

      // Fade in the new rightmost visible card so it doesn't pop in jarringly
      const newRightmost = carousel.children[visibleSlides - 1];
      fadeIn(newRightmost);

      setTimeout(() => {
        isTransitioning = false;
      }, FADE_MS + 30);
    }

    function handlePrev() {
      if (isTransitioning) return;
      isTransitioning = true;

      // Rotate DOM the other way: move last card to the beginning
      carousel.insertBefore(
        carousel.lastElementChild,
        carousel.firstElementChild
      );

      // Fade in the new leftmost card
      const newLeftmost = carousel.children[0];
      fadeIn(newLeftmost);

      setTimeout(() => {
        isTransitioning = false;
      }, FADE_MS + 30);
    }

    setVisibleSlides();

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

    window.addEventListener("resize", setVisibleSlides);

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
