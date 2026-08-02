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
  let ortSession = null;
  let lastResultBlob = null;

  // This file always lives at ".../js/app-removebg.js", whether the page
  // loading it is at the site root (src="js/app-removebg.js") or nested
  // under a locale folder (src="../js/app-removebg.js"). Resolving the
  // model/runtime paths against THIS SCRIPT's own URL, instead of against
  // the page's URL, means they land in the right place either way. A plain
  // page-relative string like "js/vendor/onnxruntime/" breaks on nested
  // pages: from /es/remove-background.html it resolves to the nonexistent
  // /es/js/vendor/onnxruntime/ instead of the real /js/vendor/onnxruntime/.
  const SCRIPT_DIR = (function () {
    var src = document.currentScript && document.currentScript.src;
    if (!src) {
      var scripts = document.getElementsByTagName("script");
      for (var i = 0; i < scripts.length; i++) {
        if (/app-removebg\.js(\?|$)/.test(scripts[i].src)) { src = scripts[i].src; break; }
      }
    }
    return src ? src.replace(/[^/]*$/, "") : "js/"; // strip filename, keep trailing slash
  })();
  const MODEL_URL = SCRIPT_DIR + "vendor/modnet/model_quantized.onnx";
  const WASM_DIR = SCRIPT_DIR + "vendor/onnxruntime/";

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

  async function handleFile(file) {
    if (!file || !file.type.startsWith("image/")) {
      setResult(I18N_C.please_choose_image || "Please choose an image file.", "error");
      return;
    }
    const { img, url } = await loadImageFile(file);
    currentImg = img;
    URL.revokeObjectURL(url); // only used to decode; the model/canvas work below doesn't need it alive
    els.originalInfo.textContent = `${file.name}, ${currentImg.width}×${currentImg.height}`;
    els.originalInfo.style.display = "block";
    els.processBtn.disabled = false;
  }

  els.drop.addEventListener("click", () => els.fileInput.click());
  els.fileInput.addEventListener("change", (e) => {
    if (e.target.files.length > 1) startBatch(e.target.files);
    else if (e.target.files[0]) handleFile(e.target.files[0]);
  });
  wireDragDrop(els.drop, (e) => {
    if (e.dataTransfer.files.length > 1) startBatch(e.dataTransfer.files);
    else if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
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

  // ---- ONNX Runtime session (MODNet portrait matting) ----
  async function getSession() {
    if (ortSession) return ortSession;
    if (typeof ort === "undefined") {
      throw new Error(
        I18N.err_lib_not_loaded || "The background-removal library didn't load. Check your connection and reload the page."
      );
    }
    console.log("[remove-bg] creating ONNX Runtime session…");
    // Must be an absolute URL, not a bare relative string: onnxruntime-web
    // internally does a dynamic import() for its .mjs companion file, and
    // dynamic import specifiers have to resolve like a real URL. A plain
    // "js/vendor/onnxruntime/" string works fine for fetch() but fails
    // import() resolution with "Failed to resolve module specifier".
    ort.env.wasm.wasmPaths = new URL(WASM_DIR, document.baseURI).href;
    // The bundled wasm binary supports multithreading, but running single-
    // threaded avoids needing cross-origin-isolation (COOP/COEP) headers,
    // which this static site doesn't set. Slightly slower, works everywhere.
    ort.env.wasm.numThreads = 1;
    ort.env.wasm.simd = true;
    try {
      ortSession = await withTimeout(
        ort.InferenceSession.create(MODEL_URL, { executionProviders: ["wasm"] }),
        30000,
        I18N.err_model_timeout || "The segmentation model took too long to load. Check your connection and try again."
      );
    } catch (err) {
      console.error("[remove-bg] session create failed:", err);
      throw err;
    }
    console.log("[remove-bg] model ready.");
    return ortSession;
  }

  // MODNet's own reference preprocessing: resize so the longer side lands
  // near 512px (upscaling small images up to that size too), then round
  // both dimensions down to a multiple of 32, since the network's encoder
  // downsamples by 32x internally and needs dimensions it divides evenly.
  function computeTargetSize(w, h) {
    const REF = 512;
    let rw, rh;
    if (Math.max(w, h) < REF || Math.min(w, h) > REF) {
      if (w >= h) { rh = REF; rw = Math.round((w / h) * REF); }
      else { rw = REF; rh = Math.round((h / w) * REF); }
    } else {
      rw = w; rh = h;
    }
    rw -= rw % 32;
    rh -= rh % 32;
    return { rw: Math.max(32, rw), rh: Math.max(32, rh) };
  }

  // Draws the image at the target inference size and returns a normalized
  // NCHW Float32 tensor: pixel/255 rescaled, then (x - 0.5) / 0.5 so values
  // land in [-1, 1], matching the mean=0.5/std=0.5 preprocessing MODNet was
  // exported with.
  function imageToTensor(imgEl, rw, rh) {
    const c = document.createElement("canvas");
    c.width = rw; c.height = rh;
    const ctx = c.getContext("2d");
    ctx.drawImage(imgEl, 0, 0, rw, rh);
    const { data } = ctx.getImageData(0, 0, rw, rh);
    const size = rw * rh;
    const float = new Float32Array(size * 3);
    for (let i = 0, p = 0; i < data.length; i += 4, p++) {
      const r = data[i] / 255, g = data[i + 1] / 255, b = data[i + 2] / 255;
      float[p] = (r - 0.5) / 0.5;
      float[size + p] = (g - 0.5) / 0.5;
      float[2 * size + p] = (b - 0.5) / 0.5;
    }
    return new ort.Tensor("float32", float, [1, 3, rh, rw]);
  }

  // Runs the model and returns a small grayscale canvas holding the raw
  // alpha matte at inference resolution. composite() below scales this up
  // to the original image size the same way it already scales the old
  // MediaPipe mask, so the rest of the pipeline barely changes.
  async function runSegmentation(session, imgEl) {
    const { rw, rh } = computeTargetSize(imgEl.width, imgEl.height);
    const input = imageToTensor(imgEl, rw, rh);
    const inputName = session.inputNames.includes("input") ? "input" : session.inputNames[0];
    const outputName = session.outputNames.includes("output") ? "output" : session.outputNames[0];

    const results = await withTimeout(
      session.run({ [inputName]: input }),
      30000,
      I18N.err_processing_timeout || "Processing took too long. Try a smaller image (under 4 megapixels works best)."
    );
    const out = results[outputName];
    const [, , oh, ow] = out.dims.length === 4 ? out.dims : [1, 1, rh, rw];

    const maskCanvas = document.createElement("canvas");
    maskCanvas.width = ow; maskCanvas.height = oh;
    const mctx = maskCanvas.getContext("2d");
    const maskImg = mctx.createImageData(ow, oh);
    const data = out.data; // Float32Array, values ~0..1
    for (let p = 0; p < ow * oh; p++) {
      const v = Math.round(Math.max(0, Math.min(1, data[p])) * 255);
      maskImg.data[p * 4] = v;
      maskImg.data[p * 4 + 1] = v;
      maskImg.data[p * 4 + 2] = v;
      maskImg.data[p * 4 + 3] = 255;
    }
    mctx.putImageData(maskImg, 0, 0);
    return maskCanvas;
  }

  // Smooths a single-channel mask with a separable box blur (two 1D passes,
  // sliding-window sums so cost stays linear in pixel count regardless of
  // radius). MODNet's matte is already fairly clean, so this only needs a
  // light touch to smooth upscaling artifacts, not to fix blocky model
  // output the way the old segmentation-mask approach required.
  function boxBlurMask(data, w, h, radius) {
    if (radius <= 0) return Uint8ClampedArray.from(data);
    const tmp = new Float32Array(w * h);
    const out = new Uint8ClampedArray(w * h);
    const winSize = radius * 2 + 1;

    for (let y = 0; y < h; y++) {
      const rowStart = y * w;
      let sum = 0;
      for (let x = -radius; x <= radius; x++) {
        const xi = Math.min(w - 1, Math.max(0, x));
        sum += data[rowStart + xi];
      }
      for (let x = 0; x < w; x++) {
        tmp[rowStart + x] = sum / winSize;
        const addXi = Math.min(w - 1, x + radius + 1);
        const subXi = Math.max(0, x - radius);
        sum += data[rowStart + addXi] - data[rowStart + subXi];
      }
    }

    for (let x = 0; x < w; x++) {
      let sum = 0;
      for (let y = -radius; y <= radius; y++) {
        const yi = Math.min(h - 1, Math.max(0, y));
        sum += tmp[yi * w + x];
      }
      for (let y = 0; y < h; y++) {
        out[y * w + x] = sum / winSize;
        const addYi = Math.min(h - 1, y + radius + 1);
        const subYi = Math.max(0, y - radius);
        sum += tmp[addYi * w + x] - tmp[subYi * w + x];
      }
    }
    return out;
  }

  // MODNet already outputs a real alpha matte (not a coarse probability
  // mask), so this remap is a light cleanup pass rather than the heavy
  // lift it was for the old model: it snaps near-zero background haze to
  // fully transparent and near-one subject pixels to fully opaque, with a
  // smoothstep ramp (instead of a hard linear one) across the narrow band
  // in between so hair and soft edges stay soft instead of getting a
  // stair-stepped edge.
  const ALPHA_LOW = 15;
  const ALPHA_HIGH = 210;

  function remapAlpha(raw) {
    if (raw <= ALPHA_LOW) return 0;
    if (raw >= ALPHA_HIGH) return 255;
    const t = (raw - ALPHA_LOW) / (ALPHA_HIGH - ALPHA_LOW);
    return Math.round(t * t * (3 - 2 * t) * 255); // smoothstep
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
    const maskPixels = mctx.getImageData(0, 0, w, h).data;

    const maskGray = new Uint8ClampedArray(w * h);
    for (let i = 0, p = 0; i < maskPixels.length; i += 4, p++) {
      maskGray[p] = maskPixels[i]; // mask is grayscale: R === G === B
    }
    const blurred = boxBlurMask(maskGray, w, h, 1);

    for (let i = 0, p = 0; i < imgData.data.length; i += 4, p++) {
      imgData.data[i + 3] = remapAlpha(blurred[p]);
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
      I18N.loading_model_status || "Loading the portrait-matting model and its runtime: about 18 MB combined, only happens once per browser session.",
      "neutral"
    );

    try {
      const session = await getSession();
      els.processBtn.textContent = I18N.processing_label || "Processing…";
      const mask = await runSegmentation(session, currentImg);
      const canvas = composite(currentImg, mask, els.bgMode.value, els.bgColor.value);

      canvas.toBlob((blob) => {
        lastResultBlob = blob;
        const url = URL.createObjectURL(blob);
        els.preview.src = url;
        els.preview.style.display = "block";
        if (els.previewHint) els.previewHint.style.display = "none";
        els.downloadBtn.disabled = false;
        setResult(
          I18N.result_success || "<strong>Background removed successfully.</strong> Works best on photos where a person is the main subject.",
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

  // ---- Batch mode ----
  const batchEls = {
    list: document.getElementById("batchList"),
    actions: document.getElementById("batchActions"),
    processBtn: document.getElementById("batchProcessBtn"),
    zipBtn: document.getElementById("batchZipBtn"),
  };
  let batchFiles = [];

  function escapeHtml(s) {
    return String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function renderBatchList() {
    if (!batchEls.list) return;
    batchEls.list.innerHTML = batchFiles
      .map((bf, i) => {
        const statusClass = bf.status === "ok" ? "ok" : bf.status === "error" ? "error" : "pending";
        const statusText = bf.status === "ok"
          ? "Done"
          : bf.status === "error"
          ? (bf.error || "Failed")
          : bf.status === "processing"
          ? "Processing..."
          : "Waiting...";
        return `<div class="batch-file-row" data-i="${i}">
          <span class="bf-name">${escapeHtml(bf.file.name)}</span>
          <span class="bf-meta bf-status ${statusClass}">${statusText}</span>
          <button type="button" class="bf-remove" data-i="${i}" aria-label="Remove">&times;</button>
        </div>`;
      })
      .join("");
    batchEls.list.querySelectorAll(".bf-remove").forEach((btn) => {
      btn.addEventListener("click", () => {
        const i = Number(btn.dataset.i);
        batchFiles.splice(i, 1);
        if (!batchFiles.length) {
          batchEls.list.style.display = "none";
          batchEls.actions.style.display = "none";
        } else {
          renderBatchList();
        }
      });
    });
  }

  function startBatch(fileList) {
    const files = Array.from(fileList).filter((f) => f.type.startsWith("image/"));
    if (!files.length) {
      setResult(I18N_C.please_choose_image || "Please choose an image file.", "error");
      return;
    }
    batchFiles = files.map((file) => ({ file, status: "pending", blob: null, error: "" }));
    els.originalInfo.style.display = "none";
    els.result.style.display = "none";
    els.preview.style.display = "none";
    if (els.previewHint) els.previewHint.style.display = "none";
    batchEls.list.style.display = "block";
    batchEls.actions.style.display = "flex";
    batchEls.zipBtn.disabled = true;
    renderBatchList();
  }

  async function runBatch() {
    batchEls.processBtn.disabled = true;
    batchEls.processBtn.textContent = I18N.loading_model_label || "Loading model...";
    let session;
    try {
      session = await getSession();
    } catch (err) {
      console.error("[remove-bg] batch: model load failed:", err);
      batchFiles.forEach((bf) => { bf.status = "error"; bf.error = err.message || "Model failed to load"; });
      renderBatchList();
      batchEls.processBtn.disabled = false;
      batchEls.processBtn.textContent = "Remove backgrounds from all";
      return;
    }
    batchEls.processBtn.textContent = I18N.processing_label || "Processing...";
    for (const bf of batchFiles) {
      bf.status = "processing";
      renderBatchList();
      try {
        const { img, url } = await loadImageFile(bf.file);
        URL.revokeObjectURL(url);
        const mask = await runSegmentation(session, img);
        const canvas = composite(img, mask, els.bgMode.value, els.bgColor.value);
        const blob = await new Promise((resolve) => canvas.toBlob(resolve, "image/png"));
        bf.blob = blob;
        bf.status = "ok";
      } catch (err) {
        bf.status = "error";
        bf.error = err.message || "Couldn't process";
      }
      renderBatchList();
    }
    batchEls.processBtn.disabled = false;
    batchEls.processBtn.textContent = "Remove backgrounds from all";
    const anyOk = batchFiles.some((bf) => bf.status === "ok");
    batchEls.zipBtn.disabled = !anyOk;
    if (anyOk) celebrateSuccess(batchEls.processBtn, batchEls.list, "Done");
  }

  if (batchEls.processBtn) batchEls.processBtn.addEventListener("click", runBatch);
  if (batchEls.zipBtn) {
    batchEls.zipBtn.addEventListener("click", async () => {
      const entries = [];
      for (const bf of batchFiles) {
        if (bf.status !== "ok" || !bf.blob) continue;
        const base = (bf.file.name || "image").replace(/\.[^.]+$/, "");
        const bytes = new Uint8Array(await bf.blob.arrayBuffer());
        entries.push({ name: `${base}-cutout.png`, bytes });
      }
      if (!entries.length) return;
      const zipBytes = createZip(entries);
      const blob = new Blob([zipBytes], { type: "application/zip" });
      downloadBlob(blob, "cutouts.zip");
      celebrateSuccess(batchEls.zipBtn, batchEls.list, "Downloaded");
    });
  }
})();
