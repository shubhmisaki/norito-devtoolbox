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
    resizeBtn: document.getElementById("resizeBtn"),
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
    try {
      decoded = await decodeGifFile(file);
      aspectRatio = decoded.width / decoded.height;
      els.originalInfo.textContent =
        `${file.name}: ${decoded.width}×${decoded.height}, ${decoded.frames.length} frames, ${formatBytes(file.size)}`;
      syncing = true;
      els.widthInput.value = decoded.width;
      els.heightInput.value = decoded.height;
      syncing = false;
      els.controls.style.display = "block";
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

  function updateModeUI() {
    const exact = els.mode.value === "exact";
    els.exactFields.style.display = exact ? "flex" : "block";
    els.percentFields.style.display = exact ? "none" : "block";
  }
  els.mode.addEventListener("change", updateModeUI);
  updateModeUI();

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

  els.resizeBtn.addEventListener("click", async () => {
    if (!decoded || busy) return;
    const { w, h } = targetDims();
    if (!w || !h || w > 4000 || h > 4000) {
      setResult("<strong>Enter valid dimensions.</strong> Width and height must be between 1 and 4000 pixels.", "error");
      return;
    }

    busy = true;
    els.resizeBtn.disabled = true;
    els.resizeBtn.textContent = "Resizing...";
    els.result.style.display = "none";

    try {
      const frames = decoded.frames.map((f) => {
        const canvas = document.createElement("canvas");
        canvas.width = w;
        canvas.height = h;
        const src = imageDataToCanvas(f.imageData);
        canvas.getContext("2d").drawImage(src, 0, 0, w, h);
        return { canvas, delay: f.delay };
      });

      const blob = await encodeGif(frames, {
        width: w,
        height: h,
        quality: 10,
        onProgress: (f) => { els.resizeBtn.textContent = `Resizing... ${Math.round(f * 100)}%`; },
      });

      const url = URL.createObjectURL(blob);
      els.preview.src = url;
      els.preview.style.display = "block";

      setResult(
        `<strong>Resized to ${w}×${h}.</strong> ${formatBytes(blob.size)}.<br><br>` +
        `<button id="dlBtn">Download resized.gif</button>`,
        "ok"
      );
      document.getElementById("dlBtn").addEventListener("click", () => downloadBlob(blob, "resized.gif"));
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
      if (typeof celebrateSuccess === "function") celebrateSuccess(els.resizeBtn, els.result);
    } catch (err) {
      setResult(`<strong>Couldn't resize that GIF.</strong> ${err.message || "Try different dimensions."}`, "error");
    } finally {
      busy = false;
      els.resizeBtn.disabled = false;
      els.resizeBtn.textContent = "Resize GIF";
    }
  });
})();
