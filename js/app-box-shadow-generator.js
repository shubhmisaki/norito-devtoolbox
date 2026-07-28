(function () {
  const els = {
    layersWrap: document.getElementById("layersWrap"),
    addLayerBtn: document.getElementById("addLayerBtn"),
    preview: document.getElementById("previewBox"),
    output: document.getElementById("output"),
    copyBtn: document.getElementById("copyBtn"),
  };

  let layers = [
    { x: 0, y: 4, blur: 12, spread: 0, color: "#000000", alpha: 25, inset: false },
  ];

  function layerCss(l) {
    const rgba = hexToRgba(l.color, l.alpha / 100);
    return `${l.inset ? "inset " : ""}${l.x}px ${l.y}px ${l.blur}px ${l.spread}px ${rgba}`;
  }

  function hexToRgba(hex, alpha) {
    const m = /^#?([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$/i.exec(hex || "");
    if (!m) return `rgba(0,0,0,${alpha})`;
    const r = parseInt(m[1], 16), g = parseInt(m[2], 16), b = parseInt(m[3], 16);
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
  }

  function renderLayers() {
    els.layersWrap.innerHTML = layers.map((l, i) => `
      <div class="panel layer-panel" data-idx="${i}" style="margin-bottom:12px;">
        <div class="field-row">
          <div class="field"><label>X offset (${l.x}px)</label><input type="range" class="l-x" min="-50" max="50" value="${l.x}" /></div>
          <div class="field"><label>Y offset (${l.y}px)</label><input type="range" class="l-y" min="-50" max="50" value="${l.y}" /></div>
        </div>
        <div class="field-row">
          <div class="field"><label>Blur (${l.blur}px)</label><input type="range" class="l-blur" min="0" max="100" value="${l.blur}" /></div>
          <div class="field"><label>Spread (${l.spread}px)</label><input type="range" class="l-spread" min="-50" max="50" value="${l.spread}" /></div>
        </div>
        <div class="field-row">
          <div class="field"><label>Color</label><input type="color" class="l-color" value="${l.color}" /></div>
          <div class="field"><label>Opacity (${l.alpha}%)</label><input type="range" class="l-alpha" min="0" max="100" value="${l.alpha}" /></div>
        </div>
        <div class="option-row">
          <span class="option-label">Inset</span>
          <label class="switch"><input type="checkbox" class="l-inset" ${l.inset ? "checked" : ""} /><span class="track"></span></label>
        </div>
        ${layers.length > 1 ? '<button type="button" class="secondary remove-layer-btn">Remove layer</button>' : ""}
      </div>`).join("");

    els.layersWrap.querySelectorAll(".layer-panel").forEach((panel) => {
      const idx = Number(panel.dataset.idx);
      const l = layers[idx];
      const bind = (sel, key, isNum, isBool) => {
        const el = panel.querySelector(sel);
        el.addEventListener("input", () => {
          l[key] = isBool ? el.checked : isNum ? Number(el.value) : el.value;
          renderLayers();
          update();
        });
      };
      bind(".l-x", "x", true);
      bind(".l-y", "y", true);
      bind(".l-blur", "blur", true);
      bind(".l-spread", "spread", true);
      bind(".l-color", "color", false);
      bind(".l-alpha", "alpha", true);
      bind(".l-inset", "inset", false, true);
      const removeBtn = panel.querySelector(".remove-layer-btn");
      if (removeBtn) removeBtn.addEventListener("click", () => { layers.splice(idx, 1); renderLayers(); update(); });
    });
  }

  els.addLayerBtn.addEventListener("click", () => {
    layers.push({ x: 0, y: 2, blur: 8, spread: 0, color: "#000000", alpha: 15, inset: false });
    renderLayers();
    update();
  });

  function update() {
    const css = layers.map(layerCss).join(",\n  ");
    els.preview.style.boxShadow = layers.map(layerCss).join(", ");
    els.output.textContent = `box-shadow: ${css};`;
  }

  renderLayers();
  update();

  els.copyBtn.addEventListener("click", async () => {
    if (!els.output.textContent) return;
    try {
      await copyToClipboard(els.output.textContent);
      const original = els.copyBtn.textContent;
      els.copyBtn.textContent = "Copied!";
      setTimeout(() => { els.copyBtn.textContent = original; }, 1500);
    } catch (e) { /* clipboard unavailable, silently ignore */ }
  });
})();
