(function () {
  const els = {
    urlsInput: document.getElementById("urlsInput"),
    changefreq: document.getElementById("changefreq"),
    priority: document.getElementById("priority"),
    includeLastmod: document.getElementById("includeLastmod"),
    generateBtn: document.getElementById("generateBtn"),
    output: document.getElementById("output"),
    downloadBtn: document.getElementById("downloadBtn"),
    result: document.getElementById("result"),
  };

  const ICONS = {
    ok: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="M22 4 12 14.01l-3-3"/></svg>',
    error: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>',
  };

  function setResult(html, state) {
    if (!html) { els.result.style.display = "none"; return; }
    els.result.innerHTML = `<span class="r-icon">${ICONS[state] || ""}</span><span class="r-body">${html}</span>`;
    els.result.style.display = "flex";
    els.result.classList.remove("ok", "error");
    if (state) els.result.classList.add(state);
  }

  function escapeXml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&apos;");
  }

  function isValidUrl(s) {
    try { const u = new URL(s); return u.protocol === "http:" || u.protocol === "https:"; }
    catch (e) { return false; }
  }

  els.generateBtn.addEventListener("click", () => {
    const rawLines = els.urlsInput.value.split("\n").map((l) => l.trim()).filter(Boolean);
    const valid = rawLines.filter(isValidUrl);
    const invalid = rawLines.length - valid.length;

    if (valid.length === 0) {
      els.output.textContent = "";
      els.downloadBtn.disabled = true;
      setResult("<strong>No valid URLs found.</strong> Enter one full URL per line, including https://.", "error");
      return;
    }

    const today = new Date().toISOString().slice(0, 10);
    const freq = els.changefreq.value;
    const priority = els.priority.value;
    const includeLastmod = els.includeLastmod.checked;

    const entries = valid.map((url) => {
      const parts = [`  <url>`, `    <loc>${escapeXml(url)}</loc>`];
      if (includeLastmod) parts.push(`    <lastmod>${today}</lastmod>`);
      if (freq !== "none") parts.push(`    <changefreq>${freq}</changefreq>`);
      if (priority !== "none") parts.push(`    <priority>${priority}</priority>`);
      parts.push(`  </url>`);
      return parts.join("\n");
    });

    const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${entries.join("\n")}\n</urlset>\n`;
    els.output.textContent = xml;
    els.downloadBtn.disabled = false;

    const skippedNote = invalid > 0 ? ` ${invalid} line${invalid === 1 ? "" : "s"} skipped (not a valid http/https URL).` : "";
    setResult(`<strong>Generated a sitemap with ${valid.length} URL${valid.length === 1 ? "" : "s"}.</strong>${skippedNote}`, "ok");
  });

  els.downloadBtn.addEventListener("click", () => {
    if (!els.output.textContent) return;
    const blob = new Blob([els.output.textContent], { type: "application/xml" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "sitemap.xml";
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  });
})();
