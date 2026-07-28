(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    fileInfo: document.getElementById("fileInfo"),
    rotateTabs: document.getElementById("rotateTabs"),
    pagesInput: document.getElementById("pagesInput"),
    rotateBtn: document.getElementById("rotateBtn"),
    result: document.getElementById("result"),
  };

  const ICON_OK =
    '<svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>';
  const ICON_ERR =
    '<svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>';

  let currentFile = null;
  let currentBytes = null;
  let pageCount = 0;
  let rotateDelta = 90;

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

  function resetFileState() {
    currentFile = null;
    currentBytes = null;
    pageCount = 0;
    els.fileInfo.style.display = "none";
    els.pagesInput.disabled = true;
    els.pagesInput.value = "";
    els.rotateBtn.disabled = true;
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
      els.pagesInput.disabled = false;
      els.rotateBtn.disabled = false;
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

  els.rotateTabs.querySelectorAll(".tab").forEach((btn) => {
    btn.addEventListener("click", () => {
      els.rotateTabs.querySelectorAll(".tab").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      rotateDelta = parseInt(btn.dataset.value, 10);
    });
  });

  // Parses "1-3, 5, 8-10" into a flat, deduplicated array of 0-based page
  // indices. Returns null for a blank/whitespace-only string, meaning "all
  // pages", same convention as the Split PDF tool.
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
      for (let p = start; p <= end; p++) set.add(p - 1);
    });
    return Array.from(set).sort((a, b) => a - b);
  }

  const DEFAULT_LABEL = els.rotateBtn.innerHTML;

  els.rotateBtn.addEventListener("click", async () => {
    if (!currentBytes) return;
    els.rotateBtn.disabled = true;
    els.rotateBtn.textContent = "Rotating...";
    let finishedOk = false;
    let outBlob = null;
    let outName = "";

    try {
      const targets = parsePages(els.pagesInput.value, pageCount);
      const indices = targets === null ? Array.from({ length: pageCount }, (_, i) => i) : targets;

      // Always re-load from the original bytes so repeated clicks are
      // predictable (relative to the source file, not a previous result).
      const doc = await PDFLib.PDFDocument.load(currentBytes);
      const pages = doc.getPages();
      indices.forEach((idx) => {
        const page = pages[idx];
        const cur = page.getRotation().angle;
        const next = ((cur + rotateDelta) % 360 + 360) % 360;
        page.setRotation(PDFLib.degrees(next));
      });

      const outBytes = await doc.save();
      outBlob = new Blob([outBytes], { type: "application/pdf" });
      outName = `${baseName(currentFile.name)}-rotated.pdf`;
      downloadBlob(outBlob, outName);

      setResult(
        `${ICON_OK}<div class="r-body"><strong>Created ${escapeHtml(outName)}</strong> ` +
          `(${indices.length} of ${pageCount} page${pageCount === 1 ? "" : "s"} rotated, ${formatBytes(outBlob.size)}). ` +
          `Download started automatically.` +
          `<div><button type="button" id="dlAgainBtn" style="margin-top:12px;">Download again</button></div></div>`,
        "ok"
      );
      finishedOk = true;
    } catch (err) {
      setResult(
        `${ICON_ERR}<div class="r-body"><strong>Couldn't rotate this PDF.</strong> ${escapeHtml(err.message || "Something went wrong.")}</div>`,
        "error"
      );
    } finally {
      els.rotateBtn.disabled = !currentBytes;
      els.rotateBtn.innerHTML = DEFAULT_LABEL;
    }

    if (finishedOk) {
      const dlAgainBtn = document.getElementById("dlAgainBtn");
      if (dlAgainBtn && outBlob) {
        dlAgainBtn.addEventListener("click", () => downloadBlob(outBlob, outName));
      }
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
      celebrateSuccess(els.rotateBtn, els.result);
    } else {
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  });
})();
