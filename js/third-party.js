// Third-party loader + product analytics.
//
// Why this file exists: analytics and ad scripts used to sit in <head> and
// inline in <body>, where they competed with the tool itself for the main
// thread on every page load (mobile Lighthouse: LCP 6.4s, 2.2s of it pure
// render delay). None of them are needed to use a tool, so they now load
// after the page is interactive: analytics on idle after `load`, ad slots
// only when they scroll near the viewport.
//
// gtag() itself is defined inline in head-common.html, so events fired
// before gtag.js arrives are queued in dataLayer and sent once it loads.
(function () {
  var GA_ID = "G-695Y7WZTCT";
  var CLARITY_ID = "xrd6nlberg";
  var SOCIAL_BAR_SRC = "https://pl30775974.effectivecpmnetwork.com/45/46/bd/4546bd692b42ca660c03716e49f94071.js";

  function loadScript(src, attrs, parent) {
    return new Promise(function (resolve) {
      var s = document.createElement("script");
      s.src = src;
      s.async = true;
      if (attrs) Object.keys(attrs).forEach(function (k) { s.setAttribute(k, attrs[k]); });
      s.onload = s.onerror = function () { resolve(); };
      (parent || document.head).appendChild(s);
    });
  }

  function whenIdle(fn, timeout) {
    if ("requestIdleCallback" in window) requestIdleCallback(fn, { timeout: timeout || 3000 });
    else setTimeout(fn, 1200);
  }

  function afterLoad(fn) {
    if (document.readyState === "complete") fn();
    else window.addEventListener("load", fn, { once: true });
  }

  // ---- analytics -------------------------------------------------------
  function loadAnalytics() {
    loadScript("https://www.googletagmanager.com/gtag/js?id=" + GA_ID);
    window.clarity = window.clarity || function () { (window.clarity.q = window.clarity.q || []).push(arguments); };
    loadScript("https://www.clarity.ms/tag/" + CLARITY_ID);
  }

  // ---- ads -------------------------------------------------------------
  // Banner units share one global (`atOptions`), so they must be injected
  // strictly one at a time: set the global, load invoke.js, wait, next.
  var adQueue = Promise.resolve();
  function fillSlot(slot) {
    var kind = slot.getAttribute("data-ad");
    if (kind === "banner") {
      var key = slot.getAttribute("data-key");
      adQueue = adQueue.then(function () {
        window.atOptions = {
          key: key,
          format: "iframe",
          height: parseInt(slot.getAttribute("data-h"), 10),
          width: parseInt(slot.getAttribute("data-w"), 10),
          params: {}
        };
        return loadScript("https://www.highperformanceformat.com/" + key + "/invoke.js", null, slot);
      });
    } else if (kind === "native") {
      loadScript(slot.getAttribute("data-src"), { "data-cfasync": "false" }, slot);
    }
  }

  function loadAds() {
    var slots = document.querySelectorAll(".ad-slot[data-ad]");
    if (slots.length) {
      if ("IntersectionObserver" in window) {
        var io = new IntersectionObserver(function (entries) {
          entries.forEach(function (e) {
            if (!e.isIntersecting) return;
            io.unobserve(e.target);
            fillSlot(e.target);
          });
        }, { rootMargin: "400px 0px" });
        slots.forEach(function (s) { io.observe(s); });
      } else {
        slots.forEach(fillSlot);
      }
      // Social Bar only on pages that already carry ad slots (tool pages).
      // The homepage, About, Privacy, Terms and Contact stay ad-free.
      loadScript(SOCIAL_BAR_SRC, null, document.body);
    }
  }

  afterLoad(function () {
    whenIdle(loadAnalytics);
    whenIdle(loadAds, 5000);
  });

  // ---- product events --------------------------------------------------
  // A deliberately small taxonomy. Nothing here contains user content:
  // only which tool, and which kind of action.
  //   tool_start     first real interaction with a tool (activation)
  //   tool_output    a result was downloaded or copied (core value)
  //   search_open    command palette opened
  //   search_select  a tool picked from the palette
  //   lang_switch    language changed
  //   support_click  Ko-fi link clicked
  //   pwa_install    app installed
  var tool = location.pathname.replace(/^\/(es|zh|ar|hi|ru|ja)\//, "/").replace(/^\//, "").replace(/\.html$/, "") || "home";
  function track(name, params) {
    try {
      var p = { tool: tool };
      if (params) Object.keys(params).forEach(function (k) { p[k] = params[k]; });
      window.gtag("event", name, p);
    } catch (e) {}
  }
  window.noritoTrack = track;

  var started = false;
  function start(how) {
    if (started) return;
    started = true;
    track("tool_start", { method: how });
  }
  function inTool(el) {
    return el && el.closest && el.closest("main") && !el.closest(".cmdk-overlay, header, footer, .faq");
  }
  document.addEventListener("input", function (e) { if (inTool(e.target)) start("input"); }, true);
  document.addEventListener("change", function (e) { if (inTool(e.target)) start(e.target.type === "file" ? "file" : "change"); }, true);
  document.addEventListener("drop", function (e) { if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length) start("drop"); }, true);
  document.addEventListener("paste", function (e) { if (inTool(e.target)) start("paste"); }, true);

  var lastOutput = 0;
  function output(method) {
    var now = Date.now();
    if (now - lastOutput < 800) return; // one batch download = one event
    lastOutput = now;
    start("output");
    track("tool_output", { method: method });
  }
  var anchorClick = HTMLAnchorElement.prototype.click;
  HTMLAnchorElement.prototype.click = function () {
    if (this.hasAttribute("download")) output("download");
    return anchorClick.apply(this, arguments);
  };
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a");
    if (!a) return;
    if (a.hasAttribute("download") && e.isTrusted) output("download");
    else if (/ko-fi\.com/.test(a.href)) track("support_click");
    else if (a.classList.contains("cmdk-item")) track("search_select", { target: a.getAttribute("href") });
    else if (a.closest(".recent-row")) track("recent_click", { target: a.getAttribute("href") });
  }, true);
  if (navigator.clipboard && navigator.clipboard.writeText) {
    var write = navigator.clipboard.writeText.bind(navigator.clipboard);
    navigator.clipboard.writeText = function (t) { output("copy"); return write(t); };
  }
  document.addEventListener("click", function (e) {
    if (e.target.closest && e.target.closest(".js-cmdk-trigger, #searchTrigger")) track("search_open");
  }, true);
  window.addEventListener("appinstalled", function () { track("pwa_install"); });
  window.addEventListener("error", function (e) {
    if (e.filename && e.filename.indexOf(location.origin) === 0) {
      track("js_error", { file: e.filename.replace(location.origin, ""), line: e.lineno });
    }
  });
})();
