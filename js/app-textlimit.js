(function () {
  const I18N = i18nFor("app-textlimit");
  const I18N_C = i18nFor("common");
  // Real, readable English sentences instead of Lorem Ipsum: assembled in
  // random order into an exact-length passage, so the output reads like an
  // actual short piece of writing rather than word salad.
  const SENTENCE_BANK = [
    "The kettle whistled just as the rain started tapping against the window.",
    "She found an old map tucked inside the cover of a secondhand book.",
    "Morning light spilled across the kitchen table while the coffee brewed.",
    "He tightened his laces and set off down the gravel path toward the lake.",
    "A gentle breeze carried the smell of fresh bread from the corner bakery.",
    "The train pulled into the station two minutes ahead of schedule.",
    "Somewhere in the garden a cat was quietly stalking a fallen leaf.",
    "They spread the blanket under the oldest tree in the park and waited for the sun to set.",
    "The library stayed open late on Thursdays, which was always her favorite night to visit.",
    "A small crowd gathered on the pier to watch the boats come in.",
    "He scribbled the idea on a napkin before it could slip out of his head.",
    "The city looked different from the rooftop, quieter somehow, almost still.",
    "Snow had settled on the fence posts overnight, turning the yard silver.",
    "She hummed an old tune while she watered the plants on the balcony.",
    "The recipe called for more butter than anyone in the house expected.",
    "A dog barked twice in the distance, then everything went quiet again.",
    "The museum's newest exhibit traced the history of local shipbuilding.",
    "He kept a notebook of small observations from every place he traveled.",
    "The market smelled of citrus and roasted nuts on Saturday mornings.",
    "Clouds rolled in fast, and the picnic ended earlier than planned.",
    "She rearranged the bookshelf by color instead of by author, just to see how it looked.",
    "The old radio still worked, though the reception came and went with the weather.",
    "A single lamp lit the workshop where he repaired clocks on weekends.",
    "The children built a fort out of couch cushions and refused to take it apart.",
    "Wind moved through the wheat field in slow, rolling waves.",
    "The bakery's ovens ran all night before the holiday rush began.",
    "He learned to sail on a lake so small you could see both shores at once.",
    "The letter arrived three weeks late, postmarked from a town she didn't recognize.",
    "A thin layer of fog hung over the valley until well past nine.",
    "She kept the ticket stub from their first concert in an old cigar box.",
    "The garden had gone wild over the summer, but nobody seemed to mind.",
    "Streetlights flickered on one by one as the sky faded from orange to blue.",
    "The bridge had stood for over a century and still carried traffic every day.",
    "He preferred to write letters by hand, even though almost no one wrote back the same way.",
    "The bookstore cat slept in the window display, undisturbed by passersby.",
    "A warm loaf of bread sat cooling on the counter, filling the kitchen with its smell.",
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
  // Whole sentences are drawn from a shuffled, cycling copy of SENTENCE_BANK
  // (so repeated clicks produce a different passage at the same length) and
  // appended as long as they fit in full; only the one sentence that would
  // overflow the limit gets trimmed, character-precisely, to land exactly
  // on target. The result reads as an actual passage, not word salad.
  function generateText(targetLen, countSpaces) {
    if (!Number.isFinite(targetLen) || targetLen <= 0) return "";

    let pool = shuffled(SENTENCE_BANK);
    let poolIndex = 0;
    function nextSentence() {
      if (poolIndex >= pool.length) {
        pool = shuffled(SENTENCE_BANK);
        poolIndex = 0;
      }
      return pool[poolIndex++];
    }

    let text = "";
    let guard = 0;
    while (guard++ < targetLen + SENTENCE_BANK.length + 10) {
      const currentLen = countSpaces ? text.length : text.replace(/\s/g, "").length;
      if (currentLen >= targetLen) break;
      const remaining = targetLen - currentLen;
      const sep = text.length > 0 ? " " : "";
      let piece = sep + nextSentence();
      const pieceLen = countSpaces ? piece.length : piece.replace(/\s/g, "").length;

      if (pieceLen <= remaining) {
        text += piece;
        continue;
      }

      // This sentence doesn't fit whole: trim it character-precisely so the
      // total lands exactly on targetLen, same as before.
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
      text += piece;
      break;
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
    showMascotToast(I18N_C.copied || "Copied!");
    setTimeout(() => { els.copyBtn.textContent = original; }, 1200);
  });

  // Seed with a first result so the page isn't empty on load.
  generate();
})();
