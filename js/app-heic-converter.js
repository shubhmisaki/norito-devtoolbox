(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    format: document.getElementById("format"),
    list: document.getElementById("batchList"),
    actions: document.getElementById("batchActions"),
    convertBtn: document.getElementById("batchConvertBtn"),
    zipBtn: document.getElementById("batchZipBtn"),
    status: document.getElementById("status"),
    preview: document.getElementById("preview"),
    previewHint: document.getElementById("previewHint"),
  };

  let files = []; // [{ file, status, blob, ext }]

  function renderList() {
    els.list.innerHTML = files
      .map((f, i) => {
        const statusHtml =
          f.status === "ok"
            ? `<span class="bf-status ok">${formatBytes(f.blob.size)}</span>`
            : f.status === "error"
            ? `<span class="bf-status error">Failed</span>`
            : `<span class="bf-status pending">Waiting</span>`;
        return `<div class="batch-file-row" data-idx="${i}">
          <span class="bf-name">${escapeHtml(f.file.name)}</span>
          <span class="bf-meta">${formatBytes(f.file.size)}</span>
          ${statusHtml}
          <button type="button" class="bf-remove" aria-label="Remove">&times;</button>
        </div>`;
      })
      .join("");
    els.list.style.display = files.length ? "flex" : "none";
    els.list.querySelectorAll(".bf-remove").forEach((btn) => {
      btn.addEventListener("click", () => {
        const idx = Number(btn.closest(".batch-file-row").dataset.idx);
        files.splice(idx, 1);
        renderList();
        els.zipBtn.disabled = !files.some((f) => f.status === "ok");
      });
    });
  }

  function escapeHtml(str) {
    const d = document.createElement("div");
    d.textContent = str;
    return d.innerHTML;
  }

  function addFiles(fileList) {
    const accepted = Array.from(fileList).filter(
      (f) => /\.(heic|heif)$/i.test(f.name) || /heic|heif/i.test(f.type)
    );
    if (!accepted.length) {
      els.status.textContent = "Those don't look like HEIC/HEIF files.";
      els.status.style.display = "block";
      return;
    }
    els.status.style.display = "none";
    files = files.concat(accepted.map((file) => ({ file, status: "pending", blob: null })));
    els.actions.style.display = "flex";
    els.zipBtn.disabled = true;
    renderList();
  }

  async function convertAll() {
    const toType = els.format.value;
    const ext = toType === "image/png" ? "png" : "jpg";
    els.convertBtn.disabled = true;
    let firstPreviewUrl = null;

    for (const f of files) {
      if (f.status === "ok") continue;
      try {
        const result = await heic2any({ blob: f.file, toType, quality: 0.92 });
        const blob = Array.isArray(result) ? result[0] : result;
        f.blob = blob;
        f.ext = ext;
        f.status = "ok";
        if (!firstPreviewUrl) firstPreviewUrl = URL.createObjectURL(blob);
      } catch (e) {
        f.status = "error";
      }
      renderList();
    }

    if (firstPreviewUrl) {
      els.preview.src = firstPreviewUrl;
      els.preview.style.display = "block";
      if (els.previewHint) els.previewHint.style.display = "none";
    }

    els.convertBtn.disabled = false;
    els.zipBtn.disabled = !files.some((f) => f.status === "ok");
  }

  els.fileInput.addEventListener("change", () => addFiles(els.fileInput.files));
  wireDragDrop(els.drop, (e) => addFiles(e.dataTransfer.files));
  els.drop.addEventListener("click", (e) => {
    if (e.target === els.fileInput) return;
    els.fileInput.click();
  });

  els.convertBtn.addEventListener("click", convertAll);

  els.zipBtn.addEventListener("click", async () => {
    const ok = files.filter((f) => f.status === "ok");
    if (!ok.length) return;
    const seen = new Map();
    const entries = [];
    for (const f of ok) {
      const base = f.file.name.replace(/\.[^.]+$/, "");
      let name = `${base}.${f.ext}`;
      const count = seen.get(name) || 0;
      seen.set(name, count + 1);
      if (count > 0) name = `${base}_${count}.${f.ext}`;
      entries.push({ name, bytes: new Uint8Array(await f.blob.arrayBuffer()) });
    }
    const zipBytes = createZip(entries);
    downloadBlob(new Blob([zipBytes], { type: "application/zip" }), "converted-photos.zip");
  });
})();
