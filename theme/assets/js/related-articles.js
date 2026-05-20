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
 * .cd-sources block transformation + category grouping
 * Scoped to /liquidation/ (page-id-7669) for the iteration. To roll out
 * site-wide, drop the body-class check.
 *
 * For each <li> inside <aside class="cd-sources">:
 *   - Strip leading "— " from text after <strong>, capitalize, wrap in
 *     <span class="cd-source-desc">
 *   - Strip leading " – " from text after </a>, wrap in
 *     <span class="cd-source-domain">
 *   - Classify by URL into 'legislation' | 'publication' | 'guidance'
 *   - Open in new tab
 * Then re-group the <li>s under labelled subheadings.
 * ------------------------------------------------------------------- */
(function () {
  const CATEGORIES = [
    { key: "legislation", label: "Primary Legislation" },
    { key: "publication", label: "Official Publications" },
    { key: "guidance",    label: "Guidance & Resources" },
  ];

  function classify(href) {
    let u;
    try { u = new URL(href, window.location.origin); } catch (e) { return "guidance"; }
    const d = u.hostname.replace(/^www\./, "");
    if (d === "legislation.gov.uk") return "legislation";
    if (d === "thegazette.co.uk") return "publication";
    if (d === "gov.uk" || d.endsWith(".gov.uk")) {
      return u.pathname.startsWith("/government/") ? "publication" : "guidance";
    }
    return "guidance";
  }

  function cleanLi(li) {
    if (li.dataset.cdTransformed === "1") return;
    const a = li.querySelector("a");
    if (a) {
      a.setAttribute("target", "_blank");
      a.setAttribute("rel", "noopener");
      Array.from(a.childNodes).forEach(function (node) {
        if (node.nodeType !== 3) return;
        let txt = node.textContent.replace(/^\s*[—–\-]\s+/, "").trim();
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
      let txt = node.textContent.replace(/^\s*[—–\-]\s+/, "").trim();
      if (!txt) { node.remove(); return; }
      const span = document.createElement("span");
      span.className = "cd-source-domain";
      span.textContent = txt;
      node.replaceWith(span);
    });
    li.dataset.cdTransformed = "1";
  }

  function transformAside(aside) {
    if (aside.dataset.cdGrouped === "1") return;
    const lis = Array.from(aside.querySelectorAll("ul > li"));
    if (!lis.length) return;

    // Clean + classify
    const buckets = { legislation: [], publication: [], guidance: [] };
    lis.forEach(function (li) {
      cleanLi(li);
      const a = li.querySelector("a");
      const href = a ? a.getAttribute("href") : "";
      const cat = classify(href);
      li.classList.add("cd-source", "cd-source--" + cat);
      buckets[cat].push(li);
    });

    // Remove the original <ul> wrapper(s)
    aside.querySelectorAll("ul").forEach(function (ul) { ul.remove(); });

    // Append one group per category that has items
    let totalCount = 0;
    let firstCatCount = 0;
    CATEGORIES.forEach(function (cat) {
      const items = buckets[cat.key];
      if (!items.length) return;
      const groupDiv = document.createElement("div");
      groupDiv.className = "cd-sources__group cd-sources__group--" + cat.key;
      const h4 = document.createElement("h4");
      h4.className = "cd-sources__subhead";
      h4.textContent = cat.label;
      groupDiv.appendChild(h4);
      const newUl = document.createElement("ul");
      items.forEach(function (li) { newUl.appendChild(li); });
      groupDiv.appendChild(newUl);
      aside.appendChild(groupDiv);
      if (firstCatCount === 0) firstCatCount = items.length;
      totalCount += items.length;
    });

    // Collapse pattern: show first category + up to 3 of its rows; rest
    // hidden behind a "Read more sources (X)" toggle button.
    const PREVIEW_COUNT = 3;
    const previewShown = Math.min(PREVIEW_COUNT, firstCatCount);
    const hiddenCount = totalCount - previewShown;
    if (hiddenCount > 0) {
      aside.classList.add("is-collapsed");
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "cd-sources__toggle";
      btn.setAttribute("aria-expanded", "false");
      btn.textContent = "Read more sources (" + hiddenCount + ")";
      btn.addEventListener("click", function () {
        const collapsed = aside.classList.toggle("is-collapsed");
        btn.setAttribute("aria-expanded", collapsed ? "false" : "true");
        btn.textContent = collapsed
          ? "Read more sources (" + hiddenCount + ")"
          : "Show fewer sources";
      });
      aside.appendChild(btn);
    }

    aside.dataset.cdGrouped = "1";
  }

  function transformSources() {
    if (!document.body.classList.contains("page-id-7669")) return;
    document.querySelectorAll(".cd-sources").forEach(transformAside);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", transformSources);
  } else {
    transformSources();
  }
})();
