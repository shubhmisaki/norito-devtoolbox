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
    undoBtn: document.getElementById("undoBtn"),
    redoBtn: document.getElementById("redoBtn"),
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

  // ---- unified undo/redo history: covers both typed text and toolbar
  // actions, since setting textarea.value programmatically (what the
  // toolbar buttons do) doesn't register on the browser's native undo
  // stack. Consecutive typing is coalesced into one step on a short pause,
  // so undo doesn't have to be replayed one keystroke at a time.
  const history = { stack: [], index: -1, max: 100 };
  let typingTimer = null;
  let suppressCapture = false;

  function snapshot() {
    return { value: els.editor.value, start: els.editor.selectionStart, end: els.editor.selectionEnd };
  }
  function updateUndoRedoButtons() {
    if (els.undoBtn) els.undoBtn.disabled = history.index <= 0;
    if (els.redoBtn) els.redoBtn.disabled = history.index >= history.stack.length - 1;
  }
  function pushHistory() {
    if (suppressCapture) return;
    const snap = snapshot();
    const top = history.stack[history.index];
    if (top && top.value === snap.value) return;
    history.stack = history.stack.slice(0, history.index + 1);
    history.stack.push(snap);
    if (history.stack.length > history.max) history.stack.shift();
    history.index = history.stack.length - 1;
    updateUndoRedoButtons();
  }
  function restoreSnapshot(snap) {
    suppressCapture = true;
    els.editor.value = snap.value;
    els.editor.focus();
    els.editor.setSelectionRange(snap.start, snap.end);
    render();
    suppressCapture = false;
    updateUndoRedoButtons();
  }
  function undo() {
    if (history.index <= 0) return;
    if (history.index === history.stack.length - 1) {
      const snap = snapshot();
      if (history.stack[history.index].value !== snap.value) history.stack.push(snap);
    }
    history.index -= 1;
    restoreSnapshot(history.stack[history.index]);
  }
  function redo() {
    if (history.index >= history.stack.length - 1) return;
    history.index += 1;
    restoreSnapshot(history.stack[history.index]);
  }
  history.stack = [snapshot()];
  history.index = 0;
  updateUndoRedoButtons();

  // Undo/redo buttons live inside #mdToolbar with data-action="undo"/"redo",
  // so the toolbar's delegated [data-action] click handler below already
  // routes clicks on them to undo()/redo() — no separate listener needed
  // here (adding one double-fires the action on every click).
  els.editor.addEventListener("keydown", (e) => {
    const mod = e.ctrlKey || e.metaKey;
    if (!mod) return;
    const key = e.key.toLowerCase();
    if (key === "z" && !e.shiftKey) { e.preventDefault(); undo(); }
    else if ((key === "z" && e.shiftKey) || key === "y") { e.preventDefault(); redo(); }
  });

  els.editor.addEventListener("input", () => {
    render();
    clearTimeout(typingTimer);
    typingTimer = setTimeout(pushHistory, 500);
  });
  els.editor.addEventListener("blur", () => { clearTimeout(typingTimer); pushHistory(); });

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
      if (btn.dataset.action === "undo") { undo(); return; }
      if (btn.dataset.action === "redo") { redo(); return; }
      const action = ACTIONS[btn.dataset.action];
      if (!action) return;
      clearTimeout(typingTimer);
      pushHistory(); // capture state right before this action
      action();
      pushHistory(); // capture state right after
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
