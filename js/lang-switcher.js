// Shared language-switcher behavior, identical on every translated page
// across all 6 locales (es/zh/ar/hi/ru/ja). Builds the dropdown links itself
// from the current page's
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

  // Work out where the current page sits relative to its own language root,
  // supporting pages nested in category subdirectories (pdf/, seo/,
  // design/, blog/, compare/, images/, developer/, text/, utilities/) as
  // well as flat root-level pages. A trailing-slash / directory URL (e.g.
  // ".../pdf/" or "/es/") is treated as that directory's index.html.
  var segments = location.pathname.split("/").filter(Boolean);
  var lastSeg = segments[segments.length - 1] || "";
  var isFile = /\.html$/i.test(lastSeg);
  var filename = isFile ? lastSeg : "index.html";

  // Directory segments from the site root, including the locale segment
  // (e.g. "es") when present. Used to count how many "../" are needed to
  // climb back up to the site root from the current page.
  var dirSegments = isFile ? segments.slice(0, -1) : segments.slice();
  var upCount = dirSegments.length;

  // Same directory segments but relative to the current page's own
  // language root (i.e. with the leading locale segment dropped for
  // non-English pages), used to build the page's path key for lookups.
  var relDirSegments = currentLang === "en" ? dirSegments : dirSegments.slice(1);
  var pagePath = relDirSegments.concat([filename]).join("/");

  // Only these pages (identified by their path relative to a language
  // root, e.g. "index.html" or "pdf/merge-pdf.html") actually exist in
  // every language. Anything else only exists in English, so linking to
  // "es/that-page.html" would 404. Keep this in sync with the page lists
  // under /es/, /zh/, /ar/, /hi/, /ru/, /ja/. Generated from the actual file
  // tree (every EN page that has all 6 locale counterparts on disk) rather
  // than hand-maintained, since hand-maintaining this list is exactly what
  // let it silently drift out of sync with 40+ real translated pages before.
  var TRANSLATABLE_PAGES = [
    "about.html", "base64-encoder.html", "blog/client-side-vs-server-side-tools.html", "blog/how-password-entropy-works.html",
    "blog/how-to-merge-pdfs-for-free.html", "blog/image-compression-without-losing-quality.html", "blog/image-format-guide-2026.html", "blog/index.html",
    "blog/jpg-vs-png-vs-webp.html", "blog/pdf-compression-explained.html", "blog/wcag-contrast-checking-guide.html", "blog/what-is-a-uuid.html",
    "case-converter.html", "changelog.html", "character-counter.html", "compare/index.html",
    "compare/norito-vs-ilovepdf.html", "compare/norito-vs-smallpdf.html", "compare/norito-vs-tinypng.html", "compress-image.html",
    "contact.html", "cron-expression-parser.html", "crop-image.html", "csv-to-json.html",
    "csv-viewer.html", "design/border-radius-generator.html", "design/box-shadow-generator.html", "design/color-converter.html",
    "design/color-palette-extractor.html", "design/contrast-checker.html", "design/css-gradient-generator.html", "design/favicon-generator.html",
    "design/index.html", "developer/index.html", "find-and-replace.html", "hash-generator.html",
    "how-it-works.html", "html-entity-encoder.html", "image-converter.html", "images/index.html",
    "index.html", "jpg-to-png-converter.html", "json-diff.html", "json-formatter.html",
    "jwt-decoder.html", "limited-text-generator.html", "lorem-ipsum-generator.html", "markdown-editor.html",
    "number-base-converter.html", "password-generator.html", "pdf/add-page-numbers.html", "pdf/add-watermark.html",
    "pdf/compress-pdf-for-email.html", "pdf/compress-pdf.html", "pdf/extract-text.html", "pdf/index.html",
    "pdf/jpg-png-to-pdf.html", "pdf/merge-pdf.html", "pdf/organize-pdf.html", "pdf/pdf-to-image.html",
    "pdf/rotate-pdf.html", "pdf/sign-pdf.html", "pdf/split-pdf.html", "placeholder-generator.html",
    "privacy.html", "qr-code-generator.html", "regex-tester.html", "remove-background.html",
    "remove-duplicate-lines.html", "remove-image-background-free.html", "remove-metadata.html", "resize-image-for-instagram.html",
    "resize-image.html", "seo-slug-generator.html", "seo/index.html", "seo/meta-tag-generator.html",
    "seo/robots-txt-generator.html", "seo/sitemap-generator.html", "seo/utm-builder.html", "sort-lines.html",
    "terms.html", "test-file-generator.html", "text-diff.html", "text/index.html",
    "timestamp-converter.html", "url-encoder-decoder.html", "utilities/index.html", "uuid-generator.html",
    "watermark-image.html", "word-counter.html", "yaml-to-json-converter.html"
  ];
  var hasTranslation = TRANSLATABLE_PAGES.indexOf(pagePath) !== -1;

  // Build a path relative to the current page for each target language by
  // climbing up to the site root (upCount "../" segments) and then
  // descending into the target language's copy of the same page path. When
  // the current page has no translation, fall back to that language's
  // homepage instead of constructing a link that 404s.
  function relativeHref(targetLang) {
    if (targetLang === currentLang) return filename;
    var upPrefix = new Array(upCount + 1).join("../");
    var targetFromRoot = targetLang === "en"
      ? (hasTranslation ? pagePath : "index.html")
      : (hasTranslation ? targetLang + "/" + pagePath : targetLang + "/index.html");
    return upPrefix + targetFromRoot;
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
