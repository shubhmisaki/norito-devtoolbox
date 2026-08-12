(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    frameList: document.getElementById("frameList"),
    delayInput: document.getElementById("delayInput"),
    qualitySelect: document.getElementById("qualitySelect"),
    makeBtn: document.getElementById("makeBtn"),
    result: document.getElementById("result"),
    preview: document.getElementById("preview"),
  };

  let items = []; // [{ file, img, url }]

  function setResult(html, state) {
    els.result.innerHTML = html;
    els.result.style.display = "block";
    els.result.className = "result-box " + (state || "");
  }

  function renderList() {
    if (!items.length) {
      els.frameList.style.display = "none";
      els.makeBtn.disabled = true;
      return;
    }
    els.frameList.style.display = "flex";
    els.frameList.style.flexWrap = "wrap";
    els.frameList.style.gap = "8px";
    els.frameList.innerHTML = items
      .map(
        (it, i) => `<div class="batch-file-row" data-i="${i}" style="display:flex; align-items:center; gap:8px; padding:6px 10px;">
          <span class="bf-name">${i + 1}. ${escapeHtml(it.file.name)}</span>
          <button type="button" class="bf-remove" data-i="${i}" aria-label="Remove">&times;</button>
        </div>`
      )
      .join("");
    els.frameList.querySelectorAll(".bf-remove").forEach((btn) => {
      btn.addEventListener("click", () => {
        const i = Number(btn.dataset.i);
        items.splice(i, 1);
        renderList();
      });
    });
    els.makeBtn.disabled = items.length < 1;
  }

  function escapeHtml(s) {
    return String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  async function addFiles(fileList) {
    const files = Array.from(fileList).filter((f) => f.type.startsWith("image/"));
    if (!files.length) {
      setResult("<strong>Those don't look like images.</strong> Choose JPG, PNG, WebP, etc.", "error");
      return;
    }
    for (const file of files) {
      try {
        const { img } = await loadImageFile(file);
        items.push({ file, img });
      } catch (e) {
        // skip files that fail to decode
      }
    }
    renderList();
  }

  els.fileInput.addEventListener("change", () => addFiles(els.fileInput.files));
  wireDragDrop(els.drop, (e) => addFiles(e.dataTransfer.files));
  els.drop.addEventListener("click", (e) => {
    if (e.target === els.fileInput) return;
    els.fileInput.click();
  });

  els.makeBtn.addEventListener("click", async () => {
    if (items.length < 1) return;
    els.makeBtn.disabled = true;
    els.makeBtn.textContent = "Encoding...";
    els.result.style.display = "none";
    try {
      const width = items[0].img.naturalWidth || items[0].img.width;
      const height = items[0].img.naturalHeight || items[0].img.height;
      const delay = Math.max(20, Number(els.delayInput.value) || 200);
      const quality = Number(els.qualitySelect.value) || 10;

      const frames = items.map((it) => {
        const canvas = document.createElement("canvas");
        canvas.width = width;
        canvas.height = height;
        canvas.getContext("2d").drawImage(it.img, 0, 0, width, height);
        return { canvas, delay };
      });

      const blob = await encodeGif(frames, {
        width,
        height,
        quality,
        onProgress: (f) => {
          els.makeBtn.textContent = `Encoding... ${Math.round(f * 100)}%`;
        },
      });

      const url = URL.createObjectURL(blob);
      els.preview.src = url;
      els.preview.style.display = "block";

      setResult(
        `<strong>GIF created.</strong> ${items.length} frames, ${formatBytes(blob.size)}.<br><br>` +
        `<button id="dlBtn">Download animation.gif</button>`,
        "ok"
      );
      document.getElementById("dlBtn").addEventListener("click", () => downloadBlob(blob, "animation.gif"));
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
      if (typeof celebrateSuccess === "function") celebrateSuccess(els.makeBtn, els.result);
    } catch (err) {
      setResult(`<strong>Couldn't create the GIF.</strong> ${err.message || "Try fewer or smaller images."}`, "error");
    } finally {
      els.makeBtn.disabled = false;
      els.makeBtn.textContent = "Create GIF";
    }
  });
})();
