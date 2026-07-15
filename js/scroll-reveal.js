(function () {
  const reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const targets = document.querySelectorAll(".card, main h2");
  if (!targets.length) return;

  if (reduceMotion || typeof IntersectionObserver !== "function") {
    // No .reveal class added at all: elements just render at their normal
    // opacity/position, which is visually identical to "reveal + visible"
    // anyway.
    return;
  }

  // Anything already inside (or above) the initial viewport at load time is
  // left completely alone: no .reveal class, no fade, no delay. Fading in
  // content that's already on screen only delays when it visually "arrives"
  // and can push out the page's Largest Contentful Paint for no real
  // benefit, since the element was never actually offscreen. Only elements
  // below the fold get the scroll-triggered fade-in.
  //
  // All the geometry reads (getBoundingClientRect) happen first, in their
  // own pass, before any DOM writes (classList/style). Interleaving reads
  // and writes per-element forces the browser to flush layout on every
  // single iteration (a "forced reflow"); batching reads-then-writes lets
  // it happen once.
  const viewportH = window.innerHeight || document.documentElement.clientHeight;
  const belowFold = [];
  targets.forEach((el) => {
    if (el.getBoundingClientRect().top >= viewportH) belowFold.push(el);
  });

  const toObserve = [];
  belowFold.forEach((el, i) => {
    el.classList.add("reveal");
    // Small stagger within a grid row so a full row of cards doesn't all
    // fade in on the exact same frame.
    el.style.transitionDelay = (i % 3) * 70 + "ms";
    toObserve.push(el);
  });

  if (!toObserve.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
  );

  toObserve.forEach((el) => observer.observe(el));
})();
