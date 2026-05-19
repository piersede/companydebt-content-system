(function () {
  document.addEventListener("DOMContentLoaded", function () {
    const carousel = document.querySelector(".carousel-items");
    if (!carousel) {
      return;
    }

    const prevButton = document.querySelector(".carousel-prev");
    const nextButton = document.querySelector(".carousel-next");

    function getCardStep() {
      const first = carousel.querySelector(".carousel-item");
      if (!first) return 0;
      const r = first.getBoundingClientRect();
      const cs = getComputedStyle(first);
      const ml = parseFloat(cs.marginLeft) || 0;
      const mr = parseFloat(cs.marginRight) || 0;
      return r.width + ml + mr;
    }

    function updateButtons() {
      if (!prevButton || !nextButton) return;
      const atStart = carousel.scrollLeft <= 1;
      const atEnd = carousel.scrollLeft + carousel.clientWidth >= carousel.scrollWidth - 1;
      prevButton.style.opacity = atStart ? "0.35" : "1";
      prevButton.style.pointerEvents = atStart ? "none" : "auto";
      nextButton.style.opacity = atEnd ? "0.35" : "1";
      nextButton.style.pointerEvents = atEnd ? "none" : "auto";
    }

    function handleNext() {
      carousel.scrollBy({ left: getCardStep(), behavior: "smooth" });
    }

    function handlePrev() {
      carousel.scrollBy({ left: -getCardStep(), behavior: "smooth" });
    }

    if (nextButton) nextButton.addEventListener("click", handleNext);
    if (prevButton) prevButton.addEventListener("click", handlePrev);

    carousel.addEventListener("scroll", updateButtons, { passive: true });
    window.addEventListener("resize", updateButtons);

    // Initial button state
    setTimeout(updateButtons, 0);

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
