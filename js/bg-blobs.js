(function () {
  const reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const blobs = document.querySelectorAll(".bg-blobs .blob");
  if (!blobs.length || reduceMotion) return;

  // mouse parallax (existing behavior) layered with a slow, continuous
  // ambient drift per blob so the background feels alive even when the
  // user isn't moving the cursor, similar to Stripe's animated gradient mesh.
  const parallaxStrength = [16, -12, 22];
  const driftAmp = [14, 18, 10];
  const driftFreq = [0.00011, 0.00008, 0.00014];
  const driftPhase = [0, 2.1, 4.2];

  let mouseX = 0, mouseY = 0;

  function onMove(e) {
    mouseX = (e.clientX / window.innerWidth) * 2 - 1;
    mouseY = (e.clientY / window.innerHeight) * 2 - 1;
  }
  window.addEventListener("mousemove", onMove, { passive: true });

  function frame(t) {
    blobs.forEach((blob, i) => {
      const p = parallaxStrength[i % parallaxStrength.length];
      const amp = driftAmp[i % driftAmp.length];
      const freq = driftFreq[i % driftFreq.length];
      const phase = driftPhase[i % driftPhase.length];
      const driftX = Math.sin(t * freq + phase) * amp;
      const driftY = Math.cos(t * freq * 1.3 + phase) * amp;
      blob.style.transform = `translate(${mouseX * p + driftX}px, ${mouseY * p + driftY}px)`;
    });
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();
