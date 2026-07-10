(function () {
  const I18N = i18nFor("app-textlimit");
  const I18N_C = i18nFor("common");
  // Classic lorem-ipsum vocabulary: deliberately meaningless filler text,
  // the standard choice for placeholder/mockup copy.
  const LOREM_WORDS = [
    "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit",
    "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore",
    "magna", "aliqua", "enim", "ad", "minim", "veniam", "quis", "nostrud",
    "exercitation", "ullamco", "laboris", "nisi", "aliquip", "ex", "ea", "commodo",
    "consequat", "duis", "aute", "irure", "in", "reprehenderit", "voluptate",
    "velit", "esse", "cillum", "eu", "fugiat", "nulla", "pariatur", "excepteur",
    "sint", "occaecat", "cupidatat", "non", "proident", "sunt", "culpa", "qui",
    "officia", "deserunt", "mollit", "anim", "id", "est", "laborum",
  ];

  const PRESETS = [50, 100, 250, 1000];

  const els = {
    output: document.getElementById("textOutput"),
    limit: document.getElementById("limitInput"),
    countSpaces: document.getElementById("optCountSpaces"),
    charCount: document.getElementById("charCount"),
    wordCount: document.getElementById("wordCount"),
    generateBtn: document.getElementById("generateBtn"),
    copyBtn: document.getElementById("copyBtn"),
    presets: document.getElementById("presets"),
    result: document.getElementById("result"),
  };

  function setResult(html, state) {
    els.result.innerHTML = html;
    els.result.style.display = "block";
    els.result.classList.remove("ok", "error");
    if (state === "ok" || state === "error") els.result.classList.add(state);
  }

  function pulseHighlight(el) {
    if (!el) return;
    el.classList.remove("highlight-pulse");
    void el.offsetWidth;
    el.classList.add("highlight-pulse");
    setTimeout(() => el.classList.remove("highlight-pulse"), 1300);
  }

  function shuffled(arr) {
    const copy = arr.slice();
    for (let i = copy.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [copy[i], copy[j]] = [copy[j], copy[i]];
    }
    return copy;
  }

  // Builds filler text whose length is *exactly* targetLen, either counting
  // every character, or only non-space characters, depending on countSpaces.
  // Words are drawn from a shuffled, cycling copy of LOREM_WORDS so repeated
  // clicks produce different text at the same length.
  function generateText(targetLen, countSpaces) {
    if (!Number.isFinite(targetLen) || targetLen <= 0) return "";

    let pool = shuffled(LOREM_WORDS);
    let poolIndex = 0;
    function nextWord() {
      if (poolIndex >= pool.length) {
        pool = shuffled(LOREM_WORDS);
        poolIndex = 0;
      }
      return pool[poolIndex++];
    }

    let text = "";
    let guard = 0;
    while (guard++ < targetLen + LOREM_WORDS.length) {
      const currentLen = countSpaces ? text.length : text.replace(/\s/g, "").length;
      if (currentLen >= targetLen) break;
      const remaining = targetLen - currentLen;
      const sep = text.length > 0 ? " " : "";
      let piece = sep + nextWord();

      if (countSpaces) {
        piece = piece.slice(0, remaining);
      } else {
        let visible = 0;
        let trimmed = "";
        for (const ch of piece) {
          if (!/\s/.test(ch)) {
            if (visible >= remaining) break;
            visible++;
          }
          trimmed += ch;
        }
        piece = trimmed;
      }

      if (!piece) break;
      text += piece;
    }

    return text.charAt(0).toUpperCase() + text.slice(1);
  }

  function updateStats(text) {
    const chars = text.length;
    const nonSpaceChars = text.replace(/\s/g, "").length;
    const words = (text.trim().match(/\S+/g) || []).length;
    els.charCount.textContent = `${chars} characters (${nonSpaceChars} without spaces)`;
    els.wordCount.textContent = `${words} words`;
  }

  // userInitiated is false only for the one-time page-load seed call, so we
  // don't yank the page around with a scroll/pulse before the user has done
  // anything.
  function generate(userInitiated, triggerBtn) {
    const limit = parseInt(els.limit.value, 10);
    if (!Number.isFinite(limit) || limit <= 0) {
      setResult(I18N.err_invalid_limit || "Enter a character count of 1 or more.", "error");
      return;
    }
    const countSpaces = els.countSpaces.checked;
    const text = generateText(limit, countSpaces);
    els.output.value = text;
    updateStats(text);

    const actual = countSpaces ? text.length : text.replace(/\s/g, "").length;
    setResult(
      fmt(I18N.result_generated || "<strong>Generated exactly {n} characters</strong>", { n: actual }) +
        (countSpaces ? (I18N.spaces_included || " (spaces included).") : (I18N.spaces_excluded || " (spaces excluded from the count).")),
      "ok"
    );
    if (userInitiated) {
      els.output.scrollIntoView({ behavior: "smooth", block: "center" });
      pulseHighlight(els.copyBtn);
      celebrateSuccess(triggerBtn || els.generateBtn, els.result);
    }
  }

  els.generateBtn.addEventListener("click", () => generate(true, els.generateBtn));
  els.limit.addEventListener("keydown", (e) => {
    if (e.key === "Enter") generate(true, els.generateBtn);
  });

  PRESETS.forEach((n) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "secondary preset-btn";
    btn.textContent = fmt(I18N.preset_suffix_characters || "{n} characters", { n });
    btn.addEventListener("click", () => {
      els.limit.value = n;
      generate(true, btn);
    });
    els.presets.appendChild(btn);
  });

  els.copyBtn.addEventListener("click", async () => {
    if (!els.output.value) return;
    try {
      await navigator.clipboard.writeText(els.output.value);
    } catch (e) {
      els.output.select();
      document.execCommand("copy");
    }
    const original = els.copyBtn.textContent;
    els.copyBtn.textContent = I18N_C.copied || "Copied";
    setTimeout(() => { els.copyBtn.textContent = original; }, 1200);
  });

  // Seed with a first result so the page isn't empty on load.
  generate();
})();
