(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    originalInfo: document.getElementById("originalInfo"),
    previewGrid: document.getElementById("previewGrid"),
    generateBtn: document.getElementById("generateBtn"),
    result: document.getElementById("result"),
  };

  let currentImg = null;

  const SIZES = [16, 32, 48, 180, 192, 512];

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

  function resizeToCanvas(img, size) {
    const canvas = document.createElement("canvas");
    canvas.width = size;
    canvas.height = size;
    const ctx = canvas.getContext("2d");
    // Cover-fit: crop to a centered square first so non-square uploads
    // don't come out stretched or with distracting empty padding.
    const srcSize = Math.min(img.width, img.height);
    const sx = (img.width - srcSize) / 2;
    const sy = (img.height - srcSize) / 2;
    ctx.drawImage(img, sx, sy, srcSize, srcSize, 0, 0, size, size);
    return canvas;
  }

  function canvasToBlob(canvas, mime) {
    return new Promise((resolve) => canvas.toBlob(resolve, mime));
  }

  async function handleFile(file) {
    if (!file || !file.type.startsWith("image/")) {
      setResult("<strong>That's not an image.</strong> Choose a JPG, PNG, or WebP file.", "error");
      return;
    }
    const { img, url } = await loadImageFile(file);
    currentImg = img;
    URL.revokeObjectURL(url); // only used to decode; canvas draws below don't need it alive
    els.originalInfo.textContent = `${file.name}, ${currentImg.width}×${currentImg.height}`;
    els.originalInfo.style.display = "block";
    els.generateBtn.disabled = false;
    els.result.style.display = "none";

    els.previewGrid.innerHTML = "";
    for (const size of SIZES) {
      const canvas = resizeToCanvas(currentImg, Math.min(size, 96)); // cap preview render size for crisp small icons
      const wrap = document.createElement("div");
      wrap.className = "favicon-preview-item";
      const img = document.createElement("img");
      img.src = canvas.toDataURL("image/png");
      img.style.width = Math.min(size, 64) + "px";
      img.style.height = Math.min(size, 64) + "px";
      const label = document.createElement("span");
      label.textContent = `${size}×${size}`;
      wrap.appendChild(img);
      wrap.appendChild(label);
      els.previewGrid.appendChild(wrap);
    }
    els.previewGrid.style.display = "flex";
  }

  els.drop.addEventListener("click", () => els.fileInput.click());
  els.fileInput.addEventListener("change", (e) => handleFile(e.target.files[0]));
  wireDragDrop(els.drop, (e) => {
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  });

  els.generateBtn.addEventListener("click", async () => {
    if (!currentImg) return;
    els.generateBtn.disabled = true;
    els.generateBtn.textContent = "Generating...";
    try {
      const entries = [];
      for (const size of SIZES) {
        const canvas = resizeToCanvas(currentImg, size);
        const blob = await canvasToBlob(canvas, "image/png");
        const bytes = new Uint8Array(await blob.arrayBuffer());
        const name = size === 180 ? "apple-touch-icon.png" : `favicon-${size}x${size}.png`;
        entries.push({ name, bytes });
      }

      // Basic favicon.ico: browsers today happily accept a PNG-in-.ico
      // container for the single most common size, but rather than hand-roll
      // ICO container bytes (a real can of worms), ship the well-supported
      // modern approach instead: PNG favicons plus a snippet using them,
      // covering everything from browser tabs to iOS home screen icons.
      const html = `<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="48x48" href="/favicon-48x48.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="192x192" href="/favicon-192x192.png">
<link rel="icon" type="image/png" sizes="512x512" href="/favicon-512x512.png">
`;
      entries.push({ name: "favicon-html-snippet.txt", bytes: new TextEncoder().encode(html) });

      const zipBytes = createZip(entries);
      const zipBlob = new Blob([zipBytes], { type: "application/zip" });
      downloadBlob(zipBlob, "favicons.zip");

      setResult(
        `<strong>Generated ${SIZES.length} favicon sizes.</strong> Downloaded as favicons.zip, including an HTML snippet with the &lt;link&gt; tags to paste into your site's &lt;head&gt;.`,
        "ok"
      );
      celebrateSuccess(els.generateBtn, els.result);
    } catch (err) {
      setResult(`<strong>Couldn't generate favicons.</strong> ${err.message || "Try a different image."}`, "error");
    } finally {
      els.generateBtn.disabled = false;
      els.generateBtn.textContent = "Generate & download favicons";
    }
  });
})();
