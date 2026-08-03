(function () {
  const els = {
    input: document.getElementById("urlInput"),
    stripParams: document.getElementById("optStripParams"),
    forceHttps: document.getElementById("optForceHttps"),
    lowercase: document.getElementById("optLowercase"),
    status: document.getElementById("status"),
    output: document.getElementById("output"),
    copyBtn: document.getElementById("copyBtn"),
  };

  const TRACKING_PARAMS = [
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "utm_id",
    "fbclid", "gclid", "msclkid", "mc_cid", "mc_eid", "igshid", "ref", "ref_src",
  ];

  function build() {
    const raw = els.input.value.trim();
    if (!raw) {
      els.output.textContent = "";
      els.status.style.display = "none";
      return;
    }
    let u;
    try {
      u = new URL(raw);
    } catch (e) {
      els.status.textContent = "That doesn't look like a full URL (needs a protocol, like https://).";
      els.status.style.display = "block";
      els.output.textContent = "";
      return;
    }
    els.status.style.display = "none";

    if (els.forceHttps.checked) u.protocol = "https:";
    if (els.stripParams.checked) {
      TRACKING_PARAMS.forEach((p) => u.searchParams.delete(p));
    }

    let href = u.toString();
    if (els.lowercase.checked) {
      // Lowercase only the protocol+host+path, leave query values and hash alone
      // (query/hash content may be case-sensitive).
      const [beforeQuery, ...rest] = href.split(/([?#])/);
      href = beforeQuery.toLowerCase() + rest.join("");
    }

    els.output.textContent = `<link rel="canonical" href="${href}" />`;
  }

  [els.input, els.stripParams, els.forceHttps, els.lowercase].forEach((el) =>
    el.addEventListener("input", build)
  );
  build();

  els.copyBtn.addEventListener("click", async () => {
    if (!els.output.textContent) return;
    try {
      await copyToClipboard(els.output.textContent);
      const I18N_C = i18nFor("common");
      showMascotToast(I18N_C.copied || "Copied!");
      celebrateSuccess(els.copyBtn);
    } catch (e) { /* clipboard unavailable, silently ignore */ }
  });
})();
