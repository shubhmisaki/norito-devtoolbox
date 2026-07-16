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
    ru: "Русский",
    ja: "日本語",
  };
  var SHORT_LABELS = {
    en: "EN",
    es: "ES",
    zh: "中",
    ar: "AR",
    hi: "HI",
    ru: "RU",
    ja: "JA",
  };
  var LANG_ORDER = ["en", "es", "zh", "ar", "hi", "ru", "ja"];

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

  // Only these pages actually exist in every language. Everything else
  // (the PDF suite, most newer tools, category hub pages, blog, compare,
  // how-it-works, and anything inside a subdirectory) only exists in
  // English, so linking to "es/that-page.html" would 404. Keep this in
  // sync with the page lists in /es/, /zh/, /ar/, /hi/.
  var TRANSLATABLE_PAGES = [
    "index.html", "compress-image.html", "json-formatter.html", "limited-text-generator.html",
    "markdown-editor.html", "password-generator.html", "placeholder-generator.html", "privacy.html",
    "qr-code-generator.html", "remove-background.html", "seo-slug-generator.html", "test-file-generator.html"
  ];

  // English root pages nested inside a category folder (pdf/, seo/, etc.)
  // have more than one path segment; localized pages have at most two
  // (the language folder plus the filename). Either way, more segments
  // than that means we're on a page with no counterpart in other languages.
  var inSubdirectory = currentLang === "en" ? segments.length > 1 : segments.length > 2;
  var hasTranslation = !inSubdirectory && TRANSLATABLE_PAGES.indexOf(filename) !== -1;

  // Build a path relative to the current page for each target language.
  // Root pages (en) live at "/", localized pages live one level down at
  // "/es/", "/zh/", "/ar/" - so the relative link only ever needs at most
  // one "../" to leave a language folder before entering another. When the
  // current page has no translation, fall back to that language's homepage
  // instead of constructing a link that 404s.
  function relativeHref(targetLang) {
    if (targetLang === currentLang) return filename;
    if (targetLang === "en") {
      if (currentLang === "en") return filename;
      return hasTranslation ? "../" + filename : "../index.html";
    }
    var prefix = currentLang === "en" ? "" : "../";
    return hasTranslation ? prefix + targetLang + "/" + filename : prefix + targetLang + "/index.html";
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
