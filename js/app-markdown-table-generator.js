(function () {
  const els = {
    input: document.getElementById("csvInput"),
    optHeader: document.getElementById("optHeader"),
    alignWrap: document.getElementById("alignWrap"),
    output: document.getElementById("output"),
    preview: document.getElementById("renderedPreview"),
    copyBtn: document.getElementById("copyBtn"),
  };

  let aligns = []; // "left" | "center" | "right" per column

  function detectDelimiter(text) {
    const firstLine = text.split("\n")[0] || "";
    const commas = (firstLine.match(/,/g) || []).length;
    const tabs = (firstLine.match(/\t/g) || []).length;
    return tabs > commas ? "\t" : ",";
  }

  function parseRows(text) {
    const delim = detectDelimiter(text);
    return text
      .split("\n")
      .map((l) => l.replace(/\r$/, ""))
      .filter((l) => l.length)
      .map((line) => line.split(delim).map((c) => c.trim()));
  }

  function ensureAligns(colCount) {
    while (aligns.length < colCount) aligns.push("left");
    aligns.length = colCount;
  }

  function renderAlignControls(colCount) {
    ensureAligns(colCount);
    els.alignWrap.innerHTML =
      `<label style="display:block; margin-bottom:6px; font-size:13px; color:var(--muted);">Column alignment</label>` +
      Array.from({ length: colCount })
        .map(
          (_, i) => `
      <div class="field-row" style="margin-bottom:6px;">
        <span class="note" style="min-width:70px;">Column ${i + 1}</span>
        <select class="align-select" data-col="${i}" style="flex:1;">
          <option value="left" ${aligns[i] === "left" ? "selected" : ""}>Left</option>
          <option value="center" ${aligns[i] === "center" ? "selected" : ""}>Center</option>
          <option value="right" ${aligns[i] === "right" ? "selected" : ""}>Right</option>
        </select>
      </div>`
        )
        .join("");
    els.alignWrap.querySelectorAll(".align-select").forEach((sel) => {
      sel.addEventListener("change", () => {
        aligns[Number(sel.dataset.col)] = sel.value;
        build();
      });
    });
  }

  function alignSeparator(align) {
    if (align === "center") return ":---:";
    if (align === "right") return "----:";
    return ":----";
  }

  function build() {
    const rows = parseRows(els.input.value);
    if (!rows.length) {
      els.output.textContent = "";
      els.preview.innerHTML = "";
      els.alignWrap.innerHTML = "";
      return;
    }
    const colCount = Math.max(...rows.map((r) => r.length));
    rows.forEach((r) => { while (r.length < colCount) r.push(""); });
    renderAlignControls(colCount);

    const hasHeader = els.optHeader.checked;
    const header = hasHeader ? rows[0] : Array.from({ length: colCount }, (_, i) => `Column ${i + 1}`);
    const body = hasHeader ? rows.slice(1) : rows;

    const widths = header.map((h, i) => Math.max(h.length, ...body.map((r) => (r[i] || "").length), 3));

    const pad = (s, w, align) => {
      const diff = w - s.length;
      if (diff <= 0) return s;
      if (align === "right") return " ".repeat(diff) + s;
      if (align === "center") {
        const left = Math.floor(diff / 2), right = diff - left;
        return " ".repeat(left) + s + " ".repeat(right);
      }
      return s + " ".repeat(diff);
    };

    const headerLine = `| ${header.map((h, i) => pad(h, widths[i], aligns[i])).join(" | ")} |`;
    const sepLine = `| ${widths.map((w, i) => alignSeparator(aligns[i]).padEnd(w, "-")).join(" | ")} |`;
    const bodyLines = body.map((r) => `| ${r.map((c, i) => pad(c, widths[i], aligns[i])).join(" | ")} |`);

    const md = [headerLine, sepLine, ...bodyLines].join("\n");
    els.output.textContent = md;

    // Rendered preview (plain HTML table, not a markdown parser)
    const alignCss = { left: "left", center: "center", right: "right" };
    els.preview.innerHTML = `<table class="compare-table"><thead><tr>${header
      .map((h, i) => `<th style="text-align:${alignCss[aligns[i]]}">${escapeHtml(h)}</th>`)
      .join("")}</tr></thead><tbody>${body
      .map((r) => `<tr>${r.map((c, i) => `<td style="text-align:${alignCss[aligns[i]]}">${escapeHtml(c)}</td>`).join("")}</tr>`)
      .join("")}</tbody></table>`;
  }

  function escapeHtml(str) {
    const d = document.createElement("div");
    d.textContent = str;
    return d.innerHTML;
  }

  els.input.addEventListener("input", build);
  els.optHeader.addEventListener("change", build);
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
