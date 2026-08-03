(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    results: document.getElementById("resultsWrap"),
  };

  function gcd(a, b) { return b === 0 ? a : gcd(b, a % b); }

  async function inspectOne(file) {
    const { img, url } = await loadImageFile(file);
    URL.revokeObjectURL(url); // only needed to decode dimensions
    const w = img.naturalWidth, h = img.naturalHeight;
    const divisor = gcd(w, h) || 1;
    return {
      name: file.name,
      w, h,
      ratioSimplified: `${w / divisor}:${h / divisor}`,
      ratioDecimal: (w / h).toFixed(3),
      megapixels: ((w * h) / 1_000_000).toFixed(2),
      size: formatBytes(file.size),
      type: file.type || "unknown",
    };
  }

  async function handleFiles(fileList) {
    const files = Array.from(fileList).filter((f) => f.type.startsWith("image/"));
    if (!files.length) return;
    const rows = [];
    for (const file of files) {
      try {
        rows.push(await inspectOne(file));
      } catch (e) { /* skip files that fail to decode */ }
    }
    render(rows);
  }

  function render(rows) {
    if (!rows.length) return;
    const html = rows
      .map(
        (r) => `
      <div class="result-box" style="text-align:left; margin-bottom:10px;">
        <div style="font-weight:600; margin-bottom:6px; word-break:break-all;">${escapeHtml(r.name)}</div>
        <div class="note">
          ${r.w} &times; ${r.h}px &middot; ${r.ratioSimplified} (${r.ratioDecimal}) &middot;
          ${r.megapixels} MP &middot; ${r.size} &middot; ${escapeHtml(r.type)}
        </div>
      </div>`
      )
      .join("");
    els.results.innerHTML = html + els.results.innerHTML;
  }

  function escapeHtml(str) {
    const d = document.createElement("div");
    d.textContent = str;
    return d.innerHTML;
  }

  els.fileInput.addEventListener("change", () => handleFiles(els.fileInput.files));
  wireDragDrop(els.drop, (e) => handleFiles(e.dataTransfer.files));
  els.drop.addEventListener("click", (e) => {
    if (e.target === els.fileInput) return;
    els.fileInput.click();
  });
})();
