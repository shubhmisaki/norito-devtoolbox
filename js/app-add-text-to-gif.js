(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    controls: document.getElementById("controls"),
    originalInfo: document.getElementById("originalInfo"),
    captionPreviewWrap: document.getElementById("captionPreviewWrap"),
    captionPreviewImg: document.getElementById("captionPreviewImg"),
    captionsList: document.getElementById("captionsList"),
    addCaptionBtn: document.getElementById("addCaptionBtn"),
    applyBtn: document.getElementById("applyBtn"),
    cancelBtn: document.getElementById("cancelBtn"),
    frameList: document.getElementById("frameList"),
    result: document.getElementById("result"),
    preview: document.getElementById("preview"),
  };

  const FONTS = [
    ["sans-serif", "Sans-serif"],
    ["serif", "Serif"],
    ["monospace", "Monospace"],
    ["Impact, Haettenschweiler, 'Franklin Gothic Bold', sans-serif", "Impact (meme style)"],
    ["'Comic Sans MS', cursive", "Comic Sans"],
    ["Inter, sans-serif", "Inter"],
    ["Poppins, sans-serif", "Poppins (bold)"],
  ];

  let currentFile = null;
  let decoded = null;
  let strip = null;
  let captions = [];
  let busy = false; // true while rendering, so a mid-flight file swap can't pull the rug out
  let previewTimer = null;
  let activeGif = null;

  function setResult(html, state) {
    els.result.innerHTML = html;
    els.result.style.display = "block";
    els.result.className = "result-box " + (state || "");
  }

  els.cancelBtn.addEventListener("click", () => {
    if (activeGif) activeGif.abort();
    els.cancelBtn.disabled = true;
    els.cancelBtn.textContent = "Cancelling...";
  });

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  function makeCaption(frameCount, yOffset) {
    return {
      text: "",
      font: "sans-serif",
      size: 28,
      color: "#ffffff",
      outline: true,
      outlineColor: "#000000",
      outlineWidth: 3,
      bg: false,
      bgColor: "#000000",
      bgOpacity: 50,
      x: 0.5,
      y: Math.max(0.08, Math.min(0.92, 0.88 - (yOffset || 0))),
      startFrame: 0,
      endFrame: Math.max(0, frameCount - 1),
    };
  }

  /* ----------------------------------------------------------------
     Drawing: shared by the live preview and the final per-frame render
     so what you see while editing is exactly what gets exported.
     ---------------------------------------------------------------- */
  function drawCaption(ctx, width, height, cap) {
    const lines = cap.text.split("\n").filter((l) => l.length);
    if (!lines.length) return;
    ctx.font = `bold ${cap.size}px ${cap.font}`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    const lineHeight = cap.size * 1.25;
    const blockHeight = lines.length * lineHeight;
    const cx = cap.x * width;
    const cy = cap.y * height;
    const startY = cy - blockHeight / 2 + lineHeight / 2;

    if (cap.bg) {
      let maxW = 0;
      lines.forEach((l) => { maxW = Math.max(maxW, ctx.measureText(l).width); });
      const pad = cap.size * 0.35;
      ctx.save();
      ctx.globalAlpha = Math.max(0, Math.min(100, cap.bgOpacity)) / 100;
      ctx.fillStyle = cap.bgColor;
      ctx.fillRect(cx - maxW / 2 - pad, cy - blockHeight / 2 - pad, maxW + pad * 2, blockHeight + pad * 2);
      ctx.restore();
    }

    lines.forEach((line, i) => {
      const y = startY + i * lineHeight;
      if (cap.outline) {
        ctx.lineWidth = cap.outlineWidth;
        ctx.strokeStyle = cap.outlineColor;
        ctx.lineJoin = "round";
        ctx.strokeText(line, cx, y);
      }
      ctx.fillStyle = cap.color;
      ctx.fillText(line, cx, y);
    });
  }

  function schedulePreview() {
    clearTimeout(previewTimer);
    previewTimer = setTimeout(renderPreview, 60);
  }

  function renderPreview() {
    if (!decoded || !decoded.frames.length) return;
    const { width, height } = decoded;
    const canvas = document.createElement("canvas");
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(frameSourceEl(decoded.frames[0]), 0, 0, width, height);
    captions.forEach((cap) => {
      if (cap.startFrame <= 0 && cap.endFrame >= 0 && cap.text.trim()) drawCaption(ctx, width, height, cap);
    });
    els.captionPreviewImg.src = canvas.toDataURL("image/png");
    renderOverlayHandles();
  }

  function renderOverlayHandles() {
    els.captionPreviewWrap.querySelectorAll(".cap-handle").forEach((el) => el.remove());
    captions.forEach((cap, i) => {
      const handle = document.createElement("div");
      handle.className = "cap-handle";
      handle.textContent = String(i + 1);
      handle.style.cssText =
        `position:absolute; left:${cap.x * 100}%; top:${cap.y * 100}%; transform:translate(-50%,-50%); ` +
        `width:24px; height:24px; border-radius:50%; background:rgba(255,77,122,0.85); color:#fff; ` +
        `font-size:12px; font-weight:700; display:flex; align-items:center; justify-content:center; ` +
        `cursor:grab; touch-action:none; border:2px solid #fff; box-shadow:0 1px 4px rgba(0,0,0,0.35);`;
      wireHandleDrag(handle, cap);
      els.captionPreviewWrap.appendChild(handle);
    });
  }

  function wireHandleDrag(handle, cap) {
    handle.addEventListener("pointerdown", (e) => {
      e.preventDefault();
      handle.setPointerCapture(e.pointerId);
      handle.style.cursor = "grabbing";
      const move = (ev) => {
        const rect = els.captionPreviewWrap.getBoundingClientRect();
        const x = Math.max(0, Math.min(1, (ev.clientX - rect.left) / rect.width));
        const y = Math.max(0, Math.min(1, (ev.clientY - rect.top) / rect.height));
        cap.x = x;
        cap.y = y;
        handle.style.left = `${x * 100}%`;
        handle.style.top = `${y * 100}%`;
      };
      const up = () => {
        handle.style.cursor = "grab";
        handle.removeEventListener("pointermove", move);
        handle.removeEventListener("pointerup", up);
        renderPreview();
      };
      handle.addEventListener("pointermove", move);
      handle.addEventListener("pointerup", up);
    });
  }

  /* ----------------------------------------------------------------
     Caption panels: one per caption, mutating the caption object in
     place on every input (no full re-render mid-edit, same pattern as
     the frame strip's delay inputs), full re-render only on add/remove.
     ---------------------------------------------------------------- */
  function renderCaptionsList() {
    els.captionsList.innerHTML = "";
    captions.forEach((cap, i) => {
      const panel = document.createElement("div");
      panel.className = "panel";
      panel.style.cssText = "margin-top:10px; padding:12px;";
      panel.innerHTML = `
        <div class="field">
          <label>Caption ${i + 1} text</label>
          <textarea rows="2" class="cap-text" placeholder="Your caption...">${escapeHtml(cap.text)}</textarea>
        </div>
        <div class="two-col">
          <div class="field">
            <label>Font</label>
            <select class="cap-font">
              ${FONTS.map(([v, label]) => `<option value="${escapeHtml(v)}">${label}</option>`).join("")}
            </select>
          </div>
          <div class="field">
            <label>Font size (px)</label>
            <input type="number" class="cap-size" min="8" max="160" value="${cap.size}" />
          </div>
        </div>
        <div class="two-col">
          <div class="field">
            <label>Text color</label>
            <input type="color" class="cap-color" value="${cap.color}" />
          </div>
          <div class="field">
            <label class="checkbox-row" style="margin-top:24px;"><input type="checkbox" class="cap-outline" ${cap.outline ? "checked" : ""} /> Outline</label>
          </div>
        </div>
        <div class="field">
          <label class="checkbox-row"><input type="checkbox" class="cap-bg" ${cap.bg ? "checked" : ""} /> Background box</label>
        </div>
        <details class="cap-advanced">
          <summary>Advanced style (outline &amp; background box details)</summary>
          <div class="two-col cap-outline-fields" style="${cap.outline ? "" : "display:none;"} margin-top:10px;">
            <div class="field"><label>Outline color</label><input type="color" class="cap-outline-color" value="${cap.outlineColor}" /></div>
            <div class="field"><label>Outline width (px)</label><input type="number" class="cap-outline-width" min="1" max="20" value="${cap.outlineWidth}" /></div>
          </div>
          <div class="two-col cap-bg-fields" style="${cap.bg ? "" : "display:none;"} margin-top:10px;">
            <div class="field"><label>Box color</label><input type="color" class="cap-bg-color" value="${cap.bgColor}" /></div>
            <div class="field"><label>Box opacity (%)</label><input type="number" class="cap-bg-opacity" min="0" max="100" value="${cap.bgOpacity}" /></div>
          </div>
          <p class="note" style="margin-top:6px;">These only apply once Outline or Background box above is turned on.</p>
        </details>
        ${captions.length > 1 ? `
        <div class="two-col" style="margin-top:10px;">
          <div class="field"><label>Show from frame</label><input type="number" class="cap-start" min="1" max="${decoded.frames.length}" value="${cap.startFrame + 1}" /></div>
          <div class="field"><label>Show until frame</label><input type="number" class="cap-end" min="1" max="${decoded.frames.length}" value="${cap.endFrame + 1}" /></div>
        </div>
        <button type="button" class="cap-remove" style="margin-top:8px;">Remove this caption</button>` : ""}
      `;
      panel.querySelector(".cap-font").value = cap.font;
      wireCaptionPanel(panel, cap, i);
      els.captionsList.appendChild(panel);
    });
  }

  function wireCaptionPanel(panel, cap, i) {
    panel.querySelector(".cap-text").addEventListener("input", (e) => { cap.text = e.target.value; schedulePreview(); });
    panel.querySelector(".cap-font").addEventListener("change", (e) => { cap.font = e.target.value; schedulePreview(); });
    panel.querySelector(".cap-size").addEventListener("change", (e) => {
      cap.size = Math.max(8, Math.min(160, Number(e.target.value) || 28));
      e.target.value = cap.size;
      schedulePreview();
    });
    panel.querySelector(".cap-color").addEventListener("input", (e) => { cap.color = e.target.value; schedulePreview(); });

    const outlineFields = panel.querySelector(".cap-outline-fields");
    panel.querySelector(".cap-outline").addEventListener("change", (e) => {
      cap.outline = e.target.checked;
      outlineFields.style.display = cap.outline ? "" : "none";
      schedulePreview();
    });
    panel.querySelector(".cap-outline-color").addEventListener("input", (e) => { cap.outlineColor = e.target.value; schedulePreview(); });
    panel.querySelector(".cap-outline-width").addEventListener("change", (e) => {
      cap.outlineWidth = Math.max(1, Math.min(20, Number(e.target.value) || 3));
      e.target.value = cap.outlineWidth;
      schedulePreview();
    });

    const bgFields = panel.querySelector(".cap-bg-fields");
    panel.querySelector(".cap-bg").addEventListener("change", (e) => {
      cap.bg = e.target.checked;
      bgFields.style.display = cap.bg ? "" : "none";
      schedulePreview();
    });
    panel.querySelector(".cap-bg-color").addEventListener("input", (e) => { cap.bgColor = e.target.value; schedulePreview(); });
    panel.querySelector(".cap-bg-opacity").addEventListener("change", (e) => {
      cap.bgOpacity = Math.max(0, Math.min(100, Number(e.target.value) || 50));
      e.target.value = cap.bgOpacity;
      schedulePreview();
    });

    // Frame-range fields only exist in the DOM once there's more than one
    // caption (a single caption spans the whole GIF by default -- showing
    // "from frame 1 to frame N" for it would just be noise).
    const startInput = panel.querySelector(".cap-start");
    const endInput = panel.querySelector(".cap-end");
    if (startInput && endInput) {
      startInput.addEventListener("change", (e) => {
        const v = Math.max(1, Math.min(decoded.frames.length, Number(e.target.value) || 1));
        cap.startFrame = v - 1;
        if (cap.startFrame > cap.endFrame) cap.endFrame = cap.startFrame;
        e.target.value = cap.startFrame + 1;
        endInput.value = cap.endFrame + 1;
        schedulePreview();
      });
      endInput.addEventListener("change", (e) => {
        const v = Math.max(1, Math.min(decoded.frames.length, Number(e.target.value) || decoded.frames.length));
        cap.endFrame = v - 1;
        if (cap.endFrame < cap.startFrame) cap.startFrame = cap.endFrame;
        e.target.value = cap.endFrame + 1;
        startInput.value = cap.startFrame + 1;
        schedulePreview();
      });
    }

    const removeBtn = panel.querySelector(".cap-remove");
    if (removeBtn) {
      removeBtn.addEventListener("click", () => {
        captions.splice(i, 1);
        renderCaptionsList();
        renderPreview();
      });
    }
  }

  els.addCaptionBtn.addEventListener("click", () => {
    if (!decoded) return;
    captions.push(makeCaption(decoded.frames.length, captions.length * 0.14));
    renderCaptionsList();
    renderPreview();
  });

  async function handleFile(file) {
    if (busy) {
      setResult("<strong>Still rendering the previous GIF.</strong> Wait for it to finish first.", "error");
      return;
    }
    if (!file || !/image\/gif/.test(file.type)) {
      setResult("<strong>That's not a GIF.</strong> Choose a .gif file.", "error");
      return;
    }
    currentFile = file;
    els.result.style.display = "none";
    els.preview.style.display = "none";
    els.controls.style.display = "none";
    els.frameList.style.display = "none";
    els.frameList.innerHTML = "";
    setResult(`<strong>Reading ${file.name}...</strong>`, "");
    try {
      decoded = await decodeGifFile(file);
      els.result.style.display = "none";
      els.originalInfo.textContent =
        `${file.name}: ${decoded.width}×${decoded.height}, ${decoded.frames.length} frames, ${formatBytes(file.size)}`;
      els.controls.style.display = "block";
      els.frameList.style.display = "flex";
      // Thumbnails so you can drop a bad frame before captioning, but no
      // delay editing or reordering -- captioning doesn't touch timing.
      strip = renderFrameStrip(els.frameList, decoded.frames, {
        allowRemove: true, allowReorder: false, allowDelayEdit: false,
        onChange: () => {
          // Frame count may have shrunk; clamp existing caption ranges to it.
          captions.forEach((cap) => {
            cap.endFrame = Math.min(cap.endFrame, decoded.frames.length - 1);
            cap.startFrame = Math.min(cap.startFrame, cap.endFrame);
          });
          renderCaptionsList();
          schedulePreview();
        },
      });
      captions = [makeCaption(decoded.frames.length, 0)];
      renderCaptionsList();
      renderPreview();
    } catch (err) {
      setResult(`<strong>Couldn't read that GIF.</strong> ${err.message ? err.message + " " : ""}Try a different file.`, "error");
    }
  }

  els.fileInput.addEventListener("change", () => handleFile(els.fileInput.files[0]));
  wireDragDrop(els.drop, (e) => handleFile(e.dataTransfer.files[0]));
  els.drop.addEventListener("click", (e) => {
    if (e.target === els.fileInput) return;
    els.fileInput.click();
  });

  els.applyBtn.addEventListener("click", async () => {
    if (!decoded || busy) return;
    const activeCaptions = captions.filter((c) => c.text.trim().length);
    if (!activeCaptions.length) {
      setResult("<strong>Enter some caption text first.</strong>", "error");
      return;
    }

    busy = true;
    const busyText = startBusyText(els.applyBtn, "Rendering");
    els.cancelBtn.style.display = "inline-block";
    els.cancelBtn.disabled = false;
    els.cancelBtn.textContent = "Cancel";
    els.result.style.display = "none";

    try {
      const { width, height } = decoded;
      const frames = decoded.frames.map((f, idx) => {
        const canvas = document.createElement("canvas");
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(frameSourceEl(f), 0, 0, width, height);
        captions.forEach((cap) => {
          if (idx >= cap.startFrame && idx <= cap.endFrame && cap.text.trim()) drawCaption(ctx, width, height, cap);
        });
        return { canvas, delay: f.delay };
      });

      const blob = await encodeGif(frames, {
        width,
        height,
        quality: 10,
        onStart: (gif) => { activeGif = gif; },
        onProgress: (f) => busyText.update(f),
      });

      const url = URL.createObjectURL(blob);
      els.preview.src = url;
      els.preview.style.display = "block";

      setResult(
        `<strong>Caption${activeCaptions.length > 1 ? "s" : ""} added.</strong> ${formatBytes(blob.size)}.<br><br>` +
        `<button id="dlBtn">Download captioned.gif</button>`,
        "ok"
      );
      document.getElementById("dlBtn").addEventListener("click", () => downloadBlob(blob, "captioned.gif"));
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
      if (typeof celebrateSuccess === "function") celebrateSuccess(els.applyBtn, els.result);
    } catch (err) {
      if (err && err.cancelled) {
        setResult("<strong>Cancelled.</strong> No file was created.", "");
      } else {
        setResult(`<strong>Couldn't add that caption.</strong> ${err.message ? err.message + " " : ""}Try again.`, "error");
      }
    } finally {
      busy = false;
      activeGif = null;
      busyText.done();
      els.cancelBtn.style.display = "none";
    }
  });
})();
