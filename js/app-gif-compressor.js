(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    controls: document.getElementById("controls"),
    originalInfo: document.getElementById("originalInfo"),
    scaleInput: document.getElementById("scaleInput"),
    skipSelect: document.getElementById("skipSelect"),
    qualitySelect: document.getElementById("qualitySelect"),
    compressBtn: document.getElementById("compressBtn"),
    result: document.getElementById("result"),
    preview: document.getElementById("preview"),
  };

  let currentFile = null;
  let decoded = null; // { width, height, frames }

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
    try {
      decoded = await decodeGifFile(file);
      els.originalInfo.textContent =
        `${file.name}: ${decoded.width}×${decoded.height}, ${decoded.frames.length} frames, ${formatBytes(file.size)}`;
      els.controls.style.display = "block";
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

  els.compressBtn.addEventListener("click", async () => {
    if (!decoded) return;
    const scale = Math.min(100, Math.max(10, Number(els.scaleInput.value) || 100)) / 100;
    const skip = Number(els.skipSelect.value) || 1;
    const quality = Number(els.qualitySelect.value) || 16;

    const outW = Math.max(1, Math.round(decoded.width * scale));
    const outH = Math.max(1, Math.round(decoded.height * scale));

    els.compressBtn.disabled = true;
    els.compressBtn.textContent = "Compressing...";
    els.result.style.display = "none";

    try {
      const keptFrames = decoded.frames.filter((_, i) => i % skip === 0);
      const frames = keptFrames.map((f) => {
        const canvas = document.createElement("canvas");
        canvas.width = outW;
        canvas.height = outH;
        const src = imageDataToCanvas(f.imageData);
        canvas.getContext("2d").drawImage(src, 0, 0, outW, outH);
        return { canvas, delay: f.delay * skip };
      });

      const blob = await encodeGif(frames, {
        width: outW,
        height: outH,
        quality,
        onProgress: (f) => { els.compressBtn.textContent = `Compressing... ${Math.round(f * 100)}%`; },
      });

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
      setResult(`<strong>Couldn't compress that GIF.</strong> ${err.message || "Try a lower scale."}`, "error");
    } finally {
      els.compressBtn.disabled = false;
      els.compressBtn.textContent = "Compress GIF";
    }
  });
})();
