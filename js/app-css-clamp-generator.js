(function () {
  const els = {
    minSize: document.getElementById("minSize"),
    minVp: document.getElementById("minVp"),
    maxSize: document.getElementById("maxSize"),
    maxVp: document.getElementById("maxVp"),
    rootFont: document.getElementById("rootFont"),
    preview: document.getElementById("previewText"),
    output: document.getElementById("output"),
    copyBtn: document.getElementById("copyBtn"),
  };

  function update() {
    const minSize = Number(els.minSize.value);
    const minVp = Number(els.minVp.value);
    const maxSize = Number(els.maxSize.value);
    const maxVp = Number(els.maxVp.value);
    const root = Number(els.rootFont.value) || 16;

    if (!minSize || !minVp || !maxSize || !maxVp || maxVp === minVp) {
      els.output.textContent = "// Enter valid, non-equal viewport widths.";
      return;
    }

    const slope = (maxSize - minSize) / (maxVp - minVp);
    const intercept = minSize - slope * minVp;

    const minRem = (minSize / root).toFixed(3).replace(/\.?0+$/, "");
    const maxRem = (maxSize / root).toFixed(3).replace(/\.?0+$/, "");
    const interceptRem = (intercept / root).toFixed(3).replace(/\.?0+$/, "");
    const vwCoefficient = (slope * 100).toFixed(3).replace(/\.?0+$/, "");

    const preferred = `${interceptRem}rem + ${vwCoefficient}vw`;
    const css = `clamp(${minRem}rem, ${preferred}, ${maxRem}rem)`;

    els.output.textContent = `font-size: ${css};`;
    els.preview.style.fontSize = css;
  }

  [els.minSize, els.minVp, els.maxSize, els.maxVp, els.rootFont].forEach((el) =>
    el.addEventListener("input", update)
  );
  update();

  els.copyBtn.addEventListener("click", async () => {
    if (!els.output.textContent || els.output.textContent.startsWith("//")) return;
    try {
      await copyToClipboard(els.output.textContent);
      const I18N_C = i18nFor("common");
      showMascotToast(I18N_C.copied || "Copied!");
      celebrateSuccess(els.copyBtn);
    } catch (e) { /* clipboard unavailable, silently ignore */ }
  });
})();
