(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    originalInfo: document.getElementById("originalInfo"),
    frameGrid: document.getElementById("frameGrid"),
    zipBtn: document.getElementById("zipBtn"),
    result: document.getElementById("result"),
  };

  let frameBlobs = []; // [{ blob, name }]

  function setResult(html, state) {
    els.result.innerHTML = html;
    els.result.style.display = "block";
    els.result.className = "result-box " + (state || "");
  }

  async function canvasToPngBlob(canvas) {
    return new Promise((resolve) => canvas.toBlob(resolve, "image/png"));
  }

  async function handleFile(file) {
    if (!file || !/image\/gif/.test(file.type)) {
      setResult("<strong>That's not a GIF.</strong> Choose a .gif file.", "error");
      return;
    }
    els.result.style.display = "none";
    els.frameGrid.style.display = "none";
    els.frameGrid.innerHTML = "";
    els.zipBtn.style.display = "none";
    els.originalInfo.style.display = "none";
    frameBlobs = [];

    try {
      const decoded = await decodeGifFile(file);
      els.originalInfo.textContent =
        `${file.name}: ${decoded.width}×${decoded.height}, ${decoded.frames.length} frames, ${formatBytes(file.size)}`;
      els.originalInfo.style.display = "block";

      const digits = String(decoded.frames.length).length;
      for (let i = 0; i < decoded.frames.length; i++) {
        const canvas = imageDataToCanvas(decoded.frames[i].imageData);
        const blob = await canvasToPngBlob(canvas);
        const name = `frame-${String(i + 1).padStart(digits, "0")}.png`;
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
