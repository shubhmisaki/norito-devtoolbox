(function () {
  const els = {
    unit: document.getElementById("unit"),
    count: document.getElementById("count"),
    startClassic: document.getElementById("startClassic"),
    asHtml: document.getElementById("asHtml"),
    output: document.getElementById("output"),
    copyBtn: document.getElementById("copyBtn"),
    regenBtn: document.getElementById("regenBtn"),
  };

  const WORDS = [
    "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit", "sed", "do",
    "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore", "magna", "aliqua", "enim",
    "ad", "minim", "veniam", "quis", "nostrud", "exercitation", "ullamco", "laboris", "nisi",
    "aliquip", "ex", "ea", "commodo", "consequat", "duis", "aute", "irure", "in", "reprehenderit",
    "voluptate", "velit", "esse", "cillum", "eu", "fugiat", "nulla", "pariatur", "excepteur",
    "sint", "occaecat", "cupidatat", "non", "proident", "sunt", "culpa", "qui", "officia",
    "deserunt", "mollit", "anim", "id", "est", "laborum", "at", "vero", "eos", "accusamus",
    "iusto", "odio", "dignissimos", "ducimus", "blanditiis", "praesentium", "voluptatum",
    "deleniti", "atque", "corrupti", "quos", "quas", "molestias", "excepturi", "sint",
    "obcaecati", "cupiditate", "provident", "similique", "culpa", "officia", "debitis",
    "rerum", "necessitatibus", "saepe", "eveniet", "voluptates", "repudiandae", "recusandae",
    "itaque", "earum", "hic", "tenetur", "sapiente", "delectus", "reiciendis", "maiores",
    "alias", "perferendis", "doloribus", "asperiores", "repellat",
  ];

  const CLASSIC_OPENER = "lorem ipsum dolor sit amet, consectetur adipiscing elit";

  function rand(min, max) { return Math.floor(Math.random() * (max - min + 1)) + min; }
  function pick() { return WORDS[rand(0, WORDS.length - 1)]; }

  function makeSentence(wordCount) {
    const words = [];
    for (let i = 0; i < wordCount; i++) words.push(pick());
    // sprinkle a comma somewhere in the middle for longer sentences
    if (wordCount > 6) {
      const commaPos = rand(2, wordCount - 3);
      words[commaPos] += ",";
    }
    let sentence = words.join(" ");
    sentence = sentence.charAt(0).toUpperCase() + sentence.slice(1) + ".";
    return sentence;
  }

  function makeParagraph(sentenceCount, forceOpener) {
    const sentences = [];
    for (let i = 0; i < sentenceCount; i++) {
      const wc = rand(6, 14);
      if (i === 0 && forceOpener) {
        let s = CLASSIC_OPENER;
        s = s.charAt(0).toUpperCase() + s.slice(1) + ".";
        sentences.push(s);
      } else {
        sentences.push(makeSentence(wc));
      }
    }
    return sentences.join(" ");
  }

  function generateWords(count, forceOpener) {
    const words = [];
    if (forceOpener) {
      words.push.apply(words, CLASSIC_OPENER.split(" "));
    }
    while (words.length < count) words.push(pick());
    return words.slice(0, count).join(" ");
  }

  function generateSentences(count, forceOpener) {
    const sentences = [];
    for (let i = 0; i < count; i++) {
      const wc = rand(6, 14);
      if (i === 0 && forceOpener) {
        sentences.push(CLASSIC_OPENER.charAt(0).toUpperCase() + CLASSIC_OPENER.slice(1) + ".");
      } else {
        sentences.push(makeSentence(wc));
      }
    }
    return sentences.join(" ");
  }

  function generateParagraphs(count, forceOpener) {
    const paragraphs = [];
    for (let i = 0; i < count; i++) {
      paragraphs.push(makeParagraph(rand(4, 7), i === 0 && forceOpener));
    }
    return paragraphs;
  }

  function render() {
    const unit = els.unit.value;
    const count = Math.max(1, Math.min(500, parseInt(els.count.value, 10) || 1));
    const forceOpener = els.startClassic.checked;
    const asHtml = els.asHtml.checked;

    if (unit === "words") {
      els.output.value = generateWords(count, forceOpener);
    } else if (unit === "sentences") {
      els.output.value = generateSentences(count, forceOpener);
    } else {
      const paragraphs = generateParagraphs(count, forceOpener);
      els.output.value = asHtml
        ? paragraphs.map(function (p) { return "<p>" + p + "</p>"; }).join("\n")
        : paragraphs.join("\n\n");
    }
  }

  els.unit.addEventListener("change", render);
  els.count.addEventListener("input", render);
  els.startClassic.addEventListener("change", render);
  els.asHtml.addEventListener("change", render);
  els.regenBtn.addEventListener("click", render);

  els.copyBtn.addEventListener("click", async function () {
    if (!els.output.value) return;
    try {
      await navigator.clipboard.writeText(els.output.value);
    } catch (err) {
      els.output.select();
      document.execCommand("copy");
    }
    showMascotToast("Copied!");
    celebrateSuccess(els.copyBtn);
  });

  render();
})();
