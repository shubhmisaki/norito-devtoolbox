(function () {
  const I18N = i18nFor("app-compress");
  const I18N_C = i18nFor("common");
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    size: document.getElementById("targetSize"),
    unit: document.getElementById("targetUnit"),
    format: document.getElementById("format"),
    allowResize: document.getElementById("allowResize"),
    compressBtn: document.getElementById("compressBtn"),
    result: document.getElementById("result"),
    preview: document.getElementById("preview"),
    originalInfo: document.getElementById("originalInfo"),
    previewHint: document.getElementById("previewHint"),
  };

  let currentImg = null;
  let currentFile = null;

  // Remember unit/resize choices between visits: nice-to-have only, silently
  // no-ops if localStorage is unavailable. Output format is deliberately
  // NOT persisted here (see handleFile below): it used to be, but that
  // meant picking PNG once to test something would silently stick as the
  // default for every future upload, including plain photos, where PNG
  // almost never beats the original size. Format now auto-matches whatever
  // file you just uploaded instead, which is the sane default for "just
  // compress this" use and avoids that trap entirely.
  const PREFS_KEY = "norito:compress-image";
  function loadPrefs() {
    try { return JSON.parse(localStorage.getItem(PREFS_KEY)) || {}; } catch (e) { return {}; }
  }
  function savePref(key, value) {
    try {
      const p = loadPrefs();
      p[key] = value;
      localStorage.setItem(PREFS_KEY, JSON.stringify(p));
    } catch (e) { /* ignore */ }
  }
  (function restorePrefs() {
    const p = loadPrefs();
    if (p.unit) els.unit.value = p.unit;
    if (typeof p.allowResize === "boolean" && els.allowResize) els.allowResize.checked = p.allowResize;
  })();
  els.unit.addEventListener("change", () => savePref("unit", els.unit.value));
  if (els.allowResize) {
    els.allowResize.addEventListener("change", () => savePref("allowResize", els.allowResize.checked));
  }

  function canvasToBlob(canvas, mime, quality) {
    return new Promise((resolve) => canvas.toBlob(resolve, mime, quality));
  }

  function loadImageFile(file) {
    return new Promise((resolve, reject) => {
      const url = URL.createObjectURL(file);
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = reject;
      img.src = url;
    });
  }

  // Picks a sensible starting output format for a freshly uploaded file:
  // matches the upload's own type (PNG stays PNG, WebP stays WebP), falling
  // back to JPEG for JPEGs and anything else canvas can decode but PNG/WebP
  // don't apply to. This runs on every upload, overriding whatever format
  // was selected for a previous file, since the right format is a property
  // of the image you just picked, not a fixed personal preference.
  function defaultFormatFor(fileType) {
    if (fileType === "image/png") return "png";
    if (fileType === "image/webp") return "webp";
    return "jpeg";
  }

  async function handleFile(file) {
    if (!file || !file.type.startsWith("image/")) {
      setResult(I18N_C.please_choose_image || "Please choose an image file.", false);
      return;
    }
    currentFile = file;
    currentImg = await loadImageFile(file);
    els.originalInfo.textContent =
      `${file.name}, ${currentImg.width}×${currentImg.height}, ${formatBytes(file.size)}`;
    els.originalInfo.style.display = "block";
    els.format.value = defaultFormatFor(file.type);
    els.compressBtn.disabled = false;
  }

  els.drop.addEventListener("click", () => els.fileInput.click());
  els.fileInput.addEventListener("change", (e) => handleFile(e.target.files[0]));
  ["dragenter", "dragover"].forEach((evt) =>
    els.drop.addEventListener(evt, (e) => { e.preventDefault(); els.drop.classList.add("drag"); })
  );
  ["dragleave", "drop"].forEach((evt) =>
    els.drop.addEventListener(evt, (e) => { e.preventDefault(); els.drop.classList.remove("drag"); })
  );
  els.drop.addEventListener("drop", (e) => {
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  });

  // Paste an image straight from the clipboard (screenshot tools, "Copy image", etc.)
  document.addEventListener("paste", (e) => {
    const items = e.clipboardData && e.clipboardData.items;
    if (!items) return;
    for (const item of items) {
      if (item.type && item.type.startsWith("image/")) {
        const file = item.getAsFile();
        if (file) { handleFile(file); e.preventDefault(); }
        break;
      }
    }
  });

  const ICONS = {
    ok: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="M22 4 12 14.01l-3-3"/></svg>',
    error: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>',
    neutral: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>',
  };

  function setResult(html, state) {
    const cls = state === true ? "ok" : state === false ? "error" : state || "neutral";
    els.result.innerHTML =
      `<span class="r-icon">${ICONS[cls] || ICONS.neutral}</span><span class="r-body">${html}</span>`;
    els.result.style.display = "flex";
    els.result.classList.remove("ok", "error");
    if (cls === "ok" || cls === "error") els.result.classList.add(cls);
  }

  function pulseHighlight(el) {
    if (!el) return;
    el.classList.remove("highlight-pulse");
    void el.offsetWidth;
    el.classList.add("highlight-pulse");
    setTimeout(() => el.classList.remove("highlight-pulse"), 1300);
  }

  // Returns { blob, width, height, resized } instead of a bare blob, so the
  // caller can tell the user whether dimensions changed. By default (allowResize
  // false) this only binary-searches quality at the image's original size.
  // it never shrinks the image unless the user explicitly opts in.
  async function compressLossy(img, targetBytes, mime, allowResize) {
    let scale = 1.0;
    let best = null; // first scale that actually hit the target
    let closest = null; // smallest blob seen, in case target is never hit
    const maxAttempts = allowResize ? 10 : 1;

    for (let attempt = 0; attempt < maxAttempts; attempt++) {
      const w = Math.max(1, Math.round(img.width * scale));
      const h = Math.max(1, Math.round(img.height * scale));
      const canvas = document.createElement("canvas");
      canvas.width = w;
      canvas.height = h;
      canvas.getContext("2d").drawImage(img, 0, 0, w, h);
      const resized = scale !== 1;

      let lo = 0.01, hi = 1.0, foundAtScale = null;
      for (let i = 0; i < 8; i++) {
        const mid = (lo + hi) / 2;
        const blob = await canvasToBlob(canvas, mime, mid);
        if (!closest || blob.size < closest.blob.size) closest = { blob, width: w, height: h, resized };
        if (blob.size <= targetBytes) { foundAtScale = blob; lo = mid; } else { hi = mid; }
      }
      if (!foundAtScale) {
        const blob = await canvasToBlob(canvas, mime, 0.01);
        if (!closest || blob.size < closest.blob.size) closest = { blob, width: w, height: h, resized };
        if (blob.size <= targetBytes) foundAtScale = blob;
      }
      if (foundAtScale) { best = { blob: foundAtScale, width: w, height: h, resized }; break; }
      if (w <= 16 || h <= 16) break;
      scale *= 0.85;
    }
    return best || closest;
  }

  // ---- PNG color quantization ----
  // PNG has no lossy "quality" parameter the way JPEG/WebP do: canvas.toBlob
  // always writes a full 24/32-bit-per-pixel losslessly-encoded file, which
  // is why a photo saved as PNG can come out several times *larger* than
  // the same photo as JPEG, with literally no lever to shrink it besides
  // resizing. Real PNG optimizers (TinyPNG, pngquant) get 60-80% smaller
  // files by reducing to a small color palette (still valid PNG, no resize,
  // no format change); browsers' canvas encoder won't do that for us, so
  // this implements it directly: median-cut palette generation, a coarse
  // 3D lookup table for fast nearest-palette-color lookups (needed so a
  // multi-megapixel photo doesn't require millions of per-pixel distance
  // comparisons), and Floyd-Steinberg error diffusion so the reduced color
  // count doesn't produce visible banding.

  // Builds a palette of up to k representative colors from the image using
  // median-cut quantization. Runs on a bounded sample of pixels (not every
  // pixel) purely for speed; the palette only needs to represent the
  // image's color distribution, the actual per-pixel mapping in
  // ditherToPalette below still sees every pixel.
  function buildPalette(data, w, h, k) {
    const total = w * h;
    const sampleStep = Math.max(1, Math.floor(total / 20000));
    const samples = [];
    for (let p = 0; p < total; p += sampleStep) {
      const i = p * 4;
      samples.push([data[i], data[i + 1], data[i + 2]]);
    }
    if (samples.length === 0) samples.push([0, 0, 0]);

    let boxes = [samples];
    while (boxes.length < k) {
      let idx = 0, maxLen = 0;
      for (let b = 0; b < boxes.length; b++) {
        if (boxes[b].length > maxLen) { maxLen = boxes[b].length; idx = b; }
      }
      if (maxLen <= 1) break; // nothing left worth splitting further
      const box = boxes[idx];

      let rMin = 255, rMax = 0, gMin = 255, gMax = 0, bMin = 255, bMax = 0;
      for (const [r, g, b] of box) {
        if (r < rMin) rMin = r; if (r > rMax) rMax = r;
        if (g < gMin) gMin = g; if (g > gMax) gMax = g;
        if (b < bMin) bMin = b; if (b > bMax) bMax = b;
      }
      const rRange = rMax - rMin, gRange = gMax - gMin, bRange = bMax - bMin;
      let axis = 0; // split along whichever channel has the widest spread
      if (gRange >= rRange && gRange >= bRange) axis = 1;
      else if (bRange >= rRange && bRange >= gRange) axis = 2;

      box.sort((a, c) => a[axis] - c[axis]);
      const mid = Math.floor(box.length / 2);
      boxes.splice(idx, 1, box.slice(0, mid), box.slice(mid));
    }

    return boxes.filter((b) => b.length).map((box) => {
      let sr = 0, sg = 0, sb = 0;
      for (const [r, g, b] of box) { sr += r; sg += g; sb += b; }
      const n = box.length;
      return [Math.round(sr / n), Math.round(sg / n), Math.round(sb / n)];
    });
  }

  // A coarse 16x16x16 grid mapping any RGB bucket to its nearest palette
  // entry, precomputed once per palette. Without this, finding the nearest
  // of e.g. 32 palette colors for every pixel of a 5-megapixel photo would
  // mean 150M+ distance comparisons; with it, each pixel is a single array
  // lookup after a cheap bucket calculation.
  const LUT_LEVELS = 16;
  function buildLut(palette) {
    const lut = new Uint8Array(LUT_LEVELS ** 3);
    const step = 256 / LUT_LEVELS;
    let b = 0;
    for (let ri = 0; ri < LUT_LEVELS; ri++) {
      const r = Math.min(255, Math.round((ri + 0.5) * step));
      for (let gi = 0; gi < LUT_LEVELS; gi++) {
        const g = Math.min(255, Math.round((gi + 0.5) * step));
        for (let bi = 0; bi < LUT_LEVELS; bi++, b++) {
          const bl = Math.min(255, Math.round((bi + 0.5) * step));
          let best = 0, bestDist = Infinity;
          for (let p = 0; p < palette.length; p++) {
            const [pr, pg, pb] = palette[p];
            const dr = r - pr, dg = g - pg, db = bl - pb;
            const dist = dr * dr + dg * dg + db * db;
            if (dist < bestDist) { bestDist = dist; best = p; }
          }
          lut[b] = best;
        }
      }
    }
    return lut;
  }
  function lutIndex(r, g, b) {
    const step = 256 / LUT_LEVELS;
    const ri = Math.min(LUT_LEVELS - 1, Math.floor(r / step));
    const gi = Math.min(LUT_LEVELS - 1, Math.floor(g / step));
    const bi = Math.min(LUT_LEVELS - 1, Math.floor(b / step));
    return (ri * LUT_LEVELS + gi) * LUT_LEVELS + bi;
  }

  // Maps every pixel to its nearest palette color, diffusing the resulting
  // rounding error to neighboring not-yet-visited pixels (standard
  // Floyd-Steinberg weights) so a small palette still looks like a smooth
  // gradient instead of visible banding. Does NOT mutate `data`, it returns
  // a fresh array of palette indices, so the same getImageData() call can
  // be reused across every palette-size attempt below instead of re-drawing
  // the canvas each time.
  //
  // Earlier version of this function wrote the palette color straight back
  // into a 4-byte RGBA buffer and let canvas.toBlob re-encode it as an
  // ordinary 24-bit truecolor PNG. Verified against real encoders that
  // approach barely helped (some palette sizes even came out *larger* than
  // full color): dithering breaks smooth gradients into higher-frequency
  // noise, and since every pixel was still 3-4 bytes, that noise fights
  // DEFLATE more than the smaller color count helps it. The only way to get
  // the real win is writing genuinely 1-byte-per-pixel indexed data, which
  // is what encodeIndexedPngBlob below does.
  function ditherToIndices(data, w, h, palette, lut) {
    const buf = new Float32Array(w * h * 3);
    for (let p = 0, i = 0; p < w * h; p++, i += 4) {
      buf[p * 3] = data[i];
      buf[p * 3 + 1] = data[i + 1];
      buf[p * 3 + 2] = data[i + 2];
    }
    const indices = new Uint8Array(w * h);
    for (let y = 0; y < h; y++) {
      for (let x = 0; x < w; x++) {
        const p = y * w + x;
        const oi = p * 3;
        const r = Math.min(255, Math.max(0, buf[oi]));
        const g = Math.min(255, Math.max(0, buf[oi + 1]));
        const b = Math.min(255, Math.max(0, buf[oi + 2]));
        const idx = lut[lutIndex(r, g, b)];
        indices[p] = idx;
        const [pr, pg, pb] = palette[idx];
        const er = r - pr, eg = g - pg, eb = b - pb;
        if (x + 1 < w) { const q = (p + 1) * 3; buf[q] += er * 7 / 16; buf[q + 1] += eg * 7 / 16; buf[q + 2] += eb * 7 / 16; }
        if (y + 1 < h) {
          if (x > 0) { const q = (p + w - 1) * 3; buf[q] += er * 3 / 16; buf[q + 1] += eg * 3 / 16; buf[q + 2] += eb * 3 / 16; }
          { const q = (p + w) * 3; buf[q] += er * 5 / 16; buf[q + 1] += eg * 5 / 16; buf[q + 2] += eb * 5 / 16; }
          if (x + 1 < w) { const q = (p + w + 1) * 3; buf[q] += er * 1 / 16; buf[q + 1] += eg * 1 / 16; buf[q + 2] += eb * 1 / 16; }
        }
      }
    }
    return indices;
  }

  function isFullyOpaque(data) {
    for (let i = 3; i < data.length; i += 4) if (data[i] !== 255) return false;
    return true;
  }

  // ---- true indexed-color PNG file writer ----
  // canvas.toBlob has no option to request an indexed-color PNG, browsers
  // only ever write full truecolor. To actually get 1-byte-per-pixel output
  // this builds the PNG file directly: signature + IHDR (color type 3) +
  // PLTE (the palette) + IDAT (the indices, DEFLATE-compressed via the
  // browser's native CompressionStream, no library needed) + IEND.
  async function deflateBytes(bytes) {
    const cs = new CompressionStream("deflate");
    const writer = cs.writable.getWriter();
    writer.write(bytes);
    writer.close();
    const chunks = [];
    let total = 0;
    const reader = cs.readable.getReader();
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      chunks.push(value);
      total += value.length;
    }
    const out = new Uint8Array(total);
    let offset = 0;
    for (const c of chunks) { out.set(c, offset); offset += c.length; }
    return out;
  }
  const CRC_TABLE = (() => {
    const t = new Uint32Array(256);
    for (let n = 0; n < 256; n++) {
      let c = n;
      for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
      t[n] = c >>> 0;
    }
    return t;
  })();
  function crc32(bytes) {
    let c = 0xffffffff;
    for (let i = 0; i < bytes.length; i++) c = CRC_TABLE[(c ^ bytes[i]) & 0xff] ^ (c >>> 8);
    return (c ^ 0xffffffff) >>> 0;
  }
  function u32be(n) {
    return new Uint8Array([(n >>> 24) & 255, (n >>> 16) & 255, (n >>> 8) & 255, n & 255]);
  }
  function pngChunk(type, data) {
    const typeBytes = new Uint8Array(type.split("").map((c) => c.charCodeAt(0)));
    const body = new Uint8Array(typeBytes.length + data.length);
    body.set(typeBytes, 0);
    body.set(data, typeBytes.length);
    const crc = crc32(body);
    const out = new Uint8Array(4 + body.length + 4);
    out.set(u32be(data.length), 0);
    out.set(body, 4);
    out.set(u32be(crc), 4 + body.length);
    return out;
  }
  function concatBytes(arrays) {
    const total = arrays.reduce((s, a) => s + a.length, 0);
    const out = new Uint8Array(total);
    let offset = 0;
    for (const a of arrays) { out.set(a, offset); offset += a.length; }
    return out;
  }
  async function encodeIndexedPngBlob(indices, palette, w, h) {
    const sig = new Uint8Array([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
    const ihdr = new Uint8Array(13);
    new DataView(ihdr.buffer).setUint32(0, w);
    new DataView(ihdr.buffer).setUint32(4, h);
    ihdr[8] = 8; // bit depth
    ihdr[9] = 3; // color type: indexed
    const plte = new Uint8Array(palette.length * 3);
    for (let i = 0; i < palette.length; i++) {
      plte[i * 3] = palette[i][0]; plte[i * 3 + 1] = palette[i][1]; plte[i * 3 + 2] = palette[i][2];
    }
    // Raw scanlines, each prefixed with a filter-type byte (0/None: palette
    // indices aren't smooth gradients, so predictive filtering doesn't
    // help them the way it helps photographic truecolor data).
    const raw = new Uint8Array(h * (w + 1));
    for (let y = 0; y < h; y++) {
      raw[y * (w + 1)] = 0;
      raw.set(indices.subarray(y * w, y * w + w), y * (w + 1) + 1);
    }
    const idatData = await deflateBytes(raw);
    const bytes = concatBytes([
      sig,
      pngChunk("IHDR", ihdr),
      pngChunk("PLTE", plte),
      pngChunk("IDAT", idatData),
      pngChunk("IEND", new Uint8Array(0)),
    ]);
    return new Blob([bytes], { type: "image/png" });
  }

  // Palette sizes to walk through, largest (best quality) first. 8 is the
  // floor: fewer colors than that looks posterized, matching the same
  // "ugly but still an honest attempt" floor the JPEG path allows at
  // quality 0.01.
  const PNG_PALETTE_STEPS = [128, 64, 32, 16, 8];

  async function compressPng(img, targetBytes, allowResize) {
    if (!allowResize) {
      // No resizing: this is PNG's one real size lever. Try full color
      // first (best quality, and plenty of PNGs, especially graphics and
      // screenshots, are already small enough here), then walk the color
      // palette down before admitting we can't hit the target.
      const canvas = document.createElement("canvas");
      canvas.width = img.width;
      canvas.height = img.height;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(img, 0, 0, img.width, img.height);
      const fullColorBlob = await canvasToBlob(canvas, "image/png");
      let best = { blob: fullColorBlob, width: img.width, height: img.height, resized: false };
      if (fullColorBlob.size <= targetBytes) return best;

      // The indexed-PNG path needs the Compression Streams API (broadly
      // supported in current browsers, but feature-detected rather than
      // assumed) and, for now, a fully opaque image: indexed PNGs only
      // support one alpha value per palette entry via a tRNS chunk, not
      // arbitrary per-pixel alpha, so an image with soft/varying
      // transparency falls through to the JPEG-switch nudge instead, which
      // is already offered whenever a PNG result misses its target.
      if (typeof CompressionStream === "function") {
        const imgData = ctx.getImageData(0, 0, img.width, img.height);
        if (isFullyOpaque(imgData.data)) {
          for (const k of PNG_PALETTE_STEPS) {
            const palette = buildPalette(imgData.data, img.width, img.height, k);
            const lut = buildLut(palette);
            const indices = ditherToIndices(imgData.data, img.width, img.height, palette, lut);
            const qBlob = await encodeIndexedPngBlob(indices, palette, img.width, img.height);
            if (qBlob.size < best.blob.size) {
              best = { blob: qBlob, width: img.width, height: img.height, resized: false };
            }
            if (qBlob.size <= targetBytes) return best;
          }
        }
      }
      return best;
    }

    // Resizing allowed: unchanged, a pure dimension search. Left as-is
    // deliberately (per design: turning resizing on shouldn't change how
    // that path behaves).
    let scale = 1.0;
    let last = null;
    const maxAttempts = 20;
    for (let attempt = 0; attempt < maxAttempts; attempt++) {
      const w = Math.max(1, Math.round(img.width * scale));
      const h = Math.max(1, Math.round(img.height * scale));
      const canvas = document.createElement("canvas");
      canvas.width = w;
      canvas.height = h;
      canvas.getContext("2d").drawImage(img, 0, 0, w, h);
      const blob = await canvasToBlob(canvas, "image/png");
      last = { blob, width: w, height: h, resized: scale !== 1 };
      if (blob.size <= targetBytes) return last;
      if (w <= 8 || h <= 8) return last; // best effort, give up shrinking further
      scale *= 0.85;
    }
    return last;
  }

  // Pulled out of the click handler so the "enable resizing and try again"
  // nudge button (built below, only shown when resizing is off and the
  // target wasn't reached) can re-run the exact same flow after flipping
  // the checkbox, without the user having to click Compress a second time.
  async function runCompress() {
    if (!currentImg) return;
    const target = parseSize(els.size.value, els.unit.value);
    if (target === null || target <= 0) {
      setResult(I18N.err_invalid_target || "Enter a valid target size.", "error");
      return;
    }

    els.compressBtn.disabled = true;
    els.compressBtn.textContent = I18N.compressing_label || "Compressing…";
    setResult(I18N_C.working || "Working…", "neutral");
    let finishedState = null;

    try {
      const outFormat = els.format.value;
      const mime = { jpeg: "image/jpeg", webp: "image/webp", png: "image/png" }[outFormat];
      const allowResize = !!(els.allowResize && els.allowResize.checked);
      let outcome;
      if (outFormat === "png") outcome = await compressPng(currentImg, target, allowResize);
      else outcome = await compressLossy(currentImg, target, mime, allowResize);

      if (!outcome || !outcome.blob) {
        setResult(
          fmt(I18N.err_no_outcome || "Couldn't get under {target} even at minimum quality. Try a larger target, switch format, or turn on \"Allow resizing\".",
            { target: formatBytes(target) }),
          "error"
        );
        return;
      }

      // We always hand back the actual best-effort result here, the
      // smallest file our search found at the original dimensions (never
      // resized unless the user opted in). We used to silently swap this
      // out for the untouched original file whenever the best attempt was
      // larger, but that just hid a real (if imperfect) compression result
      // behind a no-op. Now we're honest about it instead: if it landed
      // bigger than the original, the headline below says so plainly.
      const blob = outcome.blob;
      const resized = outcome.resized;
      const outW = outcome.width;
      const outH = outcome.height;
      const originalSize = currentFile ? currentFile.size : null;
      const largerThanOriginal = originalSize != null && blob.size > originalSize;

      const url = URL.createObjectURL(blob);
      els.preview.src = url;
      els.preview.style.display = "block";
      if (els.previewHint) els.previewHint.style.display = "none";

      const ext = { jpeg: "jpg", webp: "webp", png: "png" }[outFormat];
      const filename = `compressed_${els.size.value}${els.unit.value}.${ext}`;
      const withinTarget = blob.size <= target;
      const dimsNote = resized
        ? fmt(I18N.dims_resized || "resized to {w}×{h} (from {ow}×{oh})",
            { w: outW, h: outH, ow: currentImg.width, oh: currentImg.height })
        : fmt(I18N.dims_original || "original {w}×{h} size",
            { w: outW, h: outH });

      let statusLine;
      let state;
      // Three outcomes: (1) hit the target, (2) missed it even with resizing
      // allowed (nothing more we can offer, per design: resizing on changes
      // nothing about this messaging), or (3) missed it with resizing OFF,
      // which is the one case where there's a concrete next step to offer:
      // this is the floor for quality-only compression at the original
      // resolution, and enabling resizing is what actually gets past it.
      const hitFloorWithoutResize = !withinTarget && !allowResize;
      if (withinTarget) {
        statusLine = fmt(I18N.status_within_target || "within your target, at {dims}.", { dims: dimsNote });
        state = "ok";
      } else if (allowResize) {
        statusLine = fmt(I18N.status_closest_resized || "closest achievable size (target was too small even after resizing), at {dims}.", { dims: dimsNote });
        state = "neutral";
      } else {
        statusLine = fmt(I18N.status_closest_noresize || "the smallest size possible without resizing, at {dims}.", { dims: dimsNote });
        state = "neutral";
      }

      // PNG is lossless, and even quality-based JPEG/WebP re-encoding has a
      // floor, so some source files genuinely won't shrink below their
      // original size at these dimensions. Calling that "compressed
      // successfully" would be misleading, so the headline says so plainly
      // instead of quietly substituting the original file.
      let headlineKey, headlineVars = { size: formatBytes(blob.size), statusLine };
      if (withinTarget) {
        headlineKey = "result_success";
      } else if (largerThanOriginal) {
        headlineKey = "result_larger_than_original";
        headlineVars.origSize = formatBytes(originalSize);
      } else {
        headlineKey = "result_partial";
      }
      const headlineDefaults = {
        result_success: "<strong>Image compressed successfully.</strong> <strong>{size}</strong>. {statusLine}",
        result_partial: "<strong>Reduced as much as we could.</strong> <strong>{size}</strong>. {statusLine}",
        result_larger_than_original:
          "<strong>This is the most we could compress without resizing:</strong> <strong>{size}</strong>, slightly larger than your original ({origSize}). {statusLine}",
      };

      let nudgeHtml = "";
      if (!withinTarget && outFormat === "png") {
        nudgeHtml = `<div class="resize-nudge"><p>${
          I18N.format_nudge_question ||
          "PNG is lossless, so it often produces larger files than JPEG or WebP for photos. Want to switch to JPEG and compress again?"
        }</p><button type="button" id="formatRetryBtn" class="secondary">${
          I18N.switch_to_jpeg_retry_btn || "Switch to JPEG & compress again"
        }</button></div>`;
      } else if (hitFloorWithoutResize) {
        nudgeHtml = `<div class="resize-nudge"><p>${fmt(
          I18N.resize_nudge_question ||
            "This is the smallest file we can get without resizing. Want to enable resizing to reach {target}?",
          { target: formatBytes(target) }
        )}</p><button type="button" id="resizeRetryBtn" class="secondary">${
          I18N.enable_resize_retry_btn || "Enable resizing & compress again"
        }</button></div>`;
      }

      setResult(
        fmt(I18N[headlineKey] || headlineDefaults[headlineKey], headlineVars) +
        nudgeHtml +
        `<br><br><button id="dlBtn">${fmt(I18N.download_button || "Download {filename}", { filename })}</button>`,
        state
      );
      const dlBtn = document.getElementById("dlBtn");
      dlBtn.addEventListener("click", () => downloadBlob(blob, filename));
      const resizeRetryBtn = document.getElementById("resizeRetryBtn");
      if (resizeRetryBtn) {
        resizeRetryBtn.addEventListener("click", () => {
          els.allowResize.checked = true;
          savePref("allowResize", true);
          runCompress();
        });
      }
      const formatRetryBtn = document.getElementById("formatRetryBtn");
      if (formatRetryBtn) {
        formatRetryBtn.addEventListener("click", () => {
          els.format.value = "jpeg";
          runCompress();
        });
      }
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
      pulseHighlight(dlBtn);
      finishedState = state;
    } catch (err) {
      console.error("[compress] failed:", err);
      setResult(
        fmt(I18N.err_generic || "<strong>Couldn't compress that image.</strong> {msg}. Try a different image, or switch format and try again.",
          { msg: err.message }),
        "error"
      );
    } finally {
      els.compressBtn.disabled = false;
      els.compressBtn.textContent = I18N.btn_compress_default || "Compress to target";
    }
    // Runs after the button label has already been restored above, so the
    // checkmark morph is the last thing to touch the button, not undone by
    // the finally block's textContent reset happening in the same tick.
    if (finishedState === "ok") celebrateSuccess(els.compressBtn, els.result);
  }

  els.compressBtn.addEventListener("click", runCompress);
})();
