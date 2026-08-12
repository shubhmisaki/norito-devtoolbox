(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    frameList: document.getElementById("frameList"),
    delayInput: document.getElementById("delayInput"),
    applyDelayBtn: document.getElementById("applyDelayBtn"),
    qualitySelect: document.getElementById("qualitySelect"),
    makeBtn: document.getElementById("makeBtn"),
    result: document.getElementById("result"),
    preview: document.getElementById("preview"),
  };

  let items = []; // [{ file, img, delay }]
  let strip = null;
  let busy = false;

  function setResult(html, state) {
    els.result.innerHTML = html;
    els.result.style.display = "block";
    els.result.className = "result-box " + (state || "");
  }

  function onStripChange() {
    els.makeBtn.disabled = items.length < 1;
  }

  function renderList() {
    if (!items.length) {
      els.frameList.style.display = "none";
      els.frameList.innerHTML = "";
      strip = null;
      els.makeBtn.disabled = true;
      return;
    }
    els.frameList.style.display = "flex";
    if (!strip) {
      strip = renderFrameStrip(els.frameList, items, {
        onChange: onStripChange,
        defaultDelay: Math.max(20, Number(els.delayInput.value) || 200),
      });
    } else {
      strip.refresh();
    }
    els.makeBtn.disabled = items.length < 1;
  }

  async function addFiles(fileList) {
    const files = Array.from(fileList).filter((f) => f.type.startsWith("image/"));
    if (!files.length) {
      setResult("<strong>Those don't look like images.</strong> Choose JPG, PNG, WebP, etc.", "error");
      return;
    }
    const delay = Math.max(20, Number(els.delayInput.value) || 200);
    for (const file of files) {
      try {
        const { img } = await loadImageFile(file);
        items.push({ file, img, delay });
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

  els.applyDelayBtn.addEventListener("click", () => {
    if (!items.length) return;
    bulkSetDelay(items, els.delayInput.value);
    if (strip) strip.refresh();
  });

  els.makeBtn.addEventListener("click", async () => {
    if (items.length < 1 || busy) return;
    busy = true;
    els.makeBtn.disabled = true;
    els.makeBtn.textContent = "Encoding...";
    els.result.style.display = "none";
    try {
      const width = items[0].img.naturalWidth || items[0].img.width;
      const height = items[0].img.naturalHeight || items[0].img.height;
      const quality = Number(els.qualitySelect.value) || 10;

      const frames = items.map((it) => {
        const canvas = document.createElement("canvas");
        canvas.width = width;
        canvas.height = height;
        canvas.getContext("2d").drawImage(it.img, 0, 0, width, height);
        return { canvas, delay: it.delay };
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
      busy = false;
      els.makeBtn.disabled = false;
      els.makeBtn.textContent = "Create GIF";
    }
  });
})();
