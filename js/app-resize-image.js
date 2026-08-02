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

  async function handleFile(file) {
    if (!file || !file.type.startsWith("image/")) {
      setResult("<strong>That's not an image.</strong> Choose a JPG, PNG, or WebP file.", "error");
      return;
    }
    currentFile = file;
    const { img, url } = await loadImageFile(file);
    currentImg = img;
    URL.revokeObjectURL(url); // only used to decode; canvas draws below don't need it alive
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
  els.fileInput.addEventListener("change", (e) => {
    if (e.target.files.length > 1) startBatch(e.target.files);
    else if (e.target.files[0]) handleFile(e.target.files[0]);
  });
  wireDragDrop(els.drop, (e) => {
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

  function targetDimsFor(img) {
    if (els.mode.value === "exact") {
      const w = Math.max(1, Math.round(Number(els.width.value) || 0));
      const h = Math.max(1, Math.round(Number(els.height.value) || 0));
      return { w, h };
    }
    const pct = Math.max(1, Number(els.percent.value) || 100) / 100;
    return {
      w: Math.max(1, Math.round(img.width * pct)),
      h: Math.max(1, Math.round(img.height * pct)),
    };
  }
  function targetDims() {
    return targetDimsFor(currentImg);
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

  // ---- Batch mode ----
  const batchEls = {
    list: document.getElementById("batchList"),
    actions: document.getElementById("batchActions"),
    resizeBtn: document.getElementById("batchResizeBtn"),
    zipBtn: document.getElementById("batchZipBtn"),
  };
  let batchFiles = [];

  function renderBatchList() {
    if (!batchEls.list) return;
    batchEls.list.innerHTML = batchFiles
      .map((bf, i) => {
        const statusClass = bf.status === "ok" ? "ok" : bf.status === "error" ? "error" : "pending";
        const statusText = bf.status === "ok"
          ? `${bf.w}×${bf.h}, ${formatBytes(bf.blob.size)}`
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

  function escapeHtml(s) {
    return String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function startBatch(fileList) {
    const files = Array.from(fileList).filter((f) => f.type.startsWith("image/"));
    if (!files.length) {
      setResult("<strong>No images found.</strong> Choose JPG, PNG, or WebP files.", "error");
      return;
    }
    batchFiles = files.map((file) => ({ file, status: "pending", blob: null, w: 0, h: 0, error: "" }));
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
    batchEls.resizeBtn.disabled = true;
    batchEls.resizeBtn.textContent = "Resizing...";
    for (const bf of batchFiles) {
      try {
        const { img, url } = await loadImageFile(bf.file);
        URL.revokeObjectURL(url);
        const { w, h } = targetDimsFor(img);
        const canvas = document.createElement("canvas");
        canvas.width = w;
        canvas.height = h;
        canvas.getContext("2d").drawImage(img, 0, 0, w, h);

        const outFormat = els.format.value === "keep"
          ? (bf.file.type === "image/png" ? "png" : bf.file.type === "image/webp" ? "webp" : "jpeg")
          : els.format.value;
        const mime = { jpeg: "image/jpeg", png: "image/png", webp: "image/webp" }[outFormat];
        const blob = await canvasToBlob(canvas, mime, outFormat === "png" ? undefined : 0.92);

        bf.blob = blob;
        bf.w = w;
        bf.h = h;
        bf.ext = { jpeg: "jpg", png: "png", webp: "webp" }[outFormat];
        bf.status = "ok";
      } catch (err) {
        bf.status = "error";
        bf.error = err.message || "Couldn't resize";
      }
      renderBatchList();
    }
    batchEls.resizeBtn.disabled = false;
    batchEls.resizeBtn.textContent = "Resize all";
    const anyOk = batchFiles.some((bf) => bf.status === "ok");
    batchEls.zipBtn.disabled = !anyOk;
    if (anyOk) celebrateSuccess(batchEls.resizeBtn, batchEls.list, "Done");
  }

  if (batchEls.resizeBtn) batchEls.resizeBtn.addEventListener("click", runBatch);
  if (batchEls.zipBtn) {
    batchEls.zipBtn.addEventListener("click", async () => {
      const entries = [];
      for (const bf of batchFiles) {
        if (bf.status !== "ok" || !bf.blob) continue;
        const base = (bf.file.name || "image").replace(/\.[^.]+$/, "");
        const bytes = new Uint8Array(await bf.blob.arrayBuffer());
        entries.push({ name: `${base}-${bf.w}x${bf.h}.${bf.ext}`, bytes });
      }
      if (!entries.length) return;
      const zipBytes = createZip(entries);
      const blob = new Blob([zipBytes], { type: "application/zip" });
      downloadBlob(blob, "resized-images.zip");
      celebrateSuccess(batchEls.zipBtn, batchEls.list, "Downloaded");
    });
  }
})();
