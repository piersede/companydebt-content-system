<?php
/**
 * Plugin Name: CD Pub Closures Data Hub
 * Description: Front-end behaviour for the /articles/pub-closures-in-the-uk/ data-hub
 *              redesign. Enqueues Source Serif 4, injects the dependency-free SVG chart
 *              engine + chart config + copy-citation + scroll-spy, and emits Article
 *              JSON-LD. All of this is stripped from post content by KSES, so it lives
 *              here. Gated to the single post by slug so it loads nowhere else.
 * Version:     1.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * True only on the pub-closures post. It is a post (is_single), not a page.
 */
function cd_pubhub_is_target() {
    if ( ! is_singular( 'post' ) ) {
        return false;
    }
    return 'pub-closures-in-the-uk' === get_post_field( 'post_name', get_queried_object_id() );
}

add_action( 'wp_enqueue_scripts', function () {
    if ( ! cd_pubhub_is_target() ) {
        return;
    }
    wp_enqueue_style(
        'cd-source-serif-4',
        'https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600;8..60,700&display=swap',
        array(),
        null
    );
}, 5 );

add_action( 'wp_footer', function () {
    if ( ! cd_pubhub_is_target() ) {
        return;
    }
    ?>
<script id="cd-pub-hub-js">
/* ============================================================
   Pub Closures Data Hub — lightweight SVG chart engine
   No dependencies. Builds charts as SVG-markup strings (so they
   render in true browsers AND html-to-image based capture /
   export). Sized to container, redraws on resize and on tweak
   changes, reading colours from CSS custom properties.
   ============================================================ */
(function () {
  "use strict";

  var registry = []; // { host, cfg }

  function css(varName, fallback) {
    var root = document.querySelector(".cd-pub-hub") || document.documentElement;
    var v = getComputedStyle(root).getPropertyValue(varName).trim();
    return v || fallback;
  }
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function fmt(n) { return n.toLocaleString("en-GB"); }
  function niceMax(v) {
    if (v <= 0) return 1;
    var pow = Math.pow(10, Math.floor(Math.log10(v)));
    var f = v / pow;
    var nf = f <= 1 ? 1 : f <= 2 ? 2 : f <= 2.5 ? 2.5 : f <= 5 ? 5 : 10;
    return nf * pow;
  }
  function T(x, y, s, opts) {
    opts = opts || {};
    return '<text x="' + x + '" y="' + y + '"' +
      (opts.anchor ? ' text-anchor="' + opts.anchor + '"' : "") +
      ' font-size="' + (opts.size || 12) + '"' +
      (opts.weight ? ' font-weight="' + opts.weight + '"' : "") +
      ' fill="' + (opts.fill || "#000") + '"' +
      (opts.opacity != null ? ' opacity="' + opts.opacity + '"' : "") +
      ' font-family="inherit">' + esc(s) + "</text>";
  }
  function svgWrap(W, H, aria, inner) {
    return '<svg viewBox="0 0 ' + W + " " + H + '" width="' + W + '" height="' + H +
      '" role="img" aria-label="' + esc(aria || "chart") + '">' + inner + "</svg>";
  }

  // ---- AREA / LINE ---------------------------------------------------
  function buildArea(host, cfg) {
    var W = host.clientWidth || 680, H = cfg.height || 320;
    var padL = 58, padR = 24, padT = 30, padB = 46;
    var ink = css("--cd-figure", "#3a2716"), accent = css("--cd-accent", "#a1421a");
    var muted = css("--cd-muted", "#857567"), line = css("--cd-line", "#e8ddce");
    var mode = (document.querySelector(".cd-pub-hub").getAttribute("data-chart")) || "area";
    var data = cfg.data, n = data.length;
    var maxV = cfg.max || niceMax(Math.max.apply(null, data.map(function (d) { return d.v; })));
    var minV = cfg.min != null ? cfg.min : 0;
    var plotW = W - padL - padR, plotH = H - padT - padB;
    var useXV = data.every(function (d) { return typeof d.xv === "number"; });
    var xvMin = useXV ? Math.min.apply(null, data.map(function (d) { return d.xv; })) : 0;
    var xvMax = useXV ? Math.max.apply(null, data.map(function (d) { return d.xv; })) : 1;
    var x = function (i) {
      if (useXV) return padL + (xvMax === xvMin ? plotW / 2 : ((data[i].xv - xvMin) / (xvMax - xvMin)) * plotW);
      return padL + (n === 1 ? plotW / 2 : (plotW * i) / (n - 1));
    };
    var y = function (v) { return padT + plotH - ((v - minV) / (maxV - minV)) * plotH; };

    var s = "";
    var ticks = cfg.ticks || 4;
    for (var t = 0; t <= ticks; t++) {
      var gv = minV + ((maxV - minV) * t) / ticks, gy = y(gv);
      s += '<line x1="' + padL + '" y1="' + gy + '" x2="' + (W - padR) + '" y2="' + gy + '" stroke="' + line + '" stroke-width="1"/>';
      s += T(padL - 10, gy + 4, cfg.yfmt ? cfg.yfmt(gv) : fmt(Math.round(gv)), { anchor: "end", size: 13, fill: muted });
    }
    var dLine = "";
    data.forEach(function (d, i) { dLine += (i === 0 ? "M" : "L") + x(i) + " " + y(d.v); });
    if (mode !== "line") {
      var gid = "pcg-" + Math.random().toString(36).slice(2, 8);
      var dArea = dLine + "L" + x(n - 1) + " " + (padT + plotH) + "L" + x(0) + " " + (padT + plotH) + "Z";
      s = '<defs><linearGradient id="' + gid + '" x1="0" y1="0" x2="0" y2="1">' +
        '<stop offset="0%" stop-color="' + accent + '" stop-opacity="0.20"/>' +
        '<stop offset="100%" stop-color="' + accent + '" stop-opacity="0.02"/></linearGradient></defs>' + s;
      s += '<path d="' + dArea + '" fill="url(#' + gid + ')"/>';
    }
    s += '<path d="' + dLine + '" fill="none" stroke="' + accent + '" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>';
    data.forEach(function (d, i) {
      s += '<circle cx="' + x(i) + '" cy="' + y(d.v) + '" r="4.5" fill="#fff" stroke="' + accent + '" stroke-width="2.5"/>';
      s += T(x(i), y(d.v) - 14, d.label != null ? d.label : fmt(d.v),
        { anchor: i === 0 ? "start" : i === n - 1 ? "end" : "middle", size: 13, weight: 700, fill: ink });
      s += T(x(i), H - 18, d.x, { anchor: "middle", size: 13, fill: muted });
    });
    return svgWrap(W, H, cfg.aria || cfg.title, s);
  }

  // ---- HORIZONTAL BARS ----------------------------------------------
  function buildHBar(host, cfg) {
    var W = host.clientWidth || 680, data = cfg.data;
    var rowH = cfg.rowH || 46, gap = cfg.gap || 14, padT = 6, padB = 6;
    var H = padT + padB + data.length * rowH + (data.length - 1) * gap;
    var accent = css("--cd-accent", "#a1421a"), ink = css("--cd-figure", "#3a2716");
    var track = css("--cd-line-soft", "#f1e9dc");
    var maxV = cfg.max || niceMax(Math.max.apply(null, data.map(function (d) { return d.v; })));
    var s = "";
    data.forEach(function (d, i) {
      var top = padT + i * (rowH + gap), barTop = top + 22, bh = rowH - 22;
      s += T(0, top + 14, d.x, { size: 13, weight: 600, fill: ink });
      s += '<rect x="0" y="' + barTop + '" width="' + W + '" height="' + bh + '" rx="5" fill="' + track + '"/>';
      var w = Math.max(2, (d.v / maxV) * W);
      var fill = d.accent ? accent : ink;
      s += '<rect x="0" y="' + barTop + '" width="' + w + '" height="' + bh + '" rx="5" fill="' + fill + '" opacity="' + (d.accent ? 1 : 0.82) + '"/>';
      var vlabel = d.label != null ? d.label : fmt(d.v), inside = w > 70;
      s += T(inside ? w - 10 : w + 10, barTop + bh / 2 + 4, vlabel,
        { anchor: inside ? "end" : "start", size: 13, weight: 700, fill: inside ? "#fff" : ink });
    });
    return svgWrap(W, H, cfg.aria || cfg.title, s);
  }

  // ---- VERTICAL BARS ------------------------------------------------
  function buildVBar(host, cfg) {
    var W = host.clientWidth || 680, H = cfg.height || 320;
    var padL = 56, padR = 20, padT = 30, padB = 52;
    var ink = css("--cd-figure", "#3a2716"), accent = css("--cd-accent", "#a1421a");
    var muted = css("--cd-muted", "#857567"), line = css("--cd-line", "#e8ddce");
    var data = cfg.data, n = data.length;
    var maxV = cfg.max || niceMax(Math.max.apply(null, data.map(function (d) { return d.v; })));
    var plotW = W - padL - padR, plotH = H - padT - padB;
    var y = function (v) { return padT + plotH - (v / maxV) * plotH; };
    var s = "";
    var ticks = cfg.ticks || 4;
    for (var t = 0; t <= ticks; t++) {
      var gv = (maxV * t) / ticks, gy = y(gv);
      s += '<line x1="' + padL + '" y1="' + gy + '" x2="' + (W - padR) + '" y2="' + gy + '" stroke="' + line + '" stroke-width="1"/>';
      s += T(padL - 10, gy + 4, cfg.yfmt ? cfg.yfmt(gv) : fmt(Math.round(gv)), { anchor: "end", size: 13, fill: muted });
    }
    var slot = plotW / n, bw = Math.min(cfg.barW || 64, slot * 0.5);
    data.forEach(function (d, i) {
      var cx = padL + slot * (i + 0.5), bx = cx - bw / 2, by = y(d.v);
      var fill = d.accent ? accent : ink;
      s += '<rect x="' + bx + '" y="' + by + '" width="' + bw + '" height="' + (padT + plotH - by) + '" rx="6" fill="' + fill + '" opacity="' + (d.accent ? 1 : 0.8) + '"/>';
      s += T(cx, by - 10, d.label != null ? d.label : fmt(d.v), { anchor: "middle", size: 13, weight: 700, fill: ink });
      s += T(cx, H - 26, d.x, { anchor: "middle", size: 13, fill: muted });
      if (d.sub) s += T(cx, H - 10, d.sub, { anchor: "middle", size: 13, fill: muted, opacity: 0.8 });
    });
    return svgWrap(W, H, cfg.aria || cfg.title, s);
  }

  var BUILDERS = { area: buildArea, line: buildArea, hbar: buildHBar, vbar: buildVBar };

  function draw(item) { item.host.innerHTML = BUILDERS[item.cfg.type](item.host, item.cfg); }
  function register(host, cfg) { var item = { host: host, cfg: cfg }; registry.push(item); draw(item); }
  function redrawAll() { registry.forEach(draw); }

  var rt;
  window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(redrawAll, 120); });
  window.CDCharts = { register: register, redrawAll: redrawAll };
})();

