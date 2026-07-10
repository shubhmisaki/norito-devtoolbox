(function () {
  const I18N = i18nFor("app-removebg");
  const I18N_C = i18nFor("common");
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    originalInfo: document.getElementById("originalInfo"),
    processBtn: document.getElementById("processBtn"),
    result: document.getElementById("result"),
    preview: document.getElementById("preview"),
    previewHint: document.getElementById("previewHint"),
    bgMode: document.getElementById("bgMode"),
    bgColor: document.getElementById("bgColor"),
    bgColorField: document.getElementById("bgColorField"),
    downloadBtn: document.getElementById("downloadBtn"),
  };

  let currentImg = null;
  let segmenter = null;
  let lastResultBlob = null;

  function setResult(html, state) {
    const cls = state || "neutral";
    els.result.innerHTML = html;
    els.result.style.display = "block";
    els.result.classList.remove("ok", "error");
    if (cls === "ok" || cls === "error") els.result.classList.add(cls);
  }

  function pulseHighlight(el) {
    if (!el) return;
    el.classList.remove("highlight-pulse");
    void el.offsetWidth;
    el.classList.add("highlight-pulse");
    setTimeout(() => el.classList.remove("highlight-pulse"), 1300);
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

  async function handleFile(file) {
    if (!file || !file.type.startsWith("image/")) {
      setResult(I18N_C.please_choose_image || "Please choose an image file.", "error");
      return;
    }
    currentImg = await loadImageFile(file);
    els.originalInfo.textContent = `${file.name}, ${currentImg.width}×${currentImg.height}`;
    els.originalInfo.style.display = "block";
    els.processBtn.disabled = false;
  }

  els.drop.addEventListener("click", () => els.fileInput.click());
  els.fileInput.addEventListener("change", (e) => handleFile(e.target.files[0]));
  ["dragenter", "dragover"].forEach((evt) =>
    els.drop.addEventListener(evt, (e) => { e.preventDefault(); els.drop.classList.add("drag"); })
  );
  ["dragleave", "drop"].forEach((evt) =>
    els.drop.addEventListener(evt, (e) => { e.preventDefault(); els.drop.classList.remove("drag"); })
  );
  els.drop.addEventListener("drop", (e) => {
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  });

  // Paste an image straight from the clipboard (screenshot tools, "Copy image", etc.)
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

  els.bgMode.addEventListener("change", () => {
    els.bgColorField.style.display = els.bgMode.value === "color" ? "flex" : "none";
  });

  // Wrap a promise with a hard timeout so a stalled model load or a stalled
  // inference call surfaces as a clear error instead of hanging the button
  // on "Loading…" forever with no feedback, the most likely shape of a
  // "this tool doesn't work" report for a WASM-backed tool like this one.
  function withTimeout(promise, ms, message) {
    let timer;
    const timeout = new Promise((_, reject) => {
      timer = setTimeout(() => reject(new Error(message)), ms);
    });
    return Promise.race([promise, timeout]).finally(() => clearTimeout(timer));
  }

  async function getSegmenter() {
    if (segmenter) return segmenter;
    if (typeof SelfieSegmentation === "undefined") {
      throw new Error(
        I18N.err_lib_not_loaded || "The background-removal library didn't load. Check your connection and reload the page."
      );
    }
    console.log("[remove-bg] creating SelfieSegmentation instance…");
    const seg = new SelfieSegmentation({
      locateFile: (file) => `js/vendor/mediapipe/${file}`,
    });
    seg.setOptions({ modelSelection: 0, selfieMode: false });
    try {
      await withTimeout(
        seg.initialize(),
        20000,
        I18N.err_model_timeout || "The segmentation model took too long to load. Check your connection and try again."
      );
    } catch (err) {
      console.error("[remove-bg] initialize() failed:", err);
      throw err;
    }
    console.log("[remove-bg] model ready.");
    segmenter = seg;
    return segmenter;
  }

  function runSegmentation(seg, imgEl) {
    const inference = new Promise((resolve, reject) => {
      seg.onResults((results) => resolve(results));
      seg.send({ image: imgEl }).catch(reject);
    });
    return withTimeout(
      inference,
      20000,
      I18N.err_processing_timeout || "Processing took too long. Try a smaller image (under 4 megapixels works best)."
    );
  }

  function composite(image, mask, mode, color) {
    const w = image.width, h = image.height;
    const out = document.createElement("canvas");
    out.width = w; out.height = h;
    const octx = out.getContext("2d");
    octx.drawImage(image, 0, 0, w, h);
    const imgData = octx.getImageData(0, 0, w, h);

    const maskCanvas = document.createElement("canvas");
    maskCanvas.width = w; maskCanvas.height = h;
    const mctx = maskCanvas.getContext("2d");
    mctx.drawImage(mask, 0, 0, w, h);
    const maskData = mctx.getImageData(0, 0, w, h).data;

    for (let i = 0; i < imgData.data.length; i += 4) {
      const alpha = maskData[i]; // grayscale confidence, 0-255
      imgData.data[i + 3] = alpha;
    }
    octx.putImageData(imgData, 0, 0);

    if (mode === "color") {
      const final = document.createElement("canvas");
      final.width = w; final.height = h;
      const fctx = final.getContext("2d");
      fctx.fillStyle = color;
      fctx.fillRect(0, 0, w, h);
      fctx.drawImage(out, 0, 0);
      return final;
    }
    return out;
  }

  els.processBtn.addEventListener("click", async () => {
    if (!currentImg) return;
    els.processBtn.disabled = true;
    els.processBtn.textContent = I18N.loading_model_label || "Loading model…";
    setResult(
      I18N.loading_model_status || "Loading the segmentation model: about 5.5 MB, only happens once per browser session.",
      "neutral"
    );

    try {
      const seg = await getSegmenter();
      els.processBtn.textContent = I18N.processing_label || "Processing…";
      const results = await runSegmentation(seg, currentImg);
      const canvas = composite(results.image, results.segmentationMask, els.bgMode.value, els.bgColor.value);

      canvas.toBlob((blob) => {
        lastResultBlob = blob;
        const url = URL.createObjectURL(blob);
        els.preview.src = url;
        els.preview.style.display = "block";
        if (els.previewHint) els.previewHint.style.display = "none";
        els.downloadBtn.disabled = false;
        setResult(
          I18N.result_success || "<strong>Background removed successfully.</strong> Works best on photos where a person is the main subject. quality depends on the lightweight model used, not on your image.",
          "ok"
        );
        els.preview.scrollIntoView({ behavior: "smooth", block: "center" });
        pulseHighlight(els.downloadBtn);
        celebrateSuccess(els.processBtn, els.result);
      }, "image/png");
    } catch (err) {
      console.error("[remove-bg] processing failed:", err);
      const msg = err && err.message ? err.message : (I18N.err_unexpected || "Something unexpected happened.");
      setResult(`<strong>${I18N.err_generic_prefix || "Couldn't remove the background."}</strong> ${msg}`, "error");
    } finally {
      els.processBtn.disabled = false;
      els.processBtn.textContent = I18N.btn_remove_default || "Remove background";
    }
  });

  els.downloadBtn.addEventListener("click", () => {
    if (!lastResultBlob) return;
    const url = URL.createObjectURL(lastResultBlob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "cutout.png";
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 2000);
  });
})();
