(function () {
  const els = {
    rowsWrap: document.getElementById("rowsWrap"),
    addRowBtn: document.getElementById("addRowBtn"),
    optXDefault: document.getElementById("optXDefault"),
    xDefaultRow: document.getElementById("xDefaultRow"),
    xDefaultSelect: document.getElementById("xDefaultSelect"),
    output: document.getElementById("output"),
    copyBtn: document.getElementById("copyBtn"),
  };

  let rows = [
    { lang: "en", url: "https://example.com/" },
    { lang: "es", url: "https://example.com/es/" },
    { lang: "fr", url: "https://example.com/fr/" },
  ];
  let xDefaultIdx = 0;

  function renderRows() {
    els.rowsWrap.innerHTML = rows
      .map(
        (r, i) => `
      <div class="field-row" data-idx="${i}" style="align-items:flex-end;">
        <div class="field" style="max-width:120px;">
          <label>Locale</label>
          <input type="text" class="row-lang" value="${escapeAttr(r.lang)}" placeholder="en-US" />
        </div>
        <div class="field">
          <label>URL</label>
          <input type="text" class="row-url" value="${escapeAttr(r.url)}" placeholder="https://example.com/" />
        </div>
        ${rows.length > 1 ? '<button type="button" class="secondary row-remove">&times;</button>' : ""}
      </div>`
      )
      .join("");

    els.rowsWrap.querySelectorAll("[data-idx]").forEach((row) => {
      const idx = Number(row.dataset.idx);
      row.querySelector(".row-lang").addEventListener("input", (e) => { rows[idx].lang = e.target.value; build(); });
      row.querySelector(".row-url").addEventListener("input", (e) => { rows[idx].url = e.target.value; renderXDefaultOptions(); build(); });
      const removeBtn = row.querySelector(".row-remove");
      if (removeBtn) removeBtn.addEventListener("click", () => {
        rows.splice(idx, 1);
        if (xDefaultIdx >= rows.length) xDefaultIdx = 0;
        renderRows();
        renderXDefaultOptions();
        build();
      });
    });
  }

  function renderXDefaultOptions() {
    els.xDefaultSelect.innerHTML = rows
      .map((r, i) => `<option value="${i}" ${i === xDefaultIdx ? "selected" : ""}>${escapeAttr(r.lang || `Row ${i + 1}`)} — ${escapeAttr(r.url || "(no URL)")}</option>`)
      .join("");
  }

  function escapeAttr(str) {
    return String(str).replace(/"/g, "&quot;");
  }

  function build() {
    els.xDefaultRow.style.display = els.optXDefault.checked ? "block" : "none";
    const valid = rows.filter((r) => r.lang.trim() && r.url.trim());
    if (!valid.length) {
      els.output.textContent = "";
      return;
    }
    const lines = rows
      .filter((r) => r.lang.trim() && r.url.trim())
      .map((r) => `<link rel="alternate" hreflang="${r.lang.trim()}" href="${r.url.trim()}" />`);

    if (els.optXDefault.checked && rows[xDefaultIdx] && rows[xDefaultIdx].url.trim()) {
      lines.push(`<link rel="alternate" hreflang="x-default" href="${rows[xDefaultIdx].url.trim()}" />`);
    }
    els.output.textContent = lines.join("\n");
  }

  els.addRowBtn.addEventListener("click", () => {
    rows.push({ lang: "", url: "" });
    renderRows();
    renderXDefaultOptions();
    build();
  });
  els.optXDefault.addEventListener("change", build);
  els.xDefaultSelect.addEventListener("change", (e) => {
    xDefaultIdx = Number(e.target.value);
    build();
  });

  renderRows();
  renderXDefaultOptions();
  build();

  els.copyBtn.addEventListener("click", async () => {
    if (!els.output.textContent) return;
    try {
      await copyToClipboard(els.output.textContent);
      const I18N_C = i18nFor("common");
      showMascotToast(I18N_C.copied || "Copied!");
      celebrateSuccess(els.copyBtn);
    } catch (e) { /* clipboard unavailable, silently ignore */ }
  });
})();
