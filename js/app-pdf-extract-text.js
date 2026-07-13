import * as pdfjsLib from "./vendor/pdfjs/pdf.min.mjs";

pdfjsLib.GlobalWorkerOptions.workerSrc = new URL(
  "./vendor/pdfjs/pdf.worker.min.mjs",
  import.meta.url
).href;

(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    fileInfo: document.getElementById("fileInfo"),
    loadingInfo: document.getElementById("loadingInfo"),
    markersRow: document.getElementById("markersRow"),
    pageMarkers: document.getElementById("pageMarkers"),
    previewField: document.getElementById("previewField"),
    textOutput: document.getElementById("textOutput"),
    actionsRow: document.getElementById("actionsRow"),
    copyBtn: document.getElementById("copyBtn"),
    downloadBtn: document.getElementById("downloadBtn"),
    result: document.getElementById("result"),
  };

  const ICON_ERR =
    '<svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>';

  let currentFile = null;
  let pageTexts = []; // array of per-page extracted text, index 0 = page 1

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    }[c]));
  }

  function baseName(filename) {
    return filename.replace(/\.pdf$/i, "") || "document";
  }

  function setResult(html, state) {
    els.result.innerHTML = html;
    els.result.style.display = "flex";
    els.result.classList.remove("ok", "error");
    if (state) els.result.classList.add(state);
  }

  function resetState() {
    currentFile = null;
    pageTexts = [];
    els.fileInfo.style.display = "none";
    els.loadingInfo.style.display = "none";
    els.markersRow.style.display = "none";
    els.previewField.style.display = "none";
    els.actionsRow.style.display = "none";
    els.textOutput.value = "";
  }

  function renderOutput() {
    const withMarkers = els.pageMarkers.checked;
    const parts = pageTexts.map((text, i) =>
      withMarkers ? `--- Page ${i + 1} ---\n${text}` : text
    );
    els.textOutput.value = parts.join("\n\n").trim();
  }
  els.pageMarkers.addEventListener("change", renderOutput);

  async function loadFile(file) {
    if (!file) return;
    if (file.type !== "application/pdf" && !/\.pdf$/i.test(file.name)) {
      setResult(
        `${ICON_ERR}<div class="r-body"><strong>That's not a PDF.</strong> Choose a .pdf file.</div>`,
        "error"
      );
      return;
    }
    resetState();
    els.result.style.display = "none";
    try {
      const bytes = new Uint8Array(await file.arrayBuffer());
      const pdf = await pdfjsLib.getDocument({ data: bytes }).promise;
      currentFile = file;

      els.fileInfo.textContent = `${file.name} — ${pdf.numPages} page${pdf.numPages === 1 ? "" : "s"}, ${formatBytes(file.size)}`;
      els.fileInfo.style.display = "block";
      els.loadingInfo.style.display = "block";

      pageTexts = [];
      for (let i = 1; i <= pdf.numPages; i++) {
        const page = await pdf.getPage(i);
        const content = await page.getTextContent();
        const text = content.items.map((it) => it.str).join(" ").replace(/\s+/g, " ").trim();
        pageTexts.push(text);
      }

      els.loadingInfo.style.display = "none";
      els.markersRow.style.display = "flex";
      els.previewField.style.display = "block";
      els.actionsRow.style.display = "flex";
      renderOutput();

      const totalChars = pageTexts.reduce((a, t) => a + t.length, 0);
      if (totalChars === 0) {
        setResult(
          `${ICON_ERR}<div class="r-body"><strong>No text found.</strong> This PDF might be a scanned document with no embedded text (an image, not real text).</div>`,
          "error"
        );
      }
    } catch (err) {
      resetState();
      const isPassword = err && err.name === "PasswordException";
      const reason = isPassword
        ? "It's password protected, remove the password first."
        : "It doesn't look like a valid PDF.";
      setResult(
        `${ICON_ERR}<div class="r-body"><strong>Couldn't read "${escapeHtml(file.name)}".</strong> ${reason}</div>`,
        "error"
      );
    }
  }

  els.drop.addEventListener("click", () => els.fileInput.click());
  els.fileInput.addEventListener("change", () => {
    loadFile(els.fileInput.files[0]);
    els.fileInput.value = "";
  });

  ["dragenter", "dragover"].forEach((evt) =>
    els.drop.addEventListener(evt, (e) => {
      e.preventDefault();
      els.drop.classList.add("drag");
    })
  );
  ["dragleave", "drop"].forEach((evt) =>
    els.drop.addEventListener(evt, (e) => {
      e.preventDefault();
      els.drop.classList.remove("drag");
    })
  );
  els.drop.addEventListener("drop", (e) => {
    if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]) {
      loadFile(e.dataTransfer.files[0]);
    }
  });

  els.copyBtn.addEventListener("click", async () => {
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(els.textOutput.value);
      } else {
        els.textOutput.select();
        document.execCommand("copy");
      }
      celebrateSuccess(els.copyBtn, null, "Copied!");
    } catch (err) {
      setResult(
        `${ICON_ERR}<div class="r-body"><strong>Couldn't copy to clipboard.</strong> Select the text manually instead.</div>`,
        "error"
      );
    }
  });

  els.downloadBtn.addEventListener("click", () => {
    const blob = new Blob([els.textOutput.value], { type: "text/plain;charset=utf-8" });
    downloadBlob(blob, `${baseName(currentFile ? currentFile.name : "document")}.txt`);
    celebrateSuccess(els.downloadBtn, null);
  });
})();
