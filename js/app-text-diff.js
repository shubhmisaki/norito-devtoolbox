(function () {
  const els = {
    inputA: document.getElementById("inputA"),
    inputB: document.getElementById("inputB"),
    ignoreWhitespace: document.getElementById("ignoreWhitespace"),
    ignoreCase: document.getElementById("ignoreCase"),
    statsBox: document.getElementById("statsBox"),
    diffOutput: document.getElementById("diffOutput"),
    emptyState: document.getElementById("emptyState"),
    tooLarge: document.getElementById("tooLarge"),
    copyBtn: document.getElementById("copyBtn"),
  };

  const MAX_LINES = 4000;

  function normalize(line) {
    let out = line;
    if (els.ignoreWhitespace.checked) out = out.trim().replace(/\s+/g, " ");
    if (els.ignoreCase.checked) out = out.toLowerCase();
    return out;
  }

  function diffLines(aRaw, bRaw) {
    const aOrig = aRaw.split("\n");
    const bOrig = bRaw.split("\n");
    const a = aOrig.map(normalize);
    const b = bOrig.map(normalize);
    const n = a.length, m = b.length;
    const dp = new Array(n + 1);
    for (let i = 0; i <= n; i++) dp[i] = new Int32Array(m + 1);
    for (let i = n - 1; i >= 0; i--) {
      for (let j = m - 1; j >= 0; j--) {
        dp[i][j] = a[i] === b[j] ? dp[i + 1][j + 1] + 1 : Math.max(dp[i + 1][j], dp[i][j + 1]);
      }
    }
    const ops = [];
    let i = 0, j = 0;
    while (i < n && j < m) {
      if (a[i] === b[j]) { ops.push({ type: "equal", a: aOrig[i], b: bOrig[j] }); i++; j++; }
      else if (dp[i + 1][j] >= dp[i][j + 1]) { ops.push({ type: "remove", a: aOrig[i] }); i++; }
      else { ops.push({ type: "add", b: bOrig[j] }); j++; }
    }
    while (i < n) { ops.push({ type: "remove", a: aOrig[i] }); i++; }
    while (j < m) { ops.push({ type: "add", b: bOrig[j] }); j++; }
    return ops;
  }

  function escapeHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function render() {
    const aRaw = els.inputA.value;
    const bRaw = els.inputB.value;
    if (!aRaw && !bRaw) {
      els.emptyState.style.display = "block";
      els.tooLarge.style.display = "none";
      els.diffOutput.style.display = "none";
      els.statsBox.style.display = "none";
      return;
    }
    const aLineCount = aRaw.split("\n").length;
    const bLineCount = bRaw.split("\n").length;
    if (aLineCount > MAX_LINES || bLineCount > MAX_LINES) {
      els.emptyState.style.display = "none";
      els.diffOutput.style.display = "none";
      els.statsBox.style.display = "none";
      els.tooLarge.style.display = "flex";
      return;
    }
    els.emptyState.style.display = "none";
    els.tooLarge.style.display = "none";

    const ops = diffLines(aRaw, bRaw);
    let added = 0, removed = 0, unchanged = 0;
    let aLine = 1, bLine = 1;
    const rows = [];
    for (const op of ops) {
      if (op.type === "equal") {
        rows.push('<div class="diff-row diff-equal"><span class="diff-ln">' + aLine + "</span><span class=\"diff-ln\">" + bLine + '</span><span class="diff-marker"> </span><span class="diff-text">' + escapeHtml(op.a) + "</span></div>");
        aLine++; bLine++; unchanged++;
      } else if (op.type === "remove") {
        rows.push('<div class="diff-row diff-remove"><span class="diff-ln">' + aLine + '</span><span class="diff-ln"></span><span class="diff-marker">-</span><span class="diff-text">' + escapeHtml(op.a) + "</span></div>");
        aLine++; removed++;
      } else {
        rows.push('<div class="diff-row diff-add"><span class="diff-ln"></span><span class="diff-ln">' + bLine + '</span><span class="diff-marker">+</span><span class="diff-text">' + escapeHtml(op.b) + "</span></div>");
        bLine++; added++;
      }
    }
    els.diffOutput.innerHTML = rows.join("");
    els.diffOutput.style.display = "block";
    els.statsBox.innerHTML =
      '<span class="diff-stat diff-stat-add">+' + added + ' added</span>' +
      '<span class="diff-stat diff-stat-remove">-' + removed + ' removed</span>' +
      '<span class="diff-stat diff-stat-equal">' + unchanged + ' unchanged</span>';
    els.statsBox.style.display = "flex";
  }

  els.inputA.addEventListener("input", render);
  els.inputB.addEventListener("input", render);
  els.ignoreWhitespace.addEventListener("change", render);
  els.ignoreCase.addEventListener("change", render);

  els.copyBtn.addEventListener("click", async function () {
    const text = els.diffOutput.querySelectorAll(".diff-row");
    if (!text.length) return;
    let out = "";
    text.forEach(function (row) {
      const marker = row.querySelector(".diff-marker").textContent;
      const content = row.querySelector(".diff-text").textContent;
      out += marker + " " + content + "\n";
    });
    try {
      await navigator.clipboard.writeText(out);
    } catch (err) {
      const ta = document.createElement("textarea");
      ta.value = out;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
    }
    showMascotToast("Copied!");
    celebrateSuccess(els.copyBtn);
  });

  render();
})();