/* ---- chart config + cite + reveal ---- */
(function () {
  var C = window.CDCharts;
  function reg(id, cfg) { var h = document.getElementById(id); if (h) C.register(h, cfg); }

  reg("chart-decline", {
    type: "area", height: 320, min: 0, max: 65000, ticks: 4,
    yfmt: function (v) { return v === 0 ? "0" : (Math.round(v / 1000)) + "k"; },
    data: [
      { x: "2000", xv: 2000, v: 60800, label: "60,800" },
      { x: "2010", xv: 2010, v: 55400, label: "55,400" },
      { x: "2024", xv: 2024, v: 45000, label: "~45,000" }
    ]
  });

  reg("chart-quarter", {
    type: "hbar", max: 175, rowH: 72, gap: 24,
    data: [
      { x: "Q1 2025", v: 128, label: "128 closures" },
      { x: "Q1 2026", v: 161, label: "161 closures · almost two a day", accent: true }
    ]
  });

  reg("chart-rate", {
    type: "hbar", max: 340, rowH: 72, gap: 24,
    data: [
      { x: "2023 (peak)", v: 314, label: "314 per 10,000" },
      { x: "2025", v: 268, label: "268 per 10,000", accent: true }
    ]
  });

  reg("chart-churn", {
    type: "hbar", max: 32000, rowH: 72, gap: 24,
    data: [
      { x: "New businesses opened", v: 30360, label: "30,360" },
      { x: "Businesses closed", v: 26195, label: "26,195", accent: true }
    ]
  });

  reg("chart-challenges", {
    type: "hbar", max: 100, rowH: 48, gap: 16,
    data: [
      { x: "Any challenge", v: 83, label: "83%", accent: true },
      { x: "Cost of materials", v: 48, label: "48%" },
      { x: "Cost of labour", v: 48, label: "48%" },
      { x: "Economic uncertainty", v: 43, label: "43%" }
    ]
  });

  reg("chart-rates", {
    type: "hbar", max: 80, rowH: 48, gap: 16,
    data: [
      { x: "Pubs with a lodge", v: 70, label: "+70%", accent: true },
      { x: "Public houses / pub restaurants", v: 30, label: "+30%", accent: true },
      { x: "All property (average)", v: 19.4, label: "+19.4%" }
    ]
  });

  reg("chart-pint", {
    type: "vbar", height: 300, max: 520, ticks: 4, barW: 96,
    yfmt: function (v) { return Math.round(v) + "p"; },
    data: [
      { x: "2000", v: 200, label: "200p" },
      { x: "2024", v: 477, label: "477p", accent: true }
    ]
  });

  // citation copy
  var wrap = document.querySelector(".cd-cite");
  if (wrap) {
    var title = wrap.getAttribute("data-cite-title");
    var url = wrap.getAttribute("data-cite-url");
    var today = new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" });
    var payloads = {
      citation: "Company Debt (2026) '" + title + "'. Available at: " + url + " (Accessed: " + today + ").",
      embed: '<a href="' + url + '">' + title + '</a> — data from Company Debt'
    };
    var citEl = document.getElementById("citation");
    var embEl = document.getElementById("embed");
    if (citEl) citEl.textContent = payloads.citation;
    if (embEl) embEl.textContent = payloads.embed;
    wrap.querySelectorAll("[data-copy]").forEach(function (b) {
      var label = b.querySelector(".cd-cite__btnlabel");
      var original = label ? label.textContent : "";
      b.addEventListener("click", function () {
        var txt = payloads[b.getAttribute("data-copy")];
        if (!navigator.clipboard || !txt) return;
        navigator.clipboard.writeText(txt).then(function () {
          b.classList.add("is-copied");
          if (label) label.textContent = "Copied";
          setTimeout(function () { b.classList.remove("is-copied"); if (label) label.textContent = original; }, 2000);
        });
      });
    });
  }

  // reveal on scroll (progressive enhancement; safe fallback reveals everything)
  var hub = document.querySelector(".cd-pub-hub");
  var targets = [].slice.call(document.querySelectorAll(".cd-sec .cd-figure, .cd-sec .cd-trio, .cd-sec .cd-statrow"));
  if (hub && "IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    hub.classList.add("cd-js");
    targets.forEach(function (n) { n.classList.add("cd-reveal"); });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("cd-in"); io.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    targets.forEach(function (n) { io.observe(n); });
    // safety net: reveal anything still hidden shortly after load
    window.addEventListener("load", function () { setTimeout(function () { targets.forEach(function (n) { n.classList.add("cd-in"); }); }, 1800); });
  }
})();

