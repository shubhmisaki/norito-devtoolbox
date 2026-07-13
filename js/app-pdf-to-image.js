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
    formatSelect: document.getElementById("formatSelect"),
    qualityField: document.getElementById("qualityField"),
    qualitySelect: document.getElementById("qualitySelect"),
    dpiSelect: document.getElementById("dpiSelect"),
    pagesInput: document.getElementById("pagesInput"),
    convertBtn: document.getElementById("convertBtn"),
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

  function updateQualityVisibility() {
    const isJpg = els.formatSelect.value === "jpg";
    els.qualityField.style.display = isJpg ? "" : "none";
  }
  els.formatSelect.addEventListener("change", updateQualityVisibility);
  updateQualityVisibility();

  function resetFileState() {
    currentFile = null;
    currentPdf = null;
    pageCount = 0;
    els.fileInfo.style.display = "none";
    [els.formatSelect, els.qualitySelect, els.dpiSelect, els.pagesInput].forEach((el) => {
      el.disabled = true;
    });
    els.pagesInput.value = "";
    els.convertBtn.disabled = true;
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
      [els.formatSelect, els.qualitySelect, els.dpiSelect, els.pagesInput].forEach((el) => {
        el.disabled = false;
      });
      els.convertBtn.disabled = false;
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

  // Parses "1-3, 5, 8-10" into a flat, deduplicated, sorted array of
  // 1-based page numbers (pdf.js's getPage() is 1-based). Returns null for
  // a blank string, meaning "every page", same convention as Split/Rotate.
  function parsePages(str, maxPage) {
    const trimmed = (str || "").trim();
    if (!trimmed) return null;
    const segments = trimmed.split(",").map((s) => s.trim()).filter(Boolean);
    if (segments.length === 0) return null;
    const set = new Set();
    segments.forEach((seg) => {
      const m = seg.match(/^(\d+)(?:-(\d+))?$/);
      if (!m) throw new Error(`"${seg}" isn't a valid page or range.`);
      let start = parseInt(m[1], 10);
      let end = m[2] ? parseInt(m[2], 10) : start;
      if (start > end) { const t = start; start = end; end = t; }
      if (start < 1 || end > maxPage) {
        throw new Error(`"${seg}" is out of range, this PDF has ${maxPage} page${maxPage === 1 ? "" : "s"}.`);
      }
      for (let p = start; p <= end; p++) set.add(p);
    });
    return Array.from(set).sort((a, b) => a - b);
  }

  async function renderPageToBlob(pageNumber, scale, format, quality) {
    const page = await currentPdf.getPage(pageNumber);
    const viewport = page.getViewport({ scale });
    const canvas = document.createElement("canvas");
    canvas.width = Math.max(1, Math.ceil(viewport.width));
    canvas.height = Math.max(1, Math.ceil(viewport.height));
    const ctx = canvas.getContext("2d");
    if (format === "jpg") {
      // JPEG has no alpha channel, fill white first so transparent PDF
      // backgrounds don't render as black.
      ctx.fillStyle = "#ffffff";
      ctx.fillRect(0, 0, canvas.width, canvas.height);
    }
    await page.render({ canvasContext: ctx, viewport }).promise;
    const mime = format === "jpg" ? "image/jpeg" : "image/png";
    const blob = await new Promise((resolve) => canvas.toBlob(resolve, mime, quality));
    if (!blob) throw new Error(`Couldn't render page ${pageNumber}.`);
    return blob;
  }

  const DEFAULT_LABEL = els.convertBtn.innerHTML;

  els.convertBtn.addEventListener("click", async () => {
    if (!currentPdf) return;
    els.convertBtn.disabled = true;
    els.convertBtn.textContent = "Converting...";
    let finishedOk = false;
    let outBlob = null;
    let outName = "";

    try {
      const targets = parsePages(els.pagesInput.value, pageCount);
      const pageNumbers = targets === null ? Array.from({ length: pageCount }, (_, i) => i + 1) : targets;

      const format = els.formatSelect.value;
      const ext = format === "jpg" ? "jpg" : "png";
      const quality = parseFloat(els.qualitySelect.value);
      const dpi = parseInt(els.dpiSelect.value, 10);
      const scale = dpi / 72; // PDF user space defaults to 72 units per inch

      const base = baseName(currentFile.name);
      const outputs = [];
      for (const pageNumber of pageNumbers) {
        const blob = await renderPageToBlob(pageNumber, scale, format, quality);
        const bytes = new Uint8Array(await blob.arrayBuffer());
        outputs.push({ name: `${base}-page-${pageNumber}.${ext}`, bytes });
      }

      if (outputs.length === 1) {
        outBlob = new Blob([outputs[0].bytes], { type: format === "jpg" ? "image/jpeg" : "image/png" });
        outName = outputs[0].name;
      } else {
        const zipBytes = createZip(outputs);
        outBlob = new Blob([zipBytes], { type: "application/zip" });
        outName = `${base}-images.zip`;
      }
      downloadBlob(outBlob, outName);

      const summary =
        outputs.length === 1
          ? `<strong>Created ${escapeHtml(outName)}</strong> (${formatBytes(outBlob.size)}). Download started automatically.`
          : `<strong>Created ${outputs.length} images in ${escapeHtml(outName)}</strong> (${formatBytes(outBlob.size)}). Download started automatically.`;

      setResult(
        `${ICON_OK}<div class="r-body">${summary}` +
          `<div><button type="button" id="dlAgainBtn" style="margin-top:12px;">Download again</button></div></div>`,
        "ok"
      );
      finishedOk = true;
    } catch (err) {
      setResult(
        `${ICON_ERR}<div class="r-body"><strong>Couldn't convert this PDF.</strong> ${escapeHtml(err.message || "Something went wrong.")}</div>`,
        "error"
      );
    } finally {
      els.convertBtn.disabled = !currentPdf;
      els.convertBtn.innerHTML = DEFAULT_LABEL;
    }

    if (finishedOk) {
      const dlAgainBtn = document.getElementById("dlAgainBtn");
      if (dlAgainBtn && outBlob) {
        dlAgainBtn.addEventListener("click", () => downloadBlob(outBlob, outName));
      }
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
      celebrateSuccess(els.convertBtn, els.result);
    } else {
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  });
})();
