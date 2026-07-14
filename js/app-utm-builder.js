(function () {
  const els = {
    baseUrl: document.getElementById("baseUrl"),
    source: document.getElementById("utmSource"),
    medium: document.getElementById("utmMedium"),
    campaign: document.getElementById("utmCampaign"),
    term: document.getElementById("utmTerm"),
    content: document.getElementById("utmContent"),
    output: document.getElementById("output"),
    copyBtn: document.getElementById("copyBtn"),
    result: document.getElementById("result"),
  };

  function setResult(html, state) {
    if (!html) { els.result.style.display = "none"; return; }
    els.result.innerHTML = html;
    els.result.style.display = "block";
    els.result.classList.remove("ok", "error");
    if (state) els.result.classList.add(state);
  }

  function build() {
    const base = els.baseUrl.value.trim();
    if (!base) {
      els.output.textContent = "";
      setResult(null);
      return;
    }

    let url;
    try {
      url = new URL(base);
    } catch (e) {
      els.output.textContent = "";
      setResult("<strong>Enter a full URL</strong>, including https://", "error");
      return;
    }

    const params = [
      ["utm_source", els.source.value.trim()],
      ["utm_medium", els.medium.value.trim()],
      ["utm_campaign", els.campaign.value.trim()],
      ["utm_term", els.term.value.trim()],
      ["utm_content", els.content.value.trim()],
    ];
    for (const [key, value] of params) {
      if (value) url.searchParams.set(key, value);
      else url.searchParams.delete(key);
    }

    els.output.textContent = url.toString();
    setResult(null);
  }

  [els.baseUrl, els.source, els.medium, els.campaign, els.term, els.content].forEach((el) =>
    el.addEventListener("input", build)
  );
  build();

  els.copyBtn.addEventListener("click", async () => {
    if (!els.output.textContent) return;
    try {
      await navigator.clipboard.writeText(els.output.textContent);
      const original = els.copyBtn.textContent;
      els.copyBtn.textContent = "Copied!";
      setTimeout(() => { els.copyBtn.textContent = original; }, 1500);
    } catch (e) { /* clipboard unavailable, silently ignore */ }
  });
})();
