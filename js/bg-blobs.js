(function () {
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var container = document.querySelector(".bg-blobs");
  if (!container || reduceMotion) return;

  // Ambient drift is handled by pure CSS keyframe animations on each .blob
  // (GPU-composited, zero main-thread cost). JS only adds a light mouse
  // parallax on the container, and only when the mouse actually moves --
  // no requestAnimationFrame loop.
  var strength = 14;
  var ticking = false;

  window.addEventListener(
    "mousemove",
    function (e) {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        var x = (e.clientX / window.innerWidth) * 2 - 1;
        var y = (e.clientY / window.innerHeight) * 2 - 1;
        container.style.transform = "translate(" + x * strength + "px, " + y * strength + "px)";
        ticking = false;
      });
    },
    { passive: true }
  );
})();
