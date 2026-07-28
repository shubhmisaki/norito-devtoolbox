(function () {
  const I18N = i18nFor("app-placeholder");
  const els = {
    width: document.getElementById("width"),
    height: document.getElementById("height"),
    bg: document.getElementById("bg"),
    fg: document.getElementById("fg"),
    text: document.getElementById("text"),
    format: document.getElementById("pformat"),
    stylePicker: document.getElementById("stylePicker"),
    customColorsRow: document.getElementById("customColorsRow"),
    imageUploadRow: document.getElementById("imageUploadRow"),
    imageDrop: document.getElementById("imageDrop"),
    bgImageInput: document.getElementById("bgImageInput"),
    canvas: document.getElementById("canvas"),
    downloadBtn: document.getElementById("pDownloadBtn"),
    info: document.getElementById("pInfo"),
  };

  let lastBlob = null;
  let lastW = 600;
  let lastH = 400;
  let styleMode = "preset"; // "preset" | "custom" | "image"
  let bgImage = null;
  let infoTimer = null;

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
  els.format.addEventListener("change", () => { savePref("format", els.format.value); scheduleUpdate(); });

  // Reads a dimension field without ever writing back to it. If the field
  // is empty (the user is mid-edit, clearing it to type a new value) or not
  // a valid number yet, this falls back silently for the live preview only.
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

    if (styleMode === "image" && bgImage) {
      const scale = Math.max(w / bgImage.width, h / bgImage.height);
      const iw = bgImage.width * scale;
      const ih = bgImage.height * scale;
      ctx.drawImage(bgImage, (w - iw) / 2, (h - ih) / 2, iw, ih);
    } else {
      ctx.fillStyle = els.bg.value;
      ctx.fillRect(0, 0, w, h);
    }

    const label = els.text.value.trim() || (styleMode === "image" ? "" : `${w} × ${h}`);
    if (label) {
      const fontSize = Math.max(12, Math.round(Math.min(w, h) / 8));
      ctx.font = `600 ${fontSize}px -apple-system, Segoe UI, Roboto, sans-serif`;
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      if (styleMode === "image") {
        // Legibility backdrop so the label reads over a busy photo.
        const metrics = ctx.measureText(label);
        const padX = 14, padY = 8;
        const bw = Math.min(metrics.width + padX * 2, w * 0.92);
        const bh = fontSize + padY * 2;
        ctx.fillStyle = "rgba(0,0,0,0.45)";
        ctx.fillRect(w / 2 - bw / 2, h / 2 - bh / 2, bw, bh);
      }
      ctx.fillStyle = els.fg.value;
      ctx.fillText(label, w / 2, h / 2, w * 0.9);
    }

    return canvas;
  }

  // ---- style picker: preset swatches, custom colors, or a background image ----
  const tiles = Array.from(els.stylePicker.querySelectorAll(".style-tile"));
  function selectTile(tile) {
    tiles.forEach((t) => t.classList.remove("active"));
    tile.classList.add("active");
    styleMode = tile.dataset.mode;
    els.customColorsRow.style.display = styleMode === "custom" ? "flex" : "none";
    els.imageUploadRow.style.display = styleMode === "image" ? "block" : "none";
    if (styleMode === "preset") {
      els.bg.value = tile.dataset.bg;
      els.fg.value = tile.dataset.fg;
    }
    scheduleUpdate();
  }
  tiles.forEach((tile) => tile.addEventListener("click", () => selectTile(tile)));

  [els.bg, els.fg].forEach((el) => el.addEventListener("input", scheduleUpdate));

  function loadBgImageFile(file) {
    if (!file || !file.type.startsWith("image/")) return;
    const url = URL.createObjectURL(file);
    const img = new Image();
    img.onload = () => {
      bgImage = img;
      scheduleUpdate();
    };
    img.src = url;
  }
  if (els.imageDrop) {
    els.imageDrop.addEventListener("click", () => els.bgImageInput.click());
    els.bgImageInput.addEventListener("change", (e) => loadBgImageFile(e.target.files[0]));
    wireDragDrop(els.imageDrop, (e) => {
      const file = e.dataTransfer.files[0];
      if (file) loadBgImageFile(file);
    });
  }

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

  // Redraws the canvas immediately (cheap, synchronous) and separately
  // debounces the blob conversion + detail text (async, a bit heavier) so
  // typing doesn't feel janky. There's no more "Refresh preview" button:
  // this fires on every change instead.
  async function updatePreview() {
    const canvas = draw();
    const outFormat = els.format.value;
    const mime = { png: "image/png", jpg: "image/jpeg", webp: "image/webp" }[outFormat];
    lastBlob = await canvasToBlob(canvas, mime);
    els.info.textContent = window.fmt(I18N.placeholder_ready || "Placeholder ready: {w}×{h}, {size}, {fmt}",
      { w: canvas.width, h: canvas.height, size: formatBytes(lastBlob.size), fmt: outFormat.toUpperCase() });
    els.info.style.display = "block";
    els.downloadBtn.disabled = false;
  }

  function scheduleUpdate() {
    draw();
    clearTimeout(infoTimer);
    infoTimer = setTimeout(updatePreview, 150);
  }

  [els.width, els.height, els.text].forEach((el) => el.addEventListener("input", scheduleUpdate));

  els.downloadBtn.addEventListener("click", () => {
    if (!lastBlob) return;
    const outFormat = els.format.value;
    const filename = `placeholder_${lastW}x${lastH}.${outFormat === "jpg" ? "jpg" : outFormat}`;
    downloadBlob(lastBlob, filename);
    pulseHighlight(els.downloadBtn);
    celebrateSuccess(els.downloadBtn);
  });

  scheduleUpdate(); // initial preview
})();
