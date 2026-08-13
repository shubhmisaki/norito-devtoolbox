(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    fileInfo: document.getElementById("fileInfo"),
    pagesInput: document.getElementById("pagesInput"),
    separateToggle: document.getElementById("separateToggle"),
    splitBtn: document.getElementById("splitBtn"),
    result: document.getElementById("result"),
  };

  const ICON_OK =
    '<svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>';
  const ICON_ERR =
    '<svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>';

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

  function resetFileState() {
    currentFile = null;
    currentBytes = null;
    pageCount = 0;
    els.fileInfo.style.display = "none";
    els.pagesInput.disabled = true;
    els.pagesInput.value = "";
    els.splitBtn.disabled = true;
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
      els.splitBtn.disabled = false;
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

  // Parses "1-3, 5, 8-10" into an array of groups, each an array of 0-based
  // page indices. Returns null for a blank/whitespace-only string, so the
  // caller can tell "nothing typed" apart from "typed something invalid".
  function parseRanges(str, maxPage) {
    const trimmed = (str || "").trim();
    if (!trimmed) return null;
    const segments = trimmed.split(",").map((s) => s.trim()).filter(Boolean);
    if (segments.length === 0) return null;
    return segments.map((seg) => {
      const m = seg.match(/^(\d+)(?:-(\d+))?$/);
      if (!m) throw new Error(`"${seg}" isn't a valid page or range.`);
      let start = parseInt(m[1], 10);
      let end = m[2] ? parseInt(m[2], 10) : start;
      if (start > end) { const t = start; start = end; end = t; }
      if (start < 1 || end > maxPage) {
        throw new Error(`"${seg}" is out of range, this PDF has ${maxPage} page${maxPage === 1 ? "" : "s"}.`);
      }
      const idxs = [];
      for (let p = start; p <= end; p++) idxs.push(p - 1);
      return idxs;
    });
  }

  function labelFor(idxs) {
    if (idxs.length === 1) return `page-${idxs[0] + 1}.pdf`;
    return `pages-${idxs[0] + 1}-${idxs[idxs.length - 1] + 1}.pdf`;
  }

  els.splitBtn.addEventListener("click", async () => {
    if (!currentBytes) return;
    const busyText = startBusyText(els.splitBtn, "Splitting");
    let finishedOk = false;
    let outBlob = null;
    let outName = "";

    try {
      let groups;
      try {
        groups = parseRanges(els.pagesInput.value, pageCount);
      } catch (err) {
        throw err; // range syntax/out-of-range error, message already user-facing
      }

      const separate = els.separateToggle.checked;
      if (groups === null) {
        // blank field: "all pages", split per-page if separate mode is on
        if (separate) {
          groups = Array.from({ length: pageCount }, (_, i) => [i]);
        } else {
          groups = [Array.from({ length: pageCount }, (_, i) => i)];
        }
      } else if (!separate) {
        // combine every listed page/range into one output, in the given order
        groups = [groups.flat()];
      }

      const src = await PDFLib.PDFDocument.load(currentBytes);
      const outputs = [];
      for (const idxs of groups) {
        const doc = await PDFLib.PDFDocument.create();
        const pages = await doc.copyPages(src, idxs);
        pages.forEach((p) => doc.addPage(p));
        const bytes = await doc.save();
        outputs.push({ name: labelFor(idxs), bytes });
      }

      const base = baseName(currentFile.name);
      if (outputs.length === 1) {
        outBlob = new Blob([outputs[0].bytes], { type: "application/pdf" });
        outName = `${base}-split.pdf`;
      } else {
        const zipBytes = createZip(
          outputs.map((o) => ({ name: `${base}-${o.name}`, bytes: o.bytes }))
        );
        outBlob = new Blob([zipBytes], { type: "application/zip" });
        outName = `${base}-split.zip`;
      }
      downloadBlob(outBlob, outName);

      const summary =
        outputs.length === 1
          ? `<strong>Created ${escapeHtml(outName)}</strong> (${formatBytes(outBlob.size)}). Download started automatically.`
          : `<strong>Created ${outputs.length} files in ${escapeHtml(outName)}</strong> (${formatBytes(outBlob.size)}). Download started automatically.`;

      setResult(
        `${ICON_OK}<div class="r-body">${summary}` +
          `<div><button type="button" id="dlAgainBtn" style="margin-top:12px;">Download again</button></div></div>`,
        "ok"
      );
      finishedOk = true;
    } catch (err) {
      setResult(
        `${ICON_ERR}<div class="r-body"><strong>Couldn't split this PDF.</strong> ${escapeHtml(err.message || "Something went wrong.")}</div>`,
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
      celebrateSuccess(els.splitBtn, els.result);
    } else {
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  });
})();
