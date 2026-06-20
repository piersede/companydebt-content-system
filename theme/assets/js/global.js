(function ($) {
  $(function () {
    $(".header-search").on("click", function () {
      $(".search-form ").toggleClass("is-active");
      $(this).toggleClass("is-active");

      const $icon = $(this).find("img");
      let src = $icon.attr("src");

      if ($(this).hasClass("is-active")) {
        src = src.replace("search-white", "close-white");
      } else {
        src = src.replace("close-white", "search-white");
      }
      $icon.attr("src", src);

      const $source = $(this).find('source');

      if($source.length) {
        let sourceSrc = $source.attr('srcset');
        if ($(this).hasClass("is-active")) {
          sourceSrc = sourceSrc.replace("search-white", "close-white");
        } else {
          sourceSrc = sourceSrc.replace("close-white", "search-white");
        }
        $source.attr('srcset', sourceSrc);
      }
    });

    // Modern LiveChat tag (v2.0) + 5-second delayed init.
    // Replaces legacy direct-tracking.js insertion. Two LCP improvements:
    //   1. Modern wrapper exposes window.LiveChatWidget and stages engine load
    //      progressively (launcher paints first, heavy engine in stages).
    //   2. asyncInit=true suppresses auto-init; setTimeout fires init() after
    //      5s so tracking.js fetch happens well after LCP, not on critical path.
    // License 8321211 unchanged. Visitor experience: chat appears 5s after
    // page load instead of immediately - acceptable per stakeholder.
    window.__lc = window.__lc || {};
    window.__lc.license = 8321211;
    window.__lc.integration_name = "manual_channels";
    window.__lc.product_name = "livechat";
    window.__lc.asyncInit = true;
    /* eslint-disable */
    ;(function(n,t,c){function i(n){return e._h?e._h.apply(null,n):e._q.push(n)}var e={_q:[],_h:null,_v:"2.0",on:function(){i(["on",c.call(arguments)])},once:function(){i(["once",c.call(arguments)])},off:function(){i(["off",c.call(arguments)])},get:function(){if(!e._h)throw new Error("[LiveChatWidget] You can't use getters before load.");return i(["get",c.call(arguments)])},call:function(){i(["call",c.call(arguments)])},init:function(){var n=t.createElement("script");n.async=!0,n.type="text/javascript",n.src="https://cdn.livechatinc.com/tracking.js",t.head.appendChild(n)}};!n.__lc.asyncInit&&e.init(),n.LiveChatWidget=n.LiveChatWidget||e}(window,document,[].slice));
    /* eslint-enable */
    setTimeout(function () {
      if (window.LiveChatWidget && typeof window.LiveChatWidget.init === "function") {
        window.LiveChatWidget.init();
      }
    }, 5000);

    const foonoteLink = document.querySelectorAll(".ep-footnote__referrer");

    if (foonoteLink.length > 0) {
      const articleContent = document.querySelector(".content");

      foonoteLink.forEach(function (item) {
        item.addEventListener("mouseover", function () {
          const articleWidth = articleContent.offsetWidth;
          const articleLeft = articleContent.offsetLeft;
          const currentPosition = item.offsetLeft;
          const leftSpace = currentPosition - articleLeft;
          const rightSpace = articleWidth + articleLeft - currentPosition;
          if (window.innerWidth > 767) {
            if (leftSpace > 150 && rightSpace > 150) {
              item.lastChild.style.left = "-150px";
            } else if (leftSpace <= 150) {
              item.lastChild.style.left = `-${leftSpace}px`;
            } else {
              item.lastChild.style.left = `${rightSpace - 300}px`;
            }
          } else {
            item.lastChild.style.left = `-${leftSpace}px`;
          }
        });
      });
    }

    function downloadFile() {
      let fileDownload = "";
      fileDownload = $(".cd_gravity_download_file input").val();
      $(document).on("gform_confirmation_loaded", function () {
        if (fileDownload) {
          if (fileDownload !== undefined) {
            const link = document.createElement("a");
            link.href = fileDownload;
            link.download = fileDownload.substr(
              fileDownload.lastIndexOf("/") + 1
            );
            link.click();
          }
        }
      });
    }

    function addDataLayerFormIdVariableForGtm() {
      const { key } = gfApiKeys;
      const { secret } = gfApiKeys;

      const xhr = new XMLHttpRequest();
      xhr.withCredentials = true;

      let formName;
      let formId;

      xhr.addEventListener("readystatechange", function () {
        if (this.readyState === 4) {
          const formData = JSON.parse(this.responseText);
          formName = formData.title;
          formId = formData.id;

          window.dataLayer = window.dataLayer || [];
          window.dataLayer.push({
            event: "formSubmission",
            formID: formId,
            formName,
          });
        }
      });

      const siteUrl = `${window.location.protocol}//${window.location.hostname}`;

      $(document).bind("gform_confirmation_loaded", function (event, formID) {
        const formRestUrl = `${siteUrl}/wp-json/gf/v2/forms/${formID}`;
        xhr.open("GET", formRestUrl);

        xhr.setRequestHeader(
          "Authorization",
          `Basic ${btoa(`${key}:${secret}`)}`
        );
        xhr.send();
      });
    }

    // File Download with Gravity Forms
    if ($(".cd_gravity_download_file input").length > 0) {
      downloadFile();
    }

    if ($(".gform_wrapper").length > 0) {
      addDataLayerFormIdVariableForGtm();
    }

    // Add mandatory text under heading of Footnotes plugin
    if ($(".footnote_container_prepare").length > 0) {
      const textToAppendReferences =
        "<p>All Company Debt insolvency content is written by our licensed insolvency practitioners.</p>" +
        "<p>The primary sources for this article are listed below, including the relevant laws, and acts which procide their legal basis.</p>" +
        "<p>You can learn more about the standards we follow in producing accurate, unbiased content in our editorial policy here.</p>";
      $(".footnote_container_prepare").append(textToAppendReferences);
    }

    if(window.outerWidth < 769) {
      const $backToTop = $('#back-to-top');

      $backToTop.on('click', function(e){
        e.preventDefault();

        $("html, body").animate({ scrollTop: 0 });
      })
    }
  });
})(jQuery);

