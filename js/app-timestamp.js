(function () {
  const I18N_C = i18nFor("common");

  const els = {
    tsInput: document.getElementById("tsInput"),
    tsUnit: document.getElementById("tsUnit"),
    nowBtn: document.getElementById("nowBtn"),
    localOut: document.getElementById("localOut"),
    utcOut: document.getElementById("utcOut"),
    isoOut: document.getElementById("isoOut"),
    relativeOut: document.getElementById("relativeOut"),
    dateInput: document.getElementById("dateInput"),
    secOut: document.getElementById("secOut"),
    msOut: document.getElementById("msOut"),
    copySecBtn: document.getElementById("copySecBtn"),
    copyMsBtn: document.getElementById("copyMsBtn"),
    errorBox: document.getElementById("errorBox"),
  };

  let syncing = false;

  function relativeLabel(ms) {
    const diffSec = Math.round((ms - Date.now()) / 1000);
    const abs = Math.abs(diffSec);
    const units = [
      ["year", 31536000], ["month", 2592000], ["day", 86400],
      ["hour", 3600], ["minute", 60], ["second", 1],
    ];
    for (const [name, secs] of units) {
      if (abs >= secs || name === "second") {
        const val = Math.round(abs / secs);
        const plural = val === 1 ? "" : "s";
        return diffSec >= 0 ? `in ${val} ${name}${plural}` : `${val} ${name}${plural} ago`;
      }
    }
    return "";
  }

  function renderFromTimestamp() {
    if (syncing) return;
    syncing = true;
    els.errorBox.style.display = "none";
    const raw = els.tsInput.value.trim();
    if (!raw) {
      [els.localOut, els.utcOut, els.isoOut, els.relativeOut].forEach((el) => (el.value = ""));
      syncing = false;
      return;
    }
    const num = Number(raw);
    if (!Number.isFinite(num)) {
      els.errorBox.textContent = "That doesn't look like a valid number.";
      els.errorBox.style.display = "block";
      syncing = false;
      return;
    }
    const ms = els.tsUnit.value === "s" ? num * 1000 : num;
    const d = new Date(ms);
    if (isNaN(d.getTime())) {
      els.errorBox.textContent = "That timestamp is out of range.";
      els.errorBox.style.display = "block";
      syncing = false;
      return;
    }
    els.localOut.value = d.toLocaleString(undefined, { dateStyle: "full", timeStyle: "long" });
    els.utcOut.value = d.toUTCString();
    els.isoOut.value = d.toISOString();
    els.relativeOut.value = relativeLabel(ms);

    const local = new Date(ms - d.getTimezoneOffset() * 60000);
    els.dateInput.value = local.toISOString().slice(0, 16);
    els.secOut.value = Math.floor(ms / 1000);
    els.msOut.value = Math.floor(ms);
    syncing = false;
  }

  function renderFromDate() {
    if (syncing) return;
    syncing = true;
    if (!els.dateInput.value) {
      syncing = false;
      return;
    }
    const d = new Date(els.dateInput.value);
    if (isNaN(d.getTime())) {
      syncing = false;
      return;
    }
    const ms = d.getTime();
    els.secOut.value = Math.floor(ms / 1000);
    els.msOut.value = Math.floor(ms);
    els.tsInput.value = els.tsUnit.value === "s" ? Math.floor(ms / 1000) : Math.floor(ms);
    syncing = false;
    renderFromTimestamp();
  }

  els.tsInput.addEventListener("input", renderFromTimestamp);
  els.tsUnit.addEventListener("change", renderFromTimestamp);
  els.dateInput.addEventListener("input", renderFromDate);

  els.nowBtn.addEventListener("click", () => {
    const now = Date.now();
    els.tsUnit.value = "ms";
    els.tsInput.value = now;
    renderFromTimestamp();
    celebrateSuccess(els.nowBtn);
  });

  function copyField(el, btn) {
    return async () => {
      if (!el.value) return;
      try {
        await navigator.clipboard.writeText(el.value);
      } catch (e) {
        el.select();
        document.execCommand("copy");
      }
      showMascotToast(I18N_C.copied || "Copied!");
      celebrateSuccess(btn);
    };
  }
  els.copySecBtn.addEventListener("click", copyField(els.secOut, els.copySecBtn));
  els.copyMsBtn.addEventListener("click", copyField(els.msOut, els.copyMsBtn));

  els.tsUnit.value = "ms";
  els.tsInput.value = Date.now();
  renderFromTimestamp();
})();
