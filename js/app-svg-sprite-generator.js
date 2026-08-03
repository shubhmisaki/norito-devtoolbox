(function () {
  const els = {
    drop: document.getElementById("drop"),
    fileInput: document.getElementById("fileInput"),
    list: document.getElementById("batchList"),
    status: document.getElementById("status"),
    previewHeading: document.getElementById("previewHeading"),
    iconPreview: document.getElementById("iconPreview"),
    output: document.getElementById("output"),
    copyBtn: document.getElementById("copyBtn"),
    downloadBtn: document.getElementById("downloadBtn"),
  };

  let icons = []; // [{ file, id, viewBox, inner, status }]

  function escapeHtml(str) {
    const d = document.createElement("div");
    d.textContent = str;
    return d.innerHTML;
  }

  function slugify(name) {
    const base = name.replace(/\.[^.]+$/, "");
    return base
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "") || "icon";
  }

  function uniqueId(base, taken) {
    if (!taken.has(base)) return base;
    let n = 2;
    while (taken.has(`${base}-${n}`)) n++;
    return `${base}-${n}`;
  }

  function parseSvg(text) {
    const doc = new DOMParser().parseFromString(text, "image/svg+xml");
    if (doc.querySelector("parsererror")) throw new Error("Not valid SVG markup.");
    const root = doc.documentElement;
    if (root.nodeName.toLowerCase() !== "svg") throw new Error("Root element isn't <svg>.");
    let viewBox = root.getAttribute("viewBox");
    if (!viewBox) {
      const w = parseFloat(root.getAttribute("width")) || 24;
      const h = parseFloat(root.getAttribute("height")) || 24;
      viewBox = `0 0 ${w} ${h}`;
    }
    return { viewBox, inner: root.innerHTML.trim() };
  }

  function renderList() {
    els.list.innerHTML = icons
      .map((ic, i) => {
        const statusHtml =
          ic.status === "ok"
            ? `<span class="bf-status ok">${escapeHtml(ic.id)}</span>`
            : `<span class="bf-status error">Failed</span>`;
        return `<div class="batch-file-row" data-idx="${i}">
          <span class="bf-name">${escapeHtml(ic.file.name)}</span>
          <span class="bf-meta">${formatBytes(ic.file.size)}</span>
          ${statusHtml}
          <button type="button" class="bf-remove" aria-label="Remove">&times;</button>
        </div>`;
      })
      .join("");
    els.list.style.display = icons.length ? "flex" : "none";
    els.list.querySelectorAll(".bf-remove").forEach((btn) => {
      btn.addEventListener("click", () => {
        const idx = Number(btn.closest(".batch-file-row").dataset.idx);
        icons.splice(idx, 1);
        renderList();
        build();
      });
    });
  }

  function build() {
    const ok = icons.filter((ic) => ic.status === "ok");
    if (!ok.length) {
      els.output.textContent = "";
      els.iconPreview.innerHTML = "";
      els.previewHeading.style.display = "none";
      return;
    }
    els.previewHeading.style.display = "block";

    const symbols = ok
      .map((ic) => `  <symbol id="${ic.id}" viewBox="${ic.viewBox}">${ic.inner}</symbol>`)
      .join("\n");
    const sprite = `<svg xmlns="http://www.w3.org/2000/svg" style="display:none">\n${symbols}\n</svg>`;
    els.output.textContent = sprite;

    els.iconPreview.innerHTML = ok
      .map(
        (ic) => `<div style="text-align:center; width:64px;">
        <svg viewBox="${ic.viewBox}" style="width:32px; height:32px; display:block; margin:0 auto 4px; color:var(--text);" fill="currentColor" stroke="currentColor">${ic.inner}</svg>
        <span class="note" style="font-size:11px; word-break:break-all;">#${escapeHtml(ic.id)}</span>
      </div>`
      )
      .join("");
  }

  async function addFiles(fileList) {
    const accepted = Array.from(fileList).filter(
      (f) => /\.svg$/i.test(f.name) || /svg/i.test(f.type)
    );
    if (!accepted.length) {
      els.status.textContent = "Those don't look like .svg files.";
      els.status.style.display = "block";
      return;
    }
    els.status.style.display = "none";

    const taken = new Set(icons.map((ic) => ic.id));
    for (const file of accepted) {
      const text = await file.text();
      const id = uniqueId(slugify(file.name), taken);
      try {
        const { viewBox, inner } = parseSvg(text);
        taken.add(id);
        icons.push({ file, id, viewBox, inner, status: "ok" });
      } catch (e) {
        icons.push({ file, id, viewBox: "", inner: "", status: "error" });
      }
    }
    renderList();
    build();
  }

  els.fileInput.addEventListener("change", () => addFiles(els.fileInput.files));
  wireDragDrop(els.drop, (e) => addFiles(e.dataTransfer.files));
  els.drop.addEventListener("click", (e) => {
    if (e.target === els.fileInput) return;
    els.fileInput.click();
  });

  els.copyBtn.addEventListener("click", async () => {
    if (!els.output.textContent) return;
    try {
      await copyToClipboard(els.output.textContent);
      const I18N_C = i18nFor("common");
      showMascotToast(I18N_C.copied || "Copied!");
      celebrateSuccess(els.copyBtn);
    } catch (e) { /* clipboard unavailable */ }
  });

  els.downloadBtn.addEventListener("click", () => {
    if (!els.output.textContent) return;
    downloadBlob(new Blob([els.output.textContent], { type: "image/svg+xml" }), "sprite.svg");
  });
})();
