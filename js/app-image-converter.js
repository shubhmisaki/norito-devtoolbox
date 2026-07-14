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
    // default target format to something different from the source, unless
    // a landing-page variant has locked the format select to a specific
    // target (data-lock="true"), e.g. a "JPG to PNG converter" page that
    // should keep defaulting to PNG no matter what gets uploaded.
    if (els.format.dataset.lock !== "true") {
      if (file.type === "image/png") els.format.value = "jpeg";
      else if (file.type === "image/jpeg") els.format.value = "webp";
      else els.format.value = "png";
    }
    updateQualityVisibility();
  }

  els.drop.addEventListener("click", () => els.fileInput.click());
  els.fileInput.addEventListener("change", (e) => {
    if (e.target.files.length > 1) startBatch(e.target.files);
    else if (e.target.files[0]) handleFile(e.target.files[0]);
  });
  ["dragenter", "dragover"].forEach((evt) =>
    els.drop.addEventListener(evt, (e) => { e.preventDefault(); els.drop.classList.add("drag"); })
  );
  ["dragleave", "drop"].forEach((evt) =>
    els.drop.addEventListener(evt, (e) => { e.preventDefault(); els.drop.classList.remove("drag"); })
  );
  els.drop.addEventListener("drop", (e) => {
    if (e.dataTransfer.files.length > 1) startBatch(e.dataTransfer.files);
    else if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
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

  // ---- Batch mode ----
  const batchEls = {
    list: document.getElementById("batchList"),
    actions: document.getElementById("batchActions"),
    convertBtn: document.getElementById("batchConvertBtn"),
    zipBtn: document.getElementById("batchZipBtn"),
  };
  let batchFiles = [];

  function escapeHtml(s) {
    return String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function renderBatchList() {
    if (!batchEls.list) return;
    batchEls.list.innerHTML = batchFiles
      .map((bf, i) => {
        const statusClass = bf.status === "ok" ? "ok" : bf.status === "error" ? "error" : "pending";
        const statusText = bf.status === "ok"
          ? `${formatBytes(bf.blob.size)}`
          : bf.status === "error"
          ? (bf.error || "Failed")
          : "Waiting...";
        return `<div class="batch-file-row" data-i="${i}">
          <span class="bf-name">${escapeHtml(bf.file.name)}</span>
          <span class="bf-meta bf-status ${statusClass}">${statusText}</span>
          <button type="button" class="bf-remove" data-i="${i}" aria-label="Remove">&times;</button>
        </div>`;
      })
      .join("");
    batchEls.list.querySelectorAll(".bf-remove").forEach((btn) => {
      btn.addEventListener("click", () => {
        const i = Number(btn.dataset.i);
        batchFiles.splice(i, 1);
        if (!batchFiles.length) {
          batchEls.list.style.display = "none";
          batchEls.actions.style.display = "none";
        } else {
          renderBatchList();
        }
      });
    });
  }

  function startBatch(fileList) {
    const files = Array.from(fileList).filter((f) => f.type.startsWith("image/"));
    if (!files.length) {
      setResult("<strong>No images found.</strong> Choose JPG, PNG, or WebP files.", "error");
      return;
    }
    batchFiles = files.map((file) => ({ file, status: "pending", blob: null, ext: "", error: "" }));
    els.originalInfo.style.display = "none";
    els.result.style.display = "none";
    els.preview.style.display = "none";
    if (els.previewHint) els.previewHint.style.display = "none";
    batchEls.list.style.display = "block";
    batchEls.actions.style.display = "flex";
    batchEls.zipBtn.disabled = true;
    renderBatchList();
  }

  async function runBatch() {
    batchEls.convertBtn.disabled = true;
    batchEls.convertBtn.textContent = "Converting...";
    const outFormat = els.format.value;
    const mime = { jpeg: "image/jpeg", png: "image/png", webp: "image/webp" }[outFormat];
    const quality = outFormat === "png" ? undefined : Number(els.quality.value) / 100;
    const ext = { jpeg: "jpg", png: "png", webp: "webp" }[outFormat];
    for (const bf of batchFiles) {
      try {
        const img = await loadImageFile(bf.file);
        const canvas = document.createElement("canvas");
        canvas.width = img.width;
        canvas.height = img.height;
        const ctx = canvas.getContext("2d");
        if (outFormat === "jpeg") {
          ctx.fillStyle = "#ffffff";
          ctx.fillRect(0, 0, canvas.width, canvas.height);
        }
        ctx.drawImage(img, 0, 0);
        const blob = await canvasToBlob(canvas, mime, quality);
        bf.blob = blob;
        bf.ext = ext;
        bf.status = "ok";
      } catch (err) {
        bf.status = "error";
        bf.error = err.message || "Couldn't convert";
      }
      renderBatchList();
    }
    batchEls.convertBtn.disabled = false;
    batchEls.convertBtn.textContent = "Convert all";
    const anyOk = batchFiles.some((bf) => bf.status === "ok");
    batchEls.zipBtn.disabled = !anyOk;
    if (anyOk) celebrateSuccess(batchEls.convertBtn, batchEls.list, "Done");
  }

  if (batchEls.convertBtn) batchEls.convertBtn.addEventListener("click", runBatch);
  if (batchEls.zipBtn) {
    batchEls.zipBtn.addEventListener("click", async () => {
      const entries = [];
      for (const bf of batchFiles) {
        if (bf.status !== "ok" || !bf.blob) continue;
        const base = (bf.file.name || "image").replace(/\.[^.]+$/, "");
        const bytes = new Uint8Array(await bf.blob.arrayBuffer());
        entries.push({ name: `${base}.${bf.ext}`, bytes });
      }
      if (!entries.length) return;
      const zipBytes = createZip(entries);
      const blob = new Blob([zipBytes], { type: "application/zip" });
      downloadBlob(blob, "converted-images.zip");
      celebrateSuccess(batchEls.zipBtn, batchEls.list, "Downloaded");
    });
  }
})();
