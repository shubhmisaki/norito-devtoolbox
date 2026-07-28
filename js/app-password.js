(function () {
  const I18N_C = i18nFor("common");
  const SETS = {
    upper: "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    lower: "abcdefghijklmnopqrstuvwxyz",
    numbers: "0123456789",
    symbols: "!@#$%^&*()_+-=[]{}|;:,.<>?",
  };
  const AMBIGUOUS = new Set(["0", "O", "o", "1", "l", "I", "|"]);

  const els = {
    mode: document.getElementById("mode"),
    charOptions: document.getElementById("charOptions"),
    phraseOptions: document.getElementById("phraseOptions"),
    length: document.getElementById("length"),
    lengthOut: document.getElementById("lengthOut"),
    upper: document.getElementById("optUpper"),
    lower: document.getElementById("optLower"),
    numbers: document.getElementById("optNumbers"),
    symbols: document.getElementById("optSymbols"),
    excludeAmbiguous: document.getElementById("optExcludeAmbiguous"),
    wordCount: document.getElementById("wordCount"),
    wordCountOut: document.getElementById("wordCountOut"),
    separator: document.getElementById("separator"),
    capitalize: document.getElementById("optCapitalize"),
    includeNumber: document.getElementById("optIncludeNumber"),
    output: document.getElementById("output"),
    regenBtn: document.getElementById("regenBtn"),
    copyBtn: document.getElementById("copyBtn"),
    strengthBar: document.getElementById("strengthBar"),
    strengthLabel: document.getElementById("strengthLabel"),
    entropyOut: document.getElementById("entropyOut"),
  };

  function secureRandomInt(maxExclusive) {
    // Rejection sampling over as many bytes as maxExclusive needs, so this
    // stays unbiased for any pool size: a single byte only covers 0-255,
    // which silently breaks (or infinite-loops) once maxExclusive exceeds
    // that, e.g. the ~390-word passphrase list.
    if (maxExclusive <= 0) return 0;
    const bytesNeeded = Math.max(1, Math.ceil(Math.ceil(Math.log2(maxExclusive)) / 8));
    const maxRange = 256 ** bytesNeeded;
    const limit = maxRange - (maxRange % maxExclusive);
    const buf = new Uint8Array(bytesNeeded);
    let val;
    do {
      crypto.getRandomValues(buf);
      val = 0;
      for (let i = 0; i < bytesNeeded; i++) val = val * 256 + buf[i];
    } while (val >= limit);
    return val % maxExclusive;
  }

  function pickRandom(str) {
    return str[secureRandomInt(str.length)];
  }

  function buildPool() {
    let pool = "";
    const active = [];
    if (els.upper.checked) { pool += SETS.upper; active.push(SETS.upper); }
    if (els.lower.checked) { pool += SETS.lower; active.push(SETS.lower); }
    if (els.numbers.checked) { pool += SETS.numbers; active.push(SETS.numbers); }
    if (els.symbols.checked) { pool += SETS.symbols; active.push(SETS.symbols); }
    if (els.excludeAmbiguous.checked) {
      pool = pool.split("").filter((c) => !AMBIGUOUS.has(c)).join("");
      for (let i = 0; i < active.length; i++) {
        active[i] = active[i].split("").filter((c) => !AMBIGUOUS.has(c)).join("");
      }
    }
    return { pool, active };
  }

  function generateCharPassword() {
    const { pool, active } = buildPool();
    const length = parseInt(els.length.value, 10);
    if (!pool) return { value: "", bits: 0 };

    const chars = [];
    for (let i = 0; i < length; i++) chars.push(pickRandom(pool));

    active.forEach((set) => {
      if (!set.length) return;
      const hasOne = chars.some((c) => set.includes(c));
      if (!hasOne) {
        const pos = secureRandomInt(chars.length);
        chars[pos] = pickRandom(set);
      }
    });

    const bits = length * Math.log2(pool.length || 2);
    return { value: chars.join(""), bits };
  }

  function generatePassphrase() {
    const words = (window.WORDLIST || []);
    const count = parseInt(els.wordCount.value, 10);
    if (!words.length) return { value: "", bits: 0 };

    const picked = [];
    for (let i = 0; i < count; i++) {
      let w = words[secureRandomInt(words.length)];
      if (els.capitalize.checked) w = w[0].toUpperCase() + w.slice(1);
      picked.push(w);
    }
    if (els.includeNumber.checked) {
      picked.push(String(secureRandomInt(90) + 10));
    }
    const sep = els.separator.value === "space" ? " " : els.separator.value;
    const bits = count * Math.log2(words.length) + (els.includeNumber.checked ? Math.log2(90) : 0);
    return { value: picked.join(sep), bits };
  }

  function strengthInfo(bits) {
    const I18N = i18nFor("app-password");
    if (bits < 40) return { label: I18N.strength_weak || "Weak", pct: 20, cls: "s-weak" };
    if (bits < 60) return { label: I18N.strength_fair || "Fair", pct: 45, cls: "s-fair" };
    if (bits < 90) return { label: I18N.strength_strong || "Strong", pct: 70, cls: "s-strong" };
    return { label: I18N.strength_vstrong || "Very strong", pct: 100, cls: "s-vstrong" };
  }

  function render() {
    const isPhrase = els.mode.value === "phrase";
    els.charOptions.style.display = isPhrase ? "none" : "block";
    els.phraseOptions.style.display = isPhrase ? "block" : "none";

    const result = isPhrase ? generatePassphrase() : generateCharPassword();
    els.output.value = result.value;

    const info = strengthInfo(result.bits);
    els.strengthBar.style.width = info.pct + "%";
    els.strengthBar.className = "strength-fill " + info.cls;
    els.strengthLabel.textContent = info.label;
    els.entropyOut.textContent = fmt(i18nFor("app-password").entropy_out || "~{n} bits of entropy", { n: Math.round(result.bits) });
  }

  els.length.addEventListener("input", () => {
    els.lengthOut.textContent = els.length.value;
    render();
  });
  els.wordCount.addEventListener("input", () => {
    els.wordCountOut.textContent = els.wordCount.value;
    render();
  });
  [els.mode, els.upper, els.lower, els.numbers, els.symbols, els.excludeAmbiguous,
   els.separator, els.capitalize, els.includeNumber].forEach((el) => {
    el.addEventListener("change", render);
  });
  els.regenBtn.addEventListener("click", () => {
    render();
    celebrateSuccess(els.regenBtn);
  });

  els.copyBtn.addEventListener("click", async () => {
    if (!els.output.value) return;
    try {
      await copyToClipboard(els.output.value);
    } catch (e) {
      els.output.select();
      document.execCommand("copy");
    }
    const original = els.copyBtn.textContent;
    els.copyBtn.textContent = I18N_C.copied || "Copied";
    showMascotToast(I18N_C.copied || "Copied!");
    setTimeout(() => { els.copyBtn.textContent = original; }, 1400);
  });

  render();
})();
