(function () {
  const I18N = i18nFor("app-compress");
  const I18N_C = i18nFor("common");
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    size: document.getElementById("targetSize"),
    unit: document.getElementById("targetUnit"),
    format: document.getElementById("format"),
    allowResize: document.getElementById("allowResize"),
    compressBtn: document.getElementById("compressBtn"),
    result: document.getElementById("result"),
    preview: document.getElementById("preview"),
    originalInfo: document.getElementById("originalInfo"),
    previewHint: document.getElementById("previewHint"),
  };

  let currentImg = null;
  let currentFile = null;

  // Remember format/unit/resize choices between visits: nice-to-have only,
  // silently no-ops if localStorage is unavailable.
  const PREFS_KEY = "norito:compress-image";
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
    if (p.unit) els.unit.value = p.unit;
    if (p.format) els.format.value = p.format;
    if (typeof p.allowResize === "boolean" && els.allowResize) els.allowResize.checked = p.allowResize;
  })();
  els.unit.addEventListener("change", () => savePref("unit", els.unit.value));
  els.format.addEventListener("change", () => savePref("format", els.format.value));
  if (els.allowResize) {
    els.allowResize.addEventListener("change", () => savePref("allowResize", els.allowResize.checked));
  }

  function canvasToBlob(canvas, mime, quality) {
    return new Promise((resolve) => canvas.toBlob(resolve, mime, quality));
  }

  function loadImageFile(file) {
    return new Promise((resolve, reject) => {
      const url = URL.createObjectURL(file);
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = reject;
      img.src = url;
    });
  }

  async function handleFile(file) {
    if (!file || !file.type.startsWith("image/")) {
      setResult(I18N_C.please_choose_image || "Please choose an image file.", false);
      return;
    }
    currentFile = file;
    currentImg = await loadImageFile(file);
    els.originalInfo.textContent =
      `${file.name}, ${currentImg.width}×${currentImg.height}, ${formatBytes(file.size)}`;
    els.originalInfo.style.display = "block";
    els.compressBtn.disabled = false;
  }

  els.drop.addEventListener("click", () => els.fileInput.click());
  els.fileInput.addEventListener("change", (e) => handleFile(e.target.files[0]));
  ["dragenter", "dragover"].forEach((evt) =>
    els.drop.addEventListener(evt, (e) => { e.preventDefault(); els.drop.classList.add("drag"); })
  );
  ["dragleave", "drop"].forEach((evt) =>
    els.drop.addEventListener(evt, (e) => { e.preventDefault(); els.drop.classList.remove("drag"); })
  );
  els.drop.addEventListener("drop", (e) => {
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  });

  // Paste an image straight from the clipboard (screenshot tools, "Copy image", etc.)
  document.addEventListener("paste", (e) => {
    const items = e.clipboardData && e.clipboardData.items;
    if (!items) return;
    for (const item of items) {
      if (item.type && item.type.startsWith("image/")) {
        const file = item.getAsFile();
        if (file) { handleFile(file); e.preventDefault(); }
        break;
      }
    }
  });

  const ICONS = {
    ok: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="M22 4 12 14.01l-3-3"/></svg>',
    error: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>',
    neutral: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>',
  };

  function setResult(html, state) {
    const cls = state === true ? "ok" : state === false ? "error" : state || "neutral";
    els.result.innerHTML =
      `<span class="r-icon">${ICONS[cls] || ICONS.neutral}</span><span class="r-body">${html}</span>`;
    els.result.style.display = "flex";
    els.result.classList.remove("ok", "error");
    if (cls === "ok" || cls === "error") els.result.classList.add(cls);
  }

  function pulseHighlight(el) {
    if (!el) return;
    el.classList.remove("highlight-pulse");
    void el.offsetWidth;
    el.classList.add("highlight-pulse");
    setTimeout(() => el.classList.remove("highlight-pulse"), 1300);
  }

  // Returns { blob, width, height, resized } instead of a bare blob, so the
  // caller can tell the user whether dimensions changed. By default (allowResize
  // false) this only binary-searches quality at the image's original size.
  // it never shrinks the image unless the user explicitly opts in.
  async function compressLossy(img, targetBytes, mime, allowResize) {
    let scale = 1.0;
    let best = null; // first scale that actually hit the target
    let closest = null; // smallest blob seen, in case target is never hit
    const maxAttempts = allowResize ? 10 : 1;

    for (let attempt = 0; attempt < maxAttempts; attempt++) {
      const w = Math.max(1, Math.round(img.width * scale));
      const h = Math.max(1, Math.round(img.height * scale));
      const canvas = document.createElement("canvas");
      canvas.width = w;
      canvas.height = h;
      canvas.getContext("2d").drawImage(img, 0, 0, w, h);
      const resized = scale !== 1;

      let lo = 0.01, hi = 1.0, foundAtScale = null;
      for (let i = 0; i < 8; i++) {
        const mid = (lo + hi) / 2;
        const blob = await canvasToBlob(canvas, mime, mid);
        if (!closest || blob.size < closest.blob.size) closest = { blob, width: w, height: h, resized };
        if (blob.size <= targetBytes) { foundAtScale = blob; lo = mid; } else { hi = mid; }
      }
      if (!foundAtScale) {
        const blob = await canvasToBlob(canvas, mime, 0.01);
        if (!closest || blob.size < closest.blob.size) closest = { blob, width: w, height: h, resized };
        if (blob.size <= targetBytes) foundAtScale = blob;
      }
      if (foundAtScale) { best = { blob: foundAtScale, width: w, height: h, resized }; break; }
      if (w <= 16 || h <= 16) break;
      scale *= 0.85;
    }
    return best || closest;
  }

  async function compressPng(img, targetBytes, allowResize) {
    let scale = 1.0;
    let last = null;
    const maxAttempts = allowResize ? 20 : 1;
    for (let attempt = 0; attempt < maxAttempts; attempt++) {
      const w = Math.max(1, Math.round(img.width * scale));
      const h = Math.max(1, Math.round(img.height * scale));
      const canvas = document.createElement("canvas");
      canvas.width = w;
      canvas.height = h;
      canvas.getContext("2d").drawImage(img, 0, 0, w, h);
      const blob = await canvasToBlob(canvas, "image/png");
      last = { blob, width: w, height: h, resized: scale !== 1 };
      if (blob.size <= targetBytes) return last;
      if (w <= 8 || h <= 8) return last; // best effort, give up shrinking further
      scale *= 0.85;
    }
    return last;
  }

  els.compressBtn.addEventListener("click", async () => {
    if (!currentImg) return;
    const target = parseSize(els.size.value, els.unit.value);
    if (target === null || target <= 0) {
      setResult(I18N.err_invalid_target || "Enter a valid target size.", "error");
      return;
    }

    els.compressBtn.disabled = true;
    els.compressBtn.textContent = I18N.compressing_label || "Compressing…";
    setResult(I18N_C.working || "Working…", "neutral");
    let finishedState = null;

    try {
      const outFormat = els.format.value;
      const mime = { jpeg: "image/jpeg", webp: "image/webp", png: "image/png" }[outFormat];
      const allowResize = !!(els.allowResize && els.allowResize.checked);
      let outcome;
      if (outFormat === "png") outcome = await compressPng(currentImg, target, allowResize);
      else outcome = await compressLossy(currentImg, target, mime, allowResize);

      if (!outcome || !outcome.blob) {
        setResult(
          fmt(I18N.err_no_outcome || "Couldn't get under {target} even at minimum quality. Try a larger target, switch format, or turn on \"Allow resizing\".",
            { target: formatBytes(target) }),
          "error"
        );
        return;
      }

      const { blob, resized } = outcome;
      const url = URL.createObjectURL(blob);
      els.preview.src = url;
      els.preview.style.display = "block";
      if (els.previewHint) els.previewHint.style.display = "none";

      const ext = { jpeg: "jpg", webp: "webp", png: "png" }[outFormat];
      const filename = `compressed_${els.size.value}${els.unit.value}.${ext}`;
      const withinTarget = blob.size <= target;
      const dimsNote = resized
        ? fmt(I18N.dims_resized || "resized to {w}×{h} (from {ow}×{oh})",
            { w: outcome.width, h: outcome.height, ow: currentImg.width, oh: currentImg.height })
        : fmt(I18N.dims_original || "original {w}×{h} size",
            { w: currentImg.width, h: currentImg.height });

      let statusLine;
      let state;
      if (withinTarget) {
        statusLine = fmt(I18N.status_within_target || "within your target, at {dims}.", { dims: dimsNote });
        state = "ok";
      } else if (allowResize) {
        statusLine = fmt(I18N.status_closest_resized || "closest achievable size (target was too small even after resizing), at {dims}.", { dims: dimsNote });
        state = "neutral";
      } else {
        statusLine = fmt(I18N.status_closest_noresize || "closest achievable size at {dims}. Quality reduction alone couldn't reach your target. Turn on \"Allow resizing\" above for a smaller file.", { dims: dimsNote });
        state = "neutral";
      }

      setResult(
        fmt(I18N.result_success || "<strong>Image compressed successfully.</strong> <strong>{size}</strong>. {statusLine}",
          { size: formatBytes(blob.size), statusLine }) +
        `<br><br><button id="dlBtn">${fmt(I18N.download_button || "Download {filename}", { filename })}</button>`,
        state
      );
      const dlBtn = document.getElementById("dlBtn");
      dlBtn.addEventListener("click", () => downloadBlob(blob, filename));
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
      pulseHighlight(dlBtn);
      finishedState = state;
    } catch (err) {
      console.error("[compress] failed:", err);
      setResult(
        fmt(I18N.err_generic || "<strong>Couldn't compress that image.</strong> {msg}. Try a different image, or switch format and try again.",
          { msg: err.message }),
        "error"
      );
    } finally {
      els.compressBtn.disabled = false;
      els.compressBtn.textContent = I18N.btn_compress_default || "Compress to target";
    }
    // Runs after the button label has already been restored above, so the
    // checkmark morph is the last thing to touch the button, not undone by
    // the finally block's textContent reset happening in the same tick.
    if (finishedState === "ok") celebrateSuccess(els.compressBtn, els.result);
  });
})();
