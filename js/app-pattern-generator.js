(function () {
  const els = {
    type: document.getElementById("patType"),
    fg: document.getElementById("patFg"),
    bg: document.getElementById("patBg"),
    size: document.getElementById("patSize"),
    sizeVal: document.getElementById("patSizeVal"),
    thickness: document.getElementById("patThickness"),
    thicknessVal: document.getElementById("patThicknessVal"),
    opacity: document.getElementById("patOpacity"),
    opacityVal: document.getElementById("patOpacityVal"),
    preview: document.getElementById("preview"),
    output: document.getElementById("output"),
    copyBtn: document.getElementById("copyBtn"),
  };

  function hexToRgba(hex, alphaPct) {
    const h = hex.replace("#", "");
    const r = parseInt(h.substring(0, 2), 16);
    const g = parseInt(h.substring(2, 4), 16);
    const b = parseInt(h.substring(4, 6), 16);
    return `rgba(${r}, ${g}, ${b}, ${(alphaPct / 100).toFixed(2)})`;
  }

  function build() {
    const size = Number(els.size.value);
    const thickness = Number(els.thickness.value);
    const fg = hexToRgba(els.fg.value, Number(els.opacity.value));
    const bg = els.bg.value;
    const type = els.type.value;

    let css = "";

    if (type === "stripes") {
      css = `background: repeating-linear-gradient(45deg, ${fg} 0, ${fg} ${thickness}px, ${bg} ${thickness}px, ${bg} ${size}px);`;
    } else if (type === "stripesH") {
      css = `background: repeating-linear-gradient(0deg, ${fg} 0, ${fg} ${thickness}px, ${bg} ${thickness}px, ${bg} ${size}px);`;
    } else if (type === "dots") {
      const r = Math.max(1, thickness / 2);
      css = `background-color: ${bg};\nbackground-image: radial-gradient(${fg} ${r}px, transparent ${r}px);\nbackground-size: ${size}px ${size}px;`;
    } else if (type === "grid") {
      css = `background-color: ${bg};\nbackground-image:\n  linear-gradient(${fg} ${thickness}px, transparent ${thickness}px),\n  linear-gradient(90deg, ${fg} ${thickness}px, transparent ${thickness}px);\nbackground-size: ${size}px ${size}px;`;
    } else if (type === "checkerboard") {
      const half = size / 2;
      css = `background-color: ${bg};\nbackground-image:\n  linear-gradient(45deg, ${fg} 25%, transparent 25%, transparent 75%, ${fg} 75%, ${fg}),\n  linear-gradient(45deg, ${fg} 25%, transparent 25%, transparent 75%, ${fg} 75%, ${fg});\nbackground-size: ${size}px ${size}px;\nbackground-position: 0 0, ${half}px ${half}px;`;
    } else if (type === "crosshatch") {
      css = `background-color: ${bg};\nbackground-image:\n  repeating-linear-gradient(45deg, ${fg} 0, ${fg} ${thickness}px, transparent ${thickness}px, transparent ${size}px),\n  repeating-linear-gradient(-45deg, ${fg} 0, ${fg} ${thickness}px, transparent ${thickness}px, transparent ${size}px);`;
    }

    els.preview.style.cssText = css;
    els.output.textContent = css;
  }

  [els.type, els.fg, els.bg, els.size, els.thickness, els.opacity].forEach((el) =>
    el.addEventListener("input", () => {
      els.sizeVal.textContent = `${els.size.value}px`;
      els.thicknessVal.textContent = `${els.thickness.value}px`;
      els.opacityVal.textContent = `${els.opacity.value}%`;
      build();
    })
  );
  els.sizeVal.textContent = `${els.size.value}px`;
  els.thicknessVal.textContent = `${els.thickness.value}px`;
  els.opacityVal.textContent = `${els.opacity.value}%`;
  build();

  els.copyBtn.addEventListener("click", async () => {
    if (!els.output.textContent) return;
    try {
      await copyToClipboard(els.output.textContent);
      const I18N_C = i18nFor("common");
      showMascotToast(I18N_C.copied || "Copied!");
      celebrateSuccess(els.copyBtn);
    } catch (e) { /* clipboard unavailable, silently ignore */ }
  });
})();
