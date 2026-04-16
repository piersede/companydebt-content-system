/**
 * File navigation.js.
 *
 * Handles toggling the navigation menu for small screens and enables TAB key
 * navigation support for dropdown menus.
 */
(function () {
  let prevScrollpos = window.pageYOffset;

  window.onscroll = function () {
    let headerSearch = document.getElementById("search-form");
    let currentScrollPos = window.pageYOffset;
    let backToTop = document.getElementById("back-to-top");
    let masthead = document.getElementById("masthead");
    if (!document.body.classList.contains("menu-toggled")) {
      // Hide-on-scroll: desktop only, and only after 200px of scroll.
      // Mobile keeps the header pinned to avoid a white-gap flash caused
      // by the reserved header space remaining when masthead slides up.
      let isMobile = window.innerWidth < 1038;
      let shouldHide =
        !isMobile &&
        currentScrollPos > 200 &&
        currentScrollPos > prevScrollpos;

      if (!shouldHide) {
        if (masthead) {
          masthead.style.top = "0";
        }
        if (headerSearch) {
          if (document.getElementById("wpadminbar")) {
            headerSearch.style.top = "124px";
          } else {
            headerSearch.style.top = "92px";
          }
        }
      } else {
        if (masthead) {
          masthead.style.top = "-92px";
        }
        if (headerSearch) {
          headerSearch.style.top = "-92px";
        }
      }

      if (backToTop && window.outerWidth < 769) {
        if (currentScrollPos > 200) {
          backToTop.style.display = "flex";
        } else {
          backToTop.style.display = "none";
        }
      }
      prevScrollpos = currentScrollPos;
    }
  };

  if (window.outerWidth > 1037) {
    return;
  }
  const siteNavigation = document.getElementById("site-navigation");

  // Return early if the navigation doesn't exist.
  if (!siteNavigation) {
    return;
  }

  const button = document.getElementById("primary-menu-toggle");

  // Return early if the button doesn't exist.
  if ("undefined" === typeof button) {
    return;
  }

  const menu = siteNavigation.getElementsByTagName("ul")[0];

  // Hide menu toggle button if menu is empty and return early.
  if ("undefined" === typeof menu) {
    button.style.display = "none";
    return;
  }

  if (!menu.classList.contains("nav-menu")) {
    menu.classList.add("nav-menu");
  }

  // Toggle the .toggled class and the aria-expanded value each time the button is clicked.
  button.addEventListener("click", function () {
    siteNavigation.classList.toggle("toggled");
    document.body.classList.toggle("menu-toggled");
    if (button.getAttribute("aria-expanded") === "true") {
      button.setAttribute("aria-expanded", "false");
    } else {
      button.setAttribute("aria-expanded", "true");
    }
  });

  // Remove the .toggled class and set aria-expanded to false when the user clicks outside the navigation.
  document.addEventListener("click", function (event) {
    const isClickInside =
      siteNavigation.contains(event.target) || button.contains(event.target);

    if (!isClickInside) {
      siteNavigation.classList.remove("toggled");
      document.body.classList.remove("menu-toggled");
      button.setAttribute("aria-expanded", "false");
    }
  });

  // Get all the link elements within the menu.
  const links = menu.getElementsByTagName("a");

  // Get all the link elements with children within the menu.
  const linksWithChildren = menu.querySelectorAll(
    ".menu-item-has-children > span.menu-arrow"
  );

  // Toggle focus each time a menu link is focused or blurred.
  // for ( const link of links ) {
  // 	link.addEventListener( 'focus', toggleFocus, true );
  // 	link.addEventListener( 'blur', toggleFocus, true );
  // }

  // Toggle focus each time a menu link with children receive a touch event.
  for (const link of linksWithChildren) {
    // link.addEventListener( 'touchstart', toggleFocus, false );
    link.addEventListener("click", toggleFocus, false);
    // Also bind click on the sibling title (span/a) so tapping anywhere on the row works
    const parentLi = link.parentNode;
    const titleEl = parentLi.querySelector(':scope > span:not(.menu-arrow), :scope > a');
    if (titleEl && titleEl !== link) {
      titleEl.addEventListener("click", function(event) {
        // Synthesize the same context as clicking the arrow
        event.preventDefault();
        const menuItem = link.parentNode;
        for (const sibling of menuItem.parentNode.children) {
          if (menuItem !== sibling) {
            sibling.classList.remove("focus");
          }
        }
        menuItem.classList.toggle("focus");
      }, false);
    }
  }

  /**
   * Sets or removes .focus class on an element.
   */
  function toggleFocus(event) {
    if (event.type === "focus" || event.type === "blur") {
      let self = this;
      // Move up through the ancestors of the current link until we hit .nav-menu.
      while (!self.classList.contains("nav-menu")) {
        // On li elements toggle the class .focus.
        if ("li" === self.tagName.toLowerCase()) {
          self.classList.toggle("focus");
        }
        self = self.parentNode;
      }
      return true;
    } else if (event.type === "click") {
      const menuItem = this.parentNode;
      event.preventDefault();
      for (const link of menuItem.parentNode.children) {
        if (menuItem !== link) {
          link.classList.remove("focus");
        }
      }
      menuItem.classList.toggle("focus");
    }
  }
})();
