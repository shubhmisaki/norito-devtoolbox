(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    fileList: document.getElementById("fileList"),
    pageSizeSelect: document.getElementById("pageSizeSelect"),
    convertBtn: document.getElementById("convertBtn"),
    result: document.getElementById("result"),
  };

  let items = []; // { id, file }
  let nextId = 1;

  const ICON_IMG =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>';
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

  function isImage(file) {
    return file.type.startsWith("image/") || /\.(jpe?g|png|webp|gif|bmp)$/i.test(file.name);
  }

  function addFiles(fileListLike) {
    const incoming = Array.from(fileListLike || []).filter(isImage);
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
      els.convertBtn.disabled = true;
      return;
    }
    els.fileList.style.display = "flex";
    els.fileList.innerHTML = items
      .map((it, i) => `
        <div class="file-row" data-id="${it.id}">
          <div class="file-row-index">${i + 1}</div>
          <div class="file-row-icon">${ICON_IMG}</div>
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
    els.convertBtn.disabled = items.length < 1;
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

  // Decodes any browser-displayable image file into an ImageBitmap-like
  // object (width/height + drawable to canvas), used as the fallback path
  // for formats/JPEG variants pdf-lib's embedJpg/embedPng can't parse
  // directly (e.g. progressive JPEGs, WebP, GIF).
  async function decodeToBitmap(file) {
    if (typeof createImageBitmap === "function") {
      return await createImageBitmap(file);
    }
    return await new Promise((resolve, reject) => {
      const url = URL.createObjectURL(file);
      const img = new Image();
      img.onload = () => { URL.revokeObjectURL(url); resolve(img); };
      img.onerror = () => { URL.revokeObjectURL(url); reject(new Error("Could not decode image")); };
      img.src = url;
    });
  }

  async function bitmapToPngBytes(bitmap) {
    const w = bitmap.width, h = bitmap.height;
    const canvas = document.createElement("canvas");
    canvas.width = w;
    canvas.height = h;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(bitmap, 0, 0, w, h);
    const blob = await new Promise((resolve) => canvas.toBlob(resolve, "image/png"));
    if (!blob) throw new Error("Could not re-encode image");
    return new Uint8Array(await blob.arrayBuffer());
  }

  // Embeds a file into the PDF, trying the fast native path first (PNG/JPEG
  // bytes handed straight to pdf-lib) and falling back to a decode-and
  // re-encode-as-PNG path for anything pdf-lib rejects or doesn't natively
  // understand (WebP, GIF, some JPEG variants like progressive JPEGs).
  async function embedImageFile(doc, file) {
    const bytes = new Uint8Array(await file.arrayBuffer());
    const type = file.type;
    try {
      if (type === "image/png") return await doc.embedPng(bytes);
      if (type === "image/jpeg" || type === "image/jpg") return await doc.embedJpg(bytes);
    } catch (err) {
      // fall through to the re-encode path below
    }
    const bitmap = await decodeToBitmap(file);
    const pngBytes = await bitmapToPngBytes(bitmap);
    return await doc.embedPng(pngBytes);
  }

  const PAGE_SIZES = {
    a4: [595.28, 841.89],
    letter: [612, 792],
  };
  const FIT_SCALE = 72 / 96; // treat image pixels as 96 DPI, convert to PDF points

  const DEFAULT_LABEL = els.convertBtn.innerHTML;

  els.convertBtn.addEventListener("click", async () => {
    if (items.length < 1) return;
    els.convertBtn.disabled = true;
    els.convertBtn.textContent = "Converting...";
    let finishedOk = false;
    let outBlob = null;
    let outName = "images.pdf";

    try {
      const doc = await PDFLib.PDFDocument.create();
      const mode = els.pageSizeSelect.value;

      for (const it of items) {
        let img;
        try {
          img = await embedImageFile(doc, it.file);
        } catch (err) {
          throw new Error(`Couldn't read "${it.file.name}", it may not be a valid image.`);
        }

        if (mode === "fit") {
          const w = img.width * FIT_SCALE;
          const h = img.height * FIT_SCALE;
          const page = doc.addPage([w, h]);
          page.drawImage(img, { x: 0, y: 0, width: w, height: h });
        } else {
          const [pw, ph] = PAGE_SIZES[mode];
          const margin = 36; // half-inch margin
          const availW = pw - margin * 2;
          const availH = ph - margin * 2;
          const ratio = Math.min(availW / img.width, availH / img.height);
          const w = img.width * ratio;
          const h = img.height * ratio;
          const x = (pw - w) / 2;
          const y = (ph - h) / 2;
          const page = doc.addPage([pw, ph]);
          page.drawImage(img, { x, y, width: w, height: h });
        }
      }

      const outBytes = await doc.save();
      outBlob = new Blob([outBytes], { type: "application/pdf" });
      downloadBlob(outBlob, outName);

      setResult(
        `${ICON_OK}<div class="r-body"><strong>Created ${escapeHtml(outName)}</strong> ` +
          `(${items.length} page${items.length === 1 ? "" : "s"}, ${formatBytes(outBlob.size)}). ` +
          `Download started automatically.` +
          `<div><button type="button" id="dlAgainBtn" style="margin-top:12px;">Download again</button></div></div>`,
        "ok"
      );
      finishedOk = true;
    } catch (err) {
      setResult(
        `${ICON_ERR}<div class="r-body"><strong>Couldn't create the PDF.</strong> ${escapeHtml(err.message || "Something went wrong.")}</div>`,
        "error"
      );
    } finally {
      els.convertBtn.disabled = items.length < 1;
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
