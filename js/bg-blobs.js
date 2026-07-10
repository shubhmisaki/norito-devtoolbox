(function () {
  const reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const blobs = document.querySelectorAll(".bg-blobs .blob");
  if (!blobs.length || reduceMotion) return;

  const strength = [16, -12, 22];
  let ticking = false;
  let lastX = 0, lastY = 0;

  function onMove(e) {
    lastX = (e.clientX / window.innerWidth) * 2 - 1;
    lastY = (e.clientY / window.innerHeight) * 2 - 1;
    if (!ticking) {
      ticking = true;
      requestAnimationFrame(apply);
    }
  }

  function apply() {
    blobs.forEach((blob, i) => {
      const s = strength[i % strength.length];
      blob.style.transform = `translate(${lastX * s}px, ${lastY * s}px)`;
    });
    ticking = false;
  }

  window.addEventListener("mousemove", onMove, { passive: true });
})();
