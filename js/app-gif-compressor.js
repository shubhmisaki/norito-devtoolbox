(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    frameList: document.getElementById("frameList"),
    bulkToolbar: document.getElementById("bulkToolbar"),
    skipSelect: document.getElementById("skipSelect"),
    applySkipBtn: document.getElementById("applySkipBtn"),
    controls: document.getElementById("controls"),
    originalInfo: document.getElementById("originalInfo"),
    scaleInput: document.getElementById("scaleInput"),
    lossyInput: document.getElementById("lossyInput"),
    reduceColorsCheck: document.getElementById("reduceColorsCheck"),
    colorsInput: document.getElementById("colorsInput"),
    compressBtn: document.getElementById("compressBtn"),
    result: document.getElementById("result"),
    preview: document.getElementById("preview"),
  };

  let currentFile = null;
  let decoded = null; // { width, height, frames }, frames is what we actually encode from
  let originalFrames = null; // untouched snapshot from decode, for the "Keep frames" bulk action
  let strip = null;

  function setResult(html, state) {
    els.result.innerHTML = html;
    els.result.style.display = "block";
    els.result.className = "result-box " + (state || "");
  }

  async function handleFile(file) {
    if (!file || !/image\/gif/.test(file.type)) {
      setResult("<strong>That's not a GIF.</strong> Choose a .gif file.", "error");
      return;
    }
    currentFile = file;
    els.result.style.display = "none";
    els.preview.style.display = "none";
    els.controls.style.display = "none";
    els.bulkToolbar.style.display = "none";
    els.frameList.style.display = "none";
    els.frameList.innerHTML = "";
    try {
      decoded = await decodeGifFile(file);
      originalFrames = decoded.frames.map((f) => Object.assign({}, f));
      els.originalInfo.textContent =
        `${file.name}: ${decoded.width}×${decoded.height}, ${decoded.frames.length} frames, ${formatBytes(file.size)}`;
      els.controls.style.display = "block";
      els.bulkToolbar.style.display = "flex";
      els.frameList.style.display = "flex";
      strip = renderFrameStrip(els.frameList, decoded.frames, { allowRemove: true });
    } catch (err) {
      setResult(`<strong>Couldn't read that GIF.</strong> ${err.message || "Try a different file."}`, "error");
    }
  }

  els.fileInput.addEventListener("change", () => handleFile(els.fileInput.files[0]));
  wireDragDrop(els.drop, (e) => handleFile(e.dataTransfer.files[0]));
  els.drop.addEventListener("click", (e) => {
    if (e.target === els.fileInput) return;
    els.fileInput.click();
  });

  els.applySkipBtn.addEventListener("click", () => {
    if (!originalFrames) return;
    const n = Number(els.skipSelect.value) || 1;
    decoded.frames = bulkKeepEveryNth(originalFrames, n);
    strip = renderFrameStrip(els.frameList, decoded.frames, { allowRemove: true });
  });

  els.reduceColorsCheck.addEventListener("change", () => {
    els.colorsInput.disabled = !els.reduceColorsCheck.checked;
  });

  els.compressBtn.addEventListener("click", async () => {
    if (!decoded || !decoded.frames.length) return;
    const scale = Math.min(100, Math.max(10, Number(els.scaleInput.value) || 100)) / 100;
    const lossy = Math.max(0, Math.min(200, Number(els.lossyInput.value) || 0));
    const colors = els.reduceColorsCheck.checked ? Math.max(2, Math.min(256, Number(els.colorsInput.value) || 128)) : 0;

    const outW = Math.max(1, Math.round(decoded.width * scale));
    const outH = Math.max(1, Math.round(decoded.height * scale));

    els.compressBtn.disabled = true;
    els.compressBtn.textContent = "Re-encoding...";
    els.result.style.display = "none";

    try {
      // Stage 1: apply frame edits (removed/reordered frames, per-frame delay
      // changes) and scaling via our own canvas pipeline.
      const frames = decoded.frames.map((f) => {
        const canvas = document.createElement("canvas");
        canvas.width = outW;
        canvas.height = outH;
        const src = frameSourceEl(f);
        canvas.getContext("2d").drawImage(src, 0, 0, outW, outH);
        return { canvas, delay: f.delay };
      });

      const stage1Blob = await encodeGif(frames, {
        width: outW,
        height: outH,
        quality: 10,
        onProgress: (f) => { els.compressBtn.textContent = `Re-encoding... ${Math.round(f * 100)}%`; },
      });

      // Stage 2: real lossy compression + frame-difference optimization via
      // gifsicle (WASM), the same engine most GIF-compression sites run
      // server-side.
      els.compressBtn.textContent = "Compressing...";
      const blob = await compressWithGifsicle(stage1Blob, { lossy, colors, optimize: true });

      const url = URL.createObjectURL(blob);
      els.preview.src = url;
      els.preview.style.display = "block";

      const savedPct = Math.max(0, Math.round((1 - blob.size / currentFile.size) * 100));
      setResult(
        `<strong>Compressed.</strong> ${formatBytes(currentFile.size)} &rarr; ${formatBytes(blob.size)}` +
        (savedPct > 0 ? ` (${savedPct}% smaller).` : ".") +
        `<br><br><button id="dlBtn">Download compressed.gif</button>`,
        "ok"
      );
      document.getElementById("dlBtn").addEventListener("click", () => downloadBlob(blob, "compressed.gif"));
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
      if (typeof celebrateSuccess === "function") celebrateSuccess(els.compressBtn, els.result);
    } catch (err) {
      setResult(`<strong>Couldn't compress that GIF.</strong> ${err.message || "Try a lower scale or lossy level."}`, "error");
    } finally {
      els.compressBtn.disabled = false;
      els.compressBtn.textContent = "Compress GIF";
    }
  });
})();
