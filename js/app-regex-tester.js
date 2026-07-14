(function () {
  const els = {
    pattern: document.getElementById("pattern"),
    flags: document.getElementById("flags"),
    testString: document.getElementById("testString"),
    highlighted: document.getElementById("highlighted"),
    result: document.getElementById("result"),
    matchesPanel: document.getElementById("matchesPanel"),
    matchesList: document.getElementById("matchesList"),
  };

  const ICONS = {
    ok: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="M22 4 12 14.01l-3-3"/></svg>',
    error: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>',
    neutral: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>',
  };

  function setResult(html, state) {
    if (!html) { els.result.style.display = "none"; return; }
    els.result.innerHTML = `<span class="r-icon">${ICONS[state] || ""}</span><span class="r-body">${html}</span>`;
    els.result.style.display = "flex";
    els.result.classList.remove("ok", "error");
    if (state) els.result.classList.add(state);
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  function run() {
    const patternSrc = els.pattern.value;
    const flagsSrc = els.flags.value.replace(/[^dgimsuy]/g, "");
    const text = els.testString.value;

    if (!patternSrc) {
      els.highlighted.innerHTML = escapeHtml(text) || '<span class="note">Matches will be highlighted here.</span>';
      els.matchesPanel.style.display = "none";
      setResult(null);
      return;
    }

    let re;
    try {
      // Force "g" so we can iterate every match, regardless of what the
      // user typed in the flags field, without changing what they see there.
      re = new RegExp(patternSrc, flagsSrc.includes("g") ? flagsSrc : flagsSrc + "g");
    } catch (e) {
      els.highlighted.innerHTML = escapeHtml(text);
      els.matchesPanel.style.display = "none";
      setResult(`<strong>Invalid regular expression.</strong> ${escapeHtml(e.message)}`, "error");
      return;
    }

    if (!text) {
      els.highlighted.innerHTML = '<span class="note">Matches will be highlighted here.</span>';
      els.matchesPanel.style.display = "none";
      setResult(null);
      return;
    }

    const matches = [];
    let m;
    let iterations = 0;
    let lastIndex = -1;
    while ((m = re.exec(text)) !== null && iterations < 5000) {
      iterations++;
      matches.push(m);
      if (m.index === re.lastIndex) re.lastIndex++; // avoid infinite loop on zero-length matches
      if (re.lastIndex === lastIndex) break;
      lastIndex = re.lastIndex;
    }

    // Build highlighted HTML by walking the original text and wrapping each
    // match span, so overlapping-looking output is impossible (JS regex
    // matches are inherently non-overlapping in a left-to-right scan).
    let html = "";
    let cursor = 0;
    for (const match of matches) {
      html += escapeHtml(text.slice(cursor, match.index));
      html += `<mark class="regex-match">${escapeHtml(match[0])}</mark>`;
      cursor = match.index + match[0].length;
    }
    html += escapeHtml(text.slice(cursor));
    els.highlighted.innerHTML = html || '<span class="note">Matches will be highlighted here.</span>';

    if (matches.length === 0) {
      els.matchesPanel.style.display = "none";
      setResult("<strong>No matches.</strong>", "neutral");
      return;
    }

    els.matchesList.innerHTML = matches.map((match, i) => {
      const groups = match.slice(1).filter((g) => g !== undefined);
      const groupsHtml = groups.length
        ? `<div class="match-groups">${groups.map((g, gi) => `<span class="match-group">Group ${gi + 1}: <code>${escapeHtml(g)}</code></span>`).join("")}</div>`
        : "";
      return `<div class="match-row"><span class="match-index">#${i + 1} at ${match.index}</span><code class="match-text">${escapeHtml(match[0])}</code>${groupsHtml}</div>`;
    }).join("");
    els.matchesPanel.style.display = "block";
    setResult(`<strong>${matches.length} match${matches.length === 1 ? "" : "es"} found.</strong>`, "ok");
  }

  [els.pattern, els.flags, els.testString].forEach((el) => el.addEventListener("input", run));
  run();
})();
