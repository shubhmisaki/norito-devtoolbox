(function () {
  const I18N = i18nFor("app-testfile");
  const MAX_BYTES = 2 * 1024 * 1024 * 1024; // 2GB: typed array / browser memory ceiling

  const els = {
    ext: document.getElementById("ext"),
    size: document.getElementById("size"),
    unit: document.getElementById("unit"),
    mode: document.getElementById("mode"),
    modeRow: document.getElementById("modeRow"),
    generateBtn: document.getElementById("generateBtn"),
    result: document.getElementById("result"),
  };

  // Remember the unit the user picked last time, so it doesn't reset to KB
  // on every visit. Silently no-ops if localStorage is unavailable (private
  // browsing, quota, etc.), this is a nice-to-have, never load-bearing.
  const PREFS_KEY = "norito:test-file-generator";
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
  })();
  els.unit.addEventListener("change", () => savePref("unit", els.unit.value));

  function canvasToBlob(canvas, mime, quality) {
    return new Promise((resolve) => canvas.toBlob(resolve, mime, quality));
  }

  async function makeBaseImageBytes(mime) {
    const canvas = document.createElement("canvas");
    canvas.width = 8;
    canvas.height = 8;
    const ctx = canvas.getContext("2d");
    const grad = ctx.createLinearGradient(0, 0, 8, 8);
    grad.addColorStop(0, "#6ee7b7");
    grad.addColorStop(1, "#60a5fa");
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 8, 8);
    const blob = await canvasToBlob(canvas, mime, 0.6);
    const buf = await blob.arrayBuffer();
    return new Uint8Array(buf);
  }

  function mimeFor(ext) {
    return {
      txt: "text/plain",
      bin: "application/octet-stream",
      pdf: "application/pdf",
      zip: "application/zip",
      gif: "image/gif",
      jpg: "image/jpeg",
      png: "image/png",
    }[ext] || "application/octet-stream";
  }

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
    void el.offsetWidth; // restart the animation if it's still running
    el.classList.add("highlight-pulse");
    setTimeout(() => el.classList.remove("highlight-pulse"), 1300);
  }

  function updateModeVisibility() {
    const ext = els.ext.value;
    els.modeRow.style.display = (ext === "txt" || ext === "bin") ? "flex" : "none";
  }
  els.ext.addEventListener("change", updateModeVisibility);
  updateModeVisibility();

  els.generateBtn.addEventListener("click", async () => {
    let succeeded = false;
    const target = parseSize(els.size.value, els.unit.value);
    const ext = els.ext.value;

    if (target === null || target <= 0) {
      setResult(I18N.err_invalid_size || "Enter a valid, positive size.", "error");
      return;
    }
    if (target > MAX_BYTES) {
      setResult(I18N.err_max_size || "Max supported size is 2 GB in-browser (larger files risk crashing the tab).", "error");
      return;
    }

    els.generateBtn.disabled = true;
    els.generateBtn.textContent = I18N.generating_label || "Generating…";
    setResult(i18nFor("common").working || "Working…", "neutral");

    try {
      let bytes;
      const mode = els.mode.value;

      if (ext === "txt") bytes = generateTxt(target, mode);
      else if (ext === "bin") bytes = generateBin(target, mode);
      else if (ext === "pdf") bytes = generatePdf(target);
      else if (ext === "zip") bytes = generateZip(target, "payload.bin");
      else if (ext === "gif") bytes = padGif(target);
      else if (ext === "jpg") {
        const base = await makeBaseImageBytes("image/jpeg");
        bytes = padJpeg(base, target);
      } else if (ext === "png") {
        const base = await makeBaseImageBytes("image/png");
        bytes = padPng(base, target);
      }

      const blob = new Blob([bytes], { type: mimeFor(ext) });
      const actual = blob.size;
      const filename = `test-file_${els.size.value}${els.unit.value}.${ext}`;

      const exact = actual === target;
      const diff = actual - target;
      const note = exact
        ? fmt(I18N.result_exact || "<strong>Exact match.</strong> {size} generated.", { size: formatBytes(actual) })
        : fmt(I18N.result_offby || "<strong>{actual}</strong> generated (requested {target}, off by {diff} bytes, some formats have a small minimum structural size or padding granularity).",
            { actual: formatBytes(actual), target: formatBytes(target), diff: (diff > 0 ? "+" : "") + diff });

      setResult(
        `<strong>${I18N.result_success_prefix || "File generated successfully."}</strong> ${note}<br><br><button id="dlBtn">${fmt(I18N.download_button || "Download {filename}", { filename })}</button>`,
        exact ? "ok" : "neutral"
      );
      const dlBtn = document.getElementById("dlBtn");
      dlBtn.addEventListener("click", () => downloadBlob(blob, filename));
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
      pulseHighlight(dlBtn);
      succeeded = true;
    } catch (err) {
      console.error("[test-file] generation failed:", err);
      setResult(
        fmt(I18N.err_generic || "<strong>Couldn't generate that file.</strong> {msg}. Try a smaller size, or a different extension.", { msg: err.message }),
        "error"
      );
    } finally {
      els.generateBtn.disabled = false;
      els.generateBtn.textContent = I18N.btn_generate_default || "Generate file";
    }
    // Runs after the button label has already been restored above, so the
    // checkmark morph is the last thing to touch the button, not undone by
    // the finally block's textContent reset happening in the same tick.
    if (succeeded) celebrateSuccess(els.generateBtn, els.result);
  });
})();
