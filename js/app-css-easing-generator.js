(function () {
  const svg = document.getElementById("curveSvg");
  const path = document.getElementById("curvePath");
  const h1 = document.getElementById("handle1");
  const h2 = document.getElementById("handle2");
  const h1Line = document.getElementById("handle1Line");
  const h2Line = document.getElementById("handle2Line");
  const inputs = {
    p1x: document.getElementById("p1x"),
    p1y: document.getElementById("p1y"),
    p2x: document.getElementById("p2x"),
    p2y: document.getElementById("p2y"),
  };
  const output = document.getElementById("output");
  const copyBtn = document.getElementById("copyBtn");
  const playBtn = document.getElementById("playBtn");
  const ball = document.getElementById("animBall");

  // SVG space: x 0..200 maps to bezier x 0..1, y 0..200 maps to bezier y 1..0 (flipped).
  function toSvgX(x) { return x * 200; }
  function toSvgY(y) { return 200 - y * 200; }
  function fromSvgX(sx) { return sx / 200; }
  function fromSvgY(sy) { return (200 - sy) / 200; }

  function currentPoints() {
    return {
      p1x: Number(inputs.p1x.value),
      p1y: Number(inputs.p1y.value),
      p2x: Number(inputs.p2x.value),
      p2y: Number(inputs.p2y.value),
    };
  }

  function render() {
    const p = currentPoints();
    const sx1 = toSvgX(p.p1x), sy1 = toSvgY(p.p1y);
    const sx2 = toSvgX(p.p2x), sy2 = toSvgY(p.p2y);

    path.setAttribute("d", `M0,200 C${sx1},${sy1} ${sx2},${sy2} 200,0`);
    h1.setAttribute("cx", sx1); h1.setAttribute("cy", sy1);
    h2.setAttribute("cx", sx2); h2.setAttribute("cy", sy2);
    h1Line.setAttribute("x1", 0); h1Line.setAttribute("y1", 200);
    h1Line.setAttribute("x2", sx1); h1Line.setAttribute("y2", sy1);
    h2Line.setAttribute("x1", 200); h2Line.setAttribute("y1", 0);
    h2Line.setAttribute("x2", sx2); h2Line.setAttribute("y2", sy2);

    const fmt = (n) => Number(n.toFixed(3)).toString();
    const css = `cubic-bezier(${fmt(p.p1x)}, ${fmt(p.p1y)}, ${fmt(p.p2x)}, ${fmt(p.p2y)})`;
    output.textContent = `transition-timing-function: ${css};`;
    ball.style.transitionTimingFunction = css;
  }

  function clamp(v, min, max) { return Math.max(min, Math.min(max, v)); }

  function makeDraggable(handle, xInput, yInput, xClamp) {
    let dragging = false;
    function onMove(e) {
      if (!dragging) return;
      const rect = svg.getBoundingClientRect();
      const clientX = e.touches ? e.touches[0].clientX : e.clientX;
      const clientY = e.touches ? e.touches[0].clientY : e.clientY;
      const sx = ((clientX - rect.left) / rect.width) * 200;
      const sy = ((clientY - rect.top) / rect.height) * 200;
      const x = clamp(fromSvgX(sx), 0, 1);
      const y = clamp(fromSvgY(sy), -0.6, 1.6);
      xInput.value = x.toFixed(3);
      yInput.value = y.toFixed(3);
      render();
    }
    function onUp() {
      dragging = false;
      window.removeEventListener("pointermove", onMove);
      window.removeEventListener("pointerup", onUp);
    }
    handle.addEventListener("pointerdown", (e) => {
      dragging = true;
      e.preventDefault();
      window.addEventListener("pointermove", onMove);
      window.addEventListener("pointerup", onUp);
    });
  }

  makeDraggable(h1, inputs.p1x, inputs.p1y);
  makeDraggable(h2, inputs.p2x, inputs.p2y);

  Object.values(inputs).forEach((el) => el.addEventListener("input", render));
  render();

  document.querySelectorAll(".preset-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const [x1, y1, x2, y2] = btn.dataset.p.split(",").map(Number);
      inputs.p1x.value = x1; inputs.p1y.value = y1;
      inputs.p2x.value = x2; inputs.p2y.value = y2;
      render();
      playAnimation();
    });
  });

  function playAnimation() {
    ball.style.transition = "none";
    ball.style.left = "6px";
    // force reflow so the next transition actually animates
    void ball.offsetWidth;
    const p = currentPoints();
    const fmt = (n) => Number(n.toFixed(3)).toString();
    ball.style.transition = `left 1s cubic-bezier(${fmt(p.p1x)}, ${fmt(p.p1y)}, ${fmt(p.p2x)}, ${fmt(p.p2y)})`;
    requestAnimationFrame(() => {
      const track = document.getElementById("animTrack");
      ball.style.left = `${track.clientWidth - 38}px`;
    });
  }

  playBtn.addEventListener("click", playAnimation);
  window.addEventListener("load", playAnimation);

  copyBtn.addEventListener("click", async () => {
    if (!output.textContent) return;
    try {
      await copyToClipboard(output.textContent);
      const I18N_C = i18nFor("common");
      showMascotToast(I18N_C.copied || "Copied!");
      celebrateSuccess(copyBtn);
    } catch (e) { /* clipboard unavailable, silently ignore */ }
  });
})();
