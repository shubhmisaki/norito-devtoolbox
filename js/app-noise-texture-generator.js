(function () {
  const els = {
    size: document.getElementById("noiseSize"),
    sizeVal: document.getElementById("noiseSizeVal"),
    density: document.getElementById("noiseDensity"),
    densityVal: document.getElementById("noiseDensityVal"),
    opacity: document.getElementById("noiseOpacity"),
    opacityVal: document.getElementById("noiseOpacityVal"),
    color: document.getElementById("noiseColor"),
    bg: document.getElementById("noiseBg"),
    mono: document.getElementById("noiseMono"),
    regenBtn: document.getElementById("regenBtn"),
    canvas: document.getElementById("noiseCanvas"),
    tiled: document.getElementById("tiledPreview"),
    downloadBtn: document.getElementById("downloadBtn"),
    copyCssBtn: document.getElementById("copyCssBtn"),
  };
  const ctx = els.canvas.getContext("2d");

  function hexToRgb(hex) {
    const h = hex.replace("#", "");
    return {
      r: parseInt(h.substring(0, 2), 16),
      g: parseInt(h.substring(2, 4), 16),
      b: parseInt(h.substring(4, 6), 16),
    };
  }

  function render() {
    const size = Number(els.size.value);
    const density = Number(els.density.value) / 100;
    const opacity = Number(els.opacity.value) / 100;
    const grainColor = hexToRgb(els.color.value);
    const bgColor = els.bg.value;
    const mono = els.mono.checked;

    els.sizeVal.textContent = `${size}px`;
    els.densityVal.textContent = `${els.density.value}%`;
    els.opacityVal.textContent = `${els.opacity.value}%`;

    els.canvas.width = size;
    els.canvas.height = size;

    ctx.fillStyle = bgColor;
    ctx.fillRect(0, 0, size, size);

    const imageData = ctx.getImageData(0, 0, size, size);
    const data = imageData.data;
    for (let i = 0; i < data.length; i += 4) {
      if (Math.random() > density) continue;
      const alpha = Math.random() * opacity;
      if (mono) {
        data[i] = grainColor.r;
        data[i + 1] = grainColor.g;
        data[i + 2] = grainColor.b;
      } else {
        const v = Math.floor(Math.random() * 255);
        data[i] = v;
        data[i + 1] = v;
        data[i + 2] = v;
      }
      // Blend the grain onto the existing background pixel by alpha.
      const bg = hexToRgb(bgColor);
      data[i] = Math.round(data[i] * alpha + bg.r * (1 - alpha));
      data[i + 1] = Math.round(data[i + 1] * alpha + bg.g * (1 - alpha));
      data[i + 2] = Math.round(data[i + 2] * alpha + bg.b * (1 - alpha));
      data[i + 3] = 255;
    }
    ctx.putImageData(imageData, 0, 0);

    const dataUrl = els.canvas.toDataURL("image/png");
    els.tiled.style.backgroundImage = `url(${dataUrl})`;
    els.tiled.style.backgroundRepeat = "repeat";
    els.tiled.style.backgroundSize = `${Math.min(size, 96)}px ${Math.min(size, 96)}px`;
  }

  [els.size, els.density, els.opacity, els.color, els.bg, els.mono].forEach((el) =>
    el.addEventListener("input", render)
  );
  els.regenBtn.addEventListener("click", render);
  render();

  els.downloadBtn.addEventListener("click", () => {
    els.canvas.toBlob((blob) => {
      if (blob) downloadBlob(blob, "noise-texture.png");
    }, "image/png");
  });

  els.copyCssBtn.addEventListener("click", async () => {
    const dataUrl = els.canvas.toDataURL("image/png");
    const css = `background-image: url("${dataUrl}");\nbackground-repeat: repeat;`;
    try {
      await copyToClipboard(css);
      const I18N_C = i18nFor("common");
      showMascotToast(I18N_C.copied || "Copied!");
      celebrateSuccess(els.copyCssBtn);
    } catch (e) { /* clipboard unavailable, silently ignore */ }
  });
})();
