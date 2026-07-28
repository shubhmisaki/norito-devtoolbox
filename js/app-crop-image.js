(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    originalInfo: document.getElementById("originalInfo"),
    stage: document.getElementById("stage"),
    stageImg: document.getElementById("stageImg"),
    cropBox: document.getElementById("cropBox"),
    aspect: document.getElementById("aspect"),
    cropBtn: document.getElementById("cropBtn"),
    result: document.getElementById("result"),
    preview: document.getElementById("preview"),
    previewHint: document.getElementById("previewHint"),
    editorWrap: document.getElementById("editorWrap"),
  };

  let currentImg = null;
  let currentFile = null;
  // Crop rect stored in DISPLAYED (on-screen) pixels, relative to the stage.
  let rect = { x: 20, y: 20, w: 100, h: 100 };
  let scaleX = 1, scaleY = 1; // displayed-px -> natural-px

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

  function drawCropBox() {
    els.cropBox.style.left = rect.x + "px";
    els.cropBox.style.top = rect.y + "px";
    els.cropBox.style.width = rect.w + "px";
    els.cropBox.style.height = rect.h + "px";
  }

  function clampRect() {
    const maxW = els.stageImg.clientWidth;
    const maxH = els.stageImg.clientHeight;
    rect.w = Math.max(20, Math.min(rect.w, maxW));
    rect.h = Math.max(20, Math.min(rect.h, maxH));
    rect.x = Math.max(0, Math.min(rect.x, maxW - rect.w));
    rect.y = Math.max(0, Math.min(rect.y, maxH - rect.h));
  }

  function initRectForAspect() {
    const maxW = els.stageImg.clientWidth;
    const maxH = els.stageImg.clientHeight;
    const av = els.aspect.value;
    let ratio = null;
    if (av !== "free") {
      const [aw, ah] = av.split(":").map(Number);
      ratio = aw / ah;
    }
    let w = maxW * 0.8;
    let h = ratio ? w / ratio : maxH * 0.8;
    if (h > maxH * 0.9) { h = maxH * 0.9; w = ratio ? h * ratio : w; }
    rect = { x: (maxW - w) / 2, y: (maxH - h) / 2, w, h };
    clampRect();
    drawCropBox();
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
    els.stageImg.src = currentImg.src;
    els.editorWrap.style.display = "block";
    els.cropBtn.disabled = false;
    els.result.style.display = "none";
    // Wait a frame so the image has laid out at its displayed size before
    // computing the initial crop box and the natural-vs-displayed scale.
    requestAnimationFrame(() => {
      scaleX = currentImg.width / els.stageImg.clientWidth;
      scaleY = currentImg.height / els.stageImg.clientHeight;
      initRectForAspect();
    });
  }

  els.drop.addEventListener("click", () => els.fileInput.click());
  els.fileInput.addEventListener("change", (e) => handleFile(e.target.files[0]));
  wireDragDrop(els.drop, (e) => {
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  });

  els.aspect.addEventListener("change", () => {
    if (currentImg) initRectForAspect();
  });

  // ---- drag to move, and drag corner handles to resize ----
  function onPointerDown(e, mode, handle) {
    e.preventDefault();
    const startX = e.clientX, startY = e.clientY;
    const start = { ...rect };
    const av = els.aspect.value;
    const ratio = av !== "free" ? (() => { const [aw, ah] = av.split(":").map(Number); return aw / ah; })() : null;

    function onMove(ev) {
      const dx = ev.clientX - startX;
      const dy = ev.clientY - startY;
      if (mode === "move") {
        rect.x = start.x + dx;
        rect.y = start.y + dy;
      } else if (mode === "resize") {
        let w = Math.max(20, start.w + dx);
        let h = ratio ? w / ratio : Math.max(20, start.h + dy);
        rect.w = w;
        rect.h = h;
      }
      clampRect();
      drawCropBox();
    }
    function onUp() {
      document.removeEventListener("pointermove", onMove);
      document.removeEventListener("pointerup", onUp);
    }
    document.addEventListener("pointermove", onMove);
    document.addEventListener("pointerup", onUp);
  }
  els.cropBox.addEventListener("pointerdown", (e) => {
    if (e.target.classList.contains("crop-handle")) return;
    onPointerDown(e, "move");
  });
  const handle = els.cropBox.querySelector(".crop-handle");
  if (handle) handle.addEventListener("pointerdown", (e) => { e.stopPropagation(); onPointerDown(e, "resize"); });

  function canvasToBlob(canvas, mime, quality) {
    return new Promise((resolve) => canvas.toBlob(resolve, mime, quality));
  }

  els.cropBtn.addEventListener("click", async () => {
    if (!currentImg) return;
    els.cropBtn.disabled = true;
    els.cropBtn.textContent = "Cropping...";
    try {
      scaleX = currentImg.width / els.stageImg.clientWidth;
      scaleY = currentImg.height / els.stageImg.clientHeight;
      const sx = Math.round(rect.x * scaleX);
      const sy = Math.round(rect.y * scaleY);
      const sw = Math.round(rect.w * scaleX);
      const sh = Math.round(rect.h * scaleY);

      const canvas = document.createElement("canvas");
      canvas.width = sw;
      canvas.height = sh;
      canvas.getContext("2d").drawImage(currentImg, sx, sy, sw, sh, 0, 0, sw, sh);

      const outFormat = currentFile.type === "image/png" ? "png" : "jpeg";
      const mime = outFormat === "png" ? "image/png" : "image/jpeg";
      const blob = await canvasToBlob(canvas, mime, outFormat === "png" ? undefined : 0.92);

      const url = URL.createObjectURL(blob);
      els.preview.src = url;
      els.preview.style.display = "block";
      if (els.previewHint) els.previewHint.style.display = "none";

      const ext = outFormat === "png" ? "png" : "jpg";
      const base = (currentFile.name || "image").replace(/\.[^.]+$/, "");
      const filename = `${base}-cropped.${ext}`;

      setResult(
        `<strong>Cropped to ${sw}×${sh}.</strong> ${formatBytes(blob.size)}.<br><br>` +
        `<button id="dlBtn">Download ${filename}</button>`,
        "ok"
      );
      document.getElementById("dlBtn").addEventListener("click", () => downloadBlob(blob, filename));
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
      celebrateSuccess(els.cropBtn, els.result);
    } catch (err) {
      setResult(`<strong>Couldn't crop that image.</strong> ${err.message || "Try a different file."}`, "error");
    } finally {
      els.cropBtn.disabled = false;
      els.cropBtn.textContent = "Crop & download";
    }
  });
})();
