(function () {
  const I18N_C = i18nFor("common");
  const I18N = i18nFor("app-base64");

  const els = {
    mode: document.getElementById("mode"),
    input: document.getElementById("input"),
    output: document.getElementById("output"),
    urlSafe: document.getElementById("optUrlSafe"),
    swapBtn: document.getElementById("swapBtn"),
    copyBtn: document.getElementById("copyBtn"),
    errorBox: document.getElementById("errorBox"),
  };

  function toUtf8Bytes(str) {
    return new TextEncoder().encode(str);
  }
  function fromUtf8Bytes(bytes) {
    return new TextDecoder().decode(bytes);
  }

  function b64Encode(str, urlSafe) {
    const bytes = toUtf8Bytes(str);
    let binary = "";
    bytes.forEach((b) => { binary += String.fromCharCode(b); });
    let b64 = btoa(binary);
    if (urlSafe) b64 = b64.replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
    return b64;
  }

  function b64Decode(b64raw) {
    let b64 = b64raw.trim().replace(/-/g, "+").replace(/_/g, "/");
    while (b64.length % 4) b64 += "=";
    const binary = atob(b64);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
    return fromUtf8Bytes(bytes);
  }

  function render() {
    const isDecode = els.mode.value === "decode";
    els.errorBox.style.display = "none";
    const raw = els.input.value;
    if (!raw) {
      els.output.value = "";
      return;
    }
    try {
      els.output.value = isDecode ? b64Decode(raw) : b64Encode(raw, els.urlSafe.checked);
    } catch (e) {
      els.output.value = "";
      els.errorBox.textContent = I18N.invalid_base64 || "That doesn't look like valid Base64.";
      els.errorBox.style.display = "block";
    }
  }

  els.input.addEventListener("input", render);
  els.urlSafe.addEventListener("change", render);
  els.mode.addEventListener("change", () => {
    els.input.placeholder =
      els.mode.value === "decode"
        ? I18N.placeholder_decode || "Paste Base64 to decode..."
        : I18N.placeholder_encode || "Type or paste text to encode...";
    render();
  });

  els.swapBtn.addEventListener("click", () => {
    const newMode = els.mode.value === "decode" ? "encode" : "decode";
    const swapped = els.output.value;
    els.mode.value = newMode;
    els.mode.dispatchEvent(new Event("change"));
    els.input.value = swapped;
    render();
  });

  els.copyBtn.addEventListener("click", async () => {
    if (!els.output.value) return;
    try {
      await copyToClipboard(els.output.value);
    } catch (e) {
      els.output.select();
      document.execCommand("copy");
    }
    showMascotToast(I18N_C.copied || "Copied!");
    celebrateSuccess(els.copyBtn);
  });

  render();
})();
