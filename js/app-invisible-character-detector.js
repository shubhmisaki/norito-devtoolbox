(function () {
  const els = {
    input: document.getElementById("textInput"),
    summary: document.getElementById("summaryWrap"),
    matches: document.getElementById("matchesWrap"),
    highlight: document.getElementById("highlightWrap"),
    cleanBtn: document.getElementById("cleanBtn"),
  };

  const NAMED = {
    0x200B: "Zero-width space",
    0x200C: "Zero-width non-joiner",
    0x200D: "Zero-width joiner",
    0x200E: "Left-to-right mark",
    0x200F: "Right-to-left mark",
    0x202A: "Left-to-right embedding",
    0x202B: "Right-to-left embedding",
    0x202C: "Pop directional formatting",
    0x202D: "Left-to-right override",
    0x202E: "Right-to-left override",
    0x2060: "Word joiner",
    0x2061: "Function application",
    0x2062: "Invisible times",
    0x2063: "Invisible separator",
    0x2064: "Invisible plus",
    0xFEFF: "Zero-width no-break space (BOM)",
    0x00AD: "Soft hyphen",
    0x034F: "Combining grapheme joiner",
    0x061C: "Arabic letter mark",
  };

  function isInvisible(cp) {
    if (NAMED[cp]) return NAMED[cp];
    if (cp >= 0xE0000 && cp <= 0xE007F) return "Unicode tag character (invisible ASCII smuggling range)";
    if (cp >= 0x2066 && cp <= 0x2069) return "Bidirectional isolate control";
    return null;
  }

  function scan(text) {
    const results = [];
    const chars = Array.from(text); // iterate by codepoint, not UTF-16 code unit
    let index = 0;
    for (const ch of chars) {
      const cp = ch.codePointAt(0);
      const label = isInvisible(cp);
      if (label) {
        results.push({ char: ch, cp, label, index });
      }
      index += ch.length;
    }
    return results;
  }

  function render() {
    const text = els.input.value;
    const hits = scan(text);

    if (!text) {
      els.summary.textContent = "No invisible characters found yet, paste text to scan.";
      els.matches.innerHTML = "";
      els.highlight.innerHTML = "";
      els.cleanBtn.disabled = true;
      return;
    }

    if (!hits.length) {
      els.summary.textContent = "Clean, no invisible or hidden Unicode characters detected.";
      els.matches.innerHTML = "";
      els.cleanBtn.disabled = true;
    } else {
      els.summary.textContent = `Found ${hits.length} invisible character${hits.length === 1 ? "" : "s"}.`;
      const counts = {};
      hits.forEach((h) => { counts[h.label] = (counts[h.label] || 0) + 1; });
      els.matches.innerHTML = Object.entries(counts)
        .map(
          ([label, count]) => `
        <div class="result-box" style="text-align:left; margin-bottom:8px; display:flex; justify-content:space-between; gap:12px;">
          <span>${escapeHtml(label)}</span>
          <code>&times;${count}</code>
        </div>`
        )
        .join("");
      els.cleanBtn.disabled = false;
    }

    // Highlighted view: wrap each invisible char in a visible marker
    const hitIndexes = new Set(hits.map((h) => h.index));
    let html = "";
    let i = 0;
    for (const ch of Array.from(text)) {
      if (hitIndexes.has(i)) {
        html += `<span style="background:var(--danger-bg, #fee2e2); color:var(--danger, #dc2626); border-radius:3px; padding:0 2px; font-weight:600;" title="U+${ch.codePointAt(0).toString(16).toUpperCase().padStart(4, "0")}">&#9679;</span>`;
      } else {
        html += escapeHtml(ch);
      }
      i += ch.length;
    }
    els.highlight.innerHTML = html;
  }

  function escapeHtml(str) {
    const d = document.createElement("div");
    d.textContent = str;
    return d.innerHTML;
  }

  els.input.addEventListener("input", render);
  render();

  els.cleanBtn.addEventListener("click", async () => {
    const cleaned = Array.from(els.input.value)
      .filter((ch) => !isInvisible(ch.codePointAt(0)))
      .join("");
    try {
      await copyToClipboard(cleaned);
      const I18N_C = i18nFor("common");
      showMascotToast(I18N_C.copied || "Copied!");
      celebrateSuccess(els.cleanBtn);
    } catch (e) { /* clipboard unavailable, silently ignore */ }
  });
})();
