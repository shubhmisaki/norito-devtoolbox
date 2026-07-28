(function () {
  const els = {
    picker: document.getElementById("colorPicker"),
    swatch: document.getElementById("swatchLg"),
    hex: document.getElementById("hexOut"),
    rgb: document.getElementById("rgbOut"),
    hsl: document.getElementById("hslOut"),
    cmyk: document.getElementById("cmykOut"),
  };

  function hexToRgb(hex) {
    const m = /^#?([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$/i.exec(hex || "");
    if (!m) return null;
    return { r: parseInt(m[1], 16), g: parseInt(m[2], 16), b: parseInt(m[3], 16) };
  }
  function rgbToHex(r, g, b) {
    return "#" + [r, g, b].map((v) => Math.round(v).toString(16).padStart(2, "0")).join("");
  }
  function rgbToHsl(r, g, b) {
    r /= 255; g /= 255; b /= 255;
    const max = Math.max(r, g, b), min = Math.min(r, g, b);
    let h, s, l = (max + min) / 2;
    if (max === min) { h = s = 0; }
    else {
      const d = max - min;
      s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
      switch (max) {
        case r: h = (g - b) / d + (g < b ? 6 : 0); break;
        case g: h = (b - r) / d + 2; break;
        default: h = (r - g) / d + 4;
      }
      h /= 6;
    }
    return { h: Math.round(h * 360), s: Math.round(s * 100), l: Math.round(l * 100) };
  }
  function rgbToCmyk(r, g, b) {
    if (r === 0 && g === 0 && b === 0) return { c: 0, m: 0, y: 0, k: 100 };
    const rp = r / 255, gp = g / 255, bp = b / 255;
    const k = 1 - Math.max(rp, gp, bp);
    const c = (1 - rp - k) / (1 - k);
    const m = (1 - gp - k) / (1 - k);
    const y = (1 - bp - k) / (1 - k);
    return { c: Math.round(c * 100), m: Math.round(m * 100), y: Math.round(y * 100), k: Math.round(k * 100) };
  }

  function updateFromHex(hex) {
    const rgb = hexToRgb(hex);
    if (!rgb) return;
    const hsl = rgbToHsl(rgb.r, rgb.g, rgb.b);
    const cmyk = rgbToCmyk(rgb.r, rgb.g, rgb.b);
    els.swatch.style.background = hex;
    els.picker.value = hex;
    els.hex.value = hex.toUpperCase();
    els.rgb.value = `rgb(${rgb.r}, ${rgb.g}, ${rgb.b})`;
    els.hsl.value = `hsl(${hsl.h}, ${hsl.s}%, ${hsl.l}%)`;
    els.cmyk.value = `cmyk(${cmyk.c}%, ${cmyk.m}%, ${cmyk.y}%, ${cmyk.k}%)`;
  }

  els.picker.addEventListener("input", () => updateFromHex(els.picker.value));
  els.hex.addEventListener("input", () => {
    let v = els.hex.value.trim();
    if (!v.startsWith("#")) v = "#" + v;
    if (/^#[0-9a-fA-F]{6}$/.test(v)) updateFromHex(v);
  });

  [els.hex, els.rgb, els.hsl, els.cmyk].forEach((input) => {
    input.addEventListener("click", () => input.select());
  });

  document.querySelectorAll(".color-copy-row .copy-field-btn").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const target = document.getElementById(btn.dataset.target);
      if (!target || !target.value) return;
      try {
        await copyToClipboard(target.value);
        celebrateSuccess(null, btn, "Copied");
      } catch (e) {
        /* clipboard unavailable */
      }
    });
  });

  updateFromHex("#ff4d7a");
})();
