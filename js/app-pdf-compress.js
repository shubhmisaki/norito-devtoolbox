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
    dpiSelect: document.getElementById("dpiSelect"),
    qualitySelect: document.getElementById("qualitySelect"),
    compressBtn: document.getElementById("compressBtn"),
    result: document.getElementById("result"),
  };

  const ICON_OK =
    '<svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>';
  const ICON_ERR =
    '<svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>';

  let currentFile = null;
  let currentPdf = null; // pdfjsLib PDFDocumentProxy
  let pageCount = 0;

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

  const CONTROLS = [els.dpiSelect, els.qualitySelect];

  function resetFileState() {
    currentFile = null;
    currentPdf = null;
    pageCount = 0;
    els.fileInfo.style.display = "none";
    CONTROLS.forEach((el) => { el.disabled = true; });
    els.compressBtn.disabled = true;
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
    els.result.style.display = "none";
    try {
      const bytes = new Uint8Array(await file.arrayBuffer());
      const doc = await pdfjsLib.getDocument({ data: bytes }).promise;
      currentFile = file;
      currentPdf = doc;
      pageCount = doc.numPages;
      els.fileInfo.textContent = `${file.name} — ${pageCount} page${pageCount === 1 ? "" : "s"}, ${formatBytes(file.size)}`;
      els.fileInfo.style.display = "block";
      CONTROLS.forEach((el) => { el.disabled = false; });
      els.compressBtn.disabled = false;
    } catch (err) {
      resetFileState();
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

  ["dragenter", "dragover"].forEach((evt) =>
    els.drop.addEventListener(evt, (e) => {
      e.preventDefault();
      els.drop.classList.add("drag");
    })
  );
  ["dragleave", "drop"].forEach((evt) =>
    els.drop.addEventListener(evt, (e) => {
      e.preventDefault();
      els.drop.classList.remove("drag");
    })
  );
  els.drop.addEventListener("drop", (e) => {
    if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]) {
      loadFile(e.dataTransfer.files[0]);
    }
  });

  // Renders one page to a JPEG blob at the given DPI/quality, and also
  // returns the page's original (unscaled) width/height in PDF points so
  // the rebuilt page can be sized to match the source exactly.
  async function renderPageToJpeg(pageNumber, scale, quality) {
    const page = await currentPdf.getPage(pageNumber);
    const baseViewport = page.getViewport({ scale: 1 });
    const viewport = page.getViewport({ scale });
    const canvas = document.createElement("canvas");
    canvas.width = Math.max(1, Math.ceil(viewport.width));
    canvas.height = Math.max(1, Math.ceil(viewport.height));
    const ctx = canvas.getContext("2d");
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    await page.render({ canvasContext: ctx, viewport }).promise;
    const blob = await new Promise((resolve) => canvas.toBlob(resolve, "image/jpeg", quality));
    if (!blob) throw new Error(`Couldn't render page ${pageNumber}.`);
    const bytes = new Uint8Array(await blob.arrayBuffer());
    return { bytes, width: baseViewport.width, height: baseViewport.height };
  }

  const DEFAULT_LABEL = els.compressBtn.innerHTML;

  els.compressBtn.addEventListener("click", async () => {
    if (!currentPdf || !currentFile) return;
    els.compressBtn.disabled = true;
    els.compressBtn.textContent = "Compressing...";
    let finishedOk = false;
    let outBlob = null;
    let outName = "";

    try {
      const dpi = parseInt(els.dpiSelect.value, 10);
      const quality = parseFloat(els.qualitySelect.value);
      const scale = dpi / 72; // PDF user space defaults to 72 units per inch

      const outDoc = await PDFLib.PDFDocument.create();

      for (let pageNumber = 1; pageNumber <= pageCount; pageNumber++) {
        const { bytes, width, height } = await renderPageToJpeg(pageNumber, scale, quality);
        const jpg = await outDoc.embedJpg(bytes);
        const page = outDoc.addPage([width, height]);
        page.drawImage(jpg, { x: 0, y: 0, width, height });
      }

      const outBytes = await outDoc.save();
      outBlob = new Blob([outBytes], { type: "application/pdf" });
      outName = `${baseName(currentFile.name)}-compressed.pdf`;
      downloadBlob(outBlob, outName);

      const originalSize = currentFile.size;
      const newSize = outBlob.size;
      const pct = originalSize > 0 ? Math.round((1 - newSize / originalSize) * 100) : 0;
      const sizeLine =
        pct > 0
          ? `${formatBytes(originalSize)} &rarr; ${formatBytes(newSize)} (about ${pct}% smaller).`
          : `${formatBytes(originalSize)} &rarr; ${formatBytes(newSize)}. This particular PDF didn't get smaller, it was likely already efficient (e.g. mostly text).`;

      setResult(
        `${ICON_OK}<div class="r-body"><strong>Created ${escapeHtml(outName)}</strong><br>` +
          `${sizeLine} Download started automatically.` +
          `<div><button type="button" id="dlAgainBtn" style="margin-top:12px;">Download again</button></div></div>`,
        "ok"
      );
      finishedOk = true;
    } catch (err) {
      setResult(
        `${ICON_ERR}<div class="r-body"><strong>Couldn't compress this PDF.</strong> ${escapeHtml(err.message || "Something went wrong.")}</div>`,
        "error"
      );
    } finally {
      els.compressBtn.disabled = !currentPdf;
      els.compressBtn.innerHTML = DEFAULT_LABEL;
    }

    if (finishedOk) {
      const dlAgainBtn = document.getElementById("dlAgainBtn");
      if (dlAgainBtn && outBlob) {
        dlAgainBtn.addEventListener("click", () => downloadBlob(outBlob, outName));
      }
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
      celebrateSuccess(els.compressBtn, els.result);
    } else {
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  });
})();
