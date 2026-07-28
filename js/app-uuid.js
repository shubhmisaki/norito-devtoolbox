(function () {
  const I18N_C = i18nFor("common");

  const els = {
    count: document.getElementById("count"),
    uppercase: document.getElementById("optUppercase"),
    noHyphens: document.getElementById("optNoHyphens"),
    genBtn: document.getElementById("genBtn"),
    copyAllBtn: document.getElementById("copyAllBtn"),
    list: document.getElementById("uuidList"),
  };

  function formatUuid(raw) {
    let v = raw;
    if (els.noHyphens.checked) v = v.replace(/-/g, "");
    if (els.uppercase.checked) v = v.toUpperCase();
    return v;
  }

  function generateOne() {
    return crypto.randomUUID();
  }

  let current = [];

  function render() {
    els.list.innerHTML = current
      .map(
        (raw, i) => `
      <div class="slug-row">
        <div class="slug-row-text">
          <div class="slug-row-title">UUID v4 #${i + 1}</div>
          <div class="slug-row-slug">${formatUuid(raw)}</div>
        </div>
        <button type="button" class="secondary copy-one" data-index="${i}">${I18N_C.copy || "Copy"}</button>
      </div>`
      )
      .join("");
  }

  function generateAll() {
    const n = Math.min(100, Math.max(1, parseInt(els.count.value, 10) || 1));
    els.count.value = n;
    current = Array.from({ length: n }, generateOne);
    render();
  }

  els.genBtn.addEventListener("click", () => {
    generateAll();
    celebrateSuccess(els.genBtn);
  });
  els.uppercase.addEventListener("change", render);
  els.noHyphens.addEventListener("change", render);

  els.list.addEventListener("click", async (e) => {
    const btn = e.target.closest(".copy-one");
    if (!btn) return;
    const idx = parseInt(btn.dataset.index, 10);
    const value = formatUuid(current[idx]);
    try {
      await copyToClipboard(value);
    } catch (err) {
      const ta = document.createElement("textarea");
      ta.value = value;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
    }
    const original = btn.textContent;
    btn.textContent = I18N_C.copied || "Copied";
    setTimeout(() => { btn.textContent = original; }, 1200);
  });

  els.copyAllBtn.addEventListener("click", async () => {
    if (!current.length) return;
    const text = current.map(formatUuid).join("\n");
    try {
      await copyToClipboard(text);
    } catch (err) {
      const ta = document.createElement("textarea");
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
    }
    showMascotToast(I18N_C.copied || "Copied!");
    celebrateSuccess(els.copyAllBtn);
  });

  generateAll();
})();
