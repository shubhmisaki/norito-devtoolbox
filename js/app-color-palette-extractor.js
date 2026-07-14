(function () {
  const ICONS = {
    ok: '<svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>',
    error: '<svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m15 9-6 6M9 9l6 6"/></svg>',
  };

  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    countSelect: document.getElementById("colorCount"),
    grid: document.getElementById("paletteGrid"),
    result: document.getElementById("result"),
    preview: document.getElementById("previewImg"),
    previewWrap: document.getElementById("previewWrap"),
  };

  function setResult(kind, html) {
    if (!els.result) return;
    els.result.style.display = "flex";
    els.result.className = "result-box " + (kind || "");
    els.result.innerHTML = (kind === "ok" ? ICONS.ok : kind === "error" ? ICONS.error : "") + `<div class="r-body">${html}</div>`;
  }

  function loadImageFile(file) {
    return new Promise((resolve, reject) => {
      if (!file || !file.type.startsWith("image/")) {
        reject(new Error("Please choose an image file."));
        return;
      }
      const url = URL.createObjectURL(file);
      const img = new Image();
      img.onload = () => resolve({ img, url });
      img.onerror = () => reject(new Error("That image couldn't be read."));
      img.src = url;
    });
  }

  function rgbToHex(r, g, b) {
    return "#" + [r, g, b].map((v) => v.toString(16).padStart(2, "0")).join("");
  }

  // Simple, fast palette extraction: bucket every sampled pixel into a
  // coarse RGB grid (6 levels per channel = 216 buckets), tally which
  // buckets show up most, then average the real pixel colors that landed
  // in each of the top N buckets. Good enough for "what colors dominate
  // this image" without pulling in a k-means implementation.
  function extractPalette(img, count) {
    const canvas = document.createElement("canvas");
    const maxDim = 200; // downscale for speed, color distribution barely changes
    const scale = Math.min(1, maxDim / Math.max(img.naturalWidth, img.naturalHeight));
    canvas.width = Math.max(1, Math.round(img.naturalWidth * scale));
    canvas.height = Math.max(1, Math.round(img.naturalHeight * scale));
    const ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    const data = ctx.getImageData(0, 0, canvas.width, canvas.height).data;

    const buckets = new Map(); // key -> { count, rSum, gSum, bSum }
    const LEVELS = 6;
    const step = 256 / LEVELS;
    for (let i = 0; i < data.length; i += 4) {
      const a = data[i + 3];
      if (a < 128) continue; // skip mostly-transparent pixels
      const r = data[i], g = data[i + 1], b = data[i + 2];
      const key = `${Math.floor(r / step)}-${Math.floor(g / step)}-${Math.floor(b / step)}`;
      let bucket = buckets.get(key);
      if (!bucket) {
        bucket = { count: 0, rSum: 0, gSum: 0, bSum: 0 };
        buckets.set(key, bucket);
      }
      bucket.count++;
      bucket.rSum += r;
      bucket.gSum += g;
      bucket.bSum += b;
    }

    const sorted = Array.from(buckets.values()).sort((a, b) => b.count - a.count);
    const total = sorted.reduce((sum, b) => sum + b.count, 0) || 1;
    return sorted.slice(0, count).map((b) => {
      const r = Math.round(b.rSum / b.count);
      const g = Math.round(b.gSum / b.count);
      const bl = Math.round(b.bSum / b.count);
      return { hex: rgbToHex(r, g, bl), rgb: `rgb(${r}, ${g}, ${bl})`, pct: Math.round((b.count / total) * 100) };
    });
  }

  function renderPalette(colors) {
    els.grid.innerHTML = colors
      .map(
        (c) => `
      <button type="button" class="palette-swatch" data-hex="${c.hex}" title="Copy ${c.hex}">
        <div class="palette-swatch-color" style="background:${c.hex}"></div>
        <div class="palette-swatch-info">
          <strong>${c.hex.toUpperCase()}</strong>
          <span>${c.pct}% &middot; ${c.rgb}</span>
        </div>
      </button>`
      )
      .join("");
    els.grid.style.display = "grid";

    els.grid.querySelectorAll(".palette-swatch").forEach((btn) => {
      btn.addEventListener("click", async () => {
        try {
          await navigator.clipboard.writeText(btn.dataset.hex);
          celebrateSuccess(null, btn, "Copied " + btn.dataset.hex);
        } catch (e) {
          /* clipboard unavailable */
        }
      });
    });
  }

  let currentImg = null;

  async function handleFile(file) {
    try {
      const { img, url } = await loadImageFile(file);
      currentImg = img;
      els.previewImg.src = url;
      els.previewWrap.style.display = "block";
      run();
    } catch (e) {
      setResult("error", e.message);
    }
  }

  function run() {
    if (!currentImg) return;
    const count = Number(els.countSelect.value) || 8;
    const colors = extractPalette(currentImg, count);
    renderPalette(colors);
    setResult("ok", `Extracted ${colors.length} colors. Click any swatch to copy its hex code.`);
  }

  els.countSelect.addEventListener("change", run);

  els.fileInput.addEventListener("change", () => {
    if (els.fileInput.files[0]) handleFile(els.fileInput.files[0]);
  });
  els.drop.addEventListener("click", () => els.fileInput.click());
  els.drop.addEventListener("dragover", (e) => { e.preventDefault(); els.drop.classList.add("drag"); });
  els.drop.addEventListener("dragleave", () => els.drop.classList.remove("drag"));
  els.drop.addEventListener("drop", (e) => {
    e.preventDefault();
    els.drop.classList.remove("drag");
    if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
  });
  document.addEventListener("paste", (e) => {
    const item = Array.from(e.clipboardData?.items || []).find((it) => it.type.startsWith("image/"));
    if (item) handleFile(item.getAsFile());
  });
})();
