(function () {
  const els = {
    rulesWrap: document.getElementById("rulesWrap"),
    addRuleBtn: document.getElementById("addRuleBtn"),
    sitemapUrl: document.getElementById("sitemapUrl"),
    crawlDelay: document.getElementById("crawlDelay"),
    output: document.getElementById("output"),
    copyBtn: document.getElementById("downloadBtn"),
  };

  function ruleRowHtml(agent, type, path) {
    return `<div class="field-row robots-rule">
      <div class="field" style="flex:1.2;">
        <input type="text" class="rule-agent" placeholder="User-agent (* for all)" value="${agent}" />
      </div>
      <div class="field">
        <select class="rule-type">
          <option value="Disallow" ${type === "Disallow" ? "selected" : ""}>Disallow</option>
          <option value="Allow" ${type === "Allow" ? "selected" : ""}>Allow</option>
        </select>
      </div>
      <div class="field" style="flex:1.5;">
        <input type="text" class="rule-path" placeholder="/path" value="${path}" />
      </div>
      <button type="button" class="secondary remove-rule-btn" aria-label="Remove rule">&times;</button>
    </div>`;
  }

  function addRule(agent, type, path) {
    const div = document.createElement("div");
    div.innerHTML = ruleRowHtml(agent, type, path);
    const row = div.firstElementChild;
    row.querySelectorAll("input, select").forEach((el) => el.addEventListener("input", generate));
    row.querySelector(".remove-rule-btn").addEventListener("click", () => { row.remove(); generate(); });
    els.rulesWrap.appendChild(row);
  }

  els.addRuleBtn.addEventListener("click", () => { addRule("*", "Disallow", "/"); generate(); });

  function escapeText(s) {
    return String(s || "").replace(/[\r\n]/g, "");
  }

  function generate() {
    const groups = new Map(); // agent -> array of {type, path}
    els.rulesWrap.querySelectorAll(".robots-rule").forEach((row) => {
      const agent = row.querySelector(".rule-agent").value.trim() || "*";
      const type = row.querySelector(".rule-type").value;
      const path = row.querySelector(".rule-path").value.trim();
      if (!path) return;
      if (!groups.has(agent)) groups.set(agent, []);
      groups.get(agent).push({ type, path });
    });

    const lines = [];
    for (const [agent, rules] of groups) {
      lines.push(`User-agent: ${escapeText(agent)}`);
      for (const r of rules) lines.push(`${r.type}: ${escapeText(r.path)}`);
      const delay = els.crawlDelay.value.trim();
      if (delay) lines.push(`Crawl-delay: ${escapeText(delay)}`);
      lines.push("");
    }
    if (groups.size === 0) {
      lines.push("User-agent: *", "Disallow:", "");
    }
    const sitemap = els.sitemapUrl.value.trim();
    if (sitemap) lines.push(`Sitemap: ${escapeText(sitemap)}`);

    els.output.textContent = lines.join("\n").trim() + "\n";
  }

  [els.sitemapUrl, els.crawlDelay].forEach((el) => el.addEventListener("input", generate));
  addRule("*", "Disallow", "/admin/");
  addRule("*", "Allow", "/");
  generate();

  els.copyBtn.addEventListener("click", () => {
    const blob = new Blob([els.output.textContent], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "robots.txt";
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  });
})();
