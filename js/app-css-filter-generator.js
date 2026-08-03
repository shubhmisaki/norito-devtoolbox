(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    preview: document.getElementById("previewImg"),
    output: document.getElementById("output"),
    copyBtn: document.getElementById("copyBtn"),
    resetBtn: document.getElementById("resetBtn"),
  };

  const sliders = [
    { id: "fBlur", unit: "px", fn: "blur", neutral: 0 },
    { id: "fBrightness", unit: "%", fn: "brightness", neutral: 100 },
    { id: "fContrast", unit: "%", fn: "contrast", neutral: 100 },
    { id: "fSaturate", unit: "%", fn: "saturate", neutral: 100 },
    { id: "fGrayscale", unit: "%", fn: "grayscale", neutral: 0 },
    { id: "fSepia", unit: "%", fn: "sepia", neutral: 0 },
    { id: "fHue", unit: "deg", fn: "hue-rotate", neutral: 0 },
    { id: "fInvert", unit: "%", fn: "invert", neutral: 0 },
  ].map((s) => ({ ...s, input: document.getElementById(s.id), valSpan: document.getElementById(s.id + "Val") }));

  let currentImgUrl = null;

  function update() {
    const parts = [];
    sliders.forEach((s) => {
      const v = Number(s.input.value);
      s.valSpan.textContent = `${v}${s.unit}`;
      if (v !== s.neutral) parts.push(`${s.fn}(${v}${s.unit})`);
    });
    const css = parts.length ? parts.join(" ") : "none";
    els.preview.style.filter = css === "none" ? "" : css;
    els.output.textContent = `filter: ${css};`;
  }

  sliders.forEach((s) => s.input.addEventListener("input", update));
  update();

  els.resetBtn.addEventListener("click", () => {
    sliders.forEach((s) => { s.input.value = s.neutral; });
    update();
  });

  async function loadFile(file) {
    if (!file || !file.type.startsWith("image/")) return;
    try {
      const { img, url } = await loadImageFile(file);
      if (currentImgUrl) URL.revokeObjectURL(currentImgUrl);
      currentImgUrl = url;
      els.preview.src = currentImgUrl;
      update();
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

  els.copyBtn.addEventListener("click", async () => {
    if (!els.output.textContent) return;
    try {
      await copyToClipboard(els.output.textContent);
      const I18N_C = i18nFor("common");
      showMascotToast(I18N_C.copied || "Copied!");
      celebrateSuccess(els.copyBtn);
    } catch (e) { /* clipboard unavailable, silently ignore */ }
  });
})();
