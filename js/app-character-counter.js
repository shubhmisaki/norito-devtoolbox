(function () {
  const els = {
    text: document.getElementById("textInput"),
    withSpaces: document.getElementById("statWithSpaces"),
    noSpaces: document.getElementById("statNoSpaces"),
    bytes: document.getElementById("statBytes"),
    limitList: document.getElementById("limitList"),
  };

  const LIMITS = [
    { name: "Tweet / X post", max: 280 },
    { name: "SMS (single segment)", max: 160 },
    { name: "Meta description", max: 160 },
    { name: "Title tag", max: 60 },
    { name: "Instagram caption", max: 2200 },
    { name: "LinkedIn post", max: 3000 },
  ];

  function update() {
    const text = els.text.value;
    const withSpaces = text.length;
    const noSpaces = text.replace(/\s/g, "").length;
    const bytes = new TextEncoder().encode(text).length;

    els.withSpaces.textContent = withSpaces.toLocaleString();
    els.noSpaces.textContent = noSpaces.toLocaleString();
    els.bytes.textContent = bytes.toLocaleString();

    els.limitList.innerHTML = LIMITS.map((l) => {
      const over = withSpaces > l.max;
      const remaining = l.max - withSpaces;
      const cls = over ? "limit-over" : "limit-ok";
      const note = over
        ? `${Math.abs(remaining).toLocaleString()} over`
        : `${remaining.toLocaleString()} left`;
      return `<div class="meta-row ${cls}"><span class="meta-label">${l.name} (${l.max})</span><span class="meta-value">${note}</span></div>`;
    }).join("");
  }

  els.text.addEventListener("input", update);
  update();
})();
