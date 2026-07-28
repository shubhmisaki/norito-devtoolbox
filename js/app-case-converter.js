(function () {
  const els = {
    input: document.getElementById("textInput"),
    output: document.getElementById("textOutput"),
    buttons: document.querySelectorAll(".case-btn"),
    copyBtn: document.getElementById("copyBtn"),
  };

  function toTitleCase(s) {
    const minor = new Set(["a", "an", "the", "and", "but", "or", "for", "nor", "on", "at", "to", "from", "by", "of", "in"]);
    const words = s.toLowerCase().split(/(\s+)/);
    let firstWordSeen = false;
    return words.map((w) => {
      if (/^\s+$/.test(w) || w === "") return w;
      const isFirst = !firstWordSeen;
      firstWordSeen = true;
      if (!isFirst && minor.has(w)) return w;
      return w.charAt(0).toUpperCase() + w.slice(1);
    }).join("");
  }

  function toSentenceCase(s) {
    const lower = s.toLowerCase();
    return lower.replace(/(^\s*\w|[.!?]\s+\w)/g, (m) => m.toUpperCase());
  }

  function words(s) {
    // Splits on camelCase boundaries, and any run of non-alphanumeric
    // separators (spaces, hyphens, underscores, punctuation), giving a
    // clean word list regardless of the input's original casing style.
    return s
      .replace(/([a-z0-9])([A-Z])/g, "$1 $2")
      .split(/[^a-zA-Z0-9]+/)
      .filter(Boolean);
  }

  function toCamelCase(s) {
    const w = words(s).map((x) => x.toLowerCase());
    return w.map((x, i) => (i === 0 ? x : x.charAt(0).toUpperCase() + x.slice(1))).join("");
  }
  function toPascalCase(s) {
    return words(s).map((x) => x.charAt(0).toUpperCase() + x.slice(1).toLowerCase()).join("");
  }
  function toSnakeCase(s) {
    return words(s).map((x) => x.toLowerCase()).join("_");
  }
  function toKebabCase(s) {
    return words(s).map((x) => x.toLowerCase()).join("-");
  }
  function toConstantCase(s) {
    return words(s).map((x) => x.toUpperCase()).join("_");
  }
  function toAlternatingCase(s) {
    let flip = false;
    return s.split("").map((c) => {
      if (!/[a-zA-Z]/.test(c)) return c;
      flip = !flip;
      return flip ? c.toUpperCase() : c.toLowerCase();
    }).join("");
  }

  const CONVERTERS = {
    upper: (s) => s.toUpperCase(),
    lower: (s) => s.toLowerCase(),
    title: toTitleCase,
    sentence: toSentenceCase,
    camel: toCamelCase,
    pascal: toPascalCase,
    snake: toSnakeCase,
    kebab: toKebabCase,
    constant: toConstantCase,
    alternating: toAlternatingCase,
  };

  let activeCase = "upper";

  function apply() {
    const fn = CONVERTERS[activeCase] || CONVERTERS.upper;
    els.output.value = els.input.value ? fn(els.input.value) : "";
  }

  els.buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      activeCase = btn.dataset.case;
      els.buttons.forEach((b) => b.classList.toggle("active", b === btn));
      apply();
    });
  });
  els.input.addEventListener("input", apply);

  els.copyBtn.addEventListener("click", async () => {
    if (!els.output.value) return;
    try {
      await copyToClipboard(els.output.value);
      const original = els.copyBtn.textContent;
      els.copyBtn.textContent = "Copied!";
      setTimeout(() => { els.copyBtn.textContent = original; }, 1500);
    } catch (e) {
      els.output.select();
      document.execCommand("copy");
    }
  });
})();
