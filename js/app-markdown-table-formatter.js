(function () {
  const els = {
    input: document.getElementById("mdInput"),
    note: document.getElementById("formatNote"),
    output: document.getElementById("output"),
    preview: document.getElementById("renderedPreview"),
    copyBtn: document.getElementById("copyBtn"),
  };

  // Splits a table row on unescaped pipes, dropping one optional leading
  // and one optional trailing pipe first (the standard optional outer-pipe
  // syntax), and keeps \| inside a cell instead of splitting on it.
  function splitRow(line) {
    let s = line.trim();
    if (s.startsWith("|")) s = s.slice(1);
    if (s.endsWith("|") && !s.endsWith("\\|")) s = s.slice(0, -1);
    const cells = [];
    let cur = "";
    for (let i = 0; i < s.length; i++) {
      if (s[i] === "\\" && s[i + 1] === "|") {
        cur += "|";
        i++;
      } else if (s[i] === "|") {
        cells.push(cur.trim());
        cur = "";
      } else {
        cur += s[i];
      }
    }
    cells.push(cur.trim());
    return cells;
  }

  function isSeparatorRow(cells) {
    if (!cells.length) return false;
    return cells.every((c) => /^:?-{1,}:?$/.test(c.trim()));
  }

  function alignOf(cell) {
    const c = cell.trim();
    const left = c.startsWith(":");
    const right = c.endsWith(":");
    if (left && right) return "center";
    if (right) return "right";
    return "left";
  }

  function alignSeparator(align) {
    if (align === "center") return ":---:";
    if (align === "right") return "----:";
    return ":----";
  }

  function pad(s, w, align) {
    const diff = w - s.length;
    if (diff <= 0) return s;
    if (align === "right") return " ".repeat(diff) + s;
    if (align === "center") {
      const left = Math.floor(diff / 2), right = diff - left;
      return " ".repeat(left) + s + " ".repeat(right);
    }
    return s + " ".repeat(diff);
  }

  function escapeHtml(str) {
    const d = document.createElement("div");
    d.textContent = str;
    return d.innerHTML;
  }

  function format() {
    const lines = els.input.value.split("\n").map((l) => l.replace(/\r$/, "")).filter((l) => l.trim().length);
    if (!lines.length) {
      els.output.textContent = "";
      els.preview.innerHTML = "";
      els.note.style.display = "none";
      return;
    }

    const header = splitRow(lines[0]);
    let aligns, bodyLines, fellBack = false;

    if (lines.length > 1 && isSeparatorRow(splitRow(lines[1]))) {
      aligns = splitRow(lines[1]).map(alignOf);
      bodyLines = lines.slice(2);
    } else {
      aligns = header.map(() => "left");
      bodyLines = lines.slice(1);
      fellBack = true;
    }

    const body = bodyLines.map(splitRow);
    const colCount = Math.max(header.length, ...body.map((r) => r.length), aligns.length);
    while (aligns.length < colCount) aligns.push("left");
    while (header.length < colCount) header.push("");
    body.forEach((r) => { while (r.length < colCount) r.push(""); });

    const widths = header.map((h, i) => Math.max(h.length, ...body.map((r) => (r[i] || "").length), 3));

    const headerLine = `| ${header.map((h, i) => pad(h, widths[i], aligns[i])).join(" | ")} |`;
    const sepLine = `| ${widths.map((w, i) => alignSeparator(aligns[i]).padEnd(w, "-")).join(" | ")} |`;
    const bodyLinesOut = body.map((r) => `| ${r.map((c, i) => pad(c, widths[i], aligns[i])).join(" | ")} |`);

    els.output.textContent = [headerLine, sepLine, ...bodyLinesOut].join("\n");

    if (fellBack) {
      els.note.textContent = "No valid separator row (| --- | --- |) was found, so a plain left-aligned one was generated.";
      els.note.style.display = "block";
    } else {
      els.note.style.display = "none";
    }

    const alignCss = { left: "left", center: "center", right: "right" };
    els.preview.innerHTML = `<table class="compare-table"><thead><tr>${header
      .map((h, i) => `<th style="text-align:${alignCss[aligns[i]]}">${escapeHtml(h)}</th>`)
      .join("")}</tr></thead><tbody>${body
      .map((r) => `<tr>${r.map((c, i) => `<td style="text-align:${alignCss[aligns[i]]}">${escapeHtml(c)}</td>`).join("")}</tr>`)
      .join("")}</tbody></table>`;
  }

  els.input.addEventListener("input", format);
  format();

  els.copyBtn.addEventListener("click", async () => {
    if (!els.output.textContent) return;
    try {
      await copyToClipboard(els.output.textContent);
      const I18N_C = i18nFor("common");
      showMascotToast(I18N_C.copied || "Copied!");
      celebrateSuccess(els.copyBtn);
    } catch (e) { /* clipboard unavailable */ }
  });
})();
