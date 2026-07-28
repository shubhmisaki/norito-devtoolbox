(function () {
  const els = {
    modeTabs: document.getElementById("mode-tabs"),
    mode: document.getElementById("mode"),
    encodeType: document.getElementById("encodeType"),
    input: document.getElementById("input"),
    output: document.getElementById("output"),
    errorBox: document.getElementById("errorBox"),
    swapBtn: document.getElementById("swapBtn"),
    copyBtn: document.getElementById("copyBtn"),
  };

  function setMode(value) {
    els.mode.value = value;
    els.modeTabs.querySelectorAll(".tab").forEach((t) => t.classList.toggle("active", t.dataset.value === value));
    els.input.placeholder = value === "decode"
      ? "Paste a percent-encoded URL or string..."
      : "Type or paste text or a URL...";
    render();
  }
  els.modeTabs.addEventListener("click", (e) => {
    const btn = e.target.closest(".tab");
    if (btn) setMode(btn.dataset.value);
  });

  function render() {
    els.errorBox.style.display = "none";
    const raw = els.input.value;
    if (!raw) { els.output.value = ""; return; }
    try {
      if (els.mode.value === "decode") {
        els.output.value = decodeURIComponent(raw.replace(/\+/g, "%20"));
      } else {
        els.output.value = els.encodeType.value === "full" ? encodeURI(raw) : encodeURIComponent(raw);
      }
    } catch (err) {
      els.output.value = "";
      els.errorBox.querySelector(".r-body").textContent = "That doesn't look like valid percent-encoded text.";
      els.errorBox.style.display = "flex";
    }
  }

  els.input.addEventListener("input", render);
  els.encodeType.addEventListener("change", render);

  els.swapBtn.addEventListener("click", () => {
    const newMode = els.mode.value === "decode" ? "encode" : "decode";
    const swapped = els.output.value;
    setMode(newMode);
    els.input.value = swapped;
    render();
  });

  els.copyBtn.addEventListener("click", async () => {
    if (!els.output.value) return;
    try {
      await copyToClipboard(els.output.value);
    } catch (err) {
      els.output.select();
      document.execCommand("copy");
    }
    showMascotToast("Copied!");
    celebrateSuccess(els.copyBtn);
  });

  render();
})();
