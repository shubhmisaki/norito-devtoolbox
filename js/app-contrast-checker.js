(function () {
  const els = {
    fg: document.getElementById("fgColor"),
    fgHex: document.getElementById("fgHex"),
    bg: document.getElementById("bgColor"),
    bgHex: document.getElementById("bgHex"),
    swapBtn: document.getElementById("swapBtn"),
    preview: document.getElementById("previewBox"),
    ratioDisplay: document.getElementById("ratioDisplay"),
    badges: document.getElementById("badges"),
  };

  function hexToRgb(hex) {
    const m = /^#?([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$/i.exec(hex || "");
    if (!m) return null;
    return { r: parseInt(m[1], 16), g: parseInt(m[2], 16), b: parseInt(m[3], 16) };
  }

  function relativeLuminance({ r, g, b }) {
    const chan = [r, g, b].map((v) => {
      const c = v / 255;
      return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * chan[0] + 0.7152 * chan[1] + 0.0722 * chan[2];
  }

  function contrastRatio(hex1, hex2) {
    const c1 = hexToRgb(hex1), c2 = hexToRgb(hex2);
    if (!c1 || !c2) return null;
    const l1 = relativeLuminance(c1), l2 = relativeLuminance(c2);
    const lighter = Math.max(l1, l2), darker = Math.min(l1, l2);
    return (lighter + 0.05) / (darker + 0.05);
  }

  function badge(label, pass) {
    return `<span class="contrast-badge ${pass ? "pass" : "fail"}">${pass ? "✓" : "✕"} ${label}</span>`;
  }

  function update() {
    const fg = els.fgHex.value;
    const bg = els.bgHex.value;
    els.fg.value = fg;
    els.bg.value = bg;
    els.preview.style.color = fg;
    els.preview.style.background = bg;

    const ratio = contrastRatio(fg, bg);
    if (ratio == null) {
      els.ratioDisplay.textContent = "--";
      els.badges.innerHTML = "";
      return;
    }
    els.ratioDisplay.textContent = ratio.toFixed(2) + " : 1";
    els.badges.innerHTML =
      badge("AA Normal (4.5:1)", ratio >= 4.5) +
      badge("AA Large (3:1)", ratio >= 3) +
      badge("AAA Normal (7:1)", ratio >= 7) +
      badge("AAA Large (4.5:1)", ratio >= 4.5);
  }

  function syncFromPicker(picker, hexInput) {
    picker.addEventListener("input", () => {
      hexInput.value = picker.value;
      update();
    });
  }
  function syncFromHex(hexInput, picker) {
    hexInput.addEventListener("input", () => {
      let v = hexInput.value.trim();
      if (!v.startsWith("#")) v = "#" + v;
      if (/^#[0-9a-fA-F]{6}$/.test(v)) {
        picker.value = v;
        hexInput.value = v;
        update();
      }
    });
  }

  syncFromPicker(els.fg, els.fgHex);
  syncFromPicker(els.bg, els.bgHex);
  syncFromHex(els.fgHex, els.fg);
  syncFromHex(els.bgHex, els.bg);

  els.swapBtn.addEventListener("click", () => {
    const fg = els.fgHex.value;
    els.fgHex.value = els.bgHex.value;
    els.bgHex.value = fg;
    update();
  });

  update();
})();
