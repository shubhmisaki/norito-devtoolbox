(function () {
  const I18N = i18nFor("app-qrcode");
  const els = {
    text: document.getElementById("qrText"),
    ecLevel: document.getElementById("ecLevel"),
    fg: document.getElementById("fgColor"),
    bg: document.getElementById("bgColor"),
    size: document.getElementById("qrSize"),
    sizeInput: document.getElementById("qrSizeInput"),
    logoInput: document.getElementById("logoInput"),
    logoClear: document.getElementById("logoClear"),
    logoDropzone: document.getElementById("logoDropzone"),
    canvas: document.getElementById("qrCanvas"),
    status: document.getElementById("qrStatus"),
    downloadPngBtn: document.getElementById("downloadPngBtn"),
    downloadSvgBtn: document.getElementById("downloadSvgBtn"),
  };

  let logoImg = null;
  let lastMatrix = null;
  let lastModuleCount = 0;

  // Remember the error-correction level between visits: nice-to-have only,
  // silently no-ops if localStorage is unavailable.
  const PREFS_KEY = "norito:qr-code-generator";
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
    if (p.ecLevel) els.ecLevel.value = p.ecLevel;
  })();

  function setStatus(msg, isError) {
    if (!msg) { els.status.style.display = "none"; return; }
    els.status.textContent = msg;
    els.status.style.display = "block";
    els.status.classList.toggle("error", !!isError);
  }

  function buildMatrix(text, ecLevel) {
    // typeNumber 0 = auto-detect the smallest QR version that fits.
    const qr = qrcode(0, ecLevel);
    qr.addData(text);
    qr.make();
    const count = qr.getModuleCount();
    const matrix = [];
    for (let r = 0; r < count; r++) {
      const row = [];
      for (let c = 0; c < count; c++) row.push(qr.isDark(r, c));
      matrix.push(row);
    }
    return { matrix, count };
  }

  function drawToCanvas(matrix, count, size, fg, bg) {
    const canvas = els.canvas;
    canvas.width = size;
    canvas.height = size;
    const ctx = canvas.getContext("2d");
    const cell = size / count;

    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, size, size);
    ctx.fillStyle = fg;
    for (let r = 0; r < count; r++) {
      for (let c = 0; c < count; c++) {
        if (matrix[r][c]) ctx.fillRect(c * cell, r * cell, Math.ceil(cell), Math.ceil(cell));
      }
    }

    if (logoImg) {
      const logoSize = size * 0.22;
      const pad = logoSize * 0.16;
      const cx = (size - logoSize) / 2;
      const cy = (size - logoSize) / 2;
      ctx.fillStyle = bg;
      ctx.fillRect(cx - pad, cy - pad, logoSize + pad * 2, logoSize + pad * 2);
      ctx.drawImage(logoImg, cx, cy, logoSize, logoSize);
    }
  }

  function buildSvg(matrix, count, fg, bg) {
    const cell = 10;
    const size = count * cell;
    let rects = "";
    for (let r = 0; r < count; r++) {
      for (let c = 0; c < count; c++) {
        if (matrix[r][c]) rects += `<rect x="${c * cell}" y="${r * cell}" width="${cell}" height="${cell}"/>`;
      }
    }
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${size} ${size}" width="${size}" height="${size}">` +
      `<rect width="${size}" height="${size}" fill="${bg}"/>` +
      `<g fill="${fg}">${rects}</g></svg>`;
  }

  function render() {
    const text = els.text.value.trim();
    if (!text) {
      setStatus(I18N.prompt_enter_text || "Type a URL or some text to generate a QR code.", false);
      lastMatrix = null;
      const ctx = els.canvas.getContext("2d");
      ctx.clearRect(0, 0, els.canvas.width, els.canvas.height);
      return;
    }
    try {
      const { matrix, count } = buildMatrix(text, els.ecLevel.value);
      lastMatrix = matrix;
      lastModuleCount = count;
      const size = parseInt(els.size.value, 10);
      drawToCanvas(matrix, count, size, els.fg.value, els.bg.value);
      setStatus("", false);
    } catch (e) {
      lastMatrix = null;
      setStatus(I18N.err_too_much_text || "Too much text for a single QR code. Try shortening it.", true);
    }
  }

  els.text.addEventListener("input", render);
  els.ecLevel.addEventListener("change", () => { savePref("ecLevel", els.ecLevel.value); render(); });
  els.fg.addEventListener("input", render);
  els.bg.addEventListener("input", render);
  // Size is editable two ways: drag the slider, or type an exact value.
  // Typing is clamped only on blur, not on every keystroke, so the field
  // can be cleared and retyped without fighting the user.
  const SIZE_MIN = parseInt(els.size.min, 10) || 160;
  const SIZE_MAX = parseInt(els.size.max, 10) || 1000;
  els.size.addEventListener("input", () => {
    els.sizeInput.value = els.size.value;
    render();
  });
  els.sizeInput.addEventListener("input", () => {
    const n = parseInt(els.sizeInput.value, 10);
    if (!Number.isFinite(n)) return;
    els.size.value = Math.max(SIZE_MIN, Math.min(SIZE_MAX, n));
    render();
  });
  els.sizeInput.addEventListener("blur", () => {
    const n = parseInt(els.sizeInput.value, 10);
    els.sizeInput.value = Number.isFinite(n)
      ? Math.max(SIZE_MIN, Math.min(SIZE_MAX, n))
      : els.size.value;
  });

  function loadLogoFile(file) {
    if (!file || !file.type.startsWith("image/")) {
      setStatus(I18N.err_not_an_image || "That doesn't look like an image file. Try a PNG, JPG, or SVG.", true);
      return;
    }
    const img = new Image();
    img.onload = () => { logoImg = img; render(); };
    img.onerror = () => setStatus(I18N.err_load_failed || "Couldn't load that image. Try a different file.", true);
    img.src = URL.createObjectURL(file);
  }

  els.logoInput.addEventListener("change", (e) => loadLogoFile(e.target.files[0]));

  ["dragenter", "dragover"].forEach((evt) =>
    els.logoDropzone.addEventListener(evt, (e) => {
      e.preventDefault();
      els.logoDropzone.classList.add("drag-active");
    })
  );
  ["dragleave", "drop"].forEach((evt) =>
    els.logoDropzone.addEventListener(evt, (e) => {
      e.preventDefault();
      els.logoDropzone.classList.remove("drag-active");
    })
  );
  els.logoDropzone.addEventListener("drop", (e) => {
    const file = e.dataTransfer.files[0];
    if (file) loadLogoFile(file);
  });

  els.logoClear.addEventListener("click", () => {
    logoImg = null;
    els.logoInput.value = "";
    render();
  });

  els.downloadPngBtn.addEventListener("click", () => {
    if (!lastMatrix) return;
    els.canvas.toBlob((blob) => {
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "qr-code.png";
      document.body.appendChild(a);
      a.click();
      a.remove();
      setTimeout(() => URL.revokeObjectURL(url), 2000);
      celebrateSuccess(els.downloadPngBtn);
    });
  });

  els.downloadSvgBtn.addEventListener("click", () => {
    if (!lastMatrix) return;
    const svg = buildSvg(lastMatrix, lastModuleCount, els.fg.value, els.bg.value);
    const blob = new Blob([svg], { type: "image/svg+xml" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "qr-code.svg";
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 2000);
    celebrateSuccess(els.downloadSvgBtn);
  });

  render();
})();
