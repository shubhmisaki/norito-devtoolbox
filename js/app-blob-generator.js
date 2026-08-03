(function () {
  const els = {
    randomness: document.getElementById("blobRandomness"),
    randomnessVal: document.getElementById("blobRandomnessVal"),
    points: document.getElementById("blobPoints"),
    pointsVal: document.getElementById("blobPointsVal"),
    color: document.getElementById("blobColor"),
    seed: document.getElementById("blobSeed"),
    regenBtn: document.getElementById("regenBtn"),
    path: document.getElementById("blobPath"),
    output: document.getElementById("output"),
    copyBtn: document.getElementById("copyBtn"),
    downloadBtn: document.getElementById("downloadBtn"),
  };

  // Small deterministic PRNG (mulberry32) so a seed reproduces the same blob.
  function mulberry32(seed) {
    let t = seed >>> 0;
    return function () {
      t |= 0; t = (t + 0x6D2B79F5) | 0;
      let r = Math.imul(t ^ (t >>> 15), 1 | t);
      r = (r + Math.imul(r ^ (r >>> 7), 61 | r)) ^ r;
      return ((r ^ (r >>> 14)) >>> 0) / 4294967296;
    };
  }

  function catmullRomToBezierPath(points) {
    // points: array of {x,y}, closed loop
    const n = points.length;
    const p = (i) => points[((i % n) + n) % n];
    let d = `M ${points[0].x.toFixed(2)},${points[0].y.toFixed(2)} `;
    for (let i = 0; i < n; i++) {
      const p0 = p(i - 1), p1 = p(i), p2 = p(i + 1), p3 = p(i + 2);
      const c1x = p1.x + (p2.x - p0.x) / 6;
      const c1y = p1.y + (p2.y - p0.y) / 6;
      const c2x = p2.x - (p3.x - p1.x) / 6;
      const c2y = p2.y - (p3.y - p1.y) / 6;
      d += `C ${c1x.toFixed(2)},${c1y.toFixed(2)} ${c2x.toFixed(2)},${c2y.toFixed(2)} ${p2.x.toFixed(2)},${p2.y.toFixed(2)} `;
    }
    return d + "Z";
  }

  function generatePoints(count, randomness, seed) {
    const rand = mulberry32(seed);
    const cx = 100, cy = 100, baseR = 70;
    const pts = [];
    for (let i = 0; i < count; i++) {
      const angle = (i / count) * Math.PI * 2;
      const offset = (rand() - 0.5) * 2 * (randomness / 100) * baseR;
      const r = Math.max(20, baseR + offset);
      pts.push({ x: cx + r * Math.cos(angle), y: cy + r * Math.sin(angle) });
    }
    return pts;
  }

  function render() {
    const randomness = Number(els.randomness.value);
    const count = Number(els.points.value);
    const seed = Number(els.seed.value) || 0;
    els.randomnessVal.textContent = `${randomness}%`;
    els.pointsVal.textContent = String(count);

    const pts = generatePoints(count, randomness, seed);
    const d = catmullRomToBezierPath(pts);
    els.path.setAttribute("d", d);
    els.path.setAttribute("fill", els.color.value);

    const svgString = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><path d="${d}" fill="${els.color.value}" /></svg>`;
    els.output.textContent = svgString;
  }

  [els.randomness, els.points, els.color, els.seed].forEach((el) => el.addEventListener("input", render));
  els.regenBtn.addEventListener("click", () => {
    els.seed.value = Math.floor(Math.random() * 100000);
    render();
  });
  render();

  els.copyBtn.addEventListener("click", async () => {
    if (!els.output.textContent) return;
    try {
      await copyToClipboard(els.output.textContent);
      const I18N_C = i18nFor("common");
      showMascotToast(I18N_C.copied || "Copied!");
      celebrateSuccess(els.copyBtn);
    } catch (e) { /* clipboard unavailable, silently ignore */ }
  });

  els.downloadBtn.addEventListener("click", () => {
    if (!els.output.textContent) return;
    downloadBlob(new Blob([els.output.textContent], { type: "image/svg+xml" }), "blob.svg");
  });
})();
