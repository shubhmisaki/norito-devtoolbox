(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    input: document.getElementById("svgInput"),
    removeDims: document.getElementById("optRemoveDims"),
    previewWrap: document.getElementById("previewWrap"),
    previewHint: document.getElementById("previewHint"),
    stats: document.getElementById("sizeStats"),
    output: document.getElementById("output"),
    copyBtn: document.getElementById("copyBtn"),
    downloadBtn: document.getElementById("downloadBtn"),
  };

  function optimize(svgText) {
    let s = svgText;
    // Strip XML declaration and DOCTYPE
    s = s.replace(/<\?xml[^>]*\?>/gi, "");
    s = s.replace(/<!DOCTYPE[^>]*>/gi, "");
    // Strip comments
    s = s.replace(/<!--[\s\S]*?-->/g, "");
    // Strip metadata/title/desc blocks (editor cruft, not required for rendering)
    s = s.replace(/<metadata[\s\S]*?<\/metadata>/gi, "");
    s = s.replace(/<title>[\s\S]*?<\/title>/gi, "");
    s = s.replace(/<desc>[\s\S]*?<\/desc>/gi, "");
    // Strip editor-specific namespaced attributes (inkscape:, sodipodi:, sketch:)
    s = s.replace(/\s(inkscape|sodipodi|sketch):[\w-]+="[^"]*"/gi, "");
    // Strip empty inkscape/sodipodi elements
    s = s.replace(/<(sodipodi|inkscape):[\w-]+[^>]*\/>/gi, "");
    // Collapse whitespace between tags
    s = s.replace(/>\s+</g, "><");
    // Collapse repeated whitespace
    s = s.replace(/\s{2,}/g, " ");
    s = s.trim();

    if (els.removeDims.checked) {
      s = s.replace(/<svg([^>]*)\swidth="[^"]*"/i, "<svg$1");
      s = s.replace(/<svg([^>]*)\sheight="[^"]*"/i, "<svg$1");
    }

    return s;
  }

  function render() {
    const raw = els.input.value;
    if (!raw.trim()) {
      els.output.textContent = "";
      els.stats.textContent = "";
      els.previewWrap.innerHTML = '<p class="note" id="previewHint">Preview appears here.</p>';
      return;
    }
    const optimized = optimize(raw);
    const before = new Blob([raw]).size;
    const after = new Blob([optimized]).size;
    const pct = before > 0 ? Math.round((1 - after / before) * 100) : 0;

    els.output.textContent = optimized;
    els.stats.textContent = `${formatBytes(before)} → ${formatBytes(after)} (${pct >= 0 ? "-" : "+"}${Math.abs(pct)}%)`;

    // Preview: only render if it parses as a valid SVG document
    try {
      const doc = new DOMParser().parseFromString(optimized, "image/svg+xml");
      if (doc.querySelector("parsererror")) throw new Error("parse error");
      const svgEl = doc.documentElement;
      svgEl.style.maxWidth = "100%";
      svgEl.style.maxHeight = "160px";
      els.previewWrap.innerHTML = "";
      els.previewWrap.appendChild(document.importNode(svgEl, true));
    } catch (e) {
      els.previewWrap.innerHTML = '<p class="note">Can\'t preview: not valid SVG markup yet.</p>';
    }
  }

  els.input.addEventListener("input", render);
  els.removeDims.addEventListener("change", render);

  function loadFile(file) {
    if (!file || !/svg/.test(file.type) && !/\.svg$/i.test(file.name)) return;
    const reader = new FileReader();
    reader.onload = () => {
      els.input.value = String(reader.result || "");
      render();
    };
    reader.readAsText(file);
  }

  els.fileInput.addEventListener("change", () => loadFile(els.fileInput.files[0]));
  wireDragDrop(els.drop, (e) => {
    const file = e.dataTransfer.files && e.dataTransfer.files[0];
    loadFile(file);
  });
  els.drop.addEventListener("click", (e) => {
    if (e.target === els.fileInput) return;
    els.fileInput.click();
  });

  els.copyBtn.addEventListener("click", async () => {
    if (!els.output.textContent) return;
    try {
      await copyToClipboard(els.output.textContent);
      const I18N_C = i18nFor("common");
      showMascotToast(I18N_C.copied || "Copied!");
      celebrateSuccess(els.copyBtn);
    } catch (e) { /* clipboard unavailable, silently ignore */ }
  });

  els.downloadBtn.addEventListener("click", () => {
    if (!els.output.textContent) return;
    downloadBlob(new Blob([els.output.textContent], { type: "image/svg+xml" }), "optimized.svg");
  });
})();