/* ---- on-this-page scroll spy ---- */
(function () {
  var links = [].slice.call(document.querySelectorAll(".cd-toc a[data-target]"));
  if (!links.length) return;
  var heads = links.map(function (a) { return document.getElementById(a.getAttribute("data-target")); }).filter(Boolean);
  function spy() {
    var y = window.scrollY + 160;
    var active = heads[0];
    heads.forEach(function (h) { if (h.getBoundingClientRect().top + window.scrollY <= y) active = h; });
    links.forEach(function (a) { a.classList.toggle("is-active", a.getAttribute("data-target") === (active && active.id)); });
  }
  window.addEventListener("scroll", spy, { passive: true });
  window.addEventListener("resize", spy);
  spy();
})();
</script>
<?php
} );

add_action( 'wp_head', function () {
    if ( ! cd_pubhub_is_target() ) {
        return;
    }
    $url = get_permalink();
    $graph = array(
        '@context' => 'https://schema.org',
        '@type'    => 'Article',
        'headline' => "Pub Closures: What's Behind the Decline of British Pubs?",
        'about'    => 'UK pub closures, pub numbers, hospitality insolvency',
        'isAccessibleForFree' => true,
        'mainEntityOfPage' => $url,
        'url'      => $url,
        'author'   => array( '@type' => 'Organization', 'name' => 'Company Debt' ),
        'reviewedBy' => array( '@type' => 'Person', 'name' => 'Chris Andersen', 'jobTitle' => 'Licensed Insolvency Practitioner' ),
        'publisher' => array( '@type' => 'Organization', 'name' => 'Company Debt' ),
    );
    echo '<script type="application/ld+json" id="cd-pub-hub-schema">'
        . wp_json_encode( $graph, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE )
        . '</script>' . "\n";
}, 30 );
