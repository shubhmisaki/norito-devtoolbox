(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    originalInfo: document.getElementById("originalInfo"),
    mode: document.getElementById("mode"),
    width: document.getElementById("width"),
    height: document.getElementById("height"),
    percent: document.getElementById("percent"),
    exactFields: document.getElementById("exactFields"),
    percentFields: document.getElementById("percentFields"),
    lockRatio: document.getElementById("lockRatio"),
    format: document.getElementById("format"),
    resizeBtn: document.getElementById("resizeBtn"),
    result: document.getElementById("result"),
    preview: document.getElementById("preview"),
    previewHint: document.getElementById("previewHint"),
  };

  let currentImg = null;
  let currentFile = null;
  let aspectRatio = 1;
  let syncing = false;

  const ICONS = {
    ok: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="M22 4 12 14.01l-3-3"/></svg>',
    error: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>',
  };

  function setResult(html, state) {
    els.result.innerHTML = `<span class="r-icon">${ICONS[state] || ""}</span><span class="r-body">${html}</span>`;
    els.result.style.display = "flex";
    els.result.classList.remove("ok", "error");
    if (state) els.result.classList.add(state);
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
      setResult("<strong>That's not an image.</strong> Choose a JPG, PNG, or WebP file.", "error");
      return;
    }
    currentFile = file;
    currentImg = await loadImageFile(file);
    aspectRatio = currentImg.width / currentImg.height;
    els.originalInfo.textContent = `${file.name}, ${currentImg.width}×${currentImg.height}, ${formatBytes(file.size)}`;
    els.originalInfo.style.display = "block";
    syncing = true;
    els.width.value = currentImg.width;
    els.height.value = currentImg.height;
    syncing = false;
    els.resizeBtn.disabled = false;
    els.result.style.display = "none";
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

  function updateModeUI() {
    const exact = els.mode.value === "exact";
    els.exactFields.style.display = exact ? "flex" : "none";
    els.percentFields.style.display = exact ? "none" : "block";
  }
  els.mode.addEventListener("change", updateModeUI);
  updateModeUI();

  els.width.addEventListener("input", () => {
    if (syncing || !els.lockRatio.checked || !currentImg) return;
    syncing = true;
    els.height.value = Math.max(1, Math.round(Number(els.width.value) / aspectRatio));
    syncing = false;
  });
  els.height.addEventListener("input", () => {
    if (syncing || !els.lockRatio.checked || !currentImg) return;
    syncing = true;
    els.width.value = Math.max(1, Math.round(Number(els.height.value) * aspectRatio));
    syncing = false;
  });

  function canvasToBlob(canvas, mime, quality) {
    return new Promise((resolve) => canvas.toBlob(resolve, mime, quality));
  }

  function targetDims() {
    if (els.mode.value === "exact") {
      const w = Math.max(1, Math.round(Number(els.width.value) || 0));
      const h = Math.max(1, Math.round(Number(els.height.value) || 0));
      return { w, h };
    }
    const pct = Math.max(1, Number(els.percent.value) || 100) / 100;
    return {
      w: Math.max(1, Math.round(currentImg.width * pct)),
      h: Math.max(1, Math.round(currentImg.height * pct)),
    };
  }

  els.resizeBtn.addEventListener("click", async () => {
    if (!currentImg) return;
    const { w, h } = targetDims();
    if (!w || !h || w > 20000 || h > 20000) {
      setResult("<strong>Enter valid dimensions.</strong> Width and height must be between 1 and 20000 pixels.", "error");
      return;
    }
    els.resizeBtn.disabled = true;
    els.resizeBtn.textContent = "Resizing...";
    try {
      const canvas = document.createElement("canvas");
      canvas.width = w;
      canvas.height = h;
      canvas.getContext("2d").drawImage(currentImg, 0, 0, w, h);

      const outFormat = els.format.value === "keep"
        ? (currentFile.type === "image/png" ? "png" : currentFile.type === "image/webp" ? "webp" : "jpeg")
        : els.format.value;
      const mime = { jpeg: "image/jpeg", png: "image/png", webp: "image/webp" }[outFormat];
      const blob = await canvasToBlob(canvas, mime, outFormat === "png" ? undefined : 0.92);

      const url = URL.createObjectURL(blob);
      els.preview.src = url;
      els.preview.style.display = "block";
      if (els.previewHint) els.previewHint.style.display = "none";

      const ext = { jpeg: "jpg", png: "png", webp: "webp" }[outFormat];
      const base = (currentFile.name || "image").replace(/\.[^.]+$/, "");
      const filename = `${base}-${w}x${h}.${ext}`;

      setResult(
        `<strong>Resized to ${w}×${h}.</strong> ${formatBytes(blob.size)}.<br><br>` +
        `<button id="dlBtn">Download ${filename}</button>`,
        "ok"
      );
      document.getElementById("dlBtn").addEventListener("click", () => downloadBlob(blob, filename));
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
      celebrateSuccess(els.resizeBtn, els.result);
    } catch (err) {
      setResult(`<strong>Couldn't resize that image.</strong> ${err.message || "Try a different file."}`, "error");
    } finally {
      els.resizeBtn.disabled = false;
      els.resizeBtn.textContent = "Resize image";
    }
  });
})();
