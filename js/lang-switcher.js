// Shared language-switcher behavior, identical on all 44 pages (11 tools x
// 4 languages). Builds the dropdown links itself from the current page's
// own URL, entirely relative to the file structure (never the absolute
// domain used in the <hreflang> SEO tags), so it works identically whether
// the site is opened as local files, served from localhost, or deployed to
// any real domain later. Each language is shown in its own native script so
// a visitor can find their language without being able to read the current
// page's language at all.
(function () {
  var NATIVE_NAMES = {
    en: "English",
    es: "Español",
    zh: "中文",
    ar: "العربية",
    hi: "हिन्दी",
  };
  var SHORT_LABELS = {
    en: "EN",
    es: "ES",
    zh: "中",
    ar: "AR",
    hi: "HI",
  };
  var LANG_ORDER = ["en", "es", "zh", "ar", "hi"];

  var root = document.getElementById("langSwitch");
  if (!root) return;
  var panel = document.getElementById("langSwitchPanel");
  var currentLabel = document.getElementById("langSwitchCurrent");
  var btn = root.querySelector(".lang-switch-btn");

  var currentLang = document.documentElement.lang === "zh-Hans" ? "zh" : (document.documentElement.lang || "en");

  // Figure out the current filename (e.g. "compress-image.html"), defaulting
  // to "index.html" for a directory-root URL such as ".../es/" or "/".
  var segments = location.pathname.split("/").filter(Boolean);
  var last = segments[segments.length - 1] || "";
  var filename = /\.html$/i.test(last) ? last : "index.html";

  // Build a path relative to the current page for each target language.
  // Root pages (en) live at "/", localized pages live one level down at
  // "/es/", "/zh/", "/ar/" - so the relative link only ever needs at most
  // one "../" to leave a language folder before entering another.
  function relativeHref(targetLang) {
    if (targetLang === currentLang) return filename;
    if (targetLang === "en") {
      return currentLang === "en" ? filename : "../" + filename;
    }
    return (currentLang === "en" ? "" : "../") + targetLang + "/" + filename;
  }

  LANG_ORDER.forEach(function (code) {
    var a = document.createElement("a");
    a.href = relativeHref(code);
    a.lang = code;
    a.textContent = NATIVE_NAMES[code];
    if (code === currentLang) a.classList.add("active");
    panel.appendChild(a);
  });

  if (currentLabel) currentLabel.textContent = SHORT_LABELS[currentLang] || "EN";

  btn.addEventListener("click", function (e) {
    e.stopPropagation();
    root.classList.toggle("open");
  });
  document.addEventListener("click", function () {
    root.classList.remove("open");
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") root.classList.remove("open");
  });
})();
