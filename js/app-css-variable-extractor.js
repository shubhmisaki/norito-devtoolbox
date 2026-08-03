(function () {
  const els = {
    input: document.getElementById("cssInput"),
    resultsWrap: document.getElementById("resultsWrap"),
    emptyState: document.getElementById("emptyState"),
    exportRow: document.getElementById("exportRow"),
    copyJsonBtn: document.getElementById("copyJsonBtn"),
    copyCssBtn: document.getElementById("copyCssBtn"),
    downloadCsvBtn: document.getElementById("downloadCsvBtn"),
  };

  let lastVars = []; // [{ name, value, selector }]

  // Splits CSS text into { selector, body } blocks via recursive brace
  // matching, including nested blocks (media/supports queries) which get
  // combined selector labels. Blocks whose body itself contains a nested
  // rule are recursed into rather than treated as declaration bodies.
  function extractBlocks(text) {
    // Strip comments first so brace-matching isn't confused by them.
    const clean = text.replace(/\/\*[\s\S]*?\*\//g, "");
    const blocks = [];

    function parse(str, parentSelector) {
      let i = 0;
      while (i < str.length) {
        const braceIdx = str.indexOf("{", i);
        if (braceIdx === -1) break;
        const selector = str.slice(i, braceIdx).trim().replace(/\s+/g, " ");
        let depth = 1;
        let j = braceIdx + 1;
        while (j < str.length && depth > 0) {
          if (str[j] === "{") depth++;
          else if (str[j] === "}") depth--;
          j++;
        }
        const body = str.slice(braceIdx + 1, j - 1);
        const label = parentSelector ? `${parentSelector} ${selector}` : selector;
        if (body.indexOf("{") !== -1) {
          parse(body, label); // nested rules (e.g. inside @media/@supports)
        } else {
          blocks.push({ selector: label, body });
        }
        i = j;
      }
    }

    parse(clean, "");
    return blocks;
  }

  function extractVariables(text) {
    const blocks = extractBlocks(text);
    const found = [];
    const declRe = /--([a-zA-Z0-9_-]+)\s*:\s*([^;]+);/g;
    blocks.forEach((block) => {
      let m;
      declRe.lastIndex = 0;
      while ((m = declRe.exec(block.body))) {
        found.push({ name: `--${m[1]}`, value: m[2].trim(), selector: block.selector || "(top level)" });
      }
    });
    return found;
  }

  function prefixOf(name) {
    const body = name.slice(2); // strip "--"
    const idx = body.indexOf("-");
    return idx === -1 ? body : body.slice(0, idx);
  }

  function escapeHtml(str) {
    const d = document.createElement("div");
    d.textContent = str;
    return d.innerHTML;
  }

  function render() {
    const vars = extractVariables(els.input.value);
    lastVars = vars;

    if (!vars.length) {
      els.resultsWrap.innerHTML = "";
      els.emptyState.style.display = "block";
      els.exportRow.style.display = "none";
      return;
    }
    els.emptyState.style.display = "none";
    els.exportRow.style.display = "flex";

    // Determine duplicates: same name, different values somewhere.
    const byName = new Map();
    vars.forEach((v) => {
      if (!byName.has(v.name)) byName.set(v.name, new Set());
      byName.get(v.name).add(v.value);
    });
    const dupNames = new Set(Array.from(byName.entries()).filter(([, vals]) => vals.size > 1).map(([n]) => n));

    // Group by prefix, unique names within each group (first occurrence).
    const groups = new Map();
    const seenNames = new Set();
    vars.forEach((v) => {
      if (seenNames.has(v.name)) return;
      seenNames.add(v.name);
      const p = prefixOf(v.name);
      if (!groups.has(p)) groups.set(p, []);
      groups.get(p).push(v);
    });

    const totalUnique = seenNames.size;
    const dupCount = dupNames.size;

    let html = `<p class="note" style="margin-bottom:12px;">${totalUnique} unique variable${totalUnique === 1 ? "" : "s"} across ${groups.size} group${groups.size === 1 ? "" : "s"}${dupCount ? `, <strong>${dupCount} with conflicting values</strong>` : ""}.</p>`;

    Array.from(groups.keys())
      .sort()
      .forEach((prefix) => {
        const items = groups.get(prefix);
        html += `<div style="margin-bottom:16px;">
          <h3 style="margin:0 0 6px; font-size:14px; text-transform:uppercase; letter-spacing:.04em; color:var(--muted);">${escapeHtml(prefix)} <span class="note">(${items.length})</span></h3>
          <table class="compare-table">
            <thead><tr><th>Name</th><th>Value</th><th>Selector</th></tr></thead>
            <tbody>
              ${items
                .map(
                  (v) => `<tr${dupNames.has(v.name) ? ' style="color:var(--danger, #dc2626);"' : ""}>
                <td><code>${escapeHtml(v.name)}</code>${dupNames.has(v.name) ? ' <span class="note" title="Declared with different values elsewhere">&#9888;</span>' : ""}</td>
                <td><code>${escapeHtml(v.value)}</code></td>
                <td class="note">${escapeHtml(v.selector)}</td>
              </tr>`
                )
                .join("")}
            </tbody>
          </table>
        </div>`;
      });

    els.resultsWrap.innerHTML = html;
  }

  els.input.addEventListener("input", render);
  render();

  function uniqueLatest() {
    // last-declared value wins per name, matching normal CSS cascade order
    const map = new Map();
    lastVars.forEach((v) => map.set(v.name, v.value));
    return map;
  }

  els.copyJsonBtn.addEventListener("click", async () => {
    const map = uniqueLatest();
    const obj = {};
    map.forEach((v, k) => (obj[k] = v));
    try {
      await copyToClipboard(JSON.stringify(obj, null, 2));
      flash(els.copyJsonBtn);
    } catch (e) { /* clipboard unavailable */ }
  });

  els.copyCssBtn.addEventListener("click", async () => {
    const map = uniqueLatest();
    const lines = Array.from(map.entries()).map(([k, v]) => `  ${k}: ${v};`);
    const css = `:root {\n${lines.join("\n")}\n}`;
    try {
      await copyToClipboard(css);
      flash(els.copyCssBtn);
    } catch (e) { /* clipboard unavailable */ }
  });

  els.downloadCsvBtn.addEventListener("click", () => {
    if (!lastVars.length) return;
    const header = "Name,Value,Selector\n";
    const rows = lastVars
      .map((v) => [v.name, v.value, v.selector].map((c) => `"${String(c).replace(/"/g, '""')}"`).join(","))
      .join("\n");
    downloadBlob(new Blob([header + rows], { type: "text/csv" }), "css-variables.csv");
  });

  function flash(btn) {
    const I18N_C = i18nFor("common");
    showMascotToast(I18N_C.copied || "Copied!");
    celebrateSuccess(btn);
  }
})();
