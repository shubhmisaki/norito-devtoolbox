(function () {
  const els = {
    type: document.getElementById("gradType"),
    angle: document.getElementById("gradAngle"),
    angleRow: document.getElementById("angleRow"),
    stopsWrap: document.getElementById("stopsWrap"),
    addStopBtn: document.getElementById("addStopBtn"),
    preview: document.getElementById("preview"),
    output: document.getElementById("output"),
    copyBtn: document.getElementById("copyBtn"),
  };

  let stops = [
    { color: "#ec4899", pos: 0 },
    { color: "#6366f1", pos: 100 },
  ];

  function renderStops() {
    els.stopsWrap.innerHTML = stops.map((s, i) => `
      <div class="field-row grad-stop-row" data-idx="${i}">
        <input type="color" class="stop-color" value="${s.color}" />
        <input type="number" class="stop-pos" min="0" max="100" value="${s.pos}" />
        <span class="note">%</span>
        ${stops.length > 2 ? '<button type="button" class="secondary remove-stop-btn">&times;</button>' : ""}
      </div>`).join("");

    els.stopsWrap.querySelectorAll(".grad-stop-row").forEach((row) => {
      const idx = Number(row.dataset.idx);
      row.querySelector(".stop-color").addEventListener("input", (e) => { stops[idx].color = e.target.value; update(); });
      row.querySelector(".stop-pos").addEventListener("input", (e) => { stops[idx].pos = Number(e.target.value); update(); });
      const removeBtn = row.querySelector(".remove-stop-btn");
      if (removeBtn) removeBtn.addEventListener("click", () => { stops.splice(idx, 1); renderStops(); update(); });
    });
  }

  els.addStopBtn.addEventListener("click", () => {
    stops.push({ color: "#22c55e", pos: 50 });
    renderStops();
    update();
  });

  function buildGradientCss() {
    const sorted = [...stops].sort((a, b) => a.pos - b.pos);
    const stopStr = sorted.map((s) => `${s.color} ${s.pos}%`).join(", ");
    if (els.type.value === "radial") {
      return `radial-gradient(circle, ${stopStr})`;
    }
    return `linear-gradient(${els.angle.value}deg, ${stopStr})`;
  }

  function update() {
    els.angleRow.style.display = els.type.value === "linear" ? "flex" : "none";
    const css = buildGradientCss();
    els.preview.style.background = css;
    els.output.textContent = `background: ${css};`;
  }

  els.type.addEventListener("change", update);
  els.angle.addEventListener("input", update);
  renderStops();
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
