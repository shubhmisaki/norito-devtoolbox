(function () {
  const I18N = i18nFor("app-slug");
  const I18N_C = i18nFor("common");
  const STOPWORDS = new Set([
    "a", "an", "the", "and", "or", "but", "of", "in", "on", "at", "to", "for",
    "with", "by", "from", "as", "is", "are", "was", "were", "be", "been",
    "being", "this", "that", "these", "those", "it", "its", "into", "than",
    "then", "so", "such", "not", "no", "nor", "if", "when", "while", "about",
    "over", "under", "again", "further", "once", "here", "there", "all",
    "both", "each", "few", "more", "most", "other", "some", "only", "own",
    "same", "too", "very",
  ]);

  const els = {
    batchToggle: document.getElementById("batchToggle"),
    singleWrap: document.getElementById("singleWrap"),
    batchWrap: document.getElementById("batchWrap"),
    input: document.getElementById("titleInput"),
    batchInput: document.getElementById("batchInput"),
    separator: document.getElementById("separator"),
    lowercase: document.getElementById("optLowercase"),
    removeStopwords: document.getElementById("optRemoveStopwords"),
    maxLength: document.getElementById("maxLength"),
    domain: document.getElementById("domainInput"),
    urlPreview: document.getElementById("urlSlugPreview"),
    output: document.getElementById("output"),
    charCount: document.getElementById("charCount"),
    copyBtn: document.getElementById("copyBtn"),
    batchResults: document.getElementById("batchResults"),
    copyAllBtn: document.getElementById("copyAllBtn"),
  };

  function slugify(text) {
    const sep = els.separator.value;
    let s = text.normalize("NFKD").replace(/[̀-ͯ]/g, "");
    if (els.lowercase.checked) s = s.toLowerCase();

    if (els.removeStopwords.checked) {
      const words = s.split(/\s+/).filter(Boolean);
      const filtered = words.filter((w) => !STOPWORDS.has(w.toLowerCase()));
      if (filtered.length) s = filtered.join(" ");
    }

    s = s.replace(/&/g, " and ");
    s = s.replace(/[^a-zA-Z0-9]+/g, sep);
    const escaped = sep.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    s = s.replace(new RegExp(`${escaped}{2,}`, "g"), sep);
    s = s.replace(new RegExp(`^${escaped}+|${escaped}+$`, "g"), "");

    const maxLen = parseInt(els.maxLength.value, 10);
    if (maxLen > 0 && s.length > maxLen) {
      s = s.slice(0, maxLen);
      const lastSep = s.lastIndexOf(sep);
      if (lastSep > maxLen * 0.6) s = s.slice(0, lastSep);
      s = s.replace(new RegExp(`${escaped}+$`), "");
    }

    return s;
  }

  function renderSingle() {
    const slug = slugify(els.input.value || "");
    els.output.value = slug;
    els.charCount.textContent = `${slug.length} characters`;
    els.urlPreview.textContent = slug || "your-slug-here";
  }

  function renderBatch() {
    const lines = (els.batchInput.value || "").split("\n").map((l) => l.trim()).filter(Boolean);
    els.batchResults.innerHTML = "";
    if (!lines.length) {
      els.batchResults.innerHTML = `<p class="note" style="margin:0;">${I18N.batch_empty_hint || "Paste titles above, one per line."}</p>`;
      return;
    }
    lines.forEach((line) => {
      const slug = slugify(line);
      const row = document.createElement("div");
      row.className = "slug-row";
      row.innerHTML = `
        <div class="slug-row-text">
          <div class="slug-row-title">${escapeHtml(line)}</div>
          <div class="slug-row-slug">${escapeHtml(slug)}</div>
        </div>
        <button type="button" class="secondary slug-copy">${I18N_C.copy_label || "Copy"}</button>
      `;
      row.querySelector(".slug-copy").addEventListener("click", (e) => {
        copyText(slug);
        e.target.textContent = I18N_C.copied || "Copied";
        setTimeout(() => { e.target.textContent = I18N_C.copy_label || "Copy"; }, 1200);
      });
      els.batchResults.appendChild(row);
    });
  }

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  async function copyText(text) {
    try {
      await navigator.clipboard.writeText(text);
    } catch (e) {
      const ta = document.createElement("textarea");
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      ta.remove();
    }
  }

  function renderAll() {
    if (els.batchToggle.checked) renderBatch();
    else renderSingle();
  }

  els.input.addEventListener("input", renderSingle);
  els.batchInput.addEventListener("input", renderBatch);
  [els.separator, els.lowercase, els.removeStopwords, els.maxLength].forEach((el) =>
    el.addEventListener("input", renderAll)
  );
  els.domain.addEventListener("input", () => {
    document.getElementById("urlDomainPreview").textContent = (els.domain.value || "yoursite.com").replace(/\/+$/, "") + "/";
  });

  els.batchToggle.addEventListener("change", () => {
    const isBatch = els.batchToggle.checked;
    els.singleWrap.style.display = isBatch ? "none" : "block";
    els.batchWrap.style.display = isBatch ? "block" : "none";
    renderAll();
  });

  els.copyBtn.addEventListener("click", () => {
    copyText(els.output.value);
    const original = els.copyBtn.textContent;
    els.copyBtn.textContent = I18N_C.copied || "Copied";
    setTimeout(() => { els.copyBtn.textContent = original; }, 1200);
  });

  els.copyAllBtn.addEventListener("click", () => {
    const lines = (els.batchInput.value || "").split("\n").map((l) => l.trim()).filter(Boolean);
    const slugs = lines.map(slugify).join("\n");
    copyText(slugs);
    const original = els.copyAllBtn.textContent;
    els.copyAllBtn.textContent = I18N.copied_all || "Copied all";
    setTimeout(() => { els.copyAllBtn.textContent = original; }, 1200);
  });

  renderSingle();
})();
