(function () {
  const els = {
    modeTabs: document.getElementById("mode-tabs"),
    mode: document.getElementById("mode"),
    indentSize: document.getElementById("indentSize"),
    input: document.getElementById("input"),
    output: document.getElementById("output"),
    errorBox: document.getElementById("errorBox"),
    swapBtn: document.getElementById("swapBtn"),
    copyBtn: document.getElementById("copyBtn"),
  };

  // ---------- YAML -> JS value ----------
  function stripComment(line) {
    let inSingle = false, inDouble = false;
    for (let i = 0; i < line.length; i++) {
      const ch = line[i];
      if (ch === "'" && !inDouble) inSingle = !inSingle;
      else if (ch === '"' && !inSingle) inDouble = !inDouble;
      else if (ch === "#" && !inSingle && !inDouble) {
        if (i === 0 || /\s/.test(line[i - 1])) return line.slice(0, i);
      }
    }
    return line;
  }

  function parseFlow(s) {
    try { return JSON.parse(s); } catch (e) {}
    let t = s
      .replace(/'/g, '"')
      .replace(/([{[,]\s*)([A-Za-z_][\w-]*)\s*:/g, '$1"$2":')
      .replace(/:\s*([A-Za-z_][\w-]*)\s*([,}\]])/g, ': "$1"$2');
    try { return JSON.parse(t); } catch (e) { return s; }
  }

  function parseScalar(raw) {
    let s = raw.trim();
    if (s === "") return null;
    if (/^(~|null|Null|NULL)$/.test(s)) return null;
    if (/^(true|True|TRUE)$/.test(s)) return true;
    if (/^(false|False|FALSE)$/.test(s)) return false;
    if (s.startsWith('"') && s.endsWith('"') && s.length >= 2) {
      try { return JSON.parse(s); } catch (e) { return s.slice(1, -1); }
    }
    if (s.startsWith("'") && s.endsWith("'") && s.length >= 2) {
      return s.slice(1, -1).replace(/''/g, "'");
    }
    if (s.startsWith("[") || s.startsWith("{")) return parseFlow(s);
    if (/^-?\d+$/.test(s)) return parseInt(s, 10);
    if (/^-?\d+\.\d+$/.test(s) || /^-?\d+(\.\d+)?e[+-]?\d+$/i.test(s)) return parseFloat(s);
    return s;
  }

  function isMapRow(text) {
    return /^("(?:[^"\\]|\\.)*"|'(?:[^']|'')*'|[^:]+):(\s|$)/.test(text);
  }

  function splitKeyValue(text) {
    const m = text.match(/^("(?:[^"\\]|\\.)*"|'(?:[^']|'')*'|[^:]+):\s?(.*)$/);
    if (!m) return [text, ""];
    let key = m[1].trim();
    if ((key.startsWith('"') && key.endsWith('"')) || (key.startsWith("'") && key.endsWith("'"))) {
      key = parseScalar(key);
    }
    return [key, m[2]];
  }

  function parseYAMLDocument(text) {
    const rawLines = text.split(/\r\n|\r|\n/);
    const rows = [];
    for (const raw of rawLines) {
      const noComment = stripComment(raw).replace(/\s+$/, "");
      const trimmed = noComment.trim();
      if (trimmed === "" || trimmed === "---" || trimmed === "...") continue;
      const indent = noComment.match(/^ */)[0].length;
      rows.push({ indent: indent, text: trimmed });
    }
    let pos = 0;
    function peek() { return pos < rows.length ? rows[pos] : null; }

    function parseNode(minIndent) {
      const row = peek();
      if (!row || row.indent < minIndent) return null;
      if (row.text === "-" || row.text.indexOf("- ") === 0) return parseSeq(row.indent);
      if (isMapRow(row.text)) return parseMap(row.indent);
      pos++;
      return parseScalar(row.text);
    }

    function parseMap(indent) {
      const obj = {};
      while (pos < rows.length && rows[pos].indent === indent && isMapRow(rows[pos].text)) {
        const row = rows[pos];
        const kv = splitKeyValue(row.text);
        const key = kv[0], rest = kv[1];
        pos++;
        if (rest.trim() === "") {
          const next = peek();
          obj[key] = next && next.indent > indent ? parseNode(next.indent) : null;
        } else {
          obj[key] = parseScalar(rest);
        }
      }
      return obj;
    }

    function consumeMapInto(obj, indent) {
      while (pos < rows.length && rows[pos].indent === indent && isMapRow(rows[pos].text)) {
        const row = rows[pos];
        const kv = splitKeyValue(row.text);
        const key = kv[0], rest = kv[1];
        pos++;
        if (rest.trim() === "") {
          const next = peek();
          obj[key] = next && next.indent > indent ? parseNode(next.indent) : null;
        } else {
          obj[key] = parseScalar(rest);
        }
      }
    }

    function parseSeq(indent) {
      const arr = [];
      while (pos < rows.length && rows[pos].indent === indent && (rows[pos].text === "-" || rows[pos].text.indexOf("- ") === 0)) {
        const row = rows[pos];
        const rest = row.text === "-" ? "" : row.text.slice(2);
        pos++;
        if (rest.trim() === "") {
          const next = peek();
          arr.push(next && next.indent > indent ? parseNode(next.indent) : null);
        } else if (isMapRow(rest)) {
          const virtualIndent = indent + 2;
          const kv = splitKeyValue(rest);
          const key = kv[0], kvRest = kv[1];
          const obj = {};
          if (kvRest.trim() === "") {
            const next = peek();
            obj[key] = next && next.indent > indent ? parseNode(next.indent) : null;
          } else {
            obj[key] = parseScalar(kvRest);
          }
          consumeMapInto(obj, virtualIndent);
          arr.push(obj);
        } else {
          arr.push(parseScalar(rest));
        }
      }
      return arr;
    }

    if (rows.length === 0) return null;
    return parseNode(rows[0].indent);
  }

  // ---------- JS value -> YAML ----------
  function yamlScalarString(s) {
    if (s === "") return '""';
    if (/^(true|false|null|~|-?\d+(\.\d+)?)$/i.test(s) || /[:#[\]{},&*!|>'"%@`]/.test(s) || /^\s|\s$/.test(s)) {
      return JSON.stringify(s);
    }
    return s;
  }

  function toYAML(value, indent) {
    indent = indent || 0;
    const pad = "  ".repeat(indent);
    if (value === null || value === undefined) return "null";
    if (typeof value === "boolean" || typeof value === "number") return String(value);
    if (typeof value === "string") return yamlScalarString(value);
    if (Array.isArray(value)) {
      if (value.length === 0) return "[]";
      return value.map(function (item) {
        if (item !== null && typeof item === "object") {
          const inner = toYAML(item, indent + 1);
          const lines = inner.split("\n");
          return pad + "- " + lines[0].trim() + (lines.length > 1 ? "\n" + lines.slice(1).join("\n") : "");
        }
        return pad + "- " + toYAML(item, 0);
      }).join("\n");
    }
    if (typeof value === "object") {
      const keys = Object.keys(value);
      if (keys.length === 0) return "{}";
      return keys.map(function (k) {
        const v = value[k];
        const keyStr = /^[A-Za-z_][\w-]*$/.test(k) ? k : yamlScalarString(k);
        const isNonEmptyObj = v !== null && typeof v === "object" && ((Array.isArray(v) && v.length) || (!Array.isArray(v) && Object.keys(v).length));
        if (isNonEmptyObj) return pad + keyStr + ":\n" + toYAML(v, indent + 1);
        return pad + keyStr + ": " + toYAML(v, 0);
      }).join("\n");
    }
    return String(value);
  }

  // ---------- UI wiring ----------
  function setMode(value) {
    els.mode.value = value;
    els.modeTabs.querySelectorAll(".tab").forEach(function (t) { t.classList.toggle("active", t.dataset.value === value); });
    els.input.placeholder = value === "json2yaml"
      ? 'Paste JSON, e.g. {"name": "norito", "free": true}'
      : "Paste YAML...";
    render();
  }
  els.modeTabs.addEventListener("click", function (e) {
    const btn = e.target.closest(".tab");
    if (btn) setMode(btn.dataset.value);
  });

  function render() {
    els.errorBox.style.display = "none";
    const raw = els.input.value;
    if (!raw.trim()) { els.output.value = ""; return; }
    const indentSize = parseInt(els.indentSize.value, 10) || 2;
    try {
      if (els.mode.value === "json2yaml") {
        const value = JSON.parse(raw);
        els.output.value = toYAML(value);
      } else {
        const value = parseYAMLDocument(raw);
        els.output.value = JSON.stringify(value, null, indentSize);
      }
    } catch (err) {
      els.output.value = "";
      els.errorBox.querySelector(".r-body").textContent = els.mode.value === "json2yaml"
        ? "That doesn't look like valid JSON: " + err.message
        : "Couldn't parse that as YAML: " + err.message;
      els.errorBox.style.display = "flex";
    }
  }

  els.input.addEventListener("input", render);
  els.indentSize.addEventListener("change", render);

  els.swapBtn.addEventListener("click", function () {
    const newMode = els.mode.value === "json2yaml" ? "yaml2json" : "json2yaml";
    const swapped = els.output.value;
    setMode(newMode);
    els.input.value = swapped;
    render();
  });

  els.copyBtn.addEventListener("click", async function () {
    if (!els.output.value) return;
    try {
      await copyToClipboard(els.output.value);
    } catch (err) {
      els.output.select();
      document.execCommand("copy");
    }
    showMascotToast("Copied!");
    celebrateSuccess(els.copyBtn);
  });

  render();
})();
