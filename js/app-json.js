(function () {
  const I18N = i18nFor("app-json");
  const I18N_C = i18nFor("common");
  const els = {
    input: document.getElementById("jsonInput"),
    tabs: document.getElementById("view-tabs"),
    treeView: document.getElementById("treeView"),
    textOutput: document.getElementById("textOutput"),
    status: document.getElementById("status"),
    indent: document.getElementById("indentSize"),
    sortKeys: document.getElementById("optSortKeys"),
    minifyBtn: document.getElementById("minifyBtn"),
    formatBtn: document.getElementById("formatBtn"),
    copyBtn: document.getElementById("copyBtn"),
    downloadBtn: document.getElementById("downloadBtn"),
  };

  let currentView = "tree";
  let lastValid = null;

  function extractLineCol(text, pos) {
    const upTo = text.slice(0, pos);
    const lines = upTo.split("\n");
    return { line: lines.length, col: lines[lines.length - 1].length + 1 };
  }

  function parseSafe(text) {
    if (!text.trim()) return { ok: false, error: I18N.empty_input || "Empty input" };
    try {
      return { ok: true, data: JSON.parse(text) };
    } catch (e) {
      // Modern engines often already bake "(line N column M)" into the
      // message; older ones only give a raw character "position N". Only
      // compute our own line/col when the engine didn't already tell us.
      let msg = e.message;
      if (!/line \d+ column \d+/i.test(msg)) {
        const match = /position (\d+)/.exec(msg);
        if (match) {
          const { line, col } = extractLineCol(text, parseInt(match[1], 10));
          msg += fmt(I18N.line_col_suffix || " (line {line}, column {col})", { line, col });
        }
      }
      return { ok: false, error: msg };
    }
  }

  function sortKeysDeep(value) {
    if (Array.isArray(value)) return value.map(sortKeysDeep);
    if (value && typeof value === "object") {
      const out = {};
      Object.keys(value).sort().forEach((k) => { out[k] = sortKeysDeep(value[k]); });
      return out;
    }
    return value;
  }

  function typeLabel(v) {
    if (v === null) return "null";
    if (Array.isArray(v)) return "array";
    return typeof v;
  }

  function renderValue(v) {
    const t = typeLabel(v);
    const span = document.createElement("span");
    span.className = `jt-${t}`;
    if (t === "string") span.textContent = `"${v}"`;
    else if (t === "null") span.textContent = "null";
    else span.textContent = String(v);
    return span;
  }

  const MAX_ITEMS = 300;

  function renderNode(value, container) {
    const t = typeLabel(value);
    if (t !== "object" && t !== "array") {
      container.appendChild(renderValue(value));
      return;
    }

    const isArray = t === "array";
    const entries = isArray ? value.map((v, i) => [i, v]) : Object.entries(value);
    const wrap = document.createElement("div");
    wrap.className = "jt-node";

    const toggle = document.createElement("span");
    toggle.className = "jt-toggle";
    toggle.textContent = "▾";
    const bracketOpen = document.createElement("span");
    bracketOpen.className = "jt-bracket";
    bracketOpen.textContent = isArray ? "[" : "{";
    const count = document.createElement("span");
    count.className = "jt-count";
    count.textContent = ` ${entries.length} ${entries.length === 1 ? (I18N.item_singular || "item") : (I18N.item_plural || "items")}`;

    const head = document.createElement("div");
    head.className = "jt-head";
    head.appendChild(toggle);
    head.appendChild(bracketOpen);
    head.appendChild(count);
    wrap.appendChild(head);

    const body = document.createElement("div");
    body.className = "jt-body";

    entries.slice(0, MAX_ITEMS).forEach(([key, val]) => {
      const row = document.createElement("div");
      row.className = "jt-row";
      if (!isArray) {
        const keyEl = document.createElement("span");
        keyEl.className = "jt-key";
        keyEl.textContent = `"${key}": `;
        row.appendChild(keyEl);
      }
      renderNode(val, row);
      body.appendChild(row);
    });
    if (entries.length > MAX_ITEMS) {
      const more = document.createElement("div");
      more.className = "jt-row jt-more";
      more.textContent = fmt(I18N.more_items_not_shown || "… {n} more items not shown", { n: entries.length - MAX_ITEMS });
      body.appendChild(more);
    }

    const bracketClose = document.createElement("div");
    bracketClose.className = "jt-bracket";
    bracketClose.textContent = isArray ? "]" : "}";
    body.appendChild(bracketClose);

    wrap.appendChild(body);
    container.appendChild(wrap);

    toggle.addEventListener("click", () => {
      const collapsed = body.style.display === "none";
      body.style.display = collapsed ? "block" : "none";
      toggle.textContent = collapsed ? "▾" : "▸";
    });
  }

  function render() {
    const result = parseSafe(els.input.value);

    if (!result.ok) {
      els.status.textContent = result.error;
      els.status.className = "result-box error";
      els.status.style.display = "flex";
      els.treeView.innerHTML = "";
      els.textOutput.value = "";
      return;
    }

    els.status.style.display = "none";
    let data = result.data;
    if (els.sortKeys.checked) data = sortKeysDeep(data);
    lastValid = data;

    els.treeView.innerHTML = "";
    renderNode(data, els.treeView);

    const indent = els.indent.value === "tab" ? "\t" : parseInt(els.indent.value, 10);
    els.textOutput.value = JSON.stringify(data, null, indent);
  }

  els.input.addEventListener("input", render);
  els.indent.addEventListener("change", render);
  els.sortKeys.addEventListener("change", render);

  els.tabs.querySelectorAll(".tab").forEach((btn) => {
    btn.addEventListener("click", () => {
      els.tabs.querySelectorAll(".tab").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      currentView = btn.dataset.value;
      els.treeView.style.display = currentView === "tree" ? "block" : "none";
      els.textOutput.style.display = currentView === "text" ? "block" : "none";
    });
  });

  els.minifyBtn.addEventListener("click", () => {
    if (lastValid === undefined || lastValid === null) {
      const result = parseSafe(els.input.value);
      if (!result.ok) return;
      lastValid = result.data;
    }
    els.input.value = JSON.stringify(lastValid);
    render();
    celebrateSuccess(els.minifyBtn);
  });

  els.formatBtn.addEventListener("click", () => {
    const result = parseSafe(els.input.value);
    if (!result.ok) return;
    let data = result.data;
    if (els.sortKeys.checked) data = sortKeysDeep(data);
    const indent = els.indent.value === "tab" ? "\t" : parseInt(els.indent.value, 10);
    els.input.value = JSON.stringify(data, null, indent);
    render();
    celebrateSuccess(els.formatBtn);
  });

  els.copyBtn.addEventListener("click", async () => {
    const text = els.textOutput.value || els.input.value;
    try {
      await navigator.clipboard.writeText(text);
    } catch (e) {
      els.textOutput.select();
      document.execCommand("copy");
    }
    const original = els.copyBtn.textContent;
    els.copyBtn.textContent = I18N_C.copied || "Copied";
    setTimeout(() => { els.copyBtn.textContent = original; }, 1200);
  });

  els.downloadBtn.addEventListener("click", () => {
    const text = els.textOutput.value || els.input.value;
    if (!text) return;
    const blob = new Blob([text], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "formatted.json";
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 2000);
  });

  render();
})();
