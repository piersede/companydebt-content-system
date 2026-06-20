/**
 * Script used to print Table of Content on Pages
 */

/* eslint func-names: ["error", "never"] */
/* eslint-env jquery */

(function ($) {
  function createTOC() {
    const anchor = $(".toc__heading");
    const headings = $(".content > h2");
    let olH2Opened = true;
    let liHtml;
    let innerliHtml;
    function getOrderNumber(heading) {
      innerliHtml = " ";
      if (olH2Opened) {
        innerliHtml += "</li>";
        olH2Opened = false;
      } else {
        olH2Opened = true;
      }
      console.log($("#" + heading.id));
      return `${innerliHtml}<li class="toc__li"><a href="#${heading.id}">${heading.innerText}</a>`;
    }
    function generateTable() {
      liHtml = "";
      for (let i = 0; i < headings.length; i += 1) {
        headings[i].id = `toc-${i}`;
        liHtml += getOrderNumber(headings[i]);
      }
      return liHtml;
    }
    const htmlStart = `${`<ul class='toc__ul  active'>`}${generateTable()}`;
    anchor.append(htmlStart);
    anchor.append("</ul></div>");
  }
  function handleTocContent() {
    $(".toc__ul, .toc__heading, .widget__toc").toggleClass("active");
  }
  $(document).ready(function () {
    createTOC();
    $(".toc").on("click", handleTocContent);
  });
  // $(function () {
  //   const slugify = function (str) {
  //     return str
  //       .toLowerCase()
  //       .trim()
  //       .replace(/[^\w\s-]/g, "")
  //       .replace(/[\s_-]+/g, "-")
  //       .replace(/^-+|-+$/g, "");
  //   };
  //   let sections = [];
  //   let currentSection = {};
  //   let headers = document.querySelectorAll(".content h2, .content h3");
  //   headers.forEach((header) => {
  //     if (header.tagName === "H2") {
  //       if (Object.keys(currentSection).length !== 0) {
  //         sections.push(currentSection);
  //       }
  //       header.id = slugify(header.textContent);
  //       currentSection = {
  //         title: header.textContent,
  //         id: header.id,
  //         children: [],
  //       };
  //     } else if (header.tagName === "H3") {
  //       header.id = slugify(header.textContent);
  //       currentSection.children.push({
  //         title: header.textContent,
  //         id: header.id,
  //       });
  //     }
  //   });
  //   sections.push(currentSection);
  //   console.log(sections);
  // });
})(jQuery);
