// norito service worker
//
// Strategy: this is a 100+ page static site, so rather than precaching every
// page up front (fragile: one missing/renamed file fails the whole install),
// we precache a small app shell and otherwise cache opportunistically as
// pages are visited ("cache what you use"). That means the first visit to
// any page needs network, but every page you've ever opened works offline
// after that, and updates roll out automatically because static assets use
// stale-while-revalidate (serve the cached copy instantly, refresh it in
// the background for next time).
const CACHE_VERSION = "norito-v2";
const APP_SHELL = ["/", "/index.html", "/offline.html", "/manifest.json", "/css/style.css", "/js/nav.js", "/js/theme-toggle.js", "/js/bg-blobs.js", "/js/cmdk.js", "/assets/norito-wordmark.svg", "/assets/icon-192.png"];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches
      .open(CACHE_VERSION)
      .then((cache) => cache.addAll(APP_SHELL))
      .catch(() => {}) // never fail install over one missing shell asset
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE_VERSION).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

function isNavigation(request) {
  return request.mode === "navigate" || (request.method === "GET" && request.headers.get("accept")?.includes("text/html"));
}

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;

  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return; // let cross-origin (fonts/ads) pass through untouched

  if (isNavigation(req)) {
    // Network-first for pages: always try to get the freshest HTML, fall
    // back to whatever's cached, fall back to the offline page.
    event.respondWith(
      fetch(req)
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE_VERSION).then((cache) => cache.put(req, copy));
          return res;
        })
        .catch(() => caches.match(req).then((cached) => cached || caches.match("/offline.html")))
    );
    return;
  }

  // Network-first for CSS and JS: these must always match the HTML that
  // references them, otherwise a deploy can render pages with a stale
  // stylesheet or app logic on the first visit. Cache fallback keeps
  // offline working.
  if (url.pathname.endsWith(".css") || url.pathname.endsWith(".js")) {
    event.respondWith(
      fetch(req)
        .then((res) => {
          if (res && res.status === 200) {
            const copy = res.clone();
            caches.open(CACHE_VERSION).then((cache) => cache.put(req, copy));
          }
          return res;
        })
        .catch(() => caches.match(req))
    );
    return;
  }

  // Stale-while-revalidate for everything else (images/fonts/vendor data):
  // serve from cache instantly if we have it, refresh in the background.
  event.respondWith(
    caches.match(req).then((cached) => {
      const network = fetch(req)
        .then((res) => {
          if (res && res.status === 200) {
            const copy = res.clone();
            caches.open(CACHE_VERSION).then((cache) => cache.put(req, copy));
          }
          return res;
        })
        .catch(() => cached);
      return cached || network;
    })
  );
});
