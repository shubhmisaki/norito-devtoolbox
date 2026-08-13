import * as pdfjsLib from "./vendor/pdfjs/pdf.min.mjs";

pdfjsLib.GlobalWorkerOptions.workerSrc = new URL(
  "./vendor/pdfjs/pdf.worker.min.mjs",
  import.meta.url
).href;

(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    fileInfo: document.getElementById("fileInfo"),
    loadingInfo: document.getElementById("loadingInfo"),
    thumbGrid: document.getElementById("thumbGrid"),
    saveBtn: document.getElementById("saveBtn"),
    result: document.getElementById("result"),
  };

  const ICON_UP =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m18 15-6-6-6 6"/></svg>';
  const ICON_DOWN =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>';
  const ICON_X =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>';
  const ICON_RESTORE =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/></svg>';
  const ICON_OK =
    '<svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>';
  const ICON_ERR =
    '<svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>';

  const THUMB_TARGET_WIDTH = 160;

  let currentFile = null;
  let currentBytes = null;
  let pageCount = 0;
  let pages = []; // [{ originalIndex, removed }], in current display order
  let thumbCache = new Map(); // originalIndex -> data URL

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    }[c]));
  }

  function baseName(filename) {
    return filename.replace(/\.pdf$/i, "") || "document";
  }

  function setResult(html, state) {
    els.result.innerHTML = html;
    els.result.style.display = "flex";
    els.result.classList.remove("ok", "error");
    if (state) els.result.classList.add(state);
  }

  function resetState() {
    currentFile = null;
    currentBytes = null;
    pageCount = 0;
    pages = [];
    thumbCache = new Map();
    els.fileInfo.style.display = "none";
    els.loadingInfo.style.display = "none";
    els.thumbGrid.style.display = "none";
    els.thumbGrid.innerHTML = "";
    els.saveBtn.disabled = true;
  }

  function remainingCount() {
    return pages.filter((p) => !p.removed).length;
  }

  function render() {
    if (pages.length === 0) {
      els.thumbGrid.style.display = "none";
      els.thumbGrid.innerHTML = "";
      els.saveBtn.disabled = true;
      return;
    }
    els.thumbGrid.style.display = "grid";
    els.thumbGrid.innerHTML = pages
      .map((p, i) => {
        const src = thumbCache.get(p.originalIndex) || "";
        return `
        <div class="thumb-card${p.removed ? " removed" : ""}" data-index="${i}">
          <div class="thumb-card-canvas-wrap">
            ${src ? `<img src="${src}" alt="Page ${p.originalIndex + 1}" />` : ""}
          </div>
          <div class="thumb-card-badge">${i + 1}</div>
          <button type="button" class="thumb-card-remove" data-index="${i}" aria-label="${p.removed ? "Restore page" : "Remove page"}">
            ${p.removed ? ICON_RESTORE : ICON_X}
          </button>
          <div class="thumb-card-actions">
            <button type="button" class="mv-up" data-index="${i}" ${i === 0 ? "disabled" : ""} aria-label="Move up">${ICON_UP}</button>
            <button type="button" class="mv-down" data-index="${i}" ${i === pages.length - 1 ? "disabled" : ""} aria-label="Move down">${ICON_DOWN}</button>
          </div>
        </div>`;
      })
      .join("");
    els.saveBtn.disabled = remainingCount() < 1;
  }

  els.thumbGrid.addEventListener("click", (e) => {
    const btn = e.target.closest("button");
    if (!btn) return;
    const idx = Number(btn.dataset.index);
    if (btn.classList.contains("mv-up")) {
      if (idx > 0) {
        const tmp = pages[idx];
        pages[idx] = pages[idx - 1];
        pages[idx - 1] = tmp;
        render();
      }
    } else if (btn.classList.contains("mv-down")) {
      if (idx < pages.length - 1) {
        const tmp = pages[idx];
        pages[idx] = pages[idx + 1];
        pages[idx + 1] = tmp;
        render();
      }
    } else if (btn.classList.contains("thumb-card-remove")) {
      pages[idx].removed = !pages[idx].removed;
      render();
    }
  });

  async function renderThumbnails(pdfDoc) {
    for (let i = 1; i <= pdfDoc.numPages; i++) {
      if (pdfDoc.numPages > 1) {
        els.loadingInfo.textContent = `Rendering page thumbnails... ${i}/${pdfDoc.numPages}`;
      }
      const page = await pdfDoc.getPage(i);
      const baseViewport = page.getViewport({ scale: 1 });
      const scale = THUMB_TARGET_WIDTH / baseViewport.width;
      const viewport = page.getViewport({ scale });
      const canvas = document.createElement("canvas");
      canvas.width = Math.max(1, Math.ceil(viewport.width));
      canvas.height = Math.max(1, Math.ceil(viewport.height));
      const ctx = canvas.getContext("2d");
      ctx.fillStyle = "#ffffff";
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      await page.render({ canvasContext: ctx, viewport }).promise;
      thumbCache.set(i - 1, canvas.toDataURL("image/jpeg", 0.75));
    }
  }

  async function loadFile(file) {
    if (!file) return;
    if (file.type !== "application/pdf" && !/\.pdf$/i.test(file.name)) {
      setResult(
        `${ICON_ERR}<div class="r-body"><strong>That's not a PDF.</strong> Choose a .pdf file.</div>`,
        "error"
      );
      return;
    }
    resetState();
    els.result.style.display = "none";
    try {
      const bytes = new Uint8Array(await file.arrayBuffer());
      const pdfDoc = await pdfjsLib.getDocument({ data: bytes.slice() }).promise;
      currentFile = file;
      currentBytes = bytes;
      pageCount = pdfDoc.numPages;
      pages = Array.from({ length: pageCount }, (_, i) => ({ originalIndex: i, removed: false }));

      els.fileInfo.textContent = `${file.name} — ${pageCount} page${pageCount === 1 ? "" : "s"}, ${formatBytes(file.size)}`;
      els.fileInfo.style.display = "block";
      els.loadingInfo.style.display = "block";

      await renderThumbnails(pdfDoc);

      els.loadingInfo.style.display = "none";
      render();
    } catch (err) {
      resetState();
      const isPassword = err && err.name === "PasswordException";
      const reason = isPassword
        ? "It's password protected, remove the password first."
        : "It doesn't look like a valid PDF.";
      setResult(
        `${ICON_ERR}<div class="r-body"><strong>Couldn't read "${escapeHtml(file.name)}".</strong> ${reason}</div>`,
        "error"
      );
    }
  }

  els.drop.addEventListener("click", () => els.fileInput.click());
  els.fileInput.addEventListener("change", () => {
    loadFile(els.fileInput.files[0]);
    els.fileInput.value = "";
  });

  wireDragDrop(els.drop, (e) => {
    if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]) {
      loadFile(e.dataTransfer.files[0]);
    }
  });

  els.saveBtn.addEventListener("click", async () => {
    if (!currentBytes || remainingCount() < 1) return;
    const busyText = startBusyText(els.saveBtn, "Saving");
    let finishedOk = false;
    let outBlob = null;
    let outName = "";

    try {
      const finalOrder = pages.filter((p) => !p.removed).map((p) => p.originalIndex);
      const src = await PDFLib.PDFDocument.load(currentBytes);
      const out = await PDFLib.PDFDocument.create();
      const copied = await out.copyPages(src, finalOrder);
      copied.forEach((p) => out.addPage(p));
      const outBytes = await out.save();

      outBlob = new Blob([outBytes], { type: "application/pdf" });
      outName = `${baseName(currentFile.name)}-organized.pdf`;
      downloadBlob(outBlob, outName);

      const removedCount = pageCount - finalOrder.length;
      setResult(
        `${ICON_OK}<div class="r-body"><strong>Created ${escapeHtml(outName)}</strong> ` +
          `(${finalOrder.length} of ${pageCount} pages kept${removedCount ? `, ${removedCount} removed` : ""}, ${formatBytes(outBlob.size)}). ` +
          `Download started automatically.` +
          `<div><button type="button" id="dlAgainBtn" style="margin-top:12px;">Download again</button></div></div>`,
        "ok"
      );
      finishedOk = true;
    } catch (err) {
      setResult(
        `${ICON_ERR}<div class="r-body"><strong>Couldn't save this PDF.</strong> ${escapeHtml(err.message || "Something went wrong.")}</div>`,
        "error"
      );
    } finally {
      busyText.done();
      els.saveBtn.disabled = remainingCount() < 1;
    }

    if (finishedOk) {
      const dlAgainBtn = document.getElementById("dlAgainBtn");
      if (dlAgainBtn && outBlob) {
        dlAgainBtn.addEventListener("click", () => downloadBlob(outBlob, outName));
      }
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
      celebrateSuccess(els.saveBtn, els.result);
    } else {
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  });
})();
