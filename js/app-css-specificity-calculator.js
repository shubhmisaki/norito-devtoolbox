(function () {
  const els = {
    input: document.getElementById("selInput"),
    results: document.getElementById("resultsWrap"),
    empty: document.getElementById("emptyState"),
  };

  // Split a selector list on top-level commas (not inside brackets).
  function splitSelectors(text) {
    return text
      .split("\n")
      .map((l) => l.trim())
      .filter(Boolean);
  }

  function score(selector) {
    let s = selector;
    // Strip strings inside [attr="value"] so their contents aren't tokenized.
    s = s.replace(/\[([^\]=]+)([~|^$*]?=)?("[^"]*"|'[^']*'|[^\]]*)\]/g, (m, attr) => `[${attr}]`);

    let ids = 0, classes = 0, elements = 0;

    // IDs
    ids += (s.match(/#[a-zA-Z0-9_-]+/g) || []).length;
    s = s.replace(/#[a-zA-Z0-9_-]+/g, "");

    // Attribute selectors count as classes
    classes += (s.match(/\[[^\]]*\]/g) || []).length;
    s = s.replace(/\[[^\]]*\]/g, "");

    // Pseudo-elements (::before, or legacy single-colon :before/:after/:first-line/:first-letter) count as elements
    const pseudoElements = ["before", "after", "first-line", "first-letter", "selection", "placeholder", "marker", "backdrop"];
    s = s.replace(/::?([a-zA-Z-]+)/g, (m, name) => {
      if (pseudoElements.includes(name.toLowerCase())) {
        elements += 1;
      } else {
        classes += 1;
      }
      return "";
    });

    // Classes
    classes += (s.match(/\.[a-zA-Z0-9_-]+/g) || []).length;
    s = s.replace(/\.[a-zA-Z0-9_-]+/g, "");

    // Remaining bare element/tag names (not combinators, not *, not whitespace)
    const tagMatches = s.match(/[a-zA-Z][a-zA-Z0-9-]*/g) || [];
    elements += tagMatches.length;

    return { ids, classes, elements };
  }

  function render() {
    const selectors = splitSelectors(els.input.value);
    if (!selectors.length) {
      els.results.innerHTML = "";
      els.empty.style.display = "block";
      return;
    }
    els.empty.style.display = "none";

    const scored = selectors.map((sel, i) => ({ sel, order: i, ...score(sel) }));
    scored.sort((a, b) => {
      if (a.ids !== b.ids) return b.ids - a.ids;
      if (a.classes !== b.classes) return b.classes - a.classes;
      if (a.elements !== b.elements) return b.elements - a.elements;
      return b.order - a.order; // later source order wins ties
    });

    els.results.innerHTML = scored
      .map(
        (s, rank) => `
      <div class="result-box" style="text-align:left; margin-bottom:10px;">
        <div style="display:flex; justify-content:space-between; align-items:baseline; gap:12px;">
          <code style="font-weight:600;">${escapeHtml(s.sel)}</code>
          <span class="note" style="white-space:nowrap;">#${rank + 1}</span>
        </div>
        <div class="note" style="margin-top:4px;">
          specificity (${s.ids}, ${s.classes}, ${s.elements}) &middot; ${s.ids} ID${s.ids === 1 ? "" : "s"},
          ${s.classes} class/attr/pseudo-class${s.classes === 1 ? "" : "es"}, ${s.elements} element${s.elements === 1 ? "" : "s"}
        </div>
      </div>`
      )
      .join("");
  }

  function escapeHtml(str) {
    const d = document.createElement("div");
    d.textContent = str;
    return d.innerHTML;
  }

  els.input.addEventListener("input", render);
  render();
})();
