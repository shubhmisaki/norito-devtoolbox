(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    controls: document.getElementById("controls"),
    originalInfo: document.getElementById("originalInfo"),
    mode: document.getElementById("mode"),
    widthInput: document.getElementById("widthInput"),
    heightInput: document.getElementById("heightInput"),
    exactFields: document.getElementById("exactFields"),
    percentFields: document.getElementById("percentFields"),
    percentInput: document.getElementById("percentInput"),
    lockRatio: document.getElementById("lockRatio"),
    lockRatioRow: document.getElementById("lockRatioRow"),
    fitModeField: document.getElementById("fitModeField"),
    fitMode: document.getElementById("fitMode"),
    cropFields: document.getElementById("cropFields"),
    cropPreviewWrap: document.getElementById("cropPreviewWrap"),
    cropPreviewImg: document.getElementById("cropPreviewImg"),
    cropRect: document.getElementById("cropRect"),
    cropX: document.getElementById("cropX"),
    cropY: document.getElementById("cropY"),
    cropW: document.getElementById("cropW"),
    cropH: document.getElementById("cropH"),
    resetCropBtn: document.getElementById("resetCropBtn"),
    resizeBtn: document.getElementById("resizeBtn"),
    cancelBtn: document.getElementById("cancelBtn"),
    frameList: document.getElementById("frameList"),
    result: document.getElementById("result"),
    preview: document.getElementById("preview"),
  };

  let currentFile = null;
  let decoded = null;
  let aspectRatio = 1;
  let syncing = false;
  let strip = null;
  let busy = false; // true while resizing, so a mid-flight file swap can't pull the rug out
  let cropRectPx = null; // { x, y, w, h } in actual GIF pixel coordinates
  let activeGif = null;

  els.cancelBtn.addEventListener("click", () => {
    if (activeGif) activeGif.abort();
    els.cancelBtn.disabled = true;
    els.cancelBtn.textContent = "Cancelling...";
  });

  function setResult(html, state) {
    els.result.innerHTML = html;
    els.result.style.display = "block";
    els.result.className = "result-box " + (state || "");
  }

  async function handleFile(file) {
    if (busy) {
      setResult("<strong>Still resizing the previous GIF.</strong> Wait for it to finish first.", "error");
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
    els.frameList.style.display = "none";
    els.frameList.innerHTML = "";
    setResult(`<strong>Reading ${file.name}...</strong>`, "");
    try {
      decoded = await decodeGifFile(file);
      els.result.style.display = "none";
      aspectRatio = decoded.width / decoded.height;
      els.originalInfo.textContent =
        `${file.name}: ${decoded.width}×${decoded.height}, ${decoded.frames.length} frames, ${formatBytes(file.size)}`;
      syncing = true;
      els.widthInput.value = decoded.width;
      els.heightInput.value = decoded.height;
      syncing = false;
      els.controls.style.display = "block";
      els.frameList.style.display = "flex";
      // Preview only: resizing doesn't touch which frames exist, their
      // order, or their timing, so none of those controls are shown here.
      strip = renderFrameStrip(els.frameList, decoded.frames, { allowRemove: false, allowReorder: false, allowDelayEdit: false });
      initCrop();
      updateModeUI();
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

  function updateModeUI() {
    const mode = els.mode.value;
    els.exactFields.style.display = mode === "exact" ? "flex" : "none";
    els.percentFields.style.display = mode === "percent" ? "block" : "none";
    els.cropFields.style.display = mode === "crop" ? "block" : "none";
    els.lockRatioRow.style.display = mode === "crop" ? "none" : "flex";
    els.fitModeField.style.display = mode === "exact" && !els.lockRatio.checked ? "block" : "none";
    if (mode === "crop" && decoded) drawCropOverlay();
  }
  els.mode.addEventListener("change", updateModeUI);
  els.lockRatio.addEventListener("change", updateModeUI);
  updateModeUI();

  /* --------------------------------------------------------------------
     Crop mode: drag a rectangle on a preview of frame 1, or type exact
     pixel coordinates. cropRectPx is always in real GIF pixel units;
     the overlay div is positioned with percentages so it stays aligned
     with the (responsively-scaled) preview image without recomputing a
     px scale factor on resize.
     ------------------------------------------------------------------ */

  function initCrop() {
    const frame0 = decoded.frames[0];
    const src = frameSourceEl(frame0);
    const canvas = document.createElement("canvas");
    canvas.width = decoded.width;
    canvas.height = decoded.height;
    canvas.getContext("2d").drawImage(src, 0, 0, decoded.width, decoded.height);
    els.cropPreviewImg.src = canvas.toDataURL("image/png");
    cropRectPx = { x: 0, y: 0, w: decoded.width, h: decoded.height };
    syncCropInputs();
  }

  function syncCropInputs() {
    if (!cropRectPx) return;
    els.cropX.value = Math.round(cropRectPx.x);
    els.cropY.value = Math.round(cropRectPx.y);
    els.cropW.value = Math.round(cropRectPx.w);
    els.cropH.value = Math.round(cropRectPx.h);
    [els.cropX, els.cropY, els.cropW, els.cropH].forEach((el) => { el.max = decoded ? Math.max(decoded.width, decoded.height) : ""; });
  }

  function drawCropOverlay() {
    if (!cropRectPx || !decoded) return;
    els.cropRect.style.left = `${(cropRectPx.x / decoded.width) * 100}%`;
    els.cropRect.style.top = `${(cropRectPx.y / decoded.height) * 100}%`;
    els.cropRect.style.width = `${(cropRectPx.w / decoded.width) * 100}%`;
    els.cropRect.style.height = `${(cropRectPx.h / decoded.height) * 100}%`;
  }

  function clampCropRect() {
    cropRectPx.w = Math.max(1, Math.min(cropRectPx.w, decoded.width));
    cropRectPx.h = Math.max(1, Math.min(cropRectPx.h, decoded.height));
    cropRectPx.x = Math.max(0, Math.min(cropRectPx.x, decoded.width - cropRectPx.w));
    cropRectPx.y = Math.max(0, Math.min(cropRectPx.y, decoded.height - cropRectPx.h));
  }

  els.cropPreviewWrap.addEventListener("pointerdown", (e) => {
    if (!decoded || els.mode.value !== "crop") return;
    e.preventDefault();
    const wrap = els.cropPreviewWrap;
    wrap.setPointerCapture(e.pointerId);
    const rect = wrap.getBoundingClientRect();
    const startXFrac = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
    const startYFrac = Math.max(0, Math.min(1, (e.clientY - rect.top) / rect.height));
    const startX = startXFrac * decoded.width;
    const startY = startYFrac * decoded.height;

    const move = (ev) => {
      const xFrac = Math.max(0, Math.min(1, (ev.clientX - rect.left) / rect.width));
      const yFrac = Math.max(0, Math.min(1, (ev.clientY - rect.top) / rect.height));
      const curX = xFrac * decoded.width;
      const curY = yFrac * decoded.height;
      cropRectPx = {
        x: Math.min(startX, curX),
        y: Math.min(startY, curY),
        w: Math.max(1, Math.abs(curX - startX)),
        h: Math.max(1, Math.abs(curY - startY)),
      };
      clampCropRect();
      drawCropOverlay();
    };
    const up = () => {
      wrap.removeEventListener("pointermove", move);
      wrap.removeEventListener("pointerup", up);
      syncCropInputs();
    };
    wrap.addEventListener("pointermove", move);
    wrap.addEventListener("pointerup", up);
  });

  [els.cropX, els.cropY, els.cropW, els.cropH].forEach((el) => {
    el.addEventListener("change", () => {
      if (!decoded || !cropRectPx) return;
      cropRectPx = {
        x: Math.max(0, Number(els.cropX.value) || 0),
        y: Math.max(0, Number(els.cropY.value) || 0),
        w: Math.max(1, Number(els.cropW.value) || 1),
        h: Math.max(1, Number(els.cropH.value) || 1),
      };
      clampCropRect();
      syncCropInputs();
      drawCropOverlay();
    });
  });

  els.resetCropBtn.addEventListener("click", () => {
    if (!decoded) return;
    cropRectPx = { x: 0, y: 0, w: decoded.width, h: decoded.height };
    syncCropInputs();
    drawCropOverlay();
  });

  window.addEventListener("resize", () => {
    if (decoded && els.mode.value === "crop") drawCropOverlay();
  });

  els.widthInput.addEventListener("input", () => {
    if (syncing || !els.lockRatio.checked || !decoded) return;
    syncing = true;
    els.heightInput.value = Math.max(1, Math.round(Number(els.widthInput.value) / aspectRatio));
    syncing = false;
  });
  els.heightInput.addEventListener("input", () => {
    if (syncing || !els.lockRatio.checked || !decoded) return;
    syncing = true;
    els.widthInput.value = Math.max(1, Math.round(Number(els.heightInput.value) * aspectRatio));
    syncing = false;
  });

  function targetDims() {
    if (els.mode.value === "exact") {
      return {
        w: Math.max(1, Math.round(Number(els.widthInput.value) || 0)),
        h: Math.max(1, Math.round(Number(els.heightInput.value) || 0)),
      };
    }
    const pct = Math.max(1, Number(els.percentInput.value) || 100) / 100;
    return {
      w: Math.max(1, Math.round(decoded.width * pct)),
      h: Math.max(1, Math.round(decoded.height * pct)),
    };
  }

  /** Draw one frame's source into a w×h canvas per the chosen fit mode:
   * stretch (distort to fill), cover (crop to fill, no distortion), or
   * contain (pad the extra space with transparency, no distortion, no
   * cropping). */
  function drawFitted(ctx, src, w, h, fit) {
    if (fit === "stretch") {
      ctx.drawImage(src, 0, 0, w, h);
      return;
    }
    const srcRatio = decoded.width / decoded.height;
    const dstRatio = w / h;
    if (fit === "cover") {
      let sw = decoded.width, sh = decoded.height, sx = 0, sy = 0;
      if (srcRatio > dstRatio) { sw = decoded.height * dstRatio; sx = (decoded.width - sw) / 2; }
      else { sh = decoded.width / dstRatio; sy = (decoded.height - sh) / 2; }
      ctx.drawImage(src, sx, sy, sw, sh, 0, 0, w, h);
    } else { // contain
      let dw = w, dh = h;
      if (srcRatio > dstRatio) dh = w / srcRatio;
      else dw = h * srcRatio;
      ctx.drawImage(src, 0, 0, decoded.width, decoded.height, (w - dw) / 2, (h - dh) / 2, dw, dh);
    }
  }

  els.resizeBtn.addEventListener("click", async () => {
    if (!decoded || busy) return;
    const mode = els.mode.value;
    let w, h, frames;

    if (mode === "crop") {
      if (!cropRectPx || cropRectPx.w < 1 || cropRectPx.h < 1) {
        setResult("<strong>Select a crop area first.</strong>", "error");
        return;
      }
      w = Math.round(cropRectPx.w);
      h = Math.round(cropRectPx.h);
    } else {
      ({ w, h } = targetDims());
      if (!w || !h || w > 4000 || h > 4000) {
        setResult("<strong>Enter valid dimensions.</strong> Width and height must be between 1 and 4000 pixels.", "error");
        return;
      }
    }

    busy = true;
    els.resizeBtn.disabled = true;
    els.resizeBtn.textContent = mode === "crop" ? "Cropping..." : "Resizing...";
    els.cancelBtn.style.display = "inline-block";
    els.cancelBtn.disabled = false;
    els.cancelBtn.textContent = "Cancel";
    els.result.style.display = "none";

    try {
      const fit = mode === "exact" && !els.lockRatio.checked ? els.fitMode.value : "stretch";
      frames = decoded.frames.map((f) => {
        const canvas = document.createElement("canvas");
        canvas.width = w;
        canvas.height = h;
        const ctx = canvas.getContext("2d");
        const src = frameSourceEl(f);
        if (mode === "crop") {
          ctx.drawImage(src, cropRectPx.x, cropRectPx.y, cropRectPx.w, cropRectPx.h, 0, 0, w, h);
        } else {
          drawFitted(ctx, src, w, h, fit);
        }
        return { canvas, delay: f.delay };
      });

      const blob = await encodeGif(frames, {
        width: w,
        height: h,
        quality: 10,
        onStart: (gif) => { activeGif = gif; },
        onProgress: (f) => { els.resizeBtn.textContent = `${mode === "crop" ? "Cropping" : "Resizing"}... ${Math.round(f * 100)}%`; },
      });

      const url = URL.createObjectURL(blob);
      els.preview.src = url;
      els.preview.style.display = "block";

      setResult(
        `<strong>${mode === "crop" ? "Cropped" : "Resized"} to ${w}×${h}.</strong> ${formatBytes(blob.size)}.<br><br>` +
        `<button id="dlBtn">Download ${mode === "crop" ? "cropped" : "resized"}.gif</button>`,
        "ok"
      );
      document.getElementById("dlBtn").addEventListener("click", () => downloadBlob(blob, mode === "crop" ? "cropped.gif" : "resized.gif"));
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
      if (typeof celebrateSuccess === "function") celebrateSuccess(els.resizeBtn, els.result);
    } catch (err) {
      if (err && err.cancelled) {
        setResult("<strong>Cancelled.</strong> No file was created.", "");
      } else {
        setResult(`<strong>Couldn't ${mode === "crop" ? "crop" : "resize"} that GIF.</strong> ${err.message ? err.message + " " : ""}Try different values.`, "error");
      }
    } finally {
      busy = false;
      activeGif = null;
      els.resizeBtn.disabled = false;
      els.resizeBtn.textContent = "Resize GIF";
      els.cancelBtn.style.display = "none";
    }
  });
})();
