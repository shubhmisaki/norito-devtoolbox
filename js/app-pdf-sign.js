(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    fileInfo: document.getElementById("fileInfo"),
    sigTabs: document.getElementById("sigTabs"),
    drawPanel: document.getElementById("drawPanel"),
    typePanel: document.getElementById("typePanel"),
    sigCanvas: document.getElementById("sigCanvas"),
    clearSigBtn: document.getElementById("clearSigBtn"),
    sigText: document.getElementById("sigText"),
    sigStyle: document.getElementById("sigStyle"),
    sigPreview: document.getElementById("sigPreview"),
    pageSelect: document.getElementById("pageSelect"),
    positionSelect: document.getElementById("positionSelect"),
    sizeInput: document.getElementById("sizeInput"),
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
  let sigMode = "draw";
  let hasDrawn = false;

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

  const CONTROLS = [els.pageSelect, els.positionSelect, els.sizeInput];

  function resetFileState() {
    currentFile = null;
    currentBytes = null;
    pageCount = 0;
    els.fileInfo.style.display = "none";
    els.pageSelect.innerHTML = "";
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

      els.pageSelect.innerHTML = "";
      for (let i = 1; i <= pageCount; i++) {
        const opt = document.createElement("option");
        opt.value = String(i);
        opt.textContent = `Page ${i}`;
        if (i === pageCount) opt.selected = true;
        els.pageSelect.appendChild(opt);
      }

      CONTROLS.forEach((el) => { el.disabled = false; });
      els.sigText.disabled = sigMode !== "type";
      els.sigStyle.disabled = sigMode !== "type";
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

  // ---------- draw / type mode tabs ----------

  els.sigTabs.querySelectorAll(".tab").forEach((btn) => {
    btn.addEventListener("click", () => {
      els.sigTabs.querySelectorAll(".tab").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      sigMode = btn.dataset.value;
      els.drawPanel.style.display = sigMode === "draw" ? "block" : "none";
      els.typePanel.style.display = sigMode === "type" ? "block" : "none";
      els.sigText.disabled = sigMode !== "type" || !currentBytes;
      els.sigStyle.disabled = sigMode !== "type" || !currentBytes;
    });
  });

  // ---------- draw pad ----------

  const sigCtx = els.sigCanvas.getContext("2d");
  sigCtx.lineWidth = 3;
  sigCtx.lineCap = "round";
  sigCtx.lineJoin = "round";
  sigCtx.strokeStyle = "#111111";
  let drawing = false;
  let lastX = 0, lastY = 0;

  function canvasPointFromEvent(e) {
    const rect = els.sigCanvas.getBoundingClientRect();
    const scaleX = els.sigCanvas.width / rect.width;
    const scaleY = els.sigCanvas.height / rect.height;
    return {
      x: (e.clientX - rect.left) * scaleX,
      y: (e.clientY - rect.top) * scaleY,
    };
  }

  els.sigCanvas.addEventListener("pointerdown", (e) => {
    if (!currentBytes) return;
    drawing = true;
    els.sigCanvas.setPointerCapture(e.pointerId);
    const p = canvasPointFromEvent(e);
    lastX = p.x;
    lastY = p.y;
    sigCtx.beginPath();
    sigCtx.moveTo(p.x, p.y);
    sigCtx.lineTo(p.x + 0.01, p.y + 0.01);
    sigCtx.stroke();
    hasDrawn = true;
    els.clearSigBtn.disabled = false;
  });
  els.sigCanvas.addEventListener("pointermove", (e) => {
    if (!drawing) return;
    const p = canvasPointFromEvent(e);
    sigCtx.beginPath();
    sigCtx.moveTo(lastX, lastY);
    sigCtx.lineTo(p.x, p.y);
    sigCtx.stroke();
    lastX = p.x;
    lastY = p.y;
  });
  ["pointerup", "pointerleave", "pointercancel"].forEach((evt) => {
    els.sigCanvas.addEventListener(evt, () => { drawing = false; });
  });

  els.clearSigBtn.addEventListener("click", () => {
    sigCtx.clearRect(0, 0, els.sigCanvas.width, els.sigCanvas.height);
    hasDrawn = false;
    els.clearSigBtn.disabled = true;
  });

  // ---------- type preview ----------

  function updateTypePreview() {
    const text = els.sigText.value.trim() || "Your name";
    const opt = els.sigStyle.options[els.sigStyle.selectedIndex];
    els.sigPreview.style.fontFamily = els.sigStyle.value;
    els.sigPreview.style.fontStyle = opt && opt.dataset.italic ? "italic" : "normal";
    els.sigPreview.textContent = text;
  }
  els.sigText.addEventListener("input", updateTypePreview);
  els.sigStyle.addEventListener("change", updateTypePreview);
  updateTypePreview();

  // ---------- helpers: build the signature image ----------

  // Scans a canvas for the bounding box of non-transparent pixels and
  // returns a new, tightly-cropped canvas (with a small padding margin).
  // Throws if the canvas is entirely transparent (nothing drawn).
  function trimCanvas(canvas, pad = 6) {
    const ctx = canvas.getContext("2d");
    const { width, height } = canvas;
    const data = ctx.getImageData(0, 0, width, height).data;
    let minX = width, minY = height, maxX = -1, maxY = -1;
    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        const alpha = data[(y * width + x) * 4 + 3];
        if (alpha > 10) {
          if (x < minX) minX = x;
          if (x > maxX) maxX = x;
          if (y < minY) minY = y;
          if (y > maxY) maxY = y;
        }
      }
    }
    if (maxX < 0) return null; // nothing drawn
    minX = Math.max(0, minX - pad);
    minY = Math.max(0, minY - pad);
    maxX = Math.min(width - 1, maxX + pad);
    maxY = Math.min(height - 1, maxY + pad);
    const w = maxX - minX + 1;
    const h = maxY - minY + 1;
    const out = document.createElement("canvas");
    out.width = w;
    out.height = h;
    out.getContext("2d").drawImage(canvas, minX, minY, w, h, 0, 0, w, h);
    return out;
  }

  function renderTypedSignature(text, fontFamily, italic) {
    const fontSize = 64;
    const measureCanvas = document.createElement("canvas");
    const measureCtx = measureCanvas.getContext("2d");
    const fontSpec = `${italic ? "italic " : ""}${fontSize}px ${fontFamily}`;
    measureCtx.font = fontSpec;
    const textWidth = measureCtx.measureText(text).width;

    const padX = 20, padY = 30;
    const canvas = document.createElement("canvas");
    canvas.width = Math.max(1, Math.ceil(textWidth + padX * 2));
    canvas.height = Math.ceil(fontSize * 1.6 + padY);
    const ctx = canvas.getContext("2d");
    ctx.font = fontSpec;
    ctx.fillStyle = "#111111";
    ctx.textBaseline = "alphabetic";
    ctx.fillText(text, padX, fontSize + padY / 2);
    return canvas;
  }

  // Computes the draw origin (x/y) for a given position keyword, page
  // size, and image width/height, with a fixed margin from the edge.
  // Mirrors the position enum used by Add Page Numbers / Add Watermark.
  function positionFor(position, pageWidth, pageHeight, imgWidth, imgHeight) {
    let x;
    if (position.endsWith("left")) x = MARGIN;
    else if (position.endsWith("right")) x = pageWidth - MARGIN - imgWidth;
    else x = (pageWidth - imgWidth) / 2;

    const y = position.startsWith("top") ? pageHeight - MARGIN - imgHeight : MARGIN;
    return { x, y };
  }

  const DEFAULT_LABEL = els.applyBtn.innerHTML;

  els.applyBtn.addEventListener("click", async () => {
    if (!currentBytes) return;
    els.applyBtn.disabled = true;
    els.applyBtn.textContent = "Signing...";
    let finishedOk = false;
    let outBlob = null;
    let outName = "";

    try {
      const pageIndex = parseInt(els.pageSelect.value, 10) - 1;
      const position = els.positionSelect.value;
      const targetWidth = parseInt(els.sizeInput.value, 10);
      if (isNaN(targetWidth) || targetWidth < 40 || targetWidth > 400) {
        throw new Error("Width must be between 40 and 400 points.");
      }
      if (isNaN(pageIndex) || pageIndex < 0 || pageIndex >= pageCount) {
        throw new Error("Choose a page to sign.");
      }

      let sourceCanvas;
      if (sigMode === "draw") {
        if (!hasDrawn) throw new Error("Draw your signature first.");
        sourceCanvas = els.sigCanvas;
      } else {
        const text = els.sigText.value.trim();
        if (!text) throw new Error("Type your name first.");
        const opt = els.sigStyle.options[els.sigStyle.selectedIndex];
        sourceCanvas = renderTypedSignature(text, els.sigStyle.value, !!(opt && opt.dataset.italic));
      }

      const trimmed = trimCanvas(sourceCanvas);
      if (!trimmed) throw new Error("Draw your signature first.");

      const pngBlob = await new Promise((resolve) => trimmed.toBlob(resolve, "image/png"));
      if (!pngBlob) throw new Error("Couldn't render the signature image.");
      const pngBytes = new Uint8Array(await pngBlob.arrayBuffer());

      const doc = await PDFLib.PDFDocument.load(currentBytes);
      const pngImage = await doc.embedPng(pngBytes);
      const imgWidth = targetWidth;
      const imgHeight = imgWidth * (trimmed.height / trimmed.width);

      const page = doc.getPages()[pageIndex];
      const { x, y } = positionFor(position, page.getWidth(), page.getHeight(), imgWidth, imgHeight);
      page.drawImage(pngImage, { x, y, width: imgWidth, height: imgHeight });

      const outBytes = await doc.save();
      outBlob = new Blob([outBytes], { type: "application/pdf" });
      outName = `${baseName(currentFile.name)}-signed.pdf`;
      downloadBlob(outBlob, outName);

      setResult(
        `${ICON_OK}<div class="r-body"><strong>Created ${escapeHtml(outName)}</strong> ` +
          `(signed on page ${pageIndex + 1}, ${formatBytes(outBlob.size)}). ` +
          `Download started automatically.` +
          `<div><button type="button" id="dlAgainBtn" style="margin-top:12px;">Download again</button></div></div>`,
        "ok"
      );
      finishedOk = true;
    } catch (err) {
      setResult(
        `${ICON_ERR}<div class="r-body"><strong>Couldn't sign this PDF.</strong> ${escapeHtml(err.message || "Something went wrong.")}</div>`,
        "error"
      );
    } finally {
      els.applyBtn.disabled = !currentBytes;
      els.applyBtn.innerHTML = DEFAULT_LABEL;
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
