(function () {
  const TEMPLATES = {
    langs: {
      Node: "node_modules/\nnpm-debug.log*\nyarn-debug.log*\nyarn-error.log*\n.pnpm-debug.log*\ndist/\nbuild/\n.cache/",
      Python: "__pycache__/\n*.py[cod]\n*$py.class\n.venv/\nvenv/\nenv/\n*.egg-info/\ndist/\nbuild/\n.pytest_cache/\n.mypy_cache/",
      Java: "*.class\n*.jar\n*.war\ntarget/\n.gradle/\nbuild/\nout/",
      Go: "*.exe\n*.exe~\n*.dll\n*.so\n*.dylib\n*.test\nvendor/",
      Rust: "target/\nCargo.lock",
      "Ruby": "*.gem\n.bundle/\nvendor/bundle/\nlog/*.log\ntmp/",
      PHP: "vendor/\ncomposer.phar\n.phpunit.result.cache",
    },
    frameworks: {
      React: ".next/\nbuild/\ndist/\n.parcel-cache/",
      "Next.js": ".next/\nout/\n.vercel/",
      Vue: "dist/\n.nuxt/",
      Django: "db.sqlite3\nmedia/\nstaticfiles/\n*.pot",
      Docker: "*.pid\ndocker-compose.override.yml",
      Terraform: "*.tfstate\n*.tfstate.backup\n.terraform/\n.terraform.lock.hcl",
    },
    editors: {
      "VS Code": ".vscode/\n!.vscode/extensions.json",
      "JetBrains (IntelliJ/WebStorm/PyCharm)": ".idea/\n*.iml",
      macOS: ".DS_Store\n.AppleDouble\n.LSOverride\nIcon\r",
      Windows: "Thumbs.db\nehthumbs.db\nDesktop.ini\n$RECYCLE.BIN/",
      Linux: "*~\n.directory\n.Trash-*",
      "Env files": ".env\n.env.local\n.env.*.local",
    },
  };

  const groupEls = {
    langs: document.getElementById("giLangs"),
    frameworks: document.getElementById("giFrameworks"),
    editors: document.getElementById("giEditors"),
  };
  const output = document.getElementById("output");
  const customRules = document.getElementById("customRules");
  const copyBtn = document.getElementById("copyBtn");
  const downloadBtn = document.getElementById("downloadBtn");

  Object.entries(groupEls).forEach(([groupKey, container]) => {
    container.style.display = "flex";
    container.style.flexWrap = "wrap";
    container.style.gap = "8px 18px";
    container.style.marginBottom = "16px";
    Object.keys(TEMPLATES[groupKey]).forEach((name) => {
      const label = document.createElement("label");
      label.className = "option-row";
      label.style.flex = "0 0 auto";
      label.style.gap = "6px";
      label.innerHTML = `<input type="checkbox" data-group="${groupKey}" data-name="${name}" /> <span>${name}</span>`;
      container.appendChild(label);
    });
  });

  function dedupeLines(lines) {
    const seen = new Set();
    return lines.filter((l) => {
      const key = l.trim();
      if (!key) return true; // keep blank lines for spacing
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }

  function build() {
    const checked = Array.from(document.querySelectorAll('input[type="checkbox"][data-group]')).filter((c) => c.checked);
    const sections = [];
    checked.forEach((c) => {
      const body = TEMPLATES[c.dataset.group][c.dataset.name];
      const lines = dedupeLines(body.split("\n"));
      sections.push(`# ---- ${c.dataset.name} ----\n${lines.join("\n")}`);
    });
    const custom = customRules.value.trim();
    if (custom) sections.push(`# ---- Custom ----\n${custom}`);

    if (!sections.length) {
      output.textContent = "// Pick at least one template on the left to get started.";
      return;
    }
    output.textContent = sections.join("\n\n") + "\n";
  }

  document.querySelectorAll('input[type="checkbox"][data-group]').forEach((c) => c.addEventListener("change", build));
  customRules.addEventListener("input", build);
  build();

  copyBtn.addEventListener("click", async () => {
    if (!output.textContent || output.textContent.startsWith("//")) return;
    try {
      await copyToClipboard(output.textContent);
      const I18N_C = i18nFor("common");
      showMascotToast(I18N_C.copied || "Copied!");
      celebrateSuccess(copyBtn);
    } catch (e) { /* clipboard unavailable, silently ignore */ }
  });

  downloadBtn.addEventListener("click", () => {
    if (!output.textContent || output.textContent.startsWith("//")) return;
    downloadBlob(new Blob([output.textContent], { type: "text/plain" }), ".gitignore");
  });
})();
