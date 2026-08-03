(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    dropPanel: document.getElementById("dropPanel"),
    editorPanel: document.getElementById("editorPanel"),
    canvas: document.getElementById("annCanvas"),
    canvasWrap: document.getElementById("canvasWrap"),
    toolTabs: document.getElementById("toolTabs"),
    strokeColor: document.getElementById("strokeColor"),
    strokeWidth: document.getElementById("strokeWidth"),
    undoBtn: document.getElementById("undoBtn"),
    redoBtn: document.getElementById("redoBtn"),
    clearBtn: document.getElementById("clearBtn"),
    downloadBtn: document.getElementById("downloadBtn"),
  };
  const ctx = els.canvas.getContext("2d");

  let baseImg = null;
  let baseImgUrl = null;
  let shapes = [];
  let future = [];
  let currentTool = "arrow";
  let drawing = false;
  let startPt = null;
  let freehandPts = null;

  const MAX_DIM = 1800; // cap internal resolution for performance on huge screenshots

  function setButtons() {
    els.undoBtn.disabled = shapes.length === 0;
    els.redoBtn.disabled = future.length === 0;
  }

  function drawArrowHead(x1, y1, x2, y2, color, width) {
    const angle = Math.atan2(y2 - y1, x2 - x1);
    const headLen = Math.max(10, width * 3);
    ctx.beginPath();
    ctx.moveTo(x2, y2);
    ctx.lineTo(x2 - headLen * Math.cos(angle - Math.PI / 6), y2 - headLen * Math.sin(angle - Math.PI / 6));
    ctx.lineTo(x2 - headLen * Math.cos(angle + Math.PI / 6), y2 - headLen * Math.sin(angle + Math.PI / 6));
    ctx.closePath();
    ctx.fillStyle = color;
    ctx.fill();
  }

  function pixelateRect(x, y, w, h, blockSize) {
    const ix = Math.max(0, Math.round(x)), iy = Math.max(0, Math.round(y));
    const iw = Math.min(els.canvas.width - ix, Math.round(w));
    const ih = Math.min(els.canvas.height - iy, Math.round(h));
    if (iw <= 0 || ih <= 0) return;
    const imgData = ctx.getImageData(ix, iy, iw, ih);
    const data = imgData.data;
    const block = Math.max(4, blockSize);
    for (let by = 0; by < ih; by += block) {
      for (let bx = 0; bx < iw; bx += block) {
        let r = 0, g = 0, b = 0, a = 0, count = 0;
        const bw = Math.min(block, iw - bx), bh = Math.min(block, ih - by);
        for (let yy = 0; yy < bh; yy++) {
          for (let xx = 0; xx < bw; xx++) {
            const idx = ((by + yy) * iw + (bx + xx)) * 4;
            r += data[idx]; g += data[idx + 1]; b += data[idx + 2]; a += data[idx + 3];
            count++;
          }
        }
        r = Math.round(r / count); g = Math.round(g / count); b = Math.round(b / count); a = Math.round(a / count);
        for (let yy = 0; yy < bh; yy++) {
          for (let xx = 0; xx < bw; xx++) {
            const idx = ((by + yy) * iw + (bx + xx)) * 4;
            data[idx] = r; data[idx + 1] = g; data[idx + 2] = b; data[idx + 3] = a;
          }
        }
      }
    }
    ctx.putImageData(imgData, ix, iy);
  }

  function redraw() {
    ctx.drawImage(baseImg, 0, 0, els.canvas.width, els.canvas.height);
    shapes.forEach((s) => {
      if (s.type === "blur") {
        pixelateRect(s.x, s.y, s.w, s.h, 14);
        return;
      }
      ctx.strokeStyle = s.color;
      ctx.fillStyle = s.color;
      ctx.lineWidth = s.width;
      ctx.lineCap = "round";
      ctx.lineJoin = "round";
      if (s.type === "arrow") {
        ctx.beginPath();
        ctx.moveTo(s.x1, s.y1);
        ctx.lineTo(s.x2, s.y2);
        ctx.stroke();
        drawArrowHead(s.x1, s.y1, s.x2, s.y2, s.color, s.width);
      } else if (s.type === "rect") {
        ctx.strokeRect(Math.min(s.x1, s.x2), Math.min(s.y1, s.y2), Math.abs(s.x2 - s.x1), Math.abs(s.y2 - s.y1));
      } else if (s.type === "freehand") {
        ctx.beginPath();
        s.points.forEach((p, i) => (i === 0 ? ctx.moveTo(p.x, p.y) : ctx.lineTo(p.x, p.y)));
        ctx.stroke();
      } else if (s.type === "text") {
        ctx.font = `${s.width * 6 + 12}px sans-serif`;
        ctx.textBaseline = "top";
        ctx.fillText(s.text, s.x, s.y);
      }
    });
  }

  function commit(shape) {
    shapes.push(shape);
    future = [];
    setButtons();
    redraw();
  }

  function canvasPoint(e) {
    const rect = els.canvas.getBoundingClientRect();
    const scaleX = els.canvas.width / rect.width;
    const scaleY = els.canvas.height / rect.height;
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    return { x: (clientX - rect.left) * scaleX, y: (clientY - rect.top) * scaleY };
  }

  els.canvas.addEventListener("pointerdown", (e) => {
    if (!baseImg) return;
    const pt = canvasPoint(e);
    if (currentTool === "text") {
      const text = window.prompt("Text to add:");
      if (text) {
        commit({ type: "text", x: pt.x, y: pt.y, text, color: els.strokeColor.value, width: Number(els.strokeWidth.value) });
      }
      return;
    }
    drawing = true;
    startPt = pt;
    if (currentTool === "freehand") freehandPts = [pt];
    e.preventDefault();
  });

  els.canvas.addEventListener("pointermove", (e) => {
    if (!drawing || !baseImg) return;
    const pt = canvasPoint(e);
    redraw();
    ctx.strokeStyle = els.strokeColor.value;
    ctx.fillStyle = els.strokeColor.value;
    ctx.lineWidth = Number(els.strokeWidth.value);
    ctx.lineCap = "round";
    if (currentTool === "arrow") {
      ctx.beginPath();
      ctx.moveTo(startPt.x, startPt.y);
      ctx.lineTo(pt.x, pt.y);
      ctx.stroke();
      drawArrowHead(startPt.x, startPt.y, pt.x, pt.y, els.strokeColor.value, Number(els.strokeWidth.value));
    } else if (currentTool === "rect" || currentTool === "blur") {
      ctx.strokeRect(Math.min(startPt.x, pt.x), Math.min(startPt.y, pt.y), Math.abs(pt.x - startPt.x), Math.abs(pt.y - startPt.y));
    } else if (currentTool === "freehand") {
      freehandPts.push(pt);
      ctx.beginPath();
      freehandPts.forEach((p, i) => (i === 0 ? ctx.moveTo(p.x, p.y) : ctx.lineTo(p.x, p.y)));
      ctx.stroke();
    }
  });

  function endDraw(e) {
    if (!drawing || !baseImg) return;
    drawing = false;
    const pt = canvasPoint(e);
    const color = els.strokeColor.value;
    const width = Number(els.strokeWidth.value);
    if (currentTool === "arrow") {
      commit({ type: "arrow", x1: startPt.x, y1: startPt.y, x2: pt.x, y2: pt.y, color, width });
    } else if (currentTool === "rect") {
      commit({ type: "rect", x1: startPt.x, y1: startPt.y, x2: pt.x, y2: pt.y, color, width });
    } else if (currentTool === "blur") {
      commit({ type: "blur", x: Math.min(startPt.x, pt.x), y: Math.min(startPt.y, pt.y), w: Math.abs(pt.x - startPt.x), h: Math.abs(pt.y - startPt.y) });
    } else if (currentTool === "freehand" && freehandPts && freehandPts.length > 1) {
      commit({ type: "freehand", points: freehandPts, color, width });
    }
    freehandPts = null;
  }

  els.canvas.addEventListener("pointerup", endDraw);
  els.canvas.addEventListener("pointerleave", (e) => { if (drawing) endDraw(e); });

  els.toolTabs.querySelectorAll(".tab").forEach((btn) => {
    btn.addEventListener("click", () => {
      els.toolTabs.querySelectorAll(".tab").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      currentTool = btn.dataset.tool;
    });
  });

  els.undoBtn.addEventListener("click", () => {
    if (!shapes.length) return;
    future.push(shapes.pop());
    setButtons();
    redraw();
  });
  els.redoBtn.addEventListener("click", () => {
    if (!future.length) return;
    shapes.push(future.pop());
    setButtons();
    redraw();
  });
  els.clearBtn.addEventListener("click", () => {
    shapes = [];
    future = [];
    setButtons();
    redraw();
  });

  async function loadFile(file) {
    if (!file || !file.type.startsWith("image/")) return;
    try {
      const { img, url } = await loadImageFile(file);
      if (baseImgUrl) URL.revokeObjectURL(baseImgUrl);
      baseImg = img;
      baseImgUrl = url;
      let w = img.naturalWidth, h = img.naturalHeight;
      if (w > MAX_DIM || h > MAX_DIM) {
        const scale = MAX_DIM / Math.max(w, h);
        w = Math.round(w * scale);
        h = Math.round(h * scale);
      }
      els.canvas.width = w;
      els.canvas.height = h;
      shapes = [];
      future = [];
      setButtons();
      redraw();
      els.dropPanel.style.display = "none";
      els.editorPanel.style.display = "block";
    } catch (e) { /* couldn't read image, silently ignore */ }
  }

  els.fileInput.addEventListener("change", () => loadFile(els.fileInput.files[0]));
  wireDragDrop(els.drop, (e) => {
    const file = e.dataTransfer.files && e.dataTransfer.files[0];
    loadFile(file);
  });
  els.drop.addEventListener("click", (e) => {
    if (e.target === els.fileInput) return;
    els.fileInput.click();
  });

  els.downloadBtn.addEventListener("click", () => {
    if (!baseImg) return;
    els.canvas.toBlob((blob) => {
      if (blob) downloadBlob(blob, "annotated-screenshot.png");
    }, "image/png");
  });
})();
