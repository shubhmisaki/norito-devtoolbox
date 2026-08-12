(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    controls: document.getElementById("controls"),
    originalInfo: document.getElementById("originalInfo"),
    textInput: document.getElementById("textInput"),
    positionSelect: document.getElementById("positionSelect"),
    sizeInput: document.getElementById("sizeInput"),
    colorInput: document.getElementById("colorInput"),
    strokeCheck: document.getElementById("strokeCheck"),
    applyBtn: document.getElementById("applyBtn"),
    result: document.getElementById("result"),
    preview: document.getElementById("preview"),
  };

  let currentFile = null;
  let decoded = null;

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

  function drawCaption(ctx, width, height, lines, opts) {
    ctx.font = `bold ${opts.size}px sans-serif`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    const lineHeight = opts.size * 1.25;
    const blockHeight = lines.length * lineHeight;

    let startY;
    if (opts.position === "top") startY = opts.size * 0.9;
    else if (opts.position === "bottom") startY = height - blockHeight + lineHeight * 0.5 - opts.size * 0.15;
    else startY = height / 2 - blockHeight / 2 + lineHeight / 2;

    lines.forEach((line, i) => {
      const y = startY + i * lineHeight;
      if (opts.stroke) {
        ctx.lineWidth = Math.max(2, opts.size / 10);
        ctx.strokeStyle = "#000000";
        ctx.strokeText(line, width / 2, y);
      }
      ctx.fillStyle = opts.color;
      ctx.fillText(line, width / 2, y);
    });
  }

  els.applyBtn.addEventListener("click", async () => {
    if (!decoded) return;
    const text = els.textInput.value.trim();
    if (!text) {
      setResult("<strong>Enter some caption text first.</strong>", "error");
      return;
    }
    const lines = text.split("\n").filter((l) => l.length);
    const opts = {
      position: els.positionSelect.value,
      size: Math.max(8, Number(els.sizeInput.value) || 28),
      color: els.colorInput.value,
      stroke: els.strokeCheck.checked,
    };

    els.applyBtn.disabled = true;
    els.applyBtn.textContent = "Rendering...";
    els.result.style.display = "none";

    try {
      const { width, height } = decoded;
      const frames = decoded.frames.map((f) => {
        const canvas = document.createElement("canvas");
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext("2d");
        ctx.putImageData(f.imageData, 0, 0);
        drawCaption(ctx, width, height, lines, opts);
        return { canvas, delay: f.delay };
      });

      const blob = await encodeGif(frames, {
        width,
        height,
        quality: 10,
        onProgress: (f) => { els.applyBtn.textContent = `Rendering... ${Math.round(f * 100)}%`; },
      });

      const url = URL.createObjectURL(blob);
      els.preview.src = url;
      els.preview.style.display = "block";

      setResult(
        `<strong>Caption added.</strong> ${formatBytes(blob.size)}.<br><br>` +
        `<button id="dlBtn">Download captioned.gif</button>`,
        "ok"
      );
      document.getElementById("dlBtn").addEventListener("click", () => downloadBlob(blob, "captioned.gif"));
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
      if (typeof celebrateSuccess === "function") celebrateSuccess(els.applyBtn, els.result);
    } catch (err) {
      setResult(`<strong>Couldn't add that caption.</strong> ${err.message || "Try again."}`, "error");
    } finally {
      els.applyBtn.disabled = false;
      els.applyBtn.textContent = "Add Text";
    }
  });
})();
