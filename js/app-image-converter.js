(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    originalInfo: document.getElementById("originalInfo"),
    format: document.getElementById("format"),
    qualityRow: document.getElementById("qualityRow"),
    quality: document.getElementById("quality"),
    qualityValue: document.getElementById("qualityValue"),
    convertBtn: document.getElementById("convertBtn"),
    result: document.getElementById("result"),
    preview: document.getElementById("preview"),
    previewHint: document.getElementById("previewHint"),
  };

  let currentImg = null;
  let currentFile = null;

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

  function updateQualityVisibility() {
    const lossy = els.format.value === "jpeg" || els.format.value === "webp";
    els.qualityRow.style.display = lossy ? "flex" : "none";
  }
  els.format.addEventListener("change", updateQualityVisibility);
  updateQualityVisibility();

  els.quality.addEventListener("input", () => {
    els.qualityValue.textContent = `${els.quality.value}%`;
  });

  async function handleFile(file) {
    if (!file || !file.type.startsWith("image/")) {
      setResult("<strong>That's not an image.</strong> Choose a JPG, PNG, or WebP file.", "error");
      return;
    }
    currentFile = file;
    currentImg = await loadImageFile(file);
    els.originalInfo.textContent = `${file.name}, ${currentImg.width}×${currentImg.height}, ${formatBytes(file.size)}, ${file.type || "unknown type"}`;
    els.originalInfo.style.display = "block";
    els.convertBtn.disabled = false;
    els.result.style.display = "none";
    // default target format to something different from the source
    if (file.type === "image/png") els.format.value = "jpeg";
    else if (file.type === "image/jpeg") els.format.value = "webp";
    else els.format.value = "png";
    updateQualityVisibility();
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

  function canvasToBlob(canvas, mime, quality) {
    return new Promise((resolve) => canvas.toBlob(resolve, mime, quality));
  }

  els.convertBtn.addEventListener("click", async () => {
    if (!currentImg) return;
    els.convertBtn.disabled = true;
    els.convertBtn.textContent = "Converting...";
    try {
      const outFormat = els.format.value;
      const mime = { jpeg: "image/jpeg", png: "image/png", webp: "image/webp" }[outFormat];
      const canvas = document.createElement("canvas");
      canvas.width = currentImg.width;
      canvas.height = currentImg.height;
      const ctx = canvas.getContext("2d");
      // JPEG has no alpha channel; fill white first so transparent PNGs
      // converting to JPEG don't end up with black where alpha used to be.
      if (outFormat === "jpeg") {
        ctx.fillStyle = "#ffffff";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
      }
      ctx.drawImage(currentImg, 0, 0);
      const quality = outFormat === "png" ? undefined : Number(els.quality.value) / 100;
      const blob = await canvasToBlob(canvas, mime, quality);

      const url = URL.createObjectURL(blob);
      els.preview.src = url;
      els.preview.style.display = "block";
      if (els.previewHint) els.previewHint.style.display = "none";

      const ext = { jpeg: "jpg", png: "png", webp: "webp" }[outFormat];
      const base = (currentFile.name || "image").replace(/\.[^.]+$/, "");
      const filename = `${base}.${ext}`;

      setResult(
        `<strong>Converted to ${ext.toUpperCase()}.</strong> ${formatBytes(blob.size)} ` +
        `(was ${formatBytes(currentFile.size)}).<br><br>` +
        `<button id="dlBtn">Download ${filename}</button>`,
        "ok"
      );
      document.getElementById("dlBtn").addEventListener("click", () => downloadBlob(blob, filename));
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
      celebrateSuccess(els.convertBtn, els.result);
    } catch (err) {
      setResult(`<strong>Couldn't convert that image.</strong> ${err.message || "Try a different file."}`, "error");
    } finally {
      els.convertBtn.disabled = false;
      els.convertBtn.textContent = "Convert image";
    }
  });
})();
