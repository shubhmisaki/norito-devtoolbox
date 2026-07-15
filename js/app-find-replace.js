(function () {
  const els = {
    input: document.getElementById("input"),
    findText: document.getElementById("findText"),
    replaceText: document.getElementById("replaceText"),
    useRegex: document.getElementById("useRegex"),
    caseSensitive: document.getElementById("caseSensitive"),
    wholeWord: document.getElementById("wholeWord"),
    replaceAll: document.getElementById("replaceAll"),
    matchCount: document.getElementById("matchCount"),
    output: document.getElementById("output"),
    errorBox: document.getElementById("errorBox"),
    copyBtn: document.getElementById("copyBtn"),
  };

  function escapeRegex(s) {
    return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  function buildPattern() {
    const find = els.findText.value;
    if (find === "") return null;
    let source = els.useRegex.checked ? find : escapeRegex(find);
    if (els.wholeWord.checked) source = "\\b" + source + "\\b";
    let flags = "g";
    if (!els.caseSensitive.checked) flags += "i";
    return new RegExp(source, flags);
  }

  function render() {
    els.errorBox.style.display = "none";
    const text = els.input.value;
    const find = els.findText.value;
    if (!text || find === "") {
      els.output.value = text;
      els.matchCount.textContent = "";
      return;
    }
    let re;
    try {
      re = buildPattern();
    } catch (err) {
      els.output.value = text;
      els.matchCount.textContent = "";
      els.errorBox.querySelector(".r-body").textContent = "Invalid regular expression: " + err.message;
      els.errorBox.style.display = "flex";
      return;
    }
    const matches = text.match(re) || [];
    els.matchCount.textContent = matches.length + " match" + (matches.length === 1 ? "" : "es");
    const replaceWith = els.replaceText.value;
    if (els.replaceAll.checked) {
      els.output.value = text.replace(re, replaceWith);
    } else {
      let replaced = false;
      els.output.value = text.replace(re, function (m) {
        if (replaced) return m;
        replaced = true;
        return replaceWith;
      });
    }
  }

  [els.input, els.findText, els.replaceText].forEach(function (el) {
    el.addEventListener("input", render);
  });
  [els.useRegex, els.caseSensitive, els.wholeWord, els.replaceAll].forEach(function (el) {
    el.addEventListener("change", render);
  });

  els.copyBtn.addEventListener("click", async function () {
    if (!els.output.value) return;
    try {
      await navigator.clipboard.writeText(els.output.value);
    } catch (err) {
      els.output.select();
      document.execCommand("copy");
    }
    showMascotToast("Copied!");
    celebrateSuccess(els.copyBtn);
  });

  render();
})();
