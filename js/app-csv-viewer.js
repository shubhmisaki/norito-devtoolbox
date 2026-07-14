(function () {
  const ICONS = {
    ok: '<svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>',
    error: '<svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m15 9-6 6M9 9l6 6"/></svg>',
  };

  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    tableWrap: document.getElementById("tableWrap"),
    addRowBtn: document.getElementById("addRowBtn"),
    addColBtn: document.getElementById("addColBtn"),
    downloadBtn: document.getElementById("downloadBtn"),
    result: document.getElementById("result"),
  };

  function setResult(kind, html) {
    if (!els.result) return;
    els.result.style.display = "flex";
    els.result.className = "result-box " + (kind || "");
    els.result.innerHTML = (kind === "ok" ? ICONS.ok : kind === "error" ? ICONS.error : "") + `<div class="r-body">${html}</div>`;
  }

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

  function serializeCsv(data) {
    return data
      .map((row) =>
        row
          .map((cell) => {
            const s = String(cell ?? "");
            return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
          })
          .join(",")
      )
      .join("\r\n");
  }

  let data = []; // array of arrays, first row = headers

  function render() {
    if (!data.length) {
      els.tableWrap.innerHTML = "";
      els.tableWrap.style.display = "none";
      return;
    }
    els.tableWrap.style.display = "block";
    const headers = data[0];
    const body = data.slice(1);
    let html = '<table class="csv-table"><thead><tr>';
    headers.forEach((h, c) => {
      html += `<th><input type="text" value="${escapeAttr(h)}" data-r="0" data-c="${c}" /></th>`;
    });
    html += "</tr></thead><tbody>";
    body.forEach((row, r) => {
      html += "<tr>";
      headers.forEach((_, c) => {
        html += `<td><input type="text" value="${escapeAttr(row[c] ?? "")}" data-r="${r + 1}" data-c="${c}" /></td>`;
      });
      html += "</tr>";
    });
    html += "</tbody></table>";
    els.tableWrap.innerHTML = html;

    els.tableWrap.querySelectorAll("input").forEach((input) => {
      input.addEventListener("input", () => {
        const r = Number(input.dataset.r), c = Number(input.dataset.c);
        if (!data[r]) data[r] = [];
        data[r][c] = input.value;
      });
    });
  }

  function escapeAttr(s) {
    return String(s ?? "").replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");
  }

  function loadText(text) {
    const delim = detectDelimiter(text);
    const rows = parseCsv(text, delim);
    if (!rows.length) {
      setResult("error", "Couldn't find any rows in that file.");
      return;
    }
    data = rows;
    render();
    setResult("ok", `Loaded ${rows.length} row(s) (including header). Edit any cell directly.`);
  }

  els.fileInput.addEventListener("change", () => {
    const file = els.fileInput.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => loadText(String(reader.result || ""));
    reader.readAsText(file);
  });
  els.drop.addEventListener("click", () => els.fileInput.click());
  els.drop.addEventListener("dragover", (e) => { e.preventDefault(); els.drop.classList.add("drag"); });
  els.drop.addEventListener("dragleave", () => els.drop.classList.remove("drag"));
  els.drop.addEventListener("drop", (e) => {
    e.preventDefault();
    els.drop.classList.remove("drag");
    const file = e.dataTransfer.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => loadText(String(reader.result || ""));
    reader.readAsText(file);
  });

  els.addRowBtn.addEventListener("click", () => {
    if (!data.length) { setResult("error", "Load a CSV file first."); return; }
    data.push(data[0].map(() => ""));
    render();
  });
  els.addColBtn.addEventListener("click", () => {
    if (!data.length) { setResult("error", "Load a CSV file first."); return; }
    data.forEach((row, i) => row.push(i === 0 ? `column${data[0].length + 1}` : ""));
    render();
  });
  els.downloadBtn.addEventListener("click", () => {
    if (!data.length) return;
    const blob = new Blob([serializeCsv(data)], { type: "text/csv" });
    downloadBlob(blob, "edited.csv");
    celebrateSuccess(els.downloadBtn, els.tableWrap, "Downloaded");
  });
})();
