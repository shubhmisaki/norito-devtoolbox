(function () {
  var STORAGE_KEY = "norito:theme";

  function swapLogos(theme) {
    var imgs = document.querySelectorAll("img.logo-word");
    for (var i = 0; i < imgs.length; i++) {
      var img = imgs[i];
      var isDark = theme === "dark";
      var lightSrc = img.getAttribute("data-light-src") || img.getAttribute("src");
      if (!img.getAttribute("data-light-src")) img.setAttribute("data-light-src", lightSrc);
      if (isDark) {
        img.setAttribute("src", lightSrc.replace("norito-wordmark.svg", "norito-wordmark-dark.svg"));
      } else {
        img.setAttribute("src", lightSrc);
      }
    }
  }

  function setTheme(theme, persist) {
    document.documentElement.setAttribute("data-theme", theme);
    if (persist) {
      try { localStorage.setItem(STORAGE_KEY, theme); } catch (e) {}
    }
    swapLogos(theme);
  }

  // The inline anti-flash snippet in <head> already set data-theme before
  // paint if the user had previously picked dark mode, this just syncs the
  // logo swap (which needs the DOM to exist) and wires up the toggle button.
  var current = document.documentElement.getAttribute("data-theme") || "light";
  swapLogos(current);

  var buttons = document.querySelectorAll(".theme-toggle-btn");
  for (var j = 0; j < buttons.length; j++) {
    buttons[j].addEventListener("click", function () {
      var now = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
      setTheme(now, true);
    });
  }
})();
