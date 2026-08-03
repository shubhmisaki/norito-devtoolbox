(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    preset: document.getElementById("preset"),
    editorWrap: document.getElementById("editorWrap"),
    zoom: document.getElementById("zoom"),
    zoomVal: document.getElementById("zoomVal"),
    panX: document.getElementById("panX"),
    panY: document.getElementById("panY"),
    stage: document.getElementById("cropStage"),
    canvas: document.getElementById("cropCanvas"),
    previewHint: document.getElementById("previewHint"),
    downloadBtn: document.getElementById("downloadBtn"),
  };
  const ctx = els.canvas.getContext("2d");

  let currentImg = null;
  let currentImgUrl = null;

  function targetSize() {
    const opt = els.preset.options[els.preset.selectedIndex];
    return { w: Number(opt.dataset.w), h: Number(opt.dataset.h) };
  }

  function render() {
    if (!currentImg) return;
    const { w: targetW, h: targetH } = targetSize();
    const targetRatio = targetW / targetH;

    // Display canvas at a manageable on-screen size while sampling from full-res source.
    const displayW = Math.min(480, targetW);
    const displayH = displayW / targetRatio;
    els.canvas.width = displayW;
    els.canvas.height = displayH;
    els.stage.style.width = `${displayW}px`;

    const iw = currentImg.naturalWidth, ih = currentImg.naturalHeight;
    const imgRatio = iw / ih;

    // "cover" base scale: source rect size that exactly fills target ratio.
    let baseSrcW, baseSrcH;
    if (imgRatio > targetRatio) {
      baseSrcH = ih;
      baseSrcW = ih * targetRatio;
    } else {
      baseSrcW = iw;
      baseSrcH = iw / targetRatio;
    }

    const zoom = Number(els.zoom.value) / 100;
    const srcW = baseSrcW / zoom;
    const srcH = baseSrcH / zoom;

    const maxX = iw - srcW;
    const maxY = ih - srcH;
    const panX = Number(els.panX.value) / 100;
    const panY = Number(els.panY.value) / 100;
    const srcX = maxX * panX;
    const srcY = maxY * panY;

    ctx.clearRect(0, 0, displayW, displayH);
    ctx.drawImage(currentImg, srcX, srcY, srcW, srcH, 0, 0, displayW, displayH);
  }

  async function loadFile(file) {
    if (!file || !file.type.startsWith("image/")) return;
    try {
      const { img, url } = await loadImageFile(file);
      if (currentImgUrl) URL.revokeObjectURL(currentImgUrl);
      currentImg = img;
      currentImgUrl = url;
      els.editorWrap.style.display = "block";
      els.downloadBtn.disabled = false;
      els.previewHint.style.display = "none";
      render();
    } catch (e) { /* couldn't read image, silently ignore */ }
  }

  els.fileInput.addEventListener("change", () => loadFile(els.fileInput.files[0]));
  wireDragDrop(els.drop, (e) => {
    const file = e.dataTransfer.files && e.dataTransfer.files[0];
    loadFile(file);
  });
  els.drop.addEventListener("click", (e) => {
    if (e.target === els.fileInput) return;
    els.fileInput.click();
  });

  [els.preset, els.zoom, els.panX, els.panY].forEach((el) =>
    el.addEventListener("input", () => {
      els.zoomVal.textContent = `${els.zoom.value}%`;
      render();
    })
  );

  els.downloadBtn.addEventListener("click", () => {
    if (!currentImg) return;
    const { w: targetW, h: targetH } = targetSize();
    const outCanvas = document.createElement("canvas");
    outCanvas.width = targetW;
    outCanvas.height = targetH;
    const outCtx = outCanvas.getContext("2d");

    const iw = currentImg.naturalWidth, ih = currentImg.naturalHeight;
    const targetRatio = targetW / targetH;
    const imgRatio = iw / ih;
    let baseSrcW, baseSrcH;
    if (imgRatio > targetRatio) {
      baseSrcH = ih; baseSrcW = ih * targetRatio;
    } else {
      baseSrcW = iw; baseSrcH = iw / targetRatio;
    }
    const zoom = Number(els.zoom.value) / 100;
    const srcW = baseSrcW / zoom;
    const srcH = baseSrcH / zoom;
    const maxX = iw - srcW, maxY = ih - srcH;
    const srcX = maxX * (Number(els.panX.value) / 100);
    const srcY = maxY * (Number(els.panY.value) / 100);

    outCtx.drawImage(currentImg, srcX, srcY, srcW, srcH, 0, 0, targetW, targetH);
    outCanvas.toBlob((blob) => {
      if (blob) downloadBlob(blob, `cropped-${targetW}x${targetH}.jpg`);
    }, "image/jpeg", 0.92);
  });
})();
