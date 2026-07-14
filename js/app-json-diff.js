(function () {
  const els = {
    left: document.getElementById("leftInput"),
    right: document.getElementById("rightInput"),
    diffBtn: document.getElementById("diffBtn"),
    result: document.getElementById("result"),
    output: document.getElementById("diffOutput"),
  };

  const ICONS = {
    ok: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="M22 4 12 14.01l-3-3"/></svg>',
    error: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>',
    neutral: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>',
  };

  function setResult(html, state) {
    els.result.innerHTML = `<span class="r-icon">${ICONS[state] || ""}</span><span class="r-body">${html}</span>`;
    els.result.style.display = "flex";
    els.result.classList.remove("ok", "error");
    if (state) els.result.classList.add(state);
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  // Structural diff between two parsed JSON values, producing a flat list of
  // { path, type, before, after } entries. type is one of "added",
  // "removed", "changed". Recurses through plain objects and arrays;
  // anything else (including type mismatches) is compared by value.
  function diffValues(a, b, path, out) {
    const aIsObj = a !== null && typeof a === "object" && !Array.isArray(a);
    const bIsObj = b !== null && typeof b === "object" && !Array.isArray(b);
    const aIsArr = Array.isArray(a);
    const bIsArr = Array.isArray(b);

    if (aIsObj && bIsObj) {
      const keys = new Set([...Object.keys(a), ...Object.keys(b)]);
      for (const key of keys) {
        const p = path ? `${path}.${key}` : key;
        if (!(key in a)) out.push({ path: p, type: "added", after: b[key] });
        else if (!(key in b)) out.push({ path: p, type: "removed", before: a[key] });
        else diffValues(a[key], b[key], p, out);
      }
      return;
    }
    if (aIsArr && bIsArr) {
      const len = Math.max(a.length, b.length);
      for (let i = 0; i < len; i++) {
        const p = `${path}[${i}]`;
        if (i >= a.length) out.push({ path: p, type: "added", after: b[i] });
        else if (i >= b.length) out.push({ path: p, type: "removed", before: a[i] });
        else diffValues(a[i], b[i], p, out);
      }
      return;
    }
    // Leaf values (or mismatched types, e.g. object vs array vs primitive)
    const same = JSON.stringify(a) === JSON.stringify(b);
    if (!same) out.push({ path: path || "(root)", type: "changed", before: a, after: b });
  }

  function fmtValue(v) {
    if (v === undefined) return "undefined";
    if (typeof v === "string") return `"${v}"`;
    if (v !== null && typeof v === "object") return JSON.stringify(v);
    return String(v);
  }

  els.diffBtn.addEventListener("click", () => {
    let a, b;
    try {
      a = JSON.parse(els.left.value);
    } catch (e) {
      setResult(`<strong>Left side isn't valid JSON.</strong> ${escapeHtml(e.message)}`, "error");
      return;
    }
    try {
      b = JSON.parse(els.right.value);
    } catch (e) {
      setResult(`<strong>Right side isn't valid JSON.</strong> ${escapeHtml(e.message)}`, "error");
      return;
    }

    const diffs = [];
    diffValues(a, b, "", diffs);

    if (diffs.length === 0) {
      els.output.innerHTML = "";
      setResult("<strong>No differences.</strong> Both sides are structurally identical.", "ok");
      return;
    }

    const added = diffs.filter((d) => d.type === "added").length;
    const removed = diffs.filter((d) => d.type === "removed").length;
    const changed = diffs.filter((d) => d.type === "changed").length;

    els.output.innerHTML = diffs.map((d) => {
      if (d.type === "added") {
        return `<div class="diff-row diff-added"><span class="diff-tag">+ added</span><span class="diff-path">${escapeHtml(d.path)}</span><span class="diff-val">${escapeHtml(fmtValue(d.after))}</span></div>`;
      }
      if (d.type === "removed") {
        return `<div class="diff-row diff-removed"><span class="diff-tag">− removed</span><span class="diff-path">${escapeHtml(d.path)}</span><span class="diff-val">${escapeHtml(fmtValue(d.before))}</span></div>`;
      }
      return `<div class="diff-row diff-changed"><span class="diff-tag">~ changed</span><span class="diff-path">${escapeHtml(d.path)}</span><span class="diff-val">${escapeHtml(fmtValue(d.before))} <span class="diff-arrow">→</span> ${escapeHtml(fmtValue(d.after))}</span></div>`;
    }).join("");

    setResult(
      `<strong>${diffs.length} difference${diffs.length === 1 ? "" : "s"} found.</strong> ` +
      `${added} added, ${removed} removed, ${changed} changed.`,
      "neutral"
    );
  });
})();
