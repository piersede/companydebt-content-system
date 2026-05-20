(function () {
  document.addEventListener("DOMContentLoaded", function () {
    const carousel = document.querySelector(".carousel-items");
    if (!carousel) return;

    const prevButton = document.querySelector(".carousel-prev");
    const nextButton = document.querySelector(".carousel-next");

    let slideWidth = 25;
    let visibleSlides = 4;
    let currentIndex = 0;

    const slides = Array.from(carousel.querySelectorAll(".carousel-item"));
    const totalSlides = slides.length;

    function setSlideWidth() {
      if (window.innerWidth <= 767) {
        slideWidth = 100; visibleSlides = 1;
      } else if (window.innerWidth <= 1023) {
        slideWidth = 50; visibleSlides = 2;
      } else if (window.innerWidth <= 1280) {
        slideWidth = 33; visibleSlides = 3;
      } else {
        slideWidth = 25; visibleSlides = 4;
      }
      const maxIndex = Math.max(0, totalSlides - visibleSlides);
      if (currentIndex > maxIndex) currentIndex = maxIndex;
      apply();
      updateButtons();
    }

    function apply() {
      // No transition -- transitions are being silently swallowed by something
      // on the page. Instant snap is unstyled but at least functional.
      carousel.style.transition = "none";
      carousel.style.transform = `translateX(-${currentIndex * slideWidth}%)`;
    }

    function updateButtons() {
      if (!prevButton || !nextButton) return;
      const maxIndex = Math.max(0, totalSlides - visibleSlides);
      prevButton.style.opacity = currentIndex <= 0 ? "0.35" : "1";
      prevButton.style.pointerEvents = currentIndex <= 0 ? "none" : "auto";
      nextButton.style.opacity = currentIndex >= maxIndex ? "0.35" : "1";
      nextButton.style.pointerEvents = currentIndex >= maxIndex ? "none" : "auto";
    }

    function handleNext() {
      const maxIndex = Math.max(0, totalSlides - visibleSlides);
      if (currentIndex >= maxIndex) return;
      currentIndex++;
      apply();
      updateButtons();
    }

    function handlePrev() {
      if (currentIndex <= 0) return;
      currentIndex--;
      apply();
      updateButtons();
    }

    setSlideWidth();
    if (nextButton) nextButton.addEventListener("click", handleNext);
    if (prevButton) prevButton.addEventListener("click", handlePrev);

    let touchStartX = 0, touchEndX = 0;
    carousel.addEventListener("touchstart", e => { touchStartX = e.touches[0].clientX; });
    carousel.addEventListener("touchend", e => {
      touchEndX = e.changedTouches[0].clientX;
      if (touchEndX < touchStartX - 50) handleNext();
      else if (touchEndX > touchStartX + 50) handlePrev();
    });

    window.addEventListener("resize", setSlideWidth);

    // ------------------------------------------------------------------
    // Review popup logic (preserved from the original file)
    // ------------------------------------------------------------------
    const reviewItems = document.querySelectorAll(".carousel-items .cd-review-item");
    const reviewDetailMain = document.querySelector(".cd-review-details-popup .cd-review-detail-main");
    const reviewDetailsPopup = document.querySelector(".cd-review-details-popup");
    const reviewDetailsPopupOverlay = document.querySelector(".cd-review-details-popup-overlay");
    const closeButton = document.querySelector(".cd-review-details-popup .cd-review-close");

    function handleClick(event) {
      const clickedItem = event.currentTarget;
      const innerHTML = clickedItem.innerHTML;
      if (reviewDetailMain) {
        reviewDetailMain.innerHTML = innerHTML;
        const els = reviewDetailMain.querySelectorAll(".cd-review-content, .cd-review-content-full");
        els.forEach(el => {
          if (el.classList.contains("cd-review-content")) el.style.display = "none";
          if (el.classList.contains("cd-review-content-full")) el.style.display = "block";
        });
      }
      if (reviewDetailsPopup) reviewDetailsPopup.style.display = "block";
      if (reviewDetailsPopupOverlay) reviewDetailsPopupOverlay.style.display = "block";
    }
    function closePopup() {
      if (reviewDetailsPopup) reviewDetailsPopup.style.display = "none";
      if (reviewDetailsPopupOverlay) reviewDetailsPopupOverlay.style.display = "none";
    }
    if (closeButton) closeButton.addEventListener("click", closePopup);
    reviewItems.forEach(item => item.addEventListener("click", handleClick));
  });
})();

/* -------------------------------------------------------------------
 * .cd-sources block transformation
 * Scoped to /liquidation/ (page-id-7669) for v1 iteration. To roll out
 * site-wide, drop the body-class check.
 *
 * For each <li> inside <aside class="cd-sources">:
 *   - Strip leading "— " (or any dash) from the text node after <strong>,
 *     capitalize first letter, wrap in <span class="cd-source-desc">
 *   - Strip leading " – " from the text node after </a>, wrap in
 *     <span class="cd-source-domain">
 * ------------------------------------------------------------------- */
(function () {
  function transformSources() {
    if (!document.body.classList.contains("page-id-7669")) return;
    document.querySelectorAll(".cd-sources li").forEach(function (li) {
      if (li.dataset.cdTransformed === "1") return;
      const a = li.querySelector("a");
      if (a) {
        // Open source links in a new tab
        a.setAttribute("target", "_blank");
        a.setAttribute("rel", "noopener");
        Array.from(a.childNodes).forEach(function (node) {
          if (node.nodeType !== 3) return; // text only
          let txt = node.textContent.replace(/^\s*[—–\-]\s+/, "");
          txt = txt.trim();
          if (!txt) { node.remove(); return; }
          txt = txt.charAt(0).toUpperCase() + txt.slice(1);
          const span = document.createElement("span");
          span.className = "cd-source-desc";
          span.textContent = txt;
          node.replaceWith(span);
        });
      }
      Array.from(li.childNodes).forEach(function (node) {
        if (node.nodeType !== 3) return;
        let txt = node.textContent.replace(/^\s*[—–\-]\s+/, "");
        txt = txt.trim();
        if (!txt) { node.remove(); return; }
        const span = document.createElement("span");
        span.className = "cd-source-domain";
        span.textContent = txt;
        node.replaceWith(span);
      });
      li.dataset.cdTransformed = "1";
    });
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", transformSources);
  } else {
    transformSources();
  }
})();
