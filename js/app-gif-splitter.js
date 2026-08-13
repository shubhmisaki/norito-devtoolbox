(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    originalInfo: document.getElementById("originalInfo"),
    exportControls: document.getElementById("exportControls"),
    formatSelect: document.getElementById("formatSelect"),
    qualityRow: document.getElementById("qualityRow"),
    qualityInput: document.getElementById("qualityInput"),
    frameGrid: document.getElementById("frameGrid"),
    zipBtn: document.getElementById("zipBtn"),
    spriteToolbar: document.getElementById("spriteToolbar"),
    spriteCols: document.getElementById("spriteCols"),
    spriteBtn: document.getElementById("spriteBtn"),
    result: document.getElementById("result"),
  };

  let decoded = null; // { width, height, frames } from decodeGifFile, kept so re-exporting in a new format doesn't need to re-decode
  let frameBlobs = []; // [{ blob, name }]

  function setResult(html, state) {
    els.result.innerHTML = html;
    els.result.style.display = "block";
    els.result.className = "result-box " + (state || "");
  }

  function mimeFor(format) {
    return format === "jpeg" ? "image/jpeg" : format === "webp" ? "image/webp" : "image/png";
  }
  function extFor(format) {
    return format === "jpeg" ? "jpg" : format === "webp" ? "webp" : "png";
  }

  async function canvasToBlob(canvas, format, quality) {
    return new Promise((resolve) => canvas.toBlob(resolve, mimeFor(format), format === "png" ? undefined : quality));
  }

  async function buildFrameExports() {
    if (!decoded) return;
    const format = els.formatSelect.value;
    const quality = Math.max(1, Math.min(100, Number(els.qualityInput.value) || 90)) / 100;
    const ext = extFor(format);

    els.frameGrid.innerHTML = "";
    frameBlobs = [];
    const digits = String(decoded.frames.length).length;
    for (let i = 0; i < decoded.frames.length; i++) {
      const canvas = imageDataToCanvas(decoded.frames[i].imageData);
      const blob = await canvasToBlob(canvas, format, quality);
      const name = `frame-${String(i + 1).padStart(digits, "0")}.${ext}`;
      frameBlobs.push({ blob, name });

      const thumbUrl = URL.createObjectURL(blob);
      const cell = document.createElement("div");
      cell.className = "panel";
      cell.style.padding = "8px";
      cell.style.textAlign = "center";
      cell.innerHTML = `
        <img src="${thumbUrl}" alt="Frame ${i + 1}" style="width:100%; border-radius:6px; display:block;" />
        <span class="note" style="font-size:11px; display:block; margin:4px 0;">${name}</span>
        <button type="button" data-i="${i}" style="width:100%; font-size:12px; padding:4px;">Download</button>
      `;
      cell.querySelector("button").addEventListener("click", () => downloadBlob(blob, name));
      els.frameGrid.appendChild(cell);
    }
    els.frameGrid.style.display = "grid";
    els.zipBtn.style.display = "inline-block";
  }

  els.formatSelect.addEventListener("change", () => {
    els.qualityRow.style.display = els.formatSelect.value === "png" ? "none" : "block";
    buildFrameExports();
  });
  els.qualityInput.addEventListener("change", () => buildFrameExports());

  async function handleFile(file) {
    if (!file || !/image\/gif/.test(file.type)) {
      setResult("<strong>That's not a GIF.</strong> Choose a .gif file.", "error");
      return;
    }
    els.result.style.display = "none";
    els.exportControls.style.display = "none";
    els.frameGrid.style.display = "none";
    els.frameGrid.innerHTML = "";
    els.zipBtn.style.display = "none";
    els.spriteToolbar.style.display = "none";
    els.originalInfo.style.display = "none";
    decoded = null;
    frameBlobs = [];
    setResult(`<strong>Reading ${file.name}...</strong>`, "");

    try {
      decoded = await decodeGifFile(file);
      els.result.style.display = "none";
      els.originalInfo.textContent =
        `${file.name}: ${decoded.width}×${decoded.height}, ${decoded.frames.length} frames, ${formatBytes(file.size)}`;
      els.originalInfo.style.display = "block";

      els.exportControls.style.display = "flex";
      await buildFrameExports();

      els.spriteCols.value = Math.ceil(Math.sqrt(decoded.frames.length));
      els.spriteCols.max = decoded.frames.length;
      els.spriteToolbar.style.display = "flex";
    } catch (err) {
      setResult(`<strong>Couldn't read that GIF.</strong> ${err.message ? err.message + " " : ""}Try a different file.`, "error");
    }
  }

  els.spriteBtn.addEventListener("click", async () => {
    if (!decoded || !decoded.frames.length) return;
    els.spriteBtn.disabled = true;
    els.spriteBtn.textContent = "Building...";
    try {
      const cols = Math.max(1, Math.min(decoded.frames.length, Math.round(Number(els.spriteCols.value)) || Math.ceil(Math.sqrt(decoded.frames.length))));
      const rows = Math.ceil(decoded.frames.length / cols);
      const fw = decoded.width, fh = decoded.height;
      const sheet = document.createElement("canvas");
      sheet.width = fw * cols;
      sheet.height = fh * rows;
      const ctx = sheet.getContext("2d");
      decoded.frames.forEach((f, i) => {
        const col = i % cols, row = Math.floor(i / cols);
        ctx.drawImage(imageDataToCanvas(f.imageData), col * fw, row * fh);
      });
      const blob = await new Promise((resolve) => sheet.toBlob(resolve, "image/png"));
      downloadBlob(blob, "sprite-sheet.png");
      setResult(`<strong>Downloaded sprite sheet.</strong> ${cols}&times;${rows} grid, ${formatBytes(blob.size)}.`, "ok");
      if (typeof celebrateSuccess === "function") celebrateSuccess(els.spriteBtn, els.result, "Downloaded");
    } catch (err) {
      setResult(`<strong>Couldn't build the sprite sheet.</strong> ${err.message ? err.message + " " : ""}Try again.`, "error");
    } finally {
      els.spriteBtn.disabled = false;
      els.spriteBtn.textContent = "Download as sprite sheet";
    }
  });

  els.fileInput.addEventListener("change", () => handleFile(els.fileInput.files[0]));
  wireDragDrop(els.drop, (e) => handleFile(e.dataTransfer.files[0]));
  els.drop.addEventListener("click", (e) => {
    if (e.target === els.fileInput) return;
    els.fileInput.click();
  });

  els.zipBtn.addEventListener("click", async () => {
    if (!frameBlobs.length) return;
    els.zipBtn.disabled = true;
    els.zipBtn.textContent = "Zipping...";
    try {
      const entries = [];
      for (const fb of frameBlobs) {
        const bytes = new Uint8Array(await fb.blob.arrayBuffer());
        entries.push({ name: fb.name, bytes });
      }
      const zipBytes = createZip(entries);
      const blob = new Blob([zipBytes], { type: "application/zip" });
      downloadBlob(blob, "gif-frames.zip");
      setResult(`<strong>Downloaded ${frameBlobs.length} frames as gif-frames.zip.</strong>`, "ok");
      if (typeof celebrateSuccess === "function") celebrateSuccess(els.zipBtn, els.frameGrid, "Downloaded");
    } finally {
      els.zipBtn.disabled = false;
      els.zipBtn.textContent = "Download all as .zip";
    }
  });
})();