setTimeout(function(){
  if ( window.reviewsBadgeRibbon ) {
    reviewsBadgeRibbon("badge-ribbon-1", {
      store: "www.companydebt.com",
      size: "medium",

    });
  }
  if ( window.carouselInlineWidget ) {
    new carouselInlineWidget('reviewsio-carousel-widget', {
      store: 'www.companydebt.com',
      sku: '',
      lang: 'en',
      carousel_type: 'default',
      styles_carousel: 'CarouselWidget--sideHeader--withcards',
      options:{
          general:{
              review_type: 'company',
              min_reviews: '1',
              max_reviews: '10',
              address_format: 'CITY, COUNTRY',
              enable_auto_scroll: 10000,
          },
          header:{
              enable_overall_stars: true,
              rating_decimal_places: 2,
          },
          reviews: {
              enable_customer_name: true,
              enable_customer_location: true,
              enable_verified_badge: true,
              enable_subscriber_badge: true,
              enable_recommends_badge: true,
              enable_photos: true,
              enable_videos: true,
              enable_review_date: true,
              disable_same_customer: true,
              min_review_percent: 4,
              third_party_source: true,
              hide_empty_reviews: true,
              enable_product_name: true,
              tags: "",
              branch: "",
              enable_branch_name: false,
          },
          popups: {
              enable_review_popups:  true,
              enable_helpful_buttons: true,
              enable_helpful_count: true,
              enable_share_buttons: true,
          },
      },
      translations: {
        verified_customer:  "Verified Customer",
      },
      styles:{
        '--base-font-size': '16px',
        '--base-maxwidth':'100%',
        '--reviewsio-logo-style':'var(--logo-inverted)',
        '--common-star-color':'#ff711e',
        '--common-star-disabled-color':'rgba(0,0,0,0.25)',
        '--medium-star-size':'22px',
        '--small-star-size':'19px',
        '--x-small-star-size':'16px',
        '--x-small-star-display':'inline-flex',
        '--header-order':'1',
        '--header-width':'280px',
        '--header-bg-start-color':'#002857',
        '--header-bg-end-color':'#002857',
        '--header-gradient-direction':'135deg',
        '--header-padding':'1.5em',
        '--header-border-width':'0px',
        '--header-border-color':'rgba(0,0,0,0.1)',
        '--header-border-radius':'0px',
        '--header-shadow-size':'10px',
        '--header-shadow-color':'rgba(0, 0, 0, 0.05)',
        '--header-star-color':'#FF711E',
        '--header-disabled-star-color':'#002857',
        '--header-heading-text-color':'#ffffff',
        '--header-heading-font-size':'inherit',
        '--header-heading-font-weight':'inherit',
        '--header-heading-line-height':'inherit',
        '--header-heading-text-transform':'inherit',
        '--header-subheading-text-color':'#ffffff',
        '--header-subheading-font-size':'inherit',
        '--header-subheading-font-weight':'300',
        '--header-subheading-line-height':'inherit',
        '--header-subheading-text-transform':'inherit',
        '--item-maximum-columns':'5',
        '--item-background-start-color':'#ffffff',
        '--item-background-end-color':'#ffffff',
        '--item-gradient-direction':'135deg',
        '--item-padding':'1.5em',
        '--item-border-width':'0px',
        '--item-border-color':'rgba(0,0,0,0.1)',
        '--item-border-radius':'0px',
        '--item-shadow-size':'10px',
        '--item-shadow-color':'rgba(0,0,0,0.05)',
        '--heading-text-color':' #0E1311',
        '--heading-text-font-weight':' 600',
        '--heading-text-font-family':' inherit',
        '--heading-text-line-height':' 1.4',
        '--heading-text-letter-spacing':'0',
        '--heading-text-transform':'none',
        '--body-text-color':' #0E1311',
        '--body-text-font-weight':'400',
        '--body-text-font-family':' inherit',
        '--body-text-line-height':' 1.4',
        '--body-text-letter-spacing':'0',
        '--body-text-transform':'none',
        '--scroll-button-icon-color':'#0E1311',
        '--scroll-button-icon-size':'24px',
        '--scroll-button-bg-color':'transparent',
        '--scroll-button-border-width':'0px',
        '--scroll-button-border-color':'rgba(0,0,0,0.1)',
        '--scroll-button-border-radius':'60px',
        '--scroll-button-shadow-size':'0px',
        '--scroll-button-shadow_color':'rgba(0,0,0,0.1)',
        '--scroll-button-horizontal-position':'3px',
        '--scroll-button-vertical-position':'0px',
        '--badge-icon-color':'#0E1311',
        '--badge-icon-font-size':'15px',
        '--badge-text-color':'#0E1311',
        '--badge-text-font-size':'inherit',
        '--badge-text-letter-spacing':'inherit',
        '--badge-text-transform':'inherit',
        '--author-font-size':'inherit',
        '--author-font-weight':'inherit',
        '--author-text-transform':'inherit',
        '--photo-video-thumbnail-size':'60px',
        '--photo-video-thumbnail-border-radius':'0px',
        '--popup-backdrop-color':'rgba(0,0,0,0.75)',
        '--popup-color':'#ffffff',
        '--popup-star_color':'inherit',
        '--popup-disabled-star_color':'inherit',
        '--popup-heading-text-color':'inherit',
        '--popup-body-text_color':'inherit',
        '--popup-badge-icon_color':'inherit',
        '--popup-badge-icon-font-size':'19px',
        '--popup-badge-text_color':'inherit',
        '--popup-badge-text-font-size':'14px',
        '--popup-border-width':'0px',
        '--popup-border-color':'rgba(0,0,0,0.1)',
        '--popup-border-radius':'0px',
        '--popup-shadow-size':'0px',
        '--popup-shadow_color':'rgba(0,0,0,0.1)',
        '--popup-icon_color':'#0E1311',
        '--tooltip-bg_color':'#0E1311',
        '--tooltip-text_color':'#ffffff',
      },
    });
  }
},1000);