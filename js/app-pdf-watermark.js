(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    fileInfo: document.getElementById("fileInfo"),
    wmText: document.getElementById("wmText"),
    wmSize: document.getElementById("wmSize"),
    wmOpacity: document.getElementById("wmOpacity"),
    wmAngle: document.getElementById("wmAngle"),
    wmColor: document.getElementById("wmColor"),
    applyBtn: document.getElementById("applyBtn"),
    result: document.getElementById("result"),
  };

  const ICON_OK =
    '<svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>';
  const ICON_ERR =
    '<svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>';

  let currentFile = null;
  let currentBytes = null;
  let pageCount = 0;

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

  function hexToRgb01(hex) {
    const m = /^#?([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$/i.exec(hex || "");
    if (!m) return { r: 0.5, g: 0.5, b: 0.5 };
    return {
      r: parseInt(m[1], 16) / 255,
      g: parseInt(m[2], 16) / 255,
      b: parseInt(m[3], 16) / 255,
    };
  }

  const CONTROLS = [els.wmText, els.wmSize, els.wmOpacity, els.wmAngle, els.wmColor];

  function resetFileState() {
    currentFile = null;
    currentBytes = null;
    pageCount = 0;
    els.fileInfo.style.display = "none";
    CONTROLS.forEach((el) => { el.disabled = true; });
    els.applyBtn.disabled = true;
  }

  async function loadFile(file) {
    if (!file) return;
    if (file.type !== "application/pdf" && !/\.pdf$/i.test(file.name)) {
      setResult(
        `${ICON_ERR}<div class="r-body"><strong>That's not a PDF.</strong> Choose a .pdf file.</div>`,
        "error"
      );
      return;
    }
    els.result.style.display = "none";
    try {
      const bytes = await file.arrayBuffer();
      const doc = await PDFLib.PDFDocument.load(bytes);
      currentFile = file;
      currentBytes = bytes;
      pageCount = doc.getPageCount();
      els.fileInfo.textContent = `${file.name} — ${pageCount} page${pageCount === 1 ? "" : "s"}, ${formatBytes(file.size)}`;
      els.fileInfo.style.display = "block";
      CONTROLS.forEach((el) => { el.disabled = false; });
      els.applyBtn.disabled = false;
    } catch (err) {
      resetFileState();
      const msg = (err && err.message) || "";
      const reason = /encrypt/i.test(msg)
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

  const DEFAULT_LABEL = els.applyBtn.innerHTML;

  els.applyBtn.addEventListener("click", async () => {
    if (!currentBytes) return;
    els.applyBtn.disabled = true;
    els.applyBtn.textContent = "Adding...";
    let finishedOk = false;
    let outBlob = null;
    let outName = "";

    try {
      const text = els.wmText.value.trim();
      if (!text) throw new Error("Enter some watermark text first.");

      const size = parseInt(els.wmSize.value, 10);
      if (isNaN(size) || size < 8 || size > 200) throw new Error("Font size must be between 8 and 200.");

      const opacityPct = parseInt(els.wmOpacity.value, 10);
      if (isNaN(opacityPct) || opacityPct < 1 || opacityPct > 100) throw new Error("Opacity must be between 1 and 100.");

      const angle = parseInt(els.wmAngle.value, 10);
      if (isNaN(angle) || angle < -180 || angle > 180) throw new Error("Angle must be between -180 and 180.");

      const { r, g, b } = hexToRgb01(els.wmColor.value);

      const doc = await PDFLib.PDFDocument.load(currentBytes);
      const font = await doc.embedFont(PDFLib.StandardFonts.HelveticaBold);
      const textWidth = font.widthOfTextAtSize(text, size);
      const textHeight = font.heightAtSize(size);

      doc.getPages().forEach((page) => {
        const cx = page.getWidth() / 2;
        const cy = page.getHeight() / 2;
        page.drawText(text, {
          x: cx - textWidth / 2,
          y: cy - textHeight / 2,
          size,
          font,
          color: PDFLib.rgb(r, g, b),
          opacity: opacityPct / 100,
          rotate: PDFLib.degrees(angle),
        });
      });

      const outBytes = await doc.save();
      outBlob = new Blob([outBytes], { type: "application/pdf" });
      outName = `${baseName(currentFile.name)}-watermarked.pdf`;
      downloadBlob(outBlob, outName);

      setResult(
        `${ICON_OK}<div class="r-body"><strong>Created ${escapeHtml(outName)}</strong> ` +
          `(${pageCount} page${pageCount === 1 ? "" : "s"} watermarked, ${formatBytes(outBlob.size)}). ` +
          `Download started automatically.` +
          `<div><button type="button" id="dlAgainBtn" style="margin-top:12px;">Download again</button></div></div>`,
        "ok"
      );
      finishedOk = true;
    } catch (err) {
      setResult(
        `${ICON_ERR}<div class="r-body"><strong>Couldn't add the watermark.</strong> ${escapeHtml(err.message || "Something went wrong.")}</div>`,
        "error"
      );
    } finally {
      els.applyBtn.disabled = !currentBytes;
      els.applyBtn.innerHTML = DEFAULT_LABEL;
    }

    if (finishedOk) {
      const dlAgainBtn = document.getElementById("dlAgainBtn");
      if (dlAgainBtn && outBlob) {
        dlAgainBtn.addEventListener("click", () => downloadBlob(outBlob, outName));
      }
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
      celebrateSuccess(els.applyBtn, els.result);
    } else {
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  });
})();
