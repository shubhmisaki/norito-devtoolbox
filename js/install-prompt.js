(function () {
  var STORAGE_KEY = "norito:installPromptDismissedAt";
  var SNOOZE_DAYS = 14;

  // Already installed / running as a standalone app: nothing to do.
  if (window.matchMedia && window.matchMedia("(display-mode: standalone)").matches) return;
  if (window.navigator.standalone === true) return; // iOS Safari home-screen check

  function dismissedRecently() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return false;
      var dismissedAt = parseInt(raw, 10);
      if (!dismissedAt) return false;
      var days = (Date.now() - dismissedAt) / (1000 * 60 * 60 * 24);
      return days < SNOOZE_DAYS;
    } catch (e) {
      return false;
    }
  }

  var deferredPrompt = null;
  var banner = null;

  function buildBanner() {
    var el = document.createElement("div");
    el.className = "install-banner";
    el.setAttribute("role", "region");
    el.setAttribute("aria-label", "Install norito");
    el.innerHTML =
      '<div class="install-banner-inner">' +
      '<div class="install-banner-icon"><img src="/assets/norito-mark.svg" alt="" width="28" height="28" /></div>' +
      '<div class="install-banner-text">' +
      "<strong>Install norito</strong>" +
      "<span>Add it to your device for one-tap access, even offline.</span>" +
      "</div>" +
      '<button type="button" class="install-banner-btn" id="installBannerInstall">Install</button>' +
      '<button type="button" class="install-banner-close" id="installBannerClose" aria-label="Dismiss">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>' +
      "</button>" +
      "</div>";
    return el;
  }

  function dismiss() {
    if (!banner) return;
    banner.classList.remove("visible");
    setTimeout(function () {
      if (banner && banner.parentNode) banner.parentNode.removeChild(banner);
    }, 300);
    try {
      localStorage.setItem(STORAGE_KEY, String(Date.now()));
    } catch (e) {}
  }

  function showBanner() {
    if (banner || dismissedRecently()) return;
    banner = buildBanner();
    document.body.appendChild(banner);
    requestAnimationFrame(function () {
      banner.classList.add("visible");
    });
    document.getElementById("installBannerClose").addEventListener("click", dismiss);
    document.getElementById("installBannerInstall").addEventListener("click", async function () {
      if (!deferredPrompt) return;
      deferredPrompt.prompt();
      try {
        await deferredPrompt.userChoice;
      } catch (e) {}
      deferredPrompt = null;
      dismiss();
    });
  }

  window.addEventListener("beforeinstallprompt", function (e) {
    e.preventDefault();
    deferredPrompt = e;
    showBanner();
  });

  window.addEventListener("appinstalled", function () {
    dismiss();
    deferredPrompt = null;
  });
})();
