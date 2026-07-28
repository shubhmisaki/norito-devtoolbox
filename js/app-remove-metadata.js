(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    originalInfo: document.getElementById("originalInfo"),
    metaPanel: document.getElementById("metaPanel"),
    metaList: document.getElementById("metaList"),
    cleanBtn: document.getElementById("cleanBtn"),
    result: document.getElementById("result"),
    preview: document.getElementById("preview"),
    previewHint: document.getElementById("previewHint"),
  };

  let currentImg = null;
  let currentFile = null;

  const ICONS = {
    ok: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="M22 4 12 14.01l-3-3"/></svg>',
    error: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>',
  };

  function setResult(html, state) {
    els.result.innerHTML = `<span class="r-icon">${ICONS[state] || ""}</span><span class="r-body">${html}</span>`;
    els.result.style.display = "flex";
    els.result.classList.remove("ok", "error");
    if (state) els.result.classList.add(state);
  }

  function loadImageFile(file) {
    return new Promise((resolve, reject) => {
      const url = URL.createObjectURL(file);
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = reject;
      img.src = url;
    });
  }

  // ---- minimal JPEG EXIF reader ----
  // Walks JPEG markers looking for APP1/Exif, then reads a handful of the
  // most commonly-recognized TIFF tags directly out of the IFD0/Exif/GPS
  // sub-IFDs. This is intentionally not a full EXIF library, just enough to
  // show a user what personally-identifying info (camera model, GPS
  // coordinates, timestamp, software) is riding along in their file.
  const TAGS_IFD0 = { 0x010f: "Camera make", 0x0110: "Camera model", 0x0131: "Software", 0x0132: "Date/time modified" };
  const TAGS_EXIF = { 0x9003: "Date taken", 0xa002: "Image width (EXIF)", 0xa003: "Image height (EXIF)", 0x829a: "Exposure time", 0x829d: "F-number", 0x8827: "ISO" };
  const TAGS_GPS = { 0x0002: "GPS latitude", 0x0004: "GPS longitude" };

  function readExif(buf) {
    const view = new DataView(buf);
    if (view.getUint16(0) !== 0xffd8) return null; // not a JPEG
    let offset = 2;
    while (offset < view.byteLength - 4) {
      if (view.getUint8(offset) !== 0xff) break;
      const marker = view.getUint8(offset + 1);
      const size = view.getUint16(offset + 2);
      if (marker === 0xe1) {
        const start = offset + 4;
        if (view.getUint32(start) === 0x45786966) { // "Exif"
          return parseTiff(view, start + 6);
        }
      }
      if (marker === 0xda) break; // start of scan, no more markers
      offset += 2 + size;
    }
    return null;
  }

  function parseTiff(view, tiffStart) {
    const little = view.getUint16(tiffStart) === 0x4949;
    const g16 = (o) => view.getUint16(o, little);
    const g32 = (o) => view.getUint32(o, little);
    const ifd0Offset = tiffStart + g32(tiffStart + 4);
    const found = [];

    function readAscii(valueOffset, count) {
      let s = "";
      for (let i = 0; i < count - 1; i++) s += String.fromCharCode(view.getUint8(valueOffset + i));
      return s;
    }
    function readRational(offset) {
      const num = g32(offset), den = g32(offset + 4);
      return den ? num / den : 0;
    }

    function readIfd(ifdOffset, tagMap, onSubIfd) {
      const count = g16(ifdOffset);
      for (let i = 0; i < count; i++) {
        const entryOffset = ifdOffset + 2 + i * 12;
        const tag = g16(entryOffset);
        const type = g16(entryOffset + 2);
        const numValues = g32(entryOffset + 4);
        const valueFieldOffset = entryOffset + 8;
        // Values <=4 bytes are stored inline; longer ones are stored at the
        // offset the value field points to (both relative to tiffStart).
        const typeSize = { 1: 1, 2: 1, 3: 2, 4: 4, 5: 8, 9: 4, 10: 8 }[type] || 1;
        const totalSize = typeSize * numValues;
        const dataOffset = totalSize > 4 ? tiffStart + g32(valueFieldOffset) : valueFieldOffset;

        if (tag === 0x8769 && onSubIfd) { onSubIfd("exif", tiffStart + g32(valueFieldOffset)); continue; }
        if (tag === 0x8825 && onSubIfd) { onSubIfd("gps", tiffStart + g32(valueFieldOffset)); continue; }

        const label = tagMap[tag];
        if (!label) continue;
        let value;
        if (type === 2) value = readAscii(dataOffset, numValues).trim();
        else if (type === 5 || type === 10) value = readRational(dataOffset);
        else if (type === 3) value = g16(dataOffset);
        else if (type === 4) value = g32(dataOffset);
        else continue;
        if (value !== "" && value != null) found.push({ label, value });
      }
    }

    let exifIfd = null, gpsIfd = null;
    readIfd(ifd0Offset, TAGS_IFD0, (kind, off) => { if (kind === "exif") exifIfd = off; if (kind === "gps") gpsIfd = off; });
    if (exifIfd) readIfd(exifIfd, TAGS_EXIF);
    if (gpsIfd) readIfd(gpsIfd, TAGS_GPS, () => {});
    return found;
  }

  async function handleFile(file) {
    if (!file || !file.type.startsWith("image/")) {
      setResult("<strong>That's not an image.</strong> Choose a JPG, PNG, or WebP file.", "error");
      return;
    }
    currentFile = file;
    currentImg = await loadImageFile(file);
    els.originalInfo.textContent = `${file.name}, ${currentImg.width}×${currentImg.height}, ${formatBytes(file.size)}`;
    els.originalInfo.style.display = "block";
    els.cleanBtn.disabled = false;
    els.result.style.display = "none";

    let tags = [];
    try {
      if (file.type === "image/jpeg") {
        const buf = await file.arrayBuffer();
        tags = readExif(buf) || [];
      }
    } catch (e) { /* unreadable/corrupt EXIF block, treat as none found */ }

    if (tags.length) {
      els.metaList.innerHTML = tags.map((t) =>
        `<div class="meta-row"><span class="meta-label">${t.label}</span><span class="meta-value">${escapeHtml(String(t.value))}</span></div>`
      ).join("");
      els.metaPanel.querySelector(".meta-summary").textContent =
        `Found ${tags.length} metadata field${tags.length === 1 ? "" : "s"} in this file.`;
    } else {
      els.metaList.innerHTML = "";
      els.metaPanel.querySelector(".meta-summary").textContent =
        file.type === "image/jpeg"
          ? "No readable EXIF metadata found in this file."
          : "This file type (PNG/WebP) rarely carries EXIF data the way JPEGs do, but it can still carry color profiles or text chunks. Removing metadata will strip any that's present.";
    }
    els.metaPanel.style.display = "block";
  }

  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  els.drop.addEventListener("click", () => els.fileInput.click());
  els.fileInput.addEventListener("change", (e) => handleFile(e.target.files[0]));
  wireDragDrop(els.drop, (e) => {
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  });
  document.addEventListener("paste", (e) => {
    const items = e.clipboardData && e.clipboardData.items;
    if (!items) return;
    for (const item of items) {
      if (item.type && item.type.startsWith("image/")) {
        const file = item.getAsFile();
        if (file) { handleFile(file); e.preventDefault(); }
        break;
      }
    }
  });

  function canvasToBlob(canvas, mime, quality) {
    return new Promise((resolve) => canvas.toBlob(resolve, mime, quality));
  }

  els.cleanBtn.addEventListener("click", async () => {
    if (!currentImg) return;
    els.cleanBtn.disabled = true;
    els.cleanBtn.textContent = "Cleaning...";
    try {
      // Re-drawing onto a fresh canvas and re-encoding is what actually
      // strips the metadata: canvas.toBlob() only ever writes pixel data,
      // never the original file's EXIF/XMP/ICC chunks.
      const canvas = document.createElement("canvas");
      canvas.width = currentImg.width;
      canvas.height = currentImg.height;
      canvas.getContext("2d").drawImage(currentImg, 0, 0);
      const isJpeg = currentFile.type === "image/jpeg";
      const mime = isJpeg ? "image/jpeg" : currentFile.type === "image/webp" ? "image/webp" : "image/png";
      const blob = await canvasToBlob(canvas, mime, mime === "image/png" ? undefined : 0.95);

      const url = URL.createObjectURL(blob);
      els.preview.src = url;
      els.preview.style.display = "block";
      if (els.previewHint) els.previewHint.style.display = "none";

      const ext = { "image/jpeg": "jpg", "image/png": "png", "image/webp": "webp" }[mime];
      const base = (currentFile.name || "image").replace(/\.[^.]+$/, "");
      const filename = `${base}-clean.${ext}`;

      setResult(
        `<strong>Metadata removed.</strong> ${formatBytes(blob.size)}. The download below has no EXIF, GPS, or other embedded metadata.<br><br>` +
        `<button id="dlBtn">Download ${filename}</button>`,
        "ok"
      );
      document.getElementById("dlBtn").addEventListener("click", () => downloadBlob(blob, filename));
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
      celebrateSuccess(els.cleanBtn, els.result);
    } catch (err) {
      setResult(`<strong>Couldn't process that image.</strong> ${err.message || "Try a different file."}`, "error");
    } finally {
      els.cleanBtn.disabled = false;
      els.cleanBtn.textContent = "Remove metadata & download";
    }
  });
})();
