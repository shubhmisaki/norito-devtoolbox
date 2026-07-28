(function () {
  const els = {
    modeTabs: document.getElementById("mode-tabs"),
    mode: document.getElementById("mode"),
    allNonAscii: document.getElementById("optAllNonAscii"),
    input: document.getElementById("input"),
    output: document.getElementById("output"),
    swapBtn: document.getElementById("swapBtn"),
    copyBtn: document.getElementById("copyBtn"),
  };

  const BASE_MAP = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };

  function encode(str) {
    let out = str.replace(/[&<>"']/g, function (ch) { return BASE_MAP[ch]; });
    if (els.allNonAscii.checked) {
      out = out.replace(/[^\x00-\x7F]/g, function (ch) { return "&#" + ch.codePointAt(0) + ";"; });
    }
    return out;
  }

  // Decoding untrusted markup safely: assigning to a <textarea>'s innerHTML and
  // reading back .value lets the browser's own HTML parser resolve every named
  // and numeric entity correctly, without ever executing the content as a live
  // page (a textarea's contents are always treated as plain text, never as
  // markup or script).
  const decoderEl = document.createElement("textarea");
  function decode(str) {
    decoderEl.innerHTML = str;
    return decoderEl.value;
  }

  function setMode(value) {
    els.mode.value = value;
    els.modeTabs.querySelectorAll(".tab").forEach(function (t) { t.classList.toggle("active", t.dataset.value === value); });
    els.input.placeholder = value === "decode"
      ? "Paste HTML entities to decode..."
      : "Type or paste HTML or text...";
    render();
  }
  els.modeTabs.addEventListener("click", function (e) {
    const btn = e.target.closest(".tab");
    if (btn) setMode(btn.dataset.value);
  });

  function render() {
    const raw = els.input.value;
    if (!raw) { els.output.value = ""; return; }
    els.output.value = els.mode.value === "decode" ? decode(raw) : encode(raw);
  }

  els.input.addEventListener("input", render);
  els.allNonAscii.addEventListener("change", render);

  els.swapBtn.addEventListener("click", function () {
    const newMode = els.mode.value === "decode" ? "encode" : "decode";
    const swapped = els.output.value;
    setMode(newMode);
    els.input.value = swapped;
    render();
  });

  els.copyBtn.addEventListener("click", async function () {
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
