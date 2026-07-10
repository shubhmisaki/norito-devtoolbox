(function () {
  const I18N = i18nFor("app-markdown");
  const els = {
    editor: document.getElementById("mdEditor"),
    preview: document.getElementById("mdPreview"),
    charCount: document.getElementById("mdCharCount"),
    toolbar: document.getElementById("mdToolbar"),
    viewTabs: document.getElementById("view-tabs"),
    editorPane: document.getElementById("editorPane"),
    previewPane: document.getElementById("previewPane"),
    downloadMdBtn: document.getElementById("downloadMdBtn"),
    downloadHtmlBtn: document.getElementById("downloadHtmlBtn"),
  };

  if (window.marked && window.marked.setOptions) {
    window.marked.setOptions({ gfm: true, breaks: true });
  }

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  // Render never throws out to the caller: a bad paste or a missing library
  // used to freeze the preview and the character count with zero feedback,
  // which is what "the editor is broken" looks like from the outside.
  function render() {
    const md = els.editor.value;
    els.charCount.textContent = `${md.length} characters`;

    if (!window.marked || typeof window.marked.parse !== "function") {
      els.preview.innerHTML =
        '<div class="result-box error" style="margin:0 0 14px;">' +
        `<strong>${I18N.preview_unavailable || "Preview isn't available right now."}</strong> ` +
        (I18N.renderer_failed || "The markdown renderer didn't load. Check your connection and reload the page. Nothing you've typed is lost.") +
        "</div><pre style=\"white-space:pre-wrap; font-family:inherit;\">" + escapeHtml(md) + "</pre>";
      return;
    }

    try {
      els.preview.innerHTML = window.marked.parse(md);
    } catch (err) {
      console.error("Markdown render failed:", err);
      els.preview.innerHTML =
        '<div class="result-box error" style="margin:0;">' +
        `<strong>${I18N.render_failed_title || "Couldn't render this markdown."}</strong> ` + escapeHtml(err.message) +
        (I18N.render_failed_suffix || ". Try undoing your last change.") +
        "</div>";
    }
  }

  els.editor.addEventListener("input", render);

  // Toolbar: wrap or insert markdown syntax at the cursor.
  function applyWrap(prefix, suffix, placeholder) {
    const ta = els.editor;
    const start = ta.selectionStart;
    const end = ta.selectionEnd;
    const selected = ta.value.slice(start, end) || placeholder;
    const before = ta.value.slice(0, start);
    const after = ta.value.slice(end);
    ta.value = before + prefix + selected + suffix + after;
    const cursorStart = start + prefix.length;
    const cursorEnd = cursorStart + selected.length;
    ta.focus();
    ta.setSelectionRange(cursorStart, cursorEnd);
    render();
  }

  function applyLinePrefix(prefix) {
    const ta = els.editor;
    const start = ta.selectionStart;
    const lineStart = ta.value.lastIndexOf("\n", start - 1) + 1;
    ta.value = ta.value.slice(0, lineStart) + prefix + ta.value.slice(lineStart);
    ta.focus();
    ta.setSelectionRange(start + prefix.length, start + prefix.length);
    render();
  }

  const ACTIONS = {
    bold: () => applyWrap("**", "**", "bold text"),
    italic: () => applyWrap("_", "_", "italic text"),
    strike: () => applyWrap("~~", "~~", "strikethrough"),
    code: () => applyWrap("`", "`", "code"),
    codeblock: () => applyWrap("\n```\n", "\n```\n", "code block"),
    link: () => applyWrap("[", "](https://)", "link text"),
    h1: () => applyLinePrefix("# "),
    h2: () => applyLinePrefix("## "),
    quote: () => applyLinePrefix("> "),
    ul: () => applyLinePrefix("- "),
    ol: () => applyLinePrefix("1. "),
    table: () => applyWrap(
      "\n| Column A | Column B |\n| --- | --- |\n| ", " | value |\n", "value"
    ),
  };

  els.toolbar.querySelectorAll("[data-action]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const action = ACTIONS[btn.dataset.action];
      if (action) action();
    });
  });

  els.viewTabs.querySelectorAll(".tab").forEach((btn) => {
    btn.addEventListener("click", () => {
      els.viewTabs.querySelectorAll(".tab").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      const mode = btn.dataset.value;
      els.editorPane.style.display = mode === "preview" ? "none" : "block";
      els.previewPane.style.display = mode === "editor" ? "none" : "block";
    });
  });

  // Proportional scroll sync between panes.
  let syncing = false;
  function syncScroll(source, target) {
    if (syncing) return;
    syncing = true;
    const ratio = source.scrollTop / (source.scrollHeight - source.clientHeight || 1);
    target.scrollTop = ratio * (target.scrollHeight - target.clientHeight);
    requestAnimationFrame(() => { syncing = false; });
  }
  els.editor.addEventListener("scroll", () => syncScroll(els.editor, els.preview));
  els.preview.addEventListener("scroll", () => syncScroll(els.preview, els.editor));

  els.downloadMdBtn.addEventListener("click", () => {
    const blob = new Blob([els.editor.value], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "document.md";
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 2000);
    celebrateSuccess(els.downloadMdBtn);
  });

  els.downloadHtmlBtn.addEventListener("click", () => {
    const html = `<!DOCTYPE html>\n<html><head><meta charset="UTF-8"><title>Document</title></head><body>\n${els.preview.innerHTML}\n</body></html>`;
    const blob = new Blob([html], { type: "text/html" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "document.html";
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 2000);
    celebrateSuccess(els.downloadHtmlBtn);
  });

  render();
})();
