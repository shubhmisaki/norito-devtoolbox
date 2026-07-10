(function () {
  const I18N = i18nFor("app-placeholder");
  const els = {
    width: document.getElementById("width"),
    height: document.getElementById("height"),
    bg: document.getElementById("bg"),
    fg: document.getElementById("fg"),
    text: document.getElementById("text"),
    format: document.getElementById("pformat"),
    swatches: document.getElementById("colorSwatches"),
    canvas: document.getElementById("canvas"),
    generateBtn: document.getElementById("pGenerateBtn"),
    downloadBtn: document.getElementById("pDownloadBtn"),
    info: document.getElementById("pInfo"),
  };

  let lastBlob = null;
  let lastW = 600;
  let lastH = 400;

  // Remember the output format between visits: nice-to-have only, silently
  // no-ops if localStorage is unavailable.
  const PREFS_KEY = "norito:placeholder-generator";
  function loadPrefs() {
    try { return JSON.parse(localStorage.getItem(PREFS_KEY)) || {}; } catch (e) { return {}; }
  }
  function savePref(key, value) {
    try {
      const p = loadPrefs();
      p[key] = value;
      localStorage.setItem(PREFS_KEY, JSON.stringify(p));
    } catch (e) { /* ignore */ }
  }
  (function restorePrefs() {
    const p = loadPrefs();
    if (p.format) els.format.value = p.format;
  })();
  els.format.addEventListener("change", () => savePref("format", els.format.value));

  // Reads a dimension field without ever writing back to it. If the field
  // is empty (the user is mid-edit, clearing it to type a new value) or not
  // a valid number yet, this falls back silently for the live preview only
  // The input itself is left alone so it can be fully cleared and retyped.
  function getDimension(el, fallback) {
    const raw = el.value.trim();
    if (raw === "") return fallback;
    const n = parseInt(raw, 10);
    if (!Number.isFinite(n) || n <= 0) return fallback;
    return Math.max(1, Math.min(4000, n));
  }

  function draw() {
    const w = getDimension(els.width, lastW);
    const h = getDimension(els.height, lastH);
    lastW = w;
    lastH = h;

    const canvas = els.canvas;
    canvas.width = w;
    canvas.height = h;
    const ctx = canvas.getContext("2d");

    ctx.fillStyle = els.bg.value;
    ctx.fillRect(0, 0, w, h);

    const label = els.text.value.trim() || `${w} × ${h}`;
    ctx.fillStyle = els.fg.value;
    const fontSize = Math.max(12, Math.round(Math.min(w, h) / 8));
    ctx.font = `600 ${fontSize}px -apple-system, Segoe UI, Roboto, sans-serif`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(label, w / 2, h / 2, w * 0.9);

    return canvas;
  }

  const SWATCHES = [
    { name: I18N.swatch_brand_pink || "Brand pink", bg: "#ff4d7a", fg: "#ffffff" },
    { name: I18N.swatch_neutral_gray || "Neutral gray", bg: "#e2e2e2", fg: "#4b5563" },
    { name: I18N.swatch_slate || "Slate", bg: "#1f2937", fg: "#ffffff" },
    { name: I18N.swatch_sky_blue || "Sky blue", bg: "#60a5fa", fg: "#ffffff" },
    { name: I18N.swatch_soft_beige || "Soft beige", bg: "#f5f0e8", fg: "#44403c" },
    { name: I18N.swatch_mint || "Mint", bg: "#6ee7b7", fg: "#064e3b" },
  ];
  SWATCHES.forEach((s) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "swatch-btn";
    btn.style.background = s.bg;
    btn.title = s.name;
    btn.setAttribute("aria-label", s.name);
    btn.addEventListener("click", () => {
      els.bg.value = s.bg;
      els.fg.value = s.fg;
      draw();
    });
    els.swatches.appendChild(btn);
  });

  // If a dimension field is left empty when the user clicks away, fill in
  // the size that was actually last rendered, never a hardcoded default,
  // so the visible number always matches what's on the canvas.
  [els.width, els.height].forEach((el, i) => {
    el.addEventListener("blur", () => {
      if (el.value.trim() === "") el.value = i === 0 ? lastW : lastH;
    });
  });

  function canvasToBlob(canvas, mime) {
    return new Promise((resolve) => canvas.toBlob(resolve, mime, 0.92));
  }

  function pulseHighlight(el) {
    if (!el) return;
    el.classList.remove("highlight-pulse");
    void el.offsetWidth;
    el.classList.add("highlight-pulse");
    setTimeout(() => el.classList.remove("highlight-pulse"), 1300);
  }

  async function generate() {
    const canvas = draw();
    const fmt = els.format.value;
    const mime = { png: "image/png", jpg: "image/jpeg", webp: "image/webp" }[fmt];
    lastBlob = await canvasToBlob(canvas, mime);
    els.info.textContent = window.fmt(I18N.placeholder_ready || "Placeholder ready: {w}×{h}, {size}, {fmt}",
      { w: canvas.width, h: canvas.height, size: formatBytes(lastBlob.size), fmt: fmt.toUpperCase() });
    els.info.style.display = "block";
    els.downloadBtn.disabled = false;
    pulseHighlight(els.downloadBtn);
    celebrateSuccess(els.generateBtn);
  }

  els.generateBtn.addEventListener("click", generate);
  [els.width, els.height, els.bg, els.fg, els.text, els.format].forEach((el) =>
    el.addEventListener("input", () => draw())
  );

  els.downloadBtn.addEventListener("click", () => {
    if (!lastBlob) return;
    const fmt = els.format.value;
    const filename = `placeholder_${lastW}x${lastH}.${fmt === "jpg" ? "jpg" : fmt}`;
    downloadBlob(lastBlob, filename);
  });

  draw(); // initial preview
})();
