(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    originalInfo: document.getElementById("originalInfo"),
    editorWrap: document.getElementById("editorWrap"),
    stageImg: document.getElementById("stageImg"),
    wmPreviewText: document.getElementById("wmPreviewText"),
    wmText: document.getElementById("wmText"),
    wmSize: document.getElementById("wmSize"),
    wmOpacity: document.getElementById("wmOpacity"),
    wmAngle: document.getElementById("wmAngle"),
    wmColor: document.getElementById("wmColor"),
    wmPosition: document.getElementById("wmPosition"),
    applyBtn: document.getElementById("applyBtn"),
    result: document.getElementById("result"),
    preview: document.getElementById("preview"),
    previewHint: document.getElementById("previewHint"),
  };

  let currentImg = null;
  let currentFile = null;
  let currentImgUrl = null; // tracked so we can revoke it once a new image replaces it on screen

  const ICONS = {
    ok: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="M22 4 12 14.01l-3-3"/></svg>',
    error: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>',
  };

  function setResult(html, state) {
    els.result.innerHTML = `<span class="r-icon">${ICONS[state] || ""}</span><span class="r-body">${html}</span>`;
    els.result.style.display = "flex";
    els.result.classList.remove("ok", "error");
    if (state) els.result.classList.add(state);
  }

  function positionStyles(pos) {
    // Returns CSS position props for the 9-point grid, used identically by
    // both the live DOM preview and (converted to canvas coords) the final render.
    const map = {
      "top-left": { top: "6%", left: "6%", transform: "" },
      "top-center": { top: "6%", left: "50%", transform: "translateX(-50%)" },
      "top-right": { top: "6%", right: "6%", transform: "" },
      "center-left": { top: "50%", left: "6%", transform: "translateY(-50%)" },
      center: { top: "50%", left: "50%", transform: "translate(-50%,-50%)" },
      "center-right": { top: "50%", right: "6%", transform: "translateY(-50%)" },
      "bottom-left": { bottom: "6%", left: "6%", transform: "" },
      "bottom-center": { bottom: "6%", left: "50%", transform: "translateX(-50%)" },
      "bottom-right": { bottom: "6%", right: "6%", transform: "" },
    };
    return map[pos] || map.center;
  }

  function updatePreview() {
    const text = els.wmText.value || "(empty)";
    const size = parseInt(els.wmSize.value, 10) || 32;
    const opacityPct = parseInt(els.wmOpacity.value, 10);
    const angle = parseInt(els.wmAngle.value, 10) || 0;
    const color = els.wmColor.value || "#ffffff";

    els.wmPreviewText.textContent = text;
    els.wmPreviewText.style.fontSize = size + "px";
    els.wmPreviewText.style.opacity = String((isNaN(opacityPct) ? 40 : opacityPct) / 100);
    els.wmPreviewText.style.color = color;

    const pos = positionStyles(els.wmPosition.value);
    ["top", "bottom", "left", "right"].forEach((k) => { els.wmPreviewText.style[k] = ""; });
    Object.keys(pos).forEach((k) => { if (k !== "transform") els.wmPreviewText.style[k] = pos[k]; });
    // rotate() is applied on top of the position transform, same convention
    // used on the PDF watermark tool's own live preview.
    els.wmPreviewText.style.transform = `${pos.transform} rotate(${angle}deg)`.trim();
  }
  [els.wmText, els.wmSize, els.wmOpacity, els.wmAngle, els.wmColor, els.wmPosition].forEach((el) => {
    el.addEventListener("input", updatePreview);
    el.addEventListener("change", updatePreview);
  });

  async function handleFile(file) {
    if (!file || !file.type.startsWith("image/")) {
      setResult("<strong>That's not an image.</strong> Choose a JPG, PNG, or WebP file.", "error");
      return;
    }
    currentFile = file;
    const { img, url } = await loadImageFile(file);
    if (currentImgUrl) URL.revokeObjectURL(currentImgUrl);
    currentImg = img;
    currentImgUrl = url;
    els.originalInfo.textContent = `${file.name}, ${currentImg.width}×${currentImg.height}, ${formatBytes(file.size)}`;
    els.originalInfo.style.display = "block";
    els.stageImg.src = currentImgUrl;
    els.editorWrap.style.display = "block";
    els.applyBtn.disabled = false;
    els.result.style.display = "none";
    updatePreview();
  }

  els.drop.addEventListener("click", () => els.fileInput.click());

  // Paste an image straight from the clipboard (screenshot tools, "Copy image", etc.)
  document.addEventListener("paste", (e) => {
    const clipItems = e.clipboardData && e.clipboardData.items;
    if (!clipItems) return;
    for (const item of clipItems) {
      if (item.type && item.type.startsWith("image/")) {
        const file = item.getAsFile();
        if (file) { handleFile(file); e.preventDefault(); }
        break;
      }
    }
  });
  els.fileInput.addEventListener("change", (e) => handleFile(e.target.files[0]));
  wireDragDrop(els.drop, (e) => {
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  });

  function canvasToBlob(canvas, mime, quality) {
    return new Promise((resolve) => canvas.toBlob(resolve, mime, quality));
  }
  function hexToRgb(hex) {
    const m = /^#?([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$/i.exec(hex || "");
    if (!m) return { r: 255, g: 255, b: 255 };
    return { r: parseInt(m[1], 16), g: parseInt(m[2], 16), b: parseInt(m[3], 16) };
  }

  // Maps a 9-point position + the preview's known display size to an anchor
  // point (in natural image pixels) plus the text-align semantics needed so
  // canvas fillText lands in the same relative spot the live DOM preview showed.
  function anchorFor(pos, w, h, margin) {
    const map = {
      "top-left": { x: margin, y: margin, align: "left", baseline: "top" },
      "top-center": { x: w / 2, y: margin, align: "center", baseline: "top" },
      "top-right": { x: w - margin, y: margin, align: "right", baseline: "top" },
      "center-left": { x: margin, y: h / 2, align: "left", baseline: "middle" },
      center: { x: w / 2, y: h / 2, align: "center", baseline: "middle" },
      "center-right": { x: w - margin, y: h / 2, align: "right", baseline: "middle" },
      "bottom-left": { x: margin, y: h - margin, align: "left", baseline: "bottom" },
      "bottom-center": { x: w / 2, y: h - margin, align: "center", baseline: "bottom" },
      "bottom-right": { x: w - margin, y: h - margin, align: "right", baseline: "bottom" },
    };
    return map[pos] || map.center;
  }

  els.applyBtn.addEventListener("click", async () => {
    if (!currentImg) return;
    const text = els.wmText.value.trim();
    if (!text) { setResult("<strong>Enter some watermark text first.</strong>", "error"); return; }

    const busyText = startBusyText(els.applyBtn, "Applying");
    try {
      const w = currentImg.width, h = currentImg.height;
      const canvas = document.createElement("canvas");
      canvas.width = w;
      canvas.height = h;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(currentImg, 0, 0);

      // Scale font size from the preview's on-screen size up to natural
      // image pixels, using the ratio between the stage's displayed width
      // and the image's real width, so "48px" looks the same proportionally
      // on a tiny preview and a huge original photo.
      const displayScale = w / els.stageImg.clientWidth;
      const size = Math.round((parseInt(els.wmSize.value, 10) || 32) * displayScale);
      const opacity = (parseInt(els.wmOpacity.value, 10) || 40) / 100;
      const angle = (parseInt(els.wmAngle.value, 10) || 0) * (Math.PI / 180);
      const { r, g, b } = hexToRgb(els.wmColor.value);
      const margin = Math.round(0.06 * Math.min(w, h));
      const anchor = anchorFor(els.wmPosition.value, w, h, margin);

      ctx.save();
      ctx.translate(anchor.x, anchor.y);
      ctx.rotate(angle);
      ctx.globalAlpha = opacity;
      ctx.fillStyle = `rgb(${r},${g},${b})`;
      ctx.font = `700 ${size}px Inter, Arial, sans-serif`;
      ctx.textAlign = anchor.align;
      ctx.textBaseline = anchor.baseline;
      ctx.fillText(text, 0, 0);
      ctx.restore();

      const isJpeg = currentFile.type === "image/jpeg";
      const mime = isJpeg ? "image/jpeg" : currentFile.type === "image/webp" ? "image/webp" : "image/png";
      const blob = await canvasToBlob(canvas, mime, mime === "image/png" ? undefined : 0.95);

      const url = URL.createObjectURL(blob);
      els.preview.src = url;
      els.preview.style.display = "block";
      if (els.previewHint) els.previewHint.style.display = "none";

      const ext = { "image/jpeg": "jpg", "image/png": "png", "image/webp": "webp" }[mime];
      const base = (currentFile.name || "image").replace(/\.[^.]+$/, "");
      const filename = `${base}-watermarked.${ext}`;

      setResult(
        `<strong>Watermark added.</strong> ${formatBytes(blob.size)}.<br><br>` +
        `<button id="dlBtn">Download ${filename}</button>`,
        "ok"
      );
      document.getElementById("dlBtn").addEventListener("click", () => downloadBlob(blob, filename));
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
      celebrateSuccess(els.applyBtn, els.result);
    } catch (err) {
      setResult(`<strong>Couldn't watermark that image.</strong> ${err.message || "Try a different file."}`, "error");
    } finally {
      busyText.done();
    }
  });
})();
