(function () {
  const els = {
    input: document.getElementById("textInput"),
    output: document.getElementById("textOutput"),
    caseSensitive: document.getElementById("optCaseSensitive"),
    trimLines: document.getElementById("optTrimLines"),
    removeBlank: document.getElementById("optRemoveBlank"),
    statRemoved: document.getElementById("statRemoved"),
    copyBtn: document.getElementById("copyBtn"),
  };

  function process() {
    let lines = els.input.value.split("\n");
    if (els.trimLines.checked) lines = lines.map((l) => l.trim());
    if (els.removeBlank.checked) lines = lines.filter((l) => l.trim() !== "");

    const seen = new Set();
    const out = [];
    for (const line of lines) {
      const key = els.caseSensitive.checked ? line : line.toLowerCase();
      if (seen.has(key)) continue;
      seen.add(key);
      out.push(line);
    }

    els.output.value = out.join("\n");
    els.statRemoved.textContent = `${lines.length - out.length} duplicate line${lines.length - out.length === 1 ? "" : "s"} removed, ${out.length} remaining.`;
  }

  [els.input, els.caseSensitive, els.trimLines, els.removeBlank].forEach((el) =>
    el.addEventListener("input", process)
  );
  process();

  els.copyBtn.addEventListener("click", async () => {
    if (!els.output.value) return;
    try {
      await navigator.clipboard.writeText(els.output.value);
      const original = els.copyBtn.textContent;
      els.copyBtn.textContent = "Copied!";
      setTimeout(() => { els.copyBtn.textContent = original; }, 1500);
    } catch (e) {
      els.output.select();
      document.execCommand("copy");
    }
  });
})();
