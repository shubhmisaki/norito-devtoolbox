(function () {
  const input = document.getElementById("urlInput");
  const status = document.getElementById("status");
  const results = document.getElementById("resultsWrap");

  function row(label, value) {
    return `
      <div class="result-box" style="text-align:left; margin-bottom:10px; display:flex; justify-content:space-between; gap:12px; align-items:baseline;">
        <span class="note" style="font-weight:600; white-space:nowrap;">${label}</span>
        <code style="word-break:break-all; text-align:right;">${value || "<i>(none)</i>"}</code>
      </div>`;
  }

  function render() {
    const raw = input.value.trim();
    if (!raw) {
      results.innerHTML = "";
      status.style.display = "none";
      return;
    }
    let u;
    try {
      u = new URL(raw);
    } catch (e) {
      status.textContent = "That doesn't look like a full URL (needs a protocol, like https://).";
      status.style.display = "block";
      results.innerHTML = "";
      return;
    }
    status.style.display = "none";

    let html = "";
    html += row("Protocol", u.protocol.replace(":", ""));
    html += row("Host", u.hostname);
    html += row("Port", u.port || (u.protocol === "https:" ? "443 (default)" : u.protocol === "http:" ? "80 (default)" : ""));
    html += row("Path", u.pathname);
    html += row("Hash / fragment", u.hash.replace("#", ""));
    html += row("Origin", u.origin);

    const params = Array.from(u.searchParams.entries());
    if (params.length) {
      html += `<h3 style="margin-top:16px;">Query parameters (${params.length})</h3>`;
      params.forEach(([k, v]) => {
        html += row(k, v);
      });
    }

    results.innerHTML = html;
  }

  input.addEventListener("input", render);
  render();
})();
