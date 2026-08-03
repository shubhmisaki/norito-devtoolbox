import * as pdfjsLib from "./vendor/pdfjs/pdf.min.mjs";

pdfjsLib.GlobalWorkerOptions.workerSrc = new URL(
  "./vendor/pdfjs/pdf.worker.min.mjs",
  import.meta.url
).href;

(function () {
  const els = {
    dropA: document.getElementById("dropA"),
    dropB: document.getElementById("dropB"),
    fileInputA: document.getElementById("fileInputA"),
    fileInputB: document.getElementById("fileInputB"),
    fileInfoA: document.getElementById("fileInfoA"),
    fileInfoB: document.getElementById("fileInfoB"),
    loadingInfo: document.getElementById("loadingInfo"),
    errorBox: document.getElementById("errorBox"),
    diffStats: document.getElementById("diffStats"),
    diffOutput: document.getElementById("diffOutput"),
    emptyState: document.getElementById("emptyState"),
  };

  let fileA = null, fileB = null;
  let textA = null, textB = null;

  async function extractText(file) {
    const bytes = new Uint8Array(await file.arrayBuffer());
    const pdf = await pdfjsLib.getDocument({ data: bytes }).promise;
    const lines = [];
    for (let i = 1; i <= pdf.numPages; i++) {
      const page = await pdf.getPage(i);
      const content = await page.getTextContent();
      const text = content.items.map((it) => it.str).join(" ").replace(/\s+/g, " ").trim();
      lines.push(text);
    }
    return lines.join("\n");
  }

  function escapeHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function diffLines(aRaw, bRaw) {
    const aOrig = aRaw.split("\n");
    const bOrig = bRaw.split("\n");
    const n = aOrig.length, m = bOrig.length;
    const dp = new Array(n + 1);
    for (let i = 0; i <= n; i++) dp[i] = new Int32Array(m + 1);
    for (let i = n - 1; i >= 0; i--) {
      for (let j = m - 1; j >= 0; j--) {
        dp[i][j] = aOrig[i] === bOrig[j] ? dp[i + 1][j + 1] + 1 : Math.max(dp[i + 1][j], dp[i][j + 1]);
      }
    }
    const ops = [];
    let i = 0, j = 0;
    while (i < n && j < m) {
      if (aOrig[i] === bOrig[j]) { ops.push({ type: "equal", a: aOrig[i], b: bOrig[j] }); i++; j++; }
      else if (dp[i + 1][j] >= dp[i][j + 1]) { ops.push({ type: "remove", a: aOrig[i] }); i++; }
      else { ops.push({ type: "add", b: bOrig[j] }); j++; }
    }
    while (i < n) { ops.push({ type: "remove", a: aOrig[i] }); i++; }
    while (j < m) { ops.push({ type: "add", b: bOrig[j] }); j++; }
    return ops;
  }

  function renderDiff() {
    if (textA === null || textB === null) return;
    const ops = diffLines(textA, textB);
    let added = 0, removed = 0, unchanged = 0;
    let aLine = 1, bLine = 1;
    const rows = [];
    for (const op of ops) {
      if (op.type === "equal") {
        if (op.a) {
          rows.push('<div class="diff-row diff-equal"><span class="diff-ln">' + aLine + '</span><span class="diff-ln">' + bLine + '</span><span class="diff-marker"> </span><span class="diff-text">' + escapeHtml(op.a) + "</span></div>");
          unchanged++;
        }
        aLine++; bLine++;
      } else if (op.type === "remove") {
        if (op.a) {
          rows.push('<div class="diff-row diff-remove"><span class="diff-ln">' + aLine + '</span><span class="diff-ln"></span><span class="diff-marker">-</span><span class="diff-text">' + escapeHtml(op.a) + "</span></div>");
          removed++;
        }
        aLine++;
      } else {
        if (op.b) {
          rows.push('<div class="diff-row diff-add"><span class="diff-ln"></span><span class="diff-ln">' + bLine + '</span><span class="diff-marker">+</span><span class="diff-text">' + escapeHtml(op.b) + "</span></div>");
          added++;
        }
        bLine++;
      }
    }
    els.diffOutput.innerHTML = rows.join("");
    els.diffOutput.style.display = "block";
    els.diffStats.innerHTML =
      '<span class="diff-stat diff-stat-add">+' + added + " added</span>" +
      '<span class="diff-stat diff-stat-remove">-' + removed + " removed</span>" +
      '<span class="diff-stat diff-stat-equal">' + unchanged + " unchanged</span>";
    els.diffStats.style.display = "flex";
    els.emptyState.style.display = "none";
  }

  async function loadFile(which, file) {
    if (!file) return;
    if (file.type !== "application/pdf" && !/\.pdf$/i.test(file.name)) {
      els.errorBox.textContent = "That's not a PDF file.";
      els.errorBox.style.display = "block";
      return;
    }
    els.errorBox.style.display = "none";
    els.loadingInfo.style.display = "block";
    try {
      const text = await extractText(file);
      if (which === "A") {
        fileA = file; textA = text;
        els.fileInfoA.textContent = `${file.name} — ${formatBytes(file.size)}`;
      } else {
        fileB = file; textB = text;
        els.fileInfoB.textContent = `${file.name} — ${formatBytes(file.size)}`;
      }
      if (textA !== null && textB !== null) renderDiff();
    } catch (err) {
      els.errorBox.textContent = `Couldn't read "${file.name}". It may be password-protected or not a valid PDF.`;
      els.errorBox.style.display = "block";
    } finally {
      els.loadingInfo.style.display = "none";
    }
  }

  els.dropA.addEventListener("click", () => els.fileInputA.click());
  els.dropB.addEventListener("click", () => els.fileInputB.click());
  els.fileInputA.addEventListener("change", () => loadFile("A", els.fileInputA.files[0]));
  els.fileInputB.addEventListener("change", () => loadFile("B", els.fileInputB.files[0]));
  wireDragDrop(els.dropA, (e) => loadFile("A", e.dataTransfer.files && e.dataTransfer.files[0]));
  wireDragDrop(els.dropB, (e) => loadFile("B", e.dataTransfer.files && e.dataTransfer.files[0]));
})();
