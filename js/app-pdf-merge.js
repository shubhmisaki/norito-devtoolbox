(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    fileList: document.getElementById("fileList"),
    mergeBtn: document.getElementById("mergeBtn"),
    result: document.getElementById("result"),
  };

  let items = []; // { id, file }
  let nextId = 1;

  const ICON_FILE =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/></svg>';
  const ICON_UP =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m18 15-6-6-6 6"/></svg>';
  const ICON_DOWN =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>';
  const ICON_X =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>';
  const ICON_OK =
    '<svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>';
  const ICON_ERR =
    '<svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>';

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    }[c]));
  }

  function isPdf(file) {
    return file.type === "application/pdf" || /\.pdf$/i.test(file.name);
  }

  function addFiles(fileListLike) {
    const incoming = Array.from(fileListLike || []).filter(isPdf);
    incoming.forEach((file) => items.push({ id: nextId++, file }));
    render();
  }

  function removeItem(id) {
    items = items.filter((it) => it.id !== id);
    render();
  }

  function moveItem(id, dir) {
    const idx = items.findIndex((it) => it.id === id);
    if (idx < 0) return;
    const swapWith = idx + dir;
    if (swapWith < 0 || swapWith >= items.length) return;
    const tmp = items[idx];
    items[idx] = items[swapWith];
    items[swapWith] = tmp;
    render();
  }

  function render() {
    if (items.length === 0) {
      els.fileList.style.display = "none";
      els.fileList.innerHTML = "";
      els.mergeBtn.disabled = true;
      return;
    }
    els.fileList.style.display = "flex";
    els.fileList.innerHTML = items
      .map((it, i) => `
        <div class="file-row" data-id="${it.id}">
          <div class="file-row-index">${i + 1}</div>
          <div class="file-row-icon">${ICON_FILE}</div>
          <div class="file-row-info">
            <div class="file-row-name">${escapeHtml(it.file.name)}</div>
            <div class="file-row-size">${formatBytes(it.file.size)}</div>
          </div>
          <div class="file-row-actions">
            <button type="button" class="mv-up" data-id="${it.id}" ${i === 0 ? "disabled" : ""} aria-label="Move up">${ICON_UP}</button>
            <button type="button" class="mv-down" data-id="${it.id}" ${i === items.length - 1 ? "disabled" : ""} aria-label="Move down">${ICON_DOWN}</button>
            <button type="button" class="file-row-remove" data-id="${it.id}" aria-label="Remove">${ICON_X}</button>
          </div>
        </div>`)
      .join("");
    els.mergeBtn.disabled = items.length < 2;
  }

  els.fileList.addEventListener("click", (e) => {
    const btn = e.target.closest("button");
    if (!btn) return;
    const id = Number(btn.dataset.id);
    if (btn.classList.contains("mv-up")) moveItem(id, -1);
    else if (btn.classList.contains("mv-down")) moveItem(id, 1);
    else if (btn.classList.contains("file-row-remove")) removeItem(id);
  });

  els.drop.addEventListener("click", () => els.fileInput.click());
  els.fileInput.addEventListener("change", () => {
    addFiles(els.fileInput.files);
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
    if (e.dataTransfer && e.dataTransfer.files) addFiles(e.dataTransfer.files);
  });

  function setResult(html, state) {
    els.result.innerHTML = html;
    els.result.style.display = "flex";
    els.result.classList.remove("ok", "error");
    if (state) els.result.classList.add(state);
  }

  const DEFAULT_LABEL = els.mergeBtn.innerHTML;

  els.mergeBtn.addEventListener("click", async () => {
    if (items.length < 2) return;
    els.mergeBtn.disabled = true;
    els.mergeBtn.textContent = "Merging...";
    let finishedOk = false;
    let mergedBlob = null;

    try {
      const merged = await PDFLib.PDFDocument.create();
      let totalPages = 0;

      for (const it of items) {
        let bytes;
        try {
          bytes = await it.file.arrayBuffer();
        } catch (err) {
          throw new Error(`Couldn't read "${it.file.name}".`);
        }
        let src;
        try {
          src = await PDFLib.PDFDocument.load(bytes);
        } catch (err) {
          const msg = (err && err.message) || "";
          if (/encrypt/i.test(msg)) {
            throw new Error(`"${it.file.name}" is password protected and can't be merged.`);
          }
          throw new Error(`"${it.file.name}" doesn't look like a valid PDF.`);
        }
        const pages = await merged.copyPages(src, src.getPageIndices());
        pages.forEach((p) => merged.addPage(p));
        totalPages += pages.length;
      }

      const outBytes = await merged.save();
      mergedBlob = new Blob([outBytes], { type: "application/pdf" });
      downloadBlob(mergedBlob, "merged.pdf");

      setResult(
        `${ICON_OK}<div class="r-body"><strong>Merged ${items.length} files into merged.pdf</strong> ` +
          `(${totalPages} pages, ${formatBytes(outBytes.length)}). Download started automatically.` +
          `<div><button type="button" id="dlAgainBtn" style="margin-top:12px;">Download again</button></div></div>`,
        "ok"
      );
      finishedOk = true;
    } catch (err) {
      setResult(
        `${ICON_ERR}<div class="r-body"><strong>Couldn't merge these files.</strong> ${escapeHtml(err.message || "Something went wrong.")}</div>`,
        "error"
      );
    } finally {
      els.mergeBtn.disabled = items.length < 2;
      els.mergeBtn.innerHTML = DEFAULT_LABEL;
    }

    // Runs after the button label has already been restored above, so the
    // checkmark morph is the last thing to touch the button, matching the
    // pattern used by the other tools (see app-compress.js).
    if (finishedOk) {
      const dlAgainBtn = document.getElementById("dlAgainBtn");
      if (dlAgainBtn && mergedBlob) {
        dlAgainBtn.addEventListener("click", () => downloadBlob(mergedBlob, "merged.pdf"));
      }
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
      celebrateSuccess(els.mergeBtn, els.result);
    } else {
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  });
})();
