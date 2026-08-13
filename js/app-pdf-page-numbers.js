(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    fileInfo: document.getElementById("fileInfo"),
    positionSelect: document.getElementById("positionSelect"),
    formatSelect: document.getElementById("formatSelect"),
    startNumber: document.getElementById("startNumber"),
    fontSize: document.getElementById("fontSize"),
    applyBtn: document.getElementById("applyBtn"),
    result: document.getElementById("result"),
  };

  const ICON_OK =
    '<svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>';
  const ICON_ERR =
    '<svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>';

  const MARGIN = 24;

  let currentFile = null;
  let currentBytes = null;
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

  const CONTROLS = [els.positionSelect, els.formatSelect, els.startNumber, els.fontSize];

  function resetFileState() {
    currentFile = null;
    currentBytes = null;
    pageCount = 0;
    els.fileInfo.style.display = "none";
    CONTROLS.forEach((el) => { el.disabled = true; });
    els.applyBtn.disabled = true;
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
      const bytes = await file.arrayBuffer();
      const doc = await PDFLib.PDFDocument.load(bytes);
      currentFile = file;
      currentBytes = bytes;
      pageCount = doc.getPageCount();
      els.fileInfo.textContent = `${file.name} — ${pageCount} page${pageCount === 1 ? "" : "s"}, ${formatBytes(file.size)}`;
      els.fileInfo.style.display = "block";
      CONTROLS.forEach((el) => { el.disabled = false; });
      els.applyBtn.disabled = false;
    } catch (err) {
      resetFileState();
      const msg = (err && err.message) || "";
      const reason = /encrypt/i.test(msg)
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

  function formatLabel(format, num, total) {
    switch (format) {
      case "page-n": return `Page ${num}`;
      case "page-n-of-total": return `Page ${num} of ${total}`;
      case "n-slash-total": return `${num} / ${total}`;
      default: return `${num}`;
    }
  }

  // Computes the draw origin (baseline x/y) for a given position keyword,
  // page size, and rendered text width, with a fixed margin from the edge.
  function positionFor(position, pageWidth, pageHeight, textWidth, fontSize) {
    let x;
    if (position.endsWith("left")) x = MARGIN;
    else if (position.endsWith("right")) x = pageWidth - MARGIN - textWidth;
    else x = (pageWidth - textWidth) / 2;

    const y = position.startsWith("top") ? pageHeight - MARGIN - fontSize : MARGIN;
    return { x, y };
  }

  els.applyBtn.addEventListener("click", async () => {
    if (!currentBytes) return;
    const busyText = startBusyText(els.applyBtn, "Adding");
    let finishedOk = false;
    let outBlob = null;
    let outName = "";

    try {
      const startNum = parseInt(els.startNumber.value, 10);
      const fontSize = parseInt(els.fontSize.value, 10);
      if (isNaN(startNum)) throw new Error("Starting number isn't valid.");
      if (isNaN(fontSize) || fontSize < 6 || fontSize > 72) throw new Error("Font size must be between 6 and 72.");

      const format = els.formatSelect.value;
      const position = els.positionSelect.value;

      const doc = await PDFLib.PDFDocument.load(currentBytes);
      const font = await doc.embedFont(PDFLib.StandardFonts.Helvetica);
      const pages = doc.getPages();

      pages.forEach((page, i) => {
        const num = startNum + i;
        const text = formatLabel(format, num, pageCount);
        const textWidth = font.widthOfTextAtSize(text, fontSize);
        const { x, y } = positionFor(position, page.getWidth(), page.getHeight(), textWidth, fontSize);
        page.drawText(text, { x, y, size: fontSize, font, color: PDFLib.rgb(0, 0, 0) });
      });

      const outBytes = await doc.save();
      outBlob = new Blob([outBytes], { type: "application/pdf" });
      outName = `${baseName(currentFile.name)}-numbered.pdf`;
      downloadBlob(outBlob, outName);

      setResult(
        `${ICON_OK}<div class="r-body"><strong>Created ${escapeHtml(outName)}</strong> ` +
          `(${pageCount} page${pageCount === 1 ? "" : "s"} numbered, ${formatBytes(outBlob.size)}). ` +
          `Download started automatically.` +
          `<div><button type="button" id="dlAgainBtn" style="margin-top:12px;">Download again</button></div></div>`,
        "ok"
      );
      finishedOk = true;
    } catch (err) {
      setResult(
        `${ICON_ERR}<div class="r-body"><strong>Couldn't add page numbers.</strong> ${escapeHtml(err.message || "Something went wrong.")}</div>`,
        "error"
      );
    } finally {
      busyText.done();
    }

    if (finishedOk) {
      const dlAgainBtn = document.getElementById("dlAgainBtn");
      if (dlAgainBtn && outBlob) {
        dlAgainBtn.addEventListener("click", () => downloadBlob(outBlob, outName));
      }
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
      celebrateSuccess(els.applyBtn, els.result);
    } else {
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  });
})();
