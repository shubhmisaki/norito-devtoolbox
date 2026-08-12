(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    videoWrap: document.getElementById("videoWrap"),
    videoPreview: document.getElementById("videoPreview"),
    videoInfo: document.getElementById("videoInfo"),
    startInput: document.getElementById("startInput"),
    endInput: document.getElementById("endInput"),
    fpsSelect: document.getElementById("fpsSelect"),
    widthInput: document.getElementById("widthInput"),
    convertBtn: document.getElementById("convertBtn"),
    result: document.getElementById("result"),
    preview: document.getElementById("preview"),
  };

  const MAX_FRAMES = 300;
  let currentUrl = null;
  let videoDuration = 0;
  let videoW = 0, videoH = 0;

  function setResult(html, state) {
    els.result.innerHTML = html;
    els.result.style.display = "block";
    els.result.className = "result-box " + (state || "");
  }

  function handleFile(file) {
    if (!file || !file.type.startsWith("video/")) {
      setResult("<strong>That's not a video.</strong> Choose an MP4, WebM, or MOV file.", "error");
      return;
    }
    if (currentUrl) URL.revokeObjectURL(currentUrl);
    currentUrl = URL.createObjectURL(file);
    els.videoPreview.src = currentUrl;
    els.videoWrap.style.display = "block";
    els.result.style.display = "none";
    els.preview.style.display = "none";

    els.videoPreview.onloadedmetadata = () => {
      videoDuration = els.videoPreview.duration;
      videoW = els.videoPreview.videoWidth;
      videoH = els.videoPreview.videoHeight;
      els.videoInfo.textContent = `${file.name}, ${videoW}×${videoH}, ${videoDuration.toFixed(1)}s, ${formatBytes(file.size)}`;
      els.startInput.value = 0;
      els.endInput.value = Math.min(3, videoDuration).toFixed(1);
      els.endInput.max = videoDuration.toFixed(1);
    };
  }

  els.fileInput.addEventListener("change", () => handleFile(els.fileInput.files[0]));
  wireDragDrop(els.drop, (e) => handleFile(e.dataTransfer.files[0]));
  els.drop.addEventListener("click", (e) => {
    if (e.target === els.fileInput) return;
    els.fileInput.click();
  });

  function seekAndDraw(video, canvas, ctx, t) {
    return new Promise((resolve, reject) => {
      const onSeeked = () => {
        video.removeEventListener("seeked", onSeeked);
        try {
          ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
          resolve();
        } catch (err) {
          reject(err);
        }
      };
      video.addEventListener("seeked", onSeeked);
      video.currentTime = t;
    });
  }

  els.convertBtn.addEventListener("click", async () => {
    const start = Math.max(0, Number(els.startInput.value) || 0);
    const end = Math.min(videoDuration, Number(els.endInput.value) || 0);
    const fps = Number(els.fpsSelect.value) || 10;
    if (end <= start) {
      setResult("<strong>End time must be after start time.</strong>", "error");
      return;
    }

    let frameCount = Math.ceil((end - start) * fps);
    let effectiveFps = fps;
    if (frameCount > MAX_FRAMES) {
      effectiveFps = MAX_FRAMES / (end - start);
      frameCount = MAX_FRAMES;
    }

    const maxW = Math.max(80, Number(els.widthInput.value) || 480);
    const scale = Math.min(1, maxW / videoW);
    const outW = Math.round(videoW * scale);
    const outH = Math.round(videoH * scale);

    els.convertBtn.disabled = true;
    els.convertBtn.textContent = "Capturing frames...";
    els.result.style.display = "none";

    try {
      const canvas = document.createElement("canvas");
      canvas.width = outW;
      canvas.height = outH;
      const ctx = canvas.getContext("2d");
      const delay = Math.round(1000 / effectiveFps);
      const frames = [];

      els.videoPreview.pause();
      for (let i = 0; i < frameCount; i++) {
        const t = start + i / effectiveFps;
        await seekAndDraw(els.videoPreview, canvas, ctx, Math.min(t, videoDuration - 0.01));
        const frameCanvas = document.createElement("canvas");
        frameCanvas.width = outW;
        frameCanvas.height = outH;
        frameCanvas.getContext("2d").drawImage(canvas, 0, 0);
        frames.push({ canvas: frameCanvas, delay });
        els.convertBtn.textContent = `Capturing frames... ${i + 1}/${frameCount}`;
      }

      els.convertBtn.textContent = "Encoding...";
      const blob = await encodeGif(frames, {
        width: outW,
        height: outH,
        quality: 10,
        onProgress: (f) => { els.convertBtn.textContent = `Encoding... ${Math.round(f * 100)}%`; },
      });

      const url = URL.createObjectURL(blob);
      els.preview.src = url;
      els.preview.style.display = "block";

      setResult(
        `<strong>GIF created.</strong> ${frameCount} frames at ${Math.round(effectiveFps)} fps, ${formatBytes(blob.size)}.<br><br>` +
        `<button id="dlBtn">Download video.gif</button>`,
        "ok"
      );
      document.getElementById("dlBtn").addEventListener("click", () => downloadBlob(blob, "video.gif"));
      els.result.scrollIntoView({ behavior: "smooth", block: "center" });
      if (typeof celebrateSuccess === "function") celebrateSuccess(els.convertBtn, els.result);
    } catch (err) {
      setResult(`<strong>Couldn't convert that video.</strong> ${err.message || "Try a shorter range."}`, "error");
    } finally {
      els.convertBtn.disabled = false;
      els.convertBtn.textContent = "Convert to GIF";
    }
  });
})();
