(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    frameList: document.getElementById("frameList"),
    bulkToolbar: document.getElementById("bulkToolbar"),
    skipSelect: document.getElementById("skipSelect"),
    applySkipBtn: document.getElementById("applySkipBtn"),
    dedupeBtn: document.getElementById("dedupeBtn"),
    controls: document.getElementById("controls"),
    originalInfo: document.getElementById("originalInfo"),
    scaleInput: document.getElementById("scaleInput"),
    lossyInput: document.getElementById("lossyInput"),
    reduceColorsCheck: document.getElementById("reduceColorsCheck"),
    colorsInput: document.getElementById("colorsInput"),
    compressBtn: document.getElementById("compressBtn"),
    presetsBtn: document.getElementById("presetsBtn"),
    presetResults: document.getElementById("presetResults"),
    result: document.getElementById("result"),
    preview: document.getElementById("preview"),
  };

  let currentFile = null;
  let decoded = null; // { width, height, frames }, frames is what we actually encode from
  let originalFrames = null; // untouched snapshot from decode, for the "Keep frames" bulk action
  let strip = null;
  let busy = false; // true while compressing, so a mid-flight file swap can't pull the rug out

  function setResult(html, state) {
    els.result.innerHTML = html;
    els.result.style.display = "block";
    els.result.className = "result-box " + (state || "");
  }

  async function handleFile(file) {
    if (busy) {
      setResult("<strong>Still compressing the previous GIF.</strong> Wait for it to finish first.", "error");
      return;
    }
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
    els.presetResults.style.display = "none";
    els.presetResults.innerHTML = "";
    setResult(`<strong>Reading ${file.name}...</strong>`, "");
    try {
      decoded = await decodeGifFile(file);
      els.result.style.display = "none";
      originalFrames = decoded.frames.map((f) => Object.assign({}, f));
      els.originalInfo.textContent =
        `${file.name}: ${decoded.width}×${decoded.height}, ${decoded.frames.length} frames, ${formatBytes(file.size)}`;
      els.controls.style.display = "block";
      els.bulkToolbar.style.display = "flex";
      els.frameList.style.display = "flex";
      // Compression-focused view: thumbnails so you can spot a bad/redundant
      // frame to drop (fewer frames = smaller file), but no delay editing or
      // reordering -- neither affects file size, so they're not shown here.
      strip = renderFrameStrip(els.frameList, decoded.frames, { allowRemove: true, allowReorder: false, allowDelayEdit: false });
    } catch (err) {
      setResult(`<strong>Couldn't read that GIF.</strong> ${err.message ? err.message + " " : ""}Try a different file.`, "error");
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
    strip = renderFrameStrip(els.frameList, decoded.frames, { allowRemove: true, allowReorder: false, allowDelayEdit: false });
  });

  els.dedupeBtn.addEventListener("click", () => {
    if (!decoded || !decoded.frames.length) return;
    const before = decoded.frames.length;
    decoded.frames = bulkRemoveDuplicates(decoded.frames);
    originalFrames = decoded.frames.map((f) => Object.assign({}, f));
    strip = renderFrameStrip(els.frameList, decoded.frames, { allowRemove: true, allowReorder: false, allowDelayEdit: false });
    const removed = before - decoded.frames.length;
    setResult(
      removed > 0
        ? `<strong>Removed ${removed} duplicate frame${removed === 1 ? "" : "s"}.</strong> ${decoded.frames.length} left.`
        : `<strong>No duplicate frames found.</strong>`,
      "ok"
    );
  });

  els.reduceColorsCheck.addEventListener("change", () => {
    els.colorsInput.disabled = !els.reduceColorsCheck.checked;
  });

  /** Stage 1: apply frame edits (removed frames, scaling) via our own
   * canvas pipeline. Shared by the single-compress and 3-preset flows so
   * both start from the same freshly re-encoded base. */
  async function buildStage1(onProgress) {
    const scale = Math.min(100, Math.max(10, Number(els.scaleInput.value) || 100)) / 100;
    const outW = Math.max(1, Math.round(decoded.width * scale));
    const outH = Math.max(1, Math.round(decoded.height * scale));
    const frames = decoded.frames.map((f) => {
      const canvas = document.createElement("canvas");
      canvas.width = outW;
      canvas.height = outH;
      const src = frameSourceEl(f);
      canvas.getContext("2d").drawImage(src, 0, 0, outW, outH);
      return { canvas, delay: f.delay };
    });
    const blob = await encodeGif(frames, { width: outW, height: outH, quality: 10, onProgress });
    return { blob, outW, outH };
  }

  els.compressBtn.addEventListener("click", async () => {
    if (!decoded || !decoded.frames.length || busy) return;
    busy = true;
    const lossy = Math.max(0, Math.min(200, Number(els.lossyInput.value) || 0));
    const colors = els.reduceColorsCheck.checked ? Math.max(2, Math.min(256, Number(els.colorsInput.value) || 128)) : 0;

    els.compressBtn.disabled = true;
    els.presetsBtn.disabled = true;
    els.compressBtn.textContent = "Re-encoding...";
    els.result.style.display = "none";
    els.presetResults.style.display = "none";

    try {
      const { blob: stage1Blob } = await buildStage1((f) => {
        els.compressBtn.textContent = `Re-encoding... ${Math.round(f * 100)}%`;
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
      setResult(`<strong>Couldn't compress that GIF.</strong> ${err.message ? err.message + " " : ""}Try a lower scale or lossy level.`, "error");
    } finally {
      busy = false;
      els.compressBtn.disabled = false;
      els.presetsBtn.disabled = false;
      els.compressBtn.textContent = "Compress GIF";
    }
  });

  const PRESETS = [
    { label: "Light", lossy: 15 },
    { label: "Balanced", lossy: 50 },
    { label: "Aggressive", lossy: 120 },
  ];

  els.presetsBtn.addEventListener("click", async () => {
    if (!decoded || !decoded.frames.length || busy) return;
    busy = true;
    const colors = els.reduceColorsCheck.checked ? Math.max(2, Math.min(256, Number(els.colorsInput.value) || 128)) : 0;

    els.compressBtn.disabled = true;
    els.presetsBtn.disabled = true;
    els.presetsBtn.textContent = "Re-encoding...";
    els.result.style.display = "none";
    els.presetResults.style.display = "none";
    els.presetResults.innerHTML = "";

    try {
      const { blob: stage1Blob } = await buildStage1((f) => {
        els.presetsBtn.textContent = `Re-encoding... ${Math.round(f * 100)}%`;
      });

      els.presetsBtn.textContent = "Compressing...";
      for (const preset of PRESETS) {
        const blob = await compressWithGifsicle(stage1Blob, { lossy: preset.lossy, colors, optimize: true });
        const url = URL.createObjectURL(blob);
        const card = document.createElement("div");
        card.className = "panel";
        card.style.cssText = "padding:10px; width:150px; text-align:center;";
        card.innerHTML =
          `<img src="${url}" alt="${preset.label} preview" style="width:100%; border-radius:6px; display:block;" />` +
          `<strong style="display:block; margin-top:6px; font-size:13px;">${preset.label}</strong>` +
          `<span class="note" style="font-size:12px; display:block;">lossy ${preset.lossy} &middot; ${formatBytes(blob.size)}</span>` +
          `<button type="button" style="width:100%; font-size:12px; padding:4px; margin-top:6px;">Download</button>`;
        card.querySelector("button").addEventListener("click", () => downloadBlob(blob, `compressed-${preset.label.toLowerCase()}.gif`));
        els.presetResults.appendChild(card);
      }
      els.presetResults.style.display = "flex";
      els.presetResults.scrollIntoView({ behavior: "smooth", block: "center" });
    } catch (err) {
      setResult(`<strong>Couldn't generate preview compressions.</strong> ${err.message ? err.message + " " : ""}Try again.`, "error");
    } finally {
      busy = false;
      els.compressBtn.disabled = false;
      els.presetsBtn.disabled = false;
      els.presetsBtn.textContent = "Compare 3 quick size options";
    }
  });
})();
