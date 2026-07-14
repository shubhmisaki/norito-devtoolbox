// Registers the service worker (see /sw.js) so tools keep working offline
// after a first visit, and the site can be installed as an app. Absolute
// path so this works identically from any page depth.
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/sw.js").catch(() => {});
  });
}
