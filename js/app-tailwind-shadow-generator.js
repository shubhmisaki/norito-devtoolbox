(function () {
  const els = {
    layersWrap: document.getElementById("layersWrap"),
    addLayerBtn: document.getElementById("addLayerBtn"),
    preview: document.getElementById("previewBox"),
    twOutput: document.getElementById("twOutput"),
    cssOutput: document.getElementById("cssOutput"),
    copyTwBtn: document.getElementById("copyTwBtn"),
    copyCssBtn: document.getElementById("copyCssBtn"),
  };

  let layers = [
    { x: 0, y: 4, blur: 6, spread: -1, color: "#000000", alpha: 20, inset: false },
  ];

  function hexToRgba(hex, alphaPct) {
    const h = hex.replace("#", "");
    const r = parseInt(h.substring(0, 2), 16);
    const g = parseInt(h.substring(2, 4), 16);
    const b = parseInt(h.substring(4, 6), 16);
    return `rgba(${r}, ${g}, ${b}, ${(alphaPct / 100).toFixed(2)})`;
  }

  function layerToCss(l) {
    return `${l.inset ? "inset " : ""}${l.x}px ${l.y}px ${l.blur}px ${l.spread}px ${hexToRgba(l.color, l.alpha)}`;
  }

  function renderLayers() {
    els.layersWrap.innerHTML = layers
      .map(
        (l, i) => `
      <div class="panel" style="margin-bottom:12px;" data-idx="${i}">
        <div class="field-row">
          <div class="field"><label>Offset X (${l.x}px)</label><input type="range" class="ls-x" min="-40" max="40" value="${l.x}" /></div>
          <div class="field"><label>Offset Y (${l.y}px)</label><input type="range" class="ls-y" min="-40" max="40" value="${l.y}" /></div>
        </div>
        <div class="field-row">
          <div class="field"><label>Blur (${l.blur}px)</label><input type="range" class="ls-blur" min="0" max="80" value="${l.blur}" /></div>
          <div class="field"><label>Spread (${l.spread}px)</label><input type="range" class="ls-spread" min="-40" max="40" value="${l.spread}" /></div>
        </div>
        <div class="field-row">
          <div class="field"><label>Color</label><input type="color" class="ls-color" value="${l.color}" /></div>
          <div class="field"><label>Opacity (${l.alpha}%)</label><input type="range" class="ls-alpha" min="0" max="100" value="${l.alpha}" /></div>
        </div>
        <div class="option-row">
          <span class="option-label">Inset</span>
          <label class="switch"><input type="checkbox" class="ls-inset" ${l.inset ? "checked" : ""} /><span class="track"></span></label>
        </div>
        ${layers.length > 1 ? '<button type="button" class="secondary ls-remove">Remove layer</button>' : ""}
      </div>`
      )
      .join("");

    els.layersWrap.querySelectorAll(".panel").forEach((panel) => {
      const idx = Number(panel.dataset.idx);
      panel.querySelector(".ls-x").addEventListener("input", (e) => { layers[idx].x = Number(e.target.value); renderLayers(); update(); });
      panel.querySelector(".ls-y").addEventListener("input", (e) => { layers[idx].y = Number(e.target.value); renderLayers(); update(); });
      panel.querySelector(".ls-blur").addEventListener("input", (e) => { layers[idx].blur = Number(e.target.value); renderLayers(); update(); });
      panel.querySelector(".ls-spread").addEventListener("input", (e) => { layers[idx].spread = Number(e.target.value); renderLayers(); update(); });
      panel.querySelector(".ls-color").addEventListener("input", (e) => { layers[idx].color = e.target.value; update(); });
      panel.querySelector(".ls-alpha").addEventListener("input", (e) => { layers[idx].alpha = Number(e.target.value); renderLayers(); update(); });
      panel.querySelector(".ls-inset").addEventListener("change", (e) => { layers[idx].inset = e.target.checked; update(); });
      const removeBtn = panel.querySelector(".ls-remove");
      if (removeBtn) removeBtn.addEventListener("click", () => { layers.splice(idx, 1); renderLayers(); update(); });
    });
  }

  function update() {
    const css = layers.map(layerToCss).join(", ");
    els.preview.style.boxShadow = css;
    els.cssOutput.textContent = `box-shadow: ${css};`;
    const twValue = css.replace(/\s+/g, "_");
    els.twOutput.textContent = `shadow-[${twValue}]`;
  }

  els.addLayerBtn.addEventListener("click", () => {
    layers.push({ x: 0, y: 2, blur: 4, spread: 0, color: "#000000", alpha: 15, inset: false });
    renderLayers();
    update();
  });

  renderLayers();
  update();

  function copyText(text, btn) {
    if (!text) return;
    copyToClipboard(text).then(() => {
      const I18N_C = i18nFor("common");
      showMascotToast(I18N_C.copied || "Copied!");
      celebrateSuccess(btn);
    }).catch(() => {});
  }

  els.copyTwBtn.addEventListener("click", () => copyText(els.twOutput.textContent, els.copyTwBtn));
  els.copyCssBtn.addEventListener("click", () => copyText(els.cssOutput.textContent, els.copyCssBtn));
})();
