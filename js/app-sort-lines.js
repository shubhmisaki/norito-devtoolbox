(function () {
  const els = {
    input: document.getElementById("textInput"),
    output: document.getElementById("textOutput"),
    sortBy: document.getElementById("sortBy"),
    direction: document.getElementById("direction"),
    dedupe: document.getElementById("optDedupe"),
    removeBlank: document.getElementById("optRemoveBlank"),
    statInfo: document.getElementById("statInfo"),
    copyBtn: document.getElementById("copyBtn"),
  };

  function process() {
    let lines = els.input.value.split("\n");
    if (els.removeBlank.checked) lines = lines.filter((l) => l.trim() !== "");

    const by = els.sortBy.value;
    if (by === "shuffle") {
      // Fisher-Yates
      for (let i = lines.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [lines[i], lines[j]] = [lines[j], lines[i]];
      }
    } else {
      const cmp = {
        alpha: (a, b) => a.localeCompare(b),
        alphaCI: (a, b) => a.toLowerCase().localeCompare(b.toLowerCase()),
        numeric: (a, b) => (parseFloat(a) || 0) - (parseFloat(b) || 0),
        length: (a, b) => a.length - b.length,
      }[by] || ((a, b) => a.localeCompare(b));
      lines.sort(cmp);
      if (els.direction.value === "desc") lines.reverse();
    }

    if (els.dedupe.checked) {
      const seen = new Set();
      lines = lines.filter((l) => (seen.has(l) ? false : (seen.add(l), true)));
    }

    els.output.value = lines.join("\n");
    els.statInfo.textContent = `${lines.length} line${lines.length === 1 ? "" : "s"}.`;
  }

  [els.input, els.sortBy, els.direction, els.dedupe, els.removeBlank].forEach((el) => {
    el.addEventListener("input", process);
    el.addEventListener("change", process);
  });
  process();

  // Shuffle is a one-shot action, re-running it should re-shuffle even if
  // no dropdown value actually changed, which "input"/"change" events won't
  // naturally fire for. The explicit button covers that case directly.
  const sortNowBtn = document.getElementById("sortNowBtn");
  if (sortNowBtn) sortNowBtn.addEventListener("click", process);

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
