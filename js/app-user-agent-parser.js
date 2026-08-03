(function () {
  const input = document.getElementById("uaInput");
  const results = document.getElementById("resultsWrap");

  function parseBrowser(ua) {
    const checks = [
      { name: "Edge", re: /Edg\/([\d.]+)/ },
      { name: "Opera", re: /(?:OPR|Opera)\/([\d.]+)/ },
      { name: "Samsung Internet", re: /SamsungBrowser\/([\d.]+)/ },
      { name: "Vivaldi", re: /Vivaldi\/([\d.]+)/ },
      { name: "Brave", re: /Brave\/([\d.]+)/ },
      { name: "Firefox", re: /Firefox\/([\d.]+)/ },
      { name: "Internet Explorer", re: /(?:MSIE |Trident.*rv:)([\d.]+)/ },
      { name: "Edge Legacy", re: /Edge\/([\d.]+)/ },
      { name: "Chrome", re: /Chrome\/([\d.]+)/ },
      { name: "Safari", re: /Version\/([\d.]+).*Safari/ },
    ];
    for (const c of checks) {
      const m = ua.match(c.re);
      if (m) return { name: c.name, version: m[1] };
    }
    return { name: "Unknown", version: "" };
  }

  function parseEngine(ua) {
    if (/Gecko\/\d/.test(ua)) return "Gecko";
    if (/AppleWebKit/.test(ua) && /Blink|Chrome|Chromium|Edg|OPR/.test(ua)) return "Blink";
    if (/AppleWebKit/.test(ua)) return "WebKit";
    if (/Trident/.test(ua)) return "Trident";
    return "Unknown";
  }

  function parseOS(ua) {
    const checks = [
      { name: "Windows 11/10", re: /Windows NT 10\.0/ },
      { name: "Windows 8.1", re: /Windows NT 6\.3/ },
      { name: "Windows 8", re: /Windows NT 6\.2/ },
      { name: "Windows 7", re: /Windows NT 6\.1/ },
      { name: "Windows", re: /Windows NT [\d.]+/ },
      { name: "iOS", re: /(?:iPhone|iPad|iPod).*CPU (?:iPhone )?OS ([\d_]+)/ },
      { name: "macOS", re: /Mac OS X ([\d_]+)/ },
      { name: "Android", re: /Android ([\d.]+)/ },
      { name: "Chrome OS", re: /CrOS/ },
      { name: "Linux", re: /Linux/ },
    ];
    for (const c of checks) {
      const m = ua.match(c.re);
      if (m) return { name: c.name, version: m[1] ? m[1].replace(/_/g, ".") : "" };
    }
    return { name: "Unknown", version: "" };
  }

  function parseDevice(ua) {
    if (/iPad|Tablet(?!.*Mobile)/.test(ua)) return "Tablet";
    if (/Mobi|iPhone|Android.*Mobile/.test(ua)) return "Mobile";
    return "Desktop";
  }

  function render(ua) {
    if (!ua.trim()) {
      results.innerHTML = '<p class="note">Paste a User-Agent string above, or clear the box to use your own.</p>';
      return;
    }
    const browser = parseBrowser(ua);
    const engine = parseEngine(ua);
    const os = parseOS(ua);
    const device = parseDevice(ua);

    const rows = [
      ["Browser", `${browser.name}${browser.version ? " " + browser.version : ""}`],
      ["Engine", engine],
      ["Operating system", `${os.name}${os.version ? " " + os.version : ""}`],
      ["Device type", device],
    ];

    results.innerHTML = rows
      .map(
        ([label, value]) => `
      <div class="result-box" style="text-align:left; margin-bottom:10px; display:flex; justify-content:space-between; gap:12px;">
        <span class="note" style="font-weight:600;">${label}</span>
        <code>${value}</code>
      </div>`
      )
      .join("");
  }

  input.value = navigator.userAgent;
  render(input.value);
  input.addEventListener("input", () => render(input.value));
})();
