(function () {
  const reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const targets = document.querySelectorAll(".card, main h2");
  if (!targets.length) return;

  if (reduceMotion || typeof IntersectionObserver !== "function") {
    targets.forEach((el) => el.classList.add("reveal", "is-visible"));
    return;
  }

  targets.forEach((el, i) => {
    el.classList.add("reveal");
    // Small stagger within a grid row so a full row of cards doesn't all
    // fade in on the exact same frame.
    el.style.transitionDelay = (i % 3) * 70 + "ms";
  });

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

  targets.forEach((el) => observer.observe(el));
})();
