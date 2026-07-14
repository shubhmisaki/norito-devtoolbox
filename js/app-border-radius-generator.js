(function () {
  const els = {
    tl: document.getElementById("radTL"),
    tr: document.getElementById("radTR"),
    br: document.getElementById("radBR"),
    bl: document.getElementById("radBL"),
    linkAll: document.getElementById("linkAll"),
    preview: document.getElementById("previewBox"),
    output: document.getElementById("output"),
    copyBtn: document.getElementById("copyBtn"),
    tlVal: document.getElementById("radTLVal"),
    trVal: document.getElementById("radTRVal"),
    brVal: document.getElementById("radBRVal"),
    blVal: document.getElementById("radBLVal"),
  };

  function update(source) {
    if (els.linkAll.checked && source) {
      const v = source.value;
      [els.tl, els.tr, els.br, els.bl].forEach((el) => { el.value = v; });
    }
    els.tlVal.textContent = `${els.tl.value}px`;
    els.trVal.textContent = `${els.tr.value}px`;
    els.brVal.textContent = `${els.br.value}px`;
    els.blVal.textContent = `${els.bl.value}px`;

    const css = `${els.tl.value}px ${els.tr.value}px ${els.br.value}px ${els.bl.value}px`;
    els.preview.style.borderRadius = css;
    els.output.textContent = `border-radius: ${css};`;
  }

  [els.tl, els.tr, els.br, els.bl].forEach((el) => el.addEventListener("input", () => update(el)));
  els.linkAll.addEventListener("change", () => update(els.tl));
  update();

  els.copyBtn.addEventListener("click", async () => {
    if (!els.output.textContent) return;
    try {
      await navigator.clipboard.writeText(els.output.textContent);
      const original = els.copyBtn.textContent;
      els.copyBtn.textContent = "Copied!";
      setTimeout(() => { els.copyBtn.textContent = original; }, 1500);
    } catch (e) { /* clipboard unavailable, silently ignore */ }
  });
})();
