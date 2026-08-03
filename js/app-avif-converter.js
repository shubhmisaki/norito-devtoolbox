(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    format: document.getElementById("format"),
    qualityRow: document.getElementById("qualityRow"),
    quality: document.getElementById("quality"),
    qualityVal: document.getElementById("qualityVal"),
    convertBtn: document.getElementById("convertBtn"),
    result: document.getElementById("result"),
    unsupportedNote: document.getElementById("unsupportedNote"),
    preview: document.getElementById("preview"),
    previewHint: document.getElementById("previewHint"),
  };

  let currentImg = null;
  let avifEncodeSupported = null; // cached feature-detect result

  function checkAvifSupport() {
    return new Promise((resolve) => {
      if (avifEncodeSupported !== null) return resolve(avifEncodeSupported);
      const c = document.createElement("canvas");
      c.width = 1; c.height = 1;
      c.toBlob((blob) => {
        avifEncodeSupported = !!blob;
        resolve(avifEncodeSupported);
      }, "image/avif");
    });
  }

  async function loadFile(file) {
    if (!file) return;
    try {
      const { img, url } = await loadImageFile(file);
      URL.revokeObjectURL(url);
      currentImg = img;
      els.convertBtn.disabled = false;
      updateUnsupportedNote();
    } catch (e) {
      els.result.textContent = "Couldn't read that file as an image.";
      els.result.className = "result-box error";
      els.result.style.display = "block";
    }
  }

  async function updateUnsupportedNote() {
    els.qualityRow.style.display = els.format.value === "image/png" ? "none" : "block";
    if (els.format.value === "image/avif") {
      const supported = await checkAvifSupport();
      if (!supported) {
        els.unsupportedNote.textContent = "Your browser can't encode AVIF. Try current Chrome, Edge, or Firefox, or convert to JPEG/PNG instead.";
        els.unsupportedNote.style.display = "block";
        els.convertBtn.disabled = true;
        return;
      }
    }
    els.unsupportedNote.style.display = "none";
    if (currentImg) els.convertBtn.disabled = false;
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

  els.format.addEventListener("change", updateUnsupportedNote);
  els.quality.addEventListener("input", () => {
    els.qualityVal.textContent = `${els.quality.value}%`;
  });
  updateUnsupportedNote();

  els.convertBtn.addEventListener("click", async () => {
    if (!currentImg) return;
    const mime = els.format.value;
    const canvas = document.createElement("canvas");
    canvas.width = currentImg.naturalWidth;
    canvas.height = currentImg.naturalHeight;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(currentImg, 0, 0);

    const quality = mime === "image/png" ? undefined : Number(els.quality.value) / 100;
    canvas.toBlob((blob) => {
      if (!blob) {
        els.result.textContent = "Conversion failed, your browser may not support this output format.";
        els.result.className = "result-box error";
        els.result.style.display = "block";
        return;
      }
      const ext = { "image/avif": "avif", "image/jpeg": "jpg", "image/png": "png" }[mime];
      const url = URL.createObjectURL(blob);
      els.preview.src = url;
      els.preview.style.display = "block";
      if (els.previewHint) els.previewHint.style.display = "none";
      els.result.textContent = `Converted: ${formatBytes(blob.size)}`;
      els.result.className = "result-box";
      els.result.style.display = "block";
      downloadBlob(blob, `converted.${ext}`);
    }, mime, quality);
  });
})();
