(function () {
  const ICONS = {
    ok: '<svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>',
    error: '<svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m15 9-6 6M9 9l6 6"/></svg>',
  };

  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    input: document.getElementById("csvInput"),
    delimiter: document.getElementById("delimiter"),
    headerToggle: document.getElementById("headerToggle"),
    prettyToggle: document.getElementById("prettyToggle"),
    output: document.getElementById("jsonOutput"),
    copyBtn: document.getElementById("copyBtn"),
    downloadBtn: document.getElementById("downloadBtn"),
    result: document.getElementById("result"),
  };

  function setResult(kind, html) {
    if (!els.result) return;
    els.result.style.display = "flex";
    els.result.className = "result-box " + (kind || "");
    els.result.innerHTML = (kind === "ok" ? ICONS.ok : kind === "error" ? ICONS.error : "") + `<div class="r-body">${html}</div>`;
  }

  // Parses CSV text (RFC 4180-ish: quoted fields, "" escapes a literal
  // quote, quoted fields may contain the delimiter or newlines) into an
  // array of rows, each row an array of string cells.
  function parseCsv(text, delim) {
    const rows = [];
    let row = [];
    let field = "";
    let inQuotes = false;
    let i = 0;
    const n = text.length;
    while (i < n) {
      const ch = text[i];
      if (inQuotes) {
        if (ch === '"') {
          if (text[i + 1] === '"') { field += '"'; i += 2; continue; }
          inQuotes = false; i++; continue;
        }
        field += ch; i++; continue;
      }
      if (ch === '"') { inQuotes = true; i++; continue; }
      if (ch === delim) { row.push(field); field = ""; i++; continue; }
      if (ch === "\r") { i++; continue; }
      if (ch === "\n") { row.push(field); rows.push(row); row = []; field = ""; i++; continue; }
      field += ch; i++;
    }
    if (field.length || row.length) { row.push(field); rows.push(row); }
    // drop a single trailing empty row from a trailing newline
    if (rows.length && rows[rows.length - 1].length === 1 && rows[rows.length - 1][0] === "") rows.pop();
    return rows;
  }

  function detectDelimiter(text) {
    const firstLine = text.split(/\r?\n/, 1)[0] || "";
    const candidates = [",", ";", "\t"];
    let best = ",", bestCount = -1;
    for (const c of candidates) {
      const count = firstLine.split(c).length - 1;
      if (count > bestCount) { bestCount = count; best = c; }
    }
    return best;
  }

  function coerce(value) {
    if (value === "") return "";
    if (/^-?\d+$/.test(value)) return parseInt(value, 10);
    if (/^-?\d*\.\d+$/.test(value)) return parseFloat(value);
    if (value === "true") return true;
    if (value === "false") return false;
    return value;
  }

  function convert() {
    const text = els.input.value;
    if (!text.trim()) {
      els.output.textContent = "";
      setResult(null, "");
      els.result.style.display = "none";
      return;
    }
    let delim = els.delimiter.value;
    if (delim === "auto") delim = detectDelimiter(text);
    else if (delim === "\\t") delim = "\t";

    const rows = parseCsv(text, delim);
    if (!rows.length) {
      setResult("error", "Couldn't find any rows to convert.");
      return;
    }

    let result;
    if (els.headerToggle.checked) {
      const headers = rows[0];
      result = rows.slice(1).map((r) => {
        const obj = {};
        headers.forEach((h, idx) => { obj[h || `col${idx + 1}`] = coerce(r[idx] ?? ""); });
        return obj;
      });
    } else {
      result = rows.map((r) => r.map(coerce));
    }

    const json = els.prettyToggle.checked ? JSON.stringify(result, null, 2) : JSON.stringify(result);
    els.output.textContent = json;
    setResult("ok", `Converted ${rows.length - (els.headerToggle.checked ? 1 : 0)} row(s) to JSON.`);
  }

  function loadText(text) {
    els.input.value = text;
    convert();
  }

  els.fileInput.addEventListener("change", () => {
    const file = els.fileInput.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => loadText(String(reader.result || ""));
    reader.readAsText(file);
  });
  els.drop.addEventListener("click", () => els.fileInput.click());
  wireDragDrop(els.drop, (e) => {
    const file = e.dataTransfer.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => loadText(String(reader.result || ""));
    reader.readAsText(file);
  });

  els.input.addEventListener("input", convert);
  els.delimiter.addEventListener("change", convert);
  els.headerToggle.addEventListener("change", convert);
  els.prettyToggle.addEventListener("change", convert);

  els.copyBtn.addEventListener("click", async () => {
    if (!els.output.textContent) return;
    try {
      await copyToClipboard(els.output.textContent);
      celebrateSuccess(els.copyBtn, els.output.parentElement, "Copied to clipboard");
    } catch (e) { /* clipboard unavailable */ }
  });

  els.downloadBtn.addEventListener("click", () => {
    if (!els.output.textContent) return;
    const blob = new Blob([els.output.textContent], { type: "application/json" });
    downloadBlob(blob, "data.json");
  });
})();
