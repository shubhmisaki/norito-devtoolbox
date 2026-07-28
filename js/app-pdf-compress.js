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
  let currentBytes = null; // ArrayBuffer, re-copied fresh for each consumer
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

  // ---------- file load ----------

  const CONTROLS = [els.dpiSelect, els.qualitySelect];

  function resetFileState() {
    currentFile = null;
    currentBytes = null;
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
      const bytes = await file.arrayBuffer();
      // pdf.js's getDocument() detaches/transfers the buffer it's given, so
      // hand it a throwaway copy and keep the original untouched for the
      // real compression pass later.
      const doc = await pdfjsLib.getDocument({ data: new Uint8Array(bytes.slice(0)) }).promise;
      currentFile = file;
      currentBytes = bytes;
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

  wireDragDrop(els.drop, (e) => {
    if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]) {
      loadFile(e.dataTransfer.files[0]);
    }
  });

  // ---------- page classification: real text vs. scanned/image-only ----------

  // Pages with a meaningful amount of extractable text are left completely
  // alone structurally (their vector graphics, fonts, and text stay text).
  // Pages with no real text (a scanned page that's just one big image) are
  // safe to fully rasterize and recompress, since there's no selectable
  // text on them to lose in the first place.
  async function classifyPages(bytesCopy) {
    const pdf = await pdfjsLib.getDocument({ data: bytesCopy }).promise;
    const classes = [];
    for (let i = 1; i <= pdf.numPages; i++) {
      const page = await pdf.getPage(i);
      const content = await page.getTextContent();
      const text = content.items.map((it) => it.str).join("").trim();
      classes.push(text.length >= 4 ? "text" : "scanned");
    }
    return classes;
  }

  // ---------- low-level pdf-lib helpers ----------

  // Walks a page's Resources -> XObject dictionary (recursing into any
  // Form XObjects) and returns every unique Image XObject reachable from
  // the given page indices, deduplicated by object reference (the same
  // embedded image can be reused across multiple pages).
  function collectImageXObjects(doc, pageIndices) {
    const context = doc.context;
    const seen = new Set();
    const results = [];
    function walk(resources, depth) {
      if (!resources || depth > 6) return;
      const xObjectDict = resources.lookupMaybe(PDFLib.PDFName.of("XObject"), PDFLib.PDFDict);
      if (!xObjectDict) return;
      xObjectDict.keys().forEach((key) => {
        const ref = xObjectDict.get(key);
        if (!(ref instanceof PDFLib.PDFRef)) return;
        if (seen.has(ref.objectNumber)) return;
        seen.add(ref.objectNumber);
        const obj = context.lookup(ref);
        if (!obj || !(obj instanceof PDFLib.PDFStream)) return;
        const subtype = obj.dict.lookupMaybe(PDFLib.PDFName.of("Subtype"), PDFLib.PDFName);
        const subtypeStr = subtype ? subtype.asString() : "";
        if (subtypeStr === "/Image") {
          results.push({ ref, stream: obj });
        } else if (subtypeStr === "/Form") {
          const formResources = obj.dict.lookupMaybe(PDFLib.PDFName.of("Resources"), PDFLib.PDFDict);
          walk(formResources, depth + 1);
        }
      });
    }
    pageIndices.forEach((i) => walk(doc.getPages()[i].node.Resources(), 0));
    return results;
  }

  // pdf-lib never garbage-collects indirect objects on save(): if a page or
  // image stops being referenced (e.g. we replace a scanned page), the old
  // object silently stays in the file forever, bloating it. This does a
  // mark-and-sweep from the document's trailer roots and deletes anything
  // no longer reachable, which is essential for compression to actually
  // shrink the output.
  function pruneUnreachableObjects(doc) {
    const context = doc.context;
    const visited = new Set();
    const stack = [];
    const pushRoot = (obj) => { if (obj) stack.push(obj); };
    pushRoot(context.trailerInfo.Root);
    pushRoot(context.trailerInfo.Info);
    pushRoot(context.trailerInfo.Encrypt);

    while (stack.length) {
      const item = stack.pop();
      if (item === null || item === undefined) continue;
      if (item instanceof PDFLib.PDFRef) {
        if (visited.has(item.objectNumber)) continue;
        visited.add(item.objectNumber);
        const resolved = context.lookup(item);
        if (resolved) stack.push(resolved);
      } else if (item instanceof PDFLib.PDFStream) {
        item.dict.entries().forEach(([, value]) => stack.push(value));
      } else if (item instanceof PDFLib.PDFDict) {
        item.entries().forEach(([, value]) => stack.push(value));
      } else if (item instanceof PDFLib.PDFArray) {
        for (let i = 0; i < item.size(); i++) stack.push(item.get(i));
      }
    }

    context.enumerateIndirectObjects().forEach(([ref]) => {
      if (!visited.has(ref.objectNumber)) context.delete(ref);
    });
  }

  // Decodes a JPEG via the browser's own image pipeline, optionally
  // downsamples it, and re-encodes at the chosen quality. Relies on
  // img.decode() rejecting for anything the browser can't handle (e.g. a
  // CMYK JPEG), which doubles as a safety net.
  async function recompressJpeg(jpegBytes, quality, maxDim) {
    const blob = new Blob([jpegBytes], { type: "image/jpeg" });
    const url = URL.createObjectURL(blob);
    try {
      const img = new Image();
      img.src = url;
      await img.decode();
      let w = img.naturalWidth, h = img.naturalHeight;
      if (!w || !h) throw new Error("decode produced no dimensions");
      if (maxDim && Math.max(w, h) > maxDim) {
        const scale = maxDim / Math.max(w, h);
        w = Math.max(1, Math.round(w * scale));
        h = Math.max(1, Math.round(h * scale));
      }
      const canvas = document.createElement("canvas");
      canvas.width = w;
      canvas.height = h;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(img, 0, 0, w, h);
      const outBlob = await new Promise((resolve) => canvas.toBlob(resolve, "image/jpeg", quality));
      if (!outBlob) throw new Error("re-encode failed");
      const outBytes = new Uint8Array(await outBlob.arrayBuffer());
      return { bytes: outBytes, width: w, height: h };
    } finally {
      URL.revokeObjectURL(url);
    }
  }

  // ---------- main compression pipeline ----------

  async function compressPdf(originalBytes, { dpi, quality }) {
    const originalByteLength = originalBytes.byteLength;
    const classes = await classifyPages(new Uint8Array(originalBytes.slice(0)));
    const textPageIndices = [];
    const scannedPageIndices = [];
    classes.forEach((c, i) => (c === "text" ? textPageIndices : scannedPageIndices).push(i));

    const doc = await PDFLib.PDFDocument.load(originalBytes.slice(0));
    const maxDim = dpi * 14; // generous cap; only trims images stored far larger than any reasonable page

    // 1. Recompress embedded JPEGs reachable from TEXT pages, in place.
    //    Vector graphics, fonts, and text on these pages are never touched.
    let imagesRecompressed = 0;
    if (textPageIndices.length) {
      const images = collectImageXObjects(doc, textPageIndices);
      for (const { ref, stream } of images) {
        const dict = stream.dict;
        const filter = dict.lookupMaybe(PDFLib.PDFName.of("Filter"), PDFLib.PDFName);
        const isDct = filter && filter.asString() === "/DCTDecode";
        const hasMask = dict.has(PDFLib.PDFName.of("SMask")) || dict.has(PDFLib.PDFName.of("Mask"));
        const colorSpace = dict.lookupMaybe(PDFLib.PDFName.of("ColorSpace"), PDFLib.PDFName);
        const csStr = colorSpace ? colorSpace.asString() : "";
        const safeColorSpace = !colorSpace || ["/DeviceRGB", "/DeviceGray", "/CalRGB", "/CalGray"].includes(csStr);
        if (!isDct || hasMask || !safeColorSpace) continue;

        const originalImageBytes = stream.getContents();
        try {
          const { bytes: newBytes, width, height } = await recompressJpeg(originalImageBytes, quality, maxDim);
          if (newBytes.length < originalImageBytes.length) {
            const newStream = doc.context.stream(newBytes, {
              Type: "XObject", Subtype: "Image", Width: width, Height: height,
              ColorSpace: "DeviceRGB", BitsPerComponent: 8, Filter: "DCTDecode",
            });
            doc.context.assign(ref, newStream);
            imagesRecompressed++;
          }
        } catch (e) {
          // Couldn't decode/re-encode this particular image (e.g. an
          // unsupported color profile) -- leave it exactly as-is.
        }
      }
    }

    // 2. Fully rasterize pages with no real extractable text (scans).
    if (scannedPageIndices.length) {
      const pdf = await pdfjsLib.getDocument({ data: new Uint8Array(originalBytes.slice(0)) }).promise;
      const scale = dpi / 72;
      for (const pageIndex of scannedPageIndices) {
        const pdfPage = await pdf.getPage(pageIndex + 1);
        const baseViewport = pdfPage.getViewport({ scale: 1 });
        const viewport = pdfPage.getViewport({ scale });
        const canvas = document.createElement("canvas");
        canvas.width = Math.max(1, Math.ceil(viewport.width));
        canvas.height = Math.max(1, Math.ceil(viewport.height));
        const ctx = canvas.getContext("2d");
        ctx.fillStyle = "#ffffff";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        await pdfPage.render({ canvasContext: ctx, viewport }).promise;
        const blob = await new Promise((resolve) => canvas.toBlob(resolve, "image/jpeg", quality));
        if (!blob) continue;
        const jpegBytes = new Uint8Array(await blob.arrayBuffer());

        doc.removePage(pageIndex);
        const newPage = doc.insertPage(pageIndex, [baseViewport.width, baseViewport.height]);
        const jpgImage = await doc.embedJpg(jpegBytes);
        newPage.drawImage(jpgImage, { x: 0, y: 0, width: baseViewport.width, height: baseViewport.height });
      }
    }

    pruneUnreachableObjects(doc);
    const outBytes = await doc.save();

    if (outBytes.length >= originalByteLength) {
      return { bytes: null, changed: false };
    }
    return { bytes: outBytes, changed: true };
  }

  // ---------- UI wiring ----------

  const DEFAULT_LABEL = els.compressBtn.innerHTML;

  els.compressBtn.addEventListener("click", async () => {
    if (!currentBytes || !currentFile) return;
    els.compressBtn.disabled = true;
    els.compressBtn.textContent = "Compressing...";
    let finishedOk = false;
    let outBlob = null;
    let outName = "";

    try {
      const dpi = parseInt(els.dpiSelect.value, 10);
      const quality = parseFloat(els.qualitySelect.value);

      const { bytes: outBytes, changed } = await compressPdf(currentBytes, { dpi, quality });
      const originalSize = currentFile.size;

      if (!changed) {
        outBlob = new Blob([currentBytes.slice(0)], { type: "application/pdf" });
        outName = currentFile.name;
        downloadBlob(outBlob, outName);
        setResult(
          `${ICON_OK}<div class="r-body"><strong>This PDF is already efficient.</strong> ` +
            `Nothing here could be safely shrunk further without losing quality or flattening real text to an image, ` +
            `so the original file (${formatBytes(originalSize)}) was kept exactly as-is and downloaded again.` +
            `<div><button type="button" id="dlAgainBtn" style="margin-top:12px;">Download again</button></div></div>`,
          "ok"
        );
      } else {
        outBlob = new Blob([outBytes], { type: "application/pdf" });
        outName = `${baseName(currentFile.name)}-compressed.pdf`;
        downloadBlob(outBlob, outName);
        const newSize = outBlob.size;
        const pct = originalSize > 0 ? Math.round((1 - newSize / originalSize) * 100) : 0;
        setResult(
          `${ICON_OK}<div class="r-body"><strong>Created ${escapeHtml(outName)}</strong><br>` +
            `${formatBytes(originalSize)} &rarr; ${formatBytes(newSize)} (about ${pct}% smaller). ` +
            `Any page with real text keeps that text selectable, only scanned pages and embedded photos were recompressed. ` +
            `Download started automatically.` +
            `<div><button type="button" id="dlAgainBtn" style="margin-top:12px;">Download again</button></div></div>`,
          "ok"
        );
      }
      finishedOk = true;
    } catch (err) {
      setResult(
        `${ICON_ERR}<div class="r-body"><strong>Couldn't compress this PDF.</strong> ${escapeHtml(err.message || "Something went wrong.")}</div>`,
        "error"
      );
    } finally {
      els.compressBtn.disabled = !currentBytes;
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
